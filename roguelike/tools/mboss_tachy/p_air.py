"""Aerial / ranged patterns of 타키 (Tachy): K 블링크, W1 지상 장풍, W2 공중 장풍 + 강하, L 착지 공격 (PLAN §4.2; footage
sheets S:tk/ref/t_K_v4_{a,b}.jpg, t_K_v6_c.jpg, t_W1_v3_{a,b}.jpg, t_W2_v3_{a,b}.jpg, t_W2_v4_c.jpg, t_L_v4_a.jpg,
t_L_v4_impact.jpg). OWNER: S4.

PATTERNS = [api.Pattern(key, tid, clips, build) for key in api.AIR]; build(W) writes only p/<key>/** (W = the S4 writer).
Every hit tick comes from api.ev (the clip events), every shape / tier / element from api.HITS, dash lengths from
api.DASH_LEN, heights from api.HOVER_Y / api.HIGH_Y. All hazards are quiet (#hzQuiet 1: no ground telegraph, the footage
shows none); the tells are the poses (the rig clips), the blade glint, the chest flare, the sky arcs, the high glints and
the sounds; the hits show the slash / lightning (kit). Effects and sounds through api.K (vanilla stand-ins while the kit
is missing), rig through api.rig / api.play.

Runtime (contract §3.4): @s = the body, at it. The core sets #pat / #pt / #done / the cooldown and calls p/<key>/start,
then p/<key>/tick every tick (#pt + 1 first); #done tk 1 on the last tick. Unlike the melee patterns these ones have
random-length parts (K's hold, L's hover) and an optional W1 pre-blink, so each runs a small stage machine: #<key>_s =
the stage, #<key>_c = the stage clock (0 in s/<stage>/go, + 1 before s/<stage>/tick), and every clip is played at its
stage's tick 0, so a hit of clip event e strikes on stage tick e (a quiet hazard made at e - 1 with tell 1, as s3lib).
W1 keeps the core's #pt at 0 during its pre-blink, so the G3 window (api.G3_WINDOWS['w1'] on #pt) and the w1_wave
events stay on the clip.

End points (reappear, landings, dash ends, the blink-away) all pass the framework's mv/ok (the arena's safe disc - 0.5 b,
inside api.MOVE_R; feet and head free): candidate spots in order, else a spot walked toward the arena centre until mv/ok
passes (p/<key>/u/fit). Heights never pass api.HIGH_Y; nothing goes below the floor (CY). The body carries rlk_mb_inv
only while gone (K, the W1 blink) or high (L). Markers / props carry rlk_room rlk_mb_aux rlk_tk_p rlk_tk_p_<key>
rlk_tk_air; state = fake players #<key>_<x> tk; storage rlk:tk air.*. cancel is idempotent, works with no executor (the
body is found by tag), puts an airborne / hidden body back on the floor and visible.
"""
from collections import defaultdict

from . import api
from . import s3lib as S

L, K = api.L, api.K
OBJ = api.OBJ
NS = api.NS
CY = api.CY
E = api.ev
BODY = S.BODY
PL = '@e[tag=rlk_body,limit=1]'
ARENA = '@e[tag=rlk_mb_arena,limit=1]'
fn, sset = S.fn, S.sset
FACE = 'function rlk:mboss/mv/face'
OK = 'function rlk:mboss/mv/ok'
P3 = api.PH['p3']
EDGE_BACK = S.fn('el/edge')


def turn(deg):
    return f'function rlk:mboss/mv/turn {{max:{int(deg)}}}'


def look(ch, v):
    return api.rig(f'look/{ch}/{v}')


def num(v):
    return L.num(v, 3)


# ------------------------------------------------------------------------------------------------- entities
def tags(key, *more):
    tg = ['rlk_room', 'rlk_mb_aux', api.TAGS['pat'], S.tag_p(key), api.TAGS['air']] + list(more)
    return '[' + ','.join(f'"{t}"' for t in tg) + ']'


def marker(key, *more):
    return f'summon minecraft:marker ~ ~ ~ {{Tags:{tags(key, *more)}}}'


def m1(tag):
    return f'@e[type=minecraft:marker,tag={tag},limit=1]'


# Stand-in prop looks while the kit is missing (an item display the kit's fx/prop/<name> dresses otherwise).
_ID = 'left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],translation:[0f,0f,0f]'
STAND_PROP = {
    'crescent_h': ({1: 'minecraft:orange_stained_glass_pane', 3: 'minecraft:yellow_stained_glass_pane'}, (7.0, 0.3, 0.6)),
    'crescent_v': ({1: 'minecraft:orange_stained_glass_pane', 3: 'minecraft:yellow_stained_glass_pane'}, (0.3, 2.6, 0.6)),
    'feather': ({3: 'minecraft:feather'}, (1.6, 1.6, 1.6)),
}


def prop_lines(key, look, el, tag_new):
    """Summon one projectile display here (rotation set by pj/launch), tagged tag_new until launched; el 'cur' or 1 / 3.
    With the kit: a plain display dressed by fx/prop/<look>_<el>; without: a glowing stand-in item."""
    out = []
    els = (1, 3) if el == 'cur' else (el,)
    for e in els:
        gate = f'execute if score #el {OBJ} matches {e} run ' if el == 'cur' else ''
        name = f'{look}_{e}' if look != 'feather' else 'feather'
        if K.prop(name):
            nbt = f'{{Tags:{tags(key, "rlk_tk_pj", tag_new)},teleport_duration:1}}'
        else:
            items, sc = STAND_PROP[look]
            item = items.get(e, items[max(items)])
            nbt = (f'{{Tags:{tags(key, "rlk_tk_pj", tag_new)},teleport_duration:1,brightness:{{sky:15,block:15}},'
                   f'item:{{id:"{item}",count:1}},transformation:{{{_ID},scale:[{sc[0]}f,{sc[1]}f,{sc[2]}f]}}}}')
        out.append(f'{gate}summon minecraft:item_display ~ ~ ~ {nbt}')
        if K.prop(name):
            out.append(f'{gate}execute as @e[type=minecraft:item_display,tag={tag_new}] run {K.prop(name)}')
    return out


