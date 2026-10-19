"""야타용왕 (Azhdaha) module core: the 17 framework hooks + prep (cm.md 5.3), the state machine (intro, phases 1-3, the
transition queue and its steps, the B3 frame call, death), RES at spawn, the #mbFloor upkeep, the service dispatch,
the main / cast / background slots, the yaw driver, the field table (N6), the orbit mover (N5), the addon dispatchers
and the timers (N13), the push request (N12), the HUD, the music / cine / proxy-state service wrappers, the arena
props and element looks (N17), pause / reload / cleanup / uninstall, the test commands, the local stubs of missing
framework functions (cmstub/) and of the kit (kstub/). See __init__.py for the package layout; s2.md is the contract.

Owns F:mboss/azhdaha/** except rig/** (the rig generator, wip/az-rig) and the kit's paths (fx.md 0.1:
fx/{card,cardx,look,clear,uninstall} and fx/{e,p,tele,snd,hud,prop,test}/**); every file it owns that it did not write
in this run is deleted, so a second run and any generator order give the same bytes.
"""
import importlib
import json

from . import PATTERN_MODULES
from . import api as A
from . import ai as AI
from . import brand as BR
from . import stub_rig as SR
from .api import L, K, Gen, TL

NS = A.NS
OWN_TOP = 'mboss/' + A.ID
BODY, PLAYER, ARENA_M = A.BODY, A.PLAYER, A.ARENA_M
CY = A.CY
INTRO_LEN = A.clip_len('intro')
INTRO_DONE = INTRO_LEN + 1                    # #mbT of the fight start (the clip plays at spawn: clip tick = #mbT - 1)
assert INTRO_DONE <= A.BOSS['intro'], (INTRO_DONE, A.BOSS['intro'])
assert A.clip_len('death') <= A.BOSS['death']
RES_BY_PHASE = False                          # plan 4.2 / Q2: the rolled pair's RES from the entry (default) or per phase
HUD_EVERY = 4
PX_ID = {name: i for i, name in enumerate(('normal', 'jump', 'inv', 'tail_only', 'dead'))}
TURN_CLIPS = {1: 'turn45_l', 2: 'turn45_r', 3: 'turn90_l', 4: 'turn90_r', 5: 'turn180', 6: 'turn180'}
FLASH_GROUP = {'head': 1, 'front': 2, 'rear': 3, 'tail': 4}
SVC_TURN = A.Pattern(27, 'turn', '선회', 'service', None, recover=4, max_len=64, length=60)
SVC_WALK = A.Pattern(28, 'walk', '접근', 'service', 'walk', recover=0, max_len=60, length=AI.WALK_MAX + A.clip_len('walk_stop'))
SVC_CAST = A.Pattern(30, 'cast_host', '원소 특수 공격', 'service', None, recover=30, max_len=A.clip_len('roar_rear') + 6,
                     length=A.clip_len('roar_rear'))
CORE_PATS = (SVC_TURN, SVC_WALK, SVC_CAST)
NEED = {1: 'normal', 2: 'normal', 3: 'normal', 4: 'normal', 5: 'normal', 6: 'normal', 7: 'normal', 8: 'normal', 9: 'normal',
        10: 'normal', 20: 'service', 21: 'service', 22: 'service', 23: 'service', 31: 'cast', 32: 'cast', 41: 'special',
        42: 'special', 43: 'bg', 44: 'normal', 45: 'normal', 46: 'normal'}
MSG = '야타용왕이 곧 {el} 원소의 힘을 흡수합니다…'
SUB_B3 = '꼬리만 공격할 수 있습니다'
SUB_LAST = '마지막 일격!'
SUB_JUMP = '점프!'
GOLD = A.GOLD_HEX


def build():
    out = L.Out()
    g = Gen(out)
    pats = []
    mods = {}
    for name in PATTERN_MODULES:
        mod = importlib.import_module(f'{__package__}.{name}')
        mods[name] = mod
        for p in mod.PATTERNS:
            p.module = name
        pats.extend(mod.PATTERNS)
        g.owner = name
        mod.emit(g)
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
        assert p is not None, f'pattern id {pid} missing (s2.md 2.1)'
        assert p.kind == kind, (pid, p.kind, kind)
    core = Core(g, pats)
    core.emit()
    for p in pats:
        need = A.REQ_HOOKS[p.kind] + (('reload',) if p.kind == 'service' and 20 <= p.id <= 23 else ())
        for f in need:
            assert g.has(f'p/{p.key}/{f}'), f'{p.module}: pattern {p.key} has no {f}'
        for h in p.hooks:
            assert g.has(f'p/{p.key}/{h}'), f'{p.module}: pattern {p.key} declares {h} but writes no file'
    for rel in A.AFTER:
        assert g.has(rel), f'after() target {rel} was not written'
    core.stubs()
    SR.emit(g, A.MAN)
    removed = clean(out)
    pxs = px_target_stubs()
    normal = [p for p in pats if p.kind == 'normal']
    print(f'mboss azhdaha: {len(g.files)} functions ({len(normal)} normal patterns, {len(pats) - len(normal)} other, '
          f'modules {", ".join(PATTERN_MODULES)} + core), {removed} stale removed; manifest '
          f'{A.REAL_KIND or "absent"} + stub ({len(A.FALLBACKS)} clip fallbacks).')
    notes = []
    if A.BOSS_STUBBED:
        notes.append('registry: no "azhdaha" entry (AZ-CM commit 1): api.REG_STUB used')
    if A.ARENA_STUBBED:
        notes.append('arena: no arena_of / arenas{} (AZ-CM): api.ARENA_STUB used')
    if A.THEME_STUBBED:
        notes.append('WARN theme az_cavern missing (S1-ARENA unmerged): api._THEME_FALLBACK used (no entrance glyphs, no crystals)')
    if A.CMSTUBS:
        notes.append('framework (AZ-CM) local stubs: ' + ', '.join(f'{k} (cm.md {v})' for k, v in sorted(A.CMSTUBS.items())))
    if not A.KIT:
        notes.append(f'kit (S1-FX) absent: {len(K.used)} kit calls go to kstub/')
    if A.FALLBACKS:
        notes.append(f'rig: {len(A.FALLBACKS)} clips from the stub manifest' + ('' if A.REAL_RIG else ', the stand-in rig rig_stub/'))
    if pxs:
        notes.append('framework px runtime (AZ-CM, cm.md 9.3) missing: local no-op stubs F:mboss/px/azhdaha/{'
                     + ','.join(pxs) + '} (no proxies; requests/mod.md)')
    for n in notes:
        print('  note: ' + n)
    for clip, event, default in sorted(set(A.EV_FALLBACKS)):
        print(f'  note: manifest clip {clip} has no event {event!r}; using tick {default}')


PX_MARK = '# LOCAL STUB (S1-MOD, tools/mboss_azhdaha/core.py)'
PX_TARGETS = ('spawn', 'tick', 'park', 'poll', 'clear_input')


def px_target_stubs():
    """AZ-CM commit 1 generates the px dispatchers F:mboss/px/{spawn,tick,park,poll,clear_input} with a line for every
    enabled px boss but not yet the per-boss runtime F:mboss/px/<id>/** they call (cm.md 9.3, px_build). While a target
    is missing (or is still this stub) it is written as a marked no-op, so every reference resolves; a real file of the
    core is never touched. The core's clean removes these on its own run; the generator order (core -> ... -> this)
    puts them back. Returns the names written."""
    disp = L.FN / 'mboss' / 'px'
    root = disp / A.ID
    wrote = []
    for fn in PX_TARGETS:
        d = disp / f'{fn}.mcfunction'
        if not d.exists() or f'function rlk:mboss/px/{A.ID}/{fn}' not in d.read_text(encoding='utf-8'):
            continue
        p = root / f'{fn}.mcfunction'
        if p.exists() and not p.read_text(encoding='utf-8').startswith(PX_MARK):
            continue
        root.mkdir(parents=True, exist_ok=True)
        text = (f'{PX_MARK}: rlk:mboss/px/{A.ID}/{fn} of the framework px runtime\n'
                '# (cm.md 9.3) that AZ-CM has not compiled yet; no proxies exist, so this does nothing.\n')
        if not p.exists() or p.read_text(encoding='utf-8') != text:
            p.write_text(text, encoding='utf-8')
        wrote.append(fn)
    return wrote


def foreign():
    """Paths under F:mboss/azhdaha/ that other generators own (relative, no extension): the rig's rig/ and the kit's
    owned dirs / files (fx.md 0.1; the kit manifest's "owned" when it exists). Returns (dirs, files)."""
    dirs = {'rig'} | {f'fx/{d}' for d in KitOwned.DIRS}
    files = {f'fx/{f}' for f in KitOwned.FILES}
    man = A._TOOLS / 'mboss_az_fx_manifest.json'
    pre = f'data/rlk/function/{OWN_TOP}/'
    if man.exists():
        own = json.loads(man.read_text(encoding='utf-8')).get('owned', {})
        dirs |= {d[len(pre):] for d in own.get('dirs', []) if d.startswith(pre)}
        files |= {f[len(pre):-len('.mcfunction')] for f in own.get('files', []) if f.startswith(pre)}
    return dirs, files


class KitOwned:
    DIRS = ('e', 'p', 'tele', 'snd', 'hud', 'prop', 'test')
    FILES = ('card', 'cardx', 'look', 'clear', 'uninstall')


def is_foreign(rel, dirs, files):
    return rel in files or any(rel == d or rel.startswith(d + '/') for d in dirs)


def clean(out):
    root = L.FN / OWN_TOP
    dirs, files = foreign()
    removed = 0
    for p in sorted(root.rglob('*.mcfunction')):
        rel = p.relative_to(root).with_suffix('').as_posix()
        if is_foreign(rel, dirs, files):
            assert p.resolve() not in out.written, f'the azhdaha core wrote into a foreign path: {rel}'
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


