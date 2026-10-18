"""Field generator core: hooks, the state machine (entrance, the cruise rotation with its range-band shuffle bag, the
field trigger, the field sequence: warp to the centre, 「인력 충격파」 x3, field patterns, the closing waves, the pack-up),
the 20-hit break meter (counting rules, HUD, crack stages), the break, groggy 200 t and recovery, the field damage cut,
low gravity on and off, the body clamp r 16.5, the per-form hitbox, death, pause, reload, uninstall, tests, the
core's vanilla fx (cfx/) and the generated pattern dispatchers. See __init__.py for the package layout and the
scratchpad file mb3/fg_contract.md for the core <-> pattern contract.

Owns F:mboss/fieldgen/** except F:mboss/fieldgen/rig/** (the rig generator, wip/fg-rig) and the fx kit's paths
(tools/build_mboss_fg_fx.py: fx/{card,cardx,look,clear,uninstall} and fx/{e,p,tele,snd,hud,prop,test,rig_stub}/**,
listed under "owned" in tools/mboss_fg_fx_manifest.json). Every file it owns is deleted and rewritten on each run
(F:mboss/fieldgen/rig_stub/ too: it exists only while api.STUB). The kit is the effect engine: the core wires its
hooks (uninstall, cleanup, pause, death, the break), the meter protocol (meter_open / meter_hit / meter_close), the
field banner, the low-gravity and groggy flags and the boss-bar lines (put_extra / put_sub, redrawn when the kit's
#fkHudV changes); fg_contract.md section 15. The core's other visuals are still vanilla (cfx/**).
Copied from tools/mboss_butterfly/core.py; the butterfly review findings (scratchpad mb2/review/core_findings.json)
are not copied: kept markers die with their pattern (S1), g.release never stops the AI (S2), the body clamp is real
(S6), test cuts and reloads re-derive the rig form and the counters from the state (S3, S4, S8), the blade reach is
hr + 0.65 (FW-1, api.rocks), every volley group's members exist before its first strike (FW-4), uninstall removes the
module's storage (perf-4).
"""
import importlib
import json

from . import PATTERN_MODULES
from . import api as A
from .api import L, K, Gen, TL, ev_or, clip_len, CX, CY, CZ

NS = A.NS
OWN_TOP = 'mboss/' + A.ID
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'
ARENA_M = '@e[type=minecraft:marker,tag=rlk_mb_arena,limit=1]'

# ---------------------------------------------------------------------------------------------
# Tunables (plan.md)
FIRST_FIELD_N, NEXT_FIELD_N = 5, 4            # cruise patterns before the first field / before every later one
FIELD_T = 400                                 # field patterns stretch (checked at decision points), then the closer
GROGGY = 200                                  # after the break
CUT = 60                                      # % damage the boss takes while the field is up ("모든 저항 증가")
ICD = 6                                       # at most one meter count per 6 t (gametime)
HINT_T = 120                                  # the first field's hint on the sub-line
KEEP_MIN, KEEP_MAX = 6, 10                    # cruise idle: keep 6-10 b from the player
TURN_C, TURN_F = 4, 3                         # idle tracking, degrees per tick (the device turns slowly)
INTRO_CLIP = 1                                # intro tick of the entrance clip's tick 0 (played in intro/setup)
ENT_LEN = clip_len('entrance')
ENT_CLANK = ev_or('entrance', 'clank', 16)
ENT_UNFOLD = ev_or('entrance', 'unfold', 28)
ENT_EYE = ev_or('entrance', 'eye', 54)
ENT_RISE = ev_or('entrance', 'rise', 80)
ENT_RISEN = ev_or('entrance', 'risen', 110)   # the rise ends: targetable, the fight starts (plan: about t94 after the clank)
INTRO_DONE = INTRO_CLIP + ENT_RISEN
WARP_LEN = clip_len('warp_out')               # 34: halo flip 0-12, warp-out at 13, invisible until 34
WARP_OUT = ev_or('warp_out', 'out', 13)
FIN_UNFOLD = WARP_LEN + ev_or('warp_in_field', 'unfold', 1)       # 35: the meter opens, targetable again
FIN_BANNER = WARP_LEN + ev_or('warp_in_field', 'banner', 22)      # 56: the banner, low gravity
FIN_LEN = FIN_BANNER + 1
FOUT_LEN = clip_len('field_end')              # 78: lift-off, rise, lances, pack
FOUT_LANCES = ev_or('field_end', 'lances', 22)
FOUT_PACK = ev_or('field_end', 'pack', 50)
BRK_LEN = clip_len('break')                   # 34: bubble 0-5, burst 5, tilt, wobble, sink
BRK_BURST = ev_or('break', 'burst', 5)
BRK_WOBBLE = ev_or('break', 'wobble', 14)
REC_LEN = clip_len('recover')                 # 15: re-level 6 + core flip 9
REC_FLIP = ev_or('recover', 'flip', 6)
DEATH_LEN = clip_len('death')
D_DROP = ev_or('death', 'drop', 20)
D_SINK = ev_or('death', 'sink', 40)
D_OUT = ev_or('death', 'out', 90)
HIT = {'c': ((A.BOSS['hit']['w'], A.BOSS['hit']['h']), A.BOSS['scale']),     # cruise = the registry 2.4 x 4.6, scale 2.4
       'f': ((2.8, 5.2), 2.6),                                               # field: the core hangs exposed, stack spread
       'g': ((2.6, 3.6), 2.0)}                                               # groggy: slumped (ring centre about 3.0 b)
assert INTRO_DONE <= A.BOSS['intro'], (INTRO_DONE, A.BOSS['intro'])
assert DEATH_LEN <= A.BOSS['death'], (DEATH_LEN, A.BOSS['death'])
assert WARP_OUT < WARP_LEN < FIN_UNFOLD < FIN_BANNER and BRK_BURST < BRK_LEN

ST = {'idle': 0, 'pattern': 1, 'groggy': 3, 'recover': 4, 'break': 6, 'dead': 7}
FLD = {'cruise': 0, 'warp': 1, 'open': 2, 'patterns': 3, 'close': 4, 'pack': 5}
GOLD_HEX, VIOLET_HEX = A.GOLD_HEX, A.VIOLET_HEX
BANNER = '중력이 감소하고 점프 능력이 향상됩니다'
HINT = '코어를 공격해 역장을 깨뜨리세요'
BANNER_T = 80                                 # the kit's field banner holds the actionbar this long (hud/banner_field)
# The kit's hud/meter_hit cracks the core bubble itself at counts 5 / 10 / 15 (<RIG>crack/<n> as the body). While
# the kit drives another rig than the core (its own stub rig, before wip/fg-rig is merged) the core keeps its own
# crack call; once both drive the same rig the core calls crack only for a stage the kit skipped (test 31's +5 jumps).
KIT_CRACKS = K.RIG() == f'{NS}{A.RIG_DIR}/'
KF = K.FN                                     # rlk:mboss/fieldgen/fx/

# The field opening and the pack-up are core service patterns (their mechanics belong to the core).
FIELD_IN = A.Pattern(20, 'field_in', '역장 생성', 'c', 'warp_out', kind='service', recover=0, max_len=FIN_LEN + 5, length=FIN_LEN)
FIELD_OUT = A.Pattern(22, 'field_out', '역장 해제', 'f', 'field_end', kind='service', recover=20, max_len=FOUT_LEN + 5,
                      length=FOUT_LEN)


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
    for p in (FIELD_IN, FIELD_OUT):
        p.module = 'core'
        pats.append(p)
    ids = [p.id for p in pats]
    assert len(set(ids)) == len(ids), ids
    keys = [p.key for p in pats]
    assert len(set(keys)) == len(keys), keys
    for need, state, kind in ([(i, 'c', 'normal') for i in range(1, 7)] + [(11, 'f', 'normal'), (12, 'f', 'normal'),
                                                                          (21, 'f', 'service')]):
        p = next((x for x in pats if x.id == need), None)
        assert p is not None, f'pattern id {need} missing'
        assert (p.state, p.kind) == (state, kind), (need, p.state, p.kind)
    assert all(p.id in range(1, 7) or p.id in (11, 12, 20, 21, 22) for p in pats), ids
    core = Core(g, pats)
    core.emit()
    for p in pats:
        for f in ('start', 'tick', 'cancel'):
            assert g.has(f'p/{p.key}/{f}'), f'{p.module}: pattern {p.key} has no {f}'
    if A.STUB:
        from . import stub_rig
        stub_rig.emit(g)
    removed = clean(out)
    normal = [p for p in pats if p.kind == 'normal']
    print(f'mboss fieldgen: {len(g.files)} functions ({len(normal)} normal + {len(pats) - len(normal)} service patterns '
          f'from {", ".join(PATTERN_MODULES)} + core), {removed} stale removed, rig '
          f'{"STUB (" + A.MANIFEST.name + ")" if A.STUB else A.MANIFEST.name}.')
    for clip, event, default in sorted(set(A.FALLBACKS)):
        print(f'  note: manifest clip {clip} has no event {event!r}; using tick {default}')


def foreign():
    """Paths under F:mboss/fieldgen/ that other generators own (relative, no extension): the rig generator's rig/
    and the fx kit's owned dirs / files (tools/mboss_fg_fx_manifest.json "owned", united with the kit's own
    constants so a stale manifest never exposes a kit file). Any other name under fx/ is the core's (fg_fx_api.md 0).
    Returns (dirs, files)."""
    dirs, files = {'rig'}, set()
    pre = f'data/rlk/function/{OWN_TOP}/'
    man = A._TOOLS / 'mboss_fg_fx_manifest.json'
    if man.exists():
        own = json.loads(man.read_text(encoding='utf-8')).get('owned', {})
        dirs |= {d[len(pre):] for d in own.get('dirs', []) if d.startswith(pre)}
        files |= {f[len(pre):-len('.mcfunction')] for f in own.get('files', []) if f.startswith(pre)}
    kfx = K.FDIR[len('data/rlk/function/' + OWN_TOP + '/'):]
    dirs |= {f'{kfx}/{d}' for d in K.OWNED_DIRS}
    files |= {f'{kfx}/{f}' for f in K.OWNED_FILES}
    return dirs, files


def is_foreign(rel, dirs, files):
    """rel: path under F:mboss/fieldgen/ (posix, without .mcfunction for files)."""
    return rel in files or any(rel == d or rel.startswith(d + '/') for d in dirs)


def clean(out):
    """Owned: every file under F:mboss/fieldgen/ except the rig generator's rig/ and the fx kit's paths (foreign())."""
    root = L.FN / OWN_TOP
    dirs, files = foreign()
    removed = 0
    for p in sorted(root.rglob('*.mcfunction')):
        rel = p.relative_to(root).with_suffix('').as_posix()
        if is_foreign(rel, dirs, files):
            assert p.resolve() not in out.written, f'the fieldgen core wrote into a foreign path: {rel}'
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