# ------------------------------------------------------------------------------------------------- sounds / visuals
# Vanilla stand-ins of the kit sound recipes used here (PLAN §4.2 events); s3lib's table covers the rest.
SND_FALLBACK = {
    'blink_out': [('entity.enderman.teleport', 0.6, 0.6), ('block.amethyst_block.chime', 0.5, 1.4)],
    'blink_in': [('entity.enderman.teleport', 0.5, 0.9), ('item.trident.return', 0.4, 1.4)],
    'leap': [('entity.ender_dragon.flap', 0.6, 1.5), ('entity.phantom.flap', 0.6, 0.8)],
    'sky_arcs': [('block.respawn_anchor.charge', 0.6, 1.6), ('entity.lightning_bolt.impact', 0.3, 2.0)],
    'plunge': [('entity.lightning_bolt.impact', 1.0, 1.2), ('entity.generic.explode', 0.6, 1.1)],
    'wave_release': [('entity.player.attack.sweep', 1.0, 0.6), ('item.firecharge.use', 0.6, 1.3)],
    'air_swoop': [('entity.phantom.swoop', 0.7, 1.0)],
    'dive': [('entity.phantom.swoop', 0.9, 0.7), ('item.trident.riptide_1', 0.6, 1.2)],
    'shock': [('entity.lightning_bolt.impact', 1.0, 1.0), ('entity.generic.explode', 0.6, 0.9)],
    'high_glint': [('entity.phantom.flap', 0.4, 1.6), ('block.amethyst_block.chime', 0.6, 1.6)],
    'nova_swell': [('block.beacon.power_select', 0.8, 1.2), ('entity.warden.sonic_charge', 0.7, 1.0)],
    'nova_blast': [('entity.generic.explode', 1.0, 0.7), ('entity.lightning_bolt.impact', 0.8, 1.4)],
    'feather_fall': [('block.amethyst_block.chime', 0.5, 1.8), ('entity.phantom.flap', 0.3, 1.9)],
}
# W1's charge has no kit recipe (KIT_SOUNDS): PLAN §4.2 W1 vanilla events.
W1_CHARGE = [('block.beacon.ambient', 0.6, 1.8), ('block.respawn_anchor.charge', 0.6, 1.0)]
STOP_SOUNDS = ('block.respawn_anchor.charge', 'block.beacon.ambient', 'entity.warden.sonic_charge',
               'block.beacon.power_select')


def snd(name, pos='at @s'):
    """The kit sound recipe at pos, or its vanilla stand-in lines."""
    k = K.snd(name)
    if k:
        return S.placed([k], pos)
    if name in SND_FALLBACK:
        return S.placed([L.sound(e, v, p) for e, v, p in SND_FALLBACK[name]], pos)
    return S.placed(S.snd(name), pos)


def stop_sounds():
    return [f'stopsound @a[tag=player] hostile minecraft:{e}' for e in STOP_SOUNDS]


def fx(preset, fallback, pos, **a):
    """A kit preset at pos (execute subcommands), or the stand-in particle lines (run at pos)."""
    k = K.p(preset, **a)
    return S.placed([k] if k else list(fallback), pos)


def part(name, dx, dy, dz, spd, n):
    return f'particle {name} ~ ~ ~ {dx} {dy} {dz} {spd} {n} force @a[tag=player]'


EL_PART = S.EL_PART
GOLD = 'minecraft:dust{color:[1.0,0.82,0.25],scale:1.4}'
WHITE = 'minecraft:end_rod'
SPARK = 'minecraft:electric_spark'


def fx_el(preset, fallback_fmt, pos, el, **a):
    """A kit preset with el (cur = gated on #el tk) at pos, or fallback_fmt(e) particle lines."""
    lines = []
    for e in ((1, 3) if el == 'cur' else (el,)):
        k = K.p(preset, el=e, **a)
        ls = [k] if k else [fallback_fmt(e)]
        if el == 'cur':
            ls = [f'execute if score #el {OBJ} matches {e} run {x}' for x in ls]
        lines += ls
    return S.placed(lines, pos)


AT_BODY = 'at @s rotated as @s rotated ~ 0'


def blink_out_fx():
    return fx('blink_out', [part(GOLD, 0.4, 0.8, 0.4, 0, 24), part(WHITE, 0.3, 0.7, 0.3, 0.05, 10)],
              AT_BODY + ' positioned ~ ~1.2 ~') + snd('blink_out')


def blink_in_fx():
    return fx('blink_in', [part(GOLD, 0.4, 0.8, 0.4, 0, 24), part(WHITE, 0.3, 0.7, 0.3, 0.05, 10)],
              AT_BODY + ' positioned ~ ~1.2 ~') + snd('blink_in')


def glint_fx():
    return fx('glint', [part(WHITE, 0.05, 0.05, 0.05, 0.02, 6)], AT_BODY + ' positioned ^-0.4 ^1.6 ^1.4') + snd('glint')


def wing_fx():
    return fx('wing_flare', [part(GOLD, 0.9, 0.5, 0.9, 0, 16)], AT_BODY + ' positioned ~ ~1.4 ~')


# ------------------------------------------------------------------------------------------------- hazards
def hazard(key, hit, pos=None, tell=1, grp=False, extra_tag=None):
    """The quiet hazard of api.HITS entry `hit` (s3lib.hazard) striking `tell` ticks later; pos = execute subcommands for
    a hazard away from the body (on the floor: y CY), aim = the body yaw. extra_tag: one more tag on it."""
    lines = S.hazard(key, hit, grp=grp, tell=tell)
    if pos:
        call = lines[-2]
        head = f'execute at @s rotated as @s rotated ~ 0 positioned ~ {CY} ~ run '
        assert call.startswith(head), call
        lines[-2] = f'execute rotated as @s rotated ~ 0 {pos} positioned ~ {CY} ~ run {call[len(head):]}'
    if extra_tag:
        lines.append(f'execute as @e[type=minecraft:marker,tag=rlk_mb_hz] if score @s mbHzI = #hzLast mb run tag @s add {extra_tag}')
    return lines


