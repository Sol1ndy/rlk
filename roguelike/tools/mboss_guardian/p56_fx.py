"""Helpers of the P5 / P6 / fail-spear module (p56.py). Owner: the P5/P6 pattern author.

Not a pattern module (it is not in PATTERN_MODULES); p56.py imports it. Plain Python, stdlib only.

    TL         per-tick timeline of one pattern: lines grouped into p/<key>/k/<t>, reached through a
               small binary dispatch tree on #gdPT (a tick runs a handful of score tests, not every line)
    geometry   n3/fl/loc, vectors, quaternions, display transformation SNBT
    cubes      irregular tumbling block_display cubes (mixed sizes, tilts, colours, drift, timing)
    bars       thin block_display bars on an arc or a ring (the fly-slam ring rim, the sweep crescent slabs)
    rhombus    a flat block_display diamond (the arms of the fail-spear star decal)

Every entity these helpers summon carries rlk_room, rlk_mb_aux and the pattern tag
rlk_mb_gd_p<id>, so the pattern's cancel removes it by tag.
"""
import math
import random

from .api import NS


# ---------------------------------------------------------------------------------------------
# numbers and geometry
def n3(v):
    s = f'{v:.3f}'.rstrip('0').rstrip('.')
    return '0' if s in ('-0', '') else s


def fl(v):
    return n3(v) + 'f'


def loc(p, dy=0.0):
    """anchor-frame point (x = her left, y up, z forward) -> local coordinates ^x ^y ^z."""
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


def polar(deg, r, y=0.0):
    """Anchor-frame point at angle deg (0 = forward, + = her left) and radius r."""
    a = math.radians(deg)
    return (r * math.sin(a), y, r * math.cos(a))


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


QI = (0.0, 0.0, 0.0, 1.0)


def tf(tr, lq, sc, rq=QI):
    """Display transformation SNBT."""
    return (f'{{translation:[{",".join(fl(v) for v in tr)}],left_rotation:[{",".join(fl(v) for v in lq)}],'
            f'scale:[{",".join(fl(v) for v in sc)}],right_rotation:[{",".join(fl(v) for v in rq)}]}}')


def tags(*names):
    return '[' + ','.join(f'"{t}"' for t in names) + ']'


def base_tags(pid, *more):
    return ('rlk_room', 'rlk_mb_aux', f'rlk_mb_gd_p{pid}') + more


# ---------------------------------------------------------------------------------------------
class TL:
    """Per-tick timeline of one pattern (clock #gdPT = clip tick)."""

    def __init__(self, g, key):
        self.g, self.key, self.ev = g, key, {}

    def at(self, t, *lines):
        for line in lines:
            if not line:
                continue
            if isinstance(line, (list, tuple)):
                self.at(t, *line)
                continue
            self.ev.setdefault(int(t), []).append(line)

    def span(self, t0, t1, *lines, step=1):
        for t in range(t0, t1 + 1, step):
            self.at(t, *lines)

    def fn(self, rel):
        return f'function {NS}p/{self.key}/{rel}'

    def _node(self, ts):
        if len(ts) <= 6:
            return [f'execute if score #gdPT mb matches {t} run return run {self.fn(f"k/{t}")}' for t in ts]
        mid = len(ts) // 2
        out = []
        for part in (ts[:mid], ts[mid:]):
            name = f'd/{part[0]}_{part[-1]}'
            self.g.pw(self.key, name, [f'# dispatch #gdPT {part[0]}..{part[-1]}'] + self._node(part))
            out.append(f'execute if score #gdPT mb matches {part[0]}..{part[-1]} run return run {self.fn(name)}')
        return out

    def write(self, start_head, tick_head, tick_tail=()):
        for t, lines in sorted(self.ev.items()):
            if t >= 1:
                self.g.pw(self.key, f'k/{t}', [f'# {self.key} clip tick {t}'] + lines)
        self.g.pw(self.key, 'start', list(start_head) + self.ev.get(0, []))
        ts = sorted(t for t in self.ev if t >= 1)
        body = self._node(ts)
        if tick_tail:
            # the tail must run every tick: the dispatch lines 'return run', so wrap them
            self.g.pw(self.key, 'kd', ['# per-tick dispatch'] + body)
            self.g.pw(self.key, 'tick', list(tick_head) + [self.fn('kd')] + list(tick_tail))
        else:
            self.g.pw(self.key, 'tick', list(tick_head) + body)


