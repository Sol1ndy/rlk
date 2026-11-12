"""P1 공간 찌르기 (two thrusts) and P2 공간 투창 – 심판하는 파수꾼 (javelin).

Sources: patterns.md §3-§4, m1.md 0-9.5 s, plan.md K2/K4/K16/K17/K23, critic C23. Clips `thrust`
(79 t) and `javelin` (67 t), both played with ~25 % shorter wind-ups (guardian_clips.mjs RETIME; the
authored source ticks of the fx below go through api.rt); every hit lands on the clip's event tick, >= 10 t
after a readable tell of the clip (12 t for thrust 2). Hit areas are x1.2 the source sizes (user tuning, plan.md).

P1 공간 찌르기  (melee / mid; played ticks, authored ones in brackets)
  0-10   wind-up, she tracks the player; a gold lightning streak grows along the shaft from 3 and
         reaches past the blade by 11 (#FCF5AE / #CDB37E / #9D8650); rising shimmer from 5.
  11 [16] aim locked on the player (T): she stops turning. The 9.3 x 2.9 b lane starts at her coil spot
         C, 7.5 b behind T on the line T -> her, so after the 3 b lunge the rig's spear tip (4.46 b
         ahead of her at the hit) lands on T. She turns 5.7 deg left so the tip, held right of her
         centre line, runs down the lane.
  14     white-gold glint at the tip; 15-16 lens streak through the spear.
  15-19  coil: she drifts back to C;  19 -> 21 lunge 3 b;  21 [28] HIT 1 (100 %): burst sphere r 1.8,
         shock ring, gold / dark cubes, rock debris.
  31-33  she rises (rig) and backs off;  34 the second aim is locked on the player (U) and she flies
         to D, 6.6 b from U and 75 deg round it (the other side if that is outside the arena), so
         the second thrust comes from a new direction (PDF "전방위", C23), facing U while she glides.
         An 8.4 x 2.7 b lane from D through U strikes 12 t later.
  40-43  dive charge;  44 -> 46 dash 6 b along the lane;  46 [58] HIT 2 (115 %, knockback 4 along
         the lane, K16); the dive streak lingers to 52.  53 landing, 60-74 flourish and twirl, 79 idle.

P2 공간 투창  (mid / far)
  0-8    spear spin with a gold trail (the rig spins it 4-8), whooshes at 0 and 4; 9 the spear
         vanishes in a gold slash flash.
  10-19  the glyph: a gold concave 4-point star (1.2 -> 0.55 b, spinning) at her right-front, chest
         height (L), compressing into a spinning ring 16-20; glittery chimes.
  17 [24] aim locked (K23 + K4: 10 t before the hit, 3 t before the beam): she stops turning; a 1.2 b
         lane from L to the arena edge strikes 10 t later.
  20     vertical white-gold beam through the glyph (the last tell before the throw) and a larger re-flash.
  22     the spear re-forms in her raised hand;  26 release: white-gold explosion at L, launch disc
         facing the lane, the attack line (voice/attack).
  27 [36] HIT (130 %, resolved over 27-28): the lane strikes at once; the visual spear (rig
         prop/spear) flies down it at 5 b/t, harmless, with a gold streak, tumbling gold / dark cubes
         and rock debris; it stops at the wall and waits.
  49     it flies back butt first to her hand (50-52), stands up and is caught overhead at 54 (the rig
         spear returns); 57-61 twirl, 67 idle.

Telegraph rule (10-20, plan.md): the footage shows no ground marker before these hits (m1 0.20-3.15 s:
the streak on the spear, the glint, the hover and dive; m1 6.00-7.65 s: the air glyph, the vertical beam,
the launch disc), so the three lanes have no ground telegraph: quiet hazards (#hzQuiet 1: no framework
outline, no strike flash) and no module decal. The player reads the wind-up pose and its sounds, the
streak and glint on the spear (P1), the rise and the glide to the dive spot (P1 thrust 2), the glyph and
the beam in the air (P2); each hit shows its area with its own impact fx (hit_fx, the dive streak, the
javelin's lane streak and debris).
Spear-relative fx use p12_spear.json (the rig's spear grip / tip / butt per clip tick, measured by
p12_measure.py from the rig generator's --debug-dp poses).

Owner of this file: the P1/P2 pattern author. Writes only F:mboss/guardian/p/thrust/** and
F:mboss/guardian/p/javelin/** through gen.pw. Entities carry rlk_room, rlk_mb_aux and
rlk_mb_gd_p1 / rlk_mb_gd_p2 (cancel kills by that tag); fake players are #gp1* / #gp2*.
"""
import json
import math
import random
from pathlib import Path

from .api import (Pattern, ev, clip_len, rt, DMG, KB, CY, NS, GOLD, GOLD_DEEP, GOLD_PALE, CRIMSON, CRIMSON_DARK,
                  RED_EDGE)

PATTERNS = [
    # melee weight 2 against P4's 1 there (P4 hops back first; plan.md "P4 for melee players")
    Pattern(1, 'thrust', '공간 찌르기', bands=('melee', 'mid'), weight={'melee': 2}, recover=18, max_len=clip_len('thrust') + 4),
    Pattern(2, 'javelin', '공간 투창', bands=('mid', 'far'), recover=20, max_len=clip_len('javelin') + 4),
]

SPEAR = json.loads((Path(__file__).resolve().parent / 'p12_spear.json').read_text(encoding='utf-8'))

# Geo palette of the patterns (m1 §5): streak core / mid / edge, cubes, trail.
STREAK = ((0.988, 0.961, 0.682), (0.804, 0.702, 0.494), (0.616, 0.525, 0.314))     # #FCF5AE #CDB37E #9D8650
TRAIL = ((0.992, 0.957, 0.584), (0.780, 0.675, 0.341), (0.624, 0.478, 0.196))      # #FDF495 #C7AC57 #9F7A32
GLYPH = ((0.969, 0.918, 0.663), (0.667, 0.608, 0.345))                             # #F7EAA9 #AA9B58
WHITE = (1.0, 1.0, 0.99)
DARK = (0.23, 0.15, 0.13)                                                          # #3A2620

