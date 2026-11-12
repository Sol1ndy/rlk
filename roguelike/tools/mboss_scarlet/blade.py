"""The blade track of 홍련's fight clips and everything drawn from it (round V lane VB: the track, the wind-ups, the cue's place;
round W lane WB: the TRAIL - w_brief.md §2 WB).

tools/build_scarlet_rig.mjs writes tools/scarlet_blade_track.json: per fight / gauntlet clip tick the blade's base and tip
(and her chest, head, hat crown) in her own frame, [left, up, forward] blocks from her feet, whether the sword shows, and f0
(the tick the sword's first key ends at: before it the rig blends in from the pose before the clip). That frame is the local
frame of a display entity standing at her feet with her yaw (+x left, +y up, +z forward), so a track point is a display
translation and `^left ^up ^forward` as it stands. A key sent on pattern tick t ends at its target tick: at the instant of
pattern tick t the client shows the blade of clip tick t and moves it to tick t + 1 during that tick.

From the track this module derives, per hit (clip, hit tick h):

  the swing    [a, b]: the ticks round h in which the tip travels >= V_SWING b / t (a = the wound pose, b = the follow-through's
               end, capped); the wind-up is `reached` at w = the first tick from which the blade stays within WIND_TOL of its
               pose at a (v_brief: w <= h - 10 for a single / first hit, <= h - 6 for a chain follow-up)
  the trail    (round W; the user, 11-12: the blade's way is NOT to be shown ahead of the cut - mark the way it has come) the
               band on the blade, the pieces it leaves on what it sweeps, the ribbon behind her where her body carries it, the
               wave of a line struck beyond its reach: see the section below. Round V's drawn path, its running head, the
               target lines, the tall mark and the standing lines are gone: nothing shows where the blade is going to go.

Everything is literal commands on pattern ticks (the pattern clock #pt hr): nothing here runs on the game clock, so a clock that
is slowed or frozen (lane VP's beat) keeps the trail in step with the blade.
"""
import json
import math
from pathlib import Path

from . import api

TRACK_FILE = Path(__file__).resolve().parents[1] / 'scarlet_blade_track.json'
_TRACK = {}

# --- the rules (v_brief §3 VB 1; w_brief §2 WB; tests/test_blade.py reads them) -----------------------------------------------
V_SWING = 0.30            # b / t of the tip: a swing tick
SWING_BACK, SWING_ON = 7, 3   # at most this many ticks of swing before / after the hit tick
WIND_TOL = 0.42           # b: the blade's base and tip stay this near their pose at the swing's start = the wind-up is held
LEAD_FIRST, LEAD_CHAIN = 10, 6      # the wind-up is reached this long before a single or first / a chain hit
ARC_TAN = 0.5             # the sector sprite: its edges run from the apex (a 0, b 0) to (a +-0.5, b 1) x 1 / sqrt(1.25)
ARC_INNER = 0.30          # the sprite fades out below this share of the radius
MIN_THICK = 0.12          # b: the floor for any trail card (v_brief / w_brief: nothing thinner)
KIT = api.RP_KIT          # rlk:mboss/hr_kit/


_BLADE = []


def track(clip):
    if not _TRACK:
        d = json.loads(TRACK_FILE.read_text(encoding='utf-8'))
        _TRACK.update(d['clips'])
        _BLADE[:] = d.get('blade', (0.165, 1.6))
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
    return '[' + ','.join(f'"{t}"' for t in ('rlk_hr_sw', 'rlk_room', 'rlk_mb_aux', api.TAGS['pat'], f'rlk_hr_p_{key}') + more) + ']'


def card(key, kind, t, q, s, col, tags=(), bb='fixed', tpd=1):
    """One literal summon of a plain card at the executor (shield.py's fail column): translation t, left rotation q, scale s."""
    return ('summon minecraft:item_display ~ ~ ~ {Tags:' + _tags(key, TAG_NEW, *tags) + f',billboard:"{bb}",item_display:"none",'
            'brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
            f'teleport_duration:{int(tpd)},interpolation_duration:0,transformation:{{translation:[{",".join(f4(v) for v in t)}],'
            f'left_rotation:[{",".join(f4(v) for v in q)}],scale:[{",".join(f4(v) for v in s)}],right_rotation:[0f,0f,0f,1f]}},'
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}{kind}",'
            f'"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}}}')


SEL = '@e[type=minecraft:item_display,tag={}]'
AT_BODY = 'at @s'          # the body's place when the command runs


def _gate(cond, cmd):
    return f'execute {cond} {cmd[8:]}' if cmd.startswith('execute ') else f'execute {cond} run {cmd}'


