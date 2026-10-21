"""아펩의 오아시스 파수꾼 (Apep) module core (AP-CORE; plan 3.3 / 7; ap_contract 1): the 17 framework hooks + prep
(cm.md 5.3), the phase machine E -> P1 -> T1 -> P2 -> CS -> P3 -> D, RES (registry + organisms), pools / floor / titles,
the main slot and its services, the play wrappers (yaw schedules) and the px-set driver (proxies per form / stance from
the rig manifest), capsules (the push request), the body park, the bars (incl. the Heart bar's frame), music, pause /
reload / cleanup / uninstall per phase (plan 7.2), the arena props and looks, the test commands, the kit stand-ins.

Owns F:boss/apep/** except rig/** (the rig generator), om/** (the org generator) and the kit's owned paths
(ap_fx_api.md 0.1); every owned file not written in this run is deleted, so a second run and any generator order give
the same bytes.
"""
import importlib
import json

from . import PATTERN_MODULES, SERVICE_MODULES
from . import api as A
from . import ai as AI
from .api import L, K, Gen, TL

NS = A.NS
OWN_TOP = A.ROOT                      # boss/apep (registry fn)
BODY, PLAYER, ARENA_M, HEART_M = A.BODY, A.PLAYER, A.ARENA_M, A.HEART_M
CY = A.CY
HUD_EVERY = 4
Q2_BLAST, Q2_POP = A.ev('aftermath', 'blast'), A.ev('aftermath', 'pop')     # 156, 189 (the Q2 countdown, RP3-2)
Q2_RED, Q2_GOLD = 2, 8                     # bossui under-bar codes: 2 the warm red-orange (#FF8A3D), 8 the gauge gold
PH = A.PH
T = A.TXT

# Core patterns (ap_contract 0.8: 10 move and 61 stance are AP-CORE's services)
SVC_MOVE = A.Pattern(10, 'move', '이동', 'service', None, recover=6, max_len=80, length=72)
SVC_STANCE = A.Pattern(61, 'stance', '자세 전환', 'service', None, recover=6, max_len=20, length=16)
CORE_PATS = (SVC_MOVE, SVC_STANCE)
# the ids of plan 12.2 / ap_contract 0.8 and their kinds (the build asserts every one exists)
NEED = {1: 'normal', 2: 'normal', 3: 'normal', 4: 'normal', 5: 'normal', 6: 'normal', 7: 'opener', 10: 'service',
        20: 'service', 31: 'normal', 32: 'scheduled', 33: 'normal', 34: 'normal', 35: 'normal', 36: 'chain',
        40: 'service', 60: 'service', 61: 'service', 50: 'seq', 51: 'seq'}
SEQ_KEYS = {50: 'entrance', 51: 'death'}
LABEL_HEX = '#E9E2B8'


def build():
    out = L.Out()
    g = Gen(out)
    pats = []
    for name in PATTERN_MODULES + SERVICE_MODULES:
        mod = importlib.import_module(f'{__package__}.{name}')
        for p in getattr(mod, 'PATTERNS', []):
            p.module = name
        pats.extend(getattr(mod, 'PATTERNS', []))
        g.owner = name
        mod.emit(g)
        for rel in A.REQ_FILES.get(name, ()):
            assert g.has(rel), f'{name}: required file {rel} was not written (ap_contract 1.6)'
    g.owner = 'core'
    for p in CORE_PATS:
        p.module = 'core'
        pats.append(p)
    ids = [p.id for p in pats]
    assert len(set(ids)) == len(ids), ids
    keys = [p.key for p in pats]
    assert len(set(keys)) == len(keys), keys
    for pid, kind in NEED.items():
        p = next((x for x in pats if x.id == pid), None)
        assert p is not None, f'pattern id {pid} missing (ap_contract 0.8)'
        assert p.kind == kind, (pid, p.kind, kind)
    core = Core(g, pats)
    core.emit()
    for p in pats:
        for f in A.REQ_HOOKS[p.kind]:
            assert g.has(f'p/{p.key}/{f}'), f'{p.module}: pattern {p.key} has no {f}'
        for h in p.hooks:
            assert g.has(f'p/{p.key}/{h}'), f'{p.module}: pattern {p.key} declares {h} but writes no file'
    removed = clean(out)
    normal = [p for p in pats if p.kind == 'normal']
    print(f'mboss apep: {len(g.files)} functions ({len(normal)} normal patterns, {len(pats) - len(normal)} other, modules '
          f'{", ".join(PATTERN_MODULES + SERVICE_MODULES)} + core), {removed} stale removed; rig manifest rig '
          f'({len(A.CLIPS)} clips); org manifest org.')
    notes = []
    if A.THEME_STUBBED:
        notes.append('WARN theme ap_oasis missing (AP-ARENA unmerged): api._THEME_FALLBACK used (stub arena, no props but '
                     'the lush water tiles, no gate crystals, no look swap)')
    for n in notes:
        print('  note: ' + n)
    for clip, event, default in sorted(set(A.EV_FALLBACKS)):
        print(f'  note: manifest clip {clip} has no event {event!r}; using tick {default}')


class KitOwned:
    DIRS = ('e', 'p', 'tele', 'dress', 'snd', 'hud', 'prop', 'test')
    FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')


def foreign():
    """Paths under F:boss/apep/ that other generators own: the rig's rig/, the org generator's om/, the kit's owned
    dirs / files (ap_fx_api.md 0.1; the kit manifest's "owned" when it exists). Returns (dirs, files)."""
    dirs = {'rig', 'om'} | {f'fx/{d}' for d in KitOwned.DIRS}
    files = {f'fx/{f}' for f in KitOwned.FILES}
    man = A._TOOLS / 'mboss_ap_fx_manifest.json'
    pre = f'data/rlk/function/{OWN_TOP}/'
    if man.exists():
        own = json.loads(man.read_text(encoding='utf-8')).get('owned', {})
        dirs |= {d[len(pre):] for d in own.get('dirs', []) if d.startswith(pre)}
        files |= {f[len(pre):-len('.mcfunction')] for f in own.get('files', []) if f.startswith(pre)}
    return dirs, files


def is_foreign(rel, dirs, files):
    return rel in files or any(rel == d or rel.startswith(d + '/') for d in dirs)


def clean(out):
    root = L.FN / OWN_TOP
    dirs, files = foreign()
    removed = 0
    for p in sorted(root.rglob('*.mcfunction')):
        rel = p.relative_to(root).with_suffix('').as_posix()
        if is_foreign(rel, dirs, files):
            assert p.resolve() not in out.written, f'the apep core wrote into a foreign path: {rel}'
            continue
        if p.resolve() not in out.written:
            p.unlink()
            removed += 1
    for p in sorted(root.rglob('*'), reverse=True):
        rel = p.relative_to(root).as_posix()
        if p.is_dir() and not is_foreign(rel, dirs, files) and not any(p.iterdir()):
            p.rmdir()
    return removed


def sc(name, v):
    return f'scoreboard players set {name} mb {int(v)}'


def sci(cond, v, name, val):
    return f'execute if score {cond} mb matches {v} run scoreboard players set {name} mb {int(val)}'


def bu(name, v):
    return f'scoreboard players set {name} bu {int(v)}'


def txt(t, col, bold=False):
    return f'{{text:"{t}",color:"{col}",bold:{"true" if bold else "false"}}}'


ENTITY_OBJ = ('apK', 'apS', 'apT', 'apL', 'apShd', 'apOC', 'apOI', 'apSock', 'apTok')
MODULE_TAGS = ('rlk_mb_ap_pat', 'rlk_mb_ap_kept', 'rlk_mb_ap_lock', 'rlk_mb_ap_pop', 'rlk_mb_ap_heart', 'rlk_mb_ap_heartd',
               'rlk_mb_ap_dome', 'rlk_mb_ap_domed', 'rlk_mb_ap_wall', 'rlk_mb_ap_wall_blade', 'rlk_mb_ap_stalk',
               'rlk_mb_ap_stalkd', 'rlk_mb_ap_seed', 'rlk_mb_ap_om', 'rlk_mb_ap_aft', 'rlk_mb_ap_burstq')