class Core:
    def __init__(self, g, pats):
        self.g, self.pats = g, pats
        self.F = g.fn
        self.by_id = {p.id: p for p in pats}

    def w(self, rel, lines):
        self.g.w(rel, lines)

    def pat(self, pid):
        return self.by_id[pid]

    def with_hook(self, hook, kinds=None):
        return [p for p in self.pats if self.g.has(f'p/{p.key}/{hook}') and (kinds is None or p.kind in kinds)]

    # =========================================================================================
    def emit(self):
        self.consts_vars()
        self.utils()
        self.hooks()
        self.prep()
        self.intro()
        AI.emit(self)
        self.services()                       # before slot(): its dispatchers list the files that exist (g.has)
        self.slot()
        self.cast_bg_b3()
        self.transitions()
        self.yaw()
        BR.emit(self)
        self.fields()
        self.orbs()
        self.after()
        self.addons()
        self.push()
        self.phases_looks()
        self.arena()
        self.hud()
        self.death()
        self.tests()

    # -----------------------------------------------------------------------------------------
    def consts_vars(self):
        yw = []
        for name in SR.YAW_CLIPS:
            c = A.CLIPS[name]
            yw.append(f'c{c["id"]}:[' + ','.join(str(int(round(v * 100))) for v in c['yaw']) + ']')
        self.w('ai/consts', [
            '# Module constants (spawn, reload): the moduli #azK<n> of Gen.every, the yaw schedules of the manifest (x 100,',
            '# storage az.yw.c<clip id>), the module objectives (entity: azT age, azS state / element, azPT owner pattern id,',
            '# azF field id; player: the brand azBrT azBrE azBrS azBrC).']
            + [sc(f'#azK{n}', n) for n in Gen.MODULI]
            + [f'scoreboard objectives add {o} dummy' for o in ('azT', 'azS', 'azPT', 'azF') + BR.OBJ]
            + ['data modify storage rlk:mboss az.yw set value {' + ','.join(yw) + '}'])
        v = ['# Every fight-time fake player of the module back to its fight-start value (spawn, cleanup). The rolled pair',
             '# (#azLeg / #azTail) is not touched: spawn re-reads it from cprep.azhdaha.pair (s2.md 4.4).']
        zero = ['#azPh', '#azTr', '#azTrN', '#azBur', '#azZone', '#azFldA', '#azOrbHigh', '#azLeap', '#azBgL', '#azBgLT',
                '#azBgT', '#azBgTT', '#azBgAny', '#azCast', '#azCT', '#azCastReq', '#azCastFirst', '#azB3T', '#azB3Sp', '#azPat',
                '#azPT', '#azPNew', '#azPEnd', '#azPMax', '#azPLen', '#azPRel', '#azPDone', '#azReq', '#azReqT', '#azPick',
                '#azLast', '#azRepN', '#azClk', '#azSkipF', '#azTailN', '#azFront', '#azTurnK', '#azFsI', '#azDwell',
                '#azPxHit', '#azPxF', '#azFN', '#azF45', '#azF35', '#azExit', '#azHint', '#azHintT', '#azCue',
                '#azLastHit', '#azFlN', '#azL2', '#azL39', '#azL7', '#azL7h', '#azLT', '#azBrHint', '#azShHint', '#azShCd',
                '#azHeal', '#azBrCs', '#azBrNew', '#azBrBan', '#azNoPush', '#azNoTurn', '#azYawC', '#azYawT', '#azYaw0',
                '#azFlash', '#azMov', '#azAftN', '#azFldN', '#azFSeq', '#azCH', '#azArEl', '#azArT', '#azWk', '#azPx']
        zero += [f'#azFs{i}' for i in range(AI.DWELL_N)]
        zero += [f'#azAft{k}' for k in range(16)] + [f'#azAftT{k}' for k in range(16)]
        for i in range(A.FIELD_SLOTS):
            zero += [f'#azF{i}', f'#azFE{i}', f'#azFT{i}', f'#azFB{i}', f'#azFS{i}', f'#azFA{i}']
        zero += [f'#azFG{f}' for f in (1, 2, 3)]
        zero += [f'#azCdE{p.id}' for p in self.pats if p.cooldown]
        v += [sc(k, 0) for k in zero]
        v += [sc('#azE', 5), sc('#azET', 5), sc('#azBand', 2), sc('#azSide', 1), sc('#azPaw', 1), sc('#azCool', 30),
              sc('#azA8', 1), sc('#azHudQ', 1), sc('#azYawS', 1), sc('#azPx', PX_ID['inv']),
              sc('#azPxGT', -1000000), sc('#azFlC', -1000000), sc('#azBrRf', -1000000), sc('#azDgClk', -1000000),
              sc('#azPopC', -1000)]
        self.w('ai/vars', v)

    # -----------------------------------------------------------------------------------------
    def utils(self):
        F, g = self.F, self.g
        self.w('u/lockp', ['# Marker rlk_mb_az_lock on the floor under the player\'s body, pulled inside the walk disc (any executor).',
                           'kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]',
                           f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_lock"]}}',
                           f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_lock,limit=1] run {g.clamp_walk()}'])
        self.w('u/lockb', ['# The lock pulled into the body disc r 8 (a point the body moves to).',
                           'kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]',
                           f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_lock"]}}',
                           f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_lock,limit=1] run {g.clamp_body()}'])
        self.w('u/lockb_r', ['# Macro {r}: the lock pulled into the disc r about the arena centre.',
                             'kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]',
                             f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_lock"]}}',
                             f'$execute as @e[type=minecraft:marker,tag=rlk_mb_az_lock,limit=1] run function {NS}u/clamp_r {{r:$(r)}}'])
        for name, r in (('clamp_w', A.WALK_R), ('clamp_b', A.BODY_R), ('clamp_s', A.SAFE_R - 0.5)):
            self.w(f'u/{name}', [f'# @s = a marker: pulled toward the arena axis (0.5 b steps) until within {L.num(r)} b of it.',
                                 sc('#azCl', 0), f'function {NS}u/{name}_s'])
            self.w(f'u/{name}_s', [
                f'execute at @s positioned ~ {CY} ~ if entity {ARENA_M.replace("limit=1", f"distance=..{L.num(r)},limit=1")} run return 0',
                'scoreboard players add #azCl mb 1', 'execute if score #azCl mb matches 90.. run return 0',
                f'execute at @s facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
                f'function {NS}u/{name}_s'])
        self.w('u/clamp_r', ['# Macro {r}: @s = a marker pulled toward the arena axis until within r b of it.', sc('#azCl', 0),
                             f'$function {NS}u/clamp_rs {{r:$(r)}}'])
        self.w('u/clamp_rs', [f'$execute at @s positioned ~ {CY} ~ if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..$(r),limit=1] run return 0',
                              'scoreboard players add #azCl mb 1', 'execute if score #azCl mb matches 90.. run return 0',
                              f'execute at @s facing entity {ARENA_M} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
                              f'$function {NS}u/clamp_rs {{r:$(r)}}'])
        self.w('u/okb', [f'# At a proposed body position: mv/ok (free, inside the safe disc) and within the body disc r {L.num(A.BODY_R)}.',
                         f'execute positioned ~ {CY} ~ unless entity {ARENA_M.replace("limit=1", f"distance=..{L.num(A.BODY_R)},limit=1")} run return fail',
                         'execute unless function rlk:mboss/mv/ok run return fail', 'return 1'])
        self.w('u/toward', [f'$execute at @s facing entity {PLAYER} feet rotated ~ 0 positioned ^ ^ ^$(d) if function {NS}u/okb run tp @s ~ ~ ~'])
        self.w('u/away', [f'$execute at @s facing entity {PLAYER} feet rotated ~180 0 positioned ^ ^ ^$(d) if function {NS}u/okb run tp @s ~ ~ ~'])
        self.w('u/fwd', [f'$execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^$(d) if function {NS}u/okb run tp @s ~ ~ ~'])
        self.w('u/flash', ['# The hit flash of the hit proxy\'s part group (manifest proxies.layout flash; 0 = the front group).']
               + [f'execute if score #azFlash mb matches {i} run return run {g.flash(grp)}' for grp, i in FLASH_GROUP.items()])

    # -----------------------------------------------------------------------------------------
    def hooks(self):
        F, g = self.F, self.g
        body = A.fw('cb/body')
        self.w('spawn', [
            '# Hook spawn (@s = the arena marker at the centre = POINTS spawn, rotated 180). The body (cb/body: no miniboss,',
            '# rlk_mb_big, rlk_mb_noshield; husk scale 0.1) faces south (yaw 0) toward the arrival; intro/setup builds the rest.',
            f'execute rotated 0 0 run {body}',
            f'execute as {BODY} at @s run {F("intro/setup")}'])
        tick = [
            '# Hook tick (@s = body, at it, fight state). Order (s2.md 3): clocks, the hit flash, brand + events, the floor',
            '# queue, the zone sampler (every 4 t), the idle AI / decision, the main slot (patterns, services, the B3 frame),',
            '# the cast slot, the bg slots L then T, the timers, the fields, the orbit centre, the push request, the HUD,',
            '# the arena ambience, the yaw driver, the rig tick last.',
            'scoreboard players add #azClk mb 1',
            f'execute if score #azFlash mb matches 1.. run {F("u/flash")}', sc('#azFlash', 0),
            F('brand/tick'),
            F('ev/tick'),
            'scoreboard players operation #azQ4 mb = #azClk mb', 'scoreboard players operation #azQ4 mb %= #azK4 mb',
            f'execute if score #azQ4 mb matches 0 run {F("ai/sample4")}',
            f'execute if score #azPat mb matches 0 run {F("ai/state")}',
            f'execute if score #azPat mb matches 1.. run {F("p/run")}',
            f'execute if score #azCast mb matches 1.. run {F("cast/run")}',
            f'execute if score #azBgL mb matches 1.. run {F("bg/run_l")}',
            f'execute if score #azBgT mb matches 1.. run {F("bg/run_t")}',
            sc('#azBgAny', 0),
            'execute if score #azBgL mb matches 1.. run scoreboard players set #azBgAny mb 1',
            'execute if score #azBgT mb matches 1.. run scoreboard players set #azBgAny mb 1',
            f'execute if score #azAftN mb matches 1.. run {F("aft/tick")}',
            f'execute if score #azFldN mb matches 1.. run {F("fld/tick")}',
            f'execute if entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] run {F("orb/centre")}',
            F('push/req'),
            F('hud/tick'),
            f'execute if score #azQ4 mb matches 0 run {F("arena/tick")}',
            f'execute if score #azYawC mb matches 1.. run {F("yaw/tick")}']
        tick += A.rig_tick_lines()
        tick += [sc('#azNoPush', 0), sc('#azNoTurn', 0)]
        self.w('tick', tick)
        on_hit = ['# Hook on_hit (@s = body inside combat/apply; #elem #dmg known). Scores only: the hit flash group of the hit',
                  '# proxy (#mbPart, cm.md 9.5; 0 / unset = a direct body hit -> front), the flank-proxy record of the AI.']
        on_hit += ['execute store result score #azPxGT mb run time query gametime', sc('#azPxHit', 0),
                   'execute if score #mbPart mb matches 1.. run scoreboard players operation #azPxHit mb = #mbPart mb',
                   sc('#azFlash', FLASH_GROUP['front'])]
        for k, lay in enumerate(SR.PROXY_LAYOUT, 1):
            on_hit.append(sci('#azPxHit', k, '#azFlash', FLASH_GROUP[lay[5]]))
        if not A.fw_has('res_pre'):
            on_hit += ['# LOCAL STUB of the framework RES pre-step (cm.md 8 res_pre): mres = mbRes<#elem> on the body.']
            on_hit += [f'execute if score #elem tmp matches {k} run scoreboard players operation @s mres = @s mbRes{k}' for k in range(9)]
            A.CMSTUBS['res_pre'] = '8'
        self.w('on_hit', on_hit)
        self.w('aux_hit', ['# Hook aux_hit: the module makes no breakable aux objects (the hit proxies route to the body).'])
        inc = ['# Hook incoming (@s = body inside combat/apply_mods, after the level factor and mres). RES is per element (the',
               '# registry res + the rolled pair, set at spawn; reactions resisted as their element). The HP floor #mbFloor is',
               '# the framework\'s (mboss/floor runs after this hook, cm.md 7.2).']
        if RES_BY_PHASE:
            inc.append('# RES_BY_PHASE: the rolled two are set at the absorbs (svc/phase_2 / _3)')
        if not A.fw_has('floor'):
            inc += ['# LOCAL STUB of the framework floor (cm.md 7.2) while AZ-CM is absent: the module clamps here.',
                    f'execute if score #mbFloor mb matches 1.. run {A.fw("floor")}']
        self.w('incoming', inc)
        self.w('pause', [
            '# Hook pause (the fight froze): the kit\'s attack telegraphs and the field pool go (the module redraws its field',
            '# table on resume), a kit flash on the title line ends; every active pattern\'s pause (main, cast, bg, B3 special).',
            K.tele_clear() if hasattr(K, 'tele_clear') else f'function {K.FN}tele/clear' if A.KIT else K._c('tele/clear'),
            f'function {K.FN}tele/field_clear' if A.KIT else K._c('tele/field_clear'),
            K.hud('flash_end'),
            F('p/pause_d')])
        self.w('resume', ['# Hook resume: the field decals again from the table; every active pattern\'s resume.',
                          F('fld/redraw'), F('p/resume_d')])
        self.w('cleanup', [
            '# Hook cleanup (no executor; idempotent): module fake players to their defaults, the module storage, the brand',
            '# and the shards, every module entity (props, seal, pattern entities: all rlk_mb_aux, the framework kills them',
            '# too), the kit\'s cards and HUD flags. The rolled pair survives in cprep.azhdaha.pair (the framework\'s).',
            F('brand/clear_all'), F('ai/vars'),
            'kill @e[tag=rlk_mb_az_ap]', f'kill @e[tag={"rlk_mb_az_seal"}]', 'kill @e[tag=rlk_mb_az_pat]',
            'kill @e[type=minecraft:marker,tag=rlk_mb_az_kept]',
            'data remove storage rlk:mboss az',
            f'function {K.FN}clear' if A.KIT else K._c('clear'), K.hud('clear')])
        unin = ['# Hook uninstall (no executor; every enabled module): the rig (real or stand-in), the kit, the module',
                '# entities, objectives and storage; the entrance glow chain.',
                f'function {A.rig_fn("kill")}', f'function {A.rig_fn("uninstall")}',
                f'function {K.FN}uninstall' if A.KIT else K._c('uninstall'),
                'kill @e[tag=rlk_mb_az_ap]', 'kill @e[tag=rlk_mb_az_seal]', 'kill @e[tag=rlk_mb_az_pat]',
                'kill @e[tag=rlk_mb_az_glyph]', 'kill @e[type=minecraft:item_display,tag=rlk_az_shard]',
                f'schedule clear {NS}prep_glow',
                'data remove storage rlk:mboss az']
        unin += [f'scoreboard objectives remove {o}' for o in ('azT', 'azS', 'azPT', 'azF') + BR.OBJ]
        if 'res_pre' in A.CMSTUBS:
            unin += [f'scoreboard objectives remove mbRes{k}' for k in range(9)]
        self.w('uninstall', unin)
        rl = [
            '# Hook reload (@s = body after /reload: every aux entity is gone: the rig parts, hazards, props, markers, orbs,',
            '# shards, proxies). Scores survive; the state is re-derived from them (plan 4.9):',
            '#   intro -> the fight starts; a normal main-slot pattern is cancelled; the cast slot is cancelled; a running',
            '#   service resumes through its reload (the landslide goes on, an absorb finishes at once, the B3 resumes at its',
            '#   frame tick); bg emitters and the B3 special re-make their props (reload hooks); fields are re-made from the',
            '#   table; the proxies respawn and are re-stated; the arena props are re-made; the rig respawns with its looks.',
            F('ai/consts'),
            'execute as @e[tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
            sc('#mbNoLeash', 0), sc('#azAftN', 0)] + [sc(f'#azAft{k}', 0) for k in range(16)] + [
            f'function {A.rig_fn("init")}', f'function {A.rig_fn("spawn")}', F('look/apply'),
            f'execute if score #mbSt mb matches 0 run {F("intro/done")}',
            '# (the framework re-spawned the proxies before this hook, cm.md 5.7; px.set survives: re-state the own state)',
            F('px/restate'),
            F('arena/props'), F('arena/look_now'),
            '# the main slot: services resume, patterns are cancelled',
            f'execute if score #azPat mb matches 1.. run {F("p/reload_d")}',
            f'execute if score #azCast mb matches 1.. run {F("cast/cancel")}',
            f'execute if score #azBgL mb matches 1.. run {F("bg/reload_l")}',
            f'execute if score #azBgT mb matches 1.. run {F("bg/reload_t")}',
            F('fld/remake'),
            sc('#azHudQ', 1)]
        self.w('reload', rl)
        self.w('bars', ['# Hook bars (@s = body, every tick in intro / fight): the under-bar (hud/bar).', F('hud/bar')])
        vis = ['# Hook hz_vis (@s = hazard marker, #hzEv 0 create / 1 strike / 2 end): routed by mbHzV / 10 = the pattern id.',
               'scoreboard players operation #azV mb = @s mbHzV', 'scoreboard players operation #azV mb /= #c10 mb']
        vis += [f'execute if score #azV mb matches {p.id} run return run {F(f"p/{p.key}/vis")}' for p in self.with_hook('vis')]
        self.w('hz_vis', vis)
        pj = ['# Hook pj_end (@s = prop, #pjEv, #pjKeep): routed by the prop\'s mbId (= the pattern id).']
        pj += [f'execute if score @s mbId matches {p.id} run return run {F(f"p/{p.key}/pj_end")}' for p in self.with_hook('pj_end')]
        self.w('pj_end', pj)
        self.w('test', ['# Hook test {id:N} (as the player, /function rlk:mboss/test/pattern {id:N}). See test/help.',
                        '$scoreboard players set #azTst mb $(id)',
                        f'execute as {BODY} at @s run {F("test/run")}'])

    # -----------------------------------------------------------------------------------------
    def prep(self):
        F, g = self.F, self.g
        th = A.THEME
        lines = ['# Hook prep (cm.md 5.3; @s = the kind-9 zone marker, at it; once per entrance build): roll the element pair',
                 '# (plan 4.1: 0 불/번개 1 물/얼음 2 불/얼음 3 물/번개), write cprep.azhdaha (pair, gate label, title, sub),',
                 '# the pair on the zone marker (data.az_pair), the two glyph props on the entrance stele (upper = tail, lower =',
                 '# leg), the stele glow chain (every 10 t while the props live).',
                 'execute store result score #azPair mb run random value 0..3']
        for i, (leg, tail) in A.PAIRS.items():
            lines.append(f'execute if score #azPair mb matches {i} run function {NS}prep/pair_{i}')
        lines += [f'function {NS}prep/glyphs']
        if th['glyphs']:
            lines.append(f'schedule function {NS}prep_glow 10t replace')
        self.w('prep', lines)
        for i, (leg, tail) in A.PAIRS.items():
            ln, tn = A.EL_NAME[leg], A.EL_NAME[tail]
            lc, tc = A.EL_COL[leg], A.EL_COL[tail]
            l1 = txt(A.BOSS['name'], GOLD, True)
            l2 = (f'[{txt("흡수 원소: ", "#C8C0B0")},{txt(ln, lc)},{txt(" (다리 · 2페이즈) · ", "#C8C0B0")},{txt(tn, tc)},'
                  f'{txt(" (꼬리 · 3페이즈)", "#C8C0B0")}]')
            l3 = txt(f'내성: 물리 · 바위 · {ln} · {tn} 30% · 그 외 10%', '#B0B0B0')
            gate = (f'{{item:"minecraft:paper",model:"rlk:mboss/az_kit/glyph_{A.EL_KEY[tail]}",item2:"minecraft:paper",'
                    f'model2:"rlk:mboss/az_kit/glyph_{A.EL_KEY[leg]}",l1:{l1},l2:{l2},l3:{l3},n:{A.N}}}')
            self.w(f'prep/pair_{i}', [
                f'# Pair {i}: legs {A.EL_KEY[leg]} ({ln}, phase 2), tail {A.EL_KEY[tail]} ({tn}, phase 3).',
                f'data modify storage rlk:mboss cprep.azhdaha.pair set value {{leg:{leg},tail:{tail},i:{i}}}',
                f'data modify storage rlk:mboss cprep.azhdaha.gate set value {gate}',
                f'data modify storage rlk:mboss cprep.azhdaha.title set value {txt(A.BOSS["name"], GOLD, True)}',
                f'data modify storage rlk:mboss cprep.azhdaha.sub set value {txt(A.BOSS["sub"] + " · " + ln + " / " + tn, "#E8E2D0")}',
                f'data modify entity @s data.az_pair set value {{leg:{leg},tail:{tail},i:{i}}}'])
        gl = ['# The two glyph props on the entrance stele (theme entrance_layout glyphs; rlk_room: room/clear removes them).',
              'kill @e[type=minecraft:item_display,tag=rlk_mb_az_glyph]']
        if not th['glyphs']:
            gl.append('# theme fallback (s2.md 5.1): no entrance glyphs, no glyph props')
        for slot, which in (('upper', 'tail'), ('lower', 'leg')):
            if slot not in th['glyphs']:
                continue
            x, y, z, yaw = th['glyphs'][slot]
            els = A.TAIL_ELS if which == 'tail' else A.LEG_ELS
            for e in els:
                gl.append(f'execute if data storage rlk:mboss cprep.azhdaha.pair{{{which}:{e}}} in minecraft:overworld run summon '
                          f'minecraft:item_display {L.num(x, 3)} {L.num(y, 3)} {L.num(z, 3)} {{Tags:["rlk_room","rlk_mb_az_glyph",'
                          f'"rlk_mb_az_glyph_{slot}"],Rotation:[{L.num(float(yaw))}f,0f],billboard:"fixed",brightness:{{block:15,sky:15}},'
                          'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],'
                          f'scale:[0.9f,0.9f,0.9f]}},item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":'
                          f'"rlk:mboss/az_kit/glyph_{A.EL_KEY[e]}"}}}}}}')
        self.w('prep/glyphs', gl)
        glow = ['# The entrance stele glow (every 10 t while its glyph props live; uninstall clears the schedule).',
                'execute unless entity @e[type=minecraft:item_display,tag=rlk_mb_az_glyph,limit=1] run return 0']
        if th['stele_glow']:
            gx, gy, gz = th['stele_glow']
            glow += [f'execute in minecraft:overworld positioned {L.num(gx, 3)} {L.num(gy, 3)} {L.num(gz, 3)} run {K.fx("glyph_glow")}',
                     f'execute in minecraft:overworld run particle minecraft:wax_on {L.num(gx, 3)} {L.num(gy, 3)} {L.num(gz, 3)} '
                     '0.25 0.6 0.1 0 2 force @a[tag=player]']
        glow.append(f'schedule function {NS}prep_glow 10t replace')
        self.w('prep_glow', glow)

    # -----------------------------------------------------------------------------------------
    def intro(self):
        F, g = self.F, self.g
        pair = ['# The rolled pair from cprep.azhdaha.pair (s2.md 4.4); LOCAL fallback while no prep ran (the mid-boss path of',
                '# the tests before AZ-CM): roll here.',
                'execute unless data storage rlk:mboss cprep.azhdaha.pair run execute store result score #azPair mb run random value 0..3']
        for i, (leg, tail) in A.PAIRS.items():
            pair.append(f'execute unless data storage rlk:mboss cprep.azhdaha.pair if score #azPair mb matches {i} run '
                        f'data modify storage rlk:mboss cprep.azhdaha.pair set value {{leg:{leg},tail:{tail},i:{i}}}')
        pair += ['execute store result score #azLeg mb run data get storage rlk:mboss cprep.azhdaha.pair.leg',
                 'execute store result score #azTail mb run data get storage rlk:mboss cprep.azhdaha.pair.tail',
                 'data modify storage rlk:mboss az.pair set from storage rlk:mboss cprep.azhdaha.pair']
        self.w('pair/read', pair)
        res = ['# @s = body: per-element RES (plan 4.2): the registry res (0 / 5 / *) + the rolled pair 30 (cm.md 8).']
        if 'res_pre' in A.CMSTUBS or not A.fw_has('res_pre'):
            res += ['# LOCAL STUB (cm.md 8 body_setup / res_set): the objectives and the registry values.']
            res += [f'scoreboard objectives add mbRes{k} dummy' for k in range(9)]
            rr = A.BOSS.get('res', {})
            for k in range(9):
                res.append(f'scoreboard players set @s mbRes{k} {int(rr.get(str(k), rr.get("*", 0)))}')
            res.append('tag @s add rlk_mb_resel')
        else:
            rr = A.BOSS.get('res', {})
            res += [f'scoreboard players set @s mbRes{k} {int(rr.get(str(k), rr.get("*", 0)))}' for k in (1, 2, 3, 4)]
        if not RES_BY_PHASE:
            for e in (1, 2):
                res.append(f'execute if score #azLeg mb matches {e} run scoreboard players set @s mbRes{e} 30')
            for e in (3, 4):
                res.append(f'execute if score #azTail mb matches {e} run scoreboard players set @s mbRes{e} 30')
        self.w('res/apply', res)
        self.w('intro/setup', [
            '# @s = the new body (from the spawn hook), at it: module state, the pair, RES, the rig (geo looks, matte gold),',
            '# the arena props (geo), the intro dressing, the intro clip; HUD.',
            F('ai/consts'), F('ai/vars'), F('pair/read'), F('res/apply'),
            f'function {A.rig_fn("init")}', f'function {A.rig_fn("spawn")}', F('look/geo'), g.glow(False),
            F('arena/props'), sc('#azArEl', 5), F('arena/look_now'),
            F('seq/intro/setup'), g.play('intro'),
            sc('#azPh', 0), sc('#azHudQ', 1), F('hud/refresh')])
        self.w('intro_tick', [
            f'# Hook intro_tick (@s = body, #mbT 1..; untargetable). Clip tick = #mbT - 1; the fight at #mbT {INTRO_DONE}.',
            *A.rig_tick_lines(),
            F('seq/intro/tick'),
            f'execute if score #mbT mb matches {INTRO_DONE}.. run {F("intro/done")}'])
        self.w('intro/done', [
            '# The intro is over: targetable, the proxies on, phase 1 (Geo, floor F1), the AI after a short cooldown.',
            'function rlk:mboss/intro_end', g.px('normal'), g.phase(1), sc('#azCool', 20), sc('#azHudQ', 1)])

    # -----------------------------------------------------------------------------------------
    def slot(self):
        F, g = self.F, self.g
        pats = self.pats
        begin = ['# @s = body. First tick of the main-slot pattern #azPat: clock -lead (0 for most), the clip at clock 0, start;',
                 '# a service started at #azReqT >= 1 (tests 25 / 61) resumes through its reload instead.',
                 sc('#azPNew', 0), sc('#azPT', 0), sc('#azPEnd', 0), sc('#azPRel', 0), sc('#azPMax', 200), sc('#azPLen', 200)]
        begin += [sci('#azPat', p.id, '#azPMax', p.max_len) for p in pats]
        begin += [sci('#azPat', p.id, '#azPLen', p.length) for p in pats]
        begin += [sci('#azPat', p.id, '#azPT', -p.lead) for p in pats if p.lead]
        begin += [f'execute if score #azReqT mb matches 1.. run return run {F("p/resume_at")}',
                  sc('#azHudQ', 1),
                  f'execute if score #azPT mb matches 0 run {F("p/clip_d")}',
                  F('p/start_d')]
        self.w('p/begin', begin)
        ra = ['# A service started at a later clock (#azReqT): PT = it, its reload re-derives the state.',
              'scoreboard players operation #azPT mb = #azReqT mb', sc('#azReqT', 0)]
        ra += [f'execute if score #azPat mb matches {p.id} run return run {F(f"p/{p.key}/reload")}'
               for p in pats if p.kind == 'service' and self.g.has(f'p/{p.key}/reload')]
        ra.append(F('p/start_d'))
        self.w('p/resume_at', ra)
        self.w('p/run', [
            '# @s = body. The main slot: start on the tick it was picked, then tick with #azPT = -lead+1 .. 0 (clip) .. ;',
            '# during a front pattern\'s lead the body pre-turns <= 4 deg/t.',
            f'execute if score #azPNew mb matches 1 run return run {F("p/begin")}',
            'scoreboard players add #azPT mb 1',
            f'execute if score #azPT mb matches ..-1 run function rlk:mboss/mv/turn {{max:{AI.TURN_LEAD}}}',
            f'execute if score #azPT mb matches 0 run {F("p/clip_d")}',
            F('p/tick_d'),
            f'execute if score #azPEnd mb matches 1 run return run {F("p/finish")}',
            f'execute if score #azPT mb >= #azPMax mb run {F("p/finish")}'])
        kills = ['kill @e[type=minecraft:marker,tag=rlk_mb_az_lock]', 'kill @e[type=minecraft:marker,tag=rlk_mb_az_kept]']
        self.w('p/finish', [
            '# @s = body. The pattern ended (p/end or its max_len): clear the slot and every marker it kept (no later run aims',
            '# at them), then the bookkeeping (ai/pat_done: services advance the transition).',
            'scoreboard players operation #azPDone mb = #azPat mb',
            sc('#azPat', 0), sc('#azPEnd', 0), sc('#azPT', 0), sc('#mbNoLeash', 0)] + kills + [
            F('ai/pat_done'), sc('#azPRel', 0), sc('#azHudQ', 1)])
        self.w('p/end', ['# Called by a pattern (any executor): it is done; the core finishes it after this tick\'s pattern tick.',
                         sc('#azPEnd', 1)])
        self.w('p/release', ['# Called by a pattern: its dangerous part is over: the bar hides; with a queued transition the core ends',
                             '# the pattern here (its cancel cleans the harmless tail, s2.md 15 decision 5).',
                             sc('#azPRel', 1), sc('#azHudQ', 1),
                             f'execute if score #azTr mb matches 1 as {BODY} run {F("p/cut")}'])
        self.w('p/cut', ['# @s = body: end the running pattern now (cancel + finish).', F('p/cancel_d'), F('p/finish')])
        self.w('p/cancel', [
            '# Stop the main slot now (tests, death, reload). The pattern\'s cancel runs as the caller: selectors only.',
            f'execute if score #azPat mb matches 1.. unless score #azPNew mb matches 1 run {F("p/cancel_d")}',
            sc('#azPat', 0), sc('#azPNew', 0), sc('#azPEnd', 0), sc('#azPT', 0), sc('#azPRel', 0), sc('#mbNoLeash', 0),
            sc('#azYawC', 0)] + kills + ['kill @e[tag=rlk_mb_az_pat]'])
        for name, target in (('start_d', 'start'), ('tick_d', 'tick'), ('cancel_d', 'cancel')):
            self.w(f'p/{name}', [f'# GENERATED: the running pattern\'s {target}, by #azPat.']
                   + [f'execute if score #azPat mb matches {p.id} run return run {F(f"p/{p.key}/{target}")}'
                      for p in pats if self.g.has(f'p/{p.key}/{target}')])
        rl = ['# GENERATED (reload): services resume through their reload; any other main-slot pattern is cancelled.']
        rl += [f'execute if score #azPat mb matches {p.id} run return run {F(f"p/{p.key}/reload")}'
               for p in pats if p.kind == 'service' and self.g.has(f'p/{p.key}/reload')]
        rl.append(F('p/cancel'))
        self.w('p/reload_d', rl)
        cd = ['# GENERATED: the running pattern\'s clip at clock 0 (the core plays it; #azPT = clip tick); variant clips by',
              '# #azPaw / #azSide; clips with a yaw schedule arm the yaw driver.']
        for p in pats:
            if p.clip is None:
                continue
            if isinstance(p.clip, dict):
                key = '#azPaw' if p.clip['by'] == 'paw' else '#azSide'
                for v, clip in p.clip['map'].items():
                    cd.append(f'execute if score #azPat mb matches {p.id} if score {key} mb matches {v} run {self.play_arm(clip)}')
                first = list(p.clip['map'].values())[0]
                cd.append(f'execute if score #azPat mb matches {p.id} run return run {self.play_arm(first)}')
            else:
                cd.append(f'execute if score #azPat mb matches {p.id} run return run {self.play_arm(p.clip)}')
        self.w('p/clip_d', cd)
        # make the variant lines return after the match
        cd2 = []
        for line in cd:
            if ' if score #azPaw mb matches ' in line or ' if score #azSide mb matches ' in line:
                line = line.replace(' run function ', ' run return run function ', 1)
            cd2.append(line)
        self.w('p/clip_d', cd2)
        for hook in ('pause', 'resume'):
            lines = [f'# GENERATED: the {hook} hook of every active pattern (main, cast, bg L / T, the B3 special).']
            for p in self.with_hook(hook):
                lines.append(f'execute if score #azPat mb matches {p.id} unless score #azPNew mb matches 1 run {F(f"p/{p.key}/{hook}")}')
                lines.append(f'execute if score #azCast mb matches {p.id} run {F(f"p/{p.key}/{hook}")}')
                lines.append(f'execute if score #azBgL mb matches {p.id} run {F(f"p/{p.key}/{hook}")}')
                lines.append(f'execute if score #azBgT mb matches {p.id} run {F(f"p/{p.key}/{hook}")}')
                lines.append(f'execute if score #azB3Sp mb matches {p.id} run {F(f"p/{p.key}/{hook}")}')
            self.w(f'p/{hook}_d', lines)
        # bookkeeping after a pattern
        pd = ['# @s = body. A main-slot pattern finished (#azPDone): a transition step advances; else the recovery, the',
              '# cooldown, the FLANK skip-once, P8 + turn180 when the player is still behind.',
              f'execute if score #azPDone mb matches 20..23 if score #azTr mb matches 2.. run return run {F("tr/next")}',
              f'execute if score #azPDone mb matches 30 if score #azTr mb matches 2 run return run {F("tr/next")}',
              sc('#azCool', 20), sc('#azCastFirst', 0)]
        pd += [sci('#azPDone', p.id, '#azCool', p.recover) for p in pats]
        for p in pats:
            if p.cooldown and p.kind == 'normal':
                pd += [f'execute if score #azPDone mb matches {p.id} run scoreboard players operation #azCdE{p.id} mb = #azClk mb',
                       f'execute if score #azPDone mb matches {p.id} run scoreboard players add #azCdE{p.id} mb {p.cooldown}']
        pd += [sci('#azPDone', pid, '#azSkipF', 1) for pid in AI.SKIP_AFTER]
        pd += [f'execute if score #azPDone mb matches 8 run {F("ai/p8_turn")}']
        self.w('ai/pat_done', pd)
        self.w('ai/p8_turn', ['# P8 ends with turn180 when the player is still behind the rump (plan 5 P8).',
                              F('ai/sample'),
                              'execute unless score #azZone mb matches 6..7 run return 0',
                              sc('#azTurnK', 5), 'execute if score #azS mb matches ..-1 run scoreboard players set #azTurnK mb 6',
                              sc('#azPick', 27), F('ai/go')])

    def play_arm(self, clip):
        """The play line of a clip; for clips with a yaw schedule, a small core function that also arms the yaw driver."""
        if clip in SR.YAW_CLIPS:
            return f'function {NS}yaw/play_{clip}'
        return self.g.play(clip)

    # -----------------------------------------------------------------------------------------
    def services(self):
        F, g = self.F, self.g
        # 27 turn (scripted yaw)
        tl = TL(g, 'turn')
        g.pw('turn', 'start', ['# Core service 27: a scripted turn step (#azTurnK 1 turn45_l 2 turn45_r 3 turn90_l 4 turn90_r 5 turn180',
                               '# 6 turn180 mirrored), the yaw driver turns the anchor by the manifest schedule.']
             + [f'execute if score #azTurnK mb matches {k} run return run function {NS}yaw/play_{c}{"_m" if k == 6 else ""}'
                for k, c in TURN_CLIPS.items()])
        tick = ['# The turn ends with its clip.']
        for k, c in TURN_CLIPS.items():
            tick.append(f'execute if score #azTurnK mb matches {k} if score #azPT mb matches {A.clip_len(c)}.. run {g.end()}')
        g.pw('turn', 'tick', tick)
        g.pw('turn', 'cancel', ['# The yaw driver stops.', sc('#azYawC', 0)])
        # 28 walk
        g.pw('walk', 'start', ['# Core service 28: walk toward the player (<= 40 t at 0.13 b/t, inside the body disc), then walk_stop.',
                               sc('#azWk', 0)])
        g.pw('walk', 'tick', [
            f'execute if score #azWk mb matches 0 if score #azPT mb matches ..{AI.WALK_MAX - 1} run function rlk:mboss/mv/turn {{max:4}}',
            f'execute if score #azWk mb matches 0 if score #azPT mb matches ..{AI.WALK_MAX - 1} run {g.bstep("fwd", AI.WALK_SPD)}',
            f'execute if score #azWk mb matches 0 if entity {PLAYER.replace("limit=1", f"distance=..{L.num(A.BAND_NEAR)},limit=1")} run {F("p/walk/stop")}',
            f'execute if score #azWk mb matches 0 if score #azPT mb matches {AI.WALK_MAX}.. run {F("p/walk/stop")}',
            f'execute if score #azWk mb matches 1.. run scoreboard players add #azWk mb 1',
            f'execute if score #azWk mb matches {A.clip_len("walk_stop") + 1}.. run {g.end()}'])
        g.pw('walk', 'stop', [sc('#azWk', 1), g.play('walk_stop')])
        g.pw('walk', 'cancel', ['# Nothing lingers.'])
        # 30 cast host
        rl, rr = A.clip_len('roar_low'), A.clip_len('roar_rear')
        g.pw('cast_host', 'start', [
            '# Core service 30 (s2.md 6): the host of a leg special. Transition 2 with live orbs: roar_low + p/orbs/refresh',
            '# (full life, no new orbs); else roar_rear and the cast slot (cast/leg at its t0, #azCT = the roar_rear tick).',
            sc('#azCH', 0),
            'execute if score #azCastFirst mb matches 1 if score #azLeg mb matches 2 if score #azBgL mb matches 31 run scoreboard players set #azCH mb 1',
            f'execute if score #azCH mb matches 1 run {g.play("roar_low")}',
            f'execute if score #azCH mb matches 1 run {F("p/orbs/refresh")}' if g.has('p/orbs/refresh') else '# (no p/orbs/refresh written)',
            f'execute if score #azCH mb matches 0 run {g.play("roar_rear")}',
            f'execute if score #azCH mb matches 0 run {g.cast_leg()}'])
        g.pw('cast_host', 'tick', [f'execute if score #azCH mb matches 1 if score #azPT mb matches {rl}.. run {g.end()}',
                                   f'execute if score #azCH mb matches 0 if score #azPT mb matches {rr}.. run {g.end()}'])
        g.pw('cast_host', 'cancel', ['# The cast slot is the core\'s (cast/cancel); nothing of the host lingers.'])

    # -----------------------------------------------------------------------------------------
    def cast_bg_b3(self):
        F, g = self.F, self.g
        casts = [p for p in self.pats if p.kind == 'cast']
        leg_of = {p.elem[1]: p for p in casts}
        cl = ['# The leg special into the cast slot (s2.md 6): #azCastReq (the AI pick or a test) else the rolled leg element',
              '# (31 orbs Hydro, 32 meteors Pyro); #azCT 0 = the roar_rear tick; its cast hook now.',
              f'execute if score #azCast mb matches 1.. run {F("cast/cancel")}',
              'scoreboard players operation #azX mb = #azCastReq mb', sc('#azCastReq', 0)]
        for el, p in leg_of.items():
            cl.append(f'execute unless score #azX mb matches 31..32 if score #azLeg mb matches {el} run scoreboard players set #azX mb {p.id}')
        cl += ['scoreboard players operation #azCast mb = #azX mb', sc('#azCT', 0)]
        cl += [f'execute if score #azCast mb matches {p.id} run return run {F(f"p/{p.key}/cast")}' for p in casts]
        self.w('cast/leg', cl)
        self.w('cast/run', ['# @s = body: the cast slot clock and the special\'s ctick.', 'scoreboard players add #azCT mb 1']
               + [f'execute if score #azCast mb matches {p.id} run return run {F(f"p/{p.key}/ctick")}' for p in casts])
        end = ['# g.cast_end(): the cast slot part is over; 32\'s cooldown starts here (31\'s at the orbs\' end, bg/end_l).']
        for p in casts:
            if p.id == 32 and p.cooldown:
                end += [f'execute if score #azCast mb matches {p.id} run scoreboard players operation #azCdE{p.id} mb = #azClk mb',
                        f'execute if score #azCast mb matches {p.id} run scoreboard players add #azCdE{p.id} mb {p.cooldown}']
        end += [sc('#azCast', 0)]
        self.w('cast/end', end)
        self.w('cast/cancel', ['# The cast slot stops now (selectors only in the special\'s cancel).']
               + [f'execute if score #azCast mb matches {p.id} run {F(f"p/{p.key}/cancel")}' for p in casts] + [sc('#azCast', 0)])
        for slot, clk in (('L', '#azBgLT'), ('T', '#azBgTT')):
            other = '#azPat' if slot == 'T' else '#azCast'
            first = '#azCast' if slot == 'L' else '#azPat'
            bgp = [p for p in self.pats if self.g.has(f'p/{p.key}/bgtick')]
            self.w(f'bg/start_{slot.lower()}', [f'# g.bg_start("{slot}"): the calling pattern moves into bg slot {slot} (clock {clk} 0 = this tick).',
                                        f'scoreboard players operation #azBg{slot} mb = {first} mb',
                                        f'execute unless score #azBg{slot} mb matches 1.. run scoreboard players operation #azBg{slot} mb = {other} mb',
                                        f'scoreboard players set {clk} mb -1'])
            self.w(f'bg/run_{slot.lower()}', [f'# @s = body: bg slot {slot}.', f'scoreboard players add {clk} mb 1']
                   + [f'execute if score #azBg{slot} mb matches {p.id} run return run {F(f"p/{p.key}/bgtick")}' for p in bgp])
            end = [f'# g.bg_end("{slot}"): the emitter is over; its cooldown starts here.']
            for p in bgp:
                if p.cooldown:
                    end += [f'execute if score #azBg{slot} mb matches {p.id} run scoreboard players operation #azCdE{p.id} mb = #azClk mb',
                            f'execute if score #azBg{slot} mb matches {p.id} run scoreboard players add #azCdE{p.id} mb {p.cooldown}']
            end += [sc(f'#azBg{slot}', 0), sc(clk, 0)]
            self.w(f'bg/end_{slot.lower()}', end)
            self.w(f'bg/cancel_{slot.lower()}', [f'# Cancel bg slot {slot} (selectors only): the emitter\'s cancel_bg, then the slot ends.']
                   + [f'execute if score #azBg{slot} mb matches {p.id} run {F(f"p/{p.key}/cancel_bg")}' for p in bgp
                      if self.g.has(f'p/{p.key}/cancel_bg')] + [F(f'bg/end_{slot.lower()}')])
            self.w(f'bg/reload_{slot.lower()}', [f'# /reload with bg slot {slot} live: the emitter re-makes its props (reload), else it ends.']
                   + [f'execute if score #azBg{slot} mb matches {p.id} run return run {F(f"p/{p.key}/reload")}' for p in bgp
                      if self.g.has(f'p/{p.key}/reload')] + [F(f'bg/end_{slot.lower()}')])
        specials = [p for p in self.pats if p.kind == 'special']
        start = ['# B3 special start (s2.md 7.2; from the B3 frame at B3_TAILUP): 41 frost (Cryo tail) / 42 bolt (Electro tail).']
        for p in specials:
            start.append(f'execute if score #azTail mb matches {p.elem[1]} run scoreboard players set #azB3Sp mb {p.id}')
        start += [f'execute if score #azB3Sp mb matches {p.id} run return run {F(f"p/{p.key}/start")}' for p in specials]
        self.w('b3/special_start', start)
        for op in ('tick', 'stop', 'reload', 'cancel'):
            hook = {'tick': 'b3tick', 'stop': 'stop', 'reload': 'reload', 'cancel': 'cancel'}[op]
            lines = [f'# B3 special {op} (s2.md 7.2).']
            lines += [f'execute if score #azB3Sp mb matches {p.id} run {F(f"p/{p.key}/{hook}")}' for p in specials
                      if self.g.has(f'p/{p.key}/{hook}')]
            if op in ('stop', 'cancel'):
                lines.append(sc('#azB3Sp', 0))
            self.w(f'b3/special_{op}', lines)

    # -----------------------------------------------------------------------------------------
    def transitions(self):
        F, g = self.F, self.g
        self.w('ev/tick', [
            '# @s = body: the floor events (plan 4.3): a hit with mhpC - raw <= #mbFloor (#mbFloorHit, framework) or mhpC <=',
            '# #mbFloor (DoTs, reactions) in phases 1-2 queues the transition; the "흡수 중 (raw)" popup at most once per 10 t.',
            f'execute if score #mbFloorHit mb matches 1 run {F("ev/pop")}',
            'execute if score #azPh mb matches 1..2 if score #azTr mb matches 0 if score #mbFloor mb matches 1.. if score #mbFloorHit mb matches 1 '
            f'run {F("tr/queue")}',
            'execute if score #azPh mb matches 1..2 if score #azTr mb matches 0 if score #mbFloor mb matches 1.. if score @s mhpC <= #mbFloor mb '
            f'run {F("tr/queue")}',
            sc('#mbFloorHit', 0),
            f'execute if score #azTr mb matches 1.. if score #azPh mb matches 1..2 run scoreboard players set #azOrbHigh mb 1'])
        self.w('ev/pop', [
            '# The floor popup "흡수 중 (raw)" (the unclamped value in grey), at most once per 10 t, above the head.',
            'scoreboard players operation #azX mb = #azClk mb', 'scoreboard players operation #azX mb -= #azPopC mb',
            'execute if score #azX mb matches ..9 run return 0', 'scoreboard players operation #azPopC mb = #azClk mb',
            'execute store result storage rlk:mboss az.pop.raw int 1 run scoreboard players get #mbFloorRaw mb',
            f'execute at @s rotated as @s positioned ^ ^4.2 ^4.3 run function {NS}ev/pop_m with storage rlk:mboss az.pop'])
        self.w('ev/pop_m', ['$summon minecraft:text_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pop"],billboard:"center",'
                            'text:[{text:"흡수 중 ",color:"#FFD27A"},{text:"($(raw))",color:"gray"}],background:0,see_through:1b,'
                            'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.4f,1.4f,1.4f]}}',
                            'scoreboard players set @e[type=minecraft:text_display,tag=rlk_mb_az_pop] azT 16'])
        self.w('tr/queue', [
            '# The floor was reached: the transition is queued (#azTr 1, #azTrN = the phase); bg T is cancelled, the orbs ride',
            '# high; a released pattern ends now (its harmless tail cancelled).',
            sc('#azTr', 1), 'scoreboard players operation #azTrN mb = #azPh mb',
            F('bg/cancel_t'), sc('#azOrbHigh', 1), sc('#azHudQ', 1),
            f'execute if score #azPat mb matches 1.. if score #azPRel mb matches 1 run {F("p/cut")}'])
        self.w('tr/begin', [
            '# A decision point with a queued transition: the message, then transition 1 = 20 -> 21, transition 2 = the leg',
            '# special first (service 30) -> 20 -> 22 -> 23.',
            F('tr/msg'),
            f'execute if score #azTrN mb matches 2 run return run {F("tr/begin2")}',
            sc('#azTr', 3), sc('#azPat', 20), sc('#azPNew', 1), sc('#azReqT', 0)])
        self.w('tr/begin2', [sc('#azTr', 2), sc('#azCastFirst', 1), sc('#azCastReq', 0), sc('#azPat', 30), sc('#azPNew', 1),
                             sc('#azReqT', 0)])
        msg = ['# The transition message: kit banner (the element named: transition 1 the leg element, 2 the tail element) +',
               '# the chime; the sub-line shows the message while #azTr >= 1.']
        for e in A.LEG_ELS:
            msg.append(f'execute if score #azTrN mb matches 1 if score #azLeg mb matches {e} run {K.hude("banner_tr", e)}')
        for e in A.TAIL_ELS:
            msg.append(f'execute if score #azTrN mb matches 2 if score #azTail mb matches {e} run {K.hude("banner_tr", e)}')
        msg += [K.snd('msg_chime'), 'execute as @a[tag=player] at @s run ' + L.sound('block.bell.resonate', 0.8, 0.6, target='@s'),
                'execute as @a[tag=player] at @s run ' + L.sound('block.respawn_anchor.charge', 0.7, 0.5, target='@s'),
                sc('#azHudQ', 1)]
        self.w('tr/msg', msg)
        self.w('tr/next', [
            '# A transition step finished: the next one.',
            f'execute if score #azTr mb matches 2 run return run {F("tr/to_slide")}',
            f'execute if score #azTr mb matches 3 if score #azTrN mb matches 1 run return run {F("tr/to_abs1")}',
            f'execute if score #azTr mb matches 3 if score #azTrN mb matches 2 run return run {F("tr/to_abs2")}',
            f'execute if score #azTr mb matches 4 if score #azTrN mb matches 1 run return run {F("tr/done")}',
            f'execute if score #azTr mb matches 4 if score #azTrN mb matches 2 run return run {F("tr/to_b3")}',
            F('tr/done')])
        for name, step, pid in (('to_slide', 3, 20), ('to_abs1', 4, 21), ('to_abs2', 4, 22), ('to_b3', 5, 23)):
            self.w(f'tr/{name}', [sc('#azTr', step), sc('#azPat', pid), sc('#azPNew', 1), sc('#azReqT', 0), sc('#azCastFirst', 0)])
        self.w('tr/done', ['# The transition is over (phase 2 after absorb 1; phase 3 surfaced after the B3).',
                           sc('#azTr', 0), sc('#azTrN', 0), sc('#azOrbHigh', 0), sc('#azSkipF', 1), sc('#azCool', 20),
                           sc('#azCastFirst', 0), sc('#azHudQ', 1)])

    # -----------------------------------------------------------------------------------------
    def yaw(self):
        F, g = self.F, self.g
        for clip in SR.YAW_CLIPS:
            cid = A.clip_id(clip)
            for mirror in ((False, True) if clip == 'turn180' else (False,)):
                s = -1 if mirror else 1
                nm = f'yaw/play_{clip}' + ('_m' if mirror else '')
                self.w(nm, [f'# Play {clip}{" mirrored (to the right)" if mirror else ""} and arm the yaw driver (the anchor turns by the',
                            '# manifest schedule; teleport_duration carries it).',
                            g.play(clip), sc('#azYawC', cid), sc('#azYawS', s), sc('#azYawT', -1),
                            'execute store result score #azYaw0 mb run data get entity @s Rotation[0] 100'])
        lens = {A.clip_id(c): A.clip_len(c) for c in SR.YAW_CLIPS}
        self.w('yaw/tick', ['# @s = body: the scripted yaw (Rotation = start + sign x schedule[t] / 100); off at the clip end.',
                            'scoreboard players add #azYawT mb 1']
               + [f'execute if score #azYawC mb matches {cid} if score #azYawT mb matches {n}.. run return run scoreboard players set #azYawC mb 0'
                  for cid, n in lens.items()]
               + ['execute store result storage rlk:mboss az.ya.c int 1 run scoreboard players get #azYawC mb',
                  'execute store result storage rlk:mboss az.ya.t int 1 run scoreboard players get #azYawT mb',
                  f'function {NS}yaw/get with storage rlk:mboss az.ya',
                  'scoreboard players operation #azYd mb *= #azYawS mb',
                  'scoreboard players operation #azYd mb += #azYaw0 mb',
                  'execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #azYd mb'])
        self.w('yaw/get', ['$execute store result score #azYd mb run data get storage rlk:mboss az.yw.c$(c)[$(t)]'])

    # -----------------------------------------------------------------------------------------
    def fields(self):
        F, g = self.F, self.g
        N = A.FIELD_SLOTS
        new = ['# N6 (s2.md 9): a lingering field here (rotated as the context), args in storage az.nf {fam r len w life dmg sh',
               '# area rule yaw el}: a free slot (else the oldest overall is cancelled), the family cap, the 220 b2 total (the',
               '# oldest of the family first, else the oldest overall), the clear melee points (pattern fields only), the hazard',
               '# (#hzAct = life, #hzRearm 10, the family\'s volley group, quiet, NoRx), the kit field card, the table.',
               'execute store result score #azNfF mb run data get storage rlk:mboss az.nf.fam',
               'execute store result score #azNfA mb run data get storage rlk:mboss az.nf.area',
               F('fld/cap_fam'), F('fld/cap_area'),
               sc('#azNfI', -1)]
        for i in reversed(range(N)):
            new.append(f'execute if score #azF{i} mb matches 0 run scoreboard players set #azNfI mb {i}')
        new += [f'execute if score #azNfI mb matches -1 run {F("fld/cancel_oldest")}']
        for i in reversed(range(N)):
            new.append(f'execute if score #azNfI mb matches -1 if score #azF{i} mb matches 0 run scoreboard players set #azNfI mb {i}')
        new += ['kill @e[type=minecraft:marker,tag=rlk_mb_az_fnew]',
                'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_fnew"]}',
                'execute rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run tp @s ~ ~ ~ ~ 0',
                f'execute unless data storage rlk:mboss az.nf{{rule:1}} unless data storage rlk:mboss az.nf{{sh:1}} as '
                f'@e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run {F("fld/clear_pts")}',
                f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run {g.clamp_walk()}']
        for i in range(N):
            new.append(f'execute if score #azNfI mb matches {i} at @e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] rotated as '
                       f'@e[type=minecraft:marker,tag=rlk_mb_az_fnew,limit=1] run {F(f"fld/make_{i}")}')
        new += ['kill @e[type=minecraft:marker,tag=rlk_mb_az_fnew]']
        self.w('fld/new', new)
        # caps
        capf = ['# The family cap (fire 4, hail 2, strip 1): the oldest of the family goes when it is full.', sc('#azX', 0)]
        capf += [f'execute if score #azF{i} mb = #azNfF mb run scoreboard players add #azX mb 1' for i in range(N)]
        for fam, cap in A.FIELD_CAPS.items():
            capf.append(f'execute if score #azNfF mb matches {A.FIELD_FAM[fam]} if score #azX mb matches {cap}.. run {F("fld/cancel_oldest_fam")}')
        self.w('fld/cap_fam', capf)
        self.w('fld/cap_area', [f'# The total lingering area <= {A.FIELD_AREA_MAX} b2: the oldest (of the family, else any) goes until it fits.',
                                'scoreboard players operation #azX mb = #azFldA mb', 'scoreboard players operation #azX mb += #azNfA mb',
                                f'execute if score #azX mb matches ..{A.FIELD_AREA_MAX} run return 0',
                                'execute if score #azFldN mb matches 0 run return 0',
                                F('fld/cancel_oldest_fam'),
                                'scoreboard players operation #azX mb = #azFldA mb', 'scoreboard players operation #azX mb += #azNfA mb',
                                f'execute if score #azX mb matches {A.FIELD_AREA_MAX + 1}.. run {F("fld/cancel_oldest")}',
                                'scoreboard players operation #azX mb = #azFldA mb', 'scoreboard players operation #azX mb += #azNfA mb',
                                f'execute if score #azX mb matches {A.FIELD_AREA_MAX + 1}.. if score #azFldN mb matches 1.. run {F("fld/cap_area")}'])
        for nm, fam_only in (('fld/cancel_oldest', False), ('fld/cancel_oldest_fam', True)):
            lines = ['# Cancel the oldest live field' + (' of the new field\'s family' if fam_only else '') + ' (lowest sequence).',
                     sc('#azX', 2147483647), sc('#azY', -1)]
            for i in range(N):
                cond = f'if score #azF{i} mb = #azNfF mb' if fam_only else f'if score #azF{i} mb matches 1..'
                lines.append(f'execute {cond} if score #azFS{i} mb < #azX mb run scoreboard players set #azY mb {i}')
                lines.append(f'execute {cond} if score #azFS{i} mb < #azX mb run scoreboard players operation #azX mb = #azFS{i} mb')
            lines += [f'execute if score #azY mb matches {i} run {F(f"fld/cancel_{i}")}' for i in range(N)]
            self.w(nm, lines)
        # the clear melee points: the head-front point and the tail-lane point (anchor frame)
        hf, tl_ = A.P_HEAD_FRONT, A.P_TAIL_LANE
        cp = ['# @s = the new field\'s centre marker (pattern fields only): never within r + 1.5 of the head-front point or the',
              '# tail-lane point; pushed radially outward. #azNfR = r + pad (tenths -> the macro distance).',
              'execute store result score #azX mb run data get storage rlk:mboss az.nf.r',
              f'scoreboard players add #azX mb {int(A.CLEAR_PAD * 10)}',
              'execute store result storage rlk:mboss az.cp.d double 0.1 run scoreboard players get #azX mb']
        for nm, (x, _, z) in (('head', hf), ('tail', tl_)):
            cp.append(f'execute as {BODY} at @s rotated as @s rotated ~ 0 positioned ^{L.num(x)} ^ ^{L.num(z)} run '
                      f'function {NS}fld/cp_m with storage rlk:mboss az.cp')
        self.w('fld/clear_pts', cp)
        self.w('fld/cp_m', ['# Macro {d}: at a clear point; a field centre (rlk_mb_az_fnew) within d is pushed out to d.',
                            '$execute as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,distance=..$(d),limit=1] at @s positioned ~0.01 ~ ~ run '
                            'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_fcp"]}',
                            '$execute as @e[type=minecraft:marker,tag=rlk_mb_az_fnew,distance=..$(d),limit=1] facing entity '
                            '@e[type=minecraft:marker,tag=rlk_mb_az_fcp,limit=1] feet rotated ~ 0 positioned ^ ^ ^$(d) run tp @s ~ ~ ~',
                            'kill @e[type=minecraft:marker,tag=rlk_mb_az_fcp]'])
        for i in range(N):
            tag = f'rlk_mb_az_fld{i}'
            mk = [f'# Field slot {i} (positioned at the field, rotated = its line yaw).',
                  f'kill @e[type=minecraft:marker,tag={tag}]',
                  'execute store result score #azNfL mb run data get storage rlk:mboss az.nf.life',
                  'execute store result score #hzAct mb run data get storage rlk:mboss az.nf.life',
                  f'scoreboard players set #hzRearm mb {A.FIELD_REARM}', sc('#hzQuiet', 1), sc('#hzSfx', 0),
                  'execute store result score #hzEl mb run data get storage rlk:mboss az.nf.el']
            if 'norx' in A._HZK or A.fw_has('pl_dot'):
                mk.append(sc('#hzNR', 1))
            mk += ['# the family\'s volley group (one tick per 10 t however many fields of that family overlap)']
            for f in (1, 2, 3):
                mk += [f'execute if score #azNfF mb matches {f} unless score #azFG{f} mb matches 1.. run {L.GRP_NEW}',
                       f'execute if score #azNfF mb matches {f} unless score #azFG{f} mb matches 1.. run scoreboard players operation #azFG{f} mb = #mbGrp mb',
                       f'execute if score #azNfF mb matches {f} run scoreboard players operation #hzGrp mb = #azFG{f} mb']
            mk += ['execute store result storage rlk:mboss az.nf.tell int 1 run scoreboard players set #azX mb 1',
                   'execute if data storage rlk:mboss az.nf{sh:0} run function rlk:mboss/hz/disc with storage rlk:mboss az.nf',
                   f'execute if data storage rlk:mboss az.nf{{sh:1}} run function {NS}fld/line with storage rlk:mboss az.nf',
                   g.tag_last_hz(tag), g.tag_last_hz('rlk_mb_az_fld'),
                   f'scoreboard players set @e[type=minecraft:marker,tag={tag}] azF {i}',
                   f'scoreboard players operation #azF{i} mb = #azNfF mb',
                   f'scoreboard players operation #azFE{i} mb = #azClk mb', f'scoreboard players operation #azFE{i} mb += #azNfL mb',
                   f'scoreboard players operation #azFT{i} mb = #azClk mb',
                   f'scoreboard players operation #azFB{i} mb = #azNfL mb',
                   'scoreboard players add #azFSeq mb 1', f'scoreboard players operation #azFS{i} mb = #azFSeq mb',
                   f'scoreboard players operation #azFA{i} mb = #azNfA mb',
                   'scoreboard players operation #azFldA mb += #azNfA mb', 'scoreboard players add #azFldN mb 1',
                   f'data modify storage rlk:mboss az.f{i} set from storage rlk:mboss az.nf',
                   f'execute store result storage rlk:mboss az.f{i}.x double 0.001 run data get entity @e[type=minecraft:marker,tag={tag},limit=1] Pos[0] 1000',
                   f'execute store result storage rlk:mboss az.f{i}.y double 0.001 run data get entity @e[type=minecraft:marker,tag={tag},limit=1] Pos[1] 1000',
                   f'execute store result storage rlk:mboss az.f{i}.z double 0.001 run data get entity @e[type=minecraft:marker,tag={tag},limit=1] Pos[2] 1000',
                   f'execute store result storage rlk:mboss az.f{i}.ry int 1 run data get entity @e[type=minecraft:marker,tag={tag},limit=1] Rotation[0]',
                   f'data modify storage rlk:mboss az.f{i}.id set value {i}',
                   f'function {NS}fld/draw_{i}']
            self.w(f'fld/make_{i}', mk)
            dr = [f'# The kit card of field slot {i} with its remaining life (made, refreshed, resumed).',
                  f'execute store result storage rlk:mboss az.f{i}.left int 1 run scoreboard players operation #azX mb = #azFE{i} mb',
                  f'scoreboard players operation #azX mb -= #azClk mb',
                  f'execute store result storage rlk:mboss az.f{i}.left int 1 run scoreboard players get #azX mb']
            if A.KIT:
                dr += [f'execute if data storage rlk:mboss az.f{i}{{sh:0}} run function {NS}fld/kdisc with storage rlk:mboss az.f{i}',
                       f'execute if data storage rlk:mboss az.f{i}{{sh:1}} run function {NS}fld/kstrip with storage rlk:mboss az.f{i}']
            else:
                dr += [f'execute if data storage rlk:mboss az.f{i}{{sh:0}} run {K._c("tele/field", id=i)}',
                       f'execute if data storage rlk:mboss az.f{i}{{sh:1}} run {K._c("tele/strip", id=i)}']
            self.w(f'fld/draw_{i}', dr)
            self.w(f'fld/cancel_{i}', [f'# Field slot {i} ends now (cap, death, cleanup): the hazard, the kit card, the table.',
                                       f'kill @e[type=minecraft:marker,tag={tag}]',
                                       K.tele_field_end(i) if not A.KIT else f'function {K.FN}tele/field_end {{id:{i}}}',
                                       f'execute if score #azF{i} mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA{i} mb',
                                       f'execute if score #azF{i} mb matches 1.. run scoreboard players remove #azFldN mb 1',
                                       sc(f'#azF{i}', 0), f'data remove storage rlk:mboss az.f{i}'])
        if A.KIT:
            self.w('fld/kdisc', [f'$execute positioned $(x) $(y) $(z) run function {K.FN}tele/field {{id:$(id),r:$(r),el:$(el),life:$(left)}}'])
            self.w('fld/kstrip', [f'$execute positioned $(x) $(y) $(z) run function {K.FN}tele/strip {{id:$(id),len:$(len),w:$(w),yaw:$(ry),el:$(el),life:$(left)}}'])
        self.w('fld/line', ['# Macro: a line field from here along the context yaw (len, w tenths).',
                            '$function rlk:mboss/hz/line {len:$(len),w:$(w),tell:1,dmg:$(dmg)}'])
        tick = ['# @s = body: the field table: a field whose end tick passed is freed (its hazard expires by itself).']
        for i in range(N):
            tick.append(f'execute if score #azF{i} mb matches 1.. if score #azClk mb >= #azFE{i} mb run {F(f"fld/cancel_{i}")}')
        for f in (1, 2, 3):
            tick.append(f'execute unless score #azF0 mb matches {f} ' + ' '.join(f'unless score #azF{i} mb matches {f}' for i in range(1, N))
                        + f' run scoreboard players set #azFG{f} mb 0')
        self.w('fld/tick', tick)
        rf = ['# Macro {n} (@s = a field hazard marker, azF = its slot): extend by n, at most 2x its base life; the kit redraws it.',
              '$scoreboard players set #azX mb $(n)', 'scoreboard players operation #azNfI mb = @s azF']
        rf += [f'execute if score #azNfI mb matches {i} run return run {F(f"fld/ext_{i}")}' for i in range(N)]
        self.w('fld/refresh', rf)
        for i in range(N):
            self.w(f'fld/ext_{i}', [
                f'# @s = the hazard of slot {i}; #azX = the requested ticks. New end = min(end + n, start + 2 x base).',
                f'scoreboard players operation #azY mb = #azFT{i} mb', f'scoreboard players operation #azY mb += #azFB{i} mb',
                f'scoreboard players operation #azY mb += #azFB{i} mb',
                f'scoreboard players operation #azZ mb = #azFE{i} mb', 'scoreboard players operation #azZ mb += #azX mb',
                'execute if score #azZ mb > #azY mb run scoreboard players operation #azZ mb = #azY mb',
                f'scoreboard players operation #azX mb = #azZ mb', f'scoreboard players operation #azX mb -= #azFE{i} mb',
                'execute if score #azX mb matches ..0 run return 0',
                f'scoreboard players operation #azFE{i} mb = #azZ mb',
                'execute store result storage rlk:mboss az.ext.n int 1 run scoreboard players get #azX mb',
                f'function {NS}fld/ext_m with storage rlk:mboss az.ext',
                f'function {NS}fld/draw_{i}'])
        self.w('fld/ext_m', [A.fw('hz/extend', '{n:$(n)}').replace('function', '$function', 1)])
        self.w('fld/redraw', ['# Every live field\'s kit card again with its remaining life (resume).']
               + [f'execute if score #azF{i} mb matches 1.. run {F(f"fld/draw_{i}")}' for i in range(N)])
        self.w('fld/remake', ['# /reload: every live field re-made from the table (the hazard with its remaining life, the card).']
               + [f'execute if score #azF{i} mb matches 1.. run {F(f"fld/remake_{i}")}' for i in range(N)])
        for i in range(N):
            self.w(f'fld/remake_{i}', [
                f'scoreboard players operation #azX mb = #azFE{i} mb', 'scoreboard players operation #azX mb -= #azClk mb',
                f'execute if score #azX mb matches ..0 run return run {F(f"fld/cancel_{i}")}',
                f'data modify storage rlk:mboss az.nf set from storage rlk:mboss az.f{i}',
                'execute store result storage rlk:mboss az.nf.life int 1 run scoreboard players get #azX mb',
                'execute store result score #azNfF mb run data get storage rlk:mboss az.nf.fam',
                'execute store result score #azNfA mb run data get storage rlk:mboss az.nf.area',
                f'execute if score #azF{i} mb matches 1.. run scoreboard players operation #azFldA mb -= #azFA{i} mb',
                f'execute if score #azF{i} mb matches 1.. run scoreboard players remove #azFldN mb 1',
                sc(f'#azFG{1}', 0), sc(f'#azFG{2}', 0), sc(f'#azFG{3}', 0),
                f'function {NS}fld/remake_m with storage rlk:mboss az.f{i}'])
        self.w('fld/remake_m', [f'$execute positioned $(x) $(y) $(z) rotated $(ry) 0 run function {NS}fld/remake_go {{i:$(id)}}'])
        self.w('fld/remake_go', ['$scoreboard players set #azNfI mb $(i)']
               + [f'execute if score #azNfI mb matches {i} run return run {F(f"fld/make_{i}")}' for i in range(N)])
        self.w('fld/clear', ['# Every field now (death, cleanup, tests).'] + [F(f'fld/cancel_{i}') for i in range(N)]
               + [sc('#azFldA', 0), sc('#azFldN', 0)] + [sc(f'#azFG{f}', 0) for f in (1, 2, 3)])

    # -----------------------------------------------------------------------------------------
    def orbs(self):
        F, g = self.F, self.g
        self.w('orb/spawn', [
            '# N5 (macro {tag ring a r w hr y0 y1 dmg grp}; as the body, positioned at the orbit centre): one orb = a marker',
            '# (angle azS x 100 deg, radius azT mb, omega azPT x 100 deg/t) + its hz/disc (#hzRearm 10) that follows it.',
            f'execute unless entity @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] run summon minecraft:marker ~ {CY} ~ '
            '{Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_orbc"]}',
            '$summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_orb","$(tag)","rlk_mb_az_onew"]}',
            '$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] azS $(a)',
            '$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] azT $(r)',
            '$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] azPT $(w)',
            '$scoreboard players set @e[type=minecraft:marker,tag=rlk_mb_az_onew] mbS $(ring)',
            '$scoreboard players set #hzY0 mb $(y0)', '$scoreboard players set #hzY1 mb $(y1)',
            '$scoreboard players set #azX mb $(grp)',
            'execute if score #azX mb matches 1 run scoreboard players operation #hzGrp mb = #mbGrp mb',
            f'scoreboard players set #hzRearm mb {A.FIELD_REARM}', sc('#hzQuiet', 1), sc('#hzSfx', 0), 'scoreboard players set #hzAct mb 2000',
            '$function rlk:mboss/hz/disc {r:$(hr),tell:1,dmg:$(dmg)}',
            'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_mb_az_orbhz',
            'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run scoreboard players operation @s azF = #hzLast mb',
            'scoreboard players operation @e[type=minecraft:marker,tag=rlk_mb_az_onew] azF = #hzLast mb',
            'tag @e[type=minecraft:marker,tag=rlk_mb_az_onew] remove rlk_mb_az_onew'])
        self.w('orb/centre', [
            '# The orbit centre follows the anchor at <= 0.2 b/t (frozen while #azLeap 1).',
            'execute if score #azLeap mb matches 1 run return 0',
            f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] at @s if entity {BODY.replace("limit=1", "distance=..0.2,limit=1")} '
            f'run return run tp @s {BODY}',
            f'execute as @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] at @s facing entity {BODY} feet rotated ~ 0 positioned ^ ^ ^0.2 run tp @s ~ ~ ~'])
        self.w('orb/step', [
            '# @s = an orb marker: angle += omega; at the centre + r (sin, cos) of the angle (plain tp of the marker and its',
            '# hazard); the band rides high while #azOrbHigh 1 (transitions, absorbs) or in the head-lane eye (S2-L refines).',
            'scoreboard players operation @s azS += @s azPT',
            'execute store result storage rlk:mboss az.ob.a float 0.01 run scoreboard players get @s azS',
            'execute store result storage rlk:mboss az.ob.r double 0.001 run scoreboard players get @s azT',
            f'execute at @e[type=minecraft:marker,tag=rlk_mb_az_orbc,limit=1] run function {NS}orb/place with storage rlk:mboss az.ob',
            f'scoreboard players operation #azX mb = @s azF',
            f'execute at @s as @e[type=minecraft:marker,tag=rlk_mb_az_orbhz] if score @s mbHzI = #azX mb run tp @s ~ ~ ~',
            f'execute if score #azOrbHigh mb matches 1 as @e[type=minecraft:marker,tag=rlk_mb_az_orbhz] if score @s mbHzI = #azX mb run '
            'scoreboard players set @s mbHzY0 2600'])
        self.w('orb/place', ['$execute rotated $(a) 0 positioned ^ ^ ^$(r) run tp @s ~ ~ ~'])

    # -----------------------------------------------------------------------------------------
    def after(self):
        F, g = self.F, self.g
        new = ['# N13 g.after(delay, rel): a free slot k (16) holds the function id #azAftF until #azClk + #azAftD; its marker',
               '# rlk_az_aft<k> keeps the position / rotation. Full: the oldest-free check fails silently (logged by tests).',
               sc('#azAftI', -1)]
        for k in reversed(range(16)):
            new.append(f'execute if score #azAft{k} mb matches 0 run scoreboard players set #azAftI mb {k}')
        for k in range(16):
            new.append(f'execute if score #azAftI mb matches {k} run {F(f"aft/set_{k}")}')
        self.w('aft/new', new)
        for k in range(16):
            self.w(f'aft/set_{k}', [f'kill @e[type=minecraft:marker,tag=rlk_az_aft{k}]',
                                    f'summon minecraft:marker ~ ~ ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_az_aft","rlk_az_aft{k}"]}}',
                                    f'execute rotated ~ ~ as @e[type=minecraft:marker,tag=rlk_az_aft{k},limit=1] run tp @s ~ ~ ~ ~ ~',
                                    f'scoreboard players operation #azAft{k} mb = #azAftF mb',
                                    f'scoreboard players operation #azAftT{k} mb = #azClk mb',
                                    f'scoreboard players operation #azAftT{k} mb += #azAftD mb',
                                    'scoreboard players add #azAftN mb 1'])
        tick = ['# @s = body: due timers run as the body at their marker, rotated as it.']
        for k in range(16):
            tick.append(f'execute if score #azAft{k} mb matches 1.. if score #azClk mb >= #azAftT{k} mb run {F(f"aft/run_{k}")}')
        self.w('aft/tick', tick)
        for k in range(16):
            self.w(f'aft/run_{k}', [f'scoreboard players operation #azAftX mb = #azAft{k} mb', sc(f'#azAft{k}', 0),
                                    'scoreboard players remove #azAftN mb 1',
                                    f'execute at @e[type=minecraft:marker,tag=rlk_az_aft{k},limit=1] rotated as '
                                    f'@e[type=minecraft:marker,tag=rlk_az_aft{k},limit=1] run {F("aft/fn")}',
                                    f'kill @e[type=minecraft:marker,tag=rlk_az_aft{k}]'])
        fn = ['# GENERATED: the after() targets written in this run, by id.']
        fn += [f'execute if score #azAftX mb matches {i} run return run {F(rel)}' for rel, i in sorted(A.AFTER.items(), key=lambda kv: kv[1])]
        self.w('aft/fn', fn)
        self.w('aft/clear', ['# Every timer goes (death, cleanup, test stop, reload).', 'kill @e[type=minecraft:marker,tag=rlk_az_aft]',
                             sc('#azAftN', 0)] + [sc(f'#azAft{k}', 0) for k in range(16)])

    # -----------------------------------------------------------------------------------------
    def addons(self):
        F, g = self.F, self.g
        self.w('x/ctx', ['# The addon context marker rlk_az_ctx here, rotated as the context (s2.md 10.1).',
                         'kill @e[type=minecraft:marker,tag=rlk_az_ctx]',
                         'summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_az_ctx"]}',
                         'execute rotated ~ 0 as @e[type=minecraft:marker,tag=rlk_az_ctx,limit=1] run tp @s ~ ~ ~ ~ 0'])
        for point, d in A.ADDON_POINTS.items():
            pk = d['key']
            lines = [f'# Addon dispatcher {point} (host P{d["host"]} {d["clip"]} {d["event"]} E {d["E"]}, called at E - 12 = {d["call"]};',
                     f'# context: {d["ctx"]}). Lines only for the bodies written in this run (s2.md 10.1).']
            for el in d['bodies']:
                if el in A.LEG_BODY:
                    rel = f'xl/{pk}/{el}'
                    if g.has(rel):
                        lines.append(f'execute if score #azPh mb matches 2.. if score #azLeg mb matches {A.LEG_BODY[el]} run return run {F(rel)}')
                else:
                    rel = f'xt/{pk}/{el}'
                    if g.has(rel):
                        lines.append(f'execute if score #azPh mb matches 3 if score #azTail mb matches {A.TAIL_BODY[el]} run {F(rel)}')
            self.w(f'x/{pk}', lines)

    # -----------------------------------------------------------------------------------------
    def push(self):
        F, g = self.F, self.g
        self.w('push/req', [
            '# @s = body: the body push request (N12, cm.md 13.5; #mbPushOn is a per-tick request): only in the proxy state',
            '# normal, the anchor moved <= 0.15 b/t and turned <= 6 deg/t since the last tick, no 42 mask round with safe',
            '# markers, no pattern request #azNoPush (charge run, leap, whip pivot, emerge before out), not in a leap.',
            sc('#azMov', 0),
            'execute store result score #azX mb run data get entity @s Pos[0] 1000',
            'execute store result score #azZ mb run data get entity @s Pos[2] 1000',
            'execute store result score #azY mb run data get entity @s Rotation[0] 100',
            'scoreboard players operation #azDX mb = #azX mb', 'scoreboard players operation #azDX mb -= #azLX mb',
            'scoreboard players operation #azDZ mb = #azZ mb', 'scoreboard players operation #azDZ mb -= #azLZ mb',
            'scoreboard players operation #azDY mb = #azY mb', 'scoreboard players operation #azDY mb -= #azLY mb',
            'execute unless score #azDX mb matches -150..150 run scoreboard players set #azMov mb 1',
            'execute unless score #azDZ mb matches -150..150 run scoreboard players set #azMov mb 1',
            'execute unless score #azDY mb matches -600..600 run scoreboard players set #azMov mb 1',
            'scoreboard players operation #azLX mb = #azX mb', 'scoreboard players operation #azLZ mb = #azZ mb',
            'scoreboard players operation #azLY mb = #azY mb',
            f'execute unless score #azPx mb matches {PX_ID["normal"]} run return 0',
            'execute if score #azMov mb matches 1 run return 0',
            'execute if score #azNoPush mb matches 1 run return 0',
            'execute if score #azLeap mb matches 1 run return 0',
            'execute if entity @e[type=minecraft:marker,tag=rlk_mb_hzsafe,limit=1] run return 0',
            'scoreboard players set #mbPushOn mb 1'])

    # -----------------------------------------------------------------------------------------
    def phases_looks(self):
        F, g = self.F, self.g
        self.w('svc/phase_1', ['# Phase 1 (Geo).', sc('#azPh', 1), sc('#azE', 5), sc('#azET', 5), F('svc/floor_f1'), sc('#azHudQ', 1)])
        p2 = ['# Phase 2 (absorb 1 at t94): the leg element on the ground hazards (#azE), floor F2, music "2", the brand banner',
              '# (once per fight).', sc('#azPh', 2), 'scoreboard players operation #azE mb = #azLeg mb', sc('#azET', 5),
              F('svc/floor_f2'), g.music(2), F('svc/banner_brand'), sc('#azHudQ', 1)]
        p3 = ['# Phase 3 (absorb 2 burst t42): + the tail element (#azET), #mbFloor 1 until the B3 surfacing.', sc('#azPh', 3),
              'scoreboard players operation #azE mb = #azLeg mb', 'scoreboard players operation #azET mb = #azTail mb',
              F('svc/floor_1'), sc('#azHudQ', 1)]
        if RES_BY_PHASE:
            p2 += [f'execute as {BODY} if score #azLeg mb matches {e} run scoreboard players set @s mbRes{e} 30' for e in (1, 2)]
            p3 += [f'execute as {BODY} if score #azTail mb matches {e} run scoreboard players set @s mbRes{e} 30' for e in (3, 4)]
        self.w('svc/phase_2', p2)
        self.w('svc/phase_3', p3)
        self.w('svc/floor_f1', ['# #mbFloor = ceil(mhpM x 2 / 3) (the end of phase 1).',
                                f'execute as {BODY} run scoreboard players operation #mbFloor mb = @s mhpM',
                                'scoreboard players operation #mbFloor mb *= #c2 mb', 'scoreboard players add #mbFloor mb 2',
                                sc('#azX', 3), 'scoreboard players operation #mbFloor mb /= #azX mb'])
        self.w('svc/floor_f2', ['# #mbFloor = ceil(mhpM / 3) (the end of phase 2).',
                                f'execute as {BODY} run scoreboard players operation #mbFloor mb = @s mhpM',
                                'scoreboard players add #mbFloor mb 2', sc('#azX', 3), 'scoreboard players operation #mbFloor mb /= #azX mb'])
        self.w('svc/floor_1', ['# The boss stays alive through the B3 (#mbFloor 1).', sc('#mbFloor', 1)])
        self.w('svc/floor_0', ['# No floor any more (the B3 surfacing).', sc('#mbFloor', 0)])
        for ph in (1, 2):
            self.w(f'svc/music_{ph}', [f'# Music phase "{ph}" (registry music; cm.md 10).', A.fw('music/set', f'{{ph:{ph}}}')])
        self.w('svc/cine_on', ['# Cine (cm.md 13.7): no boss hit lands on the player; the orbs ride high.', A.fw('cine/start'), sc('#azOrbHigh', 1)])
        self.w('svc/cine_off', [A.fw('cine/end'), 'execute unless score #azTr mb matches 1.. run scoreboard players set #azOrbHigh mb 0'])
        ban = {'tr': ('banner_tr', None), 'ab': ('banner_ab', 'leg'), 'ab2': ('banner_ab2', 'tail'), 'brand': ('banner_brand', 'leg')}
        for kind, (hud, which) in ban.items():
            lines = [f'# Kit banner {hud} (fx.md 7) with the element of the step.']
            if kind == 'tr':
                lines += [f'function {NS}tr/msg']
            else:
                els = A.LEG_ELS if which == 'leg' else A.TAIL_ELS
                sc_ = '#azLeg' if which == 'leg' else '#azTail'
                if kind == 'brand':
                    lines += ['execute if score #azBrBan mb matches 1 run return 0', sc('#azBrBan', 1)]
                lines += [f'execute if score {sc_} mb matches {e} run {K.hude(hud, e)}' for e in els]
            self.w(f'svc/banner_{kind}', lines)
        self.w('svc/banner_end', [K.hud('banner_end')])
        for name, i in PX_ID.items():
            self.w(f'px/{name}', [f'# The proxy state {name} (cm.md 9.4: px/state also calls the rig visibility it names).',
                                  sc('#azPx', i), A.fw('px/state', f'{{set:"{name}"}}')])
        self.w('px/restate', ['# /reload: the proxy state again from #azPx.']
               + [f'execute if score #azPx mb matches {i} run return run {F(f"px/{name}")}' for name, i in PX_ID.items()])
        # looks
        self.w('look/legs', ['# The rolled leg element\'s legs look (#azLeg 1 Pyro / 2 Hydro).']
               + [f'execute if score #azLeg mb matches {e} run return run function {A.rig_fn("look/legs/" + A.EL_KEY[e])}' for e in A.LEG_ELS])
        self.w('look/tail', ['# The rolled tail element\'s tail look (#azTail 3 Electro / 4 Cryo).']
               + [f'execute if score #azTail mb matches {e} run return run function {A.rig_fn("look/tail/" + A.EL_KEY[e])}' for e in A.TAIL_ELS])
        self.w('look/geo', ['# Both channels Geo (the fight start; death).', f'function {A.rig_fn("look/legs/geo")}',
                            f'function {A.rig_fn("look/tail/geo")}'])
        self.w('look/apply', ['# The looks of #azPh (reload, tests): phase >= 2 legs, phase 3 the tail too.', F('look/geo'),
                              f'execute if score #azPh mb matches 2..3 run {F("look/legs")}',
                              f'execute if score #azPh mb matches 3 run {F("look/tail")}'])

    # -----------------------------------------------------------------------------------------
    def arena(self):
        F, g = self.F, self.g
        th = A.THEME
        aid = A.ARENA.get('aid', 'az_cavern')
        stand = {'water_sheet': 'minecraft:light_blue_stained_glass_pane', 'arena_crystal': 'minecraft:amethyst_cluster',
                 'glyph': 'minecraft:paper'}
        props = ['# N17 / theme.md 4.1: the per-fight display props of the theme (water sheets, crystals, the two arrival glyphs),',
                 f'# tags rlk_mb_aux rlk_mb_arena_prop rlk_mb_ar_{aid} rlk_mb_az_ap rlk_mb_az_ap_<group> (never rlk_room); made at',
                 '# the fight start and on /reload, guarded by "none alive"; the element look follows (arena/look_now).',
                 'execute if entity @e[type=minecraft:item_display,tag=rlk_mb_az_ap,limit=1] run return 0']
        for pr in th['props']:
            x, y, z = pr['pos']
            sc_ = pr.get('scale', 1.0)
            sx, sy, sz = (sc_, sc_, sc_) if not isinstance(sc_, (list, tuple)) else sc_
            rot = '[0.7071f,0f,0f,0.7071f]' if pr['kind'] == 'water_sheet' else '[0f,0f,0f,1f]'
            props.append(f'execute in minecraft:overworld run summon minecraft:item_display {L.num(x, 3)} {L.num(y, 3)} {L.num(z, 3)} '
                         f'{{Tags:["rlk_mb_aux","rlk_mb_arena_prop","rlk_mb_ar_{aid}","rlk_mb_az_ap","rlk_mb_az_ap_{pr["group"]}"],'
                         f'Rotation:[{L.num(float(pr.get("yaw", 0.0)))}f,{L.num(float(pr.get("pitch", 0.0)))}f],billboard:"fixed",'
                         'brightness:{block:13,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:'
                         f'{rot},right_rotation:[0f,0f,0f,1f],scale:[{L.num(float(sx))}f,{L.num(float(sy))}f,{L.num(float(sz))}f]}},'
                         f'item:{{id:"{stand.get(pr["kind"], "minecraft:paper")}",count:1}}}}')
        props += [F('arena/glyphs')]
        self.w('arena/props', props)
        gl = ['# The two arrival glyphs: upper = the tail element, lower = the leg element (kit glyph props).']
        for e in A.TAIL_ELS:
            gl.append(f'execute if score #azTail mb matches {e} as @e[type=minecraft:item_display,tag=rlk_mb_az_ap_glyph_upper] run {K.prope("glyph", e)}')
        for e in A.LEG_ELS:
            gl.append(f'execute if score #azLeg mb matches {e} as @e[type=minecraft:item_display,tag=rlk_mb_az_ap_glyph_lower] run {K.prope("glyph", e)}')
        self.w('arena/glyphs', gl)
        # looks: geo / leg / tail with the recolour wave (20 t outward from the boss)
        for k in ('geo', 'leg', 'tail'):
            lines = [f'# N17 / plan 2.6: the arena props to the {k} element look as a wave from the boss outward over 20 t.']
            if k == 'geo':
                lines.append(sc('#azArEl', 5))
            else:
                lines.append(f'scoreboard players operation #azArEl mb = #az{"Leg" if k == "leg" else "Tail"} mb')
            lines += ['scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap] azT 20']
            for band, t in ((7, 5), (14, 10), (21, 15)):
                lines.append(f'execute at {BODY} run scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,distance=..{band}] azT {t}')
            lines += [sc('#azArT', 21)]
            if k != 'geo':
                lines += [f'execute if score #azArEl mb matches {e} at {BODY} run {K.fxe("recolour", e, r=280, t=20)}' for e in (1, 2, 3, 4)]
            self.w(f'arena/look_{k}', lines)
        apply = ['# @s = a prop: the look of #azArEl (the kit prop families water_sheet / arena_crystal 1..5).']
        tint = {1: 'minecraft:orange_stained_glass_pane', 2: 'minecraft:light_blue_stained_glass_pane',
                3: 'minecraft:purple_stained_glass_pane', 4: 'minecraft:white_stained_glass_pane', 5: 'minecraft:yellow_stained_glass_pane'}
        for e in (1, 2, 3, 4, 5):
            apply.append(f'execute if score #azArEl mb matches {e} if entity @s[tag=rlk_mb_az_ap_water] run {K.prope("water_sheet", e)}')
            apply.append(f'execute if score #azArEl mb matches {e} if entity @s[tag=rlk_mb_az_ap_crystal] run {K.prope("arena_crystal", e)}')
            if not A.KIT:
                apply.append(f'execute if score #azArEl mb matches {e} if entity @s[tag=rlk_mb_az_ap_water] run data modify entity @s item '
                             f'set value {{id:"{tint[e]}",count:1}}')
        self.w('arena/look_one', apply)
        self.w('arena/look_now', ['# Every prop to #azArEl at once (spawn, reload, tests).',
                                  f'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_ap] run {F("arena/look_one")}', sc('#azArT', 0)])
        self.w('arena/tick', [
            '# @s = body, every 4 t: the recolour wave (props whose delay ran out take the look) and the ambience.',
            f'execute if score #azArT mb matches 1.. run {F("arena/wave")}',
            'execute store result score #azX mb run random value 0..4',
            f'execute if score #azX mb matches 0 run {F("arena/ambient")}'])
        self.w('arena/wave', ['scoreboard players remove #azArT mb 4',
                              'scoreboard players remove @e[type=minecraft:item_display,tag=rlk_mb_az_ap,scores={azT=1..}] azT 4',
                              f'execute as @e[type=minecraft:item_display,tag=rlk_mb_az_ap,scores={{azT=..0}}] run {F("arena/look_one")}',
                              'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_az_ap,scores={azT=..0}] azT -1000'])
        amb = ['# Ambient particles of the arena element (plan 2.6): gold motes (Geo), drips (Hydro), embers (Pyro), snow',
               '# (Cryo), sparks (Electro), at a random player-near spot.']
        parts = {5: 'dust{color:[0.95,0.75,0.25],scale:1.2}', 2: 'dripping_water', 1: 'lava', 4: 'snowflake', 3: 'electric_spark'}
        for e, pt in parts.items():
            amb.append(f'execute if score #azArEl mb matches {e} at {PLAYER} run particle minecraft:{pt} ~ ~6 ~ 8 3 8 0 4 force @a[tag=player]')
        amb.append(f'execute if score #azPh mb matches 3 at {PLAYER} if score #azLeg mb matches 2 run particle minecraft:dripping_water ~ ~6 ~ 8 3 8 0 2 force @a[tag=player]')
        amb.append(f'execute if score #azPh mb matches 3 at {PLAYER} if score #azLeg mb matches 1 run particle minecraft:lava ~ ~6 ~ 8 3 8 0 1 force @a[tag=player]')
        self.w('arena/ambient', amb)

    # -----------------------------------------------------------------------------------------
    def hud(self):
        F, g = self.F, self.g
        ex = ['# The name-line badges (plan 4.11): ◈<leg> ◈<tail> (dim #707070 until absorbed, then the element colour) and',
              '# ◈낙인 while branded. The framework draws "Lv.N 야타용왕" itself.',
              'data modify storage rlk:mboss extra set value []']
        for e in A.LEG_ELS:
            ex.append(f'execute if score #azLeg mb matches {e} if score #azPh mb matches ..1 run data modify storage rlk:mboss extra append value {K.badge(e, False)}')
            ex.append(f'execute if score #azLeg mb matches {e} if score #azPh mb matches 2.. run data modify storage rlk:mboss extra append value {K.badge(e, True)}')
        for e in A.TAIL_ELS:
            ex.append(f'execute if score #azTail mb matches {e} unless score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {K.badge(e, False)}')
            ex.append(f'execute if score #azTail mb matches {e} if score #azPh mb matches 3 run data modify storage rlk:mboss extra append value {K.badge(e, True)}')
        ex.append(f'execute if entity @a[tag=player,scores={{azBrT=1..}}] run data modify storage rlk:mboss extra append value {K.badge(9, True)}')
        self.w('hud/extra', ex)
        sub = ['# The sub-line (plan 4.11), first match: intro name, "마지막 일격!", the jump cue, B3 "꼬리만 공격할 수 있습니다",',
               '# the transition message, a hint, the running pattern; then the brand part and any pattern-provided part',
               '# (storage az.subx, e.g. 42\'s "안전 지대 N칸").',
               'data modify storage rlk:mboss sub set value []',
               f'execute if score #mbSt mb matches 0 run return run data modify storage rlk:mboss sub set value [{txt(A.BOSS["sub"], "#E8E2D0", True)}]',
               f'function {NS}hud/sub_main',
               F('brand/hud'),
               'execute if data storage rlk:mboss az.hud.br run data modify storage rlk:mboss sub append from storage rlk:mboss az.hud.br[]',
               'execute if data storage rlk:mboss az.subx run data modify storage rlk:mboss sub append from storage rlk:mboss az.subx[]']
        self.w('hud/sub', sub)
        main = [f'execute if score #azLastHit mb matches 1 run return run data modify storage rlk:mboss sub append value {txt(SUB_LAST, "#FFD27A", True)}',
                f'execute if score #azCue mb matches 1.. run return run data modify storage rlk:mboss sub append value {txt(SUB_JUMP, "#FFFFFF", True)}']
        for e in A.TAIL_ELS:
            main.append(f'execute if score #azBur mb matches 1 if score #azTail mb matches {e} run return run data modify storage rlk:mboss sub '
                        f'append value {txt(SUB_B3, A.EL_COL[e], True)}')
        for e in A.LEG_ELS:
            main.append(f'execute if score #azTr mb matches 1.. if score #azTrN mb matches 1 if score #azLeg mb matches {e} run return run data '
                        f'modify storage rlk:mboss sub append value {txt(MSG.format(el=A.EL_NAME[e]), A.EL_COL[e], True)}')
        for e in A.TAIL_ELS:
            main.append(f'execute if score #azTr mb matches 1.. if score #azTrN mb matches 2 if score #azTail mb matches {e} run return run data '
                        f'modify storage rlk:mboss sub append value {txt(MSG.format(el=A.EL_NAME[e]), A.EL_COL[e], True)}')
        for hid, text in AI.HINTS.items():
            main.append(f'execute if score #azHint mb matches {hid} if score #azHintT mb > #azClk mb run return run data modify storage '
                        f'rlk:mboss sub append value {txt(text, "#FFE3A8")}')
        for p in self.pats:
            if p.kind in ('normal', 'bg') or p.id == 30:
                main.append(f'execute if score #azPat mb matches {p.id} run return run data modify storage rlk:mboss sub set value '
                            f'[{{text:"패턴  ",color:"#A8A8A8"}},{txt(p.label, "#F2E2B0")}]')
        self.w('hud/sub_main', main)
        self.w('hud/refresh', ['# Both text lines from the current state.', F('hud/extra'), F('hud/sub'), sc('#azHudQ', 0)])
        self.w('hud/tick', ['# @s = body: the cue clock, the hint expiry, the floor popups, the lines every 4 t or on request.',
                            'execute if score #azCue mb matches 1.. run scoreboard players remove #azCue mb 1',
                            'execute if score #azCue mb matches 0 if score #azHint mb matches 0 run scoreboard players set #azCue mb -1',
                            'execute if score #azHint mb matches 1.. if score #azHintT mb <= #azClk mb run scoreboard players set #azHudQ mb 1',
                            'execute if score #azHint mb matches 1.. if score #azHintT mb <= #azClk mb run scoreboard players set #azHint mb 0',
                            'scoreboard players remove @e[type=minecraft:text_display,tag=rlk_mb_az_pop] azT 1',
                            'kill @e[type=minecraft:text_display,tag=rlk_mb_az_pop,scores={azT=..0}]',
                            f'execute if score #azHudQ mb matches 1 run return run {F("hud/refresh")}',
                            f'execute if score #azQ4 mb matches 0 run {F("hud/refresh")}'])
        bar = ['# @s = body: the under-bar (plan 4.11): fight = mhpC - #mbFloor of the phase pool (Geo -> leg -> tail colour);',
               '# transition = the step progress (gold); B3 tail window = time left (the tail colour).',
               'execute if score #mbSt mb matches 0 run return 0',
               f'execute if score #azBur mb matches 1 run return run {F("hud/bar_b3")}',
               f'execute if score #azTr mb matches 2.. run return run {F("hud/bar_tr")}',
               F('hud/bar_hp')]
        self.w('hud/bar', bar)
        self.w('hud/bar_b3', [f'scoreboard players set #buSub bu {A.B3_TAILSINK}', 'scoreboard players operation #buSub bu -= #azB3T mb',
                              f'scoreboard players set #buSubMax bu {A.B3_TAILSINK - A.B3_TAILUP}',
                              'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0']
              + [f'execute if score #azTail mb matches {e} run scoreboard players set #buSubCol bu {L.ELEM_TO_BU[e]}' for e in A.TAIL_ELS])
        self.w('hud/bar_tr', ['scoreboard players operation #buSub bu = #azPT mb', 'scoreboard players operation #buSubMax bu = #azPLen mb',
                              'execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1',
                              'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0', bu('#buSubCol', 8)])
        hp = ['# The phase pool: phase 1 mhpM .. F1, phase 2 F1 .. F2, phase 3 F2 .. 0 (the floors recomputed here).',
              'scoreboard players operation #buSub bu = @s mhpC', 'scoreboard players operation #buSub bu -= #mbFloor mb',
              'scoreboard players operation #azX mb = @s mhpM', 'scoreboard players operation #azX mb *= #c2 mb',
              'scoreboard players add #azX mb 2', sc('#azY', 3), 'scoreboard players operation #azX mb /= #azY mb',
              'scoreboard players operation #azZ mb = @s mhpM', 'scoreboard players add #azZ mb 2',
              'scoreboard players operation #azZ mb /= #azY mb',
              'execute if score #azPh mb matches ..1 run scoreboard players operation #buSubMax bu = @s mhpM',
              'execute if score #azPh mb matches ..1 run scoreboard players operation #buSubMax bu -= #azX mb',
              'execute if score #azPh mb matches 2 run scoreboard players operation #buSubMax bu = #azX mb',
              'execute if score #azPh mb matches 2 run scoreboard players operation #buSubMax bu -= #azZ mb',
              'execute if score #azPh mb matches 3.. run scoreboard players operation #buSubMax bu = #azZ mb',
              'execute if score #azPh mb matches 3.. run scoreboard players operation #buSubMax bu -= #mbFloor mb',
              'execute if score #buSubMax bu matches ..0 run scoreboard players set #buSubMax bu 1',
              'execute if score #buSub bu matches ..-1 run scoreboard players set #buSub bu 0',
              bu('#buSubCol', L.ELEM_TO_BU[5])]
        hp += [f'execute if score #azPh mb matches 2 if score #azLeg mb matches {e} run scoreboard players set #buSubCol bu {L.ELEM_TO_BU[e]}' for e in A.LEG_ELS]
        hp += [f'execute if score #azPh mb matches 3.. if score #azTail mb matches {e} run scoreboard players set #buSubCol bu {L.ELEM_TO_BU[e]}' for e in A.TAIL_ELS]
        self.w('hud/bar_hp', hp)

    # -----------------------------------------------------------------------------------------
    def death(self):
        F, g = self.F, self.g
        self.w('death_start', [
            '# Hook death_start (@s = body; the framework cleared its libraries, hid the bars, set the proxies dead and stopped',
            '# the music): every slot, the B3 special, the fields, orbs, timers, shards and the brand go; the arena fades back to',
            '# Geo; the death clip and seq/death.',
            F('p/cancel'), F('cast/cancel'), F('bg/cancel_l'), F('bg/cancel_t'), F('b3/special_cancel'),
            F('fld/clear'), 'kill @e[tag=rlk_mb_az_orb]', 'kill @e[tag=rlk_mb_az_orbc]', F('aft/clear'), F('brand/clear_all'),
            'kill @e[tag=rlk_mb_az_pat]', 'kill @e[tag=rlk_mb_az_seal]',
            f'function {K.FN}tele/clear' if A.KIT else K._c('tele/clear'),
            f'function {K.FN}tele/field_clear' if A.KIT else K._c('tele/field_clear'), K.hud('clear'),
            g.cine(False), sc('#mbFloor', 0), sc('#azTr', 0), sc('#azBur', 0), sc('#azPh', 9), sc('#azLastHit', 0),
            g.arena_look('geo'), g.glow(False),
            g.play('death'), F('seq/death/start')])
        self.w('death_tick', [
            '# Hook death_tick (@s = body, #mbT 1.. until cur.death): the clip (rig tick), seq/death beats, the arena wave.',
            *A.rig_tick_lines(),
            F('seq/death/tick'),
            'scoreboard players operation #azM mb = #mbT mb', 'scoreboard players operation #azM mb %= #azK4 mb',
            f'execute if score #azM mb matches 0 if score #azArT mb matches 1.. run {F("arena/wave")}'])

    # -----------------------------------------------------------------------------------------
    def tests(self):
        F, g = self.F, self.g
        HELP = [('1-9', 'P1-P9'), ('10', 'P5b'), ('20', '산사태'), ('21', '흡수 1'), ('22', '흡수 2'), ('23', 'B3'), ('24', '처치'),
                ('25', 'B3 꼬리 하강부터'), ('26', '등장'), ('31/32', '물 구체 / 운석'), ('33', '불 장판'), ('41/42', '서리 / 벼락 (B3)'),
                ('43-46', '꼬리 패턴'), ('60', '2페이즈'), ('61', '3페이즈(꼬리)'), ('62', '3페이즈'), ('70', '낙인'), ('71', '낙인 해제'),
                ('72', '결정'), ('80', '체력 = 바닥 + 1'), ('90-93', '원소 조합 고정'), ('99', '대기'),
                ('시작', '/function rlk:mboss/test/chapter {id:\\"azhdaha\\"}')]
        tx = f'[{{text:"[야타용왕 테스트] ",color:"{GOLD}",bold:true}}' + ''.join(
            f',{{text:"{k}",color:"yellow"}},{{text:" {v}  ",color:"gray"}}' for k, v in HELP) + ']'
        self.w('test/help', ['tellraw @a[tag=player] ' + tx])
        self.w('test/cut', [
            '# @s = body: stop whatever runs (hazards, slots, the B3 special, fields, orbs, timers, a transition) and re-derive a',
            '# clean state for the current phase (floor, proxies, rig, cine off).',
            'function rlk:mboss/lib_clear', F('p/cancel'), F('cast/cancel'), F('bg/cancel_l'), F('bg/cancel_t'),
            F('b3/special_cancel'), F('fld/clear'), 'kill @e[tag=rlk_mb_az_orb]', 'kill @e[tag=rlk_mb_az_orbc]', F('aft/clear'),
            f'function {K.FN}tele/clear' if A.KIT else K._c('tele/clear'),
            g.cine(False), g.glow(False), sc('#azTr', 0), sc('#azTrN', 0), sc('#azBur', 0), sc('#azOrbHigh', 0), sc('#azLastHit', 0),
            sc('#mbNoLeash', 0), sc('#azCastFirst', 0),
            f'execute if score #azPh mb matches 1 run {F("svc/floor_f1")}', f'execute if score #azPh mb matches 2 run {F("svc/floor_f2")}',
            f'execute if score #azPh mb matches 3 run {F("svc/floor_0")}',
            g.px('normal'), g.play('idle'), sc('#azCool', 10), sc('#azHudQ', 1)])
        run = ['# @s = body, #azTst = the requested test id (plan 1.7).', 'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
               f'execute if score #mbSt mb matches 1 if score #azPh mb matches 0 run {F("intro/done")}']
        req_ids = sorted({p.id for p in self.pats if p.kind in ('normal', 'cast', 'bg')} | {20, 21, 22})
        for pid in req_ids:
            run.append(f'execute if score #azTst mb matches {pid} run return run {F(f"test/req_{pid}")}')
        for pid in req_ids:
            pre = []
            if pid == 10:
                pre = ['execute if score #azPaw mb matches 3..4 run scoreboard players set #azPaw mb 1']
            if pid in (31, 32):
                pre = [f'scoreboard players set #azCastReq mb {pid}']
            self.w(f'test/req_{pid}', [F('test/cut')] + pre + [sc('#azReq', pid), sc('#azCool', 1)])
        run += [f'execute if score #azTst mb matches 23 run return run {F("test/b3")}',
                f'execute if score #azTst mb matches 24 run return run {F("test/kill")}',
                f'execute if score #azTst mb matches 25 run return run {F("test/b3_sink")}',
                f'execute if score #azTst mb matches 26 run return run {F("test/intro")}',
                f'execute if score #azTst mb matches 33 run return run {F("test/fire")}',
                f'execute if score #azTst mb matches 41 run return run {F("test/b3_41")}',
                f'execute if score #azTst mb matches 42 run return run {F("test/b3_42")}',
                f'execute if score #azTst mb matches 60 run return run {F("test/p2")}',
                f'execute if score #azTst mb matches 61 run return run {F("test/p3_tail")}',
                f'execute if score #azTst mb matches 62 run return run {F("test/p3")}',
                f'execute if score #azTst mb matches 70 run return run {F("test/brand")}',
                f'execute if score #azTst mb matches 71 run return run {F("brand/clear_all")}',
                f'execute if score #azTst mb matches 72 run return run {F("test/shard")}',
                f'execute if score #azTst mb matches 80 run return run {F("test/floor1")}']
        for i in A.PAIRS:
            run.append(f'execute if score #azTst mb matches {90 + i} run return run {F(f"test/pair_{i}")}')
        run += [f'execute if score #azTst mb matches 99 run return run {F("test/cut")}', F('test/help')]
        self.w('test/run', run)
        self.w('test/p2', ['# Phase 2 at once (no sequence): the legs look, the arena, floor F2, music 2.', F('test/cut'),
                           g.phase(2), g.look_legs(), g.arena_look('leg'), F('svc/floor_f2')])
        self.w('test/p3', ['# Phase 3 surfaced at once: both looks, the arena, floor 0.', F('test/cut'), g.phase(3), g.look_legs(),
                           g.look_tail(), g.arena_look('tail'), F('svc/floor_0')])
        self.w('test/p3_tail', ['# Phase 3 at tail-up (the B3 frame at B3_TAILUP, the special starts).', F('test/p3'), F('svc/floor_1'),
                                sc('#azReq', 23), sc('#azReqT', A.B3_TAILUP), sc('#azCool', 1)])
        self.w('test/b3', ['# The B3 with the pair\'s tail special (phase 3 first).', F('test/p3'), F('svc/floor_1'), sc('#azReq', 23),
                           sc('#azCool', 1)])
        self.w('test/b3_sink', ['# The B3 from the tail sink (the surfacing).', F('test/p3'), F('svc/floor_1'), sc('#azReq', 23),
                                sc('#azReqT', A.B3_TAILSINK), sc('#azCool', 1)])
        for pid, tail in ((41, 4), (42, 3)):
            self.w(f'test/b3_{pid}', [f'# {pid} inside a forced B3: the tail element {A.EL_KEY[tail]} (RES, looks follow), tail-up.',
                                      sc('#azTail', tail), F('test/pair_sync'), F('test/p3_tail')])
        self.w('test/pair_sync', ['# The pair changed: cprep, the mirror, RES, looks of the phase, badges.',
                                  'execute store result storage rlk:mboss cprep.azhdaha.pair.leg int 1 run scoreboard players get #azLeg mb',
                                  'execute store result storage rlk:mboss cprep.azhdaha.pair.tail int 1 run scoreboard players get #azTail mb',
                                  'data modify storage rlk:mboss az.pair set from storage rlk:mboss cprep.azhdaha.pair',
                                  f'execute as {BODY} run {F("res/reset")}', f'execute as {BODY} run {F("res/apply")}',
                                  F('look/apply'), f'execute if score #azPh mb matches 2.. run {F("arena/look_leg")}',
                                  f'execute if score #azPh mb matches 3 run {F("arena/look_tail")}', F('arena/glyphs'),
                                  'scoreboard players operation #azE mb = #azLeg mb', 'execute if score #azPh mb matches ..1 run scoreboard players set #azE mb 5',
                                  'scoreboard players operation #azET mb = #azTail mb', 'execute unless score #azPh mb matches 3 run scoreboard players set #azET mb 5',
                                  sc('#azHudQ', 1)])
        rr = A.BOSS.get('res', {})
        self.w('res/reset', ['# @s = body: the rolled four back to the registry default before a pair change.']
               + [f'scoreboard players set @s mbRes{k} {int(rr.get(str(k), rr.get("*", 0)))}' for k in (1, 2, 3, 4)])
        for i, (leg, tail) in A.PAIRS.items():
            self.w(f'test/pair_{i}', [f'# Force pair {i}: legs {A.EL_KEY[leg]}, tail {A.EL_KEY[tail]} (recolours a live rig, badges, RES).',
                                      sc('#azLeg', leg), sc('#azTail', tail),
                                      f'data modify storage rlk:mboss cprep.azhdaha.pair set value {{leg:{leg},tail:{tail},i:{i}}}',
                                      F('test/pair_sync')])
        self.w('test/kill', ['# 24: the death through a lethal true hit (bypasses the floor) -> the chapter clear.',
                             'execute if score #mbSt mb matches 0 run function rlk:mboss/intro_end',
                             'scoreboard players operation #mbTrue mb = @s mhpC', sc('#mbTrueEl', 5), 'function rlk:mboss/true_hit'])
        self.w('test/intro', ['# 26: the intro again (untargetable, the seal props, the clip).', F('test/cut'),
                              sc('#mbSt', 0), sc('#mbT', 0), 'tag @s add rlk_mb_inv', F('seq/intro/setup'), g.play('intro'),
                              g.px('inv'), sc('#azPh', 0), sc('#azHudQ', 1)])
        self.w('test/fire', ['# 33: one fire field (r 4.5 / 160 t, the fire rule\'s) under the player.',
                             f'execute at {PLAYER} positioned ~ {CY} ~ rotated ~ 0 run {F("test/fire_here")}'])
        self.w('test/fire_here', g.field('fire', 4.5, 160, A.DMG['fire'], el=1, rule=True))
        self.w('test/brand', ['# 70: a strike brand of the current absorbed element (phase 1: the leg element).',
                              'scoreboard players operation #azBrIn mb = #azLeg mb',
                              'execute if score #azPh mb matches 3 run scoreboard players operation #azBrIn mb = #azTail mb',
                              sc('#azBrStrike', 1), f'execute as @a[tag=player,limit=1] run {F("brand/apply")}'])
        self.w('test/shard', ['# 72: a shard now (cooldown ignored; the brand element, else the leg element).',
                              'kill @e[type=minecraft:item_display,tag=rlk_az_shard]', sc('#azShCd', 0),
                              'execute as @a[tag=player,limit=1] unless score @s azBrT matches 1.. run scoreboard players operation @s azBrE = #azLeg mb',
                              f'execute as @a[tag=player,limit=1] run {F("brand/shard_try")}'])
        self.w('test/floor1', ['# 80: HP to the current floor + 1 (the next hit queues the transition).',
                               'scoreboard players operation @s mhpC = #mbFloor mb', 'scoreboard players add @s mhpC 1'])

    # -----------------------------------------------------------------------------------------
    def stubs(self):
        """The LOCAL STUBS of missing framework functions (cmstub/, cm.md) and the kit stub files (kstub/)."""
        impl = {
            'cb/body': ['# @s = the arena marker context (at the spawn point, yaw = facing): mboss/body without miniboss, + rlk_mb_big',
                        '# and rlk_mb_noshield (cm.md 5.5).', 'function rlk:mboss/body',
                        'tag @e[type=minecraft:husk,tag=rlk_mb_body] remove miniboss',
                        'tag @e[type=minecraft:husk,tag=rlk_mb_body] add rlk_mb_big',
                        'tag @e[type=minecraft:husk,tag=rlk_mb_body] add rlk_mb_noshield'],
            'px/state': ['# Macro {set} (cm.md 9.3): the set is recorded; inv sets toggle rlk_mb_inv through rlk_mb_pxinv; the rig',
                         '# visibility of the set (stub manifest states.<set>.vis). No proxies exist without AZ-CM.',
                         '$data modify storage rlk:mboss px.set set value "$(set)"',
                         f'execute if data storage rlk:mboss px{{set:"inv"}} as {BODY} unless entity @s[tag=rlk_mb_inv] run tag @s add rlk_mb_pxinv',
                         f'execute if data storage rlk:mboss px{{set:"dead"}} as {BODY} unless entity @s[tag=rlk_mb_inv] run tag @s add rlk_mb_pxinv',
                         f'execute if data storage rlk:mboss px{{set:"inv"}} as {BODY} run tag @s add rlk_mb_inv',
                         f'execute if data storage rlk:mboss px{{set:"dead"}} as {BODY} run tag @s add rlk_mb_inv',
                         f'execute unless data storage rlk:mboss px{{set:"inv"}} unless data storage rlk:mboss px{{set:"dead"}} as {BODY}[tag=rlk_mb_pxinv] '
                         'run tag @s remove rlk_mb_inv'.replace(f'{BODY}[tag=rlk_mb_pxinv]', '@e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_pxinv,limit=1]'),
                         f'execute unless data storage rlk:mboss px{{set:"inv"}} unless data storage rlk:mboss px{{set:"dead"}} as {BODY} run tag @s remove rlk_mb_pxinv',
                         f'execute if data storage rlk:mboss px{{set:"normal"}} as {BODY} run function {A.rig_fn("state/normal")}',
                         f'execute if data storage rlk:mboss px{{set:"tail_only"}} as {BODY} run function {A.rig_fn("state/tail_only")}'],
            'px/spawn': ['# (cm.md 9.3) no proxies without AZ-CM.'],
            'mv/lockv': ['# Macro {lead} (cm.md 13.1): the lock rlk_mb_lock under the player (no velocity buffer without AZ-CM).',
                         '$scoreboard players set #azStub mb $(lead)', 'kill @e[type=minecraft:marker,tag=rlk_mb_lock]',
                         f'execute at {PLAYER} run summon minecraft:marker ~ {CY} ~ {{Tags:["rlk_room","rlk_mb_aux","rlk_mb_lock"]}}',
                         'scoreboard players set #mbVx mb 0', 'scoreboard players set #mbVz mb 0', 'scoreboard players set #mbV mb 0',
                         f'execute as @e[type=minecraft:marker,tag=rlk_mb_lock,limit=1] run function {NS}u/clamp_w'],
            'mv/local': ['# (cm.md 13.2) as the anchor: #mbLf / #mbLs (mb) of the player body in the anchor frame (f forward, s left).',
                         'execute store result score #azPx0 mb run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000',
                         'execute store result score #azPz0 mb run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000',
                         'execute store result score #azAx0 mb run data get entity @s Pos[0] 1000',
                         'execute store result score #azAz0 mb run data get entity @s Pos[2] 1000',
                         'scoreboard players operation #azPx0 mb -= #azAx0 mb', 'scoreboard players operation #azPz0 mb -= #azAz0 mb',
                         'execute at @s rotated as @s rotated ~ 0 positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_mb_azax"]}',
                         'execute store result score #azFx mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_azax,limit=1] Pos[0] 1000',
                         'execute store result score #azFz mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_azax,limit=1] Pos[2] 1000',
                         'kill @e[type=minecraft:marker,tag=rlk_mb_azax]',
                         'scoreboard players operation #azFx mb -= #azAx0 mb', 'scoreboard players operation #azFz mb -= #azAz0 mb',
                         '# f = (dx fx + dz fz) / 1000; s = (dx fz - dz fx) / 1000 (left = +x for yaw 0)',
                         'scoreboard players operation #mbLf mb = #azPx0 mb', 'scoreboard players operation #mbLf mb *= #azFx mb',
                         'scoreboard players operation #azT0 mb = #azPz0 mb', 'scoreboard players operation #azT0 mb *= #azFz mb',
                         'scoreboard players operation #mbLf mb += #azT0 mb', 'scoreboard players operation #mbLf mb /= #c1000 mb',
                         'scoreboard players operation #mbLs mb = #azPx0 mb', 'scoreboard players operation #mbLs mb *= #azFz mb',
                         'scoreboard players operation #azT0 mb = #azPz0 mb', 'scoreboard players operation #azT0 mb *= #azFx mb',
                         'scoreboard players operation #mbLs mb -= #azT0 mb', 'scoreboard players operation #mbLs mb /= #c1000 mb'],
            'pl_dot': ['# (cm.md 13.4) LOCAL STUB: #mbDotPct permille of maxHealth off curHealth, non-lethal, no shields.',
                       'execute as @a[tag=player,scores={dead=0},limit=1] run function ' + NS + 'cmstub/pl_dot1',
                       'scoreboard players set #mbDotLethal mb 0'],
            'push/ring': ['# Macro {r,to,kb} (cm.md 13.5): no push without AZ-CM.', '$scoreboard players set #azStub mb $(r)'],
            'cine/start': ['# (cm.md 13.7)', 'scoreboard players set #mbCine mb 1'],
            'cine/end': ['scoreboard players set #mbCine mb 0'],
            'music/set': ['# Macro {ph} (cm.md 10): the phase is recorded, nothing plays without AZ-CM.', '$scoreboard players set #mbMusPh mb $(ph)'],
            'music/stop': ['scoreboard players set #mbMusPh mb 0'],
            'hz/extend': ['# Macro {n} (cm.md 13.8) as a live hazard: the active window and the life grow together.',
                          '$scoreboard players add @s mbHzA $(n)', '$scoreboard players add @s mbHzL $(n)'],
            'hz/mask': ['# Macro {tell,dmg} (cm.md 13.6): no mask hazard without AZ-CM.', '$scoreboard players set #azStub mb $(tell)'],
            'floor': ['# (cm.md 7.2) as the body inside apply_mods: #mbFloorRaw, #mbFloorHit on <=, the clamp.',
                      'scoreboard players operation #mbFloorRaw mb = #dmg tmp',
                      'scoreboard players operation #azX mb = @s mhpC', 'scoreboard players operation #azX mb -= #dmg tmp',
                      'execute if score #azX mb <= #mbFloor mb run scoreboard players set #mbFloorHit mb 1',
                      'scoreboard players operation #azX mb = @s mhpC', 'scoreboard players operation #azX mb -= #mbFloor mb',
                      'execute if score #azX mb matches ..-1 run scoreboard players set #azX mb 0',
                      'execute if score #dmg tmp > #azX mb run scoreboard players operation #dmg tmp = #azX mb'],
        }
        for rel, sec in sorted(A.CMSTUBS.items()):
            if rel == 'res_pre':
                continue
            lines = impl.get(rel, ['# (no local equivalent)'])
            head = [f'# LOCAL STUB of rlk:mboss/{rel} (AZ-CM, cm.md {sec}) written by tools/mboss_azhdaha/core.py while the',
                    '# framework lacks it; the module calls the real function by itself once wip/az-cm provides it (api.fw).']
            self.w(f'cmstub/{rel.replace("/", "_")}', head + lines)
        if 'pl_dot' in A.CMSTUBS:
            self.w('cmstub/pl_dot1', ['scoreboard players operation #azX mb = @s maxHealth', 'scoreboard players operation #azX mb *= #mbDotPct mb',
                                      'scoreboard players operation #azX mb /= #c1000 mb', 'execute if score #azX mb matches ..0 run scoreboard players set #azX mb 1',
                                      'scoreboard players operation #mbDotDmg mb = #azX mb',
                                      'scoreboard players operation @s curHealth -= #azX mb',
                                      'execute if score @s curHealth matches ..0 run scoreboard players set @s curHealth 1'])
        if not A.KIT:
            for path, args in sorted(K.used.items()):
                a = ', '.join(f'{k}={v}' for k, v in args.items())
                self.w(f'kstub/{path}', [f'# LOCAL STUB of the kit call {K.FN}{path} (fx.md; S1-FX, wip/az-fx) — no-op until I1.',
                                         f'# first call: {a}' if a else '# (no args)'])