class Out:
    """tick -> commands (pattern ticks); merged into a pattern builder with .into(pb)."""

    def __init__(self):
        self.t = {}

    def at(self, t, *cmds, cond=None):
        self.t.setdefault(int(t), []).extend(_gate(cond, c) if cond else c for c in cmds if c)

    def into(self, pb, cond=None):
        """Merge into a pattern builder (cond: an execute condition put before every line)."""
        for t in sorted(self.t):
            pb.at(t, [_gate(cond, c) for c in self.t[t]] if cond else self.t[t])
        return self


# =================================================================================================================================
# Round W (lane WB; w_brief.md §2 WB; the user, 11-12: 「보스의 검로가 보이는건 미리 경로를 보여주라는게 아니라 공격이 좀 더 잘
# 보이도록 이미 지나온 경로를 표시하라는 거야」): the TRAIL. Nothing is drawn where the blade is going to go (round V's drawn path, its
# running head, the target lines, the tall mark and the standing lines are gone); the blade leaves a bright ribbon on what it has
# swept. Everything is generated from the blade the rig SHOWS on the pattern clock (Shown: the sword part's transform per clip
# tick as the client gets it - the track's sp / sq - played at the pattern ticks the pattern plays its clips, the blend-in before
# a clip's f0 from the pose shown before):
#
#   the band     one card on the blade (kind sw_band: a lance from the guard to the tip, W_BAND wide) with the sword part's own
#                translation and rotation (+ the constant turn of the lance onto the blade's axis): at pattern tick k it is sent
#                the sword's transform of tick k + 1 with one tick of interpolation, as the rig's own keys are, so it moves
#                exactly as the blade does. From the first known pose to the end of the last follow-through: the trail's head.
#   the pieces   per pattern tick t the surface the blade sweeps t -> t + 1 (the client's own interpolation of the sword part),
#                in planar pieces of <= ARC_STEP deg of blade turn: a sector (sw_fan) where it turns about a point of its own
#                line, else a strip (sw_quad) where it moves sideways. Every piece of the sweep t -> t + 1 is summoned at t with NO
#                width on the blade's line of tick t, and at t + 1 given its full shape with one tick of interpolation: it opens
#                from where the blade was to where it went one tick behind it (LAG) - nothing ahead of the blade, at any instant,
#                whatever the client's interpolation of the sword does inside a tick. It rides her model the two
#                ticks it is made on and is then left in the world where it was swept (a dash leaves it behind her); its fading
#                frames at FADE, gone LIFE t after it began to open. A swing's pieces (a hit's [a, b]) are whiter and wear a
#                taller rim wall (the trail seen edge-on): round V's slash IS the trail's brightest stretch (one effect).
#   the ribbon   where her BODY carries the blade (a dash, a lunge, a dive, a gauntlet approach, a leap into a cut): a band in the
#                world from where her sword hand was when the move began, grown each tick to the hand's place one tick back
#                (core/sw/rib): it stays one step behind her model at any clock speed.
#   the wave     a dash-through's line and kcut's three crossing lines strike beyond her blade's reach: ON the hit tick (never
#                before) the struck line flashes for WAVE_LIFE t.
#
# The band and the pieces carry rlk_mb_part: lane VP's beat (player/def/beat/**: its held ticks, the slow motion's stretched
# interpolation, the rocked-back tilt) treats them as it treats her rig's parts. The core's fight hook rides TR_RIDE cards to her
# model after rig/tick (RIDE_CMD: at the rig's root part). Every command is a literal line on a pattern tick: a held or slowed
# pattern clock holds the trail with the blade.
LIFE = 7                      # t: a piece is gone this long after it began to open (w_brief: fading out over ~6-8 t)
FADE = ((3, 1), (5, 2))       # (ticks after it began to open, fading frame)
RIDE_T = 2                    # t: a piece rides her model from its summon to its opening tick, then stays where it was swept
LAG = 1                       # t: the sweep t -> t + 1 opens on tick t + 1, one tick behind the blade (a planar piece cannot follow the
#                               client's curved interpolation of a fast cut within the tick without running ahead of it somewhere)
W_BAND = 0.26                 # b: the band on the blade (its bright core RIB_CORE x that)
RIB_CORE = 0.56               # the bright share of a sw_rib / sw_band card's width, of a rim wall's height (ink on both sides)
RIBBON = 0.24                 # the bright ribbon of a swept piece: this share of its length from the blade's base (ink on both sides)
WALL, WALL_HOT = 0.22, 0.30   # b: the rim wall of a piece (the trail seen edge-on); a swing's pieces
RIB_W = 0.30                  # b: a body ribbon's width
RIB_LIFE = 6                  # t: a ribbon is gone this long after its last growth
WAVE_W, WAVE_LIFE = 0.30, 4
ARC_STEP = 30.0               # deg of blade turn per planar piece (its chord lies within 3.5 % of the radius inside the tip's way)
TIP_STEP = 0.9                # b of tip travel per planar piece
MIN_TURN = 3.0                # deg: under it the blade did not turn (a strip, or nothing)
HOT_MIX = 0.55                # a swing's pieces: the colour mixed this far to white
FAN_CHORD = 1.0               # the wedge sprite's corners lie at b = this (its rim and the rim wall are the chord between them)
TAG = 'rlk_hr_sw'             # round V's tag: card() (shield.py's fail column) keeps it
TAG_NEW = 'rlk_hr_swn'
TR, TR_RIDE, TR_BAND, TR_GROW, TR_TGT, TR_NEW = 'rlk_hr_tr', 'rlk_hr_trr', 'rlk_hr_trb', 'rlk_hr_trg', 'rlk_hr_trt', 'rlk_hr_trn'
TR_FAM = {'fan': 'rlk_hr_trf', 'quad': 'rlk_hr_trq', 'rib': 'rlk_hr_tri'}      # the model family of a card (core/pp fades by it)
BEAT_TAG = 'rlk_mb_part'      # lane VP's beat passes take displays with this tag (the rig's parts carry it)
TR_SEL = SEL.format(TR)
# colours (RGB ints, the sprites are white): a parryable hit white-gold, an unparriable one its flash's colour
COL = {'P': 0xFFE9A8, 'yellow': 0xFFE14A, 'purple': 0xD68BFF, 'blue': 0x5AA8FF, 'flare': 0xFFFFFF}
R_LANCE = (-math.sqrt(0.5), 0.0, 0.0, math.sqrt(0.5))   # turns a lance card's +z onto the sword part's +y (the blade's axis)