SAFE_R = 18.5            # mv/ok: the body stays inside this disc around the arena axis
WALK_R = 21              # the javelin lane runs to this radius (the wall ring starts at 22)
# User tuning (plan.md "공격 선딜 좀 짧게 하고 공격 범위를 좀 늘려봐"): the clips play with ~25 % shorter wind-ups
# (guardian_clips.mjs RETIME; authored ticks below go through rt()) and every hit area is ~20 % larger.
TELL1, TELL2, TELL_JAV = 10, 12, 10     # aim lock -> hit (were 12, 16, 12; floor 10 t); no ground telegraph (10-20)
AREA = 1.2              # linear scale of the hit areas and their impact fx
TIP_R = 1.8             # the burst sphere at the spear tip past the target (was 1.5)
JAV_W = 1.2             # javelin lane width (was 1.0; the framework's lane widths are whole tenths)

BODY = 'at @s rotated as @s rotated ~ 0'


# ---------------------------------------------------------------------------------------------
# small helpers
def n3(v):
    s = f'{v:.3f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def fl(v):
    return n3(v) + 'f'


def loc(p, dy=0.0):
    """rig/anchor point (x left, y up, z forward) -> local coordinates ^x ^y ^z."""
    return f'^{n3(p[0])} ^{n3(p[1] + dy)} ^{n3(p[2])}'


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x - y for x, y in zip(a, b))


def mul(a, k):
    return tuple(x * k for x in a)


def lerp(a, b, s):
    return tuple(x + (y - x) * s for x, y in zip(a, b))


def length(a):
    return math.sqrt(sum(x * x for x in a))


def unit(a):
    d = length(a) or 1.0
    return mul(a, 1.0 / d)


def sp(clip, t, part='tip'):
    row = SPEAR[clip][t]
    return tuple(row[part]) if row else None


def qaxis(axis, deg):
    ax = unit(axis)
    h = math.radians(deg) / 2
    s = math.sin(h)
    return (ax[0] * s, ax[1] * s, ax[2] * s, math.cos(h))


def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by,
            aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw,
            aw * bw - ax * bx - ay * by - az * bz)


def qrot(q, v):
    x, y, z, w = q
    ix = w * v[0] + y * v[2] - z * v[1]
    iy = w * v[1] + z * v[0] - x * v[2]
    iz = w * v[2] + x * v[1] - y * v[0]
    iw = -x * v[0] - y * v[1] - z * v[2]
    return (ix * w + iw * -x + iy * -z - iz * -y,
            iy * w + iw * -y + iz * -x - ix * -z,
            iz * w + iw * -z + ix * -y - iy * -x)


def tf(tr, lq, sc):
    """Display transformation SNBT (right_rotation = identity)."""
    return (f'{{translation:[{",".join(fl(v) for v in tr)}],left_rotation:[{",".join(fl(v) for v in lq)}],'
            f'scale:[{",".join(fl(v) for v in sc)}],right_rotation:[0f,0f,0f,1f]}}')


def tags(*names):
    return '[' + ','.join(f'"{t}"' for t in names) + ']'


class TL:
    """Per-tick timeline of one pattern: lines are grouped into p/<key>/k/<t> and reached through a
    small binary dispatch tree on #gdPT, so a tick runs a handful of score tests, not every line."""

    def __init__(self, g, key):
        self.g, self.key, self.ev = g, key, {}

    def at(self, t, *lines):
        for line in lines:
            if line:
                self.ev.setdefault(int(t), []).append(line)

    def span(self, t0, t1, *lines):
        for t in range(t0, t1 + 1):
            self.at(t, *lines)

    def fn(self, rel):
        return f'function {NS}p/{self.key}/{rel}'

    def _node(self, ts):
        if len(ts) <= 6:
            return [f'execute if score #gdPT mb matches {t} run return run {self.fn(f"k/{t}")}' for t in ts]
        mid = len(ts) // 2
        a, b = ts[:mid], ts[mid:]
        out = []
        for part in (a, b):
            name = f'd/{part[0]}_{part[-1]}'
            self.g.pw(self.key, name, [f'# dispatch #gdPT {part[0]}..{part[-1]}'] + self._node(part))
            out.append(f'execute if score #gdPT mb matches {part[0]}..{part[-1]} run return run {self.fn(name)}')
        return out

    def write(self, start_head, tick_head):
        for t, lines in sorted(self.ev.items()):
            if t >= 1:
                self.g.pw(self.key, f'k/{t}', [f'# {self.key} clip tick {t}'] + lines)
        self.g.pw(self.key, 'start', start_head + self.ev.get(0, []))
        ts = sorted(t for t in self.ev if t >= 1)
        self.g.pw(self.key, 'tick', tick_head + self._node(ts))


# ---------------------------------------------------------------------------------------------
# tumbling cubes: block_display cubes that drift, tumble and shrink (one interpolation), then die
CUBE_BLOCK = {'gold': 'minecraft:yellow_stained_glass', 'goldb': 'minecraft:gold_block',
              'dark': 'minecraft:black_concrete', 'rock': 'minecraft:brown_terracotta',
              'red': 'minecraft:red_stained_glass'}


def cube_set(seed, n, mix, spread, size, drift, up=0.2, along=None):
    """Deterministic cube specs. mix = list of kinds cycled; spread = (x, y, z) half box of the spawn
    offsets (local frame); size = (lo, hi); drift = (lo, hi) blocks, isotropic with an upward bias.
    along = (z0, z1): spread the cubes along local z (javelin trail)."""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        kind = mix[k % len(mix)]
        if along:
            z = along[0] + (along[1] - along[0]) * (k + rnd.random() * 0.6) / n
        else:
            z = rnd.uniform(-spread[2], spread[2])
        off = (rnd.uniform(-spread[0], spread[0]), rnd.uniform(-spread[1], spread[1]), z)
        s = rnd.uniform(*size) * (0.6 if kind in ('goldb', 'red') else 1.0)
        a = rnd.uniform(0, 2 * math.pi)
        e = rnd.uniform(-0.3, 0.8)
        d = (math.cos(a) * math.cos(e), math.sin(e) + up, math.sin(a) * math.cos(e))
        dv = mul(unit(d), rnd.uniform(*drift))
        q0 = qaxis((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)), rnd.uniform(0, 180))
        q1 = qmul(qaxis((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)), rnd.uniform(110, 175)), q0)
        out.append(dict(kind=kind, off=off, s=s, drift=dv, q0=q0, q1=q1))
    return out