# ------------------------------------------------------------------------------------------------- stage machine
class Stage:
    def __init__(self, sm, name):
        self.sm, self.name = sm, name

    def at(self, t, *lines):
        d = self.sm.ev[self.name]
        for ln in lines:
            if isinstance(ln, (list, tuple)):
                d[t].extend(x for x in ln if x)
            elif ln:
                d[t].append(ln)
        return self

    def rng(self, t0, t1, cmd):
        if t1 >= t0:
            self.sm.rg[self.name].append((t0, t1, cmd))
        return self

    def every(self, *lines):
        """Lines at the top of every tick of this stage (before the events)."""
        self.sm.head[self.name].extend(x for x in lines if x)
        return self

    def tail(self, *lines):
        """Lines at the end of every tick of this stage (variable-length ends: `return run` a go)."""
        self.sm.tail[self.name].extend(x for x in lines if x)
        return self

    def to(self, t, nxt):
        """Go to stage nxt on tick t (the last thing of that tick)."""
        self.at(t, self.sm.go(nxt))
        self.sm.trans[self.name].add(t)
        return self


class _PBShim(S.PB):
    """s3lib.PB.dash writing into one stage of a stage machine (the stage clock == the clip tick)."""

    def __init__(self, key, W, stage):
        super().__init__(key, W)
        self.stage = stage

    def at(self, t, *lines):
        self.stage.at(t, *lines)


class SM:
    """Stage machine of one S4 pattern: p/<key>/{start,tick,cancel}, p/<key>/s/<stage>/{go,tick,k/<t>}."""

    def __init__(self, key, W):
        self.key, self.W = key, W
        self.order = []
        self.ev, self.rg = {}, {}
        self.head, self.tail = {}, {}
        self.trans = {}
        self.start = []
        self.cancel = []
        self.done_t = {}

    def st(self, name):
        if name not in self.ev:
            self.order.append(name)
            self.ev[name] = defaultdict(list)
            self.rg[name], self.head[name], self.tail[name] = [], [], []
            self.trans[name] = set()
        return Stage(self, name)

    def go(self, name):
        return fn(f'p/{self.key}/s/{name}/go')

    def c(self):
        return f'#{self.key}_c'

    def end(self, stage, t):
        self.st(stage).at(t, sset('#done', 1))
        self.done_t[stage] = t

    def dash(self, stage, t_go, ticks, max_b, hit_idx, stop_before=None):
        """s3lib.PB.dash in a stage (decided at t_go - 1, probed through core/dash/probe, the grown dash-line hazard)."""
        pb = _PBShim(self.key, self.W, self.st(stage))
        pb.dash(t_go, ticks, max_b, stop_before=stop_before, hit_idx=hit_idx, trail='thrust_trail')

    def write(self):
        key, W, c = self.key, self.W, self.c()
        name = api.PATTERN_NAMES[key]
        W.w(f'p/{key}/start', [f'# {key.upper()} {name} (S4, p_air.py): pattern start (@s = the body, at it; #pt tk 0).',
                               sset('#done', 0), sset(f'#{key}_s', 0), sset(f'#{key}_c', 0)] + self.start)
        tick = [f'# {key.upper()} {name}: one tick; the stage machine (#{key}_s = stage, {c} = stage clock).',
                f'scoreboard players add {c} {OBJ} 1']
        for i, st in enumerate(self.order):
            tick.append(f'execute if score #{key}_s {OBJ} matches {i + 1} run return run {fn(f"p/{key}/s/{st}/tick")}')
        W.w(f'p/{key}/tick', tick)
        for i, st in enumerate(self.order):
            ev = self.ev[st]
            W.w(f'p/{key}/s/{st}/go', [f'# {key.upper()} stage {st}: tick 0 (@s = body).', sset(f'#{key}_s', i + 1),
                                       sset(f'#{key}_c', 0)] + ev.get(0, []))
            tk = [f'# {key.upper()} stage {st}: one tick ({c} 1..).'] + list(self.head[st])
            for t0, t1, cmd in self.rg[st]:
                rr = f'{t0}' if t0 == t1 else f'{t0}..{t1}'
                tk.append(S.gate(f'if score {c} {OBJ} matches {rr}', cmd))
            for t in sorted(k for k in ev if k >= 1):
                lines = ev[t]
                ret = 'return run ' if t in self.trans[st] else ''
                if len(lines) == 1 and not ret:
                    tk.append(S.gate(f'if score {c} {OBJ} matches {t}', lines[0]))
                else:
                    W.w(f'p/{key}/s/{st}/k/{t}', [f'# {key.upper()} stage {st} tick {t}'] + lines)
                    tk.append(f'execute if score {c} {OBJ} matches {t} run {ret}{fn(f"p/{key}/s/{st}/k/{t}")}')
            tk += self.tail[st]
            W.w(f'p/{key}/s/{st}/tick', tk)
        W.w(f'p/{key}/cancel', [f'# {key.upper()} cancel (any executor; idempotent): its hazards, markers and props, the body',
                                '# back on the floor (inside mv/ok), visible and vulnerable, the looks and the long sounds.',
                                f'kill @e[tag={S.tag_p(key)}]',
                                f'execute as {BODY} at @s run {fn(f"p/{key}/u/settle")}',
                                sset(f'#{key}_s', 0)] + self.cancel + stop_sounds())
        helpers(W, key)


def helpers(W, key):
    """p/<key>/u/{fit,settle}: the end-point fallback and the cancel's body reset."""
    n = f'#{key}_n'
    W.w(f'p/{key}/u/fit', [
        '# @s (a spot marker or the body) on the floor: when its spot fails mv/ok (outside the safe disc, in a block), walk',
        f'# it 0.5 b toward the arena centre until it passes (at most 60 steps; {n} tk counts). Fails when none passed.',
        f'execute at @s if {OK} run return 1',
        f'execute if score {n} {OBJ} matches 60.. run return fail',
        f'scoreboard players add {n} {OBJ} 1',
        f'execute at @s unless {OK} facing entity {ARENA} feet rotated ~ 0 positioned ^ ^ ^0.5 run tp @s ~ ~ ~',
        f'return run function {NS}p/{key}/u/fit'])
    st = f'rlk_tk_{key}set'
    W.w(f'p/{key}/u/settle', [
        '# @s = the body (cancel): glide stopped, on the floor below her (walked inside mv/ok by u/fit; the arena centre',
        '# if none passed), visible, vulnerable.',
        'execute if entity @s[tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
        'tag @s remove rlk_mb_inv',
        f'kill @e[type=minecraft:marker,tag={st}]',
        f'execute at @s positioned ~ {CY} ~ run {marker(key, st)}',
        sset(n, 0),
        f'execute as {m1(st)} run function {NS}p/{key}/u/fit',
        f'execute store success score {n} {OBJ} at {m1(st)} if {OK} run tp @s ~ ~ ~',
        f'execute if score {n} {OBJ} matches 0 run function rlk:mboss/mv/home',
        f'kill @e[type=minecraft:marker,tag={st}]',
        api.rig('state/normal'), EDGE_BACK, look('chest', 'off')])


