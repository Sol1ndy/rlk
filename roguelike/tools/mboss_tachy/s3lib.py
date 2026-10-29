"""S3 helpers of the 타키 (Tachy) module generator (OWNER: S3; named in S:tk/requests/s3.md): score / call shorthands, the
kit-or-fallback visual and sound lines, hazard lines from api.HITS, and the pattern builder PB used by p_melee.py.

Importing has no side effects. Runtime conventions (contract §3.4): @s = the body, at it; #pt tk = the pattern clock
(0 in p/<key>/start, +1 before each p/<key>/tick); the shown clip tick == #pt (the core calls rig/tick after the pattern).
A hit of clip event e is a quiet hazard created at #pt e - 1 with tell 1, so it strikes on the game tick of #pt e; the
aim is the body yaw at creation (the patterns stop turning >= LOCK ticks before every hit). Hazards and pattern markers
carry rlk_tk_p + rlk_tk_p_<key>; cancel kills them (idempotent).
"""
from collections import defaultdict

from . import api

L, K = api.L, api.K
NS = api.NS
CY = api.CY
OBJ = api.OBJ
LOCK = 8                     # ticks before a hit when the body stops turning toward the player (aim locked)
TID = {v: k for k, v in api.TEST_IDS.items() if isinstance(v, str) and v in api.HITS}   # key -> test id = pattern id
TID.update({'mantle': 20})
BODY = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
PLAYER = '@e[tag=rlk_body,limit=1]'


def fn(rel):
    return f'function {NS}{rel}'


def sset(name, v):
    return f'scoreboard players set {name} {OBJ} {int(v)}'


def gate(cond, cmd):
    """`execute <cond> run <cmd>`, merged into cmd's own execute chain when it has one."""
    return f'execute {cond} {cmd[8:]}' if cmd.startswith('execute ') else f'execute {cond} run {cmd}'


def tag_p(key):
    return f'rlk_tk_p_{key}'


def clip_id(clip):
    return api.CLIP_ORDER.index(clip)


# ------------------------------------------------------------------------------------------------- sounds / visuals
# Vanilla stand-ins while the kit (S1K) is missing (api.K returns ''): the PLAN §3-5 events of each recipe.
SND_FALLBACK = {
    'flare_tell': [('entity.ravager.roar', 0.4, 1.8), ('item.firecharge.use', 0.5, 1.0)],
    'dash': [('entity.blaze.shoot', 0.6, 1.4)],
    'slash_light': [('entity.player.attack.sweep', 0.8, 1.0)],
    'slash_heavy': [('entity.player.attack.sweep', 1.0, 0.7), ('entity.iron_golem.attack', 0.5, 1.2)],
    'spin': [('entity.player.attack.sweep', 1.0, 0.6), ('item.firecharge.use', 0.5, 1.2)],
    'chop': [('entity.generic.explode', 0.6, 1.2), ('block.anvil.land', 0.4, 0.6)],
    'glint': [('block.amethyst_block.resonate', 0.8, 1.6), ('item.trident.return', 0.6, 1.0)],
    'thrust': [('item.trident.throw', 1.0, 0.7)],
    'charge_core': [('entity.warden.sonic_charge', 0.5, 1.3)],
    'step': [('entity.iron_golem.step', 0.5, 1.4)],
    'swap_pyro': [('item.firecharge.use', 0.8, 1.0), ('block.fire.extinguish', 0.4, 1.4)],
    'swap_electro': [('entity.lightning_bolt.impact', 0.4, 1.8), ('block.respawn_anchor.charge', 0.6, 1.2)],
    'mantle_wrap': [('item.elytra.flying', 0.5, 1.4), ('block.beacon.ambient', 0.6, 1.6)],
    'mantle_break': [('block.glass.break', 1.0, 0.7), ('entity.zombie_villager.cure', 0.5, 0.6)],
    'core_backfire': [('entity.generic.explode', 0.9, 0.9), ('entity.blaze.hurt', 0.7, 0.6)],
    'stagger': [('entity.iron_golem.damage', 0.6, 0.8)],
    'wave_hit': [('entity.generic.explode', 0.5, 1.4)],
    'death_knee': [('entity.iron_golem.damage', 0.6, 0.6), ('item.armor.equip_netherite', 0.5, 0.7)],
    'death_ash': [('block.sand.break', 0.7, 0.7), ('entity.blaze.death', 0.4, 0.6)],
}


