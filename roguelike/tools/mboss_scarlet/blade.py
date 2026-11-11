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
# Round W (lane WB; w_brief.md §2 WB): the TRAIL. Nothing is drawn where the blade is going to go; the blade leaves a ribbon on
# what it has swept. Everything below is generated from the blade the rig shows (Shown: the track on the pattern clock):
#
#   the band     one card on the blade itself (kind sw_rib_0, W_BAND wide, from BAND_FROM of the blade to its tip), there from
#                the first tick the clip's own pose is shown to the end of the last follow-through: the trail's head, the
#                brightest thing of the attack, in the colour of the hit the blade is on its way to. At pattern tick t it is
#                sent to the blade's place of tick t + 1 with one tick of interpolation: it moves as the rig's blade does.
#   the pieces   per pattern tick the surface the blade sweeps from t to t + 1: a sector (sw_fan: the blade turned about a point
#                on its own line; <= ARC_STEP deg each) or a strip (sw_quad: it moved sideways). A piece is summoned one tick
#                early with no width ON the blade's line of tick t, and at tick t told its full shape with one tick of
#                interpolation: it opens behind the blade exactly as the client moves the blade (its leading edge is the
#                blade), never before it. LIFE t after its growth began it is gone, through the fading frames FADE. The pieces
#                of a swing (a hit's [a, b]) are the round V slash: the same geometry, `hot` (whiter, a taller rim wall):
#                the trail's brightest stretch - one effect.
#   the ribbon   where her BODY carries the blade (a dash, a lunge, a dive, a gauntlet approach): a band (sw_rib) from the place
#                her sword hand was when the move began to where it is now, grown each tick behind her (core/sw/rib: aimed at
#                the hand's place of the next tick, as long as the way to it).
#   the wave     a dash-through's line and kcut's three crossing lines strike farther than her blade reaches: ON the hit tick
#                (never before) the struck line flashes for WAVE_LIFE t.
#
# The band and the pieces ride her model (TAG_RIDE: the core's hook teleports them after rig/tick, in the rig's own frame);
# every card is an item_display with rlk_mb_part: the perfect parry / dodge beat (player/def/beat/**: the held ticks, the
# stretched interpolation of the slow motion, the rocked-back tilt) treats it as it treats her rig's parts. All commands are
# literal lines on pattern ticks: a held or slowed pattern clock holds the trail with the blade.
LIFE = 7                      # t: a piece is gone this long after it began to open (w_brief: fading out over ~6-8 t)
FADE = ((3, 1), (5, 2))       # (ticks after it began to open, fading frame)
W_BAND = 0.26                 # b: the band on the blade (its bright core RIB_CORE x that)
BAND_FROM = 0.22              # the band starts at this share of the blade from its base (her hand stays free)
RIB_CORE = 0.70               # the bright share of a sw_rib card's width / of a rim wall's height
WALL, WALL_HOT = 0.18, 0.26   # b: the rim wall of a piece (the trail seen edge-on); a swing's pieces
RIB_W = 0.30                  # b: a body ribbon's width
RIB_LIFE = 6                  # t: a ribbon is gone this long after the move ended
WAVE_W, WAVE_LIFE = 0.30, 4
ARC_STEP = 60.0               # deg of blade turn per sector
MIN_TURN = 3.0                # deg: under it the blade did not turn (a strip, or nothing)
HOT_MIX = 0.55                # a swing's pieces: the colour mixed this far to white
TAG_OLD = 'rlk_hr_sw'         # (round V's tag: shield.py's fail column keeps it)
TAG = TAG_OLD                 # card() above
TAG_NEW = 'rlk_hr_swn'
TR, TR_RIDE, TR_BAND, TR_RIB, TR_GROW, TR_TGT = 'rlk_hr_tr', 'rlk_hr_trr', 'rlk_hr_trb', 'rlk_hr_tri', 'rlk_hr_trg', 'rlk_hr_trt'
TR_FAM = {'fan': 'rlk_hr_trf', 'quad': 'rlk_hr_trq', 'rib': 'rlk_hr_tri'}      # the model family (core/ppf fades them by family)
BEAT_TAG = 'rlk_mb_part'      # lane VP's beat passes take displays with this tag (the rig's parts carry it)
TR_NEW = 'rlk_hr_trn'
TR_SEL = SEL.format(TR)
# colours (RGB ints, the sprites are white): a parryable hit white-gold, an unparriable one its flash's colour
COL = {'P': 0xFFE9A8, 'yellow': 0xFFE14A, 'purple': 0xD68BFF, 'blue': 0x5AA8FF, 'flare': 0xFFFFFF}