# ---------------------------------------------------------------------------------------------
# irregular tumbling cubes: block_display cubes that drift, tumble and shrink (one interpolation)
CUBE_BLOCK = {'gold': 'minecraft:yellow_stained_glass', 'goldb': 'minecraft:gold_block',
              'amber': 'minecraft:orange_stained_glass', 'dark': 'minecraft:black_concrete',
              'rock': 'minecraft:brown_terracotta', 'red': 'minecraft:red_stained_glass',
              'crimson': 'minecraft:red_concrete', 'brown': 'minecraft:black_terracotta',
              'ice': 'minecraft:light_blue_stained_glass', 'blue': 'minecraft:blue_stained_glass',
              'violet': 'minecraft:magenta_stained_glass', 'white': 'minecraft:white_stained_glass',
              'pyro': 'minecraft:orange_stained_glass', 'hydro': 'minecraft:light_blue_stained_glass',
              'cryo': 'minecraft:white_stained_glass', 'electro': 'minecraft:purple_stained_glass'}
GLOWING = ('gold', 'goldb', 'amber', 'red', 'ice', 'blue', 'violet', 'white', 'pyro', 'hydro', 'cryo', 'electro')


def cube_set(seed, n, mix, spread, size, drift, up=0.2, dirv=None, delay=0):
    """Deterministic but irregular cube specs (plan.md feedback: mixed sizes and tilts, uneven gaps,
    varied colours, no lockstep). mix = kinds drawn at random; spread = (x, y, z) half box of the spawn
    offsets; size = (lo, hi) blocks; drift = (lo, hi) blocks with an upward bias; dirv = optional
    preferred drift direction (anchor frame); delay = max random spawn delay in ticks."""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        kind = rnd.choice(mix)
        off = tuple(rnd.uniform(-s, s) for s in spread)
        s = rnd.uniform(*size) * (rnd.uniform(0.55, 0.8) if kind in ('goldb', 'crimson') else 1.0)
        a = rnd.uniform(0, 2 * math.pi)
        e = rnd.uniform(-0.3, 0.9)
        d = (math.cos(a) * math.cos(e), math.sin(e) + up, math.sin(a) * math.cos(e))
        if dirv is not None:
            d = add(mul(unit(dirv), 1.4), d)
        dv = mul(unit(d), rnd.uniform(*drift))
        q0 = qaxis((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)), rnd.uniform(0, 180))
        q1 = qmul(qaxis((rnd.uniform(-1, 1), rnd.uniform(-1, 1), rnd.uniform(-1, 1)), rnd.uniform(100, 175)), q0)
        out.append(dict(kind=kind, off=off, s=s, drift=dv, q0=q0, q1=q1, dt=rnd.randint(0, delay),
                        life_k=rnd.uniform(0.75, 1.15)))
    return out


