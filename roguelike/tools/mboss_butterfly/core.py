"""Moonlit Illusion Butterfly core: hooks, the form state machine (entrance, human rotation, transformation,
butterfly rotation, 달빛 해제, revert, groggy, turn and chain re-form), the shuffle bags, locomotion, the per-form
hitbox, the wing element looks, the Burning weakness, 달빛 고치 and its reward, the 달빛 이슬 heal orbs, death,
HUD, tests and the generated pattern dispatchers. See __init__.py for the package layout and the scratchpad file
mb2/bf_contract.md for the core <-> pattern contract.

Owns F:mboss/butterfly/** except F:mboss/butterfly/rig/** (the rig generator) and the fx kit's paths (tools/
build_mboss_bf_fx.py: fx/{card,cardx,look,clear,uninstall} and fx/{e,p,tele,snd,hud,prop,test}/**, listed under
"owned" in tools/mboss_bf_fx_manifest.json). Every file it owns is deleted and rewritten on each run
(F:mboss/butterfly/rig_stub/ too: it exists only while api.STUB). Every visual of the core goes through the fx kit
(api.K / Gen.fx, snd, kcard, khud, kprop; scratchpad mb2/bf_fx_api.md), plus plain vanilla particles.
"""
import importlib
import json
import math

from . import PATTERN_MODULES
from . import api as A
from .api import L, K, Gen, TL, ev_or, clip_len, DMG, KB, CX, CY, CZ

NS = A.NS
OWN_TOP = 'mboss/' + A.ID

# ---------------------------------------------------------------------------------------------
# Tunables (plan.md "Forms and rotation", "Debuff 달빛 고치")
GROGGY = 300                                  # 15 s after 달빛 해제 (the Guardian's is 220)
TURN_T = clip_len('turn_h')                   # 24: she turns to face the player
CHAIN_T = clip_len('chain_reform')            # 18: the crescent chain re-forms
HUM_FIRST_T, HUM_FIRST_N = 600, 5             # first human stretch: 600 t of fight or 5 patterns, whichever first
HUM_NEXT_N = 4                                # after each groggy: 4 human patterns
FIRST_AFTER_GROGGY = 2                        # the video goes straight into H2 after the groggy
BF_N, BF_T = (4, 5), 900                      # butterfly form: 4-5 patterns or 900 t, then 달빛 해제
LOOK_LEAD = 8                                 # a wing element switch happens this many ticks before the pattern
INTRO_CLIP = 1                                # intro tick of the entrance clip's tick 0 (played in intro/setup)
ENT_LEN = clip_len('entrance')
ENT_BURST = ev_or('entrance', 'burst', 79)
ENT_LAND = ev_or('entrance', 'land', 90)
ENT_GLOW = ev_or('entrance', 'glow', ENT_BURST - 18)
ENT_WHITE = ev_or('entrance', 'whiteout', ENT_BURST - 8)
NAMEPLATE = 57                                # the video's fight trigger (nameplate) on the cocoon timeline
INTRO_DONE = INTRO_CLIP + ENT_LEN + 1         # she stands; the fight starts
TR_LEN = clip_len('transform')
TR_OPEN = ev_or('transform', 'open', 4)
TR_SPHERE = ev_or('transform', 'sphere', 6)   # 달빛 고치 lands with the light sphere
TR_RINGS = ev_or('transform', 'rings', TR_SPHERE + 2)
RL_LEN = clip_len('release')
RL_DET = ev_or('release', 'detonation', 53)
RL_FLAT = ev_or('release', 'flat', RL_DET + 34)
RL_REVERT = ev_or('release', 'revert', RL_DET + 39)
DEATH_LEN = clip_len('death')
D_SHATTER = ev_or('death', 'shatter', 6)
D_KNEEL = ev_or('death', 'kneel', 24)
D_DISSOLVE = ev_or('death', 'dissolve', 40)
HIT_H, SCALE_H = (A.BOSS['hit']['w'], A.BOSS['hit']['h']), A.BOSS['scale']   # human form = the registry
HIT_B, SCALE_B = (2.2, 4.4), 1.8              # butterfly form: hovering toes at +1.2 b, the body still on the floor
DEW_GLOW = int(A.LIME_HEX[1:], 16)
assert INTRO_DONE <= A.BOSS['intro'], (INTRO_DONE, A.BOSS['intro'])
assert DEATH_LEN <= A.BOSS['death'], (DEATH_LEN, A.BOSS['death'])
assert TR_OPEN <= TR_SPHERE < TR_LEN and RL_DET < RL_FLAT < RL_REVERT <= RL_LEN

ST = {'idle': 0, 'pattern': 1, 'close': 2, 'groggy': 3, 'recover': 4, 'prep': 5, 'dead': 7}
EL_BU = {A.EL_PYRO: 2, A.EL_DENDRO: 7}

# The transformation is a core service pattern (its mechanics and its fx belong to the core).
TRANSFORM = A.Pattern(20, 'transform', '변신', 'h', 'transform', kind='service', recover=0,
                      max_len=TR_LEN + 4, length=TR_LEN)


def build():
    out = L.Out()
    g = Gen(out)
    pats = []
    for name in PATTERN_MODULES:
        mod = importlib.import_module(f'{__package__}.{name}')
        for p in mod.PATTERNS:
            p.module = name
        pats.extend(mod.PATTERNS)
        mod.emit(g)
    TRANSFORM.module = 'core'
    pats.append(TRANSFORM)
    ids = [p.id for p in pats]
    assert len(set(ids)) == len(ids), ids
    keys = [p.key for p in pats]
    assert len(set(keys)) == len(keys), keys
    for need, form in ((1, 'h'), (2, 'h'), (3, 'h'), (4, 'h'), (11, 'b'), (12, 'b'), (13, 'b'), (14, 'b'), (15, 'b')):
        p = next((x for x in pats if x.id == need), None)
        assert p is not None, f'pattern id {need} missing'
        assert p.form == form, (need, p.form)
    assert next(p for p in pats if p.id == 15).kind == 'service'
    assert all(p.id in range(1, 5) or p.form == 'b' or p.id == 20 for p in pats)
    core = Core(g, pats)
    core.emit()
    from . import seq_h                         # [seq_h: human author] S1 / S3 / S4 visuals (seq_h/**), called by the hooks
    seq_h.emit(g)
    for p in pats:
        for f in ('start', 'tick', 'cancel'):
            assert g.has(f'p/{p.key}/{f}'), f'{p.module}: pattern {p.key} has no {f}'
    if A.STUB:
        from . import stub_rig
        stub_rig.emit(g)
    removed = clean(out)
    normal = [p for p in pats if p.kind == 'normal']
    print(f'mboss butterfly: {len(g.files)} functions ({len(normal)} normal + {len(pats) - len(normal)} service patterns '
          f'from {", ".join(PATTERN_MODULES)} + core), {removed} stale removed, rig '
          f'{"STUB (" + A.MANIFEST.name + ")" if A.STUB else A.MANIFEST.name}.')
    for clip, event, default in sorted(set(A.FALLBACKS)):
        print(f'  note: manifest clip {clip} has no event {event!r}; using tick {default}')


def foreign():
    """Paths under F:mboss/butterfly/ that other generators own (relative, no extension): the rig generator's rig/
    and the fx kit's owned dirs / files (tools/mboss_bf_fx_manifest.json "owned", united with the kit's own
    constants so a stale manifest never exposes a kit file). Returns (dirs, files)."""
    dirs, files = {'rig'}, set()
    pre = f'data/rlk/function/{OWN_TOP}/'
    man = A._TOOLS / 'mboss_bf_fx_manifest.json'
    if man.exists():
        own = json.loads(man.read_text(encoding='utf-8')).get('owned', {})
        dirs |= {d[len(pre):] for d in own.get('dirs', []) if d.startswith(pre)}
        files |= {f[len(pre):-len('.mcfunction')] for f in own.get('files', []) if f.startswith(pre)}
    kfx = K.FDIR[len('data/rlk/function/' + OWN_TOP + '/'):]
    dirs |= {f'{kfx}/{d}' for d in K.OWNED_DIRS}
    files |= {f'{kfx}/{f}' for f in K.OWNED_FILES}
    return dirs, files


def is_foreign(rel, dirs, files):
    """rel: path under F:mboss/butterfly/ (posix, without .mcfunction for files)."""
    return rel in files or any(rel == d or rel.startswith(d + '/') for d in dirs)


def clean(out):
    """Owned: every file under F:mboss/butterfly/ except the rig generator's rig/ and the fx kit's paths (foreign())."""
    root = L.FN / OWN_TOP
    dirs, files = foreign()
    removed = 0
    for p in sorted(root.rglob('*.mcfunction')):
        rel = p.relative_to(root).with_suffix('').as_posix()
        if is_foreign(rel, dirs, files):
            assert p.resolve() not in out.written, f'the butterfly core wrote into a foreign path: {rel}'
            continue
        if p.resolve() not in out.written:
            p.unlink()
            removed += 1
    for p in sorted(root.rglob('*'), reverse=True):
        rel = p.relative_to(root).as_posix()
        if p.is_dir() and not is_foreign(rel, dirs, files) and not any(p.iterdir()):
            p.rmdir()
    return removed


# ---------------------------------------------------------------------------------------------
def sc_set(name, v):
    return f'scoreboard players set {name} mb {int(v)}'


def sc_set_if(cond, v, name, val):
    return f'execute if score {cond} mb matches {v} run scoreboard players set {name} mb {int(val)}'


def sc_set_bu(name, v):
    return f'scoreboard players set {name} bu {int(v)}'


def at_t(clock, t, cmd):
    rng = f'{t[0]}..{t[1]}' if isinstance(t, tuple) else str(t)
    return f'execute if score {clock} mb matches {rng} run {cmd}'


def ring(g, rgb, r, n, y='0.15', scale=1.0, cnt=1):
    """Dust points on a horizontal circle of radius r around the execution position (rotation-free)."""
    out = []
    for i in range(n):
        a = 360 * i / n
        x, z = r * math.sin(math.radians(a)), r * math.cos(math.radians(a))
        out.append(g.dust(rgb, scale, f'~{L.num(x, 2)} ~{y} ~{L.num(z, 2)}', (0, 0, 0), cnt))
    return out


HUM_HEX, BF_HEX = '#C8E6A0', A.LIME_HEX


