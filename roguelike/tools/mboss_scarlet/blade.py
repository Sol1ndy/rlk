"""The blade track of 홍련's fight clips and everything drawn from it (round V, lane VB; v_brief.md §3 VB 1-3).

tools/build_scarlet_rig.mjs writes tools/scarlet_blade_track.json: per fight / gauntlet clip tick the blade's base and tip
(and her chest, head, hat crown) in her own frame, [left, up, forward] blocks from her feet. That frame is the local frame of
a display entity standing at her feet with her yaw (+x left, +y up, +z forward), so a track point is a display translation
and `^left ^up ^forward` as it stands. From the track this module derives, per hit (clip, hit tick h):

  the swing    [a, b]: the ticks round h in which the tip travels >= V_SWING b / t (a = the wound pose, b = the follow-through's
               end, capped); the wind-up is `reached` at w = the first tick from which the blade stays within WIND_TOL of its
               pose at a (v_brief: w <= h - 10 for a single / first hit, <= h - 6 for a chain follow-up)
  the path     the tip's way from a to h as the client shows it (the blade's base moves in a line, its direction turns evenly
               between two ticks: the display interpolation), cut into straight pieces of <= PATH_STEP deg: the drawn blade path
               (the user's "laser pointer"), cards of kind sw_path, PATH_W wide, with a head (sw_head) that runs along it and
               arrives at the tip's place of tick h on tick h
  the slash    the surface the blade sweeps from a to b, one sector card (sw_arc_0..2) per <= ARC_STEP deg of turn, standing
               in the plane of the two blade positions that bound it, its rim on the tip's way: plane, direction, reach and timing
               are the blade's own. A piece is born on the pattern tick its sweep is shown and is gone ARC_LIFE t later.

Everything is literal commands on pattern ticks (the pattern clock #pt hr): nothing here runs on the game clock, so a clock that
is slowed or frozen (lane VP's hit-stop beat) keeps path, head and slash in step with the blade. Cards carry rlk_hr_sw + the
pattern's tags (its cancel kills them) + rlk_room + rlk_mb_aux.

Frames: RIDE = the cards stand at her feet and are teleported with her every tick (melee swings: the path stays on the blade
while she steps and turns); HERE = left where they were made (the slash pieces: the trail hangs in the air); a caller may give
another executor (a marker's place: the gauntlet stations, the dash / dive targets).
"""
import json
import math
from pathlib import Path

from . import api

TRACK_FILE = Path(__file__).resolve().parents[1] / 'scarlet_blade_track.json'
_TRACK = {}

# --- the rules (v_brief §3 VB; tests/test_blade.py reads them) -------------------------------------------------------------
V_SWING = 0.30            # b / t of the tip: a swing tick
SWING_BACK, SWING_ON = 7, 3   # at most this many ticks of swing before / after the hit tick
WIND_TOL = 0.42           # b: the blade's base and tip stay this near their pose at the swing's start = the wind-up is held
LEAD_FIRST, LEAD_CHAIN = 10, 6      # the wind-up is reached / the path shows this long before a single or first / a chain hit
SHOW_FIRST, SHOW_CHAIN = 12, 8      # what the generators aim for (never less than the rule; a chain: never before the hit before)
PATH_W = 0.24             # b: a path card's width (its bright core PATH_CORE x that; v_brief: >= 0.12 b)
PATH_CORE = 0.56
PATH_STEP = 30.0          # deg of blade turn per straight piece of the path
ARC_STEP = 45.0           # deg of blade turn per slash piece
ARC_LIFE = 6              # t: a slash piece is gone this long after it was born (v_brief: gone within ~6 t of the hit)
ARC_FRAMES = ((0, 'sw_arc_0'), (2, 'sw_arc_1'), (4, 'sw_arc_2'))    # the piece's fading frames (ticks after its birth)
ARC_TAN = 0.5             # the sector sprite: its edges run from the apex (a 0, b 0) to (a +-0.5, b 1) x 1 / sqrt(1.25)
ARC_INNER = 0.30          # the sprite fades out below this share of the radius
HEAD_S = 0.62             # b: the head card's size
MIN_THICK = 0.12          # b: v_brief's floor for any path / effect card
TAG, TAG_RIDE, TAG_HEAD, TAG_NEW = 'rlk_hr_sw', 'rlk_hr_swr', 'rlk_hr_swh', 'rlk_hr_swn'
KIT = api.RP_KIT          # rlk:mboss/hr_kit/
# colours (RGB ints, the sprites are white): the path of a parryable hit white-gold, an unparriable one its flash's colour
COL = {'P': 0xFFE9A8, 'yellow': 0xFFE14A, 'purple': 0xD68BFF, 'blue': 0x5AA8FF, 'flare': 0xFFFFFF}
SLASH = {api.C_LILAC: 0xE2B4FF, api.C_MAGENTA: 0xFF8AD8, api.C_YELLOW: 0xFFE98A, api.C_CRIMSON: 0xFF6A80, api.C_WHITE: 0xFFFFFF}


