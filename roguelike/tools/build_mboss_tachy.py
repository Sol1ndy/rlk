#!/usr/bin/env python3
"""타키 (Tachy) special-boss module generator (plan S:tk/PLAN.md, contract S:tk/contract.md; OWNER: S3).

    python3 tools/build_mboss_tachy.py

Registry entry: tools/mboss_registry.json id "tachy", n 20, kind special, fn boss/tachy, arena tk_lift. Writes
F:boss/tachy/** through three api.Writer owners (stale files are deleted only inside each owner's prefixes):
  S3      api.OWN['S3']: the 17 hooks, init, core/ ai/ el/ mantle/ hud/ test/ rig_stub/, p/{a1,b1,b2,b3,c1,c2,c3}/
          (tools/mboss_tachy/{core,ai,elem,p_melee,s3lib}.py)
  S4      api.OWN['S4']: p/{k,w1,w2,l,mantle}/ from tools/mboss_tachy/{p_air,p_mantle}.py PATTERNS
  S2seq   api.OWN['S2seq']: seq/ from tools/mboss_tachy/seq.py SERVICES
Never touched: rig/** (tools/build_tachy_rig.mjs, S2) and the kit's fx/** (tools/build_mboss_tk_fx.py, S1K). Missing
stages degrade gracefully: no S2 manifest -> rig_stub/** (api.rig points there); no kit manifest -> api.K lines are empty
(vanilla stand-in particles / sounds); an absent S4 pattern is never picked; an absent S2 sequence runs the core stand-in.

Generator order: build_mboss_core.py -> build_mboss_arena.py -> (rig, kit) -> this -> check_mboss_pack.py. Running it twice
gives the same bytes.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from mboss_tachy import api, core, ai, elem, p_melee, p_air, p_mantle, seq  # noqa: E402
from mboss_tachy import s3lib as S  # noqa: E402

W3 = api.Writer('S3', api.OWN['S3'])
W4 = api.Writer('S4', api.OWN['S4'])
W2 = api.Writer('S2seq', api.OWN['S2seq'])


def has(Wr, rel):
    return (api.L.FN / f'{api.ROOT}/{rel}.mcfunction').resolve() in Wr.out.written


def main():
    api.rig_manifest()                                   # S2's manifest (or the D0 stub) must match the contract
    pats = []
    for mod, Wr, keys in ((p_melee, W3, api.MELEE), (p_air, W4, api.AIR), (p_mantle, W4, api.MANTLE)):
        for p in mod.PATTERNS:
            assert p.key in keys, f'{mod.__name__}: pattern {p.key} is not one of {keys}'
            assert p.tid == S.TID[p.key], f'{p.key}: tid {p.tid} != the test id {S.TID[p.key]}'
            p.build(Wr)
            need = ('feather', 'nova/start', 'nova/tick', 'nova/cancel', 'cancel') if p.key == 'mantle' else ('start', 'tick', 'cancel')
            for f in need:
                assert has(Wr, f'p/{p.key}/{f}'), f'{mod.__name__}: pattern {p.key} wrote no p/{p.key}/{f}'
            pats.append(p)
    keys = [p.key for p in pats]
    assert len(keys) == len(set(keys)), keys
    for s in seq.SERVICES:
        assert s.name in api.SEQS and s.clip in api.CLIPS, (s.name, s.clip)
        s.build(W2)
        for f in ('start', 'tick', 'cancel'):
            assert has(W2, f'seq/{s.name}/{f}'), f'seq.py: service {s.name} wrote no seq/{s.name}/{f}'
    ctx = core.Ctx(pats, W4, seq.SERVICES)
    elem.build(W3, ctx)
    ai.build(W3, ctx)
    core.build(W3, ctx)
    for h in api.L.HOOKS + api.L.HELP_HOOKS + ['init']:
        assert has(W3, h), f'hook {h} missing'
    removed = W3.clean() + W4.clean() + W2.clean()
    n3, n4, n2 = len(W3.out.written), len(W4.out.written), len(W2.out.written)
    miss = [k for k in api.MELEE + api.AIR + api.MANTLE if k not in keys]
    print(f'mboss tachy: {n3 + n4 + n2} functions (S3 {n3}, S4 {n4}, seq {n2}); patterns {", ".join(keys)}; '
          f'{removed} stale removed.')
    notes = []
    if miss:
        notes.append('patterns not present yet (never picked): ' + ', '.join(miss))
    stand = [n for n in api.SEQS if n not in {s.name for s in seq.SERVICES}]
    if stand:
        notes.append('stand-in sequences (core/sq): ' + ', '.join(stand))
    if not api.rig_real():
        notes.append('rig: stand-in rig_stub/** (tools/tachy_rig_manifest.json missing)')
    if not api.K._on():
        notes.append('kit: missing (tools/mboss_tk_fx_manifest.json): vanilla stand-in particles / sounds')
    if not api.arena_ready():
        notes.append('arena tk_lift: not in the registry yet (no look job calls)')
    for n in notes:
        print('  note: ' + n)


main()
