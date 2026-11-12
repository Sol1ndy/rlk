#!/usr/bin/env python3
"""knsim.py: the 아를레키노 (chapter-4 boss) test world of the ar suites (scratch tool, never shipped).

Built on vendored, unchanged copies of scratchpad az/tests_cm/lib (cmsim -> azsim -> fgsim -> mcsim; md5 in ../README.md).
S1 needs (test_cm_ar.py):

- `variant_ar(dp, ...)`: a temporary copy of the tree (cmsim.variant: generated folders and tools/ copied, the rest hard
  links) with the D0 `arlecchino` entry forced on (`enabled:true`, `route` as asked), regenerated (core, arena, cboss
  rooms) and, when the module is not in the tree yet (before S3 / I1), a STUB module written into the copy's
  F:boss/arlecchino/** (the 17 hooks + prep + test/help: a husk body through mboss/cb/body at the arena centre, a 20-t
  intro, the floor of phase 1 at 1 HP above 0, then repool 36 % / title / music 2 / floor 0, test ids 10 lose, 11 floor
  hit, 12 a bol disc, 13 a bol projectile). It only exercises the framework (FN-3); nothing of it is shipped.
- `ar_fight(s, chapter)`: cmsim.fight for `arlecchino`.
- small readers (`fake_names`, `ent_scores`) for the FN-1 "no new names" checks.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import cmsim as M  # noqa: E402

BID = 'arlecchino'
ROOT = 'boss/arlecchino'
FN1_NAMES = ('#hzBol', '#pjBol', '#mbBolIn', '#mbBolRe', '#mbHitBol')

STUB = {
    'spawn': ['# STUB (knsim): the chapter body at the arena centre facing south, phase 1.',
              'execute positioned 760 201 8 rotated 0 0 run function rlk:mboss/cb/body',
              'scoreboard players set #knStubPh mb 1'],
    'intro_tick': ['# STUB: a 20-t intro, then the fight (music phase 1, the phase-1 floor).',
                   'execute if score #mbT mb matches 20.. run function rlk:boss/arlecchino/start_fight'],
    'start_fight': ['function rlk:mboss/intro_end', 'function rlk:mboss/music/set {ph:1}',
                    'scoreboard players set #mbFloor mb 1'],
    'tick': ['# STUB: the phase switch on the floor hit.',
             'execute if score #knStubPh mb matches 1 if score #mbFloorHit mb matches 1 run function rlk:boss/arlecchino/phase2'],
    'phase2': ['scoreboard players set #knStubPh mb 2', 'scoreboard players set #mbFloor mb 0',
               'scoreboard players set #mbFloorHit mb 0', 'function rlk:mboss/repool {pct:36}',
               'function rlk:mboss/title {title:"두 세계 불의 잔재",sub:"페르엘",color:"#C8102E"}',
               'function rlk:mboss/music/set {ph:2}'],
    'on_hit': ['scoreboard players add #knStubHits mb 1'],
    'aux_hit': [], 'incoming': [], 'pause': ['scoreboard players add #knStubPause mb 1'],
    'resume': ['scoreboard players add #knStubResume mb 1'], 'death_start': ['scoreboard players set #knStubDeath mb 1'],
    'death_tick': [], 'cleanup': ['scoreboard players set #knStubPh mb 0'],
    'reload': ['scoreboard players add #knStubReload mb 1'], 'bars': [], 'hz_vis': [], 'pj_end': [],
    'uninstall': [],
    'test': ['$scoreboard players set #knStubReq mb $(id)',
             'execute if score #knStubReq mb matches 10 as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run function rlk:mboss/cb/lose',
             'execute if score #knStubReq mb matches 11 run scoreboard players set #mbFloorHit mb 1',
             'scoreboard players set #knStubReq mb 0'],
    'test/help': ['function rlk:help/head {cmd:"/function rlk:boss/test/pattern {id:…}",what:"아를레키노 시험 번호 (STUB)"}'],
    'prep': ['# STUB prep (@s = the kind-9 zone marker): the gate texts (api.GATE_LINES).',
             'data modify storage rlk:mboss cprep.arlecchino.gate set value {item:"minecraft:netherite_hoe",model:"minecraft:netherite_hoe",'
             'item2:"minecraft:netherite_hoe",model2:"minecraft:netherite_hoe",l1:{text:"추억: 빛과 그림자의 결별",color:"#E0303A",bold:true},'
             'l2:{text:"「아를레키노」",color:"#D0D0D0",bold:false},l3:{text:"영락한 폐허",color:"#A8A8A8",bold:false},n:12}',
             'data modify storage rlk:mboss cprep.arlecchino.title set value {text:"「아를레키노」",color:"#E0303A",bold:true}',
             'data modify storage rlk:mboss cprep.arlecchino.sub set value {text:"우인단 집행관 서열 4위",color:"#E8E2D0"}'],
}


def module_present(dp):
    return (Path(dp) / f'data/rlk/function/{ROOT}/spawn.mcfunction').exists()


def write_stub(root):
    f = Path(root) / f'data/rlk/function/{ROOT}'
    for name, lines in STUB.items():
        p = f / (name + '.mcfunction')
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def variant_ar(dp, route=True, edit=None, label='ar'):
    """The tree with arlecchino enabled (and routed when `route`), regenerated; a stub module when the tree has none.
    Returns (root, stubbed). Remove with M.drop_variant(root)."""
    stubbed = not module_present(dp)

    def ed(reg):
        b = M.entry(reg, BID)
        b['enabled'] = True
        b['route'] = bool(route)
        if edit:
            edit(reg)
    root = M.variant(dp, ed, label=label, gens=())
    if stubbed:
        write_stub(root)
    import subprocess
    for g in ('build_mboss_core', 'build_mboss_arena', 'build_cboss_rooms'):
        r = subprocess.run([sys.executable, f'tools/{g}.py'], cwd=root, capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f'{g} failed in the variant: {r.stdout[-500:]}{r.stderr[-1500:]}')
    return root, stubbed


def ar_fight(s, chapter=4, limit=2500):
    return M.fight(s, BID, chapter, limit)


def fake_names(s, names=FN1_NAMES, obj='mb'):
    return {n: s.sc(n, obj) for n in names if s.sc(n, obj) is not None}


def ent_scores(s, obj):
    return {e.id: s.sc(('e', e.id), obj) for e in s.ents if e.alive and s.sc(('e', e.id), obj) is not None}


def registry(dp):
    return json.loads((Path(dp) / 'tools/mboss_registry.json').read_text(encoding='utf-8'))
