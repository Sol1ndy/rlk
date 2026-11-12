"""Painted sprites and HUD glyphs of the 홍련 (Scarlet) fx kit (tools/build_mboss_hr_fx.py). Stdlib only, deterministic
(fixed seeds).

Her effects (scratchpad hr/PLAN.md §1.3, §4.1): lilac sword-qi (#C97EDD body, a white-pink #FFE6FA cutting rim, fading
0.3-0.8 s): crescents, rings, bands, the X, the dome; the lilac ghost form, its mist and ribbons; the yellow tell
(#FFE14A sphere + flare line); the white / pink glints; the A7 moon disc; the pale blue-white back-blink bubble; the red
slash line and the petal burst of 홍련일섬; the gold clash bursts (blade on blade only) and the cyan-gold kick flash (CS2
R8 only). The player's own effects (orange / gold parry streaks, white-cyan crescents) are not painted here.

Card coordinates follow the fg / Apep / Tachy / Arlecchino kits: every painter takes (a, b) inside its kind's painter box
(a = texture left -> right, b = texture bottom -> top) and returns straight-alpha (r, g, b, alpha) floats. Sprites the kit
tints per colour (`c` 1 lilac .. 5 white) are painted neutral (white / grey: the item tint multiplies them); the
sword-qi sprites are painted lilac with a white-pink rim and tinted only for the other colours.

The helpers (noise, polylines, ramps) are copies of the Arlecchino painter's, so the kits can change apart.
"""
import math
import random


def hexc(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def mix(a, b, t):
    t = clamp01(t)
    if isinstance(a, str):
        a = hexc(a)
    if isinstance(b, str):
        b = hexc(b)
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def ramp(stops, t):
    """Piecewise-linear colour ramp; stops = [(t, rgb), ...] ascending."""
    if t <= stops[0][0]:
        return stops[0][1]
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            return mix(c0, c1, (t - t0) / (t1 - t0))
    return stops[-1][1]


def smooth(e0, e1, x):
    t = (x - e0) / (e1 - e0)
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return t * t * (3 - 2 * t)


def rmp(*pairs):
    return [(t, hexc(h)) for t, h in pairs]


CLEAR = (0.0, 0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)

_R = random.Random(20261105)
_H = [_R.random() for _ in range(256)]
_P = list(range(256))
_R.shuffle(_P)


def _lat(ix, iy):
    return _H[_P[(_P[ix & 255] + iy) & 255]]


def vnoise(x, y):
    ix, iy = math.floor(x), math.floor(y)
    fx, fy = x - ix, y - iy
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)
    a, b = _lat(ix, iy), _lat(ix + 1, iy)
    c, d = _lat(ix, iy + 1), _lat(ix + 1, iy + 1)
    return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy


def fbm(x, y, octaves=3):
    s, amp, f, tot = 0.0, 0.5, 1.0, 0.0
    for _ in range(octaves):
        s += amp * vnoise(x * f, y * f)
        tot += amp
        amp *= 0.5
        f *= 2.03
    return s / tot