def track(clip):
    if not _TRACK:
        _TRACK.update(json.loads(TRACK_FILE.read_text(encoding='utf-8'))['clips'])
    return _TRACK[clip]


def have_track():
    return TRACK_FILE.exists()


# --- vectors -----------------------------------------------------------------------------------------------------------------
def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def add(a, b):
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def mul(a, k):
    return (a[0] * k, a[1] * k, a[2] * k)


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def norm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = norm(a)
    return mul(a, 1 / n) if n > 1e-9 else (0.0, 0.0, 1.0)


def lerp(a, b, u):
    return (a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] + (b[2] - a[2]) * u)


def angle(a, b):
    return math.degrees(math.acos(max(-1.0, min(1.0, dot(unit(a), unit(b))))))


def slerp(a, b, u):
    """unit vectors"""
    c = max(-1.0, min(1.0, dot(a, b)))
    th = math.acos(c)
    if th < 1e-4:
        return unit(lerp(a, b, u))
    if th > math.pi - 1e-3:                       # opposite: turn about any normal
        n = unit(cross(a, (0.0, 1.0, 0.0)) if abs(a[1]) < 0.9 else cross(a, (1.0, 0.0, 0.0)))
        b = unit(add(mul(a, math.cos(th)), mul(cross(n, a), math.sin(th))))
    s = math.sin(th)
    return add(mul(a, math.sin((1 - u) * th) / s), mul(b, math.sin(u * th) / s))


def quat(x, y, z):
    """The rotation whose matrix has the columns x, y, z (an orthonormal right-handed frame) as (qx, qy, qz, qw)."""
    m00, m10, m20 = x
    m01, m11, m21 = y
    m02, m12, m22 = z
    tr = m00 + m11 + m22
    if tr > 0:
        s = math.sqrt(tr + 1.0) * 2
        q = ((m21 - m12) / s, (m02 - m20) / s, (m10 - m01) / s, 0.25 * s)
    elif m00 > m11 and m00 > m22:
        s = math.sqrt(1.0 + m00 - m11 - m22) * 2
        q = (0.25 * s, (m01 + m10) / s, (m02 + m20) / s, (m21 - m12) / s)
    elif m11 > m22:
        s = math.sqrt(1.0 + m11 - m00 - m22) * 2
        q = ((m01 + m10) / s, 0.25 * s, (m12 + m21) / s, (m02 - m20) / s)
    else:
        s = math.sqrt(1.0 + m22 - m00 - m11) * 2
        q = ((m02 + m20) / s, (m12 + m21) / s, 0.25 * s, (m10 - m01) / s)
    if q[3] < 0:
        q = tuple(-v for v in q)
    return q


def frame_z(z, up=(0.0, 1.0, 0.0)):
    """A right-handed frame whose z is the unit vector z, its y as near `up` as it can be."""
    x = cross(up, z)
    if norm(x) < 1e-4:
        x = cross((0.0, 0.0, 1.0) if abs(z[2]) < 0.9 else (1.0, 0.0, 0.0), z)
    x = unit(x)
    return x, cross(z, x), z