def cubes(tl, pid, name, t, cubes_spec, anchor, life, cond=None):
    """Spawn cubes_spec at clip tick t (anchor = execute prefix that ends at the anchor point and
    rotation), start their drift at t+1, kill them at t+1+life. cond(spec) -> optional execute
    prefix (e.g. a lane-length test)."""
    tag_all, tag_set = f'rlk_mb_gd_p{pid}', f'rlk_mb_gd_q{name}'
    for k, c in enumerate(cubes_spec):
        s = c['s']
        half = (s / 2, s / 2, s / 2)
        t0 = mul(qrot(c['q0'], half), -1)
        s1 = s * 0.12
        t1 = add(c['drift'], mul(qrot(c['q1'], (s1 / 2, s1 / 2, s1 / 2)), -1))
        bright = '{sky:15,block:15}' if c['kind'] in ('gold', 'goldb', 'red') else '{sky:12,block:12}'
        nbt = (f'{{Tags:{tags("rlk_room", "rlk_mb_aux", tag_all, tag_set, f"{tag_set}_{k}")},'
               f'block_state:{{id:"{CUBE_BLOCK[c["kind"]]}"}},brightness:{bright},view_range:0.6f,shadow_radius:0f,'
               f'teleport_duration:0,interpolation_duration:0,transformation:{tf(t0, c["q0"], (s, s, s))}}}')
        pre = (cond(c) + ' ') if cond else ''
        tl.at(t, f'execute {pre}{anchor} positioned {loc(c["off"])} run summon minecraft:block_display ~ ~ ~ {nbt}')
        tl.at(t + 1, f'data merge entity @e[type=minecraft:block_display,tag={tag_set}_{k},limit=1] '
                     f'{{start_interpolation:0,interpolation_duration:{life},transformation:{tf(t1, c["q1"], (s1, s1, s1))}}}')
    tl.at(t + 1 + life, f'kill @e[type=minecraft:block_display,tag={tag_set}]')


# ---------------------------------------------------------------------------------------------
def emit(g):
    thrust(g)
    javelin(g)


def streak_points(g0, x, f, k_n, rnd, jit):
    pts = []
    for k in range(k_n):
        s = f * (k + 0.5) / k_n
        p = lerp(g0, x, s)
        pts.append(add(p, (rnd.uniform(-jit, jit), rnd.uniform(-jit, jit), rnd.uniform(-jit, jit))))
    return pts