def seg_dist(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    t = clamp01(((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy + 1e-12))
    return math.hypot(px - ax - vx * t, py - ay - vy * t)


def poly_dist(px, py, pts):
    return min(seg_dist(px, py, ax, ay, bx, by) for (ax, ay), (bx, by) in zip(pts, pts[1:]))


def jag(rnd, x0, y0, x1, y1, n, amp):
    """jagged polyline from (x0, y0) to (x1, y1): n segments, lateral jitter amp (fraction of the length)"""
    dx, dy = x1 - x0, y1 - y0
    ln = math.hypot(dx, dy) + 1e-9
    nx, ny = -dy / ln, dx / ln
    pts = [(x0, y0)]
    for k in range(1, n):
        t = k / n
        j = rnd.uniform(-amp, amp) * ln
        pts.append((x0 + dx * t + nx * j, y0 + dy * t + ny * j))
    pts.append((x1, y1))
    return pts


def over(top, bot):
    """straight-alpha 'top over bot'"""
    ta, ba = top[3], bot[3]
    a = ta + ba * (1 - ta)
    if a <= 1e-6:
        return CLEAR
    return tuple((top[i] * ta + bot[i] * ba * (1 - ta)) / a for i in range(3)) + (a,)


def glow(d, w, peak=1.0):
    """a soft falloff 1 at d = 0 -> 0 at d >= w"""
    if d >= w:
        return 0.0
    t = 1 - d / w
    return peak * t * t


# ----------------------------------------------------------------------------- the palette (PLAN §4.1)
LILAC = hexc('#C97EDD')
LILAC_DEEP = hexc('#8C52B8')
LILAC_PALE = hexc('#EBCBF6')
RIM = hexc('#FFE6FA')
MAGENTA = hexc('#E040A0')
YELLOW = hexc('#FFE14A')
CRIMSON = hexc('#E0203E')
GOLD = hexc('#FFC84A')
QI = rmp((0.0, '#FFF4FD'), (0.18, '#FFE6FA'), (0.42, '#E2A8F0'), (0.7, '#C97EDD'), (1.0, '#8C52B8'))
GREYS = rmp((0.0, '#FFFFFF'), (0.5, '#E6E6E6'), (1.0, '#B4B4B4'))      # neutral (tinted) sprites


def _qi(d, alpha):
    """colour + alpha at the normalised distance d (0 = the cutting rim, 1 = the far body edge) of a sword-qi band"""
    if d >= 1.3 or alpha <= 0:
        return CLEAR
    return ramp(QI, min(1.0, d)) + (alpha * (1 - smooth(0.78, 1.28, d)),)


# ----------------------------------------------------------------------------- qi_arc: the crescent sweep (flat, a -1..1, b 0..1)
ARC_T0, ARC_T1 = -78.0, 78.0          # sweep bearings (degrees from +b toward +a); the kit's floor clamp uses +-80
ARC_RC = 0.80                         # the rim radius (unit radius = the reach at scale r)
ARC_F = (0.36, 0.62, 0.86, 1.0)       # head position of frames 0..3 (fraction of the sweep)


def make_arc(k):
    """qi_arc sweep frame k: a lilac sword-qi crescent whose outer edge (the cutting rim, white-pink) sits on radius ARC_RC,
    the body thinning inward; from the start bearing up to the head of frame k (thick white-hot head, thin fading
    tail); frame 3 = the whole crescent, the tail faded."""
    th = ARC_T0 + (ARC_T1 - ARC_T0) * ARC_F[k]

    def paint(a, b):
        r = math.hypot(a, b)
        if r < 0.40 or r > 1.0:
            return CLEAR
        ph = math.degrees(math.atan2(a, b))
        if ph < ARC_T0 - 3 or ph > th + 4:
            return CLEAR
        u = clamp01((ph - ARC_T0) / (th - ARC_T0))
        fac = (0.25 + 0.75 * u) if k < 3 else smooth(0.0, 0.6, u) * (1 - 0.35 * smooth(0.7, 1.0, u))
        tip = clamp01((th + 4 - ph) / 9.0)
        width = (0.06 + 0.17 * math.sin(math.pi * min(1.0, 0.15 + 0.85 * u)) ** 0.7) * (0.35 + 0.65 * tip)
        n = fbm(ph * 0.08 + 5.1 * k, r * 6.0)
        dr = ARC_RC + 0.012 - r                    # 0 at the rim, growing inward
        if dr < -0.03:
            return (RIM + (glow(-dr - 0.03, 0.05, 0.55 * fac),)) if fac > 0 else CLEAR
        d = max(0.0, dr) / (width * (0.75 + 0.5 * n) + 1e-6)
        col = _qi(d, fac * (0.95 if d < 0.25 else 0.85))
        if col[3] <= 0:
            return CLEAR
        streak = 0.18 * smooth(0.55, 0.9, fbm(ph * 0.35, r * 18.0 + k)) * (1 - d)
        return (min(1.0, col[0] + streak), min(1.0, col[1] + streak), min(1.0, col[2] + streak), col[3])
    return paint


# ----------------------------------------------------------------------------- qi_ring (flat, unit radius)
def paint_ring(a, b):
    """qi_ring frame 0: the flat lilac sword-qi ring (the rim at r 0.93, the body inward to ~0.66), streaked."""
    r = math.hypot(a, b)
    if r > 1.0 or r < 0.55:
        return CLEAR
    ph = math.atan2(a, b)
    n = fbm(math.cos(ph) * 3 + 7, math.sin(ph) * 3 + r * 5)
    dr = 0.935 - r
    if dr < 0:
        return RIM + (glow(-dr, 0.06, 0.8),)
    d = dr / (0.20 + 0.10 * n)
    return _qi(d, 0.9)


def paint_ring_rim(a, b):
    """qi_ring frame 1: the thin white-pink rim (r 0.95) with three swirl arcs inside (the dome's rim, the spin's
    outline)."""
    r = math.hypot(a, b)
    if r > 1.0 or r < 0.5:
        return CLEAR
    al = glow(abs(r - 0.95), 0.045, 1.0)
    ph = math.atan2(a, b)
    for k in range(3):
        c = 0.80 - 0.07 * k
        s = (ph + 2.1 * k) % (2 * math.pi)
        if s < 2.2:
            al = max(al, glow(abs(r - c), 0.02, 0.55 * (1 - s / 2.2)))
    if al <= 0.02:
        return CLEAR
    return mix(RIM, LILAC_PALE, smooth(0.9, 0.7, r)) + (al,)


# ----------------------------------------------------------------------------- bands, ribbons, trails (long along a)
def paint_band(a, b):
    """qi_band frame 0: a broad lilac sword-qi band (a -1..1 the length, b -0.25..0.25 the height): tapered at both
    ends, the upper edge the bright white-pink rim, the body lilac, wispy at the lower edge."""
    u = (a + 1) / 2
    half = 0.25 * math.sin(math.pi * clamp01(u)) ** 0.55
    if half <= 0.005:
        return CLEAR
    top = half * (0.92 + 0.06 * math.sin(a * 7.0))
    n = fbm(a * 6.0 + 2.0, b * 9.0)
    lo = -half * (0.55 + 0.45 * n)
    if b > top + 0.03 or b < lo:
        return CLEAR
    if b > top:
        return RIM + (glow(b - top, 0.03, 0.7),)
    d = (top - b) / (top - lo + 1e-6)
    return _qi(d * 1.05, 0.92 * smooth(0.0, 0.08, u) * smooth(1.0, 0.92, u))


def paint_band_edge(a, b):
    """qi_band frame 1: the leading streak of the band: a thin bright white-pink line with a lilac glow, tapered."""
    u = (a + 1) / 2
    w = 0.05 * math.sin(math.pi * clamp01(u)) ** 0.4
    d = abs(b - 0.06 * math.sin(a * 2.2))
    al = glow(d, w + 0.06, 1.0) * smooth(0.0, 0.1, u) * smooth(1.0, 0.85, u)
    if al <= 0.02:
        return CLEAR
    return mix(RIM, LILAC, smooth(w * 0.5, w + 0.05, d)) + (al,)


def make_ribbon(k):
    """qi_ribbon frame k: a flowing lilac ribbon (a -1..1 the length, b -0.25..0.25), a sine strip with a white edge;
    frame 1 thinner and broken (the ribbon's fading end)."""
    def paint(a, b):
        u = (a + 1) / 2
        c = 0.11 * math.sin(a * 3.4 + 0.9 * k)
        half = (0.085 if k == 0 else 0.055) * (0.5 + 0.5 * math.sin(math.pi * clamp01(u)))
        d = abs(b - c)
        if d > half + 0.03:
            return CLEAR
        if k == 1 and fbm(a * 4.0 + 9.0, 1.3) < 0.42:
            return CLEAR
        fade = smooth(0.0, 0.15, u) * smooth(1.0, 0.8, u)
        if d > half:
            return RIM + (glow(d - half, 0.03, 0.6 * fade),)
        return _qi(0.15 + 0.8 * d / half, 0.9 * fade)
    return paint


def paint_trail(a, b):
    """ghost_trail frame 0 (a 0..1 from the tail to the head, b -0.125..0.125): the lilac flame trail of a ghost dash:
    wide and bright at the head (a 1), licking flames thinning back to the tail."""
    half = 0.11 * (0.25 + 0.75 * a ** 0.7)
    n = fbm(a * 9.0 + 3.0, b * 30.0)
    edge = half * (0.6 + 0.6 * n)
    d = abs(b) / (edge + 1e-6)
    if d > 1.25:
        return CLEAR
    al = 0.9 * smooth(0.0, 0.25, a) * (1 - smooth(0.85, 1.25, d))
    col = mix(mix(RIM, LILAC, d), LILAC_DEEP, smooth(0.6, 1.2, d) * (1 - a))
    return col + (al,)


def paint_speedlines(a, b):
    """ghost_trail frame 1: white speed lines (five thin streaks of different lengths)."""
    al = 0.0
    for k, (y, s, e) in enumerate(((-0.08, 0.2, 0.95), (-0.035, 0.45, 1.0), (0.0, 0.1, 0.85), (0.04, 0.35, 0.98),
                                   (0.085, 0.55, 1.0))):
        if s <= a <= e:
            f = smooth(s, s + 0.2, a) * smooth(e, e - 0.05, a)
            al = max(al, glow(abs(b - y), 0.012, f))
    if al <= 0.03:
        return CLEAR
    return mix(WHITE, LILAC_PALE, 0.25) + (al,)


# ----------------------------------------------------------------------------- dome, wedge
def paint_dome(a, b):
    """qi_dome (face, a -1..1, b 0..1): a translucent lilac dome silhouette with a thin white outline (the spin dome)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    edge = glow(abs(r - 0.965), 0.035, 1.0)
    base = glow(b, 0.03, 0.6)
    fill = 0.18 + 0.22 * smooth(0.55, 0.95, r) + 0.08 * fbm(a * 4, b * 4)
    top = (WHITE + (edge,)) if edge > 0.05 else CLEAR
    body = mix(LILAC_PALE, LILAC, 0.4) + (min(1.0, fill + base),)
    return over(top, body)


def paint_wedge(a, b):
    """qi_wedge (flat, a -0.25..0.25 the width, b 0..1 the length): a lilac sword-qi spearhead, the point at b 1, the
    wide base at b ~0.12 fading back to b 0, white edges."""
    half = 0.24 * clamp01((1.0 - b) / 0.88) * smooth(0.0, 0.12, b)
    if half <= 0.002 or abs(a) > half + 0.02:
        return CLEAR
    d = abs(a) / (half + 1e-6)
    if d > 1.0:
        return RIM + (glow((abs(a) - half), 0.02, 0.7),)
    col = _qi((1 - d) * 0.9, 0.9)
    return col[:3] + (col[3] * smooth(0.0, 0.25, b),)


# ----------------------------------------------------------------------------- glints, shards (neutral: tinted)
def paint_glint(a, b):
    """glint frame 0: a four-ray sparkle with a soft core (neutral white; the card tints it)."""
    r = math.hypot(a, b)
    core = glow(r, 0.35, 1.0)
    ray = max(glow(abs(a), 0.07 * (1 - min(1, abs(b))), 1.0) * (1 - abs(b)) ** 1.5,
              glow(abs(b), 0.07 * (1 - min(1, abs(a))), 1.0) * (1 - abs(a)) ** 1.5)
    diag = 0.5 * max(glow(abs(a - b) / 1.414, 0.04, 1.0), glow(abs(a + b) / 1.414, 0.04, 1.0)) * (1 - r) ** 2
    al = max(core, ray, diag)
    if al < 0.05:
        return CLEAR
    return ramp(GREYS, 0.6 * smooth(0.0, 0.8, r)) + (al,)


CUE_GOLD = hexc('#FFD878')
SW_INK = hexc('#1C0B2E')               # round V: the dark rim of every tell (a tint multiplies it: it stays dark)


def paint_cue(a, b):
    """cue frame 0 (HA-07, review H-A: the parry cue at her blade): a white-gold sparkle that reads from the F5 camera on
    the crimson P2 field: a bright white core with a warm gold rim, four long white rays that reach the card's edge (alpha
    >= 0.5 to 80 % of the half-width) and four short diagonal rays; painted in colour (the kit tints it white). Unlike
    glint_0 (a soft dot whose rays fade at a third of the card) it fills the card it is given."""
    r = math.hypot(a, b)

    def ray(u, v, reach, w0):
        t = abs(u) / reach
        if t >= 1:
            return 0.0
        return glow(abs(v), w0 * (1 - t) ** 0.7 + 0.03, 1.0) * (1 - t ** 4)
    d1, d2 = (a + b) / 1.4142, (a - b) / 1.4142
    core = glow(r, 0.27, 1.0)
    halo = 0.6 * glow(r, 0.45, 1.0)
    main = max(ray(a, b, 0.99, 0.13), ray(b, a, 0.99, 0.13))
    diag = 0.9 * max(ray(d1, d2, 0.62, 0.09), ray(d2, d1, 0.62, 0.09))
    al = max(core, halo, main, diag)
    if al < 0.04:
        return CLEAR
    # round V (lane VB; review v C2): a dark rim round the star's body (the core and the rays) - where the old sprite faded out
    # softly into whatever was behind it (her white hat, the pale straw grass of the P1 field) it now ends in ink
    shape = max(core, main, diag)
    if 0.08 <= shape < 0.42:
        return SW_INK + (0.9,)
    gold = smooth(0.06, 0.22, r) * (1 - smooth(0.3, 0.55, r)) + 0.35 * smooth(0.55, 1.0, r)
    if shape >= 0.42:
        return mix(WHITE, CUE_GOLD, gold) + (1.0,)
    return mix(WHITE, CUE_GOLD, gold) + (min(1.0, al * 0.6),)


# ---- round V (lane VB) / round W (lane WB; w_brief.md §2 WB): the blade's trail ---------------------------------------------------
# All are neutral (white, tinted per hit) with a DARK rim: a tell must read on the pale straw grass and her white hat of the P1
# field as well as on the crimson P2 field (review v C2; review w T3-08: round V's white-gold line was lost on the P1 wheat).
SW_CORE = 0.56                         # the band / ribbon's bright core: this share of the card's width (blade.RIB_CORE); ink
#                                        on both sides of it (each 0.18 of the width): it reads on the pale P1 wheat by its border
SW_ARC_TAN = 0.5                       # the sector's edges: a = +-SW_ARC_TAN b (blade.ARC_TAN)
SW_ALPHA = (1.0, 0.62, 0.3)            # the fading frames
# the swept piece (sector / strip): a bright ribbon along the tip's way (the outer RIBBON of the radius / the strip's length),
# ink at its outer edge, and only a faint fill inward (review w T3-11: round V's full translucent sheet covered up to 45 % of
# the frame when she cut near the camera)
SW_RIB_IN, SW_RIB_OUT, SW_FILL_IN, SW_INK_W = 0.68, 0.92, 0.42, 0.06   # ink at both edges of the ribbon


def make_sw_rib(k):
    """sw_rib frame k (a lance card, a across its width -0.5 .. 0.5, b along its length: the band on the blade, a ribbon behind
    her, a struck line, a piece's rim wall): a solid bright core SW_CORE of the width, a dark rim, even along its length; frames
    1, 2 = the same at SW_ALPHA (the fade)."""
    A = SW_ALPHA[k]

    def paint(a, b):
        x = abs(a) * 2
        if x <= SW_CORE:
            return WHITE + (A,)
        if x <= 0.92:
            return SW_INK + (0.9 * A,)
        return SW_INK + (0.9 * A * (1 - smooth(0.92, 1.0, x)),)
    return paint


def _swept(r, A):
    """the swept piece's profile at r (the share of the tip's radius / the strip's length from the blade's base)"""
    if r > 1.0 or r < SW_FILL_IN:
        return CLEAR
    if r >= SW_RIB_OUT:
        return SW_INK + (0.9 * A,)
    if r >= SW_RIB_IN:
        return WHITE + (A,)
    if r >= SW_RIB_IN - SW_INK_W:
        return SW_INK + (0.8 * A,)
    t = (r - SW_FILL_IN) / (SW_RIB_IN - SW_INK_W - SW_FILL_IN)
    return mix(hexc('#D8D8D8'), WHITE, t) + (A * (0.12 + 0.3 * t),)


def make_sw_arc(k):
    """sw_arc frame k (sw_fan's swept wedge: a flat card, the apex at a 0 b 0, the axis along b): the chord b = 1 between its
    corners (the tips of the two blade positions) as a bright ribbon with ink outside it, a faint fill inward; cut hard on the two
    edges a = +-SW_ARC_TAN b so that the pieces of a sweep close up; frames 1, 2 = the same at SW_ALPHA (the fade). (The rim is
    the chord, not a circle: the card is squeezed across to each piece's angle, and a circle would bulge past the tip's way.)"""
    A = SW_ALPHA[k]

    def paint(a, b):
        if b <= 0 or abs(a) > SW_ARC_TAN * b:
            return CLEAR
        return _swept(b, A)
    return paint


def make_sw_quad(k):
    """sw_quad frame k (sw_quad's strip between two blade lines: a flat card, a across the way, b from the blade's base 0 to the
    tip 1): the same profile as the sector along b."""
    A = SW_ALPHA[k]

    def paint(a, b):
        return _swept(b, A)
    return paint


def paint_sw_head(a, b):
    """sw_head (round V's path head; now the flashes' rimmed star only): a round white core, four short rays, a dark rim."""
    r = math.hypot(a, b)
    ang = math.atan2(b, a)
    reach = 0.42 + 0.44 * abs(math.cos(2 * ang)) ** 8
    if r <= reach:
        return WHITE + (1.0,)
    if r <= reach + 0.13:
        return SW_INK + (0.92,)
    return SW_INK + (0.92 * (1 - smooth(reach + 0.13, reach + 0.2, r)),)


def paint_star4(a, b):
    """glint frame 1 (star4): a slim four-point star inside a thin circle (A9's chest star; neutral)."""
    r = math.hypot(a, b)
    ang = math.atan2(b, a)
    k = abs(math.cos(2 * ang))
    reach = 0.18 + 0.78 * k ** 6
    star = (1 - smooth(reach - 0.05, reach + 0.02, r)) if r < reach + 0.05 else 0.0
    ring = glow(abs(r - 0.82), 0.035, 0.9)
    al = max(star, ring)
    if al < 0.05:
        return CLEAR
    return ramp(GREYS, 0.5 * r) + (al,)


def make_shard(k):
    """shards frame 0 (shield_refill): an elongated crystal shard with a bright facet; frame 1 (pip_break): a broken
    splinter. Neutral (tinted lilac)."""
    rnd = random.Random(70 + k)
    if k == 0:
        pts = [(0.0, 0.95), (0.32, 0.1), (0.0, -0.95), (-0.28, 0.0)]
    else:
        pts = [(-0.1, 0.9), (0.45, 0.35), (0.15, -0.2), (0.3, -0.85), (-0.35, -0.3), (-0.2, 0.2)]
    pts = [(x + rnd.uniform(-0.03, 0.03), y + rnd.uniform(-0.03, 0.03)) for x, y in pts]

    def inside(px, py):
        c = False
        for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
            if (y0 > py) != (y1 > py) and px < x0 + (py - y0) * (x1 - x0) / (y1 - y0):
                c = not c
        return c

    def paint(a, b):
        dist = poly_dist(a, b, pts + pts[:1])
        if inside(a, b):
            facet = 0.85 + 0.15 * (1 if a * 0.6 + b * 0.4 > 0 else 0)
            return ramp(GREYS, 0.5 * (1 - facet) + 0.2 * smooth(0.0, 0.2, dist)) + (0.95,)
        al = glow(dist, 0.12, 0.55)
        return (WHITE + (al,)) if al > 0.04 else CLEAR
    return paint


# ----------------------------------------------------------------------------- lotus (bud / bloom), face, b -1 = the base
def paint_lotus_bud(a, b):
    """lotus frame 0: a closed lotus bud standing on two small pads (pale pink, darker tips), base at b -1."""
    pad = glow(math.hypot(a / 1.0, (b + 0.85) / 0.16), 1.0, 1.0) if b < -0.6 else 0.0
    y = (b + 0.75) / 1.55                 # 0 .. 1 up the bud
    half = 0.42 * math.sin(math.pi * clamp01(y) ** 0.85) * (1 - 0.25 * y)
    if 0 <= y <= 1 and abs(a) <= half:
        t = abs(a) / (half + 1e-6)
        col = mix(hexc('#FFF0F6'), hexc('#F2A6C4'), 0.4 * t + 0.6 * smooth(0.55, 1.0, y))
        if abs(a) < 0.03 * (1 - y):
            col = mix(col, hexc('#E07AA6'), 0.5)
        return col + (0.97,)
    if pad > 0.3:
        return mix(hexc('#2E5A36'), hexc('#5E8A4E'), clamp01(a * 0.5 + 0.5)) + (0.95,)
    return CLEAR


def paint_lotus_bloom(a, b):
    """lotus frame 1: an open crimson lotus (P2): fanned petals, a golden seed head, pads at the base."""
    pad = glow(math.hypot(a / 1.0, (b + 0.85) / 0.16), 1.0, 1.0) if b < -0.6 else 0.0
    cx, cy = 0.0, -0.35
    dx, dy = a - cx, b - cy
    r = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dx, dy))
    if dy > -0.15 and r < 0.92:
        best = 0.0
        for k in range(-3, 4):
            ca = k * 24.0
            da = abs(ang - ca)
            w = 11.0 * (1 - 0.35 * abs(k) / 3)
            ln = 0.9 - 0.12 * abs(k)
            if da < w and r < ln:
                best = max(best, (1 - da / w) * (1 - r / ln * 0.3))
        if best > 0:
            tip = smooth(0.3, 0.85, r)
            col = mix(hexc('#FF7A92'), hexc('#B0102E'), 0.5 * tip + 0.3 * (1 - best))
            if r < 0.2:
                col = mix(hexc('#FFD45A'), col, smooth(0.08, 0.2, r))
            return col + (0.97,)
    if r < 0.18:
        return hexc('#FFD45A') + (0.97,)
    if pad > 0.3:
        return mix(hexc('#2E3A2A'), hexc('#4E5A3A'), clamp01(a * 0.5 + 0.5)) + (0.95,)
    return CLEAR


# ----------------------------------------------------------------------------- the yellow tell
def paint_tell_sphere(a, b):
    """yellow_tell frame 0: the yellow tell sphere (white core, #FFE14A, a soft halo)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    if r < 0.55:
        return mix(WHITE, YELLOW, smooth(0.0, 0.5, r)) + (1.0,)
    return YELLOW + (glow(r - 0.55, 0.45, 0.85),)


def paint_tell_flare(a, b):
    """yellow_tell frame 1 (a -1..1, b -0.125..0.125): the horizontal flare line through the sphere."""
    w = 0.03 + 0.06 * (1 - abs(a)) ** 2
    al = glow(abs(b), w + 0.03, 1.0) * (1 - abs(a)) ** 0.7
    if al < 0.04:
        return CLEAR
    return mix(WHITE, YELLOW, smooth(0.0, 0.6, abs(a)) * 0.8 + smooth(w * 0.4, w, abs(b)) * 0.4) + (al,)


# ----------------------------------------------------------------------------- the ghost: mist, ribbons, sparkles, flash, bubble
def make_ghost(k):
    """ghost_burst frame k: 0 a lilac-white mist puff, 1 white-lilac ribbon strands (the silhouette traced), 2 sparkles."""
    rnd = random.Random(90 + k)
    if k == 0:
        def paint(a, b):
            r = math.hypot(a, b)
            n = fbm(a * 2.8 + 4.0, b * 2.8 + 1.0)
            al = (1 - smooth(0.35 + 0.35 * n, 0.95, r)) * 0.8
            if al < 0.05:
                return CLEAR
            return mix(WHITE, LILAC, 0.25 + 0.6 * smooth(0.0, 0.9, r)) + (al,)
        return paint
    if k == 1:
        strands = []
        for i in range(4):
            ph = rnd.uniform(0, 6.28)
            strands.append([(0.85 * math.sin(ph + t * 2.4) * (1 - 0.4 * t), -0.9 + 1.8 * t) for t in [j / 12 for j in range(13)]])

        def paint(a, b):
            d = min(poly_dist(a, b, s) for s in strands)
            al = glow(d, 0.08, 0.95)
            if al < 0.05:
                return CLEAR
            return mix(WHITE, LILAC, smooth(0.0, 0.08, d)) + (al,)
        return paint
    pts = [(rnd.uniform(-0.8, 0.8), rnd.uniform(-0.8, 0.8), rnd.uniform(0.12, 0.25)) for _ in range(7)]

    def paint(a, b):
        al = 0.0
        for x, y, s in pts:
            dx, dy = abs(a - x), abs(b - y)
            al = max(al, glow(dx, 0.03, 1.0) * (1 - min(1, dy / s)) ** 2, glow(dy, 0.03, 1.0) * (1 - min(1, dx / s)) ** 2,
                     glow(math.hypot(dx, dy), s * 0.35, 1.0))
        if al < 0.05:
            return CLEAR
        return mix(WHITE, LILAC_PALE, 0.3) + (al,)
    return paint


_GF = random.Random(31)
GF_BOLTS = [jag(_GF, 0, 0, 0.95 * math.sin(t), 0.95 * math.cos(t), 6, 0.18) for t in [k * 2 * math.pi / 7 + 0.3 for k in range(7)]]


def paint_ghost_flash(a, b):
    """ghost_flash: a white-violet electric flash (D3): a hot core and seven jagged rays."""
    r = math.hypot(a, b)
    core = glow(r, 0.4, 1.0)
    d = min(poly_dist(a, b, p) for p in GF_BOLTS)
    ray = glow(d, 0.05, 1.0) * (1 - 0.6 * r)
    al = max(core, ray)
    if al < 0.05:
        return CLEAR
    return mix(WHITE, hexc('#B98CFF'), 0.25 + 0.55 * smooth(0.0, 0.9, r)) + (al,)


def paint_bubble(a, b):
    """blink_bubble: a pale blue-white translucent bubble with a bright rim and a highlight (A6)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    rim = glow(abs(r - 0.92), 0.08, 0.9)
    hl = glow(math.hypot(a + 0.35, b - 0.4), 0.22, 0.8)
    fill = 0.14 + 0.25 * r ** 3
    al = min(1.0, max(rim, hl) + fill)
    return mix(hexc('#E6F4FF'), hexc('#9FC8FF'), 0.5 * smooth(0.3, 1.0, r) * (1 - hl)) + (al,)


# ----------------------------------------------------------------------------- the afterimage silhouette (a -0.25..0.25, b 0..1)
AI_S = 2.65        # S2d (request s2d-1): >= HAT_TOP 2.30 + 0.05 and >= 2 x BRIM_D (the brim fits the card's half width 0.25 x AI_S)


def paint_afterimage(a, b):
    """afterimage: one translucent lilac silhouette of her, the player-size figure (S2d): 2.0 b to the head top, the hat crown
    2.31, feet at b 0, 2.65 b tall at scale 2.65 (the flat round brim hat, the square head, the body and two legs, her slim
    arms, the long sword held low at her side; ORIGINAL design)."""
    x = a * AI_S
    y = b * AI_S
    inside = 0.0
    # the hat: the flat brim at y 2.00 and the crown
    if abs(y - 2.00) < 0.035 and abs(x) < 0.66:
        inside = 1.0
    if 2.00 <= y <= 2.31 and abs(x) < 0.25:
        inside = 1.0
    # the head (square)
    if 1.49 <= y <= 2.02 and abs(x) < 0.28:
        inside = 1.0
    # the torso and the two legs
    if 0.74 <= y <= 1.50 and abs(x) < 0.265:
        inside = 1.0
    if 0.0 <= y <= 0.75 and 0.01 < abs(x) < 0.265:
        inside = 1.0
    # the slim arms (3 px + the sleeve layer: 0.11 b half-width, shoulders +-0.344); the left arm (+x) forward with the sword
    if seg_dist(x, y, -0.344, 1.40, -0.39, 0.78) < 0.11:
        inside = 1.0
    if seg_dist(x, y, 0.344, 1.40, 0.42, 0.86) < 0.11:
        inside = 1.0
    # the sword: a thin line down-forward from the left hand
    if seg_dist(x, y, 0.42, 0.86, 0.63, 0.10) < 0.022:
        inside = max(inside, 0.9)
    if inside <= 0:
        return CLEAR
    rim = 0.0
    for dx, dy in ((0.05, 0), (-0.05, 0), (0, 0.05), (0, -0.05)):
        if paint_inside(x + dx, y + dy) <= 0:
            rim = 1.0
    col = mix(LILAC, RIM, 0.55 * rim) if rim else mix(LILAC_DEEP, LILAC, 0.55 + 0.25 * fbm(x * 3, y * 3))
    return col + ((0.85 if rim else 0.62) * inside,)


def paint_inside(x, y):
    """the silhouette mask at (x, y) in blocks (for the rim test of paint_afterimage; S2d: the player-size figure)"""
    if abs(y - 2.00) < 0.035 and abs(x) < 0.66:
        return 1.0
    if 2.00 <= y <= 2.31 and abs(x) < 0.25:
        return 1.0
    if 1.49 <= y <= 2.02 and abs(x) < 0.28:
        return 1.0
    if 0.74 <= y <= 1.50 and abs(x) < 0.265:
        return 1.0
    if 0.0 <= y <= 0.75 and 0.01 < abs(x) < 0.265:
        return 1.0
    if seg_dist(x, y, -0.344, 1.40, -0.39, 0.78) < 0.11 or seg_dist(x, y, 0.344, 1.40, 0.42, 0.86) < 0.11:
        return 1.0
    return 0.0


# ----------------------------------------------------------------------------- impacts, columns, streaks, bolts
_DI = random.Random(41)
DI_SPIKES = [(k * 360 / 14 + _DI.uniform(-8, 8), _DI.uniform(0.55, 1.0)) for k in range(14)]


def paint_impact(a, b):
    """dive_impact (flat, unit radius): a bright lilac shock ring (r 0.6-0.8) with radial spikes and a soft centre (the dive
    landing; burst_radial turns it)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    ang = math.degrees(math.atan2(a, b)) % 360
    ring = glow(abs(r - 0.68), 0.12, 1.0)
    spike = 0.0
    for c, ln in DI_SPIKES:
        da = abs((ang - c + 180) % 360 - 180)
        if r < ln:
            spike = max(spike, glow(da * math.pi / 180 * r, 0.035 * (1 - r / ln) + 0.005, 0.9))
    centre = glow(r, 0.45, 0.35)
    al = max(ring, spike, centre)
    if al < 0.04:
        return CLEAR
    return mix(RIM, LILAC, smooth(0.0, 0.12, abs(r - 0.68)) * 0.8 + 0.2 * smooth(0.7, 1.0, r)) + (al,)


def paint_column(a, b):
    """light_column (a -0.125..0.125, b 0..1): a soft vertical light column, the core white, the sides fading (neutral:
    tinted lilac / white); also qi_line's beam (lance)."""
    w = 0.125
    d = abs(a) / w
    al = (1 - smooth(0.25, 1.0, d)) * smooth(0.0, 0.06, b) * (1 - smooth(0.75, 1.0, b))
    if al < 0.04:
        return CLEAR
    return ramp(GREYS, 0.6 * d) + (al,)


_CL = random.Random(53)


def paint_claw(a, b):
    """claw_streaks (a -0.125..0.125, b 0..1): one claw-like lilac streak: a sharp point at the bottom (b 0), widening and
    fading upward, slightly curved."""
    cx = 0.03 * math.sin(b * 2.2)
    half = 0.07 * smooth(0.0, 0.35, b) * (1 - 0.5 * b)
    d = abs(a - cx)
    if d > half + 0.03 or b > 0.98:
        return CLEAR
    al = (1 - smooth(half * 0.6, half + 0.03, d)) * (1 - smooth(0.6, 0.98, b))
    if al < 0.04:
        return CLEAR
    return mix(RIM, LILAC, smooth(0.0, half + 0.01, d) * 0.7 + 0.3 * b) + (al,)


_BO = random.Random(67)
BOLT = jag(_BO, 0.0, 0.02, 0.0, 0.98, 9, 0.12)
BOLT_FORK = jag(_BO, BOLT[4][0], BOLT[4][1], 0.07, 0.7, 4, 0.2)


def paint_bolt(a, b):
    """deco_bolt (a -0.125..0.125, b 0..1): a thin yellow lightning bolt with one fork (decoration, no hit box)."""
    d = min(poly_dist(a, b, BOLT), poly_dist(a, b, BOLT_FORK) + 0.004)
    al = glow(d, 0.035, 1.0)
    if al < 0.05:
        return CLEAR
    return mix(hexc('#FFFDE8'), YELLOW, smooth(0.0, 0.03, d)) + (al,)


def make_clash(k):
    """clash_gold frame 0: the gold starburst (blade on blade); frame 1: the cyan-gold kick flash (CS2 R8)."""
    rnd = random.Random(100 + k)
    rays = [(rnd.uniform(0, 360), rnd.uniform(0.55, 1.0), rnd.uniform(0.02, 0.05)) for _ in range(16)]

    def paint(a, b):
        r = math.hypot(a, b)
        if r > 1.0:
            return CLEAR
        ang = math.degrees(math.atan2(a, b)) % 360
        ray = 0.0
        for c, ln, w in rays:
            da = abs((ang - c + 180) % 360 - 180) * math.pi / 180 * r
            if r < ln:
                ray = max(ray, glow(da, w * (1.2 - r), 1.0) * (1 - r / ln))
        core = glow(r, 0.42, 1.0)
        al = max(core, ray)
        if k == 1:
            al = max(al, glow(abs(r - 0.5), 0.06, 0.9))
        if al < 0.04:
            return CLEAR
        if k == 0:
            col = mix(WHITE, GOLD, smooth(0.05, 0.5, r))
        else:
            col = mix(WHITE, hexc('#7FF4FF'), smooth(0.05, 0.4, r)) if r < 0.55 else mix(hexc('#7FF4FF'), GOLD, smooth(0.5, 0.8, r))
        return col + (al,)
    return paint


def make_spark(k):
    """clash_spark frame 0 (a -0.125..0.125, b -0.5..0.5): a tapered spark streak (neutral white, tinted gold); frame 1:
    a jagged lightning arc (neutral, tinted orange)."""
    if k == 0:
        def paint(a, b):
            u = b + 0.5
            w = 0.03 * u + 0.004
            d = abs(a)
            al = glow(d, w + 0.02, 1.0) * smooth(0.0, 0.4, u) * (1 - smooth(0.92, 1.0, u))
            if al < 0.04:
                return CLEAR
            return ramp(GREYS, 0.5 * smooth(0.0, w + 0.02, d)) + (al,)
        return paint
    rnd = random.Random(7)
    pts = jag(rnd, 0.0, -0.48, 0.0, 0.48, 8, 0.2)

    def paint(a, b):
        d = poly_dist(a, b, pts)
        al = glow(d, 0.03, 1.0)
        if al < 0.04:
            return CLEAR
        return ramp(GREYS, 0.6 * smooth(0.0, 0.025, d)) + (al,)
    return paint


def paint_scarlet_line(a, b):
    """scarlet_line (a -1..1 the length, b -0.0625..0.0625): 홍련일섬's red slash line: a white-hot core, crimson edges,
    long tapering ends."""
    u = 1 - abs(a)
    w = 0.05 * u ** 0.35 + 0.004
    d = abs(b)
    al = glow(d, w + 0.012, 1.0) * smooth(0.0, 0.08, u)
    if al < 0.04:
        return CLEAR
    return mix(hexc('#FFF2F2'), CRIMSON, smooth(w * 0.15, w * 0.9, d) * 0.85 + 0.15 * (1 - u)) + (al,)


# ----------------------------------------------------------------------------- petals, leaves, motes
def _petal_shape(a, b, width=0.55, notch=True):
    """a cherry-like petal along +b (base at b -0.9, notched tip at b 0.9): 0 outside .. 1 inside"""
    y = (b + 0.9) / 1.8
    if not 0 <= y <= 1:
        return 0.0
    hw = width * math.sin(math.pi * clamp01(y) ** 0.75)
    if notch and y > 0.8:
        hw *= 1 - 0.0
        if abs(a) < 0.12 * (y - 0.8) / 0.2:
            return 0.0
    return 1.0 if abs(a) <= hw else 0.0


def make_petal_big(k):
    """petal_big frame k (the CS1 petal, a red petal ~0.7 b at the card's scale): 0 whole, 1 cut (a thin glowing line across
    it), 2 split (the two halves apart, falling)."""
    def base(a, b):
        if _petal_shape(a, b, 0.62) <= 0:
            return CLEAR
        y = (b + 0.9) / 1.8
        vein = glow(abs(a), 0.025, 0.25) * (1 - y)
        col = mix(hexc('#FF6A84'), hexc('#B8122E'), 0.35 + 0.45 * y + 0.2 * fbm(a * 4, b * 4))
        col = mix(col, hexc('#FFB0C0'), vein)
        return col + (0.97,)

    def paint(a, b):
        if k == 0:
            return base(a, b)
        # the cut line: across the petal, rising slightly to the right
        line = b - (0.12 * a + 0.05)
        if k == 1:
            c = base(a, b)
            gl = glow(abs(line), 0.06, 1.0)
            if gl > 0.05 and (c[3] > 0 or abs(a) < 0.75):
                return over(mix(WHITE, hexc('#FFD0E0'), smooth(0.0, 0.06, abs(line))) + (gl,), c)
            return c
        # split: the upper half shifted up-right and turned, the lower half shifted down-left
        if line > 0:
            aa, bb = a - 0.14, b - 0.16
            ang = math.radians(-14)
        else:
            aa, bb = a + 0.12, b + 0.14
            ang = math.radians(10)
        ra = aa * math.cos(ang) - bb * math.sin(ang)
        rb = aa * math.sin(ang) + bb * math.cos(ang)
        if (rb - (0.12 * ra + 0.05) > 0) != (line > 0):
            return CLEAR
        c = base(ra, rb)
        edge = glow(abs(rb - (0.12 * ra + 0.05)), 0.05, 0.8)
        if c[3] > 0 and edge > 0.1:
            return mix(c[:3], hexc('#FFD0E0'), edge) + (c[3],)
        return c
    return paint


def make_small(k):
    """petals_small frame k (16 px): 0-2 cherry petals (pinks), 3 a heart-shaped petal, 4-6 leaves (neutral greys, the
    card tints them dark red / black), 7 a soft round mote (neutral)."""
    def paint(a, b):
        if k <= 2:
            ang = math.radians(25 * (k - 1))
            ra, rb = a * math.cos(ang) - b * math.sin(ang), a * math.sin(ang) + b * math.cos(ang)
            if _petal_shape(ra, rb, 0.55) <= 0:
                return CLEAR
            return mix(hexc('#FFD3E2'), hexc('#F27CA6'), 0.3 + 0.25 * k + 0.3 * (rb + 0.9) / 1.8) + (0.95,)
        if k == 3:
            x, y = a * 1.15, b * 1.15 + 0.15
            heart = (x * x + y * y - 0.6) ** 3 - x * x * y ** 3 <= 0
            if not heart:
                return CLEAR
            return mix(hexc('#FFC2D6'), hexc('#E25A8A'), clamp01(0.5 - 0.5 * b)) + (0.92,)
        if k <= 6:
            ang = math.radians(40 * (k - 5) + 20)
            ra, rb = a * math.cos(ang) - b * math.sin(ang), a * math.sin(ang) + b * math.cos(ang)
            y = (rb + 0.95) / 1.9
            if not 0 <= y <= 1:
                return CLEAR
            hw = 0.42 * math.sin(math.pi * y) ** 0.9
            if abs(ra) > hw:
                return CLEAR
            vein = glow(abs(ra), 0.05, 0.3)
            return ramp(GREYS, 0.55 + 0.35 * y - vein) + (0.95,)
        r = math.hypot(a, b)
        al = glow(r, 0.95, 1.0)
        if al < 0.05:
            return CLEAR
        return mix(WHITE, hexc('#E0E0E0'), r) + (al,)
    return paint


# ----------------------------------------------------------------------------- the moon halo, the disc
def make_halo(k):
    """moon_halo frame k (the card in front of the block moon, r 5 -> the halo to r ~6.2 at a 12.4-b card): 0 the white-blue
    P1 halo, 1 the red P2 halo; the centre clear (the block disc shows through)."""
    inner, outer = hexc('#F2FAFF') if k == 0 else hexc('#FFD2D6'), hexc('#8FB6FF') if k == 0 else hexc('#E8304A')

    def paint(a, b):
        r = math.hypot(a, b)
        if r < 0.78 or r > 1.0:
            return CLEAR
        rim = glow(abs(r - 0.81), 0.04, 0.9)
        haze = (1 - smooth(0.8, 1.0, r)) * 0.55
        wisp = 0.18 * smooth(0.5, 0.8, fbm(math.atan2(a, b) * 2 + 3, r * 6))
        al = min(1.0, max(rim, haze) + wisp * haze)
        if al < 0.04:
            return CLEAR
        return mix(inner, outer, smooth(0.8, 0.98, r)) + (al,)
    return paint


def make_disc(k):
    """disc frame k (the A7 moon disc, flat, unit radius): a spinning lilac sword-qi disc: a bright crescent rim on a
    translucent disc, the gold-white edge line (the A13 gold blade line), two spin phases."""
    off = 45.0 * k

    def paint(a, b):
        r = math.hypot(a, b)
        if r > 1.0:
            return CLEAR
        ang = (math.degrees(math.atan2(a, b)) + off) % 360
        rim = glow(abs(r - 0.9), 0.07, 1.0)
        cres = 0.0
        for c in (0.0, 180.0):
            da = abs((ang - c + 180) % 360 - 180)
            if da < 110:
                cres = max(cres, glow(abs(r - 0.78), 0.1 * (1 - da / 110), 0.9))
        fill = 0.32 * (1 - r) + 0.12
        al = min(1.0, max(rim, cres) + fill)
        col = mix(LILAC, RIM, max(rim, cres))
        if r > 0.95:
            col = mix(col, hexc('#FFF0B0'), 0.6)
        return col + (al,)
    return paint


# ----------------------------------------------------------------------------- the gate icon
def paint_gate_icon(a, b):
    """gate icon: a red lotus over a long blade (an upright single-edged sword, silver blade, dark grip, a brass guard)."""
    # the sword: blade from b -0.95 (grip end) up to the tip at b 0.95
    blade = abs(a - 0.02 * (b + 0.95)) < 0.07 * (1 - smooth(0.75, 0.97, b)) and -0.35 < b < 0.97
    grip = abs(a + 0.01) < 0.055 and -0.95 < b < -0.45
    guard = abs(b + 0.42) < 0.045 and abs(a) < 0.18
    out = CLEAR
    if blade:
        edge = smooth(0.0, 0.06, abs(a - 0.02 * (b + 0.95) + 0.04))
        out = mix(hexc('#F4F6FF'), hexc('#9AA0B8'), edge) + (1.0,)
    if grip:
        out = (mix(hexc('#2A1E34'), hexc('#6A3E8A'), 0.4 if int((b + 1) * 30) % 2 else 0.0)) + (1.0,)
    if guard:
        out = hexc('#C8A050') + (1.0,)
    # the red lotus in front of the blade's middle
    cx, cy = 0.0, -0.05
    dx, dy = a - cx, b - cy
    r = math.hypot(dx, dy)
    ang = math.degrees(math.atan2(dx, dy))
    lotus = 0.0
    if dy > -0.28 and r < 0.62:
        for kk in range(-3, 4):
            da = abs(ang - kk * 25.0)
            w = 12.0 * (1 - 0.3 * abs(kk) / 3)
            ln = 0.6 - 0.08 * abs(kk)
            if da < w and r < ln:
                lotus = max(lotus, 1 - da / w)
    if lotus > 0:
        col = mix(hexc('#FF6A84'), hexc('#B0102E'), 0.4 + 0.5 * smooth(0.2, 0.6, r))
        if lotus < 0.25:
            col = mix(col, hexc('#5A0814'), 0.6)
        out = col + (1.0,)
    if r < 0.12 and dy > -0.14:
        out = hexc('#FFD45A') + (1.0,)
    return out


# ----------------------------------------------------------------------------- HUD glyphs (x -1..1 left -> right, y -1..1 bottom -> top, the screen)
def glyph_flat(hx, al):
    def paint(x, y):
        return hexc(hx) + (al,)
    return paint


def glyph_negative(x, y):
    """the `negative` frame (an approximation: titles can only paint over the screen): a pale cyan-white field with a dark
    rim and a dark diagonal band (lower-left -> upper-right)."""
    edge = max(abs(x), abs(y))
    rim = smooth(0.72, 1.0, edge)
    band = glow(abs(y - 0.55 * x + 0.05) / 1.15, 0.22, 1.0)
    col = mix(hexc('#DDF6FA'), hexc('#18202A'), max(rim * 0.85, band * 0.9))
    return col + (0.97,)


def glyph_pinkwhite(x, y):
    """the overexposed pink-white frame with a dark-red then gold diagonal line (CS1 C7)."""
    t = y - 0.5 * x
    red = glow(abs(t + 0.06), 0.05, 1.0)
    gold = glow(abs(t - 0.06), 0.04, 1.0)
    col = mix(hexc('#FFEAF3'), hexc('#FFD2E4'), smooth(0.0, 1.2, abs(x)))
    col = mix(col, hexc('#7A0A1E'), red)
    col = mix(col, hexc('#FFD24A'), gold)
    return col + (0.96,)


def glyph_red_tint(x, y):
    """the red tint over 홍련일섬 (fading out over the recolour): translucent crimson, a little darker at the edges."""
    edge = smooth(0.5, 1.0, max(abs(x), abs(y)))
    return mix(hexc('#E0283C'), hexc('#7A0A1E'), edge) + (0.42 + 0.2 * edge,)


def glyph_vignette(x, y):
    """`vig` (§7.4.5): an edge-only dark vignette, the centre clear (0 alpha inside ~55 % of the screen)."""
    e = math.hypot(x * 0.92, y * 1.0)
    al = smooth(0.62, 1.22, e) * 0.8
    if al < 0.01:
        return CLEAR
    return mix(hexc('#2A0A16'), hexc('#05030A'), smooth(0.9, 1.3, e)) + (al,)