# --- the swing -----------------------------------------------------------------------------------------------------------------
class Swing:
    """The blade round one hit of a clip (clip ticks)."""

    def __init__(self, clip, h, back=SWING_BACK, on=SWING_ON, a=None, b=None):
        tr = track(clip)
        self.clip, self.h = clip, h
        self.B = [tuple(p) for p in tr['b']]
        self.T = [tuple(p) for p in tr['t']]
        self.n = len(self.T) - 1
        sp = self.speed
        if a is None:
            a = h
            # (a hit whose own tick is already slow - the blade arrived a tick or two early: the swing is the run before it)
            while a > max(1, h - 3) and sp(a) < V_SWING:
                a -= 1
            while a > max(0, h - back) and sp(a) >= V_SWING:
                a -= 1
            a = min(a, h - 1)
        if b is None:
            b = h
            while b < min(self.n, h + on) and sp(b + 1) >= V_SWING:
                b += 1
        self.a, self.b = a, b
        w = a
        while w > 0 and math.dist(self.T[w - 1], self.T[a]) <= WIND_TOL and math.dist(self.B[w - 1], self.B[a]) <= WIND_TOL:
            w -= 1
        self.w = w

    def speed(self, t):
        return math.dist(self.T[t], self.T[t - 1]) if 0 < t <= self.n else 0.0

    def blade(self, u):
        """(base, tip) at the float tick u, as the client's display interpolation shows it between two ticks."""
        u = max(0.0, min(float(self.n), u))
        i = min(self.n - 1, int(math.floor(u)))
        f = u - i
        if f < 1e-9:
            return self.B[i], self.T[i]
        b = lerp(self.B[i], self.B[i + 1], f)
        d0, d1 = sub(self.T[i], self.B[i]), sub(self.T[i + 1], self.B[i + 1])
        d = slerp(unit(d0), unit(d1), f)
        return b, add(b, mul(d, norm(d0) + (norm(d1) - norm(d0)) * f))

    def steps(self, t0, t1, deg):
        """Float ticks from t0 to t1 with at most `deg` of blade turn (and 0.9 b of tip travel) between two of them."""
        out = [float(t0)]
        for i in range(t0, t1):
            d0, d1 = sub(self.T[i], self.B[i]), sub(self.T[i + 1], self.B[i + 1])
            n = max(1, math.ceil(angle(d0, d1) / deg - 1e-6), math.ceil(math.dist(self.T[i], self.T[i + 1]) / 0.9 - 1e-6))
            out += [i + (k + 1) / n for k in range(n)]
        return out

    def path(self, a=None, h=None):
        """The tip's way a .. h: [(float tick, point)]."""
        a, h = self.a if a is None else a, self.h if h is None else h
        return [(u, self.blade(u)[1]) for u in self.steps(a, h, PATH_STEP)]

    def pieces(self, a=None, b=None):
        """The slash a .. b: one piece per step of the blade's sweep: dict(t = the pattern-clock tick (clip ticks) it shows on,
        kind 'arc' (apex q, bisector z, normal n, half-angle beta deg, radius r, inner = the base's share of r) or 'line' (the
        blade moved along itself: p0 -> p1), u0, u1)."""
        a, b = self.a if a is None else a, self.b if b is None else b
        us = self.steps(a, b, ARC_STEP)
        out = []
        for u0, u1 in zip(us, us[1:]):
            b0, t0 = self.blade(u0)
            b1, t1 = self.blade(u1)
            d0, d1 = unit(sub(t0, b0)), unit(sub(t1, b1))
            born = int(math.ceil(u1 - 1e-9))
            phi = angle(d0, d1)
            n = cross(d0, d1)
            if phi < 5.0 or norm(n) < 1e-6:
                if math.dist(t0, t1) >= 0.25:
                    out.append(dict(t=born, kind='line', p0=t0, p1=t1, u0=u0, u1=u1))
                continue
            n = unit(n)
            # the apex: the point nearest both blade lines (the two lines' common perpendicular's middle)
            w0 = sub(b0, b1)
            bb, dd, ee = dot(d0, d1), dot(d0, w0), dot(d1, w0)
            den = 1 - bb * bb
            s0 = (bb * ee - dd) / den
            s1 = (ee - bb * dd) / den
            q = lerp(add(b0, mul(d0, s0)), add(b1, mul(d1, s1)), 0.5)
            r0, r1 = norm(sub(t0, q)), norm(sub(t1, q))
            # an apex beyond the tips or far behind the bases (the blade slid more than it turned): a band of the tip's way
            # (or the two radii differ: a thrust that turns a little)
            if min(dot(sub(t0, q), d0), dot(sub(t1, q), d1)) <= 0.3 or max(r0, r1) > 6.0 or abs(r0 - r1) > 0.22:
                out.append(dict(t=born, kind='line', p0=t0, p1=t1, u0=u0, u1=u1))
                continue
            z = unit(add(unit(sub(t0, q)), unit(sub(t1, q))))
            beta = angle(sub(t0, q), sub(t1, q)) / 2
            inner = (norm(sub(b0, q)) + norm(sub(b1, q))) / (r0 + r1)
            out.append(dict(t=born, kind='arc', q=q, z=z, n=n, beta=beta, r=(r0 + r1) / 2, inner=inner, u0=u0, u1=u1,
                            tips=(t0, t1), bases=(b0, b1)))
        return out