def blade_span():
    """(bladeLo, tip): the blade along the sword part's local +y (the track's top-level `blade`)."""
    track('a1')
    return tuple(_BLADE)


def hot(col):
    r, g, b = (col >> 16) & 255, (col >> 8) & 255, col & 255
    m = lambda v: int(round(v + (255 - v) * HOT_MIX))      # noqa: E731
    return (m(r) << 16) | (m(g) << 8) | m(b)


# --- quaternions (x, y, z, w) ----------------------------------------------------------------------------------------------------
def qmul(a, b):
    ax, ay, az, aw = a
    bx, by, bz, bw = b
    return (aw * bx + ax * bw + ay * bz - az * by, aw * by - ax * bz + ay * bw + az * bx,
            aw * bz + ax * by - ay * bx + az * bw, aw * bw - ax * bx - ay * by - az * bz)


def qrot(q, v):
    x, y, z, w = q
    u = (x, y, z)
    c1 = cross(u, v)
    c2 = cross(u, c1)
    return tuple(v[i] + 2 * (w * c1[i] + c2[i]) for i in range(3))


def qslerp(a, b, u):
    """JOML's Quaternionf.slerp (the client's display interpolation): the shorter way."""
    d = sum(x * y for x, y in zip(a, b))
    if d < 0:
        b, d = tuple(-x for x in b), -d
    if d > 0.9995:
        r = tuple(x + (y - x) * u for x, y in zip(a, b))
    else:
        th = math.acos(min(1.0, d))
        s = math.sin(th)
        r = tuple((math.sin((1 - u) * th) * x + math.sin(u * th) * y) / s for x, y in zip(a, b))
    n = math.sqrt(sum(x * x for x in r))
    return tuple(x / n for x in r)


# --- what the rig shows ----------------------------------------------------------------------------------------------------------
class Shown:
    """The sword her rig shows on a pattern's clock. st[t] = (translation, rotation) of the sword part at the instant of pattern tick
    t (the client moves it to st[t + 1] during that tick), None while the sword is not shown or its place is not known.
    segs = [(pattern tick, clip)] (api.play at that tick: its clip tick 0 is that pattern tick); a clip's ticks before its f0 (the
    sword's first key) are the rig's blend from the transform shown before - known when that is, else None (a pattern's first
    clip: the stance she comes from is not known at build time). hidden = pattern ticks of state/hidden (until the next clip);
    last = the last pattern tick wanted."""

    def __init__(self, segs, hidden=(), last=None):
        self.st, self.clip = {}, {}
        self.lo, self.hi = blade_span()
        prev = None
        segs = sorted(segs)
        for i, (t0, clip) in enumerate(segs):
            tr = track(clip)
            n, f0 = len(tr['sp']) - 1, int(tr.get('f0', 0))
            t1 = segs[i + 1][0] if i + 1 < len(segs) else (t0 + n if last is None else last)
            hid = min((h for h in hidden if t0 <= h and (h < t1 or i + 1 == len(segs))), default=None)
            start = prev
            for t in range(t0, t1 + 1):
                ct = min(n, t - t0)
                if hid is not None and t >= hid:
                    s = None
                elif ct >= f0:
                    s = (tuple(tr['sp'][ct]), tuple(tr['sq'][ct])) if tr['on'][ct] else None
                elif start is not None and tr['on'][min(f0, n)]:
                    u = ct / f0
                    s = (lerp(start[0], tr['sp'][f0], u), qslerp(start[1], tuple(tr['sq'][f0]), u))
                else:
                    s = None
                self.st[t] = s
                self.clip[t] = (clip, ct)
            prev = self.st[t1]

    def known(self, t):
        return self.st.get(t) is not None

    def at(self, u):
        """(translation, rotation) at the float pattern tick u (the client's interpolation between two ticks)"""
        i = int(math.floor(u))
        f = u - i
        a = self.st.get(i)
        if f < 1e-9:
            return a
        b = self.st.get(i + 1)
        if a is None or b is None:
            return None
        return lerp(a[0], b[0], f), qslerp(a[1], b[1], f)

    def blade(self, u):
        """(base, tip) in her frame at the float pattern tick u, or None"""
        s = self.at(u)
        if s is None:
            return None
        p, q = s
        return add(p, qrot(q, (0.0, self.lo, 0.0))), add(p, qrot(q, (0.0, self.hi, 0.0)))