def thrust(g):
    k, pid = 'thrust', 1
    tl = TL(g, k)
    h1, h2 = ev(k, 'hit1'), ev(k, 'hit2')
    rise, dive, land, flo = ev(k, 'rise'), ev(k, 'dive'), ev(k, 'land'), ev(k, 'flourish')
    lock1, lock2 = h1 - TELL1, h2 - TELL2                 # K4 (tuned): aim locks 10 t and 12 t before the hits
    end = clip_len(k)
    tip1, tip2 = sp(k, h1), sp(k, h2)
    yaw1 = math.degrees(math.atan2(tip1[0], tip1[2]))     # turn so the off-centre tip runs down the lane
    yaw2 = math.degrees(math.atan2(tip2[0], tip2[2]))
    lunge = 3.0                                           # m1: 2-3 b at 27-28 (x1.2: 2.5 -> 3.0)
    reach1 = lunge + math.hypot(tip1[0], tip1[2])         # coil spot -> tip on the target
    lane1 = (round(reach1 + TIP_R, 1), 2.9)               # tip sphere r 1.8 (patterns.md §3: 1.5), width 2.4 -> 2.9
    dive_r, dash, side = 6.6, 6.0, 75                     # D 6.6 b from U, 75 deg round it; 6 b dash (x1.2)
    lane2 = (round(dive_r + TIP_R, 1), 2.7)               # dash path + sphere r 1.8 at its end, width 2.2 -> 2.7
    M = '@e[type=minecraft:marker,tag={},limit=1]'
    T, C, U, D = (M.format(f'rlk_mb_gd_p1{c}') for c in 'tcud')
    BODYSEL = '@e[type=minecraft:husk,tag=rlk_mb_body,limit=1]'
    mk = lambda c: f'{{Tags:{tags("rlk_room", "rlk_mb_aux", "rlk_mb_gd_p1", f"rlk_mb_gd_p1{c}")}}}'

    # -- wind-up and charge streak (0-16): she tracks the player until the lock
    tl.span(1, lock1 - 1, g.rig('face/track'))
    tl.at(0, g.sound('entity.player.attack.sweep', 0.35, 1.25), g.sound('item.trident.riptide_1', 0.3, 1.5))
    rnd = random.Random(11)
    for t in range(ev(k, 'glow'), lock1 + 1):
        gp, tp_ = sp(k, t, 'grip'), sp(k, t)
        x = add(tp_, mul(sub(tp_, gp), 0.7))              # the streak runs on past the blade
        f = (t - ev(k, 'glow') + 1) / (lock1 - ev(k, 'glow') + 1)
        for j, p in enumerate(streak_points(gp, x, f, 6, rnd, 0.09)):
            col = STREAK[0] if j % 2 else STREAK[1]
            tl.at(t, f'execute {BODY} positioned {loc(p)} run ' + g.dust_fade(col, STREAK[2], 0.9, '~ ~ ~', (0.03, 0.03, 0.03), 1))
        lead = lerp(gp, x, f)
        if t % 2 == 0:
            tl.at(t, f'execute {BODY} positioned {loc(lead)} run ' + g.particle('end_rod', '~ ~ ~', (0.03, 0.03, 0.03), 0.01, 1))
        tl.at(t, f'execute {BODY} positioned {loc(tp_)} run ' + g.dust(GOLD_PALE, 0.5, '~ ~ ~', (0.12, 0.12, 0.12), 2))
    tl.at(rt(k, 7), g.sound('block.beacon.power_select', 0.35, 1.6))
    for t, p in ((9, 1.5), (12, 1.7), (15, 1.9)):
        tl.at(rt(k, t), g.sound('block.amethyst_block.chime', 0.6, p))
    tl.at(rt(k, 15), g.sound('block.beacon.power_select', 0.25, 2.0))

    # -- lock 1 (16): target T, coil spot C behind her on the line T -> her, lane C -> T, her yaw
    tl.at(lock1, g.fn('p/thrust/lock1'))
    g.pw(k, 'lock1', [
        f'# @s = body (clip tick {lock1}). T = the player now; C = {n3(reach1)} b from T toward her (clamped into',
        f'# the arena) = where she coils; a {lane1[0]} x {lane1[1]} b lane from C through T strikes at clip tick {h1} (quiet:',
        '# no ground telegraph, rule 10-20; she stops tracking now and the spear streak, glint and coil are the tell).',
        'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p1]',
        f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {mk("t")}',
        f'execute at {T} facing entity @s feet rotated ~ 0 positioned ^ ^ ^{n3(reach1)} run summon minecraft:marker ~ {CY} ~ {mk("c")}',
        f'execute as {C} run function rlk:mboss/mv/clamp',
        f'execute as {C} at @s facing entity {T} feet run tp @s ~ ~ ~ ~ 0',
        *g.hz_opts(sfx=0, quiet=1, linger=4, kb=KB['default']),
        f'execute at {C} rotated as {C} run ' + g.hz_line(lane1[0], lane1[1], h1 - lock1, DMG['p1a']),
        f'execute rotated as {C} run tp @s ~ ~ ~ ~{n3(yaw1)} 0'])

    # -- glint (19), lens streak (20-21)
    gl = sp(k, ev(k, 'glint'))
    tl.at(ev(k, 'glint'),
          f'execute {BODY} run ' + g.card('star', loc(gl), bb='center', spin=45, s0=0.3, s1=1.6, life=6, fade=3),
          f'execute {BODY} run ' + g.card('glow', loc(gl), bb='center', s0=0.5, s1=1.3, life=5, fade=3),
          f'execute {BODY} positioned {loc(gl)} run ' + g.particle('end_rod', '~ ~ ~', (0.1, 0.1, 0.1), 0.06, 8),
          g.sound('block.amethyst_block.chime', 1.0, 2.0),
          g.sound('block.amethyst_cluster.hit', 0.5, 1.8))
    glint = ev(k, 'glint')
    for t, dens in ((glint + 1, 1.0), (glint + 2, 0.5)):
        gp, tp_ = sp(k, t, 'grip'), sp(k, t)
        u = unit(sub(tp_, gp))
        a, b = sub(gp, mul(u, 1.6)), add(tp_, mul(u, 2.6))
        npts = int(length(sub(b, a)) / 0.35 * dens)
        for j in range(npts + 1):
            p = lerp(a, b, j / npts)
            tl.at(t, f'execute {BODY} positioned {loc(p)} run ' + g.dust(WHITE if j % 3 else GOLD_PALE, 0.55, '~ ~ ~', (0, 0, 0), 1))
    tl.at(glint + 1, g.sound('item.trident.riptide_1', 0.35, 1.8))

    # -- coil (authored 21-26): drift back to C; tip trail; lunge into the hit (3 b along the lane, 2 t)
    coil = rt(k, 20)
    tl.at(coil, f'execute positioned as {C} run function rlk:mboss/mv/glide {{t:{h1 - 2 - coil}}}')
    for t in range(rt(k, 22), h1 + 1):
        a, b = sp(k, t - 1), sp(k, t)
        for s in (0.33, 0.66, 1.0):
            tl.at(t, f'execute {BODY} positioned {loc(lerp(a, b, s))} run ' + g.dust(TRAIL[0], 0.9, '~ ~ ~', (0.03, 0.03, 0.03), 1))
    tl.at(h1 - 2, f'execute at {C} rotated as {C} positioned ^ ^ ^{n3(lunge)} run function rlk:mboss/mv/glide {{t:2}}',
          g.sound('entity.player.attack.sweep', 0.7, 0.9))

    # -- hit 1 (28): burst sphere at the tip, shock ring facing the lane, cubes, debris
    burst1 = add(tip1, (0, 0.9, 0))
    tl.at(h1, *hit_fx(g, burst1),
          f'execute {BODY} positioned {loc(tip1, 0.15)} run ' + g.particle('block{block_state:"minecraft:gold_block"}', '~ ~ ~', (0.9 * AREA, 0.1, 0.9 * AREA), 0, 18),
          f'execute {BODY} positioned {loc(tip1, 0.15)} run ' + g.particle('block{block_state:"minecraft:polished_blackstone"}', '~ ~ ~', (0.8 * AREA, 0.1, 0.8 * AREA), 0, 10),
          g.sound('item.trident.hit', 1.0, 0.8),
          g.sound('block.amethyst_cluster.break', 0.9, 1.0),
          g.sound('entity.generic.explode', 0.4, 1.6))
    cubes(tl, pid, '1a', h1, cube_set(101, 10, ['gold', 'dark', 'gold', 'rock', 'goldb', 'gold', 'dark', 'red', 'gold', 'rock'],
                                       (0.6, 0.5, 0.6), (0.32, 0.55), (1.1 * AREA, 2.2 * AREA)), f'{BODY} positioned {loc(burst1)}', 14)
    tl.span(h1 + 1, h1 + 6, f'execute {BODY} positioned {loc(burst1)} run ' + g.dust(GOLD, 1.0, '~ ~ ~', (0.7 * AREA, 0.6, 0.7 * AREA), 2))

    # -- rise and back off (38-41), lock 2 (42): U, dive spot D 75 deg round U, lane D -> U
    tl.at(rise, g.sound('entity.phantom.flap', 0.55, 0.75), g.sound('item.trident.riptide_1', 0.25, 1.2))
    tl.span(rise, lock2 - 1, 'function rlk:mboss/mv/away {d:0.4}')
    tl.at(lock2, g.fn('p/thrust/lock2'))
    g.pw(k, 'lock2', [
        f'# @s = body (clip tick {lock2}). U = the player now; D = {dive_r} b from U, {side} deg round it from her side',
        f'# (random side, the other one when outside the arena, then clamped); a {lane2[0]} x {lane2[1]} b lane from D',
        f'# through U strikes at {h2} (knockback {KB["p1b"]} along it; quiet, no ground telegraph); she flies to D over',
        f'# {dive - lock2} t facing U.',
        f'kill {U}', f'kill {D}',
        f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {mk("u")}',
        'execute store result score #gp1S mb run random value 0..1',
        f'execute if score #gp1S mb matches 0 at {U} facing entity @s feet rotated ~{side} 0 positioned ^ ^ ^{dive_r} run summon minecraft:marker ~ {CY} ~ {mk("d")}',
        f'execute if score #gp1S mb matches 1 at {U} facing entity @s feet rotated ~-{side} 0 positioned ^ ^ ^{dive_r} run summon minecraft:marker ~ {CY} ~ {mk("d")}',
        f'execute as {D} at @s unless entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..{SAFE_R}] run function {NS}p/thrust/flip',
        f'execute as {D} run function rlk:mboss/mv/clamp',
        f'execute as {D} at @s facing entity {U} feet run tp @s ~ ~ ~ ~ 0',
        *g.hz_opts(sfx=0, quiet=1, linger=4, kb=KB['p1b']),
        f'execute at {D} rotated as {D} run ' + g.hz_line(lane2[0], lane2[1], h2 - lock2, DMG['p1b']),
        f'execute positioned as {D} run function rlk:mboss/mv/glide {{t:{dive - lock2}}}'])
    g.pw(k, 'flip', [
        '# @s = the dive marker D, outside the arena: the other side of U.',
        f'execute if score #gp1S mb matches 0 at {U} facing entity {BODYSEL} feet rotated ~-{side} 0 positioned ^ ^ ^{dive_r} run tp @s ~ {CY} ~',
        f'execute if score #gp1S mb matches 1 at {U} facing entity {BODYSEL} feet rotated ~{side} 0 positioned ^ ^ ^{dive_r} run tp @s ~ {CY} ~'])
    tl.span(lock2, dive - 1, f'execute at @s facing entity {U} feet run tp @s ~ ~ ~ ~ 0')
    tl.at(rt(k, 46), g.sound('entity.phantom.flap', 0.45, 0.8))
    tl.at(dive, f'execute rotated as {D} run tp @s ~ ~ ~ ~{n3(yaw2)} 0')
    tl.at(rt(k, 50), g.sound('block.beacon.power_select', 0.3, 1.9))
    # dive charge along the spear (it points down at the player)
    for t in range(rt(k, 50), h2):
        gp, tp_ = sp(k, t, 'grip'), sp(k, t)
        for s in (0.45, 0.75, 1.0):
            tl.at(t, f'execute {BODY} positioned {loc(lerp(gp, tp_, s))} run ' + g.dust(STREAK[0], 0.7, '~ ~ ~', (0.04, 0.04, 0.04), 1))
    tl.at(h2 - 2, f'execute at {D} rotated as {D} positioned ^ ^ ^{n3(dash)} run function rlk:mboss/mv/glide {{t:2}}',
          g.sound('entity.player.attack.sweep', 0.85, 0.7), g.sound('item.trident.riptide_1', 0.4, 1.2))

    # -- the dive streak (57-58) from D's height down to the impact, lingering to 64
    a, b = (0.0, 3.5, 0.0), (0.0, 0.9, dash + 1.2)
    npts = 22
    for t, s_max in ((h2 - 1, 0.55), (h2, 1.0)):
        for j in range(int(npts * s_max) + 1):
            p = lerp(a, b, j / npts)
            tl.at(t, f'execute at {D} rotated as {D} positioned {loc(p)} run ' + g.dust(TRAIL[0], 1.6, '~ ~ ~', (0.12, 0.12, 0.12), 2))
            if j % 3 == 0:
                tl.at(t, f'execute at {D} rotated as {D} positioned {loc(p)} run ' + g.particle('end_rod', '~ ~ ~', (0.1, 0.1, 0.1), 0.02, 1))
    for t in range(h2 + 1, h2 + 7, 2):
        for j in range(0, npts + 1, 2):
            p = lerp(a, b, j / npts)
            tl.at(t, f'execute at {D} rotated as {D} positioned {loc(p)} run ' + g.dust_fade(TRAIL[1], TRAIL[2], 1.1, '~ ~ ~', (0.08, 0.08, 0.08), 1))

    # -- hit 2 (58): impact flare at the end of the dash, cubes, debris
    burst2 = (0.0, 1.1, 1.2)
    tl.at(h2, *hit_fx(g, burst2, big=True),
          f'execute {BODY} positioned ^ ^0.15 ^1.2 run ' + g.particle('block{block_state:"minecraft:gold_block"}', '~ ~ ~', (1.0 * AREA, 0.1, 1.0 * AREA), 0, 22),
          f'execute {BODY} positioned ^ ^0.15 ^1.2 run ' + g.particle('block{block_state:"minecraft:polished_blackstone"}', '~ ~ ~', (0.9 * AREA, 0.1, 0.9 * AREA), 0, 12),
          g.sound('item.trident.hit', 1.0, 0.75),
          g.sound('block.amethyst_cluster.break', 1.0, 0.9),
          g.sound('entity.generic.explode', 0.5, 1.5))
    cubes(tl, pid, '1b', h2, cube_set(202, 10, ['gold', 'rock', 'gold', 'dark', 'gold', 'goldb', 'rock', 'gold', 'red', 'dark'],
                                       (0.7, 0.5, 0.7), (0.32, 0.6), (1.2 * AREA, 2.4 * AREA)), f'{BODY} positioned {loc(burst2)}', 14)

    # -- landing (65), flourish (72-86): glint at the raised tip, twirl whooshes
    tl.at(land, g.sound('block.amethyst_block.fall', 0.6, 0.7),
          f'execute {BODY} run ' + g.particle('block{block_state:"minecraft:calcite"}', '^ ^0.1 ^0.6', (0.5, 0.05, 0.5), 0, 8))
    glf = sp(k, flo)
    tl.at(flo, f'execute {BODY} run ' + g.card('star', loc(glf), bb='center', spin=60, s0=0.2, s1=1.1, life=6, fade=3),
          g.sound('block.amethyst_block.chime', 0.7, 1.9))
    for t in (67, 74, 78, 82, 86):
        tl.at(rt(k, t), g.sound('item.trident.riptide_1', 0.3, 1.4), g.sound('entity.player.attack.sweep', 0.45, 0.7))
    for t in range(flo + 1, rt(k, 86)):
        tl.at(t, f'execute {BODY} positioned {loc(sp(k, t))} run ' + g.dust(GOLD_PALE, 0.6, '~ ~ ~', (0.03, 0.03, 0.03), 1))
    tl.at(end, 'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p1]', g.end())

    tl.write([
        f'# P1 공간 찌르기 start (@s = body, #gdPT 0). Clip thrust ({end} t): glow 4, glint 19, hit1 {h1}, rise 38,',
        f'# dive 54, hit2 {h2}, land 65, flourish 72. Lanes (quiet, no ground telegraph): {lane1[0]} x {lane1[1]} b locked at',
        f'# {lock1} (hit {h1 - lock1} t later), {lane2[0]} x {lane2[1]} b locked at {lock2} (hit {h2 - lock2} t later); damage {DMG["p1a"]} % /',
        f'# {DMG["p1b"]} % (KB {KB["p1b"]}).',
        'kill @e[tag=rlk_mb_gd_p1]',
        g.rig('face/player'),
        g.play(k)], [
        '# P1 tick (@s = body, at it, #gdPT = clip tick 1..): per-tick lines in p/thrust/k/<t>.'])
    g.pw(k, 'cancel', [
        '# P1 cancel (any executor): markers and cubes by tag; a glide of the body stops.',
        'kill @e[tag=rlk_mb_gd_p1]',
        'execute as @e[type=minecraft:husk,tag=rlk_mb_body,tag=rlk_mb_mv] run function rlk:mboss/mv/stop',
        'scoreboard players set #gp1S mb 0'])