def hot(col):
    r, g, b = (col >> 16) & 255, (col >> 8) & 255, col & 255
    m = lambda v: int(round(v + (255 - v) * HOT_MIX))      # noqa: E731
    return (m(r) << 16) | (m(g) << 8) | m(b)


def _ttags(key, *more):
    return '[' + ','.join(f'"{t}"' for t in (TR, BEAT_TAG, 'rlk_room', 'rlk_mb_aux', api.TAGS['pat'], f'rlk_hr_p_{key}') + more) + ']'


def _xf(t, q, s):
    return (f'transformation:{{translation:[{",".join(f4(v) for v in t)}],left_rotation:[{",".join(f4(v) for v in q)}],'
            f'scale:[{",".join(f4(v) for v in s)}],right_rotation:[0f,0f,0f,1f]}}')


def tcard(key, model, xf, col, tags, tpd=1, ipd=1):
    """One literal summon of a trail card at the executor (the frame of xf = (translation, left rotation, scale))."""
    return ('summon minecraft:item_display ~ ~ ~ {Tags:' + _ttags(key, *tags) + ',billboard:"fixed",item_display:"none",'
            'brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,'
            f'teleport_duration:{int(tpd)},interpolation_duration:{int(ipd)},{_xf(*xf)},'
            f'item:{{id:"minecraft:paper",count:1,components:{{"minecraft:item_model":"{KIT}{model}",'
            f'"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}}}')


def _model_cmd(sel, model):
    return f'execute as {sel} run data modify entity @s item.components."minecraft:item_model" set value "{KIT}{model}"'


# --- what the rig shows ----------------------------------------------------------------------------------------------------------
def interp(p0, p1, u):
    """The blade (base, tip) the client shows a share u of the way from p0 to p1 (one key: the base in a line, the direction
    turning evenly, the length evenly)."""
    (b0, t0), (b1, t1) = p0, p1
    if u <= 0:
        return p0
    if u >= 1:
        return p1
    d0, d1 = sub(t0, b0), sub(t1, b1)
    b = lerp(b0, b1, u)
    d = slerp(unit(d0), unit(d1), u)
    return b, add(b, mul(d, norm(d0) + (norm(d1) - norm(d0)) * u))


class Shown:
    """The blade the rig shows on a pattern's clock: pose[t] = (base, tip) in her frame at the instant of pattern tick t (the
    client moves it to pose[t + 1] during that tick), None while the sword is not shown or its place is not known.
    segs = [(pattern tick, clip)] in order (api.play at that tick: its clip tick 0 is that pattern tick); a clip's ticks before
    its f0 (the sword's first key) are the rig's blend from the pose shown before: known when that pose is, else None (a
    pattern's first clip: the stance she comes from is not known at build time). hidden = pattern ticks of state/hidden (until
    the next clip); last = the last pattern tick wanted."""

    def __init__(self, segs, hidden=(), last=None):
        self.pose, self.clip = {}, {}
        prev = None
        segs = sorted(segs)
        for i, (t0, clip) in enumerate(segs):
            tr = track(clip)
            n, f0 = len(tr['t']) - 1, int(tr.get('f0', 0))
            t1 = segs[i + 1][0] if i + 1 < len(segs) else (t0 + n if last is None else last)
            hid = min((h for h in hidden if t0 <= h and (h < t1 or i + 1 == len(segs))), default=None)
            start = prev
            end = tuple(tr['b'][min(f0, n)]), tuple(tr['t'][min(f0, n)])
            for t in range(t0, t1 + 1):
                ct = min(n, t - t0)
                if hid is not None and t >= hid:
                    p = None
                elif ct >= f0:
                    p = (tuple(tr['b'][ct]), tuple(tr['t'][ct])) if tr['on'][ct] else None
                elif start is not None and tr['on'][min(f0, n)]:
                    p = interp(start, end, ct / f0)
                else:
                    p = None
                self.pose[t] = p
                self.clip[t] = (clip, ct)
            prev = self.pose[t1]

    def known(self, t):
        return self.pose.get(t) is not None