# --- the pieces: the surface the blade sweeps in one tick ------------------------------------------------------------------------
def _fan_scale(r, beta):
    """(sx, sz) of a sw_fan card whose corners stand at the radius r, its half-angle beta deg (the wedge sprite: edges a = +-b / 2,
    its rim the chord b = 1 between the corners - a uniform circle would bulge out past the tip's way when the card is squeezed)"""
    return 2 * r * math.sin(math.radians(beta)), r * math.cos(math.radians(beta))


def splits(sh, t):
    """Float ticks t .. t + 1 with <= ARC_STEP deg of blade turn and <= TIP_STEP b of tip travel between two of them."""
    p0, p1 = sh.blade(t), sh.blade(t + 1)
    d0, d1 = sub(p0[1], p0[0]), sub(p1[1], p1[0])
    n = max(1, math.ceil(angle(d0, d1) / ARC_STEP - 1e-6), math.ceil(math.dist(p0[1], p1[1]) / TIP_STEP - 1e-6))
    # (the client's slerp may bend the way: check the halves)
    while n < 12:
        us = [t + k / n for k in range(n + 1)]
        bl = [sh.blade(u) for u in us]
        if all(angle(sub(a[1], a[0]), sub(b[1], b[0])) <= ARC_STEP + 1e-6 and math.dist(a[1], b[1]) <= TIP_STEP + 1e-6
               for a, b in zip(bl, bl[1:])):
            return us
        n += 1
    return [t + k / n for k in range(n + 1)]


def sweep(sh, t, wall=WALL):
    """The pieces of the blade's way t -> t + 1: [dict(kind 'fan' | 'quad', u0, u1, xf0 = (translation, rotation, scale) with no
    width on the blade's line of tick t, xf1 = its full shape, + its geometry for the tests)]. Where the blade only slid along
    itself, or the piece would be narrower than MIN_THICK, there is none (the band on the blade is the trail there)."""
    b0, t0 = sh.blade(t)
    d0 = unit(sub(t0, b0))
    us = splits(sh, t)
    out = []
    for ua, ub in zip(us, us[1:]):
        (ba, ta), (bb, tb) = sh.blade(ua), sh.blade(ub)
        da, db = unit(sub(ta, ba)), unit(sub(tb, bb))
        ph = angle(da, db)
        nv = cross(da, db)
        pc = None
        if ph >= MIN_TURN and norm(nv) > 1e-6:
            nv = unit(nv)
            w0 = sub(ba, bb)
            bq, dd, ee = dot(da, db), dot(da, w0), dot(db, w0)
            den = 1 - bq * bq
            q = lerp(add(ba, mul(da, (bq * ee - dd) / den)), add(bb, mul(db, (ee - bq * dd) / den)), 0.5)
            ra, rb = norm(sub(ta, q)), norm(sub(tb, q))
            if min(dot(sub(ta, q), da), dot(sub(tb, q), db)) > 0.3 and max(ra, rb) <= 6.0 and abs(ra - rb) <= 0.22:
                z = unit(add(unit(sub(ta, q)), unit(sub(tb, q))))
                beta = angle(sub(ta, q), sub(tb, q)) / 2
                r = (ra + rb) / 2
                # (its chord and its bright ribbon - the outer 23 % of the wedge, the sprite - at least MIN_THICK)
                if 2 * r * math.sin(math.radians(beta)) >= MIN_THICK and RIBBON * r * math.cos(math.radians(beta)) >= MIN_THICK:
                    sx, sz = _fan_scale(r, beta)
                    y = nv
                    x = cross(y, z)
                    # the start: no width, in its own plane about its own apex, turned back from its first edge by the blade's
                    # turn since the tick began: it opens by turning about the apex, so every piece of the tick starts from the
                    # tick's first blade position and its leading edge never turns farther than the blade has
                    ea = unit(sub(ta, q))
                    back = -math.radians(angle(d0, da))
                    z0 = unit(add(mul(ea, math.cos(back)), mul(cross(y, ea), math.sin(back))))
                    if abs(dot(sub(t0, q), y)) > 0.08:
                        z0 = ea                         # (the tick's first blade position is not in this piece's plane: from its own edge)
                    _sx0, sz0 = _fan_scale(r, 0.0)
                    pc = dict(kind='fan', q=q, z=z, n=nv, beta=beta, r=r, tips=(ta, tb), bases=(ba, bb),
                              xf0=(q, quat(cross(y, z0), y, z0), (0.0, wall, sz0)), xf1=(q, quat(x, y, z), (sx, wall, sz)))
        if pc is None:
            # no turn about a point of its own line: a strip between the two blade lines, its far end at the tips
            u = unit(add(da, db))
            ma, mb = lerp(ba, ta, 0.5), lerp(bb, tb, 0.5)
            v = sub(mb, ma)
            vp = sub(v, mul(u, dot(v, u)))
            w = norm(vp)
            if w >= MIN_THICK and RIBBON * (norm(sub(ta, ba)) + norm(sub(tb, bb))) / 2 >= MIN_THICK:
                xw = mul(vp, 1 / w)
                y = cross(u, xw)
                ln = (norm(sub(ta, ba)) + norm(sub(tb, bb))) / 2
                c = sub(lerp(ma, mb, 0.5), mul(u, ln / 2))             # the base end's middle
                m0 = lerp(b0, t0, 0.5)
                # the start: no width, across the way where the blade of tick t is (it grows from there as the blade moves on)
                c0 = sub(c, mul(xw, dot(sub(c, m0), xw)))
                rot = quat(xw, y, u)
                pc = dict(kind='quad', c=c, u=u, x=xw, n=y, w=w, len=ln, tips=(ta, tb), bases=(ba, bb),
                          xf0=(c0, rot, (0.0, wall, ln)), xf1=(c, rot, (w, wall, ln)))
        if pc:
            pc.update(u0=ua - t, u1=ub - t)
            out.append(pc)
    return out