# a hit whose swing the rule of thumb misreads: a4's plunge is one whirl of the blade from the flip's first tick (the wind-up is
# the apex pose before it)
SWING_OPTS = {('a4', 'hit'): dict(back=9)}


def swing_of(clip, event, **kw):
    return Swing(clip, api.ev(clip, event), **{**SWING_OPTS.get((clip, event), {}), **kw})


# --- commands ------------------------------------------------------------------------------------------------------------------
def f4(v):
    s = f'{v:.4f}'.rstrip('0').rstrip('.')
    return ('0' if s in ('-0', '') else s) + 'f'


def car(p):
    """`^left ^up ^forward` of a track point"""
    def c(v):
        s = f'{v:.3f}'.rstrip('0').rstrip('.')
        return '^' + ('' if s in ('0', '-0') else s)
    return f'{c(p[0])} {c(p[1])} {c(p[2])}'


def _tags(key, *more):
    return '[' + ','.join(f'"{t}"' for t in (TAG, 'rlk_room', 'rlk_mb_aux', api.TAGS['pat'], f'rlk_hr_p_{key}') + more) + ']'


def card(key, kind, t, q, s, col, tags=(), bb='fixed', tpd=1):
    """One literal summon of a sweep card at the executor: translation t, left rotation q, scale s (the track frame)."""
    return ('summon minecraft:item_display ~ ~ ~ {Tags:' + _tags(key, TAG_NEW, *tags) + f',billboard:"{bb}",item_display:"none",'
            'brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
            f'teleport_duration:{int(tpd)},interpolation_duration:0,transformation:{{translation:[{",".join(f4(v) for v in t)}],'
            f'left_rotation:[{",".join(f4(v) for v in q)}],scale:[{",".join(f4(v) for v in s)}],right_rotation:[0f,0f,0f,1f]}},'
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}{kind}",'
            f'"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}}}')


SEL = '@e[type=minecraft:item_display,tag={}]'
AT_BODY = 'at @s'          # the frame of a card: her feet and yaw NOW (the body's place when the command runs, not the place the
#                            tick function was called at: a glide may have moved her since)


def place(at=AT_BODY):
    """The cards just summoned to the frame `at` (its place, its yaw, pitch 0)."""
    return [f'execute {at} run tp {SEL.format(TAG_NEW)} ~ ~ ~ ~ 0', f'tag {SEL.format(TAG_NEW)} remove {TAG_NEW}']


def ride_cmd(mine, at=AT_BODY):
    """Every tick while a path rides its frame."""
    return f'execute {at} run tp {SEL.format(mine)} ~ ~ ~ ~ 0'


def seg_card(key, p0, p1, col, tags, w=PATH_W, kind='sw_path'):
    d = sub(p1, p0)
    x, y, z = frame_z(unit(d))
    return card(key, kind, p0, quat(x, y, z), (w, w, norm(d)), col, tags)