# --- the pieces: the surface the blade sweeps in one tick ------------------------------------------------------------------------
def _fan_scale(r, beta):
    """(sx, sz) of a sw_fan card whose corners stand at the radius r, its half-angle beta deg"""
    k = math.tan(math.radians(beta)) / ARC_TAN
    sa2, ca2 = ARC_TAN ** 2 / (1 + ARC_TAN ** 2), 1 / (1 + ARC_TAN ** 2)
    s = r / math.sqrt(k * k * sa2 + ca2)
    return s * k, s


def sweep(p0, p1, wall=WALL):
    """The pieces of the blade's way from p0 to p1 (one tick of the client's interpolation): [dict(kind 'fan' | 'quad',
    xf0 = (translation, rotation, scale) with no width on the blade's line at p0, xf1 = its full shape, + its geometry for
    the tests: fan: q apex, z axis, n normal, beta, r, u0, u1; quad: c, u, w, n, len)]. A blade that only slid along itself,
    or moved less than MIN_THICK, leaves no piece (the band on the blade is the trail there)."""
    (b0, t0), (b1, t1) = p0, p1
    d0, d1 = unit(sub(t0, b0)), unit(sub(t1, b1))
    phi = angle(d0, d1)
    n = max(1, math.ceil(phi / ARC_STEP - 1e-6))
    out = []
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        (ba, ta), (bb, tb) = interp(p0, p1, u0), interp(p0, p1, u1)
        da, db = unit(sub(ta, ba)), unit(sub(tb, bb))
        ph = angle(da, db)
        nv = cross(da, db)
        pc = None
        if ph >= MIN_TURN and norm(nv) > 1e-6:
            nv = unit(nv)
            # the apex: the point nearest both blade lines
            w0 = sub(ba, bb)
            bq, dd, ee = dot(da, db), dot(da, w0), dot(db, w0)
            den = 1 - bq * bq
            q = lerp(add(ba, mul(da, (bq * ee - dd) / den)), add(bb, mul(db, (ee - bq * dd) / den)), 0.5)
            ra, rb = norm(sub(ta, q)), norm(sub(tb, q))
            ok = min(dot(sub(ta, q), da), dot(sub(tb, q), db)) > 0.3 and max(ra, rb) <= 6.0 and abs(ra - rb) <= 0.22
            if ok:
                z = unit(add(unit(sub(ta, q)), unit(sub(tb, q))))
                beta = angle(sub(ta, q), sub(tb, q)) / 2
                r = (ra + rb) / 2
                if 2 * r * math.sin(math.radians(beta)) >= MIN_THICK:
                    sx, sz = _fan_scale(r, beta)
                    y = nv
                    x = cross(y, z)
                    # no width, on the blade's line of the tick's start (the whole tick's first position: every piece of the
                    # tick opens from there, the last one's leading edge with the blade)
                    z0 = sub(d0, mul(y, dot(d0, y)))
                    z0 = unit(z0) if norm(z0) > 1e-6 else z
                    _sx0, sz0 = _fan_scale(r, 0.0)
                    q0 = sub(t0, mul(z0, r))
                    pc = dict(kind='fan', q=q, z=z, n=nv, beta=beta, r=r, tips=(ta, tb), bases=(ba, bb),
                              xf0=(q0, quat(cross(y, z0), y, z0), (0.0, wall, sz0)), xf1=(q, quat(x, y, z), (sx, wall, sz)))
        if pc is None:
            # no turn about a point of its own line: a strip between the two blade lines (their sideways distance)
            u = unit(add(da, db))
            ma, mb = lerp(ba, ta, 0.5), lerp(bb, tb, 0.5)
            v = sub(mb, ma)
            vp = sub(v, mul(u, dot(v, u)))
            w = norm(vp)
            if w >= MIN_THICK:
                xw = mul(vp, 1 / w)
                y = cross(u, xw)
                ln = (norm(sub(ta, ba)) + norm(sub(tb, bb))) / 2
                c = sub(lerp(ma, mb, 0.5), mul(u, ln / 2))             # the base end's middle
                v0 = sub(lerp(b0, t0, 0.5), ma)                        # (from this piece's start line back to the tick's)
                c0 = add(sub(ma, mul(u, ln / 2)), v0)
                rot = quat(xw, y, u)
                pc = dict(kind='quad', c=c, u=u, x=xw, n=y, w=w, len=ln, tips=(ta, tb), bases=(ba, bb),
                          xf0=(c0, rot, (0.0, wall, ln)), xf1=(c, rot, (w, wall, ln)))
        if pc:
            pc.update(u0=u0, u1=u1)
            out.append(pc)
    return out