def snd(name):
    """The kit sound recipe, or its vanilla stand-in lines while the kit is missing."""
    k = K.snd(name)
    if k:
        return [k]
    return [L.sound(e, v, p) for e, v, p in SND_FALLBACK[name]]


EL_PART = {1: 'minecraft:flame', 3: 'minecraft:electric_spark'}


def el_cases(el, fmt):
    """Lines for element el ('cur' = both, gated on #el tk; or a fixed 1 / 3); fmt(e) -> one command or ''."""
    if el == 'cur':
        return [f'execute if score #el {OBJ} matches {e} run {fmt(e)}' for e in (1, 3) if fmt(e)]
    c = fmt(el)
    return [c] if c else []


def placed(lines, pos):
    """Run each line at a position / rotation (pos = execute subcommands); an `execute ... run X` line gets them before
    its first ' run '."""
    out = []
    for c in lines:
        if c.startswith('execute '):
            i = c.index(' run ')
            out.append(c[:i] + ' ' + pos + c[i:])
        else:
            out.append(f'execute {pos} run {c}')
    return out


AT_BODY = 'at @s rotated as @s rotated ~ 0'


def fx_slash(r, el, roll=0, pitch=0, yaw=0):
    """A slash arc at chest height on the body (yaw / pitch / roll = offsets from the body yaw, kit slash_arc)."""
    k = el_cases(el, lambda e: K.p('slash_arc', r=int(round(r * 10)), yaw=yaw, pitch=pitch, roll=roll, el=e))
    if k:
        return placed(k, AT_BODY + ' positioned ~ ~1.2 ~')
    f = L.num(r * 0.3, 2)
    return [f'execute {AT_BODY} positioned ^ ^1.1 ^{L.num(r * 0.55, 2)} run particle minecraft:sweep_attack ~ ~ ~ {f} 0.15 '
            f'{f} 0 4 force @a[tag=player]'] + \
        placed(el_cases(el, lambda e: f'particle {EL_PART[e]} ~ ~ ~ {f} 0.2 {f} 0.02 16 force @a[tag=player]'),
               f'{AT_BODY} positioned ^ ^1.0 ^{L.num(r * 0.55, 2)}')


def fx_spin(r, el):
    k = el_cases(el, lambda e: K.p('spin_ring', r=int(round(r * 10)), el=e))
    if k:
        return placed(k, 'at @s positioned ~ ~1.0 ~')
    f = L.num(r * 0.45, 2)
    return placed(el_cases(el, lambda e: f'particle {EL_PART[e]} ~ ~1 ~ {f} 0.1 {f} 0.03 40 force @a[tag=player]'), 'at @s')


def fx_impact(el, fwd=1.6):
    pos = f'{AT_BODY} positioned ^ ^0.2 ^{L.num(fwd, 2)}'
    k = el_cases(el, lambda e: K.p('impact', el=e))
    if k:
        return placed(k, pos)
    return [f'execute {pos} run particle minecraft:explosion ~ ~ ~ 0.2 0.1 0.2 0 1 force @a[tag=player]']


def fx_trail(preset, length_tenths, el):
    """dash_trail / thrust_trail from the body along its yaw (length in tenths, quantised by the caller)."""
    k = el_cases(el, lambda e: K.p(preset, len=length_tenths, el=e))
    if k:
        return placed(k, AT_BODY + ' positioned ~ ~1.0 ~')
    return placed(el_cases(el, lambda e: f'particle {EL_PART[e]} ~ ~1 ~ 0.3 0.4 0.3 0.05 14 force @a[tag=player]'), 'at @s')


def fx_plain(preset, fallback=None, pos='~ ~1.2 ~', **a):
    k = K.p(preset, **a)
    if k:
        return placed([k], f'{AT_BODY} positioned {pos}')
    return list(fallback or [])


def fx_flare(c=2):
    """Chest + visor flare tell (core_flare; c 1 amber 2 red 3 gold)."""
    return fx_plain('core_flare', ['execute at @s run particle minecraft:dust{color:[1.0,0.25,0.1],scale:1.6} ~ ~1.5 ~ '
                                   '0.2 0.2 0.2 0 8 force @a[tag=player]'], pos='~ ~1.5 ~', c=c)


def fx_glint():
    return fx_plain('glint', [f'execute {AT_BODY} positioned ^-0.4 ^1.6 ^1.4 run particle minecraft:end_rod ~ ~ ~ 0.05 '
                              '0.05 0.05 0.02 6 force @a[tag=player]'], pos='~ ~1.6 ~')


def hud(name, **a):
    k = K.hud(name, **a)
    return [k] if k else []