def lock_lines(key, tag):
    """A lock marker (tag) at the player's feet on the floor, walked inside mv/ok (#<key>_n); the old one goes."""
    return [f'kill @e[type=minecraft:marker,tag={tag}]',
            f'execute at {PL} positioned ~ {CY} ~ run {marker(key, tag)}',
            sset(f'#{key}_n', 0),
            f'execute as {m1(tag)} unless function {NS}p/{key}/u/fit run kill @s',
            f'execute unless entity {m1(tag)} positioned as {BODY} positioned ~ {CY} ~ run {marker(key, tag)}']


def face_to(tag):
    return f'execute at @s facing entity {m1(tag)} feet run tp @s ~ ~ ~ ~ 0'


# ------------------------------------------------------------------------------------------------- K 블링크
K_R = 4.5
# reappear candidates (yaw offset from the player's facing, distance): the front arc first, then the sides, behind last
K_SPOTS = [(0, 4.5), (30, 4.5), (60, 4.5), (90, 4.5), (120, 4.5), (180, 4.5),
           (0, 3.5), (45, 3.5), (90, 3.5), (135, 3.5), (180, 3.5), (0, 5.5), (45, 5.5), (90, 5.5)]
K_HOLD = {'p12': (20, 60), 'p3': (10, 40)}
K_GONE = 24
K_LEAP_H = 6.0


def build_k(W):
    key = 'k'
    sm = SM(key, W)
    gone = E('blink_out', 'gone')
    bi_len = api.CLIPS['blink_in'][0]
    thrust = E('k_glint', 'thrust')
    up, lp_len = E('k_leap', 'up'), api.CLIPS['k_leap'][0]
    hit, pl_len = E('k_plunge', 'hit'), api.CLIPS['k_plunge'][0]
    dive_t = 4                                                   # the drop: the last 4 t before the plunge hit
    sm.start = [sset('#k_2', 0), sm.go('out')]
    # 1 out: vanish (blink_out; gone at its 'gone' event: hidden, invulnerable, parked at her spot) for K_GONE t
    out = sm.st('out')
    out.at(0, FACE, api.play('blink_out'), blink_out_fx())
    out.at(gone, 'tag @s add rlk_mb_inv', api.rig('state/hidden'))
    out.to(gone + K_GONE, 'in')
    # 2 in: reappear 4.5 b from the player (p/k/spot), blink_in, then hold 20-60 t (P3 10-40) facing the player
    hp = K_HOLD['p12']
    h3 = K_HOLD['p3']
    inn = sm.st('in')
    inn.at(0, fn('p/k/spot'), 'tag @s remove rlk_mb_inv', api.rig('state/normal'), api.play('blink_in'), blink_in_fx(),
           wing_fx(),
           f'execute store result score #k_h {OBJ} run random value {hp[0]}..{hp[1]}',
           f'execute if score #ph {OBJ} matches {P3} store result score #k_h {OBJ} run random value {h3[0]}..{h3[1]}',
           f'scoreboard players add #k_h {OBJ} {bi_len}')
    inn.at(bi_len, api.play('k_hold'))
    inn.rng(1, 200, turn(8))
    inn.tail(f'execute if score #k_c {OBJ} >= #k_h {OBJ} run return run {sm.go("gl")}')
    # 3 gl: glint (the point is locked: she faces the player once), thrust through it 16 t later (6 b dash line, T3)
    gl = sm.st('gl')
    gl.at(0, FACE, api.play('k_glint'), look('edge', 'glint'), glint_fx())
    sm.dash('gl', thrust, 4, api.DASH_LEN['k'], hit_idx=0)
    gl.at(thrust, snd('thrust'), EDGE_BACK)
    gl.at(thrust + 4, f'execute if score #k_2 {OBJ} matches 1 run return run {sset("#done", 1)}')
    gl.to(thrust + 4, 'lp')
    # 4 lp: leap (k_leap, she rises 6 b from 'up'), then the plunge stage at the clip end
    lp = sm.st('lp')
    lp.at(0, api.play('k_leap'), snd('leap'), wing_fx())
    lp.at(up, f'execute at @s positioned ~ {num(CY + K_LEAP_H)} ~ run function rlk:mboss/mv/glide {{t:{lp_len - up}}}')
    lp.to(lp_len, 'pl')
    # 5 pl: sky arcs over the player's spot (locked now, walked inside mv/ok) for 16 t, she drops on it: disc 3.5 T4 Electro
    pl = sm.st('pl')
    arcs = S.placed([K.p('sky_arcs', r=35, t=hit)] if K.p('sky_arcs', r=35, t=hit) else [], f'at {m1("rlk_tk_klock")}')
    pl.at(0, lock_lines(key, 'rlk_tk_klock'), api.play('k_plunge'), face_to('rlk_tk_klock'), arcs,
          snd('sky_arcs', f'at {m1("rlk_tk_klock")} positioned ~ ~6 ~'))
    if not K.p('sky_arcs', r=35, t=hit):
        pl.rng(0, hit - 1, f'execute at {m1("rlk_tk_klock")} positioned ~ ~6 ~ run {part(SPARK, 1.0, 1.8, 1.0, 0, 6)}')
    pl.at(hit - dive_t, f'execute positioned as {m1("rlk_tk_klock")} run function rlk:mboss/mv/glide {{t:{dive_t}}}')
    pl.at(hit - 1, hazard(key, api.HITS[key][1], pos=f'at {m1("rlk_tk_klock")}'))
    pl.at(hit, fx('bolt', [part('minecraft:explosion', 0.3, 0.1, 0.3, 0, 2), part(SPARK, 1.6, 0.3, 1.6, 0.2, 40)],
                  f'at {m1("rlk_tk_klock")}'),
          fx('shock_ring', [part(GOLD, 1.8, 0.1, 1.8, 0, 30)], f'at {m1("rlk_tk_klock")} positioned ~ ~0.1 ~', r=35),
          snd('plunge'))
    pl.at(pl_len, f'kill @e[type=minecraft:marker,tag=rlk_tk_klock]',
          f'execute if score #ph {OBJ} matches {P3} if score #k_2 {OBJ} matches 0 run return run function {NS}p/k/k2',
          sset('#done', 1))
    W.w('p/k/k2', ['# K2 (P3): after the plunge one more vanish -> reappear -> glint -> thrust (no second plunge).',
                   sset('#k_2', 1), sm.go('out')])
    # the reappear spot
    spot = ['# K reappear spot (@s = body): 4.5 b from the player, the front arc first (a random side first), then the',
            '# sides, behind last; then 3.5 / 5.5 b; each must pass mv/ok; else the front spot walked inside (u/fit); else',
            '# her own spot. She faces the player.',
            f'execute store result score #k_r {OBJ} run random value 0..1']
    for a, r in K_SPOTS:
        for v, sgn in ((0, 1), (1, -1)):
            if a in (0, 180) and v == 1:
                continue
            gate = '' if a in (0, 180) else f'if score #k_r {OBJ} matches {v} '
            for s2 in ((sgn, -sgn) if a not in (0, 180) else (1,)):
                yaw = a * s2
                spot.append(f'execute {gate}at {PL} positioned ~ {CY} ~ rotated as {PL} rotated ~{yaw} 0 '
                            f'positioned ^ ^ ^{num(r)} if {OK} run return run {fn("p/k/put")}')
    spot += [f'execute at {PL} positioned ~ {CY} ~ rotated as {PL} rotated ~ 0 positioned ^ ^ ^{num(K_R)} run '
             f'{marker(key, "rlk_tk_kspot")}', sset('#k_n', 0),
             f'execute as {m1("rlk_tk_kspot")} if function {NS}p/k/u/fit at @s run function {NS}p/k/put_m',
             'kill @e[type=minecraft:marker,tag=rlk_tk_kspot]',
             f'execute at @s facing entity {PL} feet run tp @s ~ ~ ~ ~ 0']
    W.w('p/k/spot', spot)
    W.w('p/k/put', ['# The body to this spot (@s = body; the caller checked mv/ok), facing the player.', f'execute if {OK} run tp @s ~ ~ ~',
                    f'execute at @s facing entity {PL} feet run tp @s ~ ~ ~ ~ 0'])
    W.w('p/k/put_m', ['# @s = the walked spot marker: the body goes there.', f'execute as {BODY} run {fn("p/k/put")}'])
    sm.cancel = [sset('#k_2', 0)]
    # pause / resume: the kit's sky arcs are cards (fx/clear on pause): redraw the rest of them
    if K.p('sky_arcs', r=35, t=hit):
        W.w('p/k/pause', ['# K pause: nothing to stop (the framework freezes the glide and the hazards).'])
        W.w('p/k/resume', [
            '# K resume: the sky arcs over the lock (kit cards, cleared on pause) for the rest of their 16 t.',
            f'execute unless score #k_s {OBJ} matches {sm.order.index("pl") + 1} run return 0',
            f'execute if score #k_c {OBJ} matches {hit}.. run return 0',
            f'scoreboard players set #k_t {OBJ} {hit}',
            f'scoreboard players operation #k_t {OBJ} -= #k_c {OBJ}',
            f'data modify storage {api.STORAGE} air.k set value {{r:35,t:1}}',
            f'execute store result storage {api.STORAGE} air.k.t int 1 run scoreboard players get #k_t {OBJ}',
            f'execute at {m1("rlk_tk_klock")} run function {NS}fx/p/sky_arcs with storage {api.STORAGE} air.k'])
    sm.write()
    return sm