def band_xf(p, w=W_BAND):
    b, t = p
    a = lerp(b, t, BAND_FROM)
    d = sub(t, a)
    x, y, z = frame_z(unit(d))
    return a, quat(x, y, z), (w, w, norm(d))


# --- the trail of a pattern ------------------------------------------------------------------------------------------------------
TRAILS = {}               # key -> [dict(uid, shown, t0, t1, col, hot, cond, pieces {t: [piece]}, band [(t0, t1)])] (the tests)


def trail(out, key, uid, shown, t0, t1, col_at, hot_at=None, cond_at=None, lo=0):
    """The band and the pieces of the blade `shown` on the pattern ticks t0 .. t1 into out. col_at(t) = the colour (int) of the
    sweep t -> t + 1; hot_at(t): that sweep belongs to a swing; cond_at(t): an execute condition for the commands of tick t
    (or None); lo: no command before this tick. Returns the record (TRAILS)."""
    hot_at = hot_at or (lambda t: False)
    cond_at = cond_at or (lambda t: None)
    rec = dict(uid=uid, shown=shown, t0=t0, t1=t1, pieces={}, band=[], col={}, hot={})
    # the band: runs of known poses
    t = t0
    while t <= t1:
        if not shown.known(t):
            t += 1
            continue
        e = t
        while e + 1 <= t1 and shown.known(e + 1):
            e += 1
        mine = f'{TR}_{uid}b{t}'
        sel = SEL.format(mine)
        col = col_at(min(t, t1 - 1))
        out.at(t, tcard(key, 'sw_rib_0', band_xf(shown.pose[t]), col, (TR_RIDE, TR_BAND, TR_FAM['rib'], mine)), cond=cond_at(t))
        last = _xf(*band_xf(shown.pose[t]))
        for k in range(t, e):
            xf = _xf(*band_xf(shown.pose[k + 1]))
            c2 = col_at(min(k, t1 - 1))
            extra = ''
            if c2 != col:
                col = c2
                extra = f',item:{{components:{{"minecraft:custom_model_data":{{colors:[{int(col)}]}}}}}}'
            if xf != last or extra:
                out.at(k, f'execute as {sel} run data merge entity @s {{start_interpolation:0,interpolation_duration:1,{xf}{extra}}}',
                       cond=cond_at(k))
                last = xf
        out.at(e + 1, f'kill {sel}', cond=cond_at(e + 1))
        rec['band'].append((t, e))
        t = e + 1
    # the pieces
    for t in range(max(t0, lo + 1), t1):
        if not (shown.known(t) and shown.known(t + 1)):
            continue
        h = bool(hot_at(t))
        pcs = sweep(shown.pose[t], shown.pose[t + 1], WALL_HOT if h else WALL)
        if not pcs:
            continue
        col = hot(col_at(t)) if h else col_at(t)
        grp = f'{TR}_{uid}_{t}'
        gsel = SEL.format(grp)
        for i, pc in enumerate(pcs):
            fam = pc['kind']
            mine = f'{TR}_i{i}'
            out.at(t - 1, tcard(key, f'sw_{fam}_0', pc['xf0'], col, (TR_RIDE, TR_FAM[fam], grp, mine)), cond=cond_at(t - 1))
            out.at(t, f'execute as {SEL.format(grp)[:-1]},tag={mine}] run data merge entity @s {{start_interpolation:0,{_xf(*pc["xf1"])}}}',
                   cond=cond_at(t))
        fams = sorted({pc['kind'] for pc in pcs})
        for dt, fr in FADE:
            for fam in fams:
                s_ = gsel if len(fams) == 1 else f'{gsel[:-1]},tag={TR_FAM[fam]}]'
                out.at(t + dt, _model_cmd(s_, f'sw_{fam}_{fr}'), cond=cond_at(t + dt))
        out.at(t + LIFE, f'kill {gsel}', cond=cond_at(t + LIFE))
        rec['pieces'][t] = pcs
        rec['col'][t], rec['hot'][t] = col, h
    TRAILS.setdefault(key, []).append(rec)
    return rec