def arc_card(key, pc, col, tags):
    """A slash piece (Swing.pieces row) as its card: the sector sprite's apex on q, its axis along z, lying in the plane with
    the normal n, squeezed to the half-angle beta, its rim at r on the two blade positions."""
    if pc['kind'] == 'line':
        return seg_card(key, pc['p0'], pc['p1'], col, tags, w=PATH_W * 1.5)
    k = math.tan(math.radians(pc['beta'])) / ARC_TAN
    sa, ca = ARC_TAN / math.sqrt(1 + ARC_TAN ** 2), 1 / math.sqrt(1 + ARC_TAN ** 2)
    s = pc['r'] / math.sqrt(k * k * sa * sa + ca * ca)
    z, y = pc['z'], pc['n']
    x = cross(y, z)
    return card(key, ARC_FRAMES[0][1], pc['q'], quat(x, y, z), (s * k, 1.0, s), col, tags, tpd=0)


def _gate(cond, cmd):
    return f'execute {cond} {cmd[8:]}' if cmd.startswith('execute ') else f'execute {cond} run {cmd}'


class Out:
    """tick -> commands (pattern ticks); merged into a pattern builder with .into(pb)."""

    def __init__(self):
        self.t = {}

    def at(self, t, *cmds):
        self.t.setdefault(int(t), []).extend(c for c in cmds if c)

    def into(self, pb, cond=None):
        """Merge into a pattern builder (cond: an execute condition put before every line)."""
        for t in sorted(self.t):
            pb.at(t, [_gate(cond, c) for c in self.t[t]] if cond else self.t[t])
        return self


def path_ride(out, key, sw, t0, show, col, uid, head=True, flare=True, at=AT_BODY):
    """The drawn blade path of swing sw (clip tick 0 = pattern tick t0), riding her, shown from pattern tick `show` (>= 0) to
    the hit; the head arrives at the tip's place of the hit tick on the hit tick; from the swing's start the path burns white
    (the tip's trail) and is gone ARC_LIFE - 2 t after the hit. uid: a short id unique in the pattern (the cards' own tag).
    Returns dict(show, hit, segs, first_head, pts)."""
    h, a = t0 + sw.h, t0 + sw.a
    show = max(0, min(show, a))
    pts = sw.path()
    mine = f'{TAG}_{uid}'
    sel = SEL.format(mine)
    cmds = [seg_card(key, p0, p1, col, (TAG_RIDE, mine)) for (_u0, p0), (_u1, p1) in zip(pts, pts[1:])]
    out.at(show, *cmds, *place(at))
    # the riding: from the tick after it is made until it is killed
    end = h + ARC_LIFE - 2
    for t in range(show + 1, end):
        out.at(t, ride_cmd(mine, at))
    if head:
        # the head: at pattern tick t it is sent to where it shall be at t + 1 (1 t of client interpolation): it reaches the hit
        # point as tick h is shown. It runs the whole path at an even pace.
        lens = [0.0]
        for (_u0, p0), (_u1, p1) in zip(pts, pts[1:]):
            lens.append(lens[-1] + math.dist(p0, p1))

        def at_len(s):
            for i in range(1, len(lens)):
                if s <= lens[i] or i == len(lens) - 1:
                    f = 0.0 if lens[i] == lens[i - 1] else (s - lens[i - 1]) / (lens[i] - lens[i - 1])
                    return lerp(pts[i - 1][1], pts[i][1], max(0.0, min(1.0, f)))
        hsel = f'@e[type=minecraft:item_display,tag={TAG_HEAD},tag={mine},limit=1]'
        n = max(1, h - show)
        out.at(show, 'summon minecraft:item_display ~ ~ ~ {Tags:' + _tags(key, TAG_HEAD, mine)
               + ',billboard:"center",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
               f'teleport_duration:1,interpolation_duration:0,transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
               f'scale:[{f4(HEAD_S)},{f4(HEAD_S)},{f4(HEAD_S)}],right_rotation:[0f,0f,0f,1f]}},'
               f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}sw_head",'
               f'"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}}}',
               f'execute {at} rotated ~ 0 run tp {hsel} {car(at_len(lens[-1] / n))}')
        for t in range(show + 1, h):
            out.at(t, f'execute {at} rotated ~ 0 run tp {hsel} {car(at_len(lens[-1] * (t + 1 - show) / n))}')
        out.at(h, f'kill {hsel}')
    if flare:
        out.at(max(show + 1, a + 1), f'execute as {sel} run data merge entity @s {{item:{{components:{{"minecraft:custom_model_data":{{colors:[{COL["flare"]}]}}}}}}}}')
    out.at(end, f'kill {sel}')
    return dict(show=show, hit=h, segs=len(cmds), pts=pts, uid=uid, end=end)