class Core:
    def __init__(self, g, pats):
        self.g, self.pats = g, pats
        self.normal = [p for p in pats if p.kind == 'normal']
        self.hum = [p for p in self.normal if p.form == 'h']
        self.bfl = [p for p in self.normal if p.form == 'b']
        self.F = g.fn
        self.R = g.rig

    def w(self, rel, lines):
        self.g.w(rel, lines)

    def pat(self, pid):
        return next(p for p in self.pats if p.id == pid)

    # =========================================================================================
    def emit(self):
        self.consts_vars()
        self.utils()
        self.hooks()
        self.intro()
        self.ai()
        self.slot()
        self.forms()
        self.transform()
        self.groggy()
        self.cocoon()
        self.dew()
        self.burn()
        self.death()
        self.hud()
        self.tests()

    # -----------------------------------------------------------------------------------------
    def consts_vars(self):
        self.w('ai/consts', ['# Module constants (spawn, reload). #bfK<n> are the moduli of Gen.every and the core\'s cycles.']
               + [sc_set(f'#bfK{n}', n) for n in (2, 3, 4, 5, 6, 8, 10, 20, 40)]
               + [sc_set('#bfCocPct', A.COCOON_HP_PCT), sc_set('#bfDewPct', A.DEW_HEAL_PCT)])
        v = ['# Every fake player of the module back to its fight-start value (spawn, cleanup; no executor).',
             '# AI state #bfSt: 0 idle 1 pattern 2 burst-run close-in 3 groggy 4 turn + chain re-form 5 wing look prep 7 dying',
             '# form #bfForm: 1 human 2 butterfly']
        v += [sc_set(k, 0) for k in ('#bfSt', '#bfT', '#bfMv', '#bfMvT', '#bfLast', '#bfPick', '#bfReq', '#bfPat', '#bfPNew',
                                      '#bfPT', '#bfPEnd', '#bfPMax', '#bfPLen', '#bfPRel', '#bfPDone', '#bfPCol', '#bfClk',
                                      '#bfFlash', '#bfTst', '#bfDist', '#bfWant', '#bfBurnQ', '#bfDewN', '#bfCocN',
                                      '#bfHumN', '#bfHumT', '#bfBfN', '#bfBfT')]
        v += [sc_set('#bfCool', 30), sc_set('#bfBand', 2), sc_set('#bfSide', 1), sc_set('#bfForm', 1),
              sc_set('#bfHumLim', HUM_FIRST_N), sc_set('#bfHumTL', HUM_FIRST_T), sc_set('#bfBfLim', BF_N[0]),
              sc_set('#bfLook', A.EL_DENDRO)]
        v += [sc_set(f'#bfBag{p.id}', 1) for p in self.normal]
        v += ['# 달빛 고치 / 달빛 축복 받음, the framework\'s player modifiers and the kit\'s HUD badges', self.F('coc/clear')]
        self.w('ai/vars', v)

    # -----------------------------------------------------------------------------------------
    def utils(self):
        g = self.g
        self.w('u/dest', [
            '# @s = body, at it. Marker rlk_mb_bf_dest on the line toward the player: at most #bfDMax tenths from her,',
            '# stopping #bfDKeep tenths short of the player, never outside the safe disc (0.5 b steps; none fits = at her',
            '# feet). Patterns keep it with tag ... add rlk_mb_bf_p<id>x + tag ... remove rlk_mb_bf_dest (Gen.keep).',
            'kill @e[type=minecraft:marker,tag=rlk_mb_bf_dest]',
            'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_dest"]}',
            'execute as @e[type=minecraft:marker,tag=rlk_mb_bf_dest,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0',
            'scoreboard players operation #bfDLeft mb = #bfDMax mb',
            f'execute as @e[type=minecraft:marker,tag=rlk_mb_bf_dest,limit=1] at @s run {self.F("u/dest_step")}'])
        self.w('u/dest_step', [
            '# @s = the dest marker, at it (rotation = toward the player): one 0.5 b step while allowed.',
            'execute if score #bfDLeft mb matches ..4 run return 0',
            'function rlk:mboss/mv/dist',
            'scoreboard players remove #mbDist mb 5',
            'execute if score #mbDist mb < #bfDKeep mb run return 0',
            'execute rotated as @s positioned ^ ^ ^0.5 unless function rlk:mboss/mv/ok run return 0',
            'execute rotated as @s run tp @s ^ ^ ^0.5',
            'scoreboard players remove #bfDLeft mb 5',
            f'execute at @s run {self.F("u/dest_step")}'])
        self.w('u/lockp', [
            '# Marker rlk_mb_bf_lock on the floor under the player\'s body, pulled inside the safe disc (any executor).',
            'kill @e[type=minecraft:marker,tag=rlk_mb_bf_lock]',
            f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_lock"]}}',
            'execute as @e[type=minecraft:marker,tag=rlk_mb_bf_lock,limit=1] run function rlk:mboss/mv/clamp'])

    # -----------------------------------------------------------------------------------------
    def hooks(self):
        F, R, g = self.F, self.R, self.g
        self.w('spawn', [
            '# Hook spawn (@s = arena marker at the centre, rotated north). The body stands on the centre facing south',
            '# (the arriving player); intro/setup builds the rig, plays the entrance (cocoon) and the cocoon prop.',
            'execute rotated 0 0 run function rlk:mboss/body',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {F("intro/setup")}'])
        self.w('tick', [
            '# Hook tick (@s = body, at @s, fight state). Order: clocks and flags, the heal orbs (a pickup heals),',
            '# heal events (any heal cures 달빛 고치), Burning, form clocks, AI state, pattern slot, then the rig (a clip',
            '# played this tick starts this tick). The fx kit ages its own cards (a self-scheduled function).',
            'scoreboard players add #bfClk mb 1',
            f'execute if score #bfFlash mb matches 1 run {R("flash")}',
            sc_set('#bfFlash', 0),
            f'execute if score #bfDewN mb matches 1.. run {F("dew/all")}',
            f'execute if score #mbHealEv mb matches 1.. run {F("coc/heal_ev")}',
            f'execute if score #bfBurnQ mb matches 1 run {F("burn/start")}',
            'execute if score #bfForm mb matches 1 run scoreboard players add #bfHumT mb 1',
            'execute if score #bfForm mb matches 2 run scoreboard players add #bfBfT mb 1',
            F('ai/state'),
            f'execute if score #bfPat mb matches 1.. run {F("p/run")}',
            R('tick')])
        self.w('on_hit', [
            '# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg #crit known). Flags and scores only.',
            '# Burning weakness (PDF): in butterfly form any Pyro (1) or Dendro (7) hit of the player (not reaction damage,',
            '# #tfm) starts or refreshes Burning in the module tick (burn/start), even without the other aura.',
            sc_set('#bfFlash', 1),
            'execute unless score #bfForm mb matches 2 run return 0',
            'execute if score #tfm tmp matches 1 run return 0',
            'execute if score #elem tmp matches 1 run scoreboard players set #bfBurnQ mb 1',
            'execute if score #elem tmp matches 7 run scoreboard players set #bfBurnQ mb 1'])
        self.w('aux_hit', ['# Hook aux_hit: the butterfly has no breakable helper objects (nothing spawns rlk_mb_hit).'])
        self.w('incoming', [
            '# Hook incoming (@s = body inside combat/apply_mods, after the level factor and mres). NO element RES of any',
            '# kind (user decision "불, 풀 내성은 없애줘"): mres stays 0 and nothing here reads #elem. Only the player\'s',
            f'# 달빛 고치 (DMG {A.COCOON_DMG} %, forced crits undone: CRIT -100 %) and 달빛 축복 받음 (DMG {A.BUFF_DMG} %), reactions included.',
            f'execute if score #bfCoc mb matches 1 if score #crit tmp matches 1 run {F("coc/uncrit")}',
            f'execute unless score #bfDmgPct mb matches 100 if score #dmg tmp matches 1.. run {F("coc/dmg")}'])
        self.w('pause', [
            '# Hook pause (the fight froze: player dead / reviving / selection screen / no body). Death ends 달빛 고치 and',
            '# 달빛 축복 받음 (plan "cleared on death"); the running pattern may drop what would hang (its optional pause).',
            '# The kit\'s ground decals go (the frozen hazards keep their framework markers; the decals would run on and',
            '# flash early), so does a kit screen flash / pop still on the title line (only while one is up: vBig, so a',
            '# selection screen\'s own title is left alone); a dead or reviving player clears the kit cards.',
            sc_set('#bfFlash', 0),
            f'function {K.FN}tele/clear',
            f'execute if entity @a[tag=player,scores={{vBig=1..}}] run {g.khud("flash_end")}',
            f'execute if entity @a[tag=player,scores={{dead=1}}] run {F("coc/clear_hud")}',
            f'execute if entity @a[tag=player,scores={{rnDie=1..}}] run {F("coc/clear_hud")}',
            F('p/pause_d')])
        self.w('resume', ['# Hook resume: nothing to restore (module timers live in the body tick and simply continue).'])
        self.w('cleanup', [
            '# Hook cleanup (no executor; idempotent; fight end, abort, run end, map change, wipe, uninstall): module',
            '# fake players back to their defaults, 달빛 고치 / 달빛 축복 받음 off, every kit card and both kit HUD badges',
            '# gone. Module entities carry rlk_mb_aux.',
            F('ai/vars'),
            f'function {K.FN}clear',
            g.khud('clear')])
        self.w('uninstall', [
            '# Hook uninstall (no executor; rlk:uninstall via the framework, for every module): the rig, its props, the',
            '# rig objectives the manifest names, the fx kit (cards, objectives bk*, storage rlk:bfkit, its scheduled',
            '# ager); the framework removes mb and the rlk_mb_aux entities.',
            R('kill'), R('prop/clear'),
            f'function {K.FN}uninstall',
            'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_dew]',
            'kill @e[tag=rlk_mb_bf_fx]']
            + [f'scoreboard objectives remove {o}' for o in A.RIG_OBJECTIVES])
        rl = [
            '# Hook reload (@s = body after /reload; every aux entity is gone: rig parts, props, heal orbs, fx).',
            '# HP is kept. A transformation past its sphere finishes into butterfly form (the cocoon was applied); a',
            '# release goes straight to the groggy in human form; a groggy goes on; otherwise idle in the same form.',
            F('ai/consts'),
            'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
            'execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
            sc_set('#bfX', 0),
            f'execute if score #bfPat mb matches 20 if score #bfPT mb matches {TR_SPHERE}.. run scoreboard players set #bfX mb 1',
            'execute if score #bfPat mb matches 15 run scoreboard players set #bfX mb 2',
            'execute if score #bfSt mb matches 4 run scoreboard players set #bfX mb 3',
            F('p/cancel'),
            sc_set('#mbNoLeash', 0), sc_set('#bfDewN', 0), sc_set('#bfMv', 0),
            'tag @s remove rlk_mb_inv',
            R('init'), R('spawn'),
            f'execute if score #bfX mb matches 1 run {F("form/set_b")}',
            f'execute if score #bfX mb matches 2 run {F("form/set_h")}',
            f'execute if score #bfForm mb matches 2 run {F("form/rig_b")}',
            f'execute if score #bfForm mb matches 1 run {F("form/rig_h")}',
            F('coc/assert'),
            f'execute if score #bfCoc mb matches 1 if score #bfForm mb matches 2 run {F("dew/spawn")}',
            f'execute if score #bfX mb matches 2 run return run {F("groggy/begin")}',
            f'execute if score #bfX mb matches 3 run return run {F("groggy/end")}',
            f'execute if score #bfSt mb matches 3 run return run {g.play("groggy_h")}',
            sc_set('#bfCool', 20),
            F('ai/enter')]
        self.w('reload', rl)
        self.w('bars', [
            '# Hook bars (@s = body, every tick in intro/fight). Under-bar: groggy = time left (green), turn + re-form =',
            '# progress (green), pattern = progress (its element colour), idle butterfly = time left of the butterfly form',
            '# (Dendro), idle human (first stretch) = time left before the transformation (gold). Text lines: hud/*.',
            'execute if score #mbSt mb matches 0 run return 0',
            f'execute if score #bfSt mb matches {ST["groggy"]} run return run {F("hud/bar_groggy")}',
            f'execute if score #bfSt mb matches {ST["recover"]} run return run {F("hud/bar_recover")}',
            f'execute if score #bfPat mb matches 1.. unless score #bfPNew mb matches 1 unless score #bfPRel mb matches 1 run return run {F("hud/bar_pattern")}',
            f'execute if score #bfForm mb matches 2 run return run {F("hud/bar_bform")}',
            f'execute if score #bfHumTL mb matches 1.. run {F("hud/bar_hform")}'])
        self.w('hz_vis', ['# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end). Visual ids = pattern id x 10 + k.',
                          F('p/vis')])
        self.w('pj_end', ['# Hook pj_end (@s = prop, #pjEv, #pjKeep preset). Routed by the prop\'s mbId (= pattern id).',
                          F('p/pj_end')])
        self.w('test', [
            '# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}). See test/help.',
            '$scoreboard players set #bfTst mb $(id)',
            'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
            f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] at @s run {F("test/run")}'])

    # -----------------------------------------------------------------------------------------
    def intro(self):
        F, R, g = self.F, self.R, self.g
        cocoon = g.prop('cocoon')
        setup = ['# @s = the new body (from the spawn hook), at it: module state, rig in the entrance clip (the cocoon), HUD.',
                 F('ai/consts'), F('ai/vars'),
                 R('init'), R('spawn'),
                 g.play('entrance')]
        if cocoon:
            setup.append(cocoon)
        setup += [F('form/hitbox_h'), F('hud/refresh'),
                  F('seq_h/entrance/setup')]       # [seq_h: human author] S1 visuals (the floor disc ...)
        self.w('intro/setup', setup)
        c = lambda t: INTRO_CLIP + t           # intro tick of entrance clip tick t
        self.w('intro_tick', [
            '# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end). The entrance clip has',
            f'# its tick t at intro tick t + {INTRO_CLIP}: cocoon over a glowing floor disc, nameplate chime ({NAMEPLATE}), glow ramp',
            f'# ({ENT_GLOW}), whiteout ({ENT_WHITE}), burst into crystal shards ({ENT_BURST}), the drop, landing ({ENT_LAND}), she stands',
            f'# ({ENT_LEN}); the fight at intro {INTRO_DONE}. No damage.',
            R('tick'),
            at_t('#mbT', c(NAMEPLATE), F('intro/name')),
            at_t('#mbT', c(ENT_BURST), F('intro/burst')),
            F('seq_h/entrance/tick'),                 # [seq_h: human author] S1 visuals and sounds on the intro clock
            at_t('#mbT', (INTRO_DONE, 999), F('intro/done'))])
        self.w('intro/name', [
            '# The video\'s fight trigger: the title on the sub-line (the star and the chime: seq_h/entrance).',
            'data modify storage rlk:mboss sub set value [{text:"달빛의 화신",color:"#D9F5A8",bold:true}]'])
        self.w('intro/burst', ['# BURST: the cocoon prop is gone (the crystal shards and the sounds: seq_h/entrance).',
                               self.R('prop/clear')])
        self.w('intro/done', [
            '# She stands: end of the untargetable intro.',
            'function rlk:mboss/intro_end',
            sc_set('#bfCool', 20),
            F('ai/enter')])

    # -----------------------------------------------------------------------------------------
    def ai(self):
        F, R, g = self.F, self.R, self.g
        self.w('ai/state', ['# @s = body. One AI state per tick (the pattern slot runs after it, see p/run).',
                            # [human author] H4: the flying vacuum blades outlive their pattern (spec Q14)
                            f'execute if score #bp4B mb matches 1.. run {F("p/vacuum/blades")}'] + [
            f'execute if score #bfSt mb matches {ST[k]} run return run {F(fn)}'
            for k, fn in (('idle', 'ai/idle'), ('close', 'ai/close'), ('groggy', 'groggy/tick'), ('recover', 'recover/tick'),
                          ('prep', 'ai/prep'))])
        self.w('ai/enter', ['# Enter idle (#bfCool set by the caller).',
                            sc_set('#bfSt', ST['idle']), sc_set('#bfT', 0), F('hud/refresh')])
        self.w('ai/idle', [f'execute if score #bfForm mb matches 2 run return run {F("ai/idle_b")}', F('ai/idle_h')])
        self.w('ai/idle_h', [
            '# @s = body, human form (grounded): track the player; walk in when far, back off at walking pace when she is',
            '# crowded, short strafing steps otherwise; decide when the cooldown is over.',
            R('face/track'),
            'execute if score #bfCool mb matches 1.. run scoreboard players remove #bfCool mb 1',
            F('ai/loco_h'),
            f'execute if score #bfCool mb matches ..0 run {F("ai/next")}'])
        self.w('ai/loco_h', [
            'scoreboard players add #bfMvT mb 1',
            '# walk in beyond 7 b, so most decisions fall in the mid band (every human pattern), not only the far one',
            f'execute unless entity @e[tag=rlk_body,distance=..7,limit=1] run return run {F("ai/walk")}',
            f'execute if entity @e[tag=rlk_body,distance=..2.2,limit=1] run return run {F("ai/backoff")}',
            F('ai/strafe')])
        self.w('ai/walk', [f'execute unless score #bfMv mb matches 1 run {F("ai/mv1")}', 'function rlk:mboss/mv/toward {d:0.15}'])
        self.w('ai/backoff', [f'execute unless score #bfMv mb matches 2 run {F("ai/mv2")}',
                              f'execute if score #bfMvT mb matches {clip_len("back_h")}.. run {F("ai/mv2")}',
                              'function rlk:mboss/mv/away {d:0.12}'])
        side = 'execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~{a} 0 positioned ^ ^ ^0.1 if function rlk:mboss/mv/ok run tp @s ~ ~ ~'
        self.w('ai/strafe', [
            '# Short strafing steps: 16 t of every 40 t (fight clock), alternating sides.',
            'scoreboard players operation #bfM mb = #bfClk mb',
            'scoreboard players operation #bfM mb %= #bfK40 mb',
            'execute if score #bfM mb matches 0 run scoreboard players operation #bfSide mb *= #cm1 mb',
            f'execute if score #bfM mb matches 0..15 run return run {F("ai/strafe_go")}',
            f'execute unless score #bfMv mb matches 0 run {F("ai/mv0")}'])
        self.w('ai/strafe_go', [f'execute unless score #bfMv mb matches 3 run {F("ai/mv3")}',
                                'execute if score #bfSide mb matches 1 run ' + side.format(a=90),
                                'execute if score #bfSide mb matches -1 run ' + side.format(a=-90)])
        self.w('ai/idle_b', [
            '# @s = body, butterfly form (she always hovers; the rig carries the height): track, keep 5-8 b (gliding',
            '# in at 0.25 b/t, out at 0.2 b/t), decide when the cooldown is over.',
            R('face/track'),
            'execute if score #bfCool mb matches 1.. run scoreboard players remove #bfCool mb 1',
            F('ai/loco_b'),
            f'execute if score #bfCool mb matches ..0 run {F("ai/next")}'])
        self.w('ai/loco_b', [
            f'execute unless entity @e[tag=rlk_body,distance=..8,limit=1] run return run {F("ai/glide_in")}',
            f'execute if entity @e[tag=rlk_body,distance=..5,limit=1] run return run {F("ai/glide_out")}',
            f'execute unless score #bfMv mb matches 0 run {F("ai/mv0")}'])
        self.w('ai/glide_in', [f'execute unless score #bfMv mb matches 4 run {F("ai/mv4")}', 'function rlk:mboss/mv/toward {d:0.25}'])
        self.w('ai/glide_out', [f'execute unless score #bfMv mb matches 5 run {F("ai/mv5")}', 'function rlk:mboss/mv/away {d:0.2}'])
        mv = {0: None, 1: 'step_h', 2: 'back_h', 3: 'step_h', 4: 'glide_b', 5: 'glide_b'}
        for m, clip in mv.items():
            lines = [f'# Locomotion mode {m} (0 stand, 1 walk, 2 back off, 3 strafe, 4 glide in, 5 glide out).', sc_set('#bfMv', m), sc_set('#bfMvT', 0)]
            if clip:
                lines.append(g.play(clip))
            else:
                lines += [f'execute if score #bfForm mb matches 1 run {g.play("idle_h")}', f'execute if score #bfForm mb matches 2 run {g.play("idle_b")}']
            self.w(f'ai/mv{m}', lines)
        self.w('ai/next', [
            '# Next action. Test request > test lock (#mbLock 1-4 human pattern only, 11-14 butterfly pattern only (after',
            '# a transformation), 15/16 form cycle only) > the form\'s rotation: human -> transformation when its stretch',
            f'# is over (first: {HUM_FIRST_T} t of fight or {HUM_FIRST_N} patterns, after a groggy {HUM_NEXT_N} patterns); butterfly -> 달빛 해제',
            f'# after {BF_N[0]}-{BF_N[1]} patterns or {BF_T} t. Only here, at a pattern boundary.',
            'execute if score #bfPat mb matches 1.. run return 0',
            f'execute unless score #bfMv mb matches 0 run {F("ai/mv0")}',
            f'execute if score #bfReq mb matches 1.. run return run {F("ai/req")}',
            f'execute if score #mbLock mb matches 1..4 run return run {F("ai/lock_h")}',
            f'execute if score #mbLock mb matches 11..14 run return run {F("ai/lock_b")}',
            f'execute if score #mbLock mb matches 15..16 run return run {F("ai/lock_cycle")}',
            f'execute if score #bfForm mb matches 2 run return run {F("ai/next_b")}',
            F('ai/next_h')])
        self.w('ai/next_h', [
            f'execute if score #bfHumN mb >= #bfHumLim mb run return run {F("form/transform_go")}',
            f'execute if score #bfHumTL mb matches 1.. if score #bfHumT mb >= #bfHumTL mb run return run {F("form/transform_go")}',
            F('ai/pick_h')])
        self.w('ai/next_b', [
            f'execute if score #bfBfN mb >= #bfBfLim mb run return run {F("form/release_go")}',
            f'execute if score #bfBfT mb matches {BF_T}.. run return run {F("form/release_go")}',
            F('ai/pick_b')])
        req = ['# A test request (#bfReq = pattern id): the form follows the pattern at once (no transformation).',
               'scoreboard players operation #bfPick mb = #bfReq mb', sc_set('#bfReq', 0),
               '# no immediate repeat after a requested pattern either (the forced H2 after the groggy)',
               'scoreboard players operation #bfLast mb = #bfPick mb']
        for p in self.pats:
            if p.form == 'b':
                req.append(f'execute if score #bfPick mb matches {p.id} if score #bfForm mb matches 1 run {F("form/now_b")}')
            elif p.id != 20:
                req.append(f'execute if score #bfPick mb matches {p.id} if score #bfForm mb matches 2 run {F("form/now_h")}')
        req.append(f'execute if score #bfPick mb matches 20 if score #bfForm mb matches 2 run {F("form/now_h")}')
        req.append(F('ai/launch'))
        self.w('ai/req', req)
        self.w('ai/lock_h', [f'execute if score #bfForm mb matches 2 run {F("form/now_h")}',
                             'scoreboard players operation #bfPick mb = #mbLock mb', F('ai/launch')])
        self.w('ai/lock_b', [f'execute if score #bfForm mb matches 1 run return run {F("form/transform_go")}',
                             'scoreboard players operation #bfPick mb = #mbLock mb', F('ai/launch')])
        self.w('ai/lock_cycle', [f'execute if score #bfForm mb matches 1 run return run {F("form/transform_go")}',
                                 F('form/release_go')])
        bands = A.BANDS
        mel, far = int(A.MELEE * 10), int(A.FAR * 10)
        for f, plist in (('h', self.hum), ('b', self.bfl)):
            cand = [f'# Candidates ({f}): in the bag, allowed in the current range band, not the last one.',
                    '# #bfC<id> = its draw weight in this band (0 = no candidate).']
            cand_any = [f'# Fallback candidates ({f}): allowed in the band (bag and last ignored).']
            for p in plist:
                cand.append(sc_set(f'#bfC{p.id}', 0))
                cand_any.append(sc_set(f'#bfC{p.id}', 0))
                for b in p.bands:
                    wt = p.weight[b]
                    cand.append(f'execute if score #bfBag{p.id} mb matches 1 if score #bfBand mb matches {bands[b]} '
                                f'unless score #bfLast mb matches {p.id} run scoreboard players set #bfC{p.id} mb {wt}')
                    cand_any.append(f'execute if score #bfBand mb matches {bands[b]} run scoreboard players set #bfC{p.id} mb {wt}')
            for lines in (cand, cand_any):
                lines.append(sc_set('#bfCn', 0))
                lines += [f'scoreboard players operation #bfCn mb += #bfC{p.id} mb' for p in plist]
            self.w(f'ai/cand_{f}', cand)
            self.w(f'ai/cand_any_{f}', cand_any)
            self.w(f'ai/refill_{f}', [f'# The {f} bag ran dry for this band: refill it with every normal pattern of the form.']
                   + [sc_set(f'#bfBag{p.id}', 1) for p in plist])
            draw = ['# #bfR = 0..#bfCn-1 (sum of the weights) -> the candidate whose weight range holds it.', sc_set('#bfPick', 0)]
            for p in plist:
                draw.append(f'execute if score #bfPick mb matches 0 if score #bfC{p.id} mb matches 1.. if score #bfR mb < #bfC{p.id} mb '
                            f'run scoreboard players set #bfPick mb {p.id}')
                draw.append(f'scoreboard players operation #bfR mb -= #bfC{p.id} mb')
            draw += [f'execute if score #bfPick mb matches {p.id} run scoreboard players set #bfBag{p.id} mb 0' for p in plist]
            self.w(f'ai/draw_{f}', draw)
            first = plist[0].id
            self.w(f'ai/pick_{f}', [
                f'# @s = body. Range-filtered, weighted shuffle bag of the {"human" if f == "h" else "butterfly"} form, no immediate repeat:',
                '# ' + ', '.join(f'{p.key} ' + '/'.join(b + (f'x{p.weight[b]}' if p.weight[b] > 1 else '') for b in p.bands) for p in plist)
                + f' (melee <= {A.MELEE} b, far >= {A.FAR} b).',
                'function rlk:mboss/mv/dist',
                'scoreboard players operation #bfDist mb = #mbDist mb',
                sc_set('#bfBand', bands['mid']),
                f'execute if score #bfDist mb matches ..{mel} run scoreboard players set #bfBand mb {bands["melee"]}',
                f'execute if score #bfDist mb matches {far}.. run scoreboard players set #bfBand mb {bands["far"]}',
                F(f'ai/cand_{f}'),
                f'execute if score #bfCn mb matches 0 run {F(f"ai/refill_{f}")}',
                f'execute if score #bfCn mb matches 0 run {F(f"ai/cand_{f}")}',
                f'execute if score #bfCn mb matches 0 run {F(f"ai/cand_any_{f}")}',
                f'execute if score #bfCn mb matches 0 run scoreboard players set #bfC{first} mb 1',
                'execute if score #bfCn mb matches 0 run scoreboard players set #bfCn mb 1',
                'execute store result score #bfR mb run random value 0..999',
                'scoreboard players operation #bfR mb %= #bfCn mb',
                F(f'ai/draw_{f}'),
                f'execute if score #bfPick mb matches 0 run scoreboard players set #bfPick mb {first}',
                'scoreboard players operation #bfLast mb = #bfPick mb',
                F('ai/launch')])
        launch = ['# #bfPick = pattern id: human melee patterns burst-run to their distance first, butterfly patterns switch',
                  '# the wing element look first (ai/prep); then the slot.']
        close = ['# @s = body, burst-running (12-16 m/s) for #bfPick: 0.7 b/t for at most 12 t, then the pattern starts.',
                 'scoreboard players add #bfT mb 1',
                 'function rlk:mboss/mv/turn {max:30}',
                 'function rlk:mboss/mv/toward {d:0.7}',
                 'scoreboard players operation #bfM mb = #bfT mb', 'scoreboard players operation #bfM mb %= #bfK2 mb',
                 'execute if score #bfM mb matches 0 run ' + g.particle('poof', '~ ~0.1 ~', (0.25, 0.02, 0.25), 0.02, 2)]
        for p in self.pats:
            if p.close:
                launch.append(f'execute if score #bfPick mb matches {p.id} unless entity @e[tag=rlk_body,distance=..{L.num(p.close)},limit=1] '
                              f'run return run {F("ai/close_begin")}')
                close.append(f'execute if score #bfPick mb matches {p.id} if entity @e[tag=rlk_body,distance=..{L.num(p.close)},limit=1] '
                             f'run return run {F("ai/go")}')
        for p in self.pats:
            if p.form == 'b':
                launch.append(f'execute if score #bfPick mb matches {p.id} run return run {F("ai/prep_begin")}')
        launch.append(F('ai/go'))
        close.append(f'execute if score #bfT mb matches 12.. run {F("ai/go")}')
        self.w('ai/launch', launch)
        self.w('ai/close', close)
        self.w('ai/close_begin', [sc_set('#bfSt', ST['close']), sc_set('#bfT', 0), sc_set('#bfMv', 0), g.play('run_h'),
                                  g.sound('entity.breeze.jump', 0.6, 1.3), g.sound('block.moss_carpet.step', 0.6, 1.0),
                                  F('hud/refresh')])
        prep = ['# @s = body, butterfly form: the wing element look of #bfPick (1 t switch), the pattern 8 t later; no switch',
                '# needed = at once.', sc_set('#bfWant', A.EL_DENDRO)]
        prep += [sc_set_if('#bfPick', p.id, '#bfWant', p.el) for p in self.pats if p.form == 'b']
        prep += [f'execute if score #bfLook mb = #bfWant mb run return run {F("ai/go")}',
                 sc_set('#bfSt', ST['prep']), sc_set('#bfT', 0), F('look/switch')]
        self.w('ai/prep_begin', prep)
        self.w('ai/prep', [
            'scoreboard players add #bfT mb 1',
            R('face/track'),
            '# Pyro patterns want 6-8 b',
            f'execute if score #bfWant mb matches {A.EL_PYRO} if entity @e[tag=rlk_body,distance=..6,limit=1] run function rlk:mboss/mv/away {{d:0.25}}',
            f'execute if score #bfT mb matches {LOOK_LEAD}.. run {F("ai/go")}'])
        go = ['# Into the pattern slot: p/run starts it this tick (pattern clock 0 = clip tick 0).',
              sc_set('#bfSt', ST['pattern']), 'scoreboard players operation #bfPat mb = #bfPick mb', sc_set('#bfPNew', 1)]
        go += [f'execute if score #bfPick mb matches {p.id} run scoreboard players add #bfHumN mb 1' for p in self.hum]
        go += [f'execute if score #bfPick mb matches {p.id} run scoreboard players add #bfBfN mb 1' for p in self.bfl]
        self.w('ai/go', go)
        rec = ['# A slot pattern finished (#bfPDone = its id): recovery before the next decision.', sc_set('#bfCool', 20)]
        rec += [sc_set_if('#bfPDone', p.id, '#bfCool', p.recover) for p in self.pats]
        rec.append(F('ai/enter'))
        self.w('ai/recover', rec)
        self.w('ai/pat_done', [
            '# From p/finish: the owner continues (unless it already moved on at the pattern\'s release).',
            'execute if score #bfPRel mb matches 1 run return 0',
            f'execute if score #bfPDone mb matches 20 run return run {F("form/transform_done")}',
            f'execute if score #bfPDone mb matches 15 run return run {F("groggy/begin")}',
            F('ai/recover')])

    # -----------------------------------------------------------------------------------------
    def slot(self):
        F, g = self.F, self.g
        begin = ['# @s = body. First tick of the slot pattern #bfPat: clock -lead (0 for most), the clip at clock 0, start.',
                 sc_set('#bfPNew', 0), sc_set('#bfPT', 0), sc_set('#bfPEnd', 0), sc_set('#bfPRel', 0), sc_set('#bfPMax', 200),
                 sc_set('#bfPLen', 200), sc_set('#bfPCol', 8)]
        begin += [sc_set_if('#bfPat', p.id, '#bfPMax', p.max_len) for p in self.pats]
        begin += ['# expected end for the progress bar (a pattern that decides a shorter run sets #bfPLen itself: g.set_len)']
        begin += [sc_set_if('#bfPat', p.id, '#bfPLen', p.length) for p in self.pats]
        begin += [sc_set_if('#bfPat', p.id, '#bfPCol', EL_BU[p.el]) for p in self.pats]
        begin += [sc_set_if('#bfPat', p.id, '#bfPT', -p.lead) for p in self.pats if p.lead]
        begin += [F('hud/refresh'),
                  f'execute if score #bfPT mb matches 0 run {F("p/clip_d")}',
                  F('p/start'), f'execute if score #bfPat mb matches 15.. run {F("p/svc")}']
        self.w('p/begin', begin)
        self.w('p/run', [
            '# @s = body. The slot: start on the tick it was picked, then tick with #bfPT = 1, 2, ... (= clip tick).',
            f'execute if score #bfPNew mb matches 1 run return run {F("p/begin")}',
            'scoreboard players add #bfPT mb 1',
            f'execute if score #bfPT mb matches 0 run {F("p/clip_d")}',
            F('p/tick'),
            '# the service patterns (15 달빛 해제, 20 transformation) carry core mechanics on their clocks',
            f'execute if score #bfPat mb matches 15.. run {F("p/svc")}',
            f'execute if score #bfPEnd mb matches 1 run return run {F("p/finish")}',
            f'execute if score #bfPT mb >= #bfPMax mb run {F("p/finish")}'])
        self.w('p/finish', [
            '# @s = body. The pattern ended (p/end or its max_len): clear the slot and tell the owner.',
            'scoreboard players operation #bfPDone mb = #bfPat mb',
            sc_set('#bfPat', 0), sc_set('#bfPEnd', 0), sc_set('#bfPT', 0),
            sc_set('#mbNoLeash', 0),
            'tag @s remove rlk_mb_inv',
            'kill @e[type=minecraft:marker,tag=rlk_mb_bf_dest]',
            'kill @e[type=minecraft:marker,tag=rlk_mb_bf_lock]',
            F('ai/pat_done'),
            sc_set('#bfPRel', 0)])
        self.w('p/end', ['# Called by a pattern (any executor): it is done; the core finishes it after this tick\'s pattern tick.',
                         sc_set('#bfPEnd', 1)])
        self.w('p/release', ['# Called by a pattern (any executor): its dangerous part is over; the owner may move on while the',
                             '# pattern finishes a harmless tail in the slot. The slot stays busy (no new decision) until p/end.',
                             sc_set('#bfPRel', 1)])
        self.w('p/cancel', [
            '# Stop the slot pattern now (tests, death, reload). Callers run rlk:mboss/lib_clear first when hazards must',
            '# go. The pattern\'s cancel runs as the caller (the body when it exists): it must use selectors, not @s.',
            f'execute if score #bfPat mb matches 1.. unless score #bfPNew mb matches 1 run {F("p/cancel_d")}',
            sc_set('#bfPat', 0), sc_set('#bfPNew', 0), sc_set('#bfPEnd', 0), sc_set('#bfPT', 0), sc_set('#bfPRel', 0),
            sc_set('#mbNoLeash', 0),
            'kill @e[type=minecraft:marker,tag=rlk_mb_bf_dest]',
            'kill @e[type=minecraft:marker,tag=rlk_mb_bf_lock]',
            'execute if score #mbSt mb matches 1 run tag @e[tag=rlk_mb_body] remove rlk_mb_inv'])
        for name, doc in (('start', 'start (clock -lead)'), ('tick', 'tick (#bfPT -lead+1 ..)'), ('cancel_d', 'cancel')):
            target = 'cancel' if name == 'cancel_d' else name
            self.w(f'p/{name}', [f'# GENERATED dispatcher: the running pattern\'s {doc}, by #bfPat.']
                   + [f'execute if score #bfPat mb matches {p.id} run return run {F(f"p/{p.key}/{target}")}' for p in self.pats])
        self.w('p/clip_d', ['# GENERATED: the running pattern\'s clip at clock 0 (the core plays it; #bfPT = clip tick).']
               + [f'execute if score #bfPat mb matches {p.id} run return run {g.play(p.clip)}' for p in self.pats])
        self.w('p/pause_d', ['# GENERATED dispatcher: the running pattern\'s optional pause (the fight just froze), by #bfPat.',
                             'execute unless score #bfPat mb matches 1.. run return 0',
                             'execute if score #bfPNew mb matches 1 run return 0']
               + [f'execute if score #bfPat mb matches {p.id} run return run {F(f"p/{p.key}/pause")}'
                  for p in self.pats if self.g.has(f'p/{p.key}/pause')])
        vis = ['# GENERATED: hz_vis events of hazards with #hzVis = pattern id x 10 + k (k 1-9), @s = hazard marker.',
               'scoreboard players operation #bfV mb = @s mbHzV', 'scoreboard players operation #bfV mb /= #c10 mb']
        vis += [f'execute if score #bfV mb matches {p.id} run return run {F(f"p/{p.key}/vis")}'
                for p in self.pats if self.g.has(f'p/{p.key}/vis')]
        self.w('p/vis', vis)
        pj = ['# GENERATED: pj_end of props whose mbId = pattern id (@s = prop; #pjEv, #pjKeep preset).']
        pj += [f'execute if score @s mbId matches {p.id} run return run {F(f"p/{p.key}/pj_end")}'
               for p in self.pats if self.g.has(f'p/{p.key}/pj_end')]
        self.w('p/pj_end', pj)
        self.w('p/svc', [
            '# Core mechanics on the service patterns\' clocks (their pattern files own only fx and hazards):',
            f'# transformation clock {TR_SPHERE} = the light sphere (달빛 고치, 달빛 이슬); 달빛 해제 clock 0 = its caption,',
            f'# {RL_FLAT} = the wings go flat lime, {RL_REVERT} = she is human again (hitbox, heal orbs vanish).',
            f'execute if score #bfPat mb matches 20 if score #bfPT mb matches {TR_SPHERE} run return run {F("form/sphere")}',
            f'execute if score #bfPat mb matches 15 if score #bfPT mb matches 0 run return run ' + g.say('달빛 해제', A.LINE_HEX, 2, 30, 2),
            f'execute if score #bfPat mb matches 15 if score #bfPT mb matches {RL_FLAT} run return run {g.look("flat")}',
            f'execute if score #bfPat mb matches 15 if score #bfPT mb matches {RL_REVERT} run return run {F("form/revert")}'])

    # -----------------------------------------------------------------------------------------
    def forms(self):
        F, R, g = self.F, self.R, self.g

        def hitbox(hit, scale, label):
            w_, h_ = L.num(float(hit[0])), L.num(float(hit[1]))
            return [f'# {label} hitbox: click shield {w_} x {h_} b (also for a re-created shield: cur.hit), husk scale {L.num(float(scale))}.',
                    f'data modify storage rlk:mboss cur.hit set value {{w:{w_}f,h:{h_}f}}',
                    'execute as @e[type=minecraft:interaction,tag=rlk_mshield] if score @s msid = @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] msid '
                    f'run data merge entity @s {{width:{w_}f,height:{h_}f}}',
                    f'execute as @e[type=minecraft:husk,tag=rlk_mb_body,limit=1] run attribute @s minecraft:scale base set {L.num(float(scale))}']
        self.w('form/hitbox_h', hitbox(HIT_H, SCALE_H, 'Human-form'))
        self.w('form/hitbox_b', hitbox(HIT_B, SCALE_B, 'Butterfly-form (the rig hovers 1.2 b, the body stays on the floor)'))
        self.w('form/transform_go', ['# The human stretch is over: the transformation (service pattern 20) at this decision point.',
                                     sc_set('#bfPick', 20), F('ai/launch')])
        self.w('form/release_go', ['# The butterfly form is over: 달빛 해제 (service pattern 15; the caption at its clock 0).',
                                   sc_set('#bfPick', 15), F('ai/launch')])
        self.w('form/set_b', ['# Butterfly form state: counters for the 달빛 해제 decision, butterfly hitbox.',
                              sc_set('#bfForm', 2), sc_set('#bfBfN', 0), sc_set('#bfBfT', 0),
                              f'execute store result score #bfBfLim mb run random value {BF_N[0]}..{BF_N[1]}',
                              F('form/hitbox_b')])
        self.w('form/set_h', ['# Human form state: human hitbox (the stretch counters are set by the caller).',
                              sc_set('#bfForm', 1), F('form/hitbox_h')])
        self.w('form/rig_b', ['# The rig and the hitbox in butterfly form at once (wings on, Dendro look); counters untouched (reload).',
                              R('form/butterfly'), g.look('dendro'), sc_set('#bfLook', A.EL_DENDRO), F('form/hitbox_b')])
        self.w('form/rig_h', ['# The rig and the hitbox in human form at once (wings off); counters untouched (reload).',
                              R('form/human'), sc_set('#bfLook', A.EL_DENDRO), F('form/hitbox_h')])
        self.w('form/now_b', ['# Instant butterfly form (tests): a fresh butterfly stretch, no transformation and no 달빛 고치.',
                              F('form/rig_b'), F('form/set_b'), F('hud/refresh')])
        self.w('form/now_h', ['# Instant human form (tests, a groggy started from butterfly form): heal orbs gone.',
                              F('form/rig_h'), F('form/set_h'), F('dew/clear'), F('hud/refresh')])
        self.w('look/switch', [
            '# @s = body: the wing element look #bfWant (1 pyro: orange-gold with magenta rims, 7 dendro: lime/opal), a 1 t',
            '# swap with a flash of its colour.',
            'scoreboard players operation #bfLook mb = #bfWant mb',
            f'execute if score #bfLook mb matches {A.EL_PYRO} run {g.look("pyro")}',
            f'execute if score #bfLook mb matches {A.EL_DENDRO} run {g.look("dendro")}',
            f'execute if score #bfLook mb matches {A.EL_PYRO} run ' + g.dust_fade(A.PYRO_GOLD, A.PYRO_MAG, 1.4, '~ ~3.0 ~', (1.6, 1.0, 0.6), 12),
            f'execute if score #bfLook mb matches {A.EL_PYRO} run ' + g.particle('flame', '~ ~3.0 ~', (1.4, 0.8, 0.5), 0.02, 8),
            f'execute if score #bfLook mb matches {A.EL_PYRO} rotated as @s rotated ~ 0 positioned ~ ~2.8 ~ run ' + g.fx('pyro_switch'),
            f'execute if score #bfLook mb matches {A.EL_PYRO} run ' + g.snd('pyro_switch'),
            f'execute if score #bfLook mb matches {A.EL_DENDRO} run ' + g.dust(A.LIME, 1.3, '~ ~3.0 ~', (1.6, 1.0, 0.6), 12),
            f'execute if score #bfLook mb matches {A.EL_DENDRO} rotated as @s rotated ~ 0 positioned ~ ~2.8 ~ run ' + g.fx('dendro_switch'),
            f'execute if score #bfLook mb matches {A.EL_DENDRO} run ' + g.snd('dendro_switch'),
            F('hud/refresh')])
        self.w('form/transform_done', [
            '# From ai/pat_done: the transformation clip is over: butterfly form, its counters, the first decision soon.',
            F('form/set_b'), sc_set('#bfCool', 16), F('ai/enter')])
        self.w('form/sphere', [
            f'# Transformation clock {TR_SPHERE} (@s = body): the light sphere lands 달빛 고치 on the player and {A.DEW_N} 달빛 이슬',
            '# heal orbs appear (any heal cures it).',
            F('coc/apply'),
            F('dew/spawn')])
        self.w('form/revert', [
            f'# 달빛 해제 clock {RL_REVERT} (@s = body): the wings have shattered, she is human again; uncollected heal orbs vanish.',
            F('form/set_h'), F('dew/clear'), F('hud/refresh'),
            F('seq_h/revert')])                       # [seq_h: human author] S3 drift

    # -----------------------------------------------------------------------------------------
    def transform(self):
        """Service pattern 20: the transformation (about 30 t): the cocoon glows, the folded wings open over 8 t, a light
        sphere r 2.5, ripple rings r 4-5, wings fully spread. 달빛 고치 lands with the sphere (p/svc -> form/sphere)."""
        g = self.g
        key = TRANSFORM.key
        tl = TL(g, key)
        chest = 'execute rotated as @s rotated ~ 0 positioned ~ ~1.6 ~ run '
        tl.at(0, g.look('dendro'), sc_set('#bfLook', A.EL_DENDRO), self.R('face/player'),
              g.dust(A.hexrgb('#B5F089'), 1.3, '~ ~1.0 ~', (0.3, 0.7, 0.3), 10),
              chest + g.fx('tf_sheath'), g.snd('transform_glow'))
        for t in range(1, TR_OPEN):
            tl.at(t, g.dust(A.hexrgb('#C2FA72'), 1.2, '~ ~1.0 ~', (0.25, 0.6, 0.25), 6))
        tl.at(TR_OPEN, g.sound('entity.ender_dragon.flap', 0.6, 1.5), g.particle('end_rod', '~ ~2.3 ~', (0.4, 0.3, 0.4), 0.05, 6))
        tl.at(TR_SPHERE - 1, g.dust(A.hexrgb('#FAFCD4'), 1.6, '~ ~2.2 ~', (0.15, 0.15, 0.15), 12))
        tl.at(TR_SPHERE, chest + g.fx('tf_sphere'), g.snd('transform_swell'),
              *ring(g, A.hexrgb('#F8FDBB'), 2.5, 12, y='1.6', scale=1.4))
        tl.at(TR_RINGS, chest + g.fx('tf_ripples'),
              *ring(g, A.hexrgb('#BDE592'), 4.0, 20, y='0.15', scale=1.2))
        tl.at(TR_RINGS + 4, g.snd('flap_big'))
        for t in range(TR_RINGS + 6, TR_LEN, 6):
            tl.at(t, g.snd('flap_small'))
        tl.at(TR_LEN, g.end())
        tl.write(['# Transformation (core service pattern 20; clip transform, @s = body, at it): the cocoon glows, the wings',
                  f'# open ({TR_OPEN}), the light sphere ({TR_SPHERE}: 달빛 고치 + 달빛 이슬 via p/svc), ripple rings, full spread; end {TR_LEN}.'],
                 [f'# {key} tick (#bfPT 1..{TR_LEN}).'])
        g.pw(key, 'cancel', ['# Nothing of its own lingers (dust only).'])

    # -----------------------------------------------------------------------------------------
    def groggy(self):
        F, R, g = self.F, self.R, self.g
        self.w('groggy/begin', [
            f'# @s = body, after 달빛 해제 (she has just landed in human form): {GROGGY} t of groggy: motionless idle, back',
            '# turned to the player, no tracking, no attacks; then the turn and the chain re-form (recover). No damage bonus.',
            sc_set('#bfSt', ST['groggy']), sc_set('#bfT', 0), sc_set('#mbNoLeash', 0), sc_set('#bfMv', 0),
            f'execute if score #bfForm mb matches 2 run {F("form/now_h")}',
            g.play('groggy_h'),
            'execute at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~180 0',
            F('seq_h/groggy/begin'),                   # [seq_h: human author] S3 visuals and sounds
            F('hud/refresh')])
        self.w('groggy/tick', [
            'scoreboard players add #bfT mb 1',
            f'# still debuffed after 달빛 해제: one new 달빛 이슬 during the groggy',
            f'execute if score #bfT mb matches 20 if score #bfCoc mb matches 1 run {F("dew/spawn1")}',
            F('seq_h/groggy/tick'),                    # [seq_h: human author] S3 visuals and sounds on #bfT
            f'execute if score #bfT mb matches {GROGGY}.. run {F("recover/begin")}'])
        self.w('recover/begin', [
            f'# Groggy over: she turns to face the player ({TURN_T} t), then the crescent chain re-forms ({CHAIN_T} t).',
            sc_set('#bfSt', ST['recover']), sc_set('#bfT', 0), g.play('turn_h'),
            F('seq_h/recover/begin'), F('hud/refresh')])   # [seq_h: human author]
        self.w('recover/tick', [
            'scoreboard players add #bfT mb 1',
            f'execute if score #bfT mb matches 1..{TURN_T} run function rlk:mboss/mv/turn {{max:9}}',
            at_t('#bfT', TURN_T, g.play('chain_reform')),
            F('seq_h/recover/tick'),                   # [seq_h: human author] S3 the chain re-form visuals
            f'execute if score #bfT mb matches {TURN_T + CHAIN_T}.. run {F("groggy/end")}'])
        self.w('groggy/end', [
            f'# Human rotation again: {HUM_NEXT_N} patterns before the next transformation (no time limit), starting with',
            f'# pattern {FIRST_AFTER_GROGGY} (the video goes straight into 달빛 점프).',
            sc_set('#bfHumN', 0), sc_set('#bfHumLim', HUM_NEXT_N), sc_set('#bfHumT', 0), sc_set('#bfHumTL', 0),
            f'execute if score #mbLock mb matches 0 run scoreboard players set #bfReq mb {FIRST_AFTER_GROGGY}',
            sc_set('#bfCool', 4),
            F('ai/enter')])

    # -----------------------------------------------------------------------------------------
    def cocoon(self):
        F, g = self.F, self.g
        self.w('coc/apply', [
            '# 달빛 고치 on the player (any executor): skipped while the player is dead, reviving or on a selection screen.',
            'execute as @a[tag=player,scores={dead=0},limit=1] unless score @s rnDie matches 1.. unless score @s pkMode matches 1.. '
            f'at @s run {F("coc/apply_pl")}'])
        self.w('coc/apply_pl', [
            f'# @s = player, at it. {A.COCOON_HP_PCT} % of the CURRENT HP as damage, non-lethal (at least 1, HP never below 1), no',
            '# element; a debuff, not a hit: no dash i-frames, defence or shields. Then the state: player DMG',
            f'# {A.COCOON_DMG} %, CRIT {A.COCOON_CRIT} (forced crits undone in incoming), healing received {A.COCOON_HEAL} %; a',
            '# previous 달빛 축복 받음 ends here. The kit: swirl fx and curse chime at the player, the HUD badge (coc_on,',
            '# buff_off), the actionbar notice with the numbers; the typed hint (core caption).',
            'scoreboard players operation #bfX mb = @s curHealth',
            'scoreboard players operation #bfX mb *= #bfCocPct mb',
            'scoreboard players operation #bfX mb /= #c100 mb',
            'execute if score #bfX mb matches ..0 run scoreboard players set #bfX mb 1',
            'scoreboard players operation @s curHealth -= #bfX mb',
            'execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1',
            'scoreboard players operation #hurtDmg tmp = #bfX mb',
            'scoreboard players set #elem tmp 0',
            'execute at @e[tag=rlk_body,limit=1] positioned ~ ~1.62 ~ run function rlk:player/hurt_do',
            sc_set('#bfCoc', 1), sc_set('#bfBuff', 0), sc_set('#bfDmgPct', A.COCOON_DMG),
            sc_set('#mbCritAdd', A.COCOON_CRIT), sc_set('#mbHealPct', A.COCOON_HEAL), sc_set('#mbHealEv', 0),
            'scoreboard players add #bfCocN mb 1',
            'execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run ' + g.fx('coc_apply'),
            'execute at @e[tag=rlk_body,limit=1] run ' + g.snd('debuff'),
            g.khud('buff_off'), g.khud('coc_on'), g.khud('ab_coc'),
            g.say('달빛 고치 — 회복하면 해제', A.COC_SWIRL_HEX, 2, 50, 1),
            F('hud/refresh')])
        self.w('coc/heal_ev', [
            '# The player received a heal this tick or the last (rlk:mboss/player_heal counted it; the heal itself was already',
            f'# reduced to {A.COCOON_HEAL} %): ANY heal cures 달빛 고치 (user decision; not only a full heal).',
            sc_set('#mbHealEv', 0),
            f'execute if score #bfCoc mb matches 1 run {F("coc/cure")}'])
        self.w('coc/cure', [
            f'# 달빛 고치 removed -> 달빛 축복 받음: CRIT +{A.BUFF_CRIT} %, DMG +{A.BUFF_DMG - 100} % until the next 달빛 고치 or the fight\'s end.',
            '# The kit\'s cure fx at the player\'s feet (about 20 t: gold beam down, gold burst + ring, gold emblem with',
            '# sparkles) and chime, the badges (coc_off, buff_on), the actionbar notice and the big reward badge.',
            sc_set('#bfCoc', 0), sc_set('#bfBuff', 1), sc_set('#bfDmgPct', A.BUFF_DMG), sc_set('#mbCritAdd', A.BUFF_CRIT),
            sc_set('#mbHealPct', 100),
            'execute at @e[tag=rlk_body,limit=1] rotated ~ 0 run ' + g.fx('cure'),
            'execute at @e[tag=rlk_body,limit=1] run ' + g.snd('cure_chime'),
            g.khud('coc_off'), g.khud('buff_on'), g.khud('ab_buff'), g.khud('pop_buff'),
            F('hud/refresh')])
        self.w('coc/clear', [
            '# 달빛 고치 and 달빛 축복 받음 off, the framework\'s player modifiers neutral, both kit HUD badges off (no',
            '# executor; idempotent).',
            sc_set('#bfCoc', 0), sc_set('#bfBuff', 0), sc_set('#bfDmgPct', 100),
            sc_set('#mbCritAdd', 0), sc_set('#mbHealPct', 100), sc_set('#mbHealEv', 0),
            g.khud('clear')])
        self.w('coc/clear_hud', [F('coc/clear'), f'execute if score #mbSt mb matches 0..1 run {F("hud/refresh")}'])
        self.w('coc/assert', [
            '# Reload: the framework values from the module\'s own state (init keeps live values; re-assert anyway).',
            sc_set('#bfDmgPct', 100), sc_set('#mbCritAdd', 0), sc_set('#mbHealPct', 100),
            f'execute if score #bfBuff mb matches 1 run scoreboard players set #bfDmgPct mb {A.BUFF_DMG}',
            f'execute if score #bfBuff mb matches 1 run scoreboard players set #mbCritAdd mb {A.BUFF_CRIT}',
            f'execute if score #bfCoc mb matches 1 run scoreboard players set #bfDmgPct mb {A.COCOON_DMG}',
            f'execute if score #bfCoc mb matches 1 run scoreboard players set #mbCritAdd mb {A.COCOON_CRIT}',
            f'execute if score #bfCoc mb matches 1 run scoreboard players set #mbHealPct mb {A.COCOON_HEAL}',
            '# the kit\'s HUD badges from the module state (storage rlk:bfkit survives a reload; re-assert anyway)',
            g.khud('clear'),
            f'execute if score #bfCoc mb matches 1 run {g.khud("coc_on")}',
            f'execute if score #bfBuff mb matches 1 run {g.khud("buff_on")}'])
        self.w('coc/uncrit', [
            '# A forced crit (engravings: 6 keen, frost) on the body while CRIT -100 %: back to a normal hit (x 100 / crit',
            '# damage), shown as a normal number. Roll-based crits never happen (critChance -100 in items/hook/stat_buffs).',
            'scoreboard players set #crit tmp 0',
            'execute unless score @a[tag=player,limit=1] critDamage matches 101.. run return 0',
            'scoreboard players operation #dmg tmp *= #c100 mb',
            'scoreboard players operation #dmg tmp /= @a[tag=player,limit=1] critDamage',
            'execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1'])
        self.w('coc/dmg', [
            '# Player DMG on the body x #bfDmgPct % (50 under 달빛 고치, 150 with 달빛 축복 받음), at least 1.',
            'scoreboard players operation #dmg tmp *= #bfDmgPct mb',
            'scoreboard players operation #dmg tmp /= #c100 mb',
            'execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1'])

    # -----------------------------------------------------------------------------------------
    def dew(self):
        F, g = self.F, self.g
        r0, r1 = int(A.DEW_R[0] * 10), int(A.DEW_R[1] * 10)
        self.w('dew/spawn', [
            f'# {A.DEW_N} 달빛 이슬 (moon dew) heal orbs at random spots {L.num(A.DEW_R[0])}-{L.num(A.DEW_R[1])} b from the arena centre, 120 degrees',
            f'# apart (any executor). Touching one heals {A.DEW_HEAL_PCT} % max HP through player/heal (cures 달빛 고치).',
            'execute store result score #bfX mb run random value 0..359',
            F('dew/one'),
            'scoreboard players add #bfX mb 120', F('dew/one'),
            'scoreboard players add #bfX mb 120', F('dew/one')])
        self.w('dew/spawn1', ['# One 달빛 이슬 (still debuffed during the groggy).',
                              'execute store result score #bfX mb run random value 0..359', F('dew/one'),
                              g.sound('block.amethyst_block.chime', 0.6, 1.4)])
        self.w('dew/one', [
            '# #bfX = angle (deg); a random radius.',
            'execute store result storage rlk:mboss bfd.a double 1 run scoreboard players get #bfX mb',
            f'execute store result score #bfY mb run random value {r0}..{r1}',
            'execute store result storage rlk:mboss bfd.r double 0.1 run scoreboard players get #bfY mb',
            f'function {NS}dew/at with storage rlk:mboss bfd'])
        self.w('dew/at', [f'$execute at @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] rotated $(a) 0 positioned ^ ^ ^$(r) '
                          f'positioned ~ {CY} ~ run function {NS}dew/summon'])
        self.w('dew/summon', [
            '# A glowing moon-dew orb 1.1 b above the floor here (an item_display dressed as the kit\'s dew look, with a lime',
            '# glow outline; rlk_mb_aux: dies with the fight), the kit\'s spawn ripple and chime.',
            'summon minecraft:item_display ~ ~1.1 ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_bf_dew","rlk_mb_bf_dewn"],billboard:"center",'
            f'Glowing:1b,glow_color_override:{DEW_GLOW},brightness:{{block:15,sky:15}},item:{{id:"minecraft:slime_ball",count:1}},'
            'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}',
            f'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_dewn] run {g.kprop("dew")}',
            'tag @e[type=minecraft:item_display,tag=rlk_mb_bf_dewn] remove rlk_mb_bf_dewn',
            'scoreboard players add #bfDewN mb 1',
            g.fx('dew_spawn'),
            g.particle('end_rod', '~ ~1.1 ~', (0.1, 0.1, 0.1), 0.08, 6),
            g.snd('dew_spawn')])
        self.w('dew/all', ['# Every live heal orb (module tick while #bfDewN >= 1): shimmer, pickup.', sc_set('#bfDewN', 0),
                           f'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_dew] at @s run {F("dew/tick")}'])
        self.w('dew/tick', [
            '# @s = heal orb, at it (1.1 b above the floor).',
            'scoreboard players add #bfDewN mb 1',
            'scoreboard players add @s mbT 1',
            'scoreboard players operation #bfM mb = @s mbT', 'scoreboard players operation #bfM mb %= #bfK3 mb',
            'execute if score #bfM mb matches 0 run ' + g.dust(A.LIME_PALE, 0.9, '~ ~ ~', (0.22, 0.22, 0.22), 2),
            'execute if score #bfM mb matches 1 run ' + g.particle('end_rod', '~ ~0.2 ~', (0.15, 0.25, 0.15), 0.004, 1),
            'scoreboard players operation #bfM mb = @s mbT', 'scoreboard players operation #bfM mb %= #bfK20 mb',
            '# the kit\'s idle pulse (a soft floor ring and rising motes) so it reads on the marble',
            'execute if score #bfM mb matches 0 run ' + g.fx('dew_pulse'),
            f'execute positioned ~ ~-1.1 ~ if entity @e[tag=rlk_body,distance=..1.6,limit=1] run {F("dew/take")}'])
        self.w('dew/take', [
            '# The player touched it (@s = orb, at it): heal, sparkle, gone.',
            f'execute as @a[tag=player,limit=1] run {F("dew/heal")}',
            g.dust(A.LIME_CORE, 1.4, '~ ~ ~', (0.4, 0.4, 0.4), 16),
            g.particle('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.12, 10),
            g.particle('happy_villager', '~ ~ ~', (0.4, 0.4, 0.4), 0, 6),
            g.sound('block.amethyst_block.chime', 1.0, 1.9), g.sound('block.amethyst_cluster.hit', 0.6, 1.6),
            'scoreboard players remove #bfDewN mb 1',
            'kill @s'])
        self.w('dew/heal', [
            f'# @s = player: {A.DEW_HEAL_PCT} % of max HP (red herb boosts orb heals as for the normal heal orbs), at least 1, through',
            '# player/heal (so items/hook/on_heal: 달빛 고치 -40 % and the cure).',
            'scoreboard players operation #heal tmp = @s maxHealth',
            'scoreboard players operation #heal tmp *= #bfDewPct mb',
            'scoreboard players operation #heal tmp /= #c100 mb',
            'execute if score @s it_red_herb matches 1.. run function rlk:items/proc/herb',
            'execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1',
            'function rlk:player/heal'])
        self.w('dew/clear', ['# Every heal orb fades (the butterfly form ended).',
                             'execute as @e[type=minecraft:item_display,tag=rlk_mb_bf_dew] at @s run ' + g.particle('poof', '~ ~ ~', (0.2, 0.2, 0.2), 0.02, 6),
                             'kill @e[type=minecraft:item_display,tag=rlk_mb_bf_dew]',
                             sc_set('#bfDewN', 0)])

    # -----------------------------------------------------------------------------------------
    def burn(self):
        F = self.F
        self.w('burn/start', [
            '# @s = body (module tick): the Burning weakness of the butterfly form. Pyro and Dendro auras (0.8 U each, the',
            '# element/attach rules) and, if she is not burning yet, the reaction-10 state: burnDmg = 50 % of the reaction',
            '# base of the player (element/calc), the DoT every 10 t in element/burn_tick, the "연소" text.',
            sc_set('#bfBurnQ', 0),
            'scoreboard players set #elU tmp 1000',
            'function rlk:element/attach {e:"Grass"}',
            'function rlk:element/attach {e:"Fire"}',
            'scoreboard players set @s elAct 1',
            f'execute unless score @s burnOn matches 1 run {F("burn/ignite")}'])
        self.w('burn/ignite', [
            'execute as @a[tag=player,limit=1] run function rlk:element/src_player',
            'function rlk:element/calc {m:50}',
            'scoreboard players operation @s burnDmg = #rdmg tmp',
            'scoreboard players set @s burnI 0',
            'scoreboard players set @s burnOn 1',
            'scoreboard players set #rx tmp 10',
            'scoreboard players set #lunRx tmp 0',
            'function rlk:element/rx_text'])

    # -----------------------------------------------------------------------------------------
    def death(self):
        F, R, g = self.F, self.R, self.g
        self.w('death_start', [
            '# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden). The fight is',
            '# over for the player too: 달빛 고치 / 달빛 축복 받음 off, heal orbs gone. The death clip: she staggers, the wings',
            '# (in butterfly form) shatter into lime/opal shards, she kneels and dissolves into moonlight motes and crystal',
            '# shards. No creature voices; the registry\'s deathSnd false keeps the framework roar off.',
            F('p/cancel'),
            F('coc/clear'),
            F('dew/clear'),
            sc_set('#bfSt', ST['dead']),
            R('prop/clear'),
            g.play('death'),
            '# the kit: its ground decals go (the hazards are already cleared)',
            f'function {K.FN}tele/clear',
            F('seq_h/death/start')])                   # [seq_h: human author] S4 visuals and sounds
        lines = ['# Hook death_tick (@s = body, #mbT = 1.. until cur.death): the clip runs while the rig ticks; it must NOT tick',
                 f'# after its kill at {DEATH_LEN} (it would respawn).',
                 at_t('#mbT', (1, DEATH_LEN - 1), R('tick')),
                 at_t('#mbT', DEATH_LEN, R('kill')),
                 F('seq_h/death/tick')]                  # [seq_h: human author] S4 visuals and sounds on #mbT
        self.w('death_tick', lines)

    # -----------------------------------------------------------------------------------------
    def hud(self):
        F, g = self.F, self.g
        extra = ['# Name-line suffix: form, groggy, then the kit\'s badges (hud/put_extra: the 달빛 고치 glyph, maroon disc with a',
                 '# salmon swirl, and / or the 달빛 축복 받음 glyph; flags set by fx/hud/coc_on|off, buff_on|off).',
                 'data modify storage rlk:mboss extra set value []',
                 f'execute if score #bfForm mb matches 1 run data modify storage rlk:mboss extra append value {{text:"   인간형",color:"{HUM_HEX}",bold:false}}',
                 f'execute if score #bfForm mb matches 2 run data modify storage rlk:mboss extra append value {{text:"   나비형",color:"{BF_HEX}",bold:false}}',
                 f'execute if score #bfSt mb matches {ST["groggy"]}..{ST["recover"]} run data modify storage rlk:mboss extra append value {{text:"  · 그로기",color:"#9FE8A0",bold:false}}']
        extra.append(g.khud('put_extra'))
        self.w('hud/extra', extra)
        sub = ['# Third line: what she is doing, then the player\'s 달빛 고치 / 달빛 축복 받음 state (the kit\'s hud/put_sub: badge',
               '# glyph + "달빛 고치 — 회복하면 해제" + the dew icon, or badge + "달빛 축복 받음 (치명타 +15% · 피해 +50%)").',
               'execute if score #mbSt mb matches 0 run data modify storage rlk:mboss sub set value []',
               'execute if score #mbSt mb matches 0 run return 0',
               f'data modify storage rlk:mboss sub set value [{{text:"인간형",color:"{HUM_HEX}",bold:true}}]',
               f'execute if score #bfForm mb matches 2 run data modify storage rlk:mboss sub set value [{{text:"나비형",color:"{BF_HEX}",bold:true}}]',
               f'execute if score #bfForm mb matches 2 if score #bfLook mb matches {A.EL_PYRO} run data modify storage rlk:mboss sub append value {{text:"  화염 날개",color:"#FFB070"}}',
               f'execute if score #bfForm mb matches 2 if score #bfLook mb matches {A.EL_DENDRO} run data modify storage rlk:mboss sub append value {{text:"  달빛 날개",color:"#D9F5A8"}}']
        for p in self.pats:
            col = '#FFB070' if p.el == A.EL_PYRO else '#D9F5A8'
            if p.id == 20:
                col = A.COC_SWIRL_HEX
            sub.append(f'execute if score #bfSt mb matches {ST["pattern"]}..{ST["close"]} if score #bfPick mb matches {p.id} run data modify storage rlk:mboss sub set value '
                       f'[{{text:"패턴  ",color:"#A8A8A8"}},{{text:"{p.label}",color:"{col}"}}]')
            if p.form == 'b':
                sub.append(f'execute if score #bfSt mb matches {ST["prep"]} if score #bfPick mb matches {p.id} run data modify storage rlk:mboss sub set value '
                           f'[{{text:"패턴  ",color:"#A8A8A8"}},{{text:"{p.label}",color:"{col}"}}]')
        sub += [f'execute if score #bfSt mb matches {ST["groggy"]} run data modify storage rlk:mboss sub set value [{{text:"그로기  ",color:"#9FE8A0",bold:true}},{{text:"공격할 기회",color:"#C8E8C8"}}]',
                f'execute if score #bfSt mb matches {ST["recover"]} run data modify storage rlk:mboss sub set value [{{text:"그로기  ",color:"#9FE8A0",bold:true}},{{text:"다시 일어선다",color:"#C8E8C8"}}]',
                g.khud('put_sub')]
        self.w('hud/sub', sub)
        self.w('hud/refresh', ['# Both text lines from the current state (on every state, form, look and debuff change).',
                               F('hud/extra'), F('hud/sub')])
        self.w('hud/bar_groggy', [sc_set_bu('#buSub', GROGGY), 'scoreboard players operation #buSub bu -= #bfT mb',
                                  sc_set_bu('#buSubMax', GROGGY), sc_set_bu('#buSubCol', 9)])
        self.w('hud/bar_recover', ['scoreboard players operation #buSub bu = #bfT mb', sc_set_bu('#buSubMax', TURN_T + CHAIN_T),
                                   sc_set_bu('#buSubCol', 9)])
        self.w('hud/bar_pattern', ['# Pattern progress against its real end (#bfPLen), empty at the end; colour = its element.',
                                   'scoreboard players operation #buSub bu = #bfPLen mb', 'scoreboard players operation #buSub bu -= #bfPT mb',
                                   'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
                                   'execute if score #buSub bu > #bfPLen mb run scoreboard players operation #buSub bu = #bfPLen mb',
                                   'scoreboard players operation #buSubMax bu = #bfPLen mb',
                                   'scoreboard players operation #buSubCol bu = #bfPCol mb'])
        self.w('hud/bar_bform', ['# Butterfly form: time left before 달빛 해제 (or fewer patterns).',
                                 sc_set_bu('#buSub', BF_T), 'scoreboard players operation #buSub bu -= #bfBfT mb',
                                 'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
                                 sc_set_bu('#buSubMax', BF_T), sc_set_bu('#buSubCol', 7)])
        self.w('hud/bar_hform', ['# First human stretch: fight time left before the transformation (or fewer patterns).',
                                 'scoreboard players operation #buSub bu = #bfHumTL mb', 'scoreboard players operation #buSub bu -= #bfHumT mb',
                                 'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
                                 'scoreboard players operation #buSubMax bu = #bfHumTL mb', sc_set_bu('#buSubCol', 8)])

    # -----------------------------------------------------------------------------------------
    def tests(self):
        F, R, g = self.F, self.R, self.g
        hum = ', '.join(f'{p.id} {p.label}' for p in self.hum)
        bfl = ', '.join(f'{p.id} {p.label}' for p in self.bfl)
        HELP = [
            ('1-4', f'인간형 패턴 ({hum})'), ('11-14', f'나비형 패턴 ({bfl}), 즉시 나비형'),
            ('15 / 30', '달빛 해제'), ('20', '변신(달빛 고치 · 달빛 이슬)'), ('21', '달빛 고치만'), ('22', '회복 1 (해제 → 달빛 축복)'),
            ('23', '달빛 이슬 3개'), ('24', '고치 · 축복 끄기'), ('40', '그로기'), ('42', '다음 결정에서 형태 전환'),
            ('91', '나비형 연소 약점 시험(불 타격 흉내)'), ('99', '대기로'),
            ('lock 1-4 / 11-14 / 16', '그 패턴만 / (변신 뒤) 그 나비형 패턴만 / 변신 · 해제만 반복'),
            ('시작', '/function rlk:mboss/test/start {id:\\"butterfly\\"} 또는 #mbForce mb 2'),
        ]
        txt = '[{text:"[달빛 환영 나비 테스트] ",color:"#B6E35A",bold:true}' + ''.join(
            f',{{text:"{k}",color:"yellow"}},{{text:" {v}  ",color:"gray"}}' for k, v in HELP) + ']'
        self.w('test/help', ['tellraw @a[tag=player] ' + txt])
        self.w('test/cut', [
            '# @s = body: stop whatever runs (hazards, props, pull, movement, slot pattern, close-in, look prep, groggy).',
            'function rlk:mboss/lib_clear',
            F('p/cancel'),
            R('prop/clear'),
            sc_set('#bfMv', 0),
            f'execute if score #bfForm mb matches 1 run {g.play("idle_h")}',
            f'execute if score #bfForm mb matches 2 run {g.play("idle_b")}',
            sc_set('#bfCool', 10),
            F('ai/enter')])
        run = ['# @s = body, #bfTst = the requested test id.']
        run += [f'execute if score #bfTst mb matches 1..4 run {F("test/cut")}',
                'execute if score #bfTst mb matches 1..4 run scoreboard players operation #bfReq mb = #bfTst mb',
                'execute if score #bfTst mb matches 1..4 run scoreboard players set #bfCool mb 1',
                'execute if score #bfTst mb matches 1..4 run return 0',
                f'execute if score #bfTst mb matches 11..14 run {F("test/cut")}',
                'execute if score #bfTst mb matches 11..14 run scoreboard players operation #bfReq mb = #bfTst mb',
                'execute if score #bfTst mb matches 11..14 run scoreboard players set #bfCool mb 1',
                'execute if score #bfTst mb matches 11..14 run return 0',
                'execute if score #bfTst mb matches 30 run scoreboard players set #bfTst mb 15',
                f'execute if score #bfTst mb matches 15 run {F("test/cut")}',
                f'execute if score #bfTst mb matches 15 run {sc_set("#bfReq", 15)}',
                f'execute if score #bfTst mb matches 15 run return run {sc_set("#bfCool", 1)}',
                f'execute if score #bfTst mb matches 20 run {F("test/cut")}',
                f'execute if score #bfTst mb matches 20 run {sc_set("#bfReq", 20)}',
                f'execute if score #bfTst mb matches 20 run return run {sc_set("#bfCool", 1)}',
                f'execute if score #bfTst mb matches 21 run return run {F("coc/apply")}',
                f'execute if score #bfTst mb matches 22 run return run {F("test/heal")}',
                f'execute if score #bfTst mb matches 23 run return run {F("dew/spawn")}',
                f'execute if score #bfTst mb matches 24 run return run {F("coc/clear_hud")}',
                f'execute if score #bfTst mb matches 40 run {F("test/cut")}',
                f'execute if score #bfTst mb matches 40 run return run {F("groggy/begin")}',
                f'execute if score #bfTst mb matches 42 if score #bfForm mb matches 1 run scoreboard players operation #bfHumN mb = #bfHumLim mb',
                f'execute if score #bfTst mb matches 42 if score #bfForm mb matches 2 run scoreboard players set #bfBfT mb {BF_T - 20}',
                'execute if score #bfTst mb matches 42 run return 0',
                'execute if score #bfTst mb matches 91 run scoreboard players set #elem tmp 1',
                'execute if score #bfTst mb matches 91 run scoreboard players set #tfm tmp 0',
                f'execute if score #bfTst mb matches 91 run return run {F("on_hit")}',
                f'execute if score #bfTst mb matches 99 run return run {F("test/cut")}',
                F('test/help')]
        self.w('test/run', run)
        self.w('test/heal', ['# A 1 HP heal through the real path (player/heal -> items/hook/on_heal -> mboss/player_heal).',
                             'scoreboard players set #heal tmp 1',
                             'execute as @a[tag=player,limit=1] run function rlk:player/heal'])