# ------------------------------------------------------------------------------------------------- W1 지상 장풍
W1_FAR = 12.0
W1_SPOTS = [(0, 14.0), (25, 14.0), (50, 14.0), (0, 16.0), (25, 16.0), (0, 12.5), (50, 12.5), (75, 12.5), (100, 12.5)]
W1_Y = 0.9                       # blade height above the floor: the framework's rows cover 0 .. 1.65 b


def build_w1(W):
    key = 'w1'
    sm = SM(key, W)
    clip = 'w1_wave'
    glow, end = E(clip, 'glow'), E(clip, 'end')
    waves = [E(clip, e) for e in ('wave1', 'wave2', 'wave3')]
    w0, w1 = api.G3_WINDOWS[key]
    assert w0 == glow, (w0, glow)
    sm.start = ['function rlk:mboss/mv/dist',
                f'execute if score #mbDist mb matches {int(W1_FAR * 10)}.. run return run {sm.go("ch")}',
                sm.go('bl')]
    # 1 bl: closer than 12 b -> backstep + blink to the far side (34 t). The core's #pt stays 0 meanwhile, so the G3
    # window and the w1_wave events below are on the clip.
    bo_t = api.CLIPS['backstep'][0]                                          # 12
    gone = bo_t + E('blink_out', 'gone')                                     # 18
    back = gone + 6                                                          # 24: blink_in
    bl_len = back + api.CLIPS['blink_in'][0]                                 # 34
    bl = sm.st('bl')
    bl.every(f'scoreboard players set #pt {OBJ} 0')
    bl.at(0, FACE, api.play('backstep'), snd('step'),
          f'execute at @s rotated as @s rotated ~180 0 positioned ^ ^ ^1.5 if {OK} run function rlk:mboss/mv/glide '
          f'{{t:{E("backstep", "land")}}}')
    bl.at(bo_t, api.play('blink_out'), blink_out_fx())
    bl.at(gone, 'tag @s add rlk_mb_inv', api.rig('state/hidden'))
    bl.at(back, fn('p/w1/far'), 'tag @s remove rlk_mb_inv', api.rig('state/normal'), api.play('blink_in'), blink_in_fx())
    bl.to(bl_len, 'ch')
    spot = ['# W1 blink-away spot (@s = body): 12.5-16 b from the player toward / past the arena centre (a random side',
            '# first), each must pass mv/ok; else she stays. She faces the player.',
            f'execute store result score #w1_r {OBJ} run random value 0..1']
    for a, d in W1_SPOTS:
        for v in ((0, 1) if a else (0,)):
            for s2 in ((1, -1) if v == 0 else (-1, 1)) if a else (1,):
                gate = f'if score #w1_r {OBJ} matches {v} ' if a else ''
                spot.append(f'execute {gate}at {PL} positioned ~ {CY} ~ facing entity {ARENA} feet rotated ~{a * s2} 0 '
                            f'positioned ^ ^ ^{num(d)} if {OK} run return run {fn("p/w1/put")}')
    spot.append(f'execute at @s facing entity {PL} feet run tp @s ~ ~ ~ ~ 0')
    W.w('p/w1/far', spot)
    W.w('p/w1/put', ['# The body to this spot (@s = body; the caller checked mv/ok), facing the player.', f'execute if {OK} run tp @s ~ ~ ~',
                     f'execute at @s facing entity {PL} feet run tp @s ~ ~ ~ ~ 0'])
    # 2 ch: the w1_wave clip. Plant, the gold glow grows along the level blade (chest amber = the G3 window 6..39),
    # three horizontal crescents re-aimed at each release (46 / 58 / 70), end 88.
    ch = sm.st('ch')
    ch.at(0, FACE, api.play(clip), snd('step'))
    ch.at(glow, look('chest', 'amber'), look('edge', 'yellow'), S.fx_flare(1),
          S.placed([L.sound(e, v, p) for e, v, p in W1_CHARGE], 'at @s'))
    ch.rng(1, waves[-1] - 1, turn(6))
    if not K.p('glint'):
        ch.rng(glow, waves[0] - 1, f'execute {AT_BODY} positioned ^0.9 ^1.1 ^0.6 run {part(GOLD, 0.6, 0.05, 0.3, 0, 2)}')
    ch.at(w1, look('chest', 'off'))
    hits = api.HITS[key]
    for i, t in enumerate(waves):
        clip_, ev_, shape, dims, tier, el = hits[i]
        assert (clip_, shape) == (clip, 'pj_blade') and E(clip_, ev_) == t
        ch.at(t, FACE, f'execute {AT_BODY} positioned ^ ^ ^1 positioned ~ {num(CY + W1_Y)} ~ run {fn("p/w1/wave")}',
              S.fx_slash(dims[0], el, roll=0), snd('wave_release'))
    ch.at(waves[-1], EDGE_BACK)
    sm.end('ch', end)
    hr, spd, life = hits[0][3]
    W.w('p/w1/wave', [
        f'# One W1 crescent here (@s = body; rotated = her yaw, pitch 0): a horizontal blade pj (#pjShape 1, hr {hr}, {spd} b/t,',
        f'# {life} t, wall stop), height {W1_Y} b (rows 0 .. 1.65 b: jumping does not clear it), {hits[0][4]}, the blade element.']
      + prop_lines(key, 'crescent_h', 'cur', 'rlk_tk_new')
      + [f'execute as @e[type=minecraft:item_display,tag=rlk_tk_new] run {fn("p/w1/launch")}'])
    W.w('p/w1/launch', ['# @s = the new crescent display (positioned / rotated as the release).',
                        f'scoreboard players operation #pjEl mb = #el {OBJ}']
        + L.pj_opts(shape=1, wall=1) + [L.pj_launch(spd, life, api.DMG[hits[0][4]], hr), 'tag @s remove rlk_tk_new'])
    W.w('p/w1/pj_end', [
        '# A W1 crescent ended (@s = the prop; #pjEv 1 wall, 2 life, 4 hit the player: it pierces on): sparks at walls.',
        'execute unless score #pjEv mb matches 1..2 run return 0']
        + fx_el('impact', lambda e: part('minecraft:explosion', 0.2, 0.2, 0.2, 0, 1), 'at @s', 'cur')
        + snd('wave_hit'))
    if K.prop('crescent_h_1'):
        W.w('p/w1/resume', ['# W1 resume: the crescent looks again (kit cards may have been cleared on pause).']
            + [f'execute if score #el {OBJ} matches {e} as @e[type=minecraft:item_display,tag=rlk_tk_p_w1,tag=rlk_tk_pj] run '
               f'{K.prop(f"crescent_h_{e}")}' for e in (1, 3)])
    sm.write()
    return sm