def band_xf(s, w=W_BAND):
    """The band's transformation for the sword transform s = (translation, rotation): the sword's own frame, the lance turned onto
    its +y (sw_band's lance runs from bladeLo / tip to 1 of its length: scaled to the tip it starts at the guard)."""
    p, q = s
    return p, qmul(q, R_LANCE), (w, w, blade_span()[1])


# --- cards -----------------------------------------------------------------------------------------------------------------------
def _ttags(key, *more, beat=True):
    base = (TR, BEAT_TAG) if beat else (TR,)
    return '[' + ','.join(f'"{t}"' for t in base + ('rlk_room', 'rlk_mb_aux', api.TAGS['pat'], f'rlk_hr_p_{key}') + more) + ']'


def _xf(t, q, s):
    return (f'transformation:{{translation:[{",".join(f4(v) for v in t)}],left_rotation:[{",".join(f4(v) for v in q)}],'
            f'scale:[{",".join(f4(v) for v in s)}],right_rotation:[0f,0f,0f,1f]}}')


def tcard(key, model, xf, col, tags, tpd=1, ipd=1, beat=True):
    """One literal summon of a trail card at the executor (xf = (translation, left rotation, scale) in its frame)."""
    return ('summon minecraft:item_display ~ ~ ~ {Tags:' + _ttags(key, *tags, beat=beat) + ',billboard:"fixed",item_display:"none",'
            'brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
            f'teleport_duration:{int(tpd)},interpolation_duration:{int(ipd)},{_xf(*xf)},'
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}{model}",'
            f'"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}}}')


def _model_cmd(sel, model):
    return f'execute as {sel} run data modify entity @s item.components."minecraft:item_model" set value "{KIT}{model}"'


# --- the trail of a pattern ------------------------------------------------------------------------------------------------------
TRAILS = {}               # key -> [record of trail()] (the tests)