def slash(out, key, sw, t0, col, uid, a=None, b=None):
    """The slash of swing sw: its pieces, each born on the pattern tick its sweep is shown, left in the air where the blade
    was, fading through ARC_FRAMES and gone ARC_LIFE t after its birth. Returns the pieces (with their pattern ticks)."""
    pcs = sw.pieces(a, b)
    by = {}
    for pc in pcs:
        by.setdefault(t0 + pc['t'], []).append(pc)
    for t, row in sorted(by.items()):
        grp = f'{TAG}_{uid}_{t}'
        out.at(t, *[arc_card(key, pc, col, (grp,)) for pc in row], *place())
        sel = SEL.format(grp)
        for dt, frame in ARC_FRAMES[1:]:
            if any(pc['kind'] == 'arc' for pc in row):
                out.at(t + dt, f'execute as {sel} run data modify entity @s item.components."minecraft:item_model" set value "{KIT}{frame}"')
        out.at(t + ARC_LIFE, f'kill {sel}')
    return [dict(pc, pt=t0 + pc['t']) for pc in pcs]


# --- the target line: a dash's / a dive's way, known only in the game -------------------------------------------------------------
# Where her body carries the blade (a dash through the locked spot, a plunge onto it) the blade's way in the world is her own
# way: a straight line from her to the target. Its length is measured in the game (core/sw/march: 0.5 b steps from the line's
# start along its aim until the tagged target is reached), its head runs to the target and arrives on the hit tick. One such
# line lives at a time (TAG_LINE).
TAG_LINE, TAG_LHEAD, TAG_TGT = 'rlk_hr_swl', 'rlk_hr_swlh', 'rlk_hr_swt'
LINE_STEP, LINE_MAX = 0.5, 64
STO = f'{api.STORAGE} core.sw'
LINE_SEL = f'@e[type=minecraft:item_display,tag={TAG_LINE}]'
LHEAD_SEL = f'@e[type=minecraft:item_display,tag={TAG_LHEAD}]'


def runtime(W, fn, sset):
    """core/sw/{aim,march,head}: the run-time part of the target line (written once by p1.py)."""
    W.w('core/sw/aim', [
        '# {dy} The target line (blade.py; one at a time, rlk_hr_swl) to here, aimed as the executing rotation, as long as the way',
        f'# to the target (the entity tagged {TAG_TGT}; dy = its height below the line): core/sw/march counts {LINE_STEP} b steps.',
        f'tp {LINE_SEL} ~ ~ ~ ~ ~',
        sset('#sw_n', 0),
        f'$function {api.NS}core/sw/march {{dy:"$(dy)"}}',
        f'execute as {LINE_SEL} store result entity @s transformation.scale[2] float {LINE_STEP} run scoreboard players get #sw_n {api.OBJ}'])
    W.w('core/sw/march', [
        f'# {{dy}} One {LINE_STEP} b step of the target line\'s measure (at most {LINE_MAX}): stops within 0.45 b of the target.',
        f'execute if score #sw_n {api.OBJ} matches {LINE_MAX}.. run return 0',
        f'$execute positioned ~ ~$(dy) ~ if entity @e[tag={TAG_TGT},distance=..0.45] run return 0',
        f'scoreboard players add #sw_n {api.OBJ} 1',
        f'$execute positioned ^ ^ ^{LINE_STEP} run function {api.NS}core/sw/march {{dy:"$(dy)"}}'])
    W.w('core/sw/head', [
        '# {d} The target line\'s head to d blocks along the line (blade.py: d = the line\'s length x the share of the way it',
        '# shall have run one tick from now).',
        f'$execute at {LINE_SEL[:-1]},limit=1] run tp {LHEAD_SEL} ^ ^ ^$(d)'])