def detach():
    """The riding cards stay where they are from now on (she vanishes / is put elsewhere): their fading goes on in place."""
    return f'tag {SEL.format(TR_RIDE)} remove {TR_RIDE}'


RIDE_CMD = f'execute rotated as @s rotated ~ 0 run tp {SEL.format(TR_RIDE)} ~ ~ ~ ~ ~'     # the core's hook, after rig/tick


# --- the ribbon: her body carries the blade ---------------------------------------------------------------------------------------
STO = f'{api.STORAGE} core.sw'
RIBS = {}                 # key -> [dict(uid, t0, t1, col, cond)] (the tests)


def runtime(W, fn, sset):
    """core/sw/{rib,rib1}: the run-time part of the ribbon (written once by p1.py)."""
    o = api.OBJ
    tgt = f'@e[type=minecraft:marker,tag={TR_TGT},limit=1]'
    W.w('core/sw/rib', [
        '# The growing ribbon (blade.py; rlk_hr_trg: one at a time) to here: its far end stays where the move began, it turns to',
        '# this point and becomes as long as the way to it (one tick of interpolation: it grows behind her as her model moves).',
        f'summon minecraft:marker ~ ~ ~ {{Tags:["{TR_TGT}","rlk_room","rlk_mb_aux"]}}',
        f'execute as {SEL.format(TR_GROW)} at @s facing entity {tgt} feet run function {api.NS}core/sw/rib1',
        f'kill @e[type=minecraft:marker,tag={TR_TGT}]'])
    W.w('core/sw/rib1', [
        '# @s = the ribbon, at it, facing the target marker: turn there; its length = (target - its place) . its aim.',
        'tp @s ~ ~ ~ ~ ~',
        f'execute store result score #sw_x {o} run data get entity {tgt} Pos[0] 1000',
        f'execute store result score #sw_y {o} run data get entity {tgt} Pos[1] 1000',
        f'execute store result score #sw_z {o} run data get entity {tgt} Pos[2] 1000',
        f'execute store result score #sw_n {o} run data get entity @s Pos[0] 1000',
        f'scoreboard players operation #sw_x {o} -= #sw_n {o}',
        f'execute store result score #sw_n {o} run data get entity @s Pos[1] 1000',
        f'scoreboard players operation #sw_y {o} -= #sw_n {o}',
        f'execute store result score #sw_n {o} run data get entity @s Pos[2] 1000',
        f'scoreboard players operation #sw_z {o} -= #sw_n {o}',
        f'execute positioned 0.0 0.0 0.0 run tp {tgt} ^ ^ ^1',
        f'execute store result score #sw_n {o} run data get entity {tgt} Pos[0] 1000',
        f'scoreboard players operation #sw_x {o} *= #sw_n {o}',
        f'execute store result score #sw_n {o} run data get entity {tgt} Pos[1] 1000',
        f'scoreboard players operation #sw_y {o} *= #sw_n {o}',
        f'execute store result score #sw_n {o} run data get entity {tgt} Pos[2] 1000',
        f'scoreboard players operation #sw_z {o} *= #sw_n {o}',
        f'scoreboard players operation #sw_x {o} += #sw_y {o}',
        f'scoreboard players operation #sw_x {o} += #sw_z {o}',
        f'execute if score #sw_x {o} matches ..0 run return 0',
        f'execute store result entity @s transformation.scale[2] float 0.000001 run scoreboard players get #sw_x {o}'])


def hand(shown, t):
    """The point of her frame the ribbon follows at pattern tick t: her sword hand (the blade's base); not shown: chest high."""
    p = shown.pose.get(t) if shown is not None else None
    return p[0] if p else (0.0, 1.1, 0.25)