def trail(out, key, uid, sh, t0, t1, col_at, hot_at=None, cond_at=None):
    """The band and the pieces of the shown sword sh on pattern ticks t0 .. t1 into out: the band shows the poses t0 .. t1, the
    pieces the sweeps t -> t + 1 for t0 <= t < t1. col_at(t) = the colour (int) of tick t's sweep; hot_at(t): it belongs to a
    swing; cond_at(t): an execute condition for the commands of tick t (or None). Returns the record (TRAILS)."""
    hot_at = hot_at or (lambda t: False)
    cond_at = cond_at or (lambda t: None)
    rec = dict(uid=uid, shown=sh, t0=t0, t1=t1, pieces={}, band=[], col={}, hot={}, bandcol={})
    # the band: runs of known transforms; at tick k it is sent the sword's transform of tick k + 1 (one tick of interpolation)
    t = t0
    while t <= t1:
        if not sh.known(t):
            t += 1
            continue
        e = t
        while e + 1 <= t1 and sh.known(e + 1):
            e += 1
        mine = f'{TR}_{uid}b{t}'
        sel = SEL.format(mine)
        col = col_at(min(t, t1 - 1) if t1 > t0 else t)
        # summoned a tick early with no size on the pose of tick t: from t it grows onto the blade as it moves (a display that
        # is new to the client cannot interpolate in its first tick)
        p0, q0, _s = band_xf(sh.st[t])
        out.at(t - 1, tcard(key, 'sw_band', (p0, q0, (0.0, 0.0, 0.0)), col, (TR_RIDE, TR_BAND, mine)), cond=cond_at(t - 1))
        rec['bandcol'][t] = col
        last = None
        for k in range(t, e + 1):
            if not sh.known(k + 1):
                break
            xf = _xf(*band_xf(sh.st[k + 1]))
            c2 = col_at(k)
            extra = ''
            if c2 != col:
                col = c2
                extra = f',item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}sw_band","minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}'
            rec['bandcol'][k] = col
            if xf != last or extra:
                out.at(k, f'execute as {sel} run data merge entity @s {{start_interpolation:0,interpolation_duration:1,{xf}{extra}}}',
                       cond=cond_at(k))
                last = xf
        out.at(e + 1, f'kill {sel}', cond=cond_at(e + 1))
        rec['band'].append((t, e))
        t = e + 1
    # the pieces
    for t in range(t0, t1):
        if not (sh.known(t) and sh.known(t + 1)):
            continue
        h = bool(hot_at(t))
        pcs = sweep(sh, t, WALL_HOT if h else WALL)
        if not pcs:
            continue
        col = hot(col_at(t)) if h else col_at(t)
        o = t + LAG                                     # the tick it opens on
        grp = f'{TR}_{uid}_{t}'
        gsel = SEL.format(grp)
        for i, pc in enumerate(pcs):
            fam = pc['kind']
            out.at(o - 1, tcard(key, f'sw_{fam}_0', pc['xf0'], col, (TR_RIDE, TR_FAM[fam], grp, f'{TR}_i{i}')), cond=cond_at(o - 1))
            out.at(o, f'execute as {gsel[:-1]},tag={TR}_i{i}] run data merge entity @s {{start_interpolation:0,{_xf(*pc["xf1"])}}}',
                   cond=cond_at(o))
        out.at(o + RIDE_T - 1, f'tag {gsel} remove {TR_RIDE}', cond=cond_at(o + RIDE_T - 1))
        fams = sorted({pc['kind'] for pc in pcs})
        for dt, fr in FADE:
            for fam in fams:
                s_ = gsel if len(fams) == 1 else f'{gsel[:-1]},tag={TR_FAM[fam]}]'
                out.at(o + dt, _model_cmd(s_, f'sw_{fam}_{fr}'), cond=cond_at(o + dt))
        out.at(o + LIFE, f'kill {gsel}', cond=cond_at(o + LIFE))
        rec['pieces'][t] = pcs
        rec['col'][t], rec['hot'][t] = col, h
    rec['end'] = max([e + 1 for _t, e in rec['band']] + [t + LAG + LIFE for t in rec['pieces']] + [t0])
    TRAILS.setdefault(key, []).append(rec)
    return rec


RIG_ROOT = api.RIG_UUID.format(0)
# the core's fight hook, after rig/tick: the riding cards to her model (the rig's root part: its place and yaw, also when the core
# put her elsewhere inside the hook - rig/follow_now)
RIDE_CMD = f'execute at {RIG_ROOT} run tp {SEL.format(TR_RIDE)} ~ ~ ~ ~ ~'


def stop_lines():
    """A perfect parry's flinch (core/pp): the band goes with the swing; the pieces / ribbons jump to their last fading frame (the
    pattern ends PP_FLINCH t later, core/pat_end kills them)."""
    return [f'kill {SEL.format(TR_BAND)}', f'tag {SEL.format(TR_GROW)} remove {TR_GROW}',
            f'kill @e[type=minecraft:marker,tag={TR_TGT}]'] + \
        [_model_cmd(SEL.format(TR_FAM[f]), f'sw_{f}_2') for f in ('fan', 'quad', 'rib')]


def end_lines():
    """core/pat_end and the gauntlet's end: whatever of a trail is left."""
    return [f'kill {TR_SEL}', f'kill @e[type=minecraft:marker,tag={TR_TGT}]']


# --- the ribbon: her body carries the blade ---------------------------------------------------------------------------------------
RIBS = {}                 # key -> [dict(uid, t0, t1, col, cond, end)] (the tests)