class Core:
    def __init__(self, g, pats):
        self.g, self.pats = g, pats
        self.normal = [p for p in pats if p.kind == 'normal']
        self.cru = [p for p in self.normal if p.state == 'c']
        self.fld = [p for p in self.normal if p.state == 'f']
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
        self.field()
        self.meter()
        self.groggy()
        self.forms()
        self.death()
        self.hud()
        self.tests()
        self.cfx()
        self.services()

    # -----------------------------------------------------------------------------------------
    def consts_vars(self):
        self.w('ai/consts', ['# Module constants (spawn, reload). #fgK<n> are the moduli of Gen.every, the core\'s cycles and the',
                             '# patterns\' arithmetic (#fgK11: the wave front grows 11 / 2 tenths per tick).']
               + [sc_set(f'#fgK{n}', n) for n in (2, 3, 4, 5, 6, 8, 10, 11, 20, 40)]
               + [sc_set('#fgCut', CUT)])
        v = ['# Every fake player of the module back to its fight-start value (spawn, cleanup; no executor).',
             '# AI state #fgSt: 0 idle 1 pattern 3 groggy 4 recover 6 break 7 dying.',
             '# field stage #fgField: 0 cruise 1 warp 2 opening waves 3 field patterns 4 closing waves 5 pack-up.']
        v += [sc_set(k, 0) for k in ('#fgSt', '#fgT', '#fgMv', '#fgLast', '#fgPick', '#fgReq', '#fgReqK', '#fgPat', '#fgPNew',
                                     '#fgPT', '#fgPEnd', '#fgPMax', '#fgPLen', '#fgPRel', '#fgPDone', '#fgPCol', '#fgClk',
                                     '#fgFlash', '#fgTst', '#fgDist', '#fgField', '#fgFT', '#fgFN', '#fgHintT', '#fgCruN',
                                     '#fgOpen', '#fgBrk', '#fgBrkFx', '#fgBrkQ', '#fgCrack', '#fgLowG', '#fgWvK', '#fgTri',
                                     '#fgHudV')]
        v += [sc_set('#fgCool', 30), sc_set('#fgBand', 2), sc_set('#fgCruLim', FIRST_FIELD_N), sc_set('#fgBrkT', -1000000),
              sc_set('#fgBanG', -1000000)]
        v += [sc_set(f'#fgBag{p.id}', 1) for p in self.normal]
        self.w('ai/vars', v)

    # -----------------------------------------------------------------------------------------
    def utils(self):
        g = self.g
        self.w('u/lockw', [
            '# Marker rlk_mb_fg_lock on the floor under the player\'s body, pulled inside the walk disc r 20.3 (any executor).',
            'kill @e[type=minecraft:marker,tag=rlk_mb_fg_lock]',
            f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_lock"]}}',
            f'execute as @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] run {g.clamp_walk()}'])
        self.w('u/lockb', [
            '# Marker rlk_mb_fg_lock on the floor under the player\'s body, pulled inside the body disc r 16.5 (any executor).',
            'kill @e[type=minecraft:marker,tag=rlk_mb_fg_lock]',
            f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_lock"]}}',
            f'execute as @e[type=minecraft:marker,tag=rlk_mb_fg_lock,limit=1] run {g.clamp_body()}'])
        for name, r in (('clamp_w', A.WALK_R), ('clamp_b', A.BODY_R)):
            self.w(f'u/{name}', [f'# @s = a marker: pulled toward the arena axis (0.5 b steps) until within {L.num(r)} b of it.',
                                 sc_set('#fgCl', 0), f'function {NS}u/{name}_s'])
            self.w(f'u/{name}_s', [
                f'execute at @s positioned ~ {CY} ~ if entity @e[tag=rlk_mb_arena,distance=..{L.num(r)},limit=1] run return 0',
                'scoreboard players add #fgCl mb 1',
                'execute if score #fgCl mb matches 90.. run return 0',
                f'execute at @s facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
                f'function {NS}u/{name}_s'])
        self.w('u/okb', [
            f'# At a proposed body position: mv/ok (free, inside the safe disc) and within the body disc r {L.num(A.BODY_R)}.',
            f'execute positioned ~ {CY} ~ unless entity @e[tag=rlk_mb_arena,distance=..{L.num(A.BODY_R)},limit=1] run return fail',
            'execute unless function rlk:mboss/mv/ok run return fail',
            'return 1'])
        self.w('u/toward', [f'# @s = body: {{d}} blocks toward the player when the spot passes u/okb (no turn).',
                            f'$execute at @s facing entity {PLAYER} feet rotated ~ 0 positioned ^ ^ ^$(d) if function {NS}u/okb run tp @s ~ ~ ~'])
        self.w('u/away', [f'$execute at @s facing entity {PLAYER} feet rotated ~180 0 positioned ^ ^ ^$(d) if function {NS}u/okb run tp @s ~ ~ ~'])
        self.w('u/fwd', ['$execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^$(d) if function ' + NS + 'u/okb run tp @s ~ ~ ~'])
        self.w('u/leash', [
            f'# @s = body outside the body disc r {L.num(A.BODY_R)} (module tick, not while a framework glide moves it): 0.3 b/t back',
            '# toward the arena axis (the spikes clear the wall ring; the framework leash at r 20 never triggers).',
            f'execute at @s facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.3 run tp @s ~ ~ ~'])
        self.w('u/centre', ['# @s = body: to the arena centre at once, facing the player (the field).',
                            f'tp @s {ARENA_M}',
                            f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0'])

    # -----------------------------------------------------------------------------------------
    def hooks(self):
        F, R, g = self.F, self.R, self.g
        self.w('spawn', [
            '# Hook spawn (@s = arena marker at the centre, rotated north). The body stands on the centre facing south',
            '# (the arriving player); intro/setup builds the rig in its dormant form and plays the entrance.',
            'execute rotated 0 0 run function rlk:mboss/body',
            f'execute as {BODY} at @s run {F("intro/setup")}'])
        self.w('tick', [
            '# Hook tick (@s = body, at @s, fight state). Order: clocks and flags; the break meter (a count from on_hit,',
            '# the 20th breaks the field before the AI runs: the running pattern is cancelled); the boss-bar lines again',
            '# when the fx kit rebuilt its HUD components (#fkHudV: the pip flash ends by a schedule); the field clocks;',
            '# the body clamp r 16.5; AI state; pattern slot; the low-gravity request (mboss/main clears #mbLowG every',
            '# tick, so it is set again every tick the field holds it, after the slot: the banner tick counts); the rig.',
            'scoreboard players add #fgClk mb 1',
            f'execute if score #fgFlash mb matches 1 run {R("flash")}',
            sc_set('#fgFlash', 0),
            f'execute if score #fgBrkFx mb matches 1 run {F("brk/count")}',
            f'execute if score #fgBrkQ mb matches 1 run {F("brk/begin")}',
            f'execute unless score #fgHudV mb = #fkHudV mb run {F("hud/refresh")}',
            f'execute if score #fgField mb matches 1.. run {F("field/tick")}',
            f'execute unless entity @s[tag=rlk_mb_mv] positioned ~ {CY} ~ unless entity @e[tag=rlk_mb_arena,distance=..{L.num(A.BODY_R)},limit=1] run {F("u/leash")}',
            F('ai/state'),
            f'execute if score #fgPat mb matches 1.. run {F("p/run")}',
            'execute if score #fgLowG mb matches 1 run scoreboard players set #mbLowG mb 1',
            R('tick')])
        self.w('on_hit', [
            '# Hook on_hit (@s = body inside combat/apply; #elem #elU #rx #tfm #dmg #crit #sub known). Scores only.',
            f'# The break meter (plan: 20 hits replace the 3 Pneuma hits): only while the field is open (#fgOpen 1, from the',
            '# unfold to the break or the pack-up); reaction and DoT damage (#tfm 1) and item procs (#sub itv 1) do not',
            f'# count; at most one count per {ICD} t (gametime: a multi-hit burst or a shotgun counts once). True damage and',
            '# hits while untargetable never reach this hook. The module tick turns a count into the fx / HUD (#fgBrkFx)',
            '# and the 20th into the break (#fgBrkQ).',
            sc_set('#fgFlash', 1),
            'execute unless score #fgOpen mb matches 1 run return 0',
            f'execute if score #fgBrk mb matches {A.METER_N}.. run return 0',
            'execute if score #tfm tmp matches 1 run return 0',
            'execute if score #sub itv matches 1 run return 0',
            'execute store result score #fgNow mb run time query gametime',
            'scoreboard players operation #fgNow mb -= #fgBrkT mb',
            f'execute if score #fgNow mb matches ..{ICD - 1} run return 0',
            'execute store result score #fgBrkT mb run time query gametime',
            'scoreboard players add #fgBrk mb 1',
            sc_set('#fgBrkFx', 1),
            f'execute if score #fgBrk mb matches {A.METER_N}.. run scoreboard players set #fgBrkQ mb 1'])
        self.w('aux_hit', ['# Hook aux_hit: the device has no breakable helper objects (the meter counts hits on the body).'])
        self.w('incoming', [
            '# Hook incoming (@s = body inside combat/apply_mods, after the level factor and mres). NO element RES of any',
            '# kind: mres stays 0 and nothing here reads #elem (every element deals the same). While the field is up',
            f'# (#fgOpen 1) the boss takes {CUT} % ("모든 저항이 증가"), reactions included, at least 1.',
            f'execute if score #fgOpen mb matches 1 if score #dmg tmp matches 1.. run {F("field/cut")}'])
        self.w('field/cut', ['scoreboard players operation #dmg tmp *= #fgCut mb',
                             'scoreboard players operation #dmg tmp /= #c100 mb',
                             'execute if score #dmg tmp matches ..0 run scoreboard players set #dmg tmp 1'])
        self.w('pause', [
            '# Hook pause (the fight froze: player dead / reviving / selection screen / no body). Low gravity drops by',
            '# itself (mboss/main clears #mbLowG every tick and the module tick does not run while paused; the module',
            '# keeps #fgLowG and asks again after the resume). The running pattern may drop what would hang (its pause).',
            '# The kit\'s ground decals go (the frozen hazards keep their framework markers; the decals would run on and',
            '# flash early), so does a kit screen flash / pop still on the title line (only while one is up: vBig, so a',
            '# selection screen\'s own title is left alone); a dead or reviving player clears the kit cards itself.',
            sc_set('#fgFlash', 0),
            f'function {KF}tele/clear',
            f'execute if entity @a[tag=player,scores={{vBig=1..}}] run {K.hud("flash_end")}',
            F('p/pause_d')])
        self.w('resume', ['# Hook resume: nothing to restore (module timers live in the body tick and simply continue;',
                          '# the low-gravity request comes back with the first module tick).'])
        self.w('cleanup', [
            '# Hook cleanup (no executor; idempotent; fight end, abort, run end, map change, wipe, uninstall): module',
            '# fake players back to their defaults (the meter, the field, low gravity: the framework\'s player_reset clears',
            '# #mbLowG, rlk:tick removes the modifiers), the module\'s storage, every kit card and the kit\'s HUD flags',
            '# (meter, low gravity, groggy, hint), the field banner if it still shows. Module entities carry rlk_mb_aux.',
            F('hud/banner_cut'),
            F('ai/vars'),
            'data remove storage rlk:mboss fg',
            f'function {KF}clear',
            K.hud('clear')])
        self.w('uninstall', [
            '# Hook uninstall (no executor; rlk:uninstall via the framework, for every module): the rig, its props, the',
            '# rig objectives the manifest names, every module entity, the module storage, the fx kit (cards, objectives',
            '# fk*, the #fk* fake players, storage rlk:fgkit, its schedules; its stub rig while it has one); the framework',
            '# removes mb, the rlk_mb_aux entities and the low-gravity modifiers (mboss/uninstall -> mboss/lowg_rem).',
            R('kill'), R('prop/clear'),
            f'function {KF}uninstall',
            'kill @e[tag=rlk_mb_fg_pat]',
            'kill @e[tag=rlk_mb_fg_fx]',
            'kill @e[type=minecraft:marker,tag=rlk_mb_fg_kept]',
            'data remove storage rlk:mboss fg']
            + [f'scoreboard objectives remove {o}' for o in A.RIG_OBJECTIVES])
        rl = [
            '# Hook reload (@s = body after /reload; every aux entity is gone: rig parts, hazards, props, markers). HP and',
            '# the module scores are kept; the state is re-derived from them (butterfly S3 / S4: nothing is assumed):',
            '#   a break in progress -> a fresh groggy; a groggy goes on; a recovery ends (cruise);',
            '#   the field opening (pattern 20) -> the field up at the centre (meter open, low gravity), the opening waves;',
            '#   the pack-up (22) -> cruise; any other field stage resumes at the centre (the AI restarts that stage).',
            F('ai/consts'),
            'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
            'execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
            sc_set('#fgX', 0),
            'execute if score #fgSt mb matches 6 run scoreboard players set #fgX mb 1',
            'execute if score #fgPat mb matches 20 run scoreboard players set #fgX mb 2',
            'execute if score #fgField mb matches 1 run scoreboard players set #fgX mb 2',
            'execute if score #fgPat mb matches 22 run scoreboard players set #fgX mb 3',
            'execute if score #fgField mb matches 5 run scoreboard players set #fgX mb 3',
            F('p/cancel'),
            sc_set('#mbNoLeash', 0), sc_set('#fgMv', 0), sc_set('#fgBrkQ', 0), sc_set('#fgBrkFx', 0),
            'tag @s remove rlk_mb_inv',
            R('init'), R('spawn'),
            f'execute if score #fgX mb matches 1 run {F("field/drop")}',
            f'execute if score #fgX mb matches 2 run {F("field/up")}',
            f'execute if score #fgX mb matches 3 run {F("field/now_c")}',
            f'execute if score #fgField mb matches 2..4 run {F("field/rig_f")}',
            f'execute if score #fgField mb matches 0 run {F("field/rig_c")}',
            F('u/crack_d'),
            f'execute if score #fgX mb matches 1 run return run {F("groggy/begin")}',
            f'execute if score #fgSt mb matches 3 run return run {F("groggy/rig")}',
            f'execute if score #fgSt mb matches 4 run return run {F("recover/end")}',
            sc_set('#fgCool', 20),
            F('ai/enter')]
        self.w('reload', rl)
        self.w('bars', [
            '# Hook bars (@s = body, every tick in intro/fight). Under-bar: the break meter while the field is open (violet,',
            f'# hits of {A.METER_N}; full during the break), groggy = time left (green), recovery = progress (green), pattern =',
            '# progress (Geo), cruise idle = cruise patterns done toward the next field (gold). Text lines: hud/*.',
            'execute if score #mbSt mb matches 0 run return 0',
            f'execute if score #fgOpen mb matches 1 run return run {F("hud/bar_meter")}',
            f'execute if score #fgSt mb matches {ST["break"]} run return run {F("hud/bar_full")}',
            f'execute if score #fgSt mb matches {ST["groggy"]} run return run {F("hud/bar_groggy")}',
            f'execute if score #fgSt mb matches {ST["recover"]} run return run {F("hud/bar_recover")}',
            f'execute if score #fgPat mb matches 1.. unless score #fgPNew mb matches 1 unless score #fgPRel mb matches 1 run return run {F("hud/bar_pattern")}',
            f'execute if score #fgField mb matches 0 run {F("hud/bar_next")}'])
        self.w('hz_vis', ['# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end). Visual ids = pattern id x 10 + k.',
                          F('p/vis')])
        self.w('pj_end', ['# Hook pj_end (@s = prop, #pjEv, #pjKeep preset). Routed by the prop\'s mbId (= pattern id).',
                          F('p/pj_end')])
        self.w('test', [
            '# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}). See test/help.',
            '$scoreboard players set #fgTst mb $(id)',
            'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
            f'execute as {BODY} at @s run {F("test/run")}'])

    # -----------------------------------------------------------------------------------------
    def intro(self):
        F, R, g = self.F, self.R, self.g
        self.w('intro/setup', [
            '# @s = the new body (from the spawn hook), at it: module state, the rig folded (dormant, eye shut), the entrance.',
            F('ai/consts'), F('ai/vars'),
            R('init'), R('spawn'), g.form('dormant'), g.look('off'), g.play('entrance'),
            '# the kit\'s HUD flags of an earlier fight off (this also starts the kit\'s line version #fkHudV)',
            K.hud('clear'),
            F('form/hitbox_c'), F('hud/refresh'), F('cfx/ent_setup')])
        c = lambda t: INTRO_CLIP + t
        self.w('intro_tick', [
            f'# Hook intro_tick (@s = body, #mbT = 1.. intro clock; untargetable until intro_end). Clip tick t = intro t - {INTRO_CLIP}:',
            f'# dormant, the clank ({ENT_CLANK}), the pods unfold ({ENT_UNFOLD}), the eye opens ({ENT_EYE}: nameplate), the rise',
            f'# ({ENT_RISE}..{ENT_RISEN}), the fight at intro {INTRO_DONE} (the idle turn to the player flows into the first pick).',
            R('tick'),
            at_t('#mbT', c(ENT_CLANK), F('cfx/clank')),
            at_t('#mbT', c(ENT_UNFOLD), F('cfx/unfold')),
            at_t('#mbT', c(ENT_EYE), F('intro/name')),
            at_t('#mbT', c(ENT_RISE), F('cfx/rise')),
            f'execute if score #mbT mb matches {c(ENT_RISE)}..{c(ENT_RISEN)} run {F("cfx/rise_dust")}',
            at_t('#mbT', (INTRO_DONE, 999), F('intro/done'))])
        self.w('intro/name', [
            '# The eye opens: the nameplate on the sub-line, the idle look.',
            f'data modify storage rlk:mboss sub set value [{{text:"{A.BOSS["sub"]}",color:"{A.LINE_HEX}",bold:true}}]',
            g.look('idle'), F('cfx/eye')])
        self.w('intro/done', [
            '# The rise is over: end of the untargetable intro; the device turns to the player during the cooldown.',
            'function rlk:mboss/intro_end',
            sc_set('#fgCool', 16),
            F('ai/enter')])

    # -----------------------------------------------------------------------------------------
    def ai(self):
        F, R, g = self.F, self.R, self.g
        self.w('ai/state', ['# @s = body. One AI state per tick (the pattern slot runs after it, see p/run).'] + [
            f'execute if score #fgSt mb matches {ST[k]} run return run {F(fn)}'
            for k, fn in (('idle', 'ai/idle'), ('groggy', 'groggy/tick'), ('recover', 'recover/tick'), ('break', 'brk/tick'))])
        self.w('ai/enter', ['# Enter idle (#fgCool set by the caller). Idle is never groggy: the kit\'s " · 그로기" flag goes (recovery',
                            '# end, test cuts, reloads).',
                            sc_set('#fgSt', ST['idle']), sc_set('#fgT', 0),
                            f'execute if data storage {K.STO} hud{{grog:1b}} run {K.hud("groggy_off")}',
                            F('hud/refresh')])
        self.w('ai/idle', [f'execute if score #fgField mb matches 1.. run return run {F("ai/idle_f")}', F('ai/idle_c')])
        self.w('ai/idle_c', [
            f'# @s = body, cruise: track the player ({TURN_C} deg/t), keep {KEEP_MIN}-{KEEP_MAX} b (glide in at 0.18 b/t, out at 0.15 b/t, only',
            f'# inside r {L.num(A.BODY_R)}), decide when the cooldown is over.',
            f'function rlk:mboss/mv/turn {{max:{TURN_C}}}',
            'execute if score #fgCool mb matches 1.. run scoreboard players remove #fgCool mb 1',
            F('ai/loco'),
            f'execute if score #fgCool mb matches ..0 run {F("ai/next")}'])
        self.w('ai/idle_f', [
            f'# @s = body at the centre, field: no travel, slow tracking ({TURN_F} deg/t), decide when the cooldown is over.',
            f'function rlk:mboss/mv/turn {{max:{TURN_F}}}',
            'execute if score #fgCool mb matches 1.. run scoreboard players remove #fgCool mb 1',
            f'execute if score #fgCool mb matches ..0 run {F("ai/next")}'])
        self.w('ai/loco', [
            f'execute unless entity {PLAYER.replace("limit=1", f"distance=..{KEEP_MAX},limit=1")} run return run {F("ai/glide_in")}',
            f'execute if entity {PLAYER.replace("limit=1", f"distance=..{KEEP_MIN},limit=1")} run return run {F("ai/glide_out")}',
            f'execute unless score #fgMv mb matches 0 run {F("ai/mv0")}'])
        self.w('ai/glide_in', [f'execute unless score #fgMv mb matches 1 run {F("ai/mv1")}', g.bstep('toward', 0.18)])
        self.w('ai/glide_out', [f'execute unless score #fgMv mb matches 2 run {F("ai/mv2")}', g.bstep('away', 0.15)])
        for m, clip in ((0, None), (1, 'glide'), (2, 'glide')):
            lines = [f'# Locomotion mode {m} (0 hover, 1 glide in, 2 glide out).', sc_set('#fgMv', m)]
            lines.append(g.play(clip) if clip else g.play('idle_cruise'))
            self.w(f'ai/mv{m}', lines)
        self.w('ai/next', [
            '# Next action, only here (a pattern boundary). Test request > lock 1-6 (cruise pattern only) > the field',
            '# stage (1 finish the opening, 2 the opening waves, 4 the closing waves, 5 the pack-up) > lock 11-12 (that',
            f'# field pattern only, after a normal field opening) / 17 (the field cycle only) > field patterns (until {FIELD_T} t',
            f'# of them, then the closing waves) > cruise (after {FIRST_FIELD_N} cruise patterns, later {NEXT_FIELD_N}: the field).',
            'execute if score #fgPat mb matches 1.. run return 0',
            f'execute unless score #fgMv mb matches 0 run {F("ai/mv0")}',
            f'execute if score #fgReq mb matches 1.. run return run {F("ai/req")}',
            f'execute if score #mbLock mb matches 1..6 run return run {F("ai/lock_c")}',
            f'execute if score #fgField mb matches 1 run return run {F("field/up")}',
            f'execute if score #fgField mb matches 2 run return run {F("ai/waves_open")}',
            f'execute if score #fgField mb matches 4 run return run {F("ai/waves_close")}',
            f'execute if score #fgField mb matches 5 run return run {F("ai/pack")}',
            f'execute if score #mbLock mb matches 11..12 run return run {F("ai/lock_f")}',
            f'execute if score #mbLock mb matches 17 run return run {F("ai/lock_cycle")}',
            f'execute if score #fgField mb matches 3 run return run {F("ai/next_f")}',
            F('ai/next_c')])
        self.w('ai/next_c', [f'execute if score #fgCruN mb >= #fgCruLim mb run return run {F("field/go")}', F('ai/pick_c')])
        self.w('ai/next_f', [f'execute if score #fgFT mb matches {FIELD_T}.. run return run {F("field/closer")}', F('ai/pick_f')])
        self.w('ai/waves_open', ['# The opening 「인력 충격파」 x3.', sc_set('#fgWvK', 1), sc_set('#fgPick', 21), F('ai/go')])
        self.w('ai/waves_close', ['# The closing 「인력 충격파」 x3 (an unbroken field).', sc_set('#fgWvK', 2), sc_set('#fgPick', 21), F('ai/go')])
        self.w('ai/pack', ['# The pack-up (service 22).', sc_set('#fgPick', 22), F('ai/go')])
        self.w('field/go', ['# The cruise stretch is over: the field opening (service 20) at this decision point.', sc_set('#fgPick', 20), F('ai/go')])
        self.w('field/closer', [f'# {FIELD_T} t of field patterns: the closing waves.', sc_set('#fgField', FLD['close']), F('ai/waves_close')])
        req = ['# A test request (#fgReq = pattern id): the device state follows the pattern at once.',
               'scoreboard players operation #fgPick mb = #fgReq mb', sc_set('#fgReq', 0),
               'scoreboard players operation #fgLast mb = #fgPick mb']
        for p in self.cru + [FIELD_IN]:
            req.append(f'execute if score #fgPick mb matches {p.id} if score #fgField mb matches 1.. run {F("field/now_c")}')
        for p in self.fld:
            req.append(f'execute if score #fgPick mb matches {p.id} unless score #fgField mb matches 3 run {F("field/now_f")}')
        req += [f'execute if score #fgPick mb matches 21..22 run {F("field/now_f")}',
                'execute if score #fgPick mb matches 21 run scoreboard players operation #fgWvK mb = #fgReqK mb',
                'execute if score #fgPick mb matches 21 if score #fgWvK mb matches 1 run scoreboard players set #fgField mb 2',
                'execute if score #fgPick mb matches 21 if score #fgWvK mb matches 2 run scoreboard players set #fgField mb 4',
                f'execute if score #fgPick mb matches 22 run scoreboard players set #fgField mb {FLD["pack"]}',
                F('ai/go')]
        self.w('ai/req', req)
        self.w('ai/lock_c', [f'execute if score #fgField mb matches 1.. run {F("field/now_c")}',
                             'scoreboard players operation #fgPick mb = #mbLock mb', F('ai/go')])
        self.w('ai/lock_f', [f'execute if score #fgField mb matches 0 run return run {F("field/go")}',
                             'scoreboard players operation #fgPick mb = #mbLock mb', F('ai/go')])
        self.w('ai/lock_cycle', [f'execute if score #fgField mb matches 0 run return run {F("field/go")}', F('field/closer')])
        bands = A.BANDS
        mel, far = int(A.MELEE * 10), int(A.FAR * 10)
        for f, plist in (('c', self.cru), ('f', self.fld)):
            cand = [f'# Candidates ({f}): in the bag, allowed in the current range band, not the last one.',
                    '# #fgC<id> = its draw weight in this band (0 = no candidate).']
            cand_any = [f'# Fallback candidates ({f}): allowed in the band (bag and last ignored).']
            for p in plist:
                cand.append(sc_set(f'#fgC{p.id}', 0))
                cand_any.append(sc_set(f'#fgC{p.id}', 0))
                for b in p.bands:
                    wt = p.weight[b]
                    cand.append(f'execute if score #fgBag{p.id} mb matches 1 if score #fgBand mb matches {bands[b]} '
                                f'unless score #fgLast mb matches {p.id} run scoreboard players set #fgC{p.id} mb {wt}')
                    cand_any.append(f'execute if score #fgBand mb matches {bands[b]} unless score #fgLast mb matches {p.id} '
                                    f'run scoreboard players set #fgC{p.id} mb {wt}')
            for lines in (cand, cand_any):
                lines.append(sc_set('#fgCn', 0))
                lines += [f'scoreboard players operation #fgCn mb += #fgC{p.id} mb' for p in plist]
            self.w(f'ai/cand_{f}', cand)
            self.w(f'ai/cand_any_{f}', cand_any)
            self.w(f'ai/refill_{f}', [f'# The {f} bag ran dry for this band: refill it with every normal pattern of the state.']
                   + [sc_set(f'#fgBag{p.id}', 1) for p in plist])
            draw = ['# #fgR = 0..#fgCn-1 (sum of the weights) -> the candidate whose weight range holds it.', sc_set('#fgPick', 0)]
            for p in plist:
                draw.append(f'execute if score #fgPick mb matches 0 if score #fgC{p.id} mb matches 1.. if score #fgR mb < #fgC{p.id} mb '
                            f'run scoreboard players set #fgPick mb {p.id}')
                draw.append(f'scoreboard players operation #fgR mb -= #fgC{p.id} mb')
            draw += [f'execute if score #fgPick mb matches {p.id} run scoreboard players set #fgBag{p.id} mb 0' for p in plist]
            self.w(f'ai/draw_{f}', draw)
            first = plist[0].id
            self.w(f'ai/pick_{f}', [
                f'# @s = body. Range-filtered, weighted shuffle bag of the {"cruise" if f == "c" else "field"} state, no immediate repeat:',
                '# ' + ', '.join(f'{p.key} ' + '/'.join(b + (f'x{p.weight[b]}' if p.weight[b] > 1 else '') for b in p.bands) for p in plist)
                + f' (melee <= {A.MELEE} b, far >= {A.FAR} b).',
                'function rlk:mboss/mv/dist',
                'scoreboard players operation #fgDist mb = #mbDist mb',
                sc_set('#fgBand', bands['mid']),
                f'execute if score #fgDist mb matches ..{mel} run scoreboard players set #fgBand mb {bands["melee"]}',
                f'execute if score #fgDist mb matches {far}.. run scoreboard players set #fgBand mb {bands["far"]}',
                F(f'ai/cand_{f}'),
                f'execute if score #fgCn mb matches 0 run {F(f"ai/refill_{f}")}',
                f'execute if score #fgCn mb matches 0 run {F(f"ai/cand_{f}")}',
                f'execute if score #fgCn mb matches 0 run {F(f"ai/cand_any_{f}")}',
                f'execute if score #fgCn mb matches 0 run scoreboard players set #fgC{first} mb 1',
                'execute if score #fgCn mb matches 0 run scoreboard players set #fgCn mb 1',
                'execute store result score #fgR mb run random value 0..999',
                'scoreboard players operation #fgR mb %= #fgCn mb',
                F(f'ai/draw_{f}'),
                f'execute if score #fgPick mb matches 0 run scoreboard players set #fgPick mb {first}',
                'scoreboard players operation #fgLast mb = #fgPick mb',
                F('ai/go')])
        go = ['# Into the pattern slot: p/run starts it this tick (pattern clock 0 = clip tick 0).',
              sc_set('#fgSt', ST['pattern']), 'scoreboard players operation #fgPat mb = #fgPick mb', sc_set('#fgPNew', 1),
              f'execute unless score #fgMv mb matches 0 run {sc_set("#fgMv", 0)}']
        go += [f'execute if score #fgPick mb matches {p.id} run scoreboard players add #fgCruN mb 1' for p in self.cru]
        self.w('ai/go', go)
        rec = ['# A slot pattern finished (#fgPDone = its id): recovery before the next decision.', sc_set('#fgCool', 20)]
        rec += [sc_set_if('#fgPDone', p.id, '#fgCool', p.recover) for p in self.pats]
        rec.append(F('ai/enter'))
        self.w('ai/recover', rec)
        self.w('ai/pat_done', [
            '# From p/finish: the field sequence moves on; any other pattern recovers. (No early return on a released',
            '# pattern: the butterfly\'s S2 froze the AI there.)',
            f'execute if score #fgPDone mb matches 20 run return run {F("field/opened")}',
            f'execute if score #fgPDone mb matches 21 if score #fgWvK mb matches 1 run return run {F("field/patterns")}',
            f'execute if score #fgPDone mb matches 21 if score #fgWvK mb matches 2 run return run {F("field/packing")}',
            f'execute if score #fgPDone mb matches 22 run return run {F("field/down")}',
            F('ai/recover')])

    # -----------------------------------------------------------------------------------------
    def slot(self):
        F, g = self.F, self.g
        begin = ['# @s = body. First tick of the slot pattern #fgPat: clock -lead (0 for most), the clip at clock 0, start.',
                 sc_set('#fgPNew', 0), sc_set('#fgPT', 0), sc_set('#fgPEnd', 0), sc_set('#fgPRel', 0), sc_set('#fgPMax', 200),
                 sc_set('#fgPLen', 200), sc_set('#fgPCol', A.L.ELEM_TO_BU[A.EL_GEO])]
        begin += [sc_set_if('#fgPat', p.id, '#fgPMax', p.max_len) for p in self.pats]
        begin += ['# expected end for the progress bar (a pattern that decides a shorter run sets #fgPLen itself: g.set_len)']
        begin += [sc_set_if('#fgPat', p.id, '#fgPLen', p.length) for p in self.pats]
        begin += [sc_set_if('#fgPat', p.id, '#fgPT', -p.lead) for p in self.pats if p.lead]
        begin += [F('hud/refresh'),
                  f'execute if score #fgPT mb matches 0 run {F("p/clip_d")}',
                  F('p/start'), f'execute if score #fgPat mb matches 20.. run {F("p/svc")}']
        self.w('p/begin', begin)
        self.w('p/run', [
            '# @s = body. The slot: start on the tick it was picked, then tick with #fgPT = 1, 2, ... (= clip tick).',
            f'execute if score #fgPNew mb matches 1 run return run {F("p/begin")}',
            'scoreboard players add #fgPT mb 1',
            f'execute if score #fgPT mb matches 0 run {F("p/clip_d")}',
            F('p/tick'),
            '# the service patterns (20 field opening, 22 pack-up) carry core mechanics on their clocks',
            f'execute if score #fgPat mb matches 20.. run {F("p/svc")}',
            f'execute if score #fgPEnd mb matches 1 run return run {F("p/finish")}',
            f'execute if score #fgPT mb >= #fgPMax mb run {F("p/finish")}'])
        kills = ['kill @e[type=minecraft:marker,tag=rlk_mb_fg_lock]', 'kill @e[type=minecraft:marker,tag=rlk_mb_fg_kept]',
                 'kill @e[tag=rlk_mb_fg_pat]']
        self.w('p/finish', [
            '# @s = body. The pattern ended (p/end or its max_len): clear the slot and every marker / entity a pattern kept',
            '# (rlk_mb_fg_lock, rlk_mb_fg_kept, rlk_mb_fg_pat: no later run aims at this run\'s markers), tell the owner.',
            'scoreboard players operation #fgPDone mb = #fgPat mb',
            sc_set('#fgPat', 0), sc_set('#fgPEnd', 0), sc_set('#fgPT', 0),
            sc_set('#mbNoLeash', 0),
            'tag @s remove rlk_mb_inv'] + kills + [
            F('ai/pat_done'),
            sc_set('#fgPRel', 0)])
        self.w('p/end', ['# Called by a pattern (any executor): it is done; the core finishes it after this tick\'s pattern tick.',
                         sc_set('#fgPEnd', 1)])
        self.w('p/release', ['# Called by a pattern (any executor): its dangerous part is over; the pattern bar hides while the',
                             '# pattern finishes a harmless tail. The slot stays busy until p/end; the AI is not affected.',
                             sc_set('#fgPRel', 1)])
        self.w('p/cancel', [
            '# Stop the slot pattern now (tests, death, the break, reload). Callers run rlk:mboss/lib_clear first when hazards',
            '# must go. The pattern\'s cancel runs as the caller (the body when it exists): it must use selectors, not @s.',
            f'execute if score #fgPat mb matches 1.. unless score #fgPNew mb matches 1 run {F("p/cancel_d")}',
            sc_set('#fgPat', 0), sc_set('#fgPNew', 0), sc_set('#fgPEnd', 0), sc_set('#fgPT', 0), sc_set('#fgPRel', 0),
            sc_set('#mbNoLeash', 0)] + kills + [
            'kill @e[tag=rlk_mb_fg_fxw]',
            'execute if score #mbSt mb matches 1 run tag @e[tag=rlk_mb_body] remove rlk_mb_inv'])
        for name, doc in (('start', 'start (clock -lead)'), ('tick', 'tick (#fgPT -lead+1 ..)'), ('cancel_d', 'cancel')):
            target = 'cancel' if name == 'cancel_d' else name
            self.w(f'p/{name}', [f'# GENERATED dispatcher: the running pattern\'s {doc}, by #fgPat.']
                   + [f'execute if score #fgPat mb matches {p.id} run return run {F(f"p/{p.key}/{target}")}' for p in self.pats])
        self.w('p/clip_d', ['# GENERATED: the running pattern\'s clip at clock 0 (the core plays it; #fgPT = clip tick).']
               + [f'execute if score #fgPat mb matches {p.id} run return run {g.play(p.clip)}' for p in self.pats])
        self.w('p/pause_d', ['# GENERATED dispatcher: the running pattern\'s optional pause (the fight just froze), by #fgPat.',
                             'execute unless score #fgPat mb matches 1.. run return 0',
                             'execute if score #fgPNew mb matches 1 run return 0']
               + [f'execute if score #fgPat mb matches {p.id} run return run {F(f"p/{p.key}/pause")}'
                  for p in self.pats if self.g.has(f'p/{p.key}/pause')])
        vis = ['# GENERATED: hz_vis events of hazards with #hzVis = pattern id x 10 + k (k 1-9), @s = hazard marker.',
               'scoreboard players operation #fgV mb = @s mbHzV', 'scoreboard players operation #fgV mb /= #c10 mb']
        vis += [f'execute if score #fgV mb matches {p.id} run return run {F(f"p/{p.key}/vis")}'
                for p in self.pats if self.g.has(f'p/{p.key}/vis')]
        self.w('p/vis', vis)
        pj = ['# GENERATED: pj_end of props whose mbId = pattern id (@s = prop; #pjEv, #pjKeep preset).']
        pj += [f'execute if score @s mbId matches {p.id} run return run {F(f"p/{p.key}/pj_end")}'
               for p in self.pats if self.g.has(f'p/{p.key}/pj_end')]
        self.w('p/pj_end', pj)
        self.w('p/svc', [
            '# Core mechanics on the service patterns\' clocks (their pattern files own only fx): the field opening (20)',
            f'# 0 = the stage, {WARP_OUT} = warp-out (untargetable, to the centre), {WARP_LEN} = warp-in clip, {FIN_UNFOLD} = the unfold',
            f'# (the meter opens, targetable), {FIN_BANNER} = the banner and low gravity; the pack-up (22) 0 = meter and low gravity off.',
            f'execute if score #fgPat mb matches 20 if score #fgPT mb matches 0 run return run {F("field/warp_begin")}',
            f'execute if score #fgPat mb matches 20 if score #fgPT mb matches {WARP_OUT} run return run {F("field/warp")}',
            f'execute if score #fgPat mb matches 20 if score #fgPT mb matches {WARP_LEN} run return run {g.play("warp_in_field")}',
            f'execute if score #fgPat mb matches 20 if score #fgPT mb matches {FIN_UNFOLD} run return run {F("field/open")}',
            f'execute if score #fgPat mb matches 20 if score #fgPT mb matches {FIN_BANNER} run return run {F("field/banner")}',
            f'execute if score #fgPat mb matches 22 if score #fgPT mb matches 0 run return run {F("field/close")}'])

    # -----------------------------------------------------------------------------------------
    def field(self):
        F, R, g = self.F, self.R, self.g
        self.w('field/warp_begin', ['# Field opening clock 0 (@s = body): the stage; the halo flips while it noses up.',
                                    sc_set('#fgField', FLD['warp']), F('hud/refresh')])
        self.w('field/warp', [
            f'# Field opening clock {WARP_OUT} (@s = body): warp-out flash over the old spot (the glitch marker), untargetable,',
            '# teleported to the arena centre facing the player (invisible until the warp-in clip).',
            'kill @e[tag=rlk_mb_fg_fxw]',
            'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_fg_fx","rlk_mb_fg_fxw"]}',
            F('cfx/warp_out'),
            'tag @s add rlk_mb_inv',
            F('u/centre')])
        self.w('field/open', [
            f'# Field opening clock {FIN_UNFOLD} (@s = body): the unfold; targetable again; the meter opens at 0/{A.METER_N} (crack 0;',
            '# the kit\'s meter on the sub-line), the field look, the field hitbox, the field damage cut',
            f'# ({CUT} %), the first field\'s hint for {HINT_T} t (the kit\'s hint_on / hint_off).',
            'tag @s remove rlk_mb_inv',
            sc_set('#fgOpen', 1), sc_set('#fgBrk', 0), sc_set('#fgBrkT', -1000000), sc_set('#fgBrkFx', 0), sc_set('#fgBrkQ', 0),
            sc_set('#fgCrack', 0), R('crack/0'), g.look('field'), F('form/hitbox_f'),
            'scoreboard players add #fgFN mb 1', sc_set('#fgHintT', 0),
            K.hud('meter_open'),
            f'execute if score #fgFN mb matches 1 run {K.hud("hint_on")}',
            F('cfx/unfold_f'), F('hud/refresh')])
        self.w('field/banner', [
            f'# Field opening clock {FIN_BANNER}: low gravity (#fgLowG -> #mbLowG every tick), the kit\'s banner "{BANNER}"',
            f'# (actionbar {BANNER_T} t, the big icon, its sound; the start gametime #fgBanG lets a break / cut drop it early), the',
            '# low-gravity icon on the name line, the typed caption.',
            sc_set('#fgLowG', 1),
            K.hud('banner_field'),
            'execute store result score #fgBanG mb run time query gametime',
            K.hud('lowg_on'),
            g.say(BANNER, '#D9C8FF', 1, 50, 1)])
        self.w('field/close', [
            '# The pack-up begins (@s = body): the meter closes, low gravity and the damage cut end (the kit\'s meter, icon',
            '# and hint leave the lines), the idle look.',
            sc_set('#fgOpen', 0), sc_set('#fgLowG', 0), F('hud/kit_off'), g.look('idle'), F('hud/refresh')])
        self.w('field/opened', ['# The field opening is over: the opening waves next.', sc_set('#fgField', FLD['open']),
                                sc_set('#fgCool', 1), F('ai/enter')])
        self.w('field/patterns', [f'# The opening waves are over: field patterns for {FIELD_T} t.', sc_set('#fgField', FLD['patterns']),
                                  sc_set('#fgFT', 0), sc_set('#fgCool', 14), F('ai/enter')])
        self.w('field/packing', ['# The closing waves are over: the pack-up next.', sc_set('#fgField', FLD['pack']),
                                 sc_set('#fgCool', 1), F('ai/enter')])
        self.w('field/down', [
            f'# The pack-up is over (@s = body): cruise again, {NEXT_FIELD_N} cruise patterns before the next field; the cruise hitbox.',
            F('field/drop'), sc_set('#fgCool', 20), F('ai/enter')])
        self.w('field/drop', [
            '# The field state ends without its sequence (pack-up done, the break, a reload): stage 0, the next field after',
            f'# {NEXT_FIELD_N} cruise patterns, meter / low gravity / cut off, the cruise hitbox.',
            sc_set('#fgField', FLD['cruise']), sc_set('#fgWvK', 0), sc_set('#fgFT', 0), sc_set('#fgOpen', 0), sc_set('#fgLowG', 0),
            sc_set('#fgCruN', 0), sc_set('#fgCruLim', NEXT_FIELD_N), F('hud/kit_off'), F('form/hitbox_c'), F('hud/refresh')])
        self.w('field/rig_f', ['# @s = body: the rig in the field form at the centre (reload, tests).',
                               F('u/centre'), g.form('field'), g.look('field'), g.play('field_idle'), F('form/hitbox_f')])
        self.w('field/rig_c', ['# @s = body: the rig in the cruise form (reload, tests).',
                               g.form('cruise'), g.look('idle'), g.play('idle_cruise'), F('form/hitbox_c')])
        self.w('field/now_f', [
            '# Instant field (tests, the reload of a field opening): at the centre in the field form, the meter open,',
            f'# low gravity, the field patterns stage ({FIELD_T} t from now).',
            'tag @s remove rlk_mb_inv', 'kill @e[tag=rlk_mb_fg_fxw]',
            F('field/rig_f'), F('field/open'), F('field/banner'),
            sc_set('#fgField', FLD['patterns']), sc_set('#fgFT', 0), sc_set('#fgWvK', 0)])
        self.w('field/up', ['# Finish an interrupted field opening (a test cut, a reload): the field at once, then the opening waves.',
                            F('field/now_f'), sc_set('#fgField', FLD['open'])])
        self.w('field/now_c', [
            '# Instant cruise (tests, the reload of a pack-up): meter / low gravity off, the cruise form, crack 0.',
            F('field/close'), F('field/drop'), g.form('cruise'), g.play('idle_cruise'), sc_set('#fgCrack', 0), R('crack/0')])
        self.w('field/tick', [
            '# @s = body, every module tick while #fgField >= 1: the field-pattern clock, the first field\'s hint, the floating',
            '# pebbles around the player while low gravity holds.',
            f'execute if score #fgField mb matches {FLD["patterns"]} run scoreboard players add #fgFT mb 1',
            f'execute if score #fgOpen mb matches 1 if score #fgHintT mb matches ..{HINT_T} run scoreboard players add #fgHintT mb 1',
            f'execute if score #fgHintT mb matches {HINT_T} if score #fgFN mb matches 1 run {F("hud/hint_end")}',
            'scoreboard players operation #fgM mb = #fgClk mb', 'scoreboard players operation #fgM mb %= #fgK10 mb',
            f'execute if score #fgLowG mb matches 1 if score #fgM mb matches 0 at {PLAYER} run {F("cfx/pebbles")}'])

    # -----------------------------------------------------------------------------------------
    def meter(self):
        F, R, g = self.F, self.R, self.g
        self.w('brk/count', [
            '# @s = body (module tick after a counted hit): the crack stage (hits 0-4 / 5-9 / 10-14 / 15-19 = 0-3); the',
            '# kit\'s per-count feedback with #fkM = the count, as the body (the rig anchor) at the field core',
            f'# ({L.num(A.CORE_FIELD_H)} b up): the newest pip flashes white for 4 t, the crack glint, the brass ping + a note rising',
            '# with the count, and at 5 / 10 / 15 the bubble crack fx, its sound and the rig crack/<n>.',
            sc_set('#fgBrkFx', 0),
            'scoreboard players operation #fgX mb = #fgBrk mb',
            'scoreboard players operation #fgX mb /= #fgK5 mb',
            'execute if score #fgX mb matches 4.. run scoreboard players set #fgX mb 3',
            f'execute unless score #fgX mb = #fgCrack mb run {F("brk/stage")}',
            'scoreboard players operation #fkM mb = #fgBrk mb',
            f'execute positioned ~ ~{L.num(A.CORE_FIELD_H)} ~ run {K.hud("meter_hit")}',
            F('hud/refresh')])
        if KIT_CRACKS:
            stage = ['# The core bubble shows the next crack stage (#fgCrack, read by reloads and tests). The kit\'s meter_hit',
                     '# cracks the rig on the counts 5 / 10 / 15; the core does it only for a stage reached another way (test 31).',
                     'scoreboard players operation #fgCrack mb = #fgX mb',
                     f'execute unless score #fgBrk mb matches 5 unless score #fgBrk mb matches 10 unless score #fgBrk mb matches 15 run {F("u/crack_d")}']
        else:
            stage = ['# The core bubble shows the next crack stage (#fgCrack, read by reloads and tests). The kit\'s meter_hit',
                     f'# cracks its own stub rig ({K.RIG()}) while the real rig is not merged, so the core cracks its rig here.',
                     'scoreboard players operation #fgCrack mb = #fgX mb',
                     F('u/crack_d')]
        self.w('brk/stage', stage)
        self.w('u/crack_d', ['# The rig crack look of #fgCrack (0-3 the meter stages, 4 burst).']
               + [f'execute if score #fgCrack mb matches {n} run return run {R(f"crack/{n}")}' for n in A.CRACKS])
        self.w('brk/begin', [
            f'# @s = body: the {A.METER_N}th count broke the field (역장 붕괴). Every threat goes (hazards, props, pulls, glides:',
            '# lib_clear; the running pattern, waves included: p/cancel), the meter / low gravity / the damage cut end, the',
            f'# field state ends; the break plays ({BRK_LEN} t: bubble, burst at {BRK_BURST}, tilt, wobble, sink), then groggy {GROGGY} t.',
            '# The kit: every decal goes (tele/clear), the banner if it still shows, the meter / low-gravity icon / hint',
            '# (field/drop -> hud/kit_off); " · 그로기" on the name line from here to the end of the recovery.',
            sc_set('#fgBrkQ', 0),
            'function rlk:mboss/lib_clear',
            F('p/cancel'),
            f'function {KF}tele/clear',
            F('hud/banner_cut'),
            F('field/drop'),
            F('hud/groggy_on'),
            '# #fgT -1: the AI state runs brk/tick later this same tick, so #fgT = the break clip tick',
            sc_set('#fgSt', ST['break']), sc_set('#fgT', -1), sc_set('#fgMv', 0),
            g.play('break'),
            g.say('역장 붕괴', '#FFE7A0', 2, 40, 2),
            F('cfx/break_start'),
            F('hud/refresh')])
        self.w('brk/tick', [
            'scoreboard players add #fgT mb 1',
            f'execute if score #fgT mb matches {BRK_BURST} run {F("brk/burst")}',
            f'execute if score #fgT mb matches {BRK_WOBBLE} run {F("cfx/groan")}',
            f'execute if score #fgT mb matches {BRK_LEN}.. run {F("groggy/begin")}'])
        self.w('brk/burst', ['# The bubble bursts: crack 4, the gold flash and the floor ring.', sc_set('#fgCrack', 4), R('crack/4'),
                             F('cfx/break_burst')])

    # -----------------------------------------------------------------------------------------
    def groggy(self):
        F, R, g = self.F, self.R, self.g
        self.w('groggy/begin', [
            f'# @s = body, after the break (or a reload / test): {GROGGY} t slumped (ring centre about 3 b, core on the floor):',
            f'# hittable, no attacks, no tracking. The cruise counters restart here ({NEXT_FIELD_N} patterns to the next field; a',
            '# test cut of the groggy keeps them: butterfly S8). No damage bonus.',
            sc_set('#fgSt', ST['groggy']), sc_set('#fgT', 0), sc_set('#mbNoLeash', 0), sc_set('#fgMv', 0),
            sc_set('#fgBrk', 0), sc_set('#fgCruN', 0), sc_set('#fgCruLim', NEXT_FIELD_N),
            F('hud/groggy_on'),
            F('groggy/rig'),
            F('cfx/groggy'),
            F('hud/refresh')])
        self.w('groggy/rig', ['# The groggy rig (clip, look) and hitbox.', g.form('cruise'), g.play('groggy'), g.look('groggy'),
                              F('form/hitbox_g')])
        self.w('groggy/tick', [
            'scoreboard players add #fgT mb 1',
            'scoreboard players operation #fgM mb = #fgT mb', 'scoreboard players operation #fgM mb %= #fgK20 mb',
            f'execute if score #fgM mb matches 0 run {F("cfx/groggy_spark")}',
            f'execute if score #fgT mb matches {GROGGY}.. run {F("recover/begin")}'])
        self.w('recover/begin', [
            f'# Groggy over: re-level ({REC_FLIP} t), the core flips to the top ({REC_LEN - REC_FLIP} t), compact again.',
            sc_set('#fgSt', ST['recover']), sc_set('#fgT', 0), g.play('recover'), g.look('idle'),
            sc_set('#fgCrack', 0), R('crack/0'), F('cfx/recover'), F('hud/refresh')])
        self.w('recover/tick', ['scoreboard players add #fgT mb 1',
                                f'execute if score #fgT mb matches {REC_FLIP} run {F("cfx/flip")}',
                                f'execute if score #fgT mb matches {REC_LEN}.. run {F("recover/end")}'])
        self.w('recover/end', ['# Back to the cruise rotation.', F('form/hitbox_c'), g.look('idle'), sc_set('#fgCool', 16), F('ai/enter')])

    # -----------------------------------------------------------------------------------------
    def forms(self):
        def hitbox(hit, scale, label):
            w_, h_ = L.num(float(hit[0])), L.num(float(hit[1]))
            return [f'# {label} hitbox: click shield {w_} x {h_} b (also for a re-created shield: cur.hit), husk scale {L.num(float(scale))}.',
                    f'data modify storage rlk:mboss cur.hit set value {{w:{w_}f,h:{h_}f}}',
                    f'execute as @e[type=minecraft:interaction,tag=rlk_mshield] if score @s msid = {BODY} msid '
                    f'run data merge entity @s {{width:{w_}f,height:{h_}f}}',
                    f'execute as {BODY} run attribute @s minecraft:scale base set {L.num(float(scale))}']
        self.w('form/hitbox_c', hitbox(*HIT['c'], 'Cruise (the registry)'))
        self.w('form/hitbox_f', hitbox(*HIT['f'], 'Field (the core hangs exposed under the ring, the stack spread)'))
        self.w('form/hitbox_g', hitbox(*HIT['g'], 'Groggy (slumped)'))

    # -----------------------------------------------------------------------------------------
    def death(self):
        F, R, g = self.F, self.R, self.g
        self.w('death_start', [
            '# Hook death_start (@s = body; hazards, props, pull and movement already cleared, bars hidden). The pattern goes,',
            '# the field ends (meter, low gravity, cut). The death clip: the seam flickers out, the halo and the drill pods',
            '# fall, the ring sinks tilted 40 degrees, then it scales out. Mechanical sounds only (deathSnd false).',
            '# The kit: every decal goes, the banner if it still shows, every HUD flag off (meter, low gravity, hint, groggy).',
            F('p/cancel'),
            f'function {KF}tele/clear',
            F('hud/banner_cut'),
            K.hud('clear'),
            sc_set('#fgOpen', 0), sc_set('#fgLowG', 0), sc_set('#fgField', 0), sc_set('#fgBrkQ', 0),
            sc_set('#fgSt', ST['dead']),
            R('prop/clear'),
            g.play('death'),
            F('cfx/death_start')])
        self.w('death_tick', [
            '# Hook death_tick (@s = body, #mbT = 1.. until cur.death): the clip runs while the rig ticks; it must NOT tick',
            f'# after its kill at {DEATH_LEN} (it would respawn).',
            at_t('#mbT', (1, DEATH_LEN - 1), R('tick')),
            at_t('#mbT', (4, 4), F('cfx/death_flicker')), at_t('#mbT', (9, 9), F('cfx/death_flicker')),
            at_t('#mbT', 12, g.look('off')),
            at_t('#mbT', D_DROP, F('cfx/death_drop')),
            at_t('#mbT', D_SINK, F('cfx/death_sink')),
            at_t('#mbT', D_OUT, F('cfx/death_out')),
            at_t('#mbT', DEATH_LEN, R('kill'))])

    # -----------------------------------------------------------------------------------------
    def hud(self):
        F, g = self.F, self.g
        self.w('hud/extra', [
            '# Name-line suffix: 순항 (gold) in cruise, 역장 (violet) during the warp and the pack-up; the kit\'s flags',
            '# (put_extra) supply the rest: " · 역장" + the badge while the meter is open, the low-gravity icon, " · 그로기"',
            '# (the break, groggy and recovery).',
            'data modify storage rlk:mboss extra set value []',
            f'execute if score #fgField mb matches 0 run data modify storage rlk:mboss extra append value {{text:"   순항",color:"{GOLD_HEX}",bold:false}}',
            'execute if score #fgField mb matches 1.. unless score #fgOpen mb matches 1 run data modify storage rlk:mboss extra append value {text:"   역장",color:"#9C86E8",bold:false}',
            K.hud('put_extra')])
        sub = ['# Third line: what the device is doing. While the meter is open the core writes only the running field',
               '# pattern ("패턴  <label>") and the kit\'s put_sub appends the meter: badge, 역장, the 20 pips in groups of five',
               '# (the newest one white for 4 t), the "n/20" digits and the first field\'s hint (font rlk:mboss_fg).',
               'execute if score #mbSt mb matches 0 run data modify storage rlk:mboss sub set value []',
               'execute if score #mbSt mb matches 0 run return 0',
               f'data modify storage rlk:mboss sub set value [{{text:"순항",color:"{GOLD_HEX}",bold:true}}]',
               'execute if score #fgField mb matches 1.. run data modify storage rlk:mboss sub set value [{text:"역장",color:"#C58BFF",bold:true}]',
               'execute if score #fgOpen mb matches 1 run data modify storage rlk:mboss sub set value []']
        for p in self.pats:
            sub.append(f'execute if score #fgSt mb matches {ST["pattern"]} if score #fgPat mb matches {p.id} run data modify storage rlk:mboss sub set value '
                       f'[{{text:"패턴  ",color:"#A8A8A8"}},{{text:"{p.label}",color:"{"#C9B8F5" if p.state == "f" else "#F2E2B0"}"}}]')
        sub += [f'execute if score #fgSt mb matches {ST["break"]} run data modify storage rlk:mboss sub set value '
                f'[{{text:"{A.GLYPH["break"]}",font:"{A.FONT}",color:"white"}},{{text:" 역장 붕괴",color:"#FFE7A0",bold:true}}]',
                f'execute if score #fgSt mb matches {ST["groggy"]} run data modify storage rlk:mboss sub set value [{{text:"그로기  ",color:"#9FE8A0",bold:true}},{{text:"공격할 기회",color:"#C8E8C8"}}]',
                f'execute if score #fgSt mb matches {ST["recover"]} run data modify storage rlk:mboss sub set value [{{text:"그로기  ",color:"#9FE8A0",bold:true}},{{text:"다시 떠오른다",color:"#C8E8C8"}}]',
                f'execute if score #fgOpen mb matches 1 run {K.hud("put_sub")}']
        self.w('hud/sub', sub)
        self.w('hud/refresh', ['# Both text lines from the current state (on every state, stage and meter change, and when the kit rebuilt',
                               '# its HUD components: #fkHudV, compared every module tick).',
                               F('hud/extra'), F('hud/sub'),
                               'scoreboard players operation #fgHudV mb = #fkHudV mb'])
        self.w('hud/kit_off', ['# The field is over (the pack-up, the break, a reload, a test): the kit\'s meter, low-gravity icon and hint',
                               '# leave the lines (only the flags still on: each kit call rebuilds its components; the caller refreshes',
                               '# the lines).',
                               f'execute if data storage {K.STO} hud{{open:1b}} run {K.hud("meter_close")}',
                               f'execute if data storage {K.STO} hud{{lowg:1b}} run {K.hud("lowg_off")}',
                               f'execute if data storage {K.STO} hud{{hint:1b}} run {K.hud("hint_off")}'])
        self.w('hud/hint_end', [f'# The first field\'s hint has shown {HINT_T} t: off.', K.hud('hint_off'), F('hud/refresh')])
        self.w('hud/groggy_on', ['# " · 그로기" on the name line (the break and groggy; ai/enter drops it).',
                                 f'execute unless data storage {K.STO} hud{{grog:1b}} run {K.hud("groggy_on")}'])
        self.w('hud/banner_cut', [
            f'# Drop the kit\'s field banner while it still shows (within {BANNER_T} t of field/banner; any executor): the break,',
            '# death, a test cut, a cleanup. Another actionbar message is never cut.',
            'execute store result score #fgX mb run time query gametime',
            'scoreboard players operation #fgX mb -= #fgBanG mb',
            f'execute if score #fgX mb matches 0..{BANNER_T} run {K.hud("banner_end")}'])
        self.w('hud/bar_meter', ['scoreboard players operation #buSub bu = #fgBrk mb', sc_set_bu('#buSubMax', A.METER_N), sc_set_bu('#buSubCol', 1)])
        self.w('hud/bar_full', [sc_set_bu('#buSub', A.METER_N), sc_set_bu('#buSubMax', A.METER_N), sc_set_bu('#buSubCol', 1)])
        self.w('hud/bar_groggy', [sc_set_bu('#buSub', GROGGY), 'scoreboard players operation #buSub bu -= #fgT mb',
                                  sc_set_bu('#buSubMax', GROGGY), sc_set_bu('#buSubCol', 9)])
        self.w('hud/bar_recover', ['scoreboard players operation #buSub bu = #fgT mb', sc_set_bu('#buSubMax', REC_LEN), sc_set_bu('#buSubCol', 9)])
        self.w('hud/bar_pattern', ['# Pattern progress against its real end (#fgPLen), empty at the end; Geo colour.',
                                   'scoreboard players operation #buSub bu = #fgPLen mb', 'scoreboard players operation #buSub bu -= #fgPT mb',
                                   'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
                                   'execute if score #buSub bu > #fgPLen mb run scoreboard players operation #buSub bu = #fgPLen mb',
                                   'scoreboard players operation #buSubMax bu = #fgPLen mb',
                                   'scoreboard players operation #buSubCol bu = #fgPCol mb'])
        self.w('hud/bar_next', ['# Cruise: patterns done toward the next field (gold).',
                                'scoreboard players operation #buSub bu = #fgCruN mb',
                                'scoreboard players operation #buSubMax bu = #fgCruLim mb',
                                'execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1',
                                sc_set_bu('#buSubCol', 8)])

    # -----------------------------------------------------------------------------------------
    def tests(self):
        F, R, g = self.F, self.R, self.g
        cru = ', '.join(f'{p.id} {p.label}' for p in self.cru)
        fld = ', '.join(f'{p.id} {p.label}' for p in self.fld)
        HELP = [
            ('1-6', f'순항 패턴 ({cru})'), ('11-12', f'역장 패턴 ({fld}), 즉시 역장'),
            ('20', '역장 생성(순간이동 · 펼침 · 저중력)'), ('21', '「인력 충격파」 ×3(시작)'), ('22', '「인력 충격파」 ×3(끝) → 접기'),
            ('23', '접기만'), ('30', '역장 붕괴(20타)'), ('31', '역장 계수 +5'), ('40', '그로기'), ('41', '저중력 켜고 끄기'),
            ('42', '체력 50% 미만 세 겹 충격파 켜고 끄기'), ('99', '대기로'),
            ('lock 1-6 / 11-12 / 17', '그 순항 패턴만 / (역장 안에서) 그 역장 패턴만 / 역장 순환만'),
            ('시작', '/function rlk:mboss/test/start {id:\\"fieldgen\\"} 또는 #mbForce mb 3'),
        ]
        txt = f'[{{text:"[실험성 역장 발생 장치 테스트] ",color:"{GOLD_HEX}",bold:true}}' + ''.join(
            f',{{text:"{k}",color:"yellow"}},{{text:" {v}  ",color:"gray"}}' for k, v in HELP) + ']'
        self.w('test/help', ['tellraw @a[tag=player] ' + txt])
        self.w('test/cut', [
            '# @s = body: stop whatever runs (hazards, props, pull, movement, the slot pattern, the break / groggy / recovery)',
            '# and re-derive the rig and the hitbox from the field stage (butterfly S3: never a stale rig form).',
            'function rlk:mboss/lib_clear',
            F('p/cancel'),
            R('prop/clear'),
            f'function {KF}tele/clear',
            F('hud/banner_cut'),
            sc_set('#fgMv', 0), sc_set('#fgBrkQ', 0),
            f'execute if score #fgSt mb matches {ST["groggy"]}..{ST["break"]} run {sc_set("#fgCrack", 0)}',
            '# a cut field opening (invisible, untargetable, maybe not at the centre yet) finishes at once',
            f'execute if score #fgField mb matches 1 run {F("field/up")}',
            f'execute if score #fgField mb matches 2.. run {F("field/rig_f")}',
            f'execute if score #fgField mb matches 0 run {F("field/rig_c")}',
            F('u/crack_d'),
            sc_set('#fgCool', 10),
            F('ai/enter')])
        run = ['# @s = body, #fgTst = the requested test id.']
        for lo, hi in ((1, 6), (11, 12)):
            run += [f'execute if score #fgTst mb matches {lo}..{hi} run {F("test/cut")}',
                    f'execute if score #fgTst mb matches {lo}..{hi} run scoreboard players operation #fgReq mb = #fgTst mb',
                    f'execute if score #fgTst mb matches {lo}..{hi} run return run {sc_set("#fgCool", 1)}']
        for tid, req, k in ((20, 20, 0), (21, 21, 1), (22, 21, 2), (23, 22, 0)):
            run += [f'execute if score #fgTst mb matches {tid} run {F("test/cut")}',
                    f'execute if score #fgTst mb matches {tid} run {sc_set("#fgReqK", k)}',
                    f'execute if score #fgTst mb matches {tid} run {sc_set("#fgReq", req)}',
                    f'execute if score #fgTst mb matches {tid} run return run {sc_set("#fgCool", 1)}']
        run += [f'execute if score #fgTst mb matches 30 unless score #fgOpen mb matches 1 run {F("test/cut")}',
                f'execute if score #fgTst mb matches 30 unless score #fgOpen mb matches 1 run {F("field/now_f")}',
                f'execute if score #fgTst mb matches 30 run {sc_set("#fgBrk", A.METER_N)}',
                f'execute if score #fgTst mb matches 30 run return run {sc_set("#fgBrkQ", 1)}',
                f'execute if score #fgTst mb matches 31 if score #fgOpen mb matches 1 run scoreboard players add #fgBrk mb 5',
                f'execute if score #fgTst mb matches 31 if score #fgBrk mb matches {A.METER_N}.. run {sc_set("#fgBrk", A.METER_N - 1)}',
                f'execute if score #fgTst mb matches 31 if score #fgOpen mb matches 1 run {sc_set("#fgBrkFx", 1)}',
                'execute if score #fgTst mb matches 31 run return 0',
                f'execute if score #fgTst mb matches 40 run {F("test/cut")}',
                f'execute if score #fgTst mb matches 40 run {F("field/drop")}',
                f'execute if score #fgTst mb matches 40 run return run {F("groggy/begin")}',
                f'execute if score #fgTst mb matches 41 run return run {F("test/lowg")}',
                f'execute if score #fgTst mb matches 42 run return run {F("test/tri")}',
                f'execute if score #fgTst mb matches 99 run return run {F("test/cut")}',
                F('test/help')]
        self.w('test/run', run)
        self.w('test/lowg', ['# Low gravity on / off by hand (the jump check in both views); the field sets it again at its banner.',
                             'scoreboard players set #fgX mb 1', 'execute if score #fgLowG mb matches 1 run scoreboard players set #fgX mb 0',
                             'scoreboard players operation #fgLowG mb = #fgX mb',
                             f'execute if score #fgLowG mb matches 1 run {K.hud("lowg_on")}',
                             f'execute if score #fgLowG mb matches 0 run {K.hud("lowg_off")}',
                             'execute if score #fgLowG mb matches 1 run tellraw @a[tag=player] {text:"[테스트] 저중력 켬",color:"gray"}',
                             'execute if score #fgLowG mb matches 0 run tellraw @a[tag=player] {text:"[테스트] 저중력 끔",color:"gray"}'])
        self.w('test/tri', ['# The HP < 50 % triple front of the 3rd wave by hand.',
                            'scoreboard players set #fgX mb 1', 'execute if score #fgTri mb matches 1 run scoreboard players set #fgX mb 0',
                            'scoreboard players operation #fgTri mb = #fgX mb',
                            'execute if score #fgTri mb matches 1 run tellraw @a[tag=player] {text:"[테스트] 세 겹 충격파 켬",color:"gray"}',
                            'execute if score #fgTri mb matches 0 run tellraw @a[tag=player] {text:"[테스트] 세 겹 충격파 끔",color:"gray"}'])

    # -----------------------------------------------------------------------------------------
    def cfx(self):
        """The core's own visuals: vanilla particles and mechanical / brass vanilla sounds (plan: anvil, chain, piston,
        beacon, respawn anchor, amethyst, trial spawner, breeze charge, crafter). The meter count, the crack stages and
        the banner are the kit's now (hud/meter_hit, hud/banner_field); the entrance, warp, break, groggy and death
        visuals here are mapped to kit presets by the stage-2 specs (scratchpad mb3/spec E, S1-S4)."""
        g = self.g
        G, GD, WG, V, VD = A.GOLD, A.GOLD_DEEP, A.WHITE_GOLD, A.VIOLET, A.VIOLET_DEEP
        at = lambda y, *cmds: [f'execute at @s run {c}' for c in cmds]
        fx = {
            'ent_setup': ['# @s = body: the folded device on the floor, dust and a low mechanical hum.',
                          g.particle('block{block_state:"minecraft:tuff"}', '~ ~0.3 ~', (1.2, 0.1, 1.2), 0, 10),
                          g.sound('block.respawn_anchor.ambient', 0.6, 0.6)],
            'clank': [g.sound('block.anvil.place', 0.7, 0.6), g.sound('block.chain.place', 1.0, 0.8),
                      g.sound('block.piston.extend', 0.8, 0.7), g.particle('crit', '~ ~2 ~', (1.0, 0.4, 1.0), 0.1, 8)],
            'unfold': [g.sound('block.chain.hit', 0.9, 0.9), g.sound('block.piston.contract', 0.8, 0.8),
                       g.sound('block.crafter.craft', 0.8, 0.9), *g.ring_dust(G, 3.2, 12, 2.0, 1.2)],
            'eye': [g.sound('block.beacon.activate', 0.6, 1.4), g.particle('end_rod', '~ ~3.2 ~', (0.3, 0.3, 0.3), 0.02, 6)],
            'rise': [g.sound('block.respawn_anchor.charge', 0.8, 1.0), g.sound('block.trial_spawner.about_to_spawn_item', 0.8, 0.8)],
            'rise_dust': [g.dust(G, 1.0, '~ ~0.2 ~', (1.6, 0.05, 1.6), 1)],
            'warp_out': ['# @s = body at the old spot: the white-cyan pillar and the warp sounds.',
                         *[g.particle('end_rod', f'~ ~{y} ~', (0.2, 0.4, 0.2), 0.02, 3) for y in (1, 3, 5, 7)],
                         g.sound('block.respawn_anchor.deplete', 1.0, 1.2), g.sound('entity.enderman.teleport', 0.8, 0.6)],
            'warp_in': ['# @s = body at the centre: the warp-in flash.',
                        g.particle('flash{color:[0.92,0.86,1.0,1.0]}', '~ ~5 ~', (0, 0, 0), 0, 1),
                        g.particle('end_rod', '~ ~5 ~', (1.2, 1.2, 1.2), 0.08, 20),
                        g.sound('block.beacon.power_select', 1.0, 0.8), g.sound('entity.enderman.teleport', 0.8, 0.8)],
            'unfold_f': [*g.ring_dust(V, 3.8, 16, 3.8, 1.4), g.sound('block.amethyst_block.chime', 1.0, 0.8),
                         g.sound('block.chain.place', 0.9, 0.7), g.sound('block.crafter.craft', 0.8, 0.7)],
            'pebbles': ['# At the player\'s feet (never at the eyes): pebbles and ash drifting up (low gravity).',
                        g.particle('white_ash', '~ ~0.6 ~', (3.0, 0.4, 3.0), 0, 6),
                        g.particle('end_rod', '~ ~0.4 ~', (3.0, 0.2, 3.0), 0.005, 1),
                        g.dust(V, 0.9, '~ ~0.3 ~', (2.5, 0.2, 2.5), 2)],
            'break_start': [g.sound('block.respawn_anchor.deplete', 1.0, 0.7),
                            g.particle('end_rod', '~ ~3.8 ~', (0.9, 0.9, 0.9), 0.02, 12)],
            'break_burst': [g.particle('flash{color:[1.0,0.9,0.62,1.0]}', '~ ~3.8 ~', (0, 0, 0), 0, 1),
                            g.dust(WG, 1.6, '~ ~3.8 ~', (1.2, 1.2, 1.2), 20), *g.ring_dust(GD, 4.0, 20, 0.2, 1.4),
                            g.sound('block.glass.break', 1.0, 0.8), g.sound('block.amethyst_cluster.break', 1.0, 0.7),
                            g.sound('block.respawn_anchor.deplete', 1.0, 0.5)],
            'groan': [g.sound('block.anvil.place', 0.8, 0.5), g.sound('entity.iron_golem.damage', 0.7, 0.6)],
            'groggy': [g.sound('block.beacon.deactivate', 0.9, 0.7), g.particle('smoke', '~ ~2 ~', (0.8, 0.5, 0.8), 0.01, 10)],
            'groggy_spark': [g.particle('electric_spark', '~ ~2.6 ~', (0.8, 0.6, 0.8), 0.05, 4), g.sound('block.chain.hit', 0.3, 1.6)],
            'recover': [g.sound('block.piston.contract', 0.9, 0.7), g.sound('block.chain.place', 0.9, 0.8)],
            'flip': [g.sound('block.crafter.craft', 0.9, 0.8), g.sound('block.beacon.power_select', 0.7, 1.2),
                     g.particle('end_rod', '~ ~4.6 ~', (0.4, 0.3, 0.4), 0.02, 6)],
            'death_start': [g.sound('block.beacon.deactivate', 1.0, 0.6), g.sound('block.respawn_anchor.deplete', 1.0, 0.6),
                            g.particle('electric_spark', '~ ~4 ~', (1.5, 0.6, 1.5), 0.1, 12)],
            'death_flicker': [g.sound('block.beacon.deactivate', 0.6, 1.6), g.particle('electric_spark', '~ ~4 ~', (1.5, 0.4, 1.5), 0.1, 8)],
            'death_drop': [g.sound('block.anvil.land', 0.9, 0.7), g.sound('block.chain.break', 1.0, 0.8),
                           g.particle('block{block_state:"minecraft:gold_block"}', '~ ~0.5 ~', (2.0, 0.2, 2.0), 0, 20)],
            'death_sink': [g.sound('block.anvil.place', 0.9, 0.4), g.sound('entity.iron_golem.damage', 0.8, 0.5),
                           g.particle('poof', '~ ~0.5 ~', (2.0, 0.2, 2.0), 0.02, 16)],
            'death_out': [g.sound('block.glass.break', 1.0, 0.6), g.sound('block.amethyst_cluster.break', 1.0, 0.6),
                          g.dust(G, 1.6, '~ ~1.5 ~', (2.0, 1.2, 2.0), 30), g.dust(V, 1.2, '~ ~1.5 ~', (2.0, 1.2, 2.0), 12)],
        }
        for name, lines in fx.items():
            body = [ln for ln in lines if ln.startswith('#')] + [f'execute at @s run {ln}' for ln in lines if not ln.startswith('#')]
            if name == 'pebbles':
                body = [ln for ln in lines]
            self.w(f'cfx/{name}', [f'# Core fx {name} (vanilla particles / sounds; @s = body unless noted).'] + body)

    # -----------------------------------------------------------------------------------------
    def services(self):
        """The core's service patterns: their fx timelines (the mechanics run from p/svc)."""
        g, F = self.g, self.F
        key, tl = FIELD_IN.key, TL(g, FIELD_IN.key)
        tl.at(0, f'execute at @s facing entity {PLAYER} feet run tp @s ~ ~ ~ ~ 0',
              g.sound('block.chain.place', 0.9, 0.7), g.sound('block.piston.extend', 0.8, 0.8))
        tl.at(6, g.sound('block.beacon.power_select', 0.8, 1.2))
        for t in range(WARP_OUT + 1, WARP_LEN, 2):
            tl.at(t, 'execute at @e[tag=rlk_mb_fg_fxw,limit=1] run ' + g.particle('reverse_portal', '~ ~3 ~', (0.8, 2.0, 0.8), 0.05, 6),
                  'execute at @e[tag=rlk_mb_fg_fxw,limit=1] run ' + g.dust(A.VIOLET_DEEP, 1.2, '~ ~3 ~', (0.6, 1.8, 0.6), 3))
        tl.at(WARP_LEN, 'kill @e[tag=rlk_mb_fg_fxw]', F('cfx/warp_in'))
        for t in range(FIN_UNFOLD, FIN_BANNER, 4):
            tl.at(t, *['execute at @s run ' + x for x in g.ring_dust(A.VIOLET, 3.8, 12, 3.8, 1.2)])
        tl.at(FIN_LEN, g.end())
        tl.write([f'# Field opening (core service 20; clip warp_out, then warp_in_field at {WARP_LEN}; @s = body): halo flip, warp-out',
                  f'# at {WARP_OUT}, violet glitch over the old spot, warp-in at the centre, unfold at {FIN_UNFOLD}, banner at {FIN_BANNER}.'],
                 [f'# {key} tick.'])
        g.pw(key, 'cancel', ['# The glitch marker (the core re-derives the field state: ai/next -> field/up).', 'kill @e[tag=rlk_mb_fg_fxw]'])
        key, tl = FIELD_OUT.key, TL(g, FIELD_OUT.key)
        tl.at(0, 'execute at @s run ' + g.particle('flash{color:[1.0,0.95,0.8,1.0]}', '~ ~0.5 ~', (0, 0, 0), 0, 1),
              'execute at @s run ' + g.particle('end_rod', '~ ~0.4 ~', (1.5, 0.2, 1.5), 0.05, 16),
              g.sound('block.respawn_anchor.set_spawn', 0.9, 0.8), g.sound('entity.breeze.wind_burst', 0.8, 0.7))
        for t in range(2, FOUT_LANCES, 4):
            tl.at(t, 'execute at @s run ' + g.dust(A.GOLD, 1.0, '~ ~1 ~', (1.2, 0.6, 1.2), 3))
        tl.at(FOUT_LANCES, g.sound('block.chain.place', 1.0, 0.7), g.sound('block.piston.extend', 0.9, 0.6))
        tl.at(FOUT_PACK, g.sound('block.piston.contract', 1.0, 0.6), g.sound('block.crafter.craft', 0.9, 0.7))
        tl.at(FOUT_LEN - 1, g.sound('block.chain.place', 0.8, 1.0))
        tl.at(FOUT_LEN, g.end())
        tl.write([f'# Pack-up (core service 22; clip field_end; @s = body at the centre): lift-off flash, rise, lances at {FOUT_LANCES},',
                  f'# the roll / pack at {FOUT_PACK}, compact at {FOUT_LEN}; the meter and low gravity ended at 0 (p/svc).'],
                 [f'# {key} tick.'])
        g.pw(key, 'cancel', ['# Nothing of its own lingers.'])