def ribbon(out, key, uid, shown, ta, tb, col, cond=None, w=RIB_W, seg=99):
    """The ribbon of a body move (mv/glide, mv/leap called at pattern tick ta, the body there at tb): it starts where her hand
    is at ta and is sent on each of ta + 1 .. tb to the hand's place of the next tick (@s = the body, moved by mv/all before
    the pattern tick: where her model goes during this tick). seg: a new piece every seg ticks (a curved way). After tb it
    fades through the frames and is gone RIB_LIFE t later."""
    def at_hand(t):
        return f'at @s rotated as @s rotated ~ 0 positioned {car(hand(shown, t))}'
    starts = list(range(ta, tb, seg))
    for i, s in enumerate(starts):
        e = min(tb, s + seg)
        mine = f'{TR}_{uid}r{s}'
        sel = SEL.format(mine)
        # (a ribbon piece does not ride: it lies in the world; billboard fixed, its length along its own +z)
        out.at(s, f'tag {SEL.format(TR_GROW)} remove {TR_GROW}',
               f'execute {at_hand(s + (1 if i else 0))} run ' + tcard(key, 'sw_rib_0', ((0, 0, 0), (0, 0, 0, 1), (w, w, 0.0)), col, (TR_RIB, TR_FAM['rib'], TR_GROW, mine), tpd=0),
               cond=cond)
        for t in range(s + 1, e + 1):
            out.at(t, f'execute {at_hand(t + 1)} run function {api.NS}core/sw/rib', cond=cond)
        out.at(e + 1, f'tag {sel} remove {TR_GROW}', cond=cond)
        out.at(e + 2, _model_cmd(sel, 'sw_rib_1'), cond=cond)
        out.at(e + 4, _model_cmd(sel, 'sw_rib_2'), cond=cond)
        out.at(e + RIB_LIFE, f'kill {sel}', cond=cond)
    RIBS.setdefault(key, []).append(dict(uid=uid, t0=ta, t1=tb, col=col, cond=cond, seg=seg))
    return tb + RIB_LIFE


def wave(out, key, uid, h, col, where, length=None, store=None, w=WAVE_W, cond=None):
    """The struck line of a hit that reaches farther than her blade (a dash-through's line, kcut's crossing lines): a band left
    in the world ON the hit tick h, WAVE_LIFE t. where = execute subcommands for its start and aim; its length a number, or
    store = the fake player holding it in half blocks (a dash's probed length)."""
    mine = f'{TR}_{uid}w'
    sel = SEL.format(mine)
    out.at(h, f'execute {where} run ' + tcard(key, 'sw_rib_0', ((0, 0, 0), (0, 0, 0, 1), (w, w, length or 0.0)), col, (TR_FAM['rib'], TR_NEW, mine), tpd=0, ipd=0),
           f'execute {where} run tp {SEL.format(TR_NEW)} ~ ~ ~ ~ ~', cond=cond)
    if store:
        out.at(h, f'execute as {SEL.format(TR_NEW)} store result entity @s transformation.scale[2] float 0.5 run scoreboard players get {store} {api.OBJ}',
               cond=cond)
    out.at(h, f'tag {SEL.format(TR_NEW)} remove {TR_NEW}', cond=cond)
    out.at(h + 2, _model_cmd(sel, 'sw_rib_1'), cond=cond)
    out.at(h + 3, _model_cmd(sel, 'sw_rib_2'), cond=cond)
    out.at(h + WAVE_LIFE, f'kill {sel}', cond=cond)
    WAVES.setdefault(key, []).append(dict(uid=uid, hit=h, col=col))


WAVES = {}


# --- a pattern's hits -------------------------------------------------------------------------------------------------------------
def colour_of(key, idx):
    """The trail colour of api.HITS[key][idx]: white-gold for a parryable hit, else its (group's) last flash's colour."""
    row = api.HITS[key][idx]
    if row[6] == 'P':
        return COL['P'], 'P'
    fl = api.FLASH_AT[key].get(idx) or next(v for v in api.FLASH_AT[key].values() if v)
    return COL[fl[-1][0]], fl[-1][0]


def hits_on(key, t0_of=None):
    """[(pattern tick of the hit, Swing, colour, colour name, HITS index, clip tick 0's pattern tick)] of a P1 / P2 pattern,
    one per clip event."""
    out, seen = [], set()
    for i, row in enumerate(api.HITS[key]):
        clip, ev = row[0], row[1]
        if (clip, ev) in seen:
            continue
        seen.add((clip, ev))
        c0 = (t0_of or {}).get(clip, 0)
        sw = swing_of(clip, ev)
        col, name = colour_of(key, i)
        out.append((c0 + sw.h, sw, col, name, i, c0))
    return out


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