def target_line(out, key, show, lock, h, col, start, pre, post, dy='0', w=PATH_W):
    """The target line of a dash / dive hit (pattern ticks; @s = the body): shown from `show`, aimed every tick at `pre` (the
    player) until the lock, at `post` (the lock marker) from the lock tick on, the head arriving on h. start: execute
    subcommands that put the executing position on the line's start and the rotation on its aim, with {T} = the target
    selector. Returns dict(show, lock, hit)."""
    show = min(show, lock) if pre else lock
    tags = (TAG_LINE,)
    out.at(show, f'kill {LINE_SEL}', f'kill {LHEAD_SEL}',
           card(key, 'sw_path', (0, 0, 0), (0, 0, 0, 1), (w, w, 1.0), col, tags, tpd=0),
           'summon minecraft:item_display ~ ~ ~ {Tags:' + _tags(key, TAG_LHEAD)
           + ',billboard:"center",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
           f'teleport_duration:1,interpolation_duration:0,transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
           f'scale:[{f4(HEAD_S)},{f4(HEAD_S)},{f4(HEAD_S)}],right_rotation:[0f,0f,0f,1f]}},'
           f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}sw_head",'
           f'"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}}}',
           f'tag {SEL.format(TAG_NEW)} remove {TAG_NEW}')
    n = h - show
    for t in range(show, h):
        if t <= lock:
            tgt = post if t == lock else pre
            out.at(t, f'tag @e[tag={TAG_TGT}] remove {TAG_TGT}', f'tag {tgt} add {TAG_TGT}',
                   f'execute {start.replace("{T}", tgt)} run function {api.NS}core/sw/aim {{dy:"{dy}"}}',
                   f'tag @e[tag={TAG_TGT}] remove {TAG_TGT}')
        u = (t + 1 - show) / n
        out.at(t, f'execute store result storage {STO}.d double {f4(LINE_STEP * u)[:-1]} run scoreboard players get #sw_n {api.OBJ}',
               f'function {api.NS}core/sw/head with storage {STO}')
    out.at(h, f'kill {LHEAD_SEL}',
           f'execute as {LINE_SEL} run data merge entity @s {{item:{{components:{{"minecraft:custom_model_data":{{colors:[{COL["flare"]}]}}}}}}}}')
    out.at(h + 3, f'kill {LINE_SEL}')
    return dict(show=show, lock=lock, hit=h)


def static_line(out, key, uid, show, h, col, where, length, w=PATH_W, life=3):
    """A straight path card of a known length left in the world (kcut's crossing lines, nb's bands: through the locked spot):
    where = execute subcommands for its start and aim (the card runs `length` b along the executing rotation)."""
    mine = f'{TAG}_{uid}'
    sel = SEL.format(mine)
    out.at(show, f'execute {where} run ' + card(key, 'sw_path', (0, 0, 0), (0, 0, 0, 1), (w, w, length), col, (mine,), tpd=0),
           f'execute {where} run tp {SEL.format(TAG_NEW)} ~ ~ ~ ~ ~', f'tag {SEL.format(TAG_NEW)} remove {TAG_NEW}')
    out.at(h, f'execute as {sel} run data merge entity @s {{item:{{components:{{"minecraft:custom_model_data":{{colors:[{COL["flare"]}]}}}}}}}}')
    out.at(h + life, f'kill {sel}')
    return dict(show=show, hit=h, len=length)


# --- a hit of a pattern ---------------------------------------------------------------------------------------------------------
DRAWN = {}                # key -> [dict(kind 'ride' | 'line' | 'static', clip, event, show, hit, lead, col, first, ...)] (tests)


def lead_of(h, prev):
    """(first?, the tick the path shows): a single / first hit SHOW_FIRST before it, a chain follow-up SHOW_CHAIN before it
    but never before the tick after the hit before it."""
    if prev is None or h - prev > 24:
        return True, h - SHOW_FIRST
    return False, max(prev + 1, h - SHOW_CHAIN)