# ------------------------------------------------------------------------------------------------- W2 공중 장풍 + 강하
W2_SHORT = 1.5                  # she lands this far short of the locked point (the arc's middle is on it)
W2_DIVE_T = 6


def build_w2(W):
    key = 'w2'
    sm = SM(key, W)
    lift, top = E('leap_up', 'lift'), E('leap_up', 'top')
    cs = [E('w2_air', e) for e in ('c1', 'c2', 'c3')]
    pull, go = E('w2_air', 'pull'), E('w2_air', 'go')
    slash, dend = E('w2_dive', 'slash'), E('w2_dive', 'end')
    lend = api.CLIPS['land'][0]
    lock_t = go - 6
    sm.start = [sm.go('up')]
    # 1 up: leap to HOVER_Y (feet) over the lift
    up = sm.st('up')
    up.at(0, FACE, api.play('leap_up'), snd('leap'), wing_fx())
    up.at(lift, f'execute at @s positioned ~ {num(api.HOVER_Y)} ~ run function rlk:mboss/mv/glide {{t:{top - lift}}}')
    up.to(top, 'air')
    # 2 air: three vertical crescents at the player's chest (re-aimed each), pull back, the point locked 6 t before the dive
    air = sm.st('air')
    air.at(0, api.play('w2_air'))
    air.rng(1, lock_t, turn(8))
    hits = api.HITS[key]
    for i, t in enumerate(cs):
        clip_, ev_, shape, dims, tier, el = hits[i]
        assert shape == 'pj_ball' and E(clip_, ev_) == t
        air.at(t, FACE, f'execute {AT_BODY} positioned ^ ^1.6 ^0.8 run {fn("p/w2/wave")}',
               S.fx_slash(2.6, el, roll=90), snd('wave_release'))
    air.at(pull, look('edge', 'glint'), wing_fx(), snd('air_swoop'))
    air.at(lock_t, lock_lines(key, 'rlk_tk_w2lock'), face_to('rlk_tk_w2lock'))
    air.to(go, 'dv')
    hr, spd, life = hits[0][3]
    W.w('p/w2/wave', [
        f'# One W2 crescent here (@s = body, at her chest): a vertical crescent pj (sphere hr {hr}, {spd} b/t, {life} t,',
        f'# wall stop) aimed down at the player\'s chest (feet + 0.9: the hit point 0.9 b below it meets the feet), {hits[0][4]}.',
        'kill @e[type=minecraft:marker,tag=rlk_tk_aim]',
        f'execute at {PL} positioned ~ ~0.9 ~ run {marker(key, "rlk_tk_aim")}']
      + [f'execute facing entity {m1("rlk_tk_aim")} feet run {x}' for x in prop_lines(key, 'crescent_v', 'cur', 'rlk_tk_new')]
      + [f'execute facing entity {m1("rlk_tk_aim")} feet as @e[type=minecraft:item_display,tag=rlk_tk_new] run '
         f'{fn("p/w2/launch")}',
         'kill @e[type=minecraft:marker,tag=rlk_tk_aim]'])
    W.w('p/w2/launch', ['# @s = the new crescent display (positioned at her chest, rotated toward the player\'s chest).',
                        f'scoreboard players operation #pjEl mb = #el {OBJ}']
        + L.pj_opts(shape=0, wall=1) + [L.pj_launch(spd, life, api.DMG[hits[0][4]], hr), 'tag @s remove rlk_tk_new'])
    W.w('p/w2/pj_end', [
        '# A W2 crescent ended (@s = the prop; #pjEv 1 floor / wall, 2 life, 4 hit the player: it flies on): sparks.',
        'execute unless score #pjEv mb matches 1..2 run return 0']
        + fx_el('impact', lambda e: part('minecraft:explosion', 0.2, 0.2, 0.2, 0, 1), 'at @s', 'cur')
        + snd('wave_hit'))
    # 3 dv: the dive to the locked point (<= 14 b, 6 t; landing W2_SHORT b short, probed along the floor through mv/ok),
    # the big arc at the clip's slash: sector 4.5 / 80 T4
    dv = sm.st('dv')
    steps = int(api.DASH_LEN['w2'] * 2)
    dv.at(0, api.play('w2_dive'), snd('dive'), face_to('rlk_tk_w2lock'),
          'kill @e[type=minecraft:marker,tag=rlk_tk_w2p]',
          f'execute at @s positioned ~ {CY} ~ facing entity {m1("rlk_tk_w2lock")} feet rotated ~ 0 run {marker(key, "rlk_tk_w2p")}',
          f'execute at @s positioned ~ {CY} ~ facing entity {m1("rlk_tk_w2lock")} feet rotated ~ 0 as {m1("rlk_tk_w2p")} run '
          'tp @s ~ ~ ~ ~ 0',
          sset('#w2_n', 0),
          f'execute as {m1("rlk_tk_w2p")} at @s run {fn("p/w2/probe")}',
          f'execute positioned as {m1("rlk_tk_w2p")} run function rlk:mboss/mv/glide {{t:{W2_DIVE_T}}}')
    W.w('p/w2/probe', [
        f'# The dive probe (@s = marker on the floor, rotated toward the lock): 0.5 b steps while the next spot passes mv/ok,',
        f'# at most {steps} ({api.DASH_LEN["w2"]} b), stopping {W2_SHORT} b short of the locked point.',
        f'execute if score #w2_n {OBJ} matches {steps}.. run return 0',
        f'execute if entity @e[type=minecraft:marker,tag=rlk_tk_w2lock,distance=..{num(W2_SHORT)}] run return 0',
        f'execute positioned ^ ^ ^0.5 unless {OK} run return 0',
        f'execute positioned ^ ^ ^0.5 if {OK} run tp @s ~ ~ ~',
        f'scoreboard players add #w2_n {OBJ} 1',
        f'execute at @s run function {NS}p/w2/probe'])
    if not K.p('thrust_trail', len=10, el=1):
        dv.rng(1, W2_DIVE_T, f'execute at @s run {part(GOLD, 0.3, 0.6, 0.3, 0, 6)}')
    dv.at(W2_DIVE_T + 1, 'kill @e[type=minecraft:marker,tag=rlk_tk_w2p]', 'kill @e[type=minecraft:marker,tag=rlk_tk_w2lock]')
    dv.at(slash - 1, hazard(key, hits[3]))
    dv.at(slash, S.fx_slash(hits[3][3][0], hits[3][5], roll=20), S.fx_impact(hits[3][5], fwd=2.2), S.snd('chop'),
          fx('dust_ring', [part('minecraft:poof', 1.2, 0.05, 1.2, 0.02, 14)], AT_BODY + ' positioned ^ ^0.1 ^2', r=30),
          EDGE_BACK)
    dv.to(dend, 'ld')
    ld = sm.st('ld')
    ld.at(0, api.play('land'))
    sm.end('ld', lend)
    if K.prop('crescent_v_1'):
        W.w('p/w2/resume', ['# W2 resume: the crescent looks again (kit cards may have been cleared on pause).']
            + [f'execute if score #el {OBJ} matches {e} as @e[type=minecraft:item_display,tag=rlk_tk_p_w2,tag=rlk_tk_pj] run '
               f'{K.prop(f"crescent_v_{e}")}' for e in (1, 3)])
    sm.write()
    return sm