class Core:
    def __init__(self, g, pats):
        self.g, self.pats = g, pats
        self.F = g.fn
        self.by_id = {p.id: p for p in pats}

    def w(self, rel, lines):
        self.g.w(rel, lines)

    def pat(self, pid):
        return self.by_id[pid]

    def slot_pats(self):
        return [p for p in self.pats if p.kind != 'seq']

    def with_hook(self, hook):
        return [p for p in self.slot_pats() if self.g.has(f'p/{p.key}/{hook}')]

    # =========================================================================================
    def emit(self):
        self.consts_vars()
        self.utils()
        self.plays()
        self.px_sets()
        self.hooks()
        self.prep()
        self.intro()
        AI.emit(self)
        self.moves()
        self.stance_svc()
        self.slot()
        self.floor_tr()
        self.services()
        self.ready()
        self.push()
        self.arena()
        self.hud()
        self.death()
        self.tests()

    # -----------------------------------------------------------------------------------------
    def consts_vars(self):
        yw = []
        for name in A.YAW_CLIPS:
            c = A.CLIPS[name]
            yw.append(f'c{c["id"]}:[' + ','.join(str(int(round(v * 100))) for v in c['yaw']) + ']')
        self.w('ai/consts', [
            '# Module constants (spawn, reload): the moduli #apK<n> of Gen.every, the module\'s entity objectives',
            '# (ap_contract 0.3.3: apK kind, apS state, apT state clock, apL link, apShd shield pool, apOC / apOI org clip clock /',
            '# id, apSock Heart socket, apTok attack token) and the yaw schedules of the rig manifest (x 100, ap.yw.c<clip id>).']
            + [sc(f'#apK{n}', n) for n in Gen.MODULI]
            + [f'scoreboard objectives add {o} dummy' for o in ENTITY_OBJ]
            + ['data modify storage rlk:mboss ap.yw set value {' + ','.join(yw) + '}'])
        zero = ['#apPh', '#apTr', '#apPid', '#apPNew', '#apPT', '#apPEnd', '#apPMax', '#apPLen', '#apPRel', '#apPDone',
                '#apReq', '#apReqT', '#apNext', '#apArg', '#apLast', '#apPatN', '#apP3N', '#apChP', '#apChT',
                '#apAft1', '#apAftN', '#apAftCd', '#apZone', '#apBand', '#apBackT', '#apBkI', '#apBk0', '#apBk1', '#apBk2',
                '#apBackN', '#apBackH', '#apRim', '#apFc', '#apYawC', '#apYawT', '#apYaw0', '#apYawSg', '#apMvK', '#apMvT',
                '#apMvD', '#apFlash', '#apNoPush', '#apMov', '#apPark', '#apHide', '#apStance', '#apDist', '#apF', '#apS',
                '#apAs', '#apSide', '#apP1Done', '#apSeqT', '#apChainRun', '#apLastMv', '#apWide', '#apCol', '#apCFree',
                '#apPick', '#apBackN']
        zero += [f'#apCdE{p.id}' for p in self.pats if p.cooldown]
        zero = list(dict.fromkeys(zero))
        v = ['# Every fight-time fake player of the core back to its fight-start value (spawn, cleanup). The revival stage keeps',
             '# its own (#apHt #apWave #apClk #apTo #apFail ...: rev/clear).']
        v += [sc(k, 0) for k in zero]
        v += [sc('#apYawS', 1), sc('#apCool', 30), sc('#apHudQ', 1), sc('#apPx', -1), sc('#apPopC', -1000),
              sc('#apTot', 0)]
        self.w('ai/vars', v)

    # -----------------------------------------------------------------------------------------
    def utils(self):
        F = self.F
        lock_new = ['kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]',
                    f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_lock"]}}']
        self.w('u/lockp', ['# Marker rlk_mb_ap_lock on the floor under the player\'s body, pulled inside the walk disc (any executor).']
               + lock_new + [f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run {F("u/clamp_walk")}'])
        self.w('u/lockb', ['# Macro {d}: the lock d b in front of the player on the boss -> player line (as the body), clamped to',
                           f'# the idle disc r {L.num(A.IDLE_R)} (R\'s re-emergence point, plan 8.1 R).',
                           'kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]',
                           f'$execute at {PLAYER} facing entity {BODY} feet rotated ~ 0 positioned ^ ^ ^$(d) run summon minecraft:marker '
                           f'~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_lock"]}}',
                           f'execute as @e[type=minecraft:marker,tag=rlk_mb_ap_lock,limit=1] run {F("u/clamp_idle")}'])
        for name, r in A.CLAMPS.items():
            self.w(f'u/clamp_{name}', [f'# @s = a marker / the body: pulled toward the arena axis (0.5 b steps) until within {L.num(r)} b of it.',
                                       sc('#apCl', 0), F(f'u/clamp_{name}_s')])
            self.w(f'u/clamp_{name}_s', [
                f'execute at @s positioned ~ {CY} ~ if entity {ARENA_M.replace("limit=1", f"distance=..{L.num(r)},limit=1")} run return 0',
                'scoreboard players add #apCl mb 1', 'execute if score #apCl mb matches 80.. run return 0',
                f'execute at @s facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
                F(f'u/clamp_{name}_s')])
        self.w('u/step_here', [f'# @s = body, positioned at a proposed step: there if it stays inside the glide disc r {L.num(A.GLIDE_R)} (yaw kept).',
                               f'execute positioned ~ {CY} ~ unless entity {ARENA_M.replace("limit=1", f"distance=..{L.num(A.GLIDE_R)},limit=1")} run return fail',
                               f'tp @s ~ {CY} ~'])
        self.w('u/flash', ['# The hit flash of the hit proxy\'s part group (manifest proxies.layout flash; 0 / a direct body hit = body).']
               + [f'execute if score #apFlash mb matches {k} run return run {self.g.flash(grp)}' for k, grp in sorted(A.PX_FLASH.items())]
               + [self.g.flash('body')])

    # -----------------------------------------------------------------------------------------
    def plays(self):
        """AP:play/<clip>: the rig's play + (yaw clips) the yaw driver armed with the sign #apYawS (then reset to 1).
        turn_p3 is a rate loop (ap_contract D7): the AI turns with mv/turn {max:6} instead, so it is not driven here."""
        driven = [c for c in A.YAW_CLIPS if c != 'turn_p3']
        for clip in A.CLIP_NAMES:
            lines = [f'# Play {clip} ({A.clip_len(clip)} t, clip id {A.clip_id(clip)}) from its tick 0 (@s = the body). The',
                     '# px sets of the clip follow it (pxs/tick reads the rig clock); the stance / looks / hands are the rig\'s.',
                     f'function {A.play_fn(clip)}']
            if clip in driven:
                lines += ['# the yaw schedule of the manifest turns the anchor (sign #apYawS: -1 mirrors it)',
                          sc('#apYawC', A.clip_id(clip)), 'scoreboard players operation #apYawSg mb = #apYawS mb', sc('#apYawS', 1),
                          sc('#apYawT', -1), 'execute store result score #apYaw0 mb run data get entity @s Rotation[0] 100']
            else:
                lines += [sc('#apYawC', 0), sc('#apYawS', 1)]
            self.w(f'play/{clip}', lines)
        lens = {A.clip_id(c): A.clip_len(c) for c in driven}
        self.w('yaw/tick', ['# @s = body (module tick, before the rig tick): Rotation = start + sign x schedule[t] / 100; off at the',
                            '# clip end (the anchor keeps the final yaw).',
                            'scoreboard players add #apYawT mb 1']
               + [f'execute if score #apYawC mb matches {cid} if score #apYawT mb matches {n}.. run return run scoreboard players set #apYawC mb 0'
                  for cid, n in sorted(lens.items())]
               + ['execute store result storage rlk:mboss ap.ya.c int 1 run scoreboard players get #apYawC mb',
                  'execute store result storage rlk:mboss ap.ya.t int 1 run scoreboard players get #apYawT mb',
                  f'function {NS}yaw/get with storage rlk:mboss ap.ya',
                  'scoreboard players operation #apYd mb *= #apYawSg mb',
                  'scoreboard players operation #apYd mb += #apYaw0 mb',
                  'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #apYd mb'])
        self.w('yaw/get', ['$execute store result score #apYd mb run data get storage rlk:mboss ap.yw.c$(c)[$(t)]'])
        self.w('yaw/rebase', [
            '# @s = body (Gen.yaw_rebase(); AP-I2, requests RP1-1 / RP3-1): a pattern turned the body inside a yaw clip; the',
            '# driver keeps that facing: #apYaw0 = Rotation x 100 - sign x schedule[t], t = the tick it shows next (#apYawT + 1).',
            'execute unless score #apYawC mb matches 1.. run return 0',
            'execute store result score #apYaw0 mb run data get entity @s Rotation[0] 100',
            'execute store result storage rlk:mboss ap.ya.c int 1 run scoreboard players get #apYawC mb',
            'scoreboard players operation #apYd mb = #apYawT mb', 'scoreboard players add #apYd mb 1',
            'execute store result storage rlk:mboss ap.ya.t int 1 run scoreboard players get #apYd mb',
            sc('#apYd', 0), f'function {NS}yaw/get with storage rlk:mboss ap.ya',
            'scoreboard players operation #apYd mb *= #apYawSg mb',
            'scoreboard players operation #apYaw0 mb -= #apYd mb'])
        objs = [('heart', 'rlk_mb_ap_heart_bulb'), ('dome', 'rlk_mb_ap_dome_shell'), ('stalk', 'rlk_mb_ap_stalk_low'),
                ('wall', 'rlk_mb_ap_wall_blade')]
        self.w('obj/tick', [
            '# Any executor, once per module tick (E, phases 1-3, D; frozen while paused): every org object\'s clip step',
            '# (om/<object>/tick; RORG-3, AP-I2 requests RP1-2 / RP3-4 / RREV-1), each object only while its displays',
            '# exist. Before the stage and the main slot: a clip played in tick T shows its key 0 at T + 1.']
            + [f'execute if entity @e[type=minecraft:item_display,tag={tag},limit=1] run function {NS}om/{o}/tick'
               for o, tag in objs])

    # -----------------------------------------------------------------------------------------
    def px_sets(self):
        """The px sets (cm.md 9.4) through AP:px/<set> and the per-tick driver AP:pxs/tick (ap_contract 0.11 decision 2:
        the core applies the clips' px_sets, read after the rig tick from apRigC / apRigT, so `next` chains and loops
        follow; a set equal to the current one is skipped)."""
        F = self.F
        for name, i in A.PX_ID.items():
            hide = name in A.HIDDEN_SETS
            lines = [f'# The proxy set {name} (#apPx {i}): the framework px/state (cm.md 9.3: inv sets toggle rlk_mb_inv through',
                     '# rlk_mb_pxinv)' + ('; hidden (FN-13 / R10): the husk at scale 0.1 without its click shield.' if hide else
                                          '; visible: the husk back at the registry scale with its torso click shield.'),
                     sc('#apPx', i), L.px_state(name)]
            lines.append(f'execute as {BODY} run {F("u/hide_on" if hide else "u/hide_off")}')
            self.w(f'px/{name}', lines)
        self.w('u/hide_on', ['# @s = body: hidden (burrowed / parked): scale 0.1, no click shield (cm.md 5.5, FN-13).',
                             'execute if score #apHide mb matches 1 run return 0', sc('#apHide', 1),
                             f'function rlk:mboss/body_scale {{s:{L.num(A.HIDE_SCALE)}}}', 'tag @s add rlk_mb_noshield'])
        self.w('u/hide_off', ['# @s = body: visible again: the registry scale and the torso click shield (shield:true).',
                              'execute if score #apHide mb matches 0 run return 0', sc('#apHide', 0),
                              f'function rlk:mboss/body_scale {{s:{L.num(A.HUSK_SCALE)}}}', 'tag @s remove rlk_mb_noshield'])
        self.w('px/restate', ['# /reload: the proxy set again from #apPx (the framework re-spawned the proxies in px.set already).']
               + [f'execute if score #apPx mb matches {i} run return run {F(f"px/{name}")}' for name, i in A.PX_ID.items()]
               + [F('svc/px_rest')])
        # the driver: clip id -> its (t, set) entries
        ent = {}
        for clip in A.CLIP_NAMES:
            sets = A.px_sets(clip)
            n = A.clip_len(clip)
            rows = [(t, s) for t, s in sets if 0 <= t < n]
            if rows:
                ent[A.clip_id(clip)] = (clip, rows)
        ids = sorted(ent)

        def node(lo):
            if len(lo) <= 4:
                return [f'execute if score @s apRigC matches {c} run return run {F(f"pxs/c{c}")}' for c in lo]
            mid = len(lo) // 2
            out = []
            for part in (lo[:mid], lo[mid:]):
                nm = f'pxs/d{part[0]}_{part[-1]}'
                self.w(nm, node(part))
                out.append(f'execute if score @s apRigC matches {part[0]}..{part[-1]} run return run {F(nm)}')
            return out
        self.w('pxs/tick', ['# @s = body, after the rig tick: the px set of the clip tick shown now (#apStance mirrors the rig).',
                            'scoreboard players operation #apStance mb = @s apRigStance'] + node(ids))
        for c in ids:
            clip, rows = ent[c]
            self.w(f'pxs/c{c}', [f'# {clip}: {rows}']
                   + [f'execute if score @s apRigT matches {t} unless score #apPx mb matches {A.PX_ID[s]} run return run {F(f"px/{s}")}'
                      for t, s in rows])

    # -----------------------------------------------------------------------------------------
    def hooks(self):
        F, g = self.F, self.g
        sp = A.POINTS['spawn']
        self.w('spawn', [
            '# Hook spawn (@s = the arena marker at the centre): the chapter body (cb/body: no miniboss, rlk_mb_big, the torso',
            f'# click shield {A.BOSS["hit"]}) at POINTS spawn facing south (yaw {L.num(sp[3])}) toward the arrival; intro/setup.',
            f'execute positioned {L.num(sp[0])} {L.num(sp[1])} {L.num(sp[2])} rotated {L.num(sp[3])} 0 run function rlk:mboss/cb/body',
            f'execute as {BODY} at @s run {F("intro/setup")}'])
        tick = [
            '# Hook tick (@s = body, at it, fight state #mbSt 1). Order (ap_contract 1.2): clocks, the hit flash, the floor',
            '# events, the org objects\' clips (obj/tick, AP-I2), the phase-2 stage (revival), the idle AI / decision (phases 1',
            '# and 3, not in a cine), the main slot, the yaw driver, the push request (not in phase 2: the body is parked;',
            '# AP-I2 RREV-5), the HUD, the rig tick, then the px-set driver (after the rig tick).',
            'scoreboard players add #apFc mb 1',
            f'execute if score #apFlash mb matches 0.. run {F("u/flash")}', sc('#apFlash', -1),
            f'execute if score #apPh mb matches 1 run {F("ev/tick")}',
            f'execute if score #apPh mb matches 1 run {F("ai/ring")}',
            F('obj/tick'),
            f'execute if score #apPh mb matches 2 run {F("rev/tick")}',
            f'execute if score #apPid mb matches 0 unless score #mbCine mb matches 1 if score #apPh mb matches 1 run {F("ai/state")}',
            f'execute if score #apPid mb matches 0 unless score #mbCine mb matches 1 if score #apPh mb matches 3 run {F("ai/state")}',
            f'execute if score #apPid mb matches 1.. run {F("p/run")}',
            f'execute if score #apYawC mb matches 1.. run {F("yaw/tick")}',
            f'execute unless score #apPh mb matches 2 run {F("push/req")}',
            F('hud/tick')]
        tick += A.rig_tick_lines()
        tick += [F('pxs/tick'), sc('#apNoPush', 0)]
        self.w('tick', tick)
        self.w('on_hit', [
            '# Hook on_hit (@s = body inside combat/apply; #elem #dmg known; RES already from mres = mbRes<#elem>, cm.md 8):',
            '# the flash group of the hit proxy (#mbPart, cm.md 9.5; 0 = a direct body hit -> the body group).',
            'scoreboard players operation #apFlash mb = #mbPart mb'])
        self.w('aux_hit', [
            '# Hook aux_hit (@s = an aux inside combat/apply, #dmg after RES; cm.md 8): the 양육 immunity (U2, "buffed',
            f'# organisms can\'t be damaged"; NURTURE_MODE {A.NURTURE_MODE}: AP-REV tags the immune organism rlk_mb_ap_imm): #dmg 0 ->',
            '# aux/take shows "면역" and takes nothing. Otherwise the organism runtime (shield pools, ...: org/aux_hit).',
            'execute if entity @s[tag=rlk_mb_ap_imm] run return run scoreboard players set #dmg tmp 0',
            F('org/aux_hit')])
        self.w('incoming', [
            '# Hook incoming (@s = body inside combat/apply_mods, after the level factor and mres). RES is per element (the',
            '# registry res {"7":30,"*":10}, cm.md 8). The HP floor #mbFloor is the framework\'s (mboss/floor runs after this',
            '# hook, cm.md 7.2): phase 1 = 1 % of the P1 pool (svc/floor_p1), phase 3 = 0.'])
        pause = ['# Hook pause (the fight froze): the kit\'s telegraphs and overlays go; every active pattern\'s pause; phase 2:',
                 '# the walls are cleared (re-cast later) and the organisms freeze (the module tick does not run; plan 7.2).',
                 f'function {K.FN}tele/clear', K.hud('flash_end'), K.hud('banner_end'),
                 F('p/pause_d'),
                 f'execute if score #apPh mb matches 2 run {F("rev/pause")}']
        self.w('pause', pause)
        self.w('resume', ['# Hook resume: every active pattern\'s resume; a running Q2 is cancelled (domes removed, 300 t; plan',
                          '# 7.2); phase 2: rev/resume.',
                          F('p/resume_d'),
                          f'execute if score #apPid mb matches 32 run {F("aft/cancel")}',
                          f'execute if score #apPh mb matches 2 run {F("rev/resume")}'])
        self.w('aft/cancel', ['# Q2 cancelled (pause / reload, plan 7.2): its cancel (domes), the slot freed, the next Q2 300 t later.',
                              F('p/cancel'), F('dome/clear'), 'scoreboard players operation #apAftCd mb = #apFc mb',
                              f'scoreboard players add #apAftCd mb {A.Q2_CANCEL_CD}', sc('#apCool', 10)])
        kills = [f'kill @e[tag={t}]' for t in MODULE_TAGS]
        self.w('cleanup', [
            '# Hook cleanup (no executor; idempotent): the barrier walls (recorded blocks) first, then every module entity',
            '# (organisms and their models, the Heart, domes, walls, stalks, the seed, pattern entities, locks, the arena props),',
            '# the stage, the module fake players and storage, the kit\'s cards and HUD.',
            F('wall/clear'), F('org/clear'), F('rev/clear'), F('dome/clear')] + kills + [
            f'kill @e[tag=rlk_mb_ar_{A.AID}]', 'kill @e[type=minecraft:husk,tag=rlk_mb_ap_org]', F('ai/vars'),
            'data remove storage rlk:mboss ap',
            f'function {K.FN}clear', K.hud('clear'), K.dress('clear')])
        unin = ['# Hook uninstall (no executor; every enabled module): the rig (real or stand-in), the kit, the module entities,',
                '# objectives and storage.',
                f'function {A.rig_fn("kill")}', f'function {A.rig_fn("uninstall")}',
                f'function {K.FN}uninstall',
                F('wall/clear')] + kills + [f'kill @e[tag=rlk_mb_ar_{A.AID}]', 'kill @e[type=minecraft:husk,tag=rlk_mb_ap_org]',
                                            '# every AP-ORG display (organism models, the Heart, domes, stalks, the seed, wall',
                                            '# blades; AP-I2 RREV-4): their husks die above, so the dismounted models go by tag',
                                            'kill @e[tag=rlk_ap_om]',
                                            'kill @e[tag=rlk_mb_ap_gate]', 'data remove storage rlk:mboss ap']
        unin += [f'scoreboard objectives remove {o}' for o in ENTITY_OBJ]
        self.w('uninstall', unin)
        rl = [
            '# Hook reload (@s = body after /reload: every rlk_mb_aux entity is gone: the rig parts, hazards, organisms, the',
            '# Heart, domes, walls\' markers, props, proxies). Scores survive; the state is re-derived from them (plan 7.2):',
            '#   E -> the end of E; P1 -> the rig again, the pattern cancelled; T1 -> phase 2 ready; P2 -> the stage keeps its',
            '#   progress / wave / clock / strikes, the Heart and the wave again, parked; CS -> phase 3 ready; P3 -> the rig',
            '#   again (UPRIGHT), the pattern cancelled, a running Q2 cancelled (300 t).',
            F('ai/consts'), sc('#apHide', -1),
            'execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
            f'function {A.rig_fn("init")}', f'function {A.rig_fn("spawn")}',
            f'execute if score #apPid mb matches 32 run {F("aft/cancel")}',
            f'execute if score #mbSt mb matches 0 run return run {F("intro/done")}',
            f'execute if score #apPh mb matches 15 run return run {F("ph/ready_2")}',
            f'execute if score #apPh mb matches 25 run return run {F("ph/ready_3")}',
            f'execute if score #apPh mb matches 2 run return run {F("rl/p2")}',
            f'execute if score #apPh mb matches 3 run return run {F("rl/p3")}',
            F('rl/p1')]
        self.w('reload', rl)
        self.w('rl/p1', ['# /reload in phase 1: the rig in the p1 look, CROUCH; the pattern cancelled; the drawn-up Heart prop; the props.',
                         F('p/cancel'), F('svc/look_p1'), f'function {A.rig_fn("stance/crouch")}', g.play('idle_p1'),
                         F('px/restate'), F('heart/p1_respawn'), F('arena/props_now'), sc('#apCool', 20), sc('#apHudQ', 1)])
        cx, cy, cz = (L.num(v, 3) for v in A.CENTRE)
        self.w('rl/p2', ['# /reload in phase 2: the stage (revival) re-makes the Heart, clears the walls, respawns the wave; parked again;',
                         '# the kit re-makes its dressing pool (the cards died with every rlk_mb_aux; ap_fx_api 0.12) at the arena centre.',
                         F('p/reload_d'), F('svc/park'), F('rev/reload'), F('arena/props_now'),
                         f'execute in minecraft:overworld positioned {cx} {cy} {cz} run function {K.FN}dress/redraw', sc('#apHudQ', 1)])
        self.w('rl/p3', ['# /reload in phase 3: the rig in the p3 look, UPRIGHT; the pattern cancelled; the lush props.',
                         F('p/cancel'), F('svc/look_p3'), f'function {A.rig_fn("stance/upright")}', g.play('idle_p3'),
                         F('px/restate'), F('arena/props_now'), sc('#apCool', 20), sc('#apHudQ', 1)])
        self.w('bars', ['# Hook bars (@s = body, every tick in intro / fight): the under-bar (hud/bar); phase 2 the Heart bar.', F('hud/bar')])
        vis = ['# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end): routed by mbHzV / 10 = the pattern id.',
               'scoreboard players operation #apV mb = @s mbHzV', 'scoreboard players operation #apV mb /= #c10 mb']
        vis += [f'execute if score #apV mb matches {p.id} run return run {F(f"p/{p.key}/vis")}' for p in self.with_hook('vis')]
        if g.has('org/vis'):
            vis.append(f'execute if score #apV mb matches 70..79 run return run {F("org/vis")}')
        self.w('hz_vis', vis)
        pj = ['# Hook pj_end (@s = prop, #pjEv, #pjKeep): routed by the prop\'s pattern tag rlk_mb_ap_p<id> (organisms: rlk_mb_ap_opj).']
        pj += [f'execute if entity @s[tag=rlk_mb_ap_p{p.id}] run return run {F(f"p/{p.key}/pj_end")}' for p in self.with_hook('pj_end')]
        if g.has('org/pj_end'):
            pj.append(f'execute if entity @s[tag=rlk_mb_ap_opj] run return run {F("org/pj_end")}')
        self.w('pj_end', pj)
        self.w('test', ['# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}; ap_contract 0.8). See test/help.',
                        '$scoreboard players set #apTst mb $(id)',
                        f'execute as {BODY} at @s run {F("test/run")}'])

    # -----------------------------------------------------------------------------------------
    def prep(self):
        F = self.F
        l1 = txt(A.BOSS['name'], A.GOLD_HEX, True)
        l2 = txt(T['gate_l2'], '#D0D0D0')
        l3 = txt(T['gate_l3'], '#A8A8A8')
        m2 = 'rlk:mboss/ap_kit/gate_crystal'
        gate = (f'{{item:"{A.BOSS["icon"]["item"]}",model:"{A.BOSS["icon"]["model"]}",item2:"minecraft:emerald",'
                f'model2:"{m2}",l1:{l1},l2:{l2},l3:{l3},n:{A.N}}}')
        lines = ['# Hook prep (cm.md 5.3; @s = the kind-9 zone marker, at it; once per entrance build; cb/pp/apep cleared',
                 '# cprep.apep first): the gate texts (ap_contract 0.6.7), the title / sub of the gate press, the two gate crystals',
                 '# (theme entrance_layout glyphs; rlk_room props: room/clear removes them).',
                 f'data modify storage rlk:mboss cprep.apep.gate set value {gate}',
                 f'data modify storage rlk:mboss cprep.apep.title set value {txt(A.BOSS["name"], A.GOLD_HEX, True)}',
                 f'data modify storage rlk:mboss cprep.apep.sub set value {txt(A.BOSS["sub"], "#E8E2D0")}',
                 'kill @e[type=minecraft:item_display,tag=rlk_mb_ap_gate]']
        if not A.ENTRANCE_GLYPHS:
            lines.append('# (theme fallback: no gate-crystal spots)')
        for name, (x, y, z, yaw) in sorted(A.ENTRANCE_GLYPHS.items()):
            lines.append(f'summon minecraft:item_display ~{L.num(x)} {L.num(y)} ~{L.num(z)} {{Tags:["rlk_room","rlk_mb_ap_gate"],'
                         f'Rotation:[{L.num(float(yaw))}f,0f],billboard:"fixed",brightness:{{block:15,sky:15}},'
                         'transformation:{translation:[0f,0.6f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
                         'scale:[1.2f,1.2f,1.2f]},item:{id:"minecraft:emerald",count:1}}')
        self.w('prep', lines)

    # -----------------------------------------------------------------------------------------
    def intro(self):
        F, g = self.F, self.g
        self.w('intro/setup', [
            '# @s = the new body (from the spawn hook), at it: module state, the rig (p1 look, CROUCH), the withered arena props,',
            '# the entrance (seq/entrance/setup) and its clip; #apTot = the full pool (#mbTot is set right after this hook).',
            F('ai/consts'), F('ai/vars'), sc('#apHide', -1), sc('#apPh', PH['E']),
            f'function {A.rig_fn("init")}', f'function {A.rig_fn("spawn")}', F('svc/look_p1'),
            f'function {A.rig_fn("stance/crouch")}', F('u/hide_off'),
            F('arena/props_kill'), F('arena/props_withered'),
            F('seq/entrance/setup'), g.play('entrance_p1'), sc('#apHudQ', 1)])
        self.w('intro_tick', [
            f'# Hook intro_tick (@s = body, #mbT 1..; untargetable): E (entrance_p1, {A.E_LEN} t; clock #apPT = #mbT - 1).',
            'scoreboard players operation #apPT mb = #mbT mb', 'scoreboard players remove #apPT mb 1',
            F('obj/tick'),
            F('seq/entrance/tick'),
            F('hud/tick'),
            *A.rig_tick_lines(),
            F('pxs/tick'),
            f'execute if score #mbT mb matches {A.E_LEN}.. run {F("intro/done")}'])
        self.w('intro/done', [
            '# E is over (or skipped: /reload, tests): targetable, phase 1 (pool 53 %, floor 1 %), the AI after a short cooldown.',
            'execute store result score #apTot mb run scoreboard players get #mbTot mb',
            'function rlk:mboss/intro_end', F('seq/entrance/done'), F('svc/phase_1'),
            f'function {A.rig_fn("stance/crouch")}', F('svc/look_p1'), g.play('idle_p1'), F('px/p1'), sc('#apPT', 0),
            sc('#apCool', 20), sc('#apHudQ', 1),
            f'execute unless score #mbMusPh mb matches 1.. run {F("svc/music_1")}'])

    # -----------------------------------------------------------------------------------------
    def moves(self):
        """Service 10 (ap_contract 0.8, the core's): #apMvK 1 crab crawl toward the player (crawl_p1 <= 40 t at 0.25 b/t,
        then crawl_stop_p1), 2 side walk (walk_p1 <= 40 t at 0.12 b/t, #apMvD = the side), 3 a crab-turn step (turn_p1_step,
        90 deg in 10 t, toward the player), 4 a 180 deg crab-turn (two steps). p1.py may add sounds in p/move/fx (step
        ticks: #apMvT, kind #apMvK)."""
        F, g = self.F, self.g
        fx = [F('p/move/fx')] if g.has('p/move/fx') else []
        cr, wk = A.CRAWL, A.WALK
        stop = A.clip_len('crawl_stop_p1')
        g.pw('move', 'start', ['# Core service 10: the move kind #apMvK (1 crawl 2 walk 3 step 4 turn180).', sc('#apMvT', 0),
                               f'execute if score #apMvK mb matches 1 run {g.play("crawl_p1")}',
                               f'execute if score #apMvK mb matches 2 run {g.play("walk_p1")}',
                               f'execute if score #apMvK mb matches 3..4 run {F("mv/step")}'])
        g.pw('move', 'tick', [
            'scoreboard players add #apMvT mb 1', *fx,
            f'execute if score #apMvK mb matches 1 run return run {F("mv/crawl")}',
            f'execute if score #apMvK mb matches 2 run return run {F("mv/walk")}',
            f'execute if score #apMvK mb matches 3 if score #apMvT mb matches {A.clip_len("turn_p1_step")}.. run return run {g.end()}',
            f'execute if score #apMvK mb matches 4 if score #apMvT mb matches {A.clip_len("turn_p1_step")} run {F("mv/step")}',
            f'execute if score #apMvK mb matches 4 if score #apMvT mb matches {2 * A.clip_len("turn_p1_step")}.. run return run {g.end()}'])
        g.pw('move', 'cancel', ['# Nothing lingers (the yaw driver stops with the slot).', sc('#apYawC', 0)])
        self.w('mv/step', ['# A crab-turn step toward the player: turn_p1_step (-90 deg) mirrored when the player is on the right.',
                           AI.local_line(), sc('#apYawS', 1),
                           'execute if score #mbLs mb matches ..-1 run scoreboard players set #apYawS mb -1',
                           g.play('turn_p1_step')])
        self.w('mv/crawl', [
            f'# Crab crawl toward the player at {cr["spd"]} b/t (inside the glide disc) until the near band or {cr["max"]} t, then',
            f'# crawl_stop_p1 ({stop} t).',
            f'execute if score #apMvT mb matches ..{cr["max"]} run function rlk:mboss/mv/turn {{max:4}}',
            f'execute if score #apMvT mb matches ..{cr["max"]} run {g.move_to(PLAYER, cr["spd"])}',
            f'execute if score #apMvT mb matches ..{cr["max"] - 1} if entity {PLAYER.replace("limit=1", f"distance=..{L.num(A.BAND_P1[0])},limit=1")} '
            f'run scoreboard players set #apMvT mb {cr["max"] + 1}',
            f'execute if score #apMvT mb matches {cr["max"] + 1} run {g.play("crawl_stop_p1")}',
            f'execute if score #apMvT mb matches {cr["max"] + 1 + stop}.. run {g.end()}'])
        self.w('mv/walk', [
            f'# Side walk at {wk["spd"]} b/t across the facing (#apMvD 1 left / -1 right) for {wk["max"]} t, facing the player.',
            'function rlk:mboss/mv/turn {max:3}',
            f'execute if score #apMvD mb matches 1 rotated as @s rotated ~ 0 positioned ^{L.num(wk["spd"])} ^ ^ run {F("u/step_here")}',
            f'execute if score #apMvD mb matches -1 rotated as @s rotated ~ 0 positioned ^-{L.num(wk["spd"])} ^ ^ run {F("u/step_here")}',
            f'execute if score #apMvT mb matches {wk["max"]}.. run {g.play("idle_p1")}',
            f'execute if score #apMvT mb matches {wk["max"]}.. run {g.end()}'])

    def stance_svc(self):
        F, g = self.F, self.g
        cl, sl = A.clip_len('crouch_p3'), A.clip_len('stand_p3')
        g.pw('stance', 'start', ['# Core service 61 (phase 3): toggle the stance (UPRIGHT -> crouch_p3, CROUCH -> stand_p3).',
                                 sc('#apX', 0), 'execute if score #apStance mb matches 1 run scoreboard players set #apX mb 1',
                                 f'execute if score #apX mb matches 1 run {g.play("crouch_p3")}',
                                 f'execute if score #apX mb matches 0 run {g.play("stand_p3")}',
                                 'scoreboard players operation #apMvK mb = #apX mb'])
        g.pw('stance', 'tick', [f'execute if score #apMvK mb matches 1 if score #apPT mb matches {cl}.. run {g.end()}',
                                f'execute if score #apMvK mb matches 0 if score #apPT mb matches {sl}.. run {g.end()}'])
        g.pw('stance', 'cancel', ['# Nothing lingers.'])

    # -----------------------------------------------------------------------------------------
    def slot(self):
        F, g = self.F, self.g
        pats = self.slot_pats()
        begin = ['# @s = body. First tick of the main-slot pattern #apPid: clock -lead (0 for most), its first clip at clock 0,',
                 '# start; a service started at #apReqT >= 1 (tests) resumes through its reload at that clock.',
                 sc('#apPNew', 0), sc('#apPT', 0), sc('#apPEnd', 0), sc('#apPRel', 0), sc('#apPMax', 400), sc('#apPLen', 400)]
        begin += [sci('#apPid', p.id, '#apPMax', p.max_len) for p in pats]
        begin += [sci('#apPid', p.id, '#apPLen', p.length) for p in pats]
        begin += [sci('#apPid', p.id, '#apPT', -p.lead) for p in pats if p.lead]
        begin += [f'execute if score #apReqT mb matches 1.. run return run {F("p/resume_at")}', sc('#apHudQ', 1),
                  f'execute if score #apPT mb matches 0 run {F("p/clip_d")}', F('p/start_d')]
        self.w('p/begin', begin)
        ra = ['# A service started at a later clock (#apReqT): PT = it, its reload re-derives the state.',
              'scoreboard players operation #apPT mb = #apReqT mb', sc('#apReqT', 0)]
        ra += [f'execute if score #apPid mb matches {p.id} run return run {F(f"p/{p.key}/reload")}'
               for p in pats if p.kind == 'service' and g.has(f'p/{p.key}/reload')]
        ra.append(F('p/start_d'))
        self.w('p/resume_at', ra)
        self.w('p/run', [
            '# @s = body. The main slot: start on the tick it was picked, then tick with #apPT = -lead+1 .. 0 (clip) .. ;',
            f'# during a lead the body pre-turns <= {A.TURN_MAX[3]} deg/t (phase 1: {A.TURN_MAX[1]}).',
            f'execute if score #apPNew mb matches 1 run return run {F("p/begin")}',
            'scoreboard players add #apPT mb 1',
            f'execute if score #apPT mb matches ..-1 if score #apPh mb matches 1 run function rlk:mboss/mv/turn {{max:{A.TURN_MAX[1]}}}',
            f'execute if score #apPT mb matches ..-1 if score #apPh mb matches 3 run function rlk:mboss/mv/turn {{max:{A.TURN_MAX[3]}}}',
            f'execute if score #apPT mb matches 0 run {F("p/clip_d")}',
            F('p/tick_d'),
            f'execute if score #apPEnd mb matches 1 run return run {F("p/finish")}',
            f'execute if score #apPT mb >= #apPMax mb run {F("p/finish")}'])
        kills = ['kill @e[type=minecraft:marker,tag=rlk_mb_ap_lock]', 'kill @e[type=minecraft:marker,tag=rlk_mb_ap_kept]']
        self.w('p/finish', [
            '# @s = body. The pattern ended (p/end or its max_len): the slot freed, the kept markers gone, the bookkeeping',
            '# (ai/pat_done: cooldowns, recover, chains, the Q2 count, the opener hand-over), the rest px set of the form.',
            'scoreboard players operation #apPDone mb = #apPid mb',
            sc('#apPid', 0), sc('#apPEnd', 0), sc('#apPT', 0), sc('#apYawC', 0), sc('#mbNoLeash', 0)] + kills + [
            F('ai/pat_done'), sc('#apPRel', 0), sc('#apHudQ', 1)])
        self.w('p/end', ['# Called by a pattern (any executor): it is done; the core finishes it after this tick\'s pattern tick.',
                         sc('#apPEnd', 1)])
        self.w('p/release', ['# Called by a pattern: its dangerous part is over; with a queued transition (#apTr 1) the core ends the',
                             '# pattern here (its cancel cleans the harmless tail) and T1 starts at the next decision.',
                             sc('#apPRel', 1), sc('#apHudQ', 1),
                             f'execute if score #apTr mb matches 1 as {BODY} run {F("p/cut")}'])
        self.w('p/cut', ['# @s = body: end the running pattern now (cancel + finish).', F('p/cancel_d'), F('p/finish')])
        self.w('p/cancel', [
            '# Stop the main slot now (tests, death, reload, the phase jumps). The pattern\'s cancel runs as the caller.',
            f'execute if score #apPid mb matches 1.. unless score #apPNew mb matches 1 run {F("p/cancel_d")}',
            sc('#apPid', 0), sc('#apPNew', 0), sc('#apPEnd', 0), sc('#apPT', 0), sc('#apPRel', 0), sc('#mbNoLeash', 0),
            sc('#apYawC', 0), sc('#apChP', 0), sc('#apNext', 0)] + kills + ['kill @e[tag=rlk_mb_ap_pat]'])
        for name, target in (('start_d', 'start'), ('tick_d', 'tick'), ('cancel_d', 'cancel')):
            self.w(f'p/{name}', [f'# GENERATED: the running pattern\'s {target}, by #apPid.']
                   + [f'execute if score #apPid mb matches {p.id} run return run {F(f"p/{p.key}/{target}")}'
                      for p in pats if g.has(f'p/{p.key}/{target}')])
        rl = ['# GENERATED (reload): services resume through their reload; any other main-slot pattern is cancelled.']
        rl += [f'execute if score #apPid mb matches {p.id} run return run {F(f"p/{p.key}/reload")}'
               for p in pats if p.kind == 'service' and g.has(f'p/{p.key}/reload')]
        rl.append(F('p/cancel'))
        self.w('p/reload_d', rl)
        cd = ['# GENERATED: the running pattern\'s first clip at clock 0 (the core plays it; #apPT = its clip tick).']
        for p in pats:
            if p.clip is not None:
                cd.append(f'execute if score #apPid mb matches {p.id} run return run {g.play(p.clip)}')
        self.w('p/clip_d', cd)
        for hook in ('pause', 'resume'):
            lines = [f'# GENERATED: the {hook} hook of the running pattern.']
            for p in self.with_hook(hook):
                lines.append(f'execute if score #apPid mb matches {p.id} unless score #apPNew mb matches 1 run {F(f"p/{p.key}/{hook}")}')
            self.w(f'p/{hook}_d', lines)
        # bookkeeping after a pattern
        pd = ['# @s = body. A main-slot pattern finished (#apPDone): the opener hand-over, the recover, the cooldown, the counts',
              '# (patterns of the fight, phase-3 patterns, Q2 bookkeeping), the chain roll (never after a chain), the rest set.',
              f'execute if score #apNext mb matches 1.. run return run {F("ai/next_go")}',
              sc('#apCool', 20)]
        pd += [sci('#apPDone', p.id, '#apCool', p.recover) for p in pats if p.recover != 20]
        for p in pats:
            if p.cooldown:
                pd += [f'execute if score #apPDone mb matches {p.id} run scoreboard players operation #apCdE{p.id} mb = #apFc mb',
                       f'execute if score #apPDone mb matches {p.id} run scoreboard players add #apCdE{p.id} mb {p.cooldown}']
        normal = [p.id for p in pats if p.kind in ('normal', 'scheduled', 'chain')]
        pd += [f'execute if score #apPDone mb matches {i} run scoreboard players add #apPatN mb 1' for i in normal]
        pd += [f'execute if score #apPDone mb matches {p.id} run scoreboard players add #apP3N mb 1' for p in pats if p.phase == 3]
        pd += ['# Q2 (plan 7.4): the first-cast flag, the clock, the count of other patterns since']
        pd += [f'execute if score #apPDone mb matches {p.id} run scoreboard players add #apAftN mb 1'
               for p in pats if p.phase == 3 and p.id != 32]
        pd += ['execute if score #apPDone mb matches 32 run scoreboard players set #apAft1 mb 1',
               'execute if score #apPDone mb matches 32 run scoreboard players set #apAftN mb 0',
               'execute if score #apPDone mb matches 32 run scoreboard players operation #apAftCd mb = #apFc mb',
               f'execute if score #apPDone mb matches 32 run scoreboard players add #apAftCd mb {A.Q2_EVERY}']
        pd += ['# chains: rolled after a pattern that names some, unless it ran as a chain itself (never two in a row)']
        for p in pats:
            if p.chain:
                pd.append(f'execute if score #apPDone mb matches {p.id} unless score #apChainRun mb matches 1 run {F(f"ai/chain_{p.id}")}')
        pd += [sc('#apChainRun', 0),
               f'execute if score #apPh mb matches 1 run {F("svc/px_rest")}',
               f'execute if score #apPh mb matches 3 run {F("svc/px_rest")}']
        self.w('ai/pat_done', pd)
        for p in pats:
            if not p.chain:
                continue
            delay = max(0, p.last_hit + A.CHAIN_GAP - p.length)
            lines = [f'# After {p.label}: the chain roll ({p.chain}); the chain starts {delay} t after the end (>= {A.CHAIN_GAP} t after',
                     f'# the last hit at clock {p.last_hit}, plan 7.4).', 'execute store result score #apR mb run random value 0..99']
            acc = 0
            for cid, pct in p.chain.items():
                lines.append(f'execute if score #apR mb matches {acc}..{acc + pct - 1} run scoreboard players set #apChP mb {cid}')
                acc += pct
            lines += ['execute if score #apChP mb matches 1.. run scoreboard players operation #apChT mb = #apFc mb',
                      f'execute if score #apChP mb matches 1.. run scoreboard players add #apChT mb {delay}',
                      f'execute if score #apChP mb matches 1.. run scoreboard players set #apCool mb {max(1, delay)}']
            self.w(f'ai/chain_{p.id}', lines)

    # -----------------------------------------------------------------------------------------
    def floor_tr(self):
        F = self.F
        self.w('ev/tick', [
            '# @s = body (phase 1): the floor (plan 7.2): a hit with mhpC - raw <= #mbFloor (#mbFloorHit, framework) or mhpC <=',
            '# #mbFloor (DoTs, reactions) queues the transition (#apTr 1); a released pattern ends now; the popup "…" at most',
            '# once per 10 t while clamped.',
            f'execute if score #mbFloorHit mb matches 1 run {F("ev/pop")}',
            f'execute if score #apTr mb matches 0 if score #mbFloor mb matches 1.. if score #mbFloorHit mb matches 1 run {F("tr/queue")}',
            f'execute if score #apTr mb matches 0 if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb run {F("tr/queue")}',
            sc('#mbFloorHit', 0)])
        self.w('ev/pop', [
            '# The floor popup "…" above the head, at most once per 10 t.',
            'scoreboard players operation #apX mb = #apFc mb', 'scoreboard players operation #apX mb -= #apPopC mb',
            'execute if score #apX mb matches ..9 run return 0', 'scoreboard players operation #apPopC mb = #apFc mb',
            f'execute at @s run summon minecraft:text_display ~ ~4.6 ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pop"],billboard:"center",'
            f'text:{{text:"{T["floor_pop"]}",color:"#E9E2B8"}},background:0,see_through:1b,transformation:{{translation:[0f,0f,0f],'
            'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.6f,1.6f,1.6f]}}',
            'scoreboard players set @e[type=minecraft:text_display,tag=rlk_mb_ap_pop] apT 16'])
        self.w('tr/queue', ['# The P1 floor was reached: T1 is queued (#apTr 1); a released pattern ends now.',
                            sc('#apTr', 1), sc('#apHudQ', 1),
                            f'execute if score #apPid mb matches 1.. if score #apPRel mb matches 1 run {F("p/cut")}'])
        self.w('tr/begin', ['# A decision point with T1 queued: the T1 service (20, revival) starts; phase 15.',
                            sc('#apTr', 2), sc('#apPid', 20), sc('#apPNew', 1), sc('#apReqT', 0), F('svc/phase_t1')])

    # -----------------------------------------------------------------------------------------
    def services(self):
        """The core services of ap_contract 1.5 (g.svc(name)); each is idempotent and works from any executor."""
        F, g = self.F, self.g
        w = lambda n, lines: self.w(f'svc/{n}', lines)    # noqa: E731
        cx, cz = A.CENTRE[0], A.CENTRE[2]
        w('park', ['# R10 (plan 7.2): the body parked 30 b above the centre (NoGravity husk, rlk_mb_inv through the px set',
                   '# parked, husk 0.1, no shield), the rig parked, #mbNoLeash 1 (re-set by every reload: rl/p2). Keeps rlk_zmob',
                   '# (the zone cannot clear) and stays the bars carrier.',
                   sc('#apPark', 1), sc('#mbNoLeash', 1),
                   f'execute as {BODY} run tp @s {L.num(cx)} {L.num(CY + A.PARK_Y)} {L.num(cz)} 0 0',
                   f'execute as {BODY} at @s run function {A.rig_fn("park")}', F('px/parked')])
        w('unpark', ['# Back at the centre on the floor facing south (the CS white-out), the rig unparked; proxies inv (the revival',
                     '# clip hides the body until its burst; its px sets make it targetable).',
                     sc('#apPark', 0), sc('#mbNoLeash', 0),
                     f'execute as {BODY} run tp @s {L.num(cx)} {CY} {L.num(cz)} 0 0',
                     f'execute as {BODY} at @s run function {A.rig_fn("unpark")}', F('px/inv')])
        w('centre_hidden', ['# The body on the floor at the centre facing south, hidden (proxies inv).',
                            f'execute as {BODY} run tp @s {L.num(cx)} {CY} {L.num(cz)} 0 0', F('px/inv')])
        w('cine_on', ['# Cine (cm.md 13.7): boss hits on the player refused; the AI clock frozen (the module tick skips the decision).',
                      L.cine(True)])
        w('cine_off', [L.cine(False)])
        for ph in (1, 2, 3):
            w(f'music_{ph}', [f'# Music phase "{ph}" (registry music, a random-track pool with its re-pick period; cm.md 10).', L.music(ph)])
        w('music_stop', [L.music(0)])
        w('title_p1', [L.title(T['title_p1'], T['sub_p1'], A.GOLD_HEX)])
        w('title_heart', [L.title(T['title_heart'], T['p2_goal'], A.HEART_HEX)])
        w('title_p3', [L.title(T['title_p3'], T['sub_p3'], A.P3_HEX)])
        w('px_rest', ['# The rest px set of the form and stance (phase 1 p1; phase 3 p3u UPRIGHT / p3c CROUCH).',
                      f'execute if score #apPh mb matches ..1 run return run {F("px/p1")}',
                      f'execute if score #apPh mb matches 3 if score #apStance mb matches 1 run return run {F("px/p3u")}',
                      f'execute if score #apPh mb matches 3 run return run {F("px/p3c")}'])
        w('phase_1', ['# Phase 1 (종막 오아시스 파수꾼): pool 53 % (applied at spawn by the framework), floor 1 %, the title.',
                      sc('#apPh', PH['P1']), F('svc/floor_p1'), F('svc/title_p1'), sc('#apHudQ', 1)])
        w('phase_t1', ['# T1 (소생 단계 진입) starts (#apPh 15).', sc('#apPh', PH['T1']), sc('#apHudQ', 1)])
        w('phase_2', ['# Phase 2 (the revival stage) runs (#apPh 2); no boss damage (the body is parked, inv).',
                      sc('#apPh', PH['P2']), sc('#apTr', 0), sc('#mbFloor', 0), sc('#apHudQ', 1)])
        w('phase_cs', ['# The CS (2 -> 3) runs (#apPh 25).', sc('#apPh', PH['CS']), sc('#apHudQ', 1)])
        w('phase_3', ['# Phase 3 (기원 오아시스 파수꾼): the fresh pool (repooled in the CS), floor 0 (the normal death), the rest set.',
                      sc('#apPh', PH['P3']), sc('#mbFloor', 0), sc('#apTr', 0), sc('#apCool', 20), sc('#apAftCd', 0),
                      F('svc/px_rest'), sc('#apHudQ', 1)])
        w('repool_p3', [f'# The phase-3 pool: {A.POOL[3]} % of #mbTot, full; the bar refills over 30 t (cm.md 7.1).', L.repool(A.POOL[3])])
        w('repool_p1', [f'# The phase-1 pool again ({A.POOL[1]} %; tests only).', L.repool(A.POOL[1])])
        w('floor_p1', [f'# #mbFloor = ceil(mhpM x {A.FLOOR_PCT_P1} / 100) (the P1 pool\'s 1 %, plan 7.2; framework clamp, cm.md 7.2).',
                       f'execute as {BODY} run scoreboard players operation #mbFloor mb = @s mhpM',
                       'scoreboard players add #mbFloor mb 99', 'scoreboard players operation #mbFloor mb /= #c100 mb'])
        w('floor_0', [sc('#mbFloor', 0)])
        w('look_p1', ['# The rig in the phase-1 form (R12; the form swap sets face / core / hands / tint itself).',
                      f'execute as {BODY} run function {A.rig_fn("look/form/p1")}'])
        w('look_p3', ['# The rig in the phase-3 form (the CS white-out).', f'execute as {BODY} run function {A.rig_fn("look/form/p3")}'])
        lush = []
        if A.THEME_STUBBED:
            lush.append('# (theme fallback: the stub arena has no look job; only the props swap)')
        else:
            lush.append(f'function rlk:mboss/arena/{A.AID}/look/lush')
        w('arena_lush', ['# The arena to the lush look (FN-3, cm.md 6.5: a sliced look job, done flag) and the lush props (kept across',
                         '# the swap by UUID).'] + lush + [F('arena/props_lush')])
        w('arena_withered', ['# The withered props (the fight start; the entrance prep restores the withered look itself).',
                             F('arena/props_kill'), F('arena/props_withered')])
        w('heal_cs', ['# CS t80 (Q25): the player heals 25 % max HP through player/heal (item heal hooks see it).',
                      f'execute as @a[tag=player,scores={{dead=0}}] run {F("svc/heal_cs1")}'])
        w('heal_cs1', ['scoreboard players operation #heal tmp = @s maxHealth', 'scoreboard players operation #heal tmp /= #4 tmp',
                       'execute if score #heal tmp matches ..0 run scoreboard players set #heal tmp 1', 'function rlk:player/heal',
                       L.say(T['cs_heal'], '#B6E35A', 2, 50, 1)])
        w('push_ring_cs', ['# CS white-out: players within 8 b of the centre pushed out to 12 b (cm.md 13.5, A9).',
                           f'execute positioned {L.num(cx)} {CY} {L.num(cz)} run {L.push_ring(8, 6, 12)}'])
        w('req_cs', ['# The Heart reached 10000: the CS service (60) now (the stage stops at its t0).',
                     f'execute if score #apPid mb matches 60 run return 0',
                     f'execute as {BODY} run {F("p/cancel")}', sc('#apPid', 60), sc('#apPNew', 1), sc('#apReqT', 0)])
        w('req_fail', ['# The Heart reached 0: the failure strike service (40) now.',
                       f'execute if score #apPid mb matches 40 run return 0',
                       f'execute as {BODY} run {F("p/cancel")}', sc('#apPid', 40), sc('#apPNew', 1), sc('#apReqT', 0)])
        w('lose', ['# The second failure (plan 3.4, FN-9): the normal death path (run over / test/defeat).', 'function rlk:mboss/cb/lose'])
        w('lib_clear', ['# Every running framework library effect and the kit telegraphs (T1 t6, CS t0, tests).',
                        'function rlk:mboss/lib_clear', f'function {K.FN}tele/clear'])
        w('targetable', ['# The body targetable (outside px inv sets).', 'tag @e[type=minecraft:husk,tag=rlk_mb_body] remove rlk_mb_inv'])
        w('untargetable', ['tag @e[type=minecraft:husk,tag=rlk_mb_body] add rlk_mb_inv'])
        w('hud_now', [sc('#apHudQ', 1)])

    # -----------------------------------------------------------------------------------------
    def ready(self):
        """The phase-ready states (plan 7.2: reload in T1 / CS; the phase jumps of the test ids, ap_contract 1.8)."""
        F, g = self.F, self.g
        self.w('ph/cut', [
            '# @s = body: stop whatever runs (hazards, the slot, chains, the yaw driver, the cine, a queued transition).',
            F('svc/lib_clear'), F('p/cancel'), F('dome/clear'), sc('#apTr', 0), sc('#apChP', 0), sc('#apNext', 0),
            sc('#apYawC', 0), F('svc/cine_off'), sc('#mbFloorHit', 0)])
        self.w('ph/ready_1', [
            '# @s = body: phase 1 ready (tests): the stage gone, unparked at its place, p1 look, CROUCH, pool 53 %, floor 1 %.',
            F('ph/cut'), F('rev/clear'), F('org/clear'), F('wall/clear'),
            f'execute if score #apPark mb matches 1 run {F("svc/unpark")}',
            f'execute unless score #mbPoolPct mb matches {A.POOL[1]} run {F("svc/repool_p1")}',
            F('svc/look_p1'), f'function {A.rig_fn("stance/crouch")}', g.play('idle_p1'),
            F('svc/phase_1'), F('px/p1'), F('heart/p1_respawn'), sc('#apCool', 10),
            f'execute unless score #mbMusPh mb matches 1 run {F("svc/music_1")}'])
        self.w('ph/ready_2', [
            '# @s = body: phase 2 ready (reload in T1; tests): parked, the Heart and cradle in place, the stage from wave 1.',
            F('ph/cut'), F('heart/clear'), F('svc/park'), F('svc/phase_2'), F('svc/title_heart'),
            f'execute unless score #mbMusPh mb matches 2 run {F("svc/music_2")}',
            F('rev/ready'), F('rev/start')])
        self.w('ph/ready_3', [
            '# @s = body: phase 3 ready (reload mid-CS; tests): the stage gone, the lush look, pool 47 %, the p3 title, the rig in',
            '# p3 UPRIGHT at the centre, unparked, targetable.',
            F('ph/cut'), F('rev/clear'), F('org/clear'), F('wall/clear'), F('heart/clear'),
            f'execute if score #apPark mb matches 1 run {F("svc/unpark")}',
            f'execute as {BODY} run tp @s {L.num(A.CENTRE[0])} {CY} {L.num(A.CENTRE[2])} 0 0',
            F('svc/arena_lush'),
            f'execute unless score #mbPoolPct mb matches {A.POOL[3]} run {F("svc/repool_p3")}',
            F('svc/look_p3'), f'function {A.rig_fn("stance/upright")}', g.play('idle_p3'),
            F('svc/title_p3'), f'execute unless score #mbMusPh mb matches 3 run {F("svc/music_3")}',
            F('svc/phase_3'), F('px/p3u')])

    # -----------------------------------------------------------------------------------------
    def push(self):
        F = self.F
        self.w('push/req', [
            '# @s = body: the body push request (FN-21, cm.md 13.5; #mbPushOn is a per-tick request): only in the rest sets p1 /',
            '# p3u / p3c, the anchor moved <= 0.15 b/t and turned <= 6 deg/t since the last tick, no pattern request #apNoPush,',
            '# no Q2 dome round (rlk_mb_hzsafe markers).',
            sc('#apMov', 0),
            'execute store result score #apX mb run data get entity @s Pos[0] 1000',
            'execute store result score #apZ mb run data get entity @s Pos[2] 1000',
            'execute store result score #apY mb run data get entity @s Rotation[0] 100',
            'scoreboard players operation #apDX mb = #apX mb', 'scoreboard players operation #apDX mb -= #apLX mb',
            'scoreboard players operation #apDZ mb = #apZ mb', 'scoreboard players operation #apDZ mb -= #apLZ mb',
            'scoreboard players operation #apDY mb = #apY mb', 'scoreboard players operation #apDY mb -= #apLY mb',
            'execute unless score #apDX mb matches -150..150 run scoreboard players set #apMov mb 1',
            'execute unless score #apDZ mb matches -150..150 run scoreboard players set #apMov mb 1',
            'execute unless score #apDY mb matches -600..600 run scoreboard players set #apMov mb 1',
            'scoreboard players operation #apLX mb = #apX mb', 'scoreboard players operation #apLZ mb = #apZ mb',
            'scoreboard players operation #apLY mb = #apY mb',
            f'execute unless score #apPx mb matches {min(A.PX_ID[s] for s in A.PUSH_SETS)}..{max(A.PX_ID[s] for s in A.PUSH_SETS)} run return 0',
            'execute if score #apMov mb matches 1 run return 0',
            'execute if score #apNoPush mb matches 1 run return 0',
            'execute if entity @e[type=minecraft:marker,tag=rlk_mb_hzsafe,limit=1] run return 0',
            'scoreboard players set #mbPushOn mb 1'])
        assert sorted(A.PX_ID[s] for s in A.PUSH_SETS) == list(range(min(A.PX_ID[s] for s in A.PUSH_SETS),
                                                                     max(A.PX_ID[s] for s in A.PUSH_SETS) + 1)), A.PX_ID

    # -----------------------------------------------------------------------------------------
    def arena(self):
        F = self.F
        stand = {'water_sheet': 'minecraft:light_blue_stained_glass_pane', 'lily_pad': 'minecraft:lily_pad',
                 'bell_flower': 'minecraft:spore_blossom', 'bulb_flower': 'minecraft:pitcher_plant',
                 'bank_crystal': 'minecraft:emerald'}

        def summon(pr):
            x, y, z = pr['pos'][:3]
            s = float(pr.get('scale', 1.0))
            u = int(pr['uuid']) if pr.get('uuid') is not None else 0
            rot = '[0f,0f,0f,1f]'                # the kit's water_sheet prop lays the sheet flat itself
            line = (f'execute in minecraft:overworld run summon minecraft:item_display {L.num(x, 3)} {L.num(y, 3)} {L.num(z, 3)} '
                    f'{{UUID:[I;{A.PROP_INTS[0]},{A.PROP_INTS[1]},{A.PROP_INTS[2]},{u}],'
                    f'Tags:["rlk_mb_arena_prop","rlk_mb_ar_{A.AID}","rlk_mb_ap_ar_{pr["group"]}"],'
                    f'Rotation:[{L.num(float(pr.get("yaw", 0.0)))}f,{L.num(float(pr.get("pitch", 0.0)))}f],billboard:"fixed",'
                    'brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:'
                    f'{rot},right_rotation:[0f,0f,0f,1f],scale:[{L.num(s)}f,{L.num(s)}f,{L.num(s)}f]}},'
                    f'item:{{id:"{stand.get(pr["kind"], "minecraft:paper")}",count:1}}}}')
            uu = f'{A.PROP_BLOCK}{u:02x}'
            out = [f'execute unless entity {uu} run {line}']
            out.append(f'execute as {uu} run {K.prop(pr["kind"])}')
            return out
        by = {lk: {pr['name']: pr for pr in A.PROPS.get(lk, [])} for lk in A.LOOKS}
        for lk in A.LOOKS:
            lines = [f'# The {lk} props of the theme (ap_contract 0.6.6; arena-prop UUID block, tags rlk_mb_arena_prop',
                     f'# rlk_mb_ar_{A.AID} rlk_mb_ap_ar_<group>, never rlk_room / rlk_mb_aux): the ones missing are made, the other',
                     '# look\'s ones it lacks are killed by UUID (kept across the swap: same name, same UUID).']
            for nm, pr in sorted(by[lk].items()):
                lines += summon(pr)
            other = [lo for lo in A.LOOKS if lo != lk]
            for lo in other:
                for nm, pr in sorted(by[lo].items()):
                    if nm not in by[lk] and pr.get('uuid') is not None:
                        lines.append(f'kill {A.PROP_BLOCK}{int(pr["uuid"]):02x}')
            if len(lines) == 3:
                lines.append('# (no props in this look)')
            self.w(f'arena/props_{lk}', lines)
        self.w('arena/props_kill', [f'kill @e[tag=rlk_mb_ar_{A.AID}]'])
        self.w('arena/props_now', ['# The props of the current look (reload): look_ap_oasis (cm.md 3.3), else the phase.',
                                   f'execute if data storage rlk:mboss {{look_{A.AID}:"lush"}} run return run {F("arena/props_lush")}',
                                   f'execute if score #apPh mb matches 3 run return run {F("arena/props_lush")}',
                                   F('arena/props_withered')])

    # -----------------------------------------------------------------------------------------
    def hud(self):
        F = self.F
        labels = [p for p in self.slot_pats() if p.kind in ('normal', 'scheduled', 'chain', 'opener')]
        sub = ['# @s = body: the sub-line and the name-line extras (every 4 t or on #apHudQ). Phase 2 is the stage\'s (rev/hud).',
               f'execute if score #apPh mb matches 2 run return run {F("rev/hud")}',
               'data modify storage rlk:mboss extra set value []',
               'data modify storage rlk:mboss sub set value []',
               f'execute if score #mbSt mb matches 0 run return run data modify storage rlk:mboss sub set value [{txt(T["sub_p1_line"], "#E8E2D0", True)}]',
               f'execute if score #apPh mb matches 15 run return run data modify storage rlk:mboss sub set value [{txt(T["t1_sink"], "#E8E2D0")}]',
               f'execute if score #apPh mb matches 25 run return run data modify storage rlk:mboss sub set value [{txt(T["cs_done"], A.HEART_HEX)}]',
               f'execute if score #apTr mb matches 1 run return run data modify storage rlk:mboss sub set value [{txt(T["t1_sink"], "#E8E2D0")}]']
        for p in labels:
            sub.append(f'execute if score #apPid mb matches {p.id} run return run data modify storage rlk:mboss sub set value '
                       f'[{{text:"패턴  ",color:"#A8A8A8"}},{txt(p.label, LABEL_HEX)}]')
        sub.append(f'execute if score #apPh mb matches 3 run return run data modify storage rlk:mboss sub set value [{txt(T["sub_p3"], "#CDEBC8")}]')
        self.w('hud/refresh', sub + [sc('#apHudQ', 0)])
        self.w('hud/tick', ['# @s = body: the floor popups age; the lines every 4 t or on request.',
                            'scoreboard players remove @e[type=minecraft:text_display,tag=rlk_mb_ap_pop] apT 1',
                            'kill @e[type=minecraft:text_display,tag=rlk_mb_ap_pop,scores={apT=..0}]',
                            f'execute if score #apHudQ mb matches 1 run return run {F("hud/refresh")}',
                            'scoreboard players operation #apM mb = #apFc mb', 'scoreboard players operation #apM mb %= #apK4 mb',
                            f'execute if score #apM mb matches 0 run {F("hud/refresh")}'])
        self.w('hud/bar', [
            '# @s = body (bars hook, every tick): the under-bar. Phase 1: HP down to the floor (the P1 pool, Dendro colour);',
            '# T1 / CS: the sequence progress (gold); phase 2: the Heart bar (rev/bars: #buHp = #apHt / 10, #buMax 1000,',
            '# #buHpCol 10 gold, #buNoNum 1; cm.md 11); phase 3: HP.',
            'execute if score #mbSt mb matches 0 run return 0',
            f'execute if score #apPh mb matches 2 run return run {F("rev/bars")}',
            f'execute if score #apPh mb matches 15 run return run {F("hud/bar_seq")}',
            f'execute if score #apPh mb matches 25 run return run {F("hud/bar_seq")}',
            f'execute if score #apPid mb matches 32 if score #apq32 mb matches ..{Q2_POP - 1} run return run {F("hud/bar_q2")}',
            'scoreboard players operation #buSub bu = @s mhpC', 'scoreboard players operation #buSub bu -= #mbFloor mb',
            'scoreboard players operation #buSubMax bu = @s mhpM', 'scoreboard players operation #buSubMax bu -= #mbFloor mb',
            'execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1',
            'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
            bu('#buSubCol', L.ELEM_TO_BU[7])])
        self.w('hud/bar_q2', [
            f'# Q2 (plan 8.3 B0; AP-I2 RP3-2): the two-segment countdown: red (code {Q2_RED}) from the banner to the blast (aftermath',
            f'# clip t{Q2_BLAST}), then gold (code {Q2_GOLD}) to the dome pop (t{Q2_POP}). #apq32 = the clip tick (negative on the',
            '# approach), #apq32S = the pattern tick the clip starts on.',
            f'execute if score #apq32 mb matches {Q2_BLAST}.. run return run {F("hud/bar_q2g")}',
            bu('#buSub', Q2_BLAST), 'scoreboard players operation #buSub bu -= #apq32 mb',
            bu('#buSubMax', Q2_BLAST), 'scoreboard players operation #buSubMax bu += #apq32S mb',
            'execute if score #buSub bu > #buSubMax bu run scoreboard players operation #buSub bu = #buSubMax bu',
            bu('#buSubCol', Q2_RED)])
        self.w('hud/bar_q2g', [
            bu('#buSub', Q2_POP), 'scoreboard players operation #buSub bu -= #apq32 mb',
            bu('#buSubMax', Q2_POP - Q2_BLAST),
            'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
            bu('#buSubCol', Q2_GOLD)])
        self.w('hud/bar_seq', ['scoreboard players operation #buSub bu = #apPT mb', 'scoreboard players operation #buSubMax bu = #apPLen mb',
                               'execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1',
                               'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
                               bu('#buSubCol', L.ELEM_TO_BU[5])])

    # -----------------------------------------------------------------------------------------
    def death(self):
        F, g = self.F, self.g
        self.w('death_start', [
            '# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, set the proxies dead, stopped the',
            '# music): the slot, domes, walls, organisms, the kit telegraphs and HUD; the cine; the death clip and seq/death.',
            F('p/cancel'), F('dome/clear'), F('wall/clear'), F('org/clear'),
            f'function {K.FN}tele/clear', K.hud('clear'),
            F('svc/cine_on'), sc('#mbFloor', 0), sc('#apTr', 0), sc('#apPh', PH['D']), sc('#apPT', 0),
            F('u/hide_off'), g.play('death'), F('seq/death/start')])
        self.w('death_tick', [
            '# Hook death_tick (@s = body, #mbT 1.. until cur.death): seq/death (clock #apPT = #mbT - 1), the rig.',
            'scoreboard players operation #apPT mb = #mbT mb', 'scoreboard players remove #apPT mb 1',
            F('obj/tick'),
            F('seq/death/tick'),
            *A.rig_tick_lines()])

    # -----------------------------------------------------------------------------------------
    def tests(self):
        F, g = self.F, self.g
        HELP = [('1-6', 'P1-P6'), ('8', 'R + P4'), ('9', 'P6 4타'), ('20', '소생 단계 진입'), ('21/22', '심장 +25% / -25%'),
                ('23', '기본 x4'), ('24-28', '수호 / 둥지 / 양육 / 포식성 / 파괴'), ('29', '시간 초과'), ('30', '3페이즈 (컷신)'),
                ('31-35', 'Q1-Q5'), ('36', 'Q3s'), ('37', 'Q2 (치명)'), ('40/41', '소생 실패 1 / 2'), ('60', '컷신만'),
                ('61', '자세 전환'), ('99', '대기'), ('시작', '/function rlk:mboss/test/chapter {id:\\"apep\\"}')]
        tx = f'[{{text:"[아펩 테스트] ",color:"{A.GOLD_HEX}",bold:true}}' + ''.join(
            f',{{text:"{k}",color:"yellow"}},{{text:" {v}  ",color:"gray"}}' for k, v in HELP) + ']'
        self.w('test/help', ['tellraw @a[tag=player] ' + tx])
        run = ['# @s = body, #apTst = the requested test id (ap_contract 0.8; the phase jumps of 1.8).',
               f'execute if score #mbSt mb matches 0 run {F("intro/done")}',
               sc('#apArg', 0)]
        p1 = [p.id for p in self.pats if p.phase == 1 and p.kind == 'normal']
        p3 = [p.id for p in self.pats if p.phase == 3 and p.kind in ('normal', 'scheduled', 'chain')]
        for pid in p1:
            run.append(f'execute if score #apTst mb matches {pid} run return run {F(f"test/p1_{pid}")}')
            self.w(f'test/p1_{pid}', [f'execute unless score #apPh mb matches 1 run {F("ph/ready_1")}', F('ph/cut'),
                                      sc('#apReq', pid), sc('#apCool', 1)])
        run += [f'execute if score #apTst mb matches 8 run return run {F("test/r_p4")}',
                f'execute if score #apTst mb matches 9 run return run {F("test/p6_4")}']
        self.w('test/r_p4', [f'execute unless score #apPh mb matches 1 run {F("ph/ready_1")}', F('ph/cut'), sc('#apReq', 7),
                             sc('#apNext', 4), sc('#apCool', 1)])
        self.w('test/p6_4', [f'execute unless score #apPh mb matches 1 run {F("ph/ready_1")}', F('ph/cut'), sc('#apReq', 6),
                             sc('#apArg', 4), sc('#apCool', 1)])
        run.append(f'execute if score #apTst mb matches 20 run return run {F("test/t1")}')
        self.w('test/t1', ['# 20: T1 now (from phase 1; phase 2 / 3 first jump to phase 1).',
                           f'execute unless score #apPh mb matches 1 run {F("ph/ready_1")}', F('ph/cut'), sc('#apReq', 20),
                           sc('#apCool', 1)])
        p2_need = f'execute unless score #apPh mb matches 2 run {F("ph/ready_2")}'
        run += [f'execute if score #apTst mb matches 21 run return run {F("test/h_up")}',
                f'execute if score #apTst mb matches 22 run return run {F("test/h_down")}']
        self.w('test/h_up', [p2_need, F('heart/add') + ' {v:2500}'])
        self.w('test/h_down', [p2_need, F('heart/sub') + ' {v:2500}'])
        kinds = {23: 'basic', 24: 'guard', 25: 'nest', 26: 'nurt', 27: 'pred', 28: 'destr'}
        for tid, k in kinds.items():
            run.append(f'execute if score #apTst mb matches {tid} run return run {F(f"test/org_{k}")}')
            n = 4 if k == 'basic' else 1
            pts = [3, 4, 5, 6] if k == 'basic' else [1]
            lines = [p2_need]
            for i in range(n):
                x, y, z = A.ORG_SPAWN[pts[i]]
                lines.append(f'execute positioned {L.num(x)} {L.num(y)} {L.num(z)} run {F("org/spawn_" + k)}')
            self.w(f'test/org_{k}', lines)
        run += [f'execute if score #apTst mb matches 29 run return run {F("test/timeout")}',
                f'execute if score #apTst mb matches 30 run return run {F("test/cs_full")}',
                f'execute if score #apTst mb matches 60 run return run {F("test/cs_only")}']
        self.w('test/timeout', [p2_need, F('rev/test_timeout')])
        self.w('test/cs_full', ['# 30: to phase 3 through the CS (phase 2 first; the Heart full -> the CS service).', p2_need,
                                'scoreboard players set #apHt mb 10000', F('svc/req_cs')])
        self.w('test/cs_only', ['# 60: the CS service at once (phase 2 state first).', p2_need, F('svc/req_cs')])
        for pid in p3:
            run.append(f'execute if score #apTst mb matches {pid} run return run {F(f"test/p3_{pid}")}')
            extra = []
            if pid == 32:
                extra = [sc('#apAft1', 0)]
            self.w(f'test/p3_{pid}', [f'execute unless score #apPh mb matches 3 run {F("ph/ready_3")}', F('ph/cut')] + extra
                   + [sc('#apReq', pid), sc('#apCool', 1)])
        run.append(f'execute if score #apTst mb matches 37 run return run {F("test/q2_lethal")}')
        self.w('test/q2_lethal', [f'execute unless score #apPh mb matches 3 run {F("ph/ready_3")}', F('ph/cut'),
                                  sc('#apAft1', 1), sc('#apReq', 32), sc('#apCool', 1)])
        run += [f'execute if score #apTst mb matches 40 run return run {F("test/fail1")}',
                f'execute if score #apTst mb matches 41 run return run {F("test/fail2")}']
        self.w('test/fail1', [p2_need, 'scoreboard players set #apFail mb 0', 'scoreboard players set #apHt mb 0', F('svc/req_fail')])
        self.w('test/fail2', [p2_need, 'scoreboard players set #apFail mb 1', 'scoreboard players set #apHt mb 0', F('svc/req_fail')])
        run.append(f'execute if score #apTst mb matches 61 run return run {F("test/stance")}')
        self.w('test/stance', [f'execute unless score #apPh mb matches 3 run {F("ph/ready_3")}', F('ph/cut'), sc('#apReq', 61),
                               sc('#apCool', 1)])
        run += [f'execute if score #apTst mb matches 99 run return run {F("test/idle")}', F('test/help')]
        self.w('test/idle', ['# 99: idle (whatever runs is cut; the phase stays).', F('ph/cut'), sc('#apCool', 40),
                             f'execute if score #apPh mb matches 1 run {F("svc/px_rest")}',
                             f'execute if score #apPh mb matches 3 run {F("svc/px_rest")}'])
        self.w('test/run', run)