def cubes(tl, pid, name, t, specs, anchor, life, cond=''):
    """Spawn specs from clip tick t (each at t + its random delay; anchor = execute prefix that ends at
    the anchor point and rotation), drift from the next tick, kill each at its own end. The drift is
    in world axes (the displays are unrotated), so it is yaw-independent noise."""
    tag_all, tag_set = f'rlk_mb_gd_p{pid}', f'rlk_mb_gd_q{name}'
    pre = (cond + ' ') if cond else ''
    for k, c in enumerate(specs):
        s = c['s']
        t0 = mul(qrot(c['q0'], (s / 2, s / 2, s / 2)), -1)
        s1 = s * 0.1
        t1 = add(c['drift'], mul(qrot(c['q1'], (s1 / 2, s1 / 2, s1 / 2)), -1))
        br = '{sky:15,block:15}' if c['kind'] in GLOWING else '{sky:11,block:11}'
        nbt = (f'{{Tags:{tags("rlk_room", "rlk_mb_aux", tag_all, tag_set, f"{tag_set}_{k}")},'
               f'block_state:{{id:"{CUBE_BLOCK[c["kind"]]}"}},brightness:{br},view_range:0.7f,shadow_radius:0f,'
               f'teleport_duration:0,interpolation_duration:0,transformation:{tf(t0, c["q0"], (s, s, s))}}}')
        ts = t + c['dt']
        lf = max(3, int(round(life * c['life_k'])))
        tl.at(ts, f'execute {pre}{anchor} positioned {loc(c["off"])} run summon minecraft:block_display ~ ~ ~ {nbt}')
        tl.at(ts + 1, f'execute as @e[type=minecraft:block_display,tag={tag_set}_{k},limit=1] run data merge entity @s '
                      f'{{start_interpolation:0,interpolation_duration:{lf},transformation:{tf(t1, c["q1"], (s1, s1, s1))}}}')
        tl.at(ts + 1 + lf, f'kill @e[type=minecraft:block_display,tag={tag_set}_{k}]')


# ---------------------------------------------------------------------------------------------
# floor bars (the P5 ring rim, the sweep slabs)
def bar_tf(theta, r, ln, w, h, y):
    """A bar tangent to the circle of radius r at angle theta (0 = forward, + = her left), centred on
    it radially; ln along the tangent, w radial width, h height, bottom at y."""
    q = qaxis((0, 1, 0), theta)
    tr = qrot(q, (-ln / 2, y, r - w / 2))
    return tr, q, (ln, h, w)


def bd(block, tr, q, sc, tagl, bright=15, extra=''):
    """summon line of a block_display bar (run it positioned at the anchor; rotate afterwards)."""
    return (f'summon minecraft:block_display ~ ~ ~ {{Tags:{tags(*tagl)},block_state:{{id:"{block}"}},'
            f'brightness:{{sky:{bright},block:{bright}}},view_range:1.6f,shadow_radius:0f,teleport_duration:0,'
            f'interpolation_duration:0{extra},transformation:{tf(tr, q, sc)}}}')


# ---------------------------------------------------------------------------------------------
# flat rhombus (one arm pair of a concave 4-point star)
R45 = qaxis((0, 1, 0), 45)
H = 0.70710678


def rhombus_tf(yaw, half_len, half_w, h, y, centre=(0.0, 0.0)):
    """A flat diamond centred at (centre x, y, centre z) of the anchor frame, its long axis along yaw
    (0 = forward), tips at +-half_len, widest (+-half_w) at the centre: unit cube turned 45 deg about Y
    (right_rotation), scaled, then turned to yaw (left_rotation)."""
    L = qaxis((0, 1, 0), yaw)
    S = (half_w / H, h, half_len / H)
    c = qrot(R45, (0.5, 0.5, 0.5))
    c = (c[0] * S[0], c[1] * S[1], c[2] * S[2])
    c = qrot(L, c)
    tr = (centre[0] - c[0], y - c[1], centre[1] - c[2])
    return tr, L, S, R45


def rhombus_edges(yaw, half_len, half_w, n):
    """n points per edge along the 4 edges of the rhombus (anchor frame, y = 0)."""
    L = qaxis((0, 1, 0), yaw)
    tips = [(0, 0, half_len), (half_w, 0, 0), (0, 0, -half_len), (-half_w, 0, 0)]
    tips = [qrot(L, p) for p in tips]
    pts = []
    for a, b in zip(tips, tips[1:] + tips[:1]):
        for k in range(n):
            pts.append(lerp(a, b, (k + 0.5) / n))
    return pts