# ------------------------------------------------------------------------------------------------- L 착지 공격
L_HOVER = (80, 120)
L_FOLLOW = 0.15
L_GLINT_EVERY = 30
L_INV = 8                       # rlk_mb_inv from this tick of the leap (>= 4 b up) until the dive starts
L_CUE = 6                       # the last glint + the dive cry this many ticks before the dive (dive cue -> impact 16 t)


def build_l(W):
    key = 'l'
    sm = SM(key, W)
    gone_high = E('leap_high', 'gone_high')
    impact, dlen = E('dive', 'impact'), api.CLIPS['dive'][0]
    shock = impact + E('l_shock', 'shock')                    # dive + 20
    sl_end = impact + E('l_shock', 'end')
    sm.start = [sm.go('up')]
    # 1 up: leap high (+13 b, HIGH_Y), invulnerable from the lift until the dive
    up = sm.st('up')
    up.at(0, FACE, api.play('leap_high'), snd('leap'), wing_fx(),
          fx('dust_ring', [part('minecraft:poof', 1.0, 0.05, 1.0, 0.02, 14)], 'at @s positioned ~ ~0.1 ~', r=20))
    up.at(4, f'execute at @s positioned ~ {num(api.HIGH_Y)} ~ run function rlk:mboss/mv/glide {{t:{gone_high - 4}}}')
    up.at(L_INV, 'tag @s add rlk_mb_inv')
    up.to(gone_high, 'hv')
    # 2 hv: the small glinting silhouette follows the player (0.15 b/t), glints every 30 t, 80-120 t; the dive cue 6 t
    # before the dive
    hv = sm.st('hv')
    hv.at(0, api.play('hover_high'), f'execute store result score #l_h {OBJ} run random value {L_HOVER[0]}..{L_HOVER[1]}',
          f'scoreboard players operation #l_q {OBJ} = #l_h {OBJ}', f'scoreboard players remove #l_q {OBJ} {L_CUE}',
          sset('#l_g', L_GLINT_EVERY))
    glint = fx('high_glint', [part(WHITE, 0.2, 0.2, 0.2, 0.05, 8), part(GOLD, 0.3, 0.3, 0.3, 0, 6)],
               AT_BODY + ' positioned ~ ~1.4 ~') + snd('high_glint')
    W.w('p/l/glint', ['# L high glint (@s = body).'] + glint)
    hv.every(fn('p/l/follow'), turn(10), f'scoreboard players remove #l_g {OBJ} 1',
             f'execute if score #l_g {OBJ} matches ..0 run {fn("p/l/glint_t")}')
    W.w('p/l/glint_t', [sset('#l_g', L_GLINT_EVERY), f'execute if score #l_c {OBJ} < #l_q {OBJ} run {fn("p/l/glint")}'])
    hv.tail(f'execute if score #l_c {OBJ} = #l_q {OBJ} run {fn("p/l/cue")}',
            f'execute if score #l_c {OBJ} >= #l_h {OBJ} run return run {sm.go("dv")}')
    W.w('p/l/cue', ['# The dive cue (@s = body): the last big glint and the cry; the spot locks at the dive start.',
                    fn('p/l/glint')] + snd('air_swoop'))
    W.w('p/l/follow', [
        f'# L hover (@s = body at HIGH_Y): {L_FOLLOW} b/t toward the player\'s x / z while the floor spot below passes mv/ok.',
        f'execute at {PL} positioned ~ {num(api.HIGH_Y)} ~ if entity @s[distance=..{num(L_FOLLOW + 0.05)}] run return 0',
        f'execute at @s positioned ~ {CY} ~ facing entity {PL} feet rotated ~ 0 positioned ^ ^ ^{num(L_FOLLOW)} '
        f'if {OK} positioned ~ {num(api.HIGH_Y)} ~ run tp @s ~ ~ ~'])
    # 3 dv: the dive to the spot locked now (12 t visible streak, lands at its impact: disc 1.4 T2 Electro), l_shock
    # from the impact: the shock disc 5.5 T4 Electro at dive + 20
    dv = sm.st('dv')
    hits = api.HITS[key]
    lock = m1('rlk_tk_llock')
    dv.at(0, lock_lines(key, 'rlk_tk_llock'), 'tag @s remove rlk_mb_inv', api.play('dive'), face_to('rlk_tk_llock'),
          f'execute positioned as {lock} run function rlk:mboss/mv/glide {{t:{impact}}}', snd('dive'))
    if not K.p('thrust_trail', len=10, el=3):
        dv.rng(1, impact, f'execute at @s run {part(WHITE, 0.2, 0.6, 0.2, 0.02, 4)}')
    dv.at(impact - 1, hazard(key, hits[0], pos=f'at {lock}'))
    dv.at(impact, api.play('l_shock'), fx('impact', [part('minecraft:explosion', 0.3, 0.1, 0.3, 0, 2)], f'at {lock}', el=3),
          fx('dust_ring', [part('minecraft:poof', 1.2, 0.05, 1.2, 0.03, 16)], f'at {lock} positioned ~ ~0.1 ~', r=20),
          S.snd('chop'))
    dv.rng(impact + 1, shock - 1, f'execute at @s run {part(SPARK, 0.6, 0.9, 0.6, 0.1, 3)}')
    dv.at(shock - 1, hazard(key, hits[1], pos=f'at {lock}'))
    dv.at(shock, fx('bolt', [part(SPARK, 1.5, 2.0, 1.5, 0.3, 40)], f'at {lock}'),
          fx('shock_ring', [part(GOLD, 2.8, 0.1, 2.8, 0, 50)], f'at {lock} positioned ~ ~0.1 ~', r=55), snd('shock'))
    dv.at(sl_end, 'kill @e[type=minecraft:marker,tag=rlk_tk_llock]')
    sm.end('dv', sl_end)
    assert dlen >= impact
    sm.write()
    return sm


BUILT = {}


def _mk(key, f):
    def build(W):
        BUILT[key] = f(W)
    return build


PATTERNS = [
    api.Pattern('k', S.TID['k'], ('blink_out', 'blink_in', 'k_hold', 'k_glint', 'k_leap', 'k_plunge'), _mk('k', build_k),
                notes='vanish 24 t, reappear 4.5 b in front, hold, glint -> thrust, leap, sky arcs -> plunge; P3 K2'),
    api.Pattern('w1', S.TID['w1'], ('backstep', 'blink_out', 'blink_in', 'w1_wave'), _mk('w1', build_w1),
                notes='blink to >= 12 b first if nearer; 40 t charge (G3 6..39), three crescents re-aimed'),
    api.Pattern('w2', S.TID['w2'], ('leap_up', 'w2_air', 'w2_dive', 'land'), _mk('w2', build_w2),
                notes='hover at HOVER_Y, three vertical crescents, pull back, dive <= 14 b, big arc'),
    api.Pattern('l', S.TID['l'], ('leap_high', 'hover_high', 'dive', 'l_shock'), _mk('l', build_l),
                notes='high hover (invulnerable) following the player, dive to the locked spot, impact + shock'),
]
assert [p.key for p in PATTERNS] == list(api.AIR)