def runtime(W, fn, sset):
    """core/sw/{rib,rib1}: the run-time part of the ribbon (written once by p1.py)."""
    o = api.OBJ
    tgt = f'@e[type=minecraft:marker,tag={TR_TGT},limit=1]'
    W.w('core/sw/rib', [
        '# The growing ribbon (blade.py; rlk_hr_trg: one at a time; @s = the body, at the hand\'s place now): it turns to the',
        f'# marker {TR_TGT} (the hand\'s place one tick ago) and becomes as long as the way to it (one tick of interpolation: one',
        '# step behind her model, never ahead of it), then the marker comes here.',
        f'execute as {SEL.format(TR_GROW)} at @s facing entity {tgt} feet run function {api.NS}core/sw/rib1',
        f'tp {tgt} ~ ~ ~'])
    W.w('core/sw/rib1', [
        f'# @s = the growing ribbon, at it, facing the marker {TR_TGT}: turn there; its length = (marker - here) . the aim (x 1000).',
        'tp @s ~ ~ ~ ~ ~',
        f'execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {{Tags:["rlk_hr_tru","rlk_room","rlk_mb_aux"]}}',
        *[f'execute store result score #sw_{a} {o} run data get entity {tgt} Pos[{i}] 1000' for i, a in enumerate('xyz')],
        *[ln for i, a in enumerate('xyz') for ln in (
            f'execute store result score #sw_n {o} run data get entity @s Pos[{i}] 1000',
            f'scoreboard players operation #sw_{a} {o} -= #sw_n {o}',
            f'execute store result score #sw_u {o} run data get entity @e[type=minecraft:marker,tag=rlk_hr_tru,limit=1] Pos[{i}] 1000',
            f'scoreboard players operation #sw_u {o} -= #sw_n {o}',
            f'scoreboard players operation #sw_{a} {o} *= #sw_u {o}')],
        'kill @e[type=minecraft:marker,tag=rlk_hr_tru]',
        f'scoreboard players operation #sw_x {o} += #sw_y {o}',
        f'scoreboard players operation #sw_x {o} += #sw_z {o}',
        f'execute if score #sw_x {o} matches ..0 run return 0',
        f'execute store result entity @s transformation.scale[2] float 0.000001 run scoreboard players get #sw_x {o}'])


def hand(sh, t):
    """The point of her frame the ribbon follows at pattern tick t: her sword hand (the blade's base); not shown: chest high."""
    p = sh.blade(t) if sh is not None and sh.known(t) else None
    return p[0] if p else (0.0, 1.1, 0.25)


def ribbon(out, key, uid, sh, ta, tb, col, cond=None, w=RIB_W, seg=99):
    """The ribbon of a body move (the glide / leap called at pattern tick ta; the body there at tb). @s = the body: on pattern tick
    t the hook runs after the movement library moved it (its place of tick t; her model reaches it during this tick). The ribbon
    starts at the hand's place of ta; on ta + 1 .. tb + 1 it grows to the hand's place one tick back (core/sw/rib). seg: a new
    straight piece every seg ticks (a curved way: a leap). Then it fades and is gone RIB_LIFE t after its last growth."""
    def at_hand(t):
        return f'at @s rotated as @s rotated ~ 0 positioned {car(hand(sh, t))}'
    tgt = f'@e[type=minecraft:marker,tag={TR_TGT},limit=1]'
    end = ta
    for s in range(ta, tb + 1, seg):
        e = min(tb + 1, s + seg)
        mine = f'{TR}_{uid}r{s}'
        sel = SEL.format(mine)
        first = s == ta
        mk = (f'kill @e[type=minecraft:marker,tag={TR_TGT}]',
              f'execute {at_hand(s)} run summon minecraft:marker ~ ~ ~ {{Tags:{_ttags(key, TR_TGT, beat=False)}}}') if first else ()
        out.at(s, *mk, f'tag {SEL.format(TR_GROW)} remove {TR_GROW}',
               f'execute {"at " + tgt if not first else at_hand(s)} run ' + tcard(key, 'sw_rib_0', ((0, 0, 0), (0, 0, 0, 1), (w, w, 0.0)),
                                                                              col, (TR_FAM['rib'], TR_GROW, mine), tpd=0, beat=False),
               cond=cond)
        for t in range(s + 1, e + 1):
            out.at(t, f'execute {at_hand(t + 1)} run function {api.NS}core/sw/rib', cond=cond)
        out.at(e + 1, f'tag {sel} remove {TR_GROW}', cond=cond)
        out.at(e + 2, _model_cmd(sel, 'sw_rib_1'), cond=cond)
        out.at(e + 4, _model_cmd(sel, 'sw_rib_2'), cond=cond)
        out.at(e + RIB_LIFE, f'kill {sel}', cond=cond)
        end = max(end, e + RIB_LIFE)
    out.at(tb + 2, f'kill @e[type=minecraft:marker,tag={TR_TGT}]', cond=cond)
    RIBS.setdefault(key, []).append(dict(uid=uid, t0=ta, t1=tb, col=col, cond=cond, seg=seg, end=end))
    return end