# ------------------------------------------------------------------------------------------------- hazards
SHAPE_FN = {'sector': L.hz_sector, 'disc': L.hz_disc, 'line': L.hz_line}


def hz_el(el):
    if el == 'cur':
        return [f'scoreboard players operation #hzEl mb = #el {OBJ}']
    return [f'scoreboard players set #hzEl mb {int(el)}']


def hz_tag(key):
    """Tag the hazard just made (#hzLast) rlk_tk_p + rlk_tk_p_<key> (core/hz_tag/<key>; the pattern's cancel kills it)."""
    return (f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run '
            f'function {NS}core/hz_tag/{key}')


def hazard(key, hit, grp=False, tell=1, act=None, kb=None):
    """Lines that create the quiet hazard of api.HITS entry `hit` at the body (floor), aim = body yaw, striking `tell`
    ticks later."""
    clip, event, shape, dims, tier, el = hit
    assert shape in SHAPE_FN, shape
    out = L.hz_opts(quiet=1, sfx=0, grp=grp, act=act, kb=kb) + hz_el(el)
    call = SHAPE_FN[shape](*dims, tell, api.DMG[tier])
    out.append(f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run {call}')
    out.append(hz_tag(key))
    return out


# ------------------------------------------------------------------------------------------------- pattern builder
class PB:
    """Collects the commands of one pattern by pattern tick and writes p/<key>/{start,tick,cancel,k/<t>}."""

    def __init__(self, key, W):
        self.key, self.W = key, W
        self.ticks = defaultdict(list)
        self.ranges = []                    # (t0, t1, command)
        self.cancel_lines = []
        self.hit_ticks = []                 # (event tick, hit index): the tests read them back from the files
        self.end_t = None

    def at(self, t, *lines):
        for ln in lines:
            if isinstance(ln, (list, tuple)):
                self.ticks[t].extend(x for x in ln if x)
            elif ln:
                self.ticks[t].append(ln)

    def rng(self, t0, t1, cmd):
        if t1 >= t0:
            self.ranges.append((t0, t1, cmd))

    def track(self, t0, t1, deg=6):
        """Turn toward the player by at most deg per tick on pattern ticks t0..t1."""
        self.rng(max(1, t0), t1, f'function rlk:mboss/mv/turn {{max:{int(deg)}}}')

    def advance(self, t0, t1, d, unless_within):
        """Step d blocks forward per tick on t0..t1 while the player is farther than unless_within (mv/step: mv/ok)."""
        self.rng(t0, t1, f'execute at @s unless entity @e[tag=rlk_body,distance=..{L.num(unless_within, 2)},limit=1] '
                         f'run function rlk:mboss/mv/step {{d:{L.num(d, 3)}}}')

    def hit(self, idx, grp=False, kb=None):
        """The api.HITS[key][idx] hazard: made at its event tick - 1 (tell 1)."""
        h = api.HITS[self.key][idx]
        t = api.ev(h[0], h[1])
        assert t >= 1
        self.at(t - 1, hazard(self.key, h, grp=grp, kb=kb))
        self.hit_ticks.append((t, idx))
        return t

    def dash(self, t_go, ticks, max_b, stop_before=None, hit_idx=None, grp=False, trail='dash_trail'):
        """A straight dash along the locked body yaw: decided at t_go - 1 (length = max_b, or the player distance -
        stop_before, at most max_b; probed in 0.5 b steps through mv/ok so the end point is inside the arena's safe disc
        and never in a block), glided over `ticks` from t_go. hit_idx: the api.HITS dash_line hazard (made at t_go - 1,
        strikes at t_go, active `ticks` ticks while its length grows with the body: core/dash/grow)."""
        key = self.key
        t0 = t_go - 1
        dl = f'#{key}_dl'
        lines = []
        if stop_before is None:
            lines.append(f'scoreboard players set #t {OBJ} {int(max_b * 2)}')
        else:
            lines += ['function rlk:mboss/mv/dist',
                      f'scoreboard players operation #t {OBJ} = #mbDist mb',
                      f'scoreboard players remove #t {OBJ} {int(round(stop_before * 10))}',
                      f'scoreboard players operation #t {OBJ} /= #c5 {OBJ}',
                      f'execute if score #t {OBJ} matches ..-1 run scoreboard players set #t {OBJ} 0',
                      f'execute if score #t {OBJ} matches {int(max_b * 2) + 1}.. run scoreboard players set #t {OBJ} {int(max_b * 2)}']
        lines += [fn('core/dash/probe'),
                  f'scoreboard players operation {dl} {OBJ} = #t2 {OBJ}',
                  f'execute positioned as @e[type=minecraft:marker,tag=rlk_tk_dp,limit=1] run function rlk:mboss/mv/glide {{t:{int(ticks)}}}',
                  'kill @e[type=minecraft:marker,tag=rlk_tk_dp]']
        el = 'cur'
        if hit_idx is not None:
            clip, event, shape, dims, tier, el = api.HITS[key][hit_idx]
            assert shape == 'dash_line' and api.ev(clip, event) == t_go, (key, hit_idx)
            if grp:
                lines.append(L.GRP_NEW)
            lines += [f'data modify storage {api.STORAGE} core.dl set value {{len:0,w:{int(round(dims[0] * 10))},tell:1,'
                      f'dmg:{api.DMG[tier]}}}',
                      f'execute store result storage {api.STORAGE} core.dl.len int 5 run scoreboard players get {dl} {OBJ}']
            lines += L.hz_opts(quiet=1, sfx=0, grp=grp, act=ticks) + hz_el(el)
            lines += [f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run function rlk:mboss/hz/line with storage '
                      f'{api.STORAGE} core.dl',
                      hz_tag(key),
                      f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add rlk_tk_dl']
            for j in range(ticks):
                self.at(t_go + j,
                        f'scoreboard players operation #hzSzR mb = {dl} {OBJ}',
                        f'scoreboard players set #t3 {OBJ} {5 * (j + 1)}',
                        f'scoreboard players operation #hzSzR mb *= #t3 {OBJ}',
                        f'scoreboard players set #t3 {OBJ} {int(ticks)}',
                        f'scoreboard players operation #hzSzR mb /= #t3 {OBJ}',
                        f'execute as @e[type=minecraft:marker,tag=rlk_tk_dl,tag={tag_p(key)}] run {fn("core/dash/grow")}')
            self.hit_ticks.append((t_go, hit_idx))
        self.at(t0, lines)
        mx = int(max_b * 2)
        q = [(0, mx // 3, mx * 5 // 3), (mx // 3 + 1, 2 * mx // 3, 2 * mx * 5 // 3), (2 * mx // 3 + 1, mx, mx * 5)]
        vis = []
        for lo, hi, ln in q:
            vis += [f'execute if score {dl} {OBJ} matches {lo}..{hi} run {c}' if not c.startswith('execute ')
                    else c.replace('execute ', f'execute if score {dl} {OBJ} matches {lo}..{hi} ', 1)
                    for c in fx_trail(trail, ln, el)]
        self.at(t_go, vis)
        return t_go

    def group(self, t):
        """A new volley group at tick t (before the hazards of one strike: one hit per group)."""
        self.at(t, L.GRP_NEW)

    def end(self, t):
        self.end_t = t
        self.at(t, sset('#done', 1))

    def write(self, start_head=()):
        key, W = self.key, self.W
        assert self.end_t is not None, key
        name = api.PATTERN_NAMES[key]
        W.w(f'p/{key}/start', [f'# {key.upper()} {name} (S3, p_melee.py): pattern tick 0 (@s = the body, at it). Clock #pt tk.',
                               sset('#done', 0)] + list(start_head) + self.ticks.get(0, []))
        tick = [f'# {key.upper()} {name}: one pattern tick (#pt tk = 1..{self.end_t}); events in k/<t>.']
        for t0, t1, cmd in self.ranges:
            rr = f'{t0}' if t0 == t1 else f'{t0}..{t1}'
            tick.append(gate(f'if score #pt {OBJ} matches {rr}', cmd))
        for t in sorted(k for k in self.ticks if k >= 1):
            lines = self.ticks[t]
            if len(lines) == 1 and not lines[0].startswith('$'):
                tick.append(gate(f'if score #pt {OBJ} matches {t}', lines[0]))
            else:
                W.w(f'p/{key}/k/{t}', [f'# {key.upper()} pattern tick {t}'] + lines)
                tick.append(f'execute if score #pt {OBJ} matches {t} run {fn(f"p/{key}/k/{t}")}')
        W.w(f'p/{key}/tick', tick)
        W.w(f'p/{key}/cancel', [f'# {key.upper()} cancel (any executor; idempotent): its hazards and markers, the body glide, the looks.',
                                f'kill @e[tag={tag_p(key)}]',
                                f'execute as {BODY[:-1]},tag=rlk_mb_mv] run function rlk:mboss/mv/stop'] + self.cancel_lines)