def hit_fx(g, centre, big=False):
    """Burst sphere (~3.6 b = the tip sphere r 1.8), soft glow, shock ring facing her aim, sparks (body frame, at the
    hit); x AREA over the source sizes (burst 3 b, ring 3.5 b)."""
    c = loc(centre)
    k = (1.15 if big else 1.0) * AREA
    return [
        f'execute {BODY} run ' + g.card('burst', c, bb='center', spin=20, s0=0.6, s1=3.0 * k, life=6, fade=3),
        f'execute {BODY} run ' + g.card('glow', c, bb='center', s0=1.0, s1=2.6 * k, life=7, fade=4),
        f'execute {BODY} run ' + g.card('ring', c, rot='~ 0', spin=40, s0=0.8, s1=3.5 * k, life=7, fade=3),
        f'execute {BODY} positioned {c} run ' + g.dust(GOLD, 1.6, '~ ~ ~', (0.8 * k, 0.7, 0.8 * k), 24),
        f'execute {BODY} positioned {c} run ' + g.dust(WHITE, 1.2, '~ ~ ~', (0.4 * k, 0.4, 0.4 * k), 10),
        f'execute {BODY} positioned {c} run ' + g.particle('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.18, 12)]


# ---------------------------------------------------------------------------------------------
def javelin(g):
    k, pid = 'javelin', 2
    tl = TL(g, k)
    vanish, glyph, beam = ev(k, 'vanish'), ev(k, 'glyph'), ev(k, 'beam')
    remat, rel, launch = ev(k, 'rematerialise'), ev(k, 'release'), ev(k, 'launch')
    ret, catch, end = ev(k, 'return'), ev(k, 'catch'), clip_len(k)
    lock = launch - TELL_JAV                              # K4 floor (tuned 10 t); the beam stays the last flash
    L2 = (-0.9, 1.5, 1.2)                                 # glyph / launch point: right-front, chest height
    M = '@e[type=minecraft:marker,tag={},limit=1]'
    T, A = M.format('rlk_mb_gd_p2t'), M.format('rlk_mb_gd_p2a')
    PROP = '@e[type=minecraft:item_display,tag=rlk_mb_gd_p2s,limit=1]'
    AT_A = f'at {A} rotated as {A}'
    mk = lambda c: f'{{Tags:{tags("rlk_room", "rlk_mb_aux", "rlk_mb_gd_p2", f"rlk_mb_gd_p2{c}")}}}'

    tl.span(1, lock - 1, g.rig('face/track'))
    # -- spin with a gold trail (0-9), whooshes at 0 and 5, vanish flash at 10
    tl.at(0, g.sound('entity.player.attack.sweep', 0.7, 0.7), g.sound('item.trident.riptide_1', 0.4, 1.4))
    tl.at(rt(k, 5), g.sound('entity.player.attack.sweep', 0.7, 0.8), g.sound('item.trident.riptide_1', 0.3, 1.5))
    for t in range(1, vanish):
        a, b = sp(k, t - 1), sp(k, t)
        if not a or not b:
            continue
        for s in (0.25, 0.5, 0.75, 1.0):
            p = lerp(a, b, s)
            tl.at(t, f'execute {BODY} positioned {loc(p)} run ' + g.dust(TRAIL[0] if s < 1 else GOLD_PALE, 1.0, '~ ~ ~', (0.04, 0.04, 0.04), 1))
        mid = lerp(sp(k, t, 'grip'), b, 0.6)
        tl.at(t, f'execute {BODY} positioned {loc(mid)} run ' + g.dust(TRAIL[1], 0.7, '~ ~ ~', (0.05, 0.05, 0.05), 1))
    last = sp(k, vanish - 1)
    tl.at(vanish,
          f'execute {BODY} run ' + g.card('crescent', '^-0.8 ^0.9 ^0.9', rot='~ 0', roll=-20, spin=60, s0=1.6, s1=2.5, life=5, fade=2),
          f'execute {BODY} positioned {loc(last)} run ' + g.dust(GOLD_PALE, 0.9, '~ ~ ~', (0.5, 0.3, 0.5), 12),
          f'execute {BODY} positioned {loc(last)} run ' + g.particle('end_rod', '~ ~ ~', (0.3, 0.2, 0.3), 0.04, 5),
          g.sound('entity.player.attack.sweep', 0.5, 1.2), g.sound('block.amethyst_block.break', 0.5, 1.4))

    # -- glyph (11-27): spinning, shrinking 4-point star at L, then a spinning ring (22-27)
    Lp = loc(L2)
    tl.at(glyph, f'execute {BODY} run ' + g.card('star', Lp, bb='center', spin=170, s0=1.6, s1=0.75, life=lock - glyph + 1, fade=2),
          f'execute {BODY} run ' + g.card('glow', Lp, bb='center', s0=0.6, s1=1.4, life=lock - glyph, fade=4),
          g.sound('block.amethyst_block.resonate', 0.8, 1.3))
    tl.at(rt(k, 22), f'execute {BODY} run ' + g.card('ring', Lp, bb='center', spin=-170, s0=1.0, s1=0.6, life=beam - rt(k, 22), fade=2))
    for t in range(glyph, beam, 2):
        tl.at(t, f'execute {BODY} positioned {Lp} run ' + g.dust(GLYPH[0], 0.55, '~ ~ ~', (0.35, 0.35, 0.35), 3))
    for t in range(glyph + 1, beam, 4):
        tl.at(t, f'execute {BODY} positioned {Lp} run ' + g.particle('end_rod', '~ ~ ~', (0.25, 0.25, 0.25), 0.01, 1))
    for t, p in ((20, 1.7), (22, 1.8), (24, 1.9), (26, 2.0)):
        tl.at(rt(k, t), g.sound('block.amethyst_block.chime', 0.5, p))

    # -- lock (24): target T, launch marker A at L aimed at T, lane A -> arena edge
    tl.at(lock, g.fn('p/javelin/lock'))
    buckets = [f'execute if score #gp2Len mb matches {v} {AT_A} positioned ~ {CY} ~ run function rlk:mboss/hz/line '
               f'{{len:{v},w:{round(JAV_W * 10)},tell:{launch - lock},dmg:{DMG["p2"]}}}' for v in range(20, 441, 10)]
    g.pw(k, 'lock', [
        f'# @s = body (clip tick {lock}). T = the player now; she faces it; A = the glyph point {Lp} aimed at T',
        f'# (pitch 0). A {JAV_W:g} b lane from A to the arena edge (r {WALK_R}) strikes at {launch} for 2 t (K23; quiet,',
        '# no ground telegraph: the glyph and the beam in the air are the tell).',
        'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p2]',
        f'execute at @e[tag=rlk_body,limit=1] run summon minecraft:marker ~ {CY} ~ {mk("t")}',
        f'execute at @s facing entity {T} feet run tp @s ~ ~ ~ ~ 0',
        f'execute {BODY} positioned {Lp} run summon minecraft:marker ~ ~ ~ {mk("a")}',
        f'execute as {A} at @s facing entity {T} feet run tp @s ~ ~ ~ ~ 0',
        'scoreboard players set #gp2Len mb 0',
        f'execute {AT_A} positioned ~ {CY} ~ run function {NS}p/javelin/edge',
        '# whole blocks (the hazard, the streak and the debris use the same length), 2..44 b',
        'scoreboard players add #gp2Len mb 5', 'scoreboard players operation #gp2Len mb /= #c10 mb',
        'scoreboard players operation #gp2Len mb *= #c10 mb',
        'execute if score #gp2Len mb matches ..19 run scoreboard players set #gp2Len mb 20',
        'execute if score #gp2Len mb matches 441.. run scoreboard players set #gp2Len mb 440',
        *g.hz_opts(sfx=0, quiet=1, linger=4, act=2, kb=KB['light']),
        *buckets,
        'function rlk:mboss/opts_reset'])
    g.pw(k, 'edge', [
        '# Positioned on the floor, rotated = the lane: #gp2Len += 0.5 b while the next point is inside the walk disc.',
        'scoreboard players add #gp2Len mb 5',
        'execute if score #gp2Len mb matches 440.. run return 0',
        f'execute positioned ^ ^ ^0.5 if entity @e[type=minecraft:marker,tag=rlk_mb_arena,distance=..{WALK_R}] run function {NS}p/javelin/edge'])

    # -- beam (28) and re-flash, rematerialise (31)
    tl.at(beam,
          f'execute {BODY} run ' + g.card('shard', f'^{n3(L2[0])} ^ ^{n3(L2[2])}', bb='vertical', s0=3.2, s1=3.6, life=3, fade=1),
          f'execute {BODY} run ' + g.card('star', Lp, bb='center', spin=90, s0=0.5, s1=1.6, life=4, fade=2),
          f'execute {BODY} positioned {Lp} run ' + g.dust(GOLD_PALE, 1.2, '~ ~ ~', (0.05, 1.3, 0.05), 24),
          f'execute {BODY} positioned {Lp} run ' + g.particle('end_rod', '~ ~ ~', (0.04, 1.4, 0.04), 0.0, 12),
          g.sound('block.beacon.activate', 0.7, 1.8))
    tl.at(beam + 3, f'execute {BODY} run ' + g.card('ring', Lp, bb='center', spin=120, s0=0.9, s1=0.5, life=4, fade=2))
    hand = sp(k, remat, 'grip')
    tl.at(remat, f'execute {BODY} run ' + g.card('glow', loc(hand), bb='center', s0=0.3, s1=1.2, life=5, fade=3),
          f'execute {BODY} positioned {loc(hand)} run ' + g.dust(GOLD, 0.9, '~ ~ ~', (0.3, 0.3, 0.3), 8),
          g.sound('block.amethyst_block.chime', 0.6, 1.2), g.sound('item.trident.riptide_1', 0.3, 1.6))
    cubes(tl, pid, '2h', remat, cube_set(303, 3, ['gold', 'goldb', 'gold'], (0.25, 0.25, 0.25), (0.18, 0.26), (0.4, 0.8)),
          f'{BODY} positioned {loc(hand)}', 8)
    for t in range(remat + 1, rel):
        tl.at(t, f'execute {BODY} positioned {loc(sp(k, t))} run ' + g.dust(GOLD_PALE, 0.6, '~ ~ ~', (0.05, 0.05, 0.05), 1))

    # -- release (35): explosion at L, launch disc facing the lane, the attack line
    tl.at(rel,
          f'execute {BODY} run ' + g.card('burst', Lp, bb='center', spin=25, s0=0.8, s1=2.4, life=5, fade=2),
          f'execute {BODY} run ' + g.card('glow', Lp, bb='center', s0=1.0, s1=2.8, life=6, fade=3),
          f'execute {AT_A} run ' + g.card('ring', '^ ^ ^0.2', rot='~ ~', spin=60, s0=1.0, s1=2.0, life=8, fade=3),
          f'execute {AT_A} run ' + g.card('glow', '^ ^ ^0.25', rot='~ ~', s0=0.8, s1=1.8, life=6, fade=3),
          f'execute {BODY} positioned {Lp} run ' + g.particle('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.2, 16),
          f'execute {BODY} positioned {Lp} run ' + g.dust(WHITE, 1.6, '~ ~ ~', (0.6, 0.6, 0.6), 18),
          g.voice_attack(),
          g.sound('item.trident.throw', 1.0, 0.7),
          g.sound('entity.firework_rocket.blast', 0.9, 1.2))

    # -- launch (36): the visual spear, the streak along the lane, cubes, debris (37)
    tl.at(launch, g.fn('p/javelin/throw'), g.sound('item.trident.riptide_2', 0.6, 1.0),
          'scoreboard players set #gp2S mb 0', f'execute {AT_A} run function {NS}p/javelin/streak')
    tl.at(launch + 1, 'scoreboard players set #gp2S mb 0', f'execute {AT_A} run function {NS}p/javelin/streak',
          'scoreboard players set #gp2S mb 0', f'execute {AT_A} positioned ~ {CY} ~ run function {NS}p/javelin/debris',
          g.sound('block.amethyst_cluster.break', 0.5, 1.2))
    for t in range(launch + 2, launch + 8, 2):
        tl.at(t, 'scoreboard players set #gp2S mb 0', f'execute {AT_A} run function {NS}p/javelin/trail')
    g.pw(k, 'throw', [
        '# @s = body: the visual spear (rig prop/spear, tip turned forward) at L flies down the lane at 5 b/t,',
        '# harmless (dmg 0, K23: the lane is the damage), stops at the wall and is kept (pj_end) until the return.',
        f'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s]',
        f'execute {AT_A} run ' + g.rig('prop/spear'),
        'tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p2',
        'tag @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] add rlk_mb_gd_p2s',
        'data merge entity @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] '
        '{transformation:{translation:[0f,0f,0f],left_rotation:[0.7071f,0f,0f,0.7071f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]}}',
        'scoreboard players set @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] mbId 2',
        '# flight time = the lane length at 5 b/t (the wall check stays on)',
        *[f'execute if score #gp2Len mb matches {50 * (n - 1) + 1}..{50 * n} as @e[type=minecraft:item_display,tag=rlk_mb_gd_prop_new,limit=1] '
          f'at @s run function rlk:mboss/pj/launch {{spd:50,life:{n},dmg:0,hr:5}}' for n in range(1, 10)]])
    g.pw(k, 'pj_end', [
        '# @s = the javelin prop (#pjEv 1 wall / 2 life over): keep it where it stopped until the return (58).',
        'scoreboard players set #pjKeep mb 1',
        'execute at @s run ' + g.particle('block{block_state:"minecraft:gold_block"}', '^ ^ ^2', (0.3, 0.3, 0.3), 0, 10),
        'execute at @s run ' + g.particle('end_rod', '^ ^ ^2', (0.2, 0.2, 0.2), 0.05, 4),
        'execute at @s run ' + g.sound('item.trident.hit_ground', 0.7, 0.9)])
    g.pw(k, 'streak', [
        '# @s = body, at A rotated along the lane: the hot streak, a step every 0.5 b up to #gp2Len.',
        g.dust(TRAIL[0], 1.8, '~ ~ ~', (0.06, 0.06, 0.12), 2),
        'scoreboard players operation #gp2M mb = #gp2S mb',
        'scoreboard players operation #gp2M mb %= #c10 mb',
        'execute if score #gp2M mb matches 0 run ' + g.particle('end_rod', '~ ~ ~', (0.05, 0.05, 0.1), 0.01, 1),
        'scoreboard players add #gp2S mb 5',
        f'execute if score #gp2S mb < #gp2Len mb positioned ^ ^ ^0.5 run function {NS}p/javelin/streak'])
    g.pw(k, 'trail', [
        '# @s = body, at A rotated along the lane: the fading trail, a step every 1 b.',
        g.dust_fade(TRAIL[1], TRAIL[2], 1.1, '~ ~ ~', (0.06, 0.06, 0.1), 1),
        'scoreboard players add #gp2S mb 10',
        f'execute if score #gp2S mb < #gp2Len mb positioned ^ ^ ^1 run function {NS}p/javelin/trail'])
    g.pw(k, 'debris', [
        '# @s = body, on the floor under the lane: rock and gold debris every 2 b.',
        g.particle('block{block_state:"minecraft:gold_block"}', '~ ~0.1 ~', (0.4, 0.05, 0.4), 0, 3),
        g.particle('block{block_state:"minecraft:polished_blackstone"}', '~ ~0.1 ~', (0.4, 0.05, 0.4), 0, 2),
        'scoreboard players add #gp2S mb 20',
        f'execute if score #gp2S mb < #gp2Len mb positioned ^ ^ ^2 run function {NS}p/javelin/debris'])
    trail_cubes = cube_set(404, 12, ['gold', 'dark', 'gold', 'goldb', 'rock', 'gold', 'gold', 'dark', 'gold', 'red', 'gold', 'rock'],
                           (0.7, 0.45, 0), (0.35, 0.7), (0.5, 1.3), up=0.5, along=(1.2, 15.0))
    cubes(tl, pid, '2t', launch, trail_cubes, AT_A, 18,
          cond=lambda c: f'if score #gp2Len mb matches {int(math.ceil(c["off"][2] * 10))}..')

    # -- waiting prop (40-57), return (58 -> 61), upright (61), catch (63), twirl
    for t in range(rt(k, 40), ret, 4):
        tl.at(t, f'execute as {PROP} at @s run ' + g.particle('end_rod', '~ ~ ~', (0.2, 0.2, 0.2), 0.01, 2))
    hand_r = (-0.36, 2.95, 0.25)                          # rig right hand at 58 (javelin key rw)
    tl.at(ret, f'execute {BODY} positioned {loc(hand_r)} as {PROP} run function rlk:mboss/mv/glide {{t:3}}',
          g.sound('item.trident.return', 0.8, 0.8))
    for t in range(ret + 1, ret + 4):
        tl.at(t, f'execute as {PROP} at @s run ' + g.dust(TRAIL[0], 1.1, '~ ~ ~', (0.1, 0.1, 0.1), 4),
              f'execute as {PROP} at @s run ' + g.particle('end_rod', '~ ~ ~', (0.05, 0.05, 0.05), 0.01, 1))
    tl.at(ret + 3, f'execute as {PROP} run data merge entity @s {{start_interpolation:0,interpolation_duration:2,'
                   'transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.2f,2.2f,2.2f],right_rotation:[0f,0f,0f,1f]}}')
    top = sp(k, catch)
    tl.at(catch, 'kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p2s]',
          f'execute {BODY} run ' + g.card('star', loc(top), bb='center', spin=45, s0=0.2, s1=1.0, life=5, fade=2),
          f'execute {BODY} positioned {loc(sp(k, catch, "grip"))} run ' + g.dust(GOLD, 1.0, '~ ~ ~', (0.25, 0.25, 0.25), 8),
          g.sound('entity.player.attack.sweep', 0.5, 0.6), g.sound('item.armor.equip_netherite', 0.4, 1.3))
    for t in (66, 70):
        tl.at(rt(k, t), g.sound('item.trident.riptide_1', 0.3, 1.4))
    tl.at(end, 'kill @e[type=minecraft:marker,tag=rlk_mb_gd_p2]', g.end())

    tl.write([
        f'# P2 공간 투창 start (@s = body, #gdPT 0). Clip javelin ({end} t): spin 0, vanish {vanish}, glyph {glyph},',
        f'# beam {beam}, rematerialise {remat}, release {rel}, launch {launch}, return {ret}, catch {catch}. Lane locked at {lock}',
        f'# (quiet, no ground telegraph; hit {launch - lock} t later), {JAV_W:g} b wide to the arena edge, {DMG["p2"]} % over {launch}-{launch + 1};',
        '# the flying spear is visual.',
        'kill @e[tag=rlk_mb_gd_p2]',
        g.rig('face/player'),
        g.play(k)], [
        '# P2 tick (@s = body, at it, #gdPT = clip tick 1..): per-tick lines in p/javelin/k/<t>.'])
    g.pw(k, 'cancel', [
        '# P2 cancel (any executor): the prop (also while it is a projectile), markers, cubes by tag.',
        'kill @e[tag=rlk_mb_gd_p2]',
        'scoreboard players set #gp2Len mb 0',
        'scoreboard players set #gp2S mb 0'])