WAVES = {}


def wave(out, key, uid, h, col, where, length=None, store=None, w=WAVE_W, cond=None):
    """The struck line of a hit that reaches beyond her blade (a dash-through's line, kcut's crossing lines): a band left in the
    world ON the hit tick h, WAVE_LIFE t. where = execute subcommands for its start and aim; its length a number, or store = the
    fake player holding it in half blocks (a dash's probed length)."""
    mine = f'{TR}_{uid}w'
    sel = SEL.format(mine)
    out.at(h, f'execute {where} run ' + tcard(key, 'sw_rib_0', ((0, 0, 0), (0, 0, 0, 1), (w, w, length or 0.0)), col,
                                             (TR_FAM['rib'], TR_NEW, mine), tpd=0, ipd=0, beat=False),
           f'execute {where} run tp {SEL.format(TR_NEW)} ~ ~ ~ ~ ~', cond=cond)
    if store:
        out.at(h, f'execute as {SEL.format(TR_NEW)} store result entity @s transformation.scale[2] float 0.5 run scoreboard players get {store} {api.OBJ}',
               cond=cond)
    out.at(h, f'tag {SEL.format(TR_NEW)} remove {TR_NEW}', cond=cond)
    out.at(h + 2, _model_cmd(sel, 'sw_rib_1'), cond=cond)
    out.at(h + 3, _model_cmd(sel, 'sw_rib_2'), cond=cond)
    out.at(h + WAVE_LIFE, f'kill {sel}', cond=cond)
    WAVES.setdefault(key, []).append(dict(uid=uid, hit=h, col=col, len=length, store=store))
    return h + WAVE_LIFE


# --- a pattern's hits and its trail ----------------------------------------------------------------------------------------------
def colour_of(key, idx):
    """The trail colour of api.HITS[key][idx]: white-gold for a parryable hit, else its (group's) last flash's colour."""
    row = api.HITS[key][idx]
    if row[6] == 'P':
        return COL['P'], 'P'
    fl = api.FLASH_AT[key].get(idx) or next(v for v in api.FLASH_AT[key].values() if v)
    return COL[fl[-1][0]], fl[-1][0]


def pattern_hits(key, t0_of=None, only=None):
    """[(pattern tick of the hit, Swing, colour, colour name, HITS index, clip tick 0's pattern tick)] of a P1 / P2 pattern, one
    per clip event (t0_of: clip -> its pattern tick 0; only: the HITS indices to take)."""
    out, seen = [], set()
    for i, row in enumerate(api.HITS[key]):
        clip, ev = row[0], row[1]
        if (clip, ev) in seen or (only is not None and i not in only):
            continue
        seen.add((clip, ev))
        c0 = (t0_of or {}).get(clip, 0)
        sw = swing_of(clip, ev)
        col, name = colour_of(key, i)
        out.append((c0 + sw.h, sw, col, name, i, c0))
    return out


def colours(hits):
    """col_at, hot_at for trail() from hits = [(hit tick, Swing, colour, ..., clip t0)]: a sweep has the colour of the next hit
    (after the last: the last one's); it is hot inside a swing [a, b]."""
    hs = sorted(hits, key=lambda x: x[0])

    def col_at(t):
        for h in hs:
            if h[0] >= t + 1:
                return h[2]
        return hs[-1][2]

    def hot_at(t):
        return any(h[5] + h[1].a <= t and t + 1 <= h[5] + h[1].b for h in hs)
    return col_at, hot_at


def end_of(hits):
    """The trail's last tick: the end of the last hit's follow-through (its swing's b)."""
    return max(h[5] + h[1].b for h in hits)


# --- the parry cue's place -------------------------------------------------------------------------------------------------------
CUE_LOW, CUE_HAT_R, CUE_OVER = 1.75, 0.8, 0.9


def cue_point(clip, t):
    """Where the parry cue's star stands at clip tick t (her frame): on the blade's middle - unless that is low (under CUE_LOW:
    from the F5 camera the avatar's own head covers it) or on her hat (white-gold on white: review v C2): then CUE_OVER above
    the hat's crown, clear of both."""
    tr = track(clip)
    t = max(0, min(len(tr['t']) - 1, t))
    m = lerp(tr['b'][t], tr['t'][t], 0.5)
    k = tr['k'][t]
    on_hat = math.hypot(m[0] - k[0], m[2] - k[2]) < CUE_HAT_R and k[1] - 0.7 <= m[1] <= k[1] + 0.35
    if m[1] < CUE_LOW or on_hat or not tr['on'][t]:
        return (k[0], k[1] + CUE_OVER, k[2])
    return m