def colour_of(key, idx):
    """The path colour of api.HITS[key][idx]: white-gold for a parryable hit, else its (group's) last flash's colour."""
    row = api.HITS[key][idx]
    if row[6] == 'P':
        return COL['P'], 'P'
    fl = api.FLASH_AT[key].get(idx) or next(v for v in api.FLASH_AT[key].values() if v)
    return COL[fl[-1][0]], fl[-1][0]


def ride(pb, key, idx, prev=None, t0=0, cond=None, slash_col=api.C_LILAC, path=True, sl=True, show=None, a=None, b=None):
    """The drawn path (riding her) and the slash of api.HITS[key][idx] into the pattern builder pb. prev = the hit tick before
    it in the chain (None: a single / first hit); t0 = the pattern tick of the clip's tick 0."""
    clip, event = api.HITS[key][idx][0], api.HITS[key][idx][1]
    sw = swing_of(clip, event, a=a, b=b)
    h = t0 + sw.h
    first, sh = lead_of(h, prev)
    sh = max(0, sh if show is None else show)
    col, cname = colour_of(key, idx)
    uid = f'{clip}{sw.h}'
    out = Out()
    rec = dict(kind='ride', clip=clip, event=event, hit=h, first=first, col=cname, sw=sw, t0=t0, show=None, pieces=[])
    if path:
        r = path_ride(out, key, sw, t0, sh, col, uid)
        rec.update(show=r['show'], lead=h - r['show'], pts=r['pts'], end=r['end'])
    if sl:
        rec['pieces'] = slash(out, key, sw, t0, SLASH[slash_col], uid)
    out.into(pb, cond)
    DRAWN.setdefault(key, []).append(rec)
    return rec


MARK_W, MARK_H0, MARK_H1, MARK_HEAD = 0.14, 1.95, 4.35, 0.36


def target_mark(out, key, uid, show, h, col, at):
    """The tall in-air mark over a target (v_brief §3 VB 4: a tell at the target that cannot be missed; never a floor decal): a
    thin bright column from MARK_H0 to MARK_H1 over the point `at` (execute subcommands: the lock marker's place) from `show`
    on, a head that comes down it and reaches its foot on the hit tick h. A dash runs straight at the player's lens (its own
    line is seen end-on, behind the avatar): this mark stands over the avatar's head, across the view."""
    mine = f'{TAG}_{uid}'
    sel = SEL.format(mine)
    hsel = f'@e[type=minecraft:item_display,tag={TAG_HEAD},tag={mine},limit=1]'
    up = f'{at} positioned ~ ~{MARK_H0} ~ rotated 0 -90'
    out.at(show, f'execute {up} run ' + card(key, 'sw_path', (0, 0, 0), (0, 0, 0, 1), (MARK_W, MARK_W, MARK_H1 - MARK_H0), col, (mine,), tpd=0),
           f'execute {up} run tp {SEL.format(TAG_NEW)} ~ ~ ~ ~ ~', f'tag {SEL.format(TAG_NEW)} remove {TAG_NEW}',
           f'execute {at} positioned ~ ~{MARK_H1} ~ run summon minecraft:item_display ~ ~ ~ {{Tags:' + _tags(key, TAG_HEAD, mine)
           + ',billboard:"center",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
           f'teleport_duration:1,interpolation_duration:0,transformation:{{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],'
           f'scale:[{f4(MARK_HEAD)},{f4(MARK_HEAD)},{f4(MARK_HEAD)}],right_rotation:[0f,0f,0f,1f]}},'
           f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}sw_head",'
           f'"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}}}')
    n = max(1, h - show)
    for t in range(show, h):
        y = MARK_H1 + (MARK_H0 - MARK_H1) * (t + 1 - show) / n
        out.at(t, f'execute {at} run tp {hsel} ~ ~{y:.3f} ~')
    out.at(h, f'kill {hsel}', f'execute as {sel} run data merge entity @s {{item:{{components:{{"minecraft:custom_model_data":{{colors:[{COL["flare"]}]}}}}}}}}')
    out.at(h + 2, f'kill {sel}')
    return dict(show=show, hit=h)
