"""Painted sprites of the 아를레키노 (Arlecchino) fx kit (tools/build_mboss_kn_fx.py). Stdlib only, deterministic (fixed
seeds).

Arlecchino fights with one huge crimson scythe (P1) / twin scythes and six blade legs (P2). The footage shows two effect
colours (scratchpad ar/PLAN.md §1.3, ar/ref/*.jpg): plain Pyro hits burn orange-gold (white-hot core -> #FFD27A gold ->
#FF8A2A orange, red-orange tips: the slash arcs, the flaming scythe wheel, the spin rings, the thrown crescents), the
Bond-of-Life attacks are crimson with black smoke (#FF3A4A bright crimson -> #7A0A1A deep crimson -> black: the threads,
thorns, giant blades, clones, the red X, the moon halo, the floor flood / cracks / strips / outlines). The player's own
effects (blue water rings, white-blue bubbles, golden shields) are not painted here.

Card coordinates follow the fg / Apep / Tachy kits: every painter takes (a, b) inside its kind's painter box and returns
straight-alpha (r, g, b, alpha) floats; +a is the card's local -x (the right seen from behind or from above), +b is up
(face / cross cards) or forward (flat / lance cards). Sprites are painted in their colour (tint white) except the
`neutral` ones (warm white / white: the item tint gives Pyro orange or crimson).

The helpers (noise, polylines, ramps) are copies of the Tachy painter's so the kits can change apart.
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

_R = random.Random(20261102)
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


def make_lines(polys):
    out = []
    for pts in polys:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        out.append(((min(xs), min(ys), max(xs), max(ys)), pts))
    return out


def lines_dist(px, py, lines, pad=0.08):
    best = 9.0
    for (x0, y0, x1, y1), pts in lines:
        if px < x0 - pad or px > x1 + pad or py < y0 - pad or py > y1 + pad:
            continue
        best = min(best, poly_dist(px, py, pts))
    return best


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


def crescent(x, y, cx, cy, R, ix, iy, r):
    """a crescent blade (y >= cy side): inside the circle (cx, cy, R), outside the circle (ix, iy, r); returns 0 outside,
    else 0..1 toward the outer (cutting) edge"""
    d = math.hypot(x - cx, y - cy)
    if d > R or y < cy - 0.02 or math.hypot(x - ix, y - iy) < r:
        return 0.0
    di = math.hypot(x - ix, y - iy) - r
    return clamp01(0.25 + 0.75 * (1 - (R - d) / (R - d + di + 1e-6)))


# ----------------------------------------------------------------------------- the two colour ramps (footage)
PYRO = rmp((0.0, '#FFFFFF'), (0.22, '#FFF4CF'), (0.48, '#FFD27A'), (0.78, '#FF8A2A'), (1.0, '#D8441A'))
CRIM = rmp((0.0, '#FFE0E4'), (0.2, '#FF7A86'), (0.45, '#FF3A4A'), (0.75, '#C0122C'), (1.0, '#7A0A1A'))
SMOKE = hexc('#160608')
WARM = rmp((0.0, '#FFFFFF'), (0.4, '#FFF6E6'), (1.0, '#FFE2C4'))      # neutral warm white (tinted)
RAMPS = {'p': PYRO, 'c': CRIM}


def _band(d, alpha, rp):
    """colour + alpha at the normalised distance d (0 core .. 1 edge) of a flame band of ramp rp"""
    if d >= 1.25 or alpha <= 0:
        return CLEAR
    return ramp(rp, min(1.0, d)) + (alpha * (1 - smooth(0.72, 1.22, d)),)


def _smoke(a, b, k, amount, rr=1.0):
    """black smoke wisps (alpha) around a crimson band: amount 0..1 at this point"""
    n = fbm(a * 5.0 * rr + 11.0 + k, b * 5.0 * rr + 3.0)
    al = amount * smooth(0.45, 0.75, n)
    return SMOKE + (0.75 * al,)


# ----------------------------------------------------------------------------- slash arcs (flat, a -1..1, b 0..1)
ARC_T0, ARC_T1 = -78.0, 78.0          # sweep bearings (degrees from +b toward +a); the kit's floor clamp uses +-80
ARC_RC = 0.80                         # band centre radius (unit radius = the reach at scale r)
ARC_F = (0.34, 0.60, 0.84, 1.0)       # head position of frames 0..3 (fraction of the sweep)


def make_arc(k, col):
    """Slash-arc sweep frame k of colour col ('p' Pyro orange-gold, 'c' crimson with black smoke): a flame band on the
    circle of radius ARC_RC from the start bearing up to the head of frame k (the leading edge thick and white-hot, the
    tail thinner and fading); frame 3 = the whole arc, the tail faded."""
    th = ARC_T0 + (ARC_T1 - ARC_T0) * ARC_F[k]
    rp = RAMPS[col]

    def paint(a, b):
        r = math.hypot(a, b)
        if r < 0.38 or r > 1.0:
            return CLEAR
        ph = math.degrees(math.atan2(a, b))
        if ph < ARC_T0 - 3 or ph > th + 4:
            return CLEAR
        u = clamp01((ph - ARC_T0) / (th - ARC_T0))
        fac = (0.30 + 0.70 * u) if k < 3 else smooth(0.0, 0.55, u)
        tip = clamp01((th + 4 - ph) / 9.0)
        ht = (0.075 + 0.13 * u ** 0.8) * (0.35 + 0.65 * tip)
        n = fbm(ph * 0.09 + 7.3 * k, r * 7.0)
        e_out = ht * (0.9 + 1.1 * n)
        e_in = ht * (0.7 + 0.4 * n)
        dr = r - ARC_RC
        d = abs(dr) / (e_out if dr > 0 else e_in)
        px = _band(d, fac, rp)
        lick = vnoise(ph * 0.35 + 3.1 * k, r * 22.0)
        if dr > 0 and d < 2.2 and lick > 0.62:
            al = fac * 0.75 * (1 - smooth(1.0, 2.2, d)) * smooth(0.62, 0.8, lick)
            if al > px[3]:
                px = ramp(rp, 0.8) + (al,)
        if col == 'c' and dr > -0.02 and px[3] < 0.6:
            sm = _smoke(a, b, k, fac * (1 - smooth(0.9, 2.6, d)) * smooth(-0.02, 0.04, dr))
            if sm[3] > 0.02:
                px = over(px, sm) if px[3] > 0 else sm
        return px
    return paint


# ----------------------------------------------------------------------------- rings (flat, unit radius)
def make_ring(col):
    """A full ring of fire (unit radius, band on r 0.8), licks swirling clockwise; 'c' adds black smoke outside."""
    rp = RAMPS[col]

    def paint(a, b):
        r = math.hypot(a, b)
        if r > 1.0 or r < 0.5:
            return CLEAR
        ph = math.atan2(a, b)
        sw = ph * 3.0 + r * 9.0
        n = fbm(math.cos(sw) * 2.0 + 5.0, math.sin(sw) * 2.0 + r * 4.0)
        ht = 0.07 + 0.05 * n
        dr = r - 0.80
        d = abs(dr) / (ht * (1.6 if dr > 0 else 1.0))
        px = _band(d, 1.0, rp)
        lick = vnoise(ph * 9.0, r * 18.0)
        if dr > 0 and lick > 0.6 and d < 2.4:
            al = 0.7 * (1 - smooth(1.0, 2.4, d)) * smooth(0.6, 0.78, lick)
            if al > px[3]:
                px = ramp(rp, 0.8) + (al,)
        if col == 'c' and dr > 0 and px[3] < 0.6:
            sm = _smoke(a, b, 2, (1 - smooth(1.2, 2.8, d)))
            if sm[3] > 0.02:
                px = over(px, sm) if px[3] > 0 else sm
        return px
    return paint


# ----------------------------------------------------------------------------- the flaming scythe wheel (face, BX)
def make_wheel(k):
    """Frame k of the spinning wheel (B 붉은 달의 낫, ref p1_B_throw.jpg v1 16.0-16.8): a ring of orange-gold flame on r 0.78
    with licks trailing against the spin, and the dark crimson scythe inside (haft through the centre, the crescent blade
    at one end) turned k x 90 degrees; the flame noise turns with it."""
    rot = math.radians(90.0 * k)
    cr, sr = math.cos(rot), math.sin(rot)

    def paint(a, b):
        x, y = a * cr + b * sr, -a * sr + b * cr           # the frame's own coordinates (turned)
        r = math.hypot(a, b)
        out = CLEAR
        if r <= 1.0:
            ph = math.atan2(y, x)
            n = fbm(math.cos(ph * 3) * 2 + 3, math.sin(ph * 3) * 2 + r * 5)
            dr = r - 0.78
            d = abs(dr) / ((0.08 + 0.07 * n) * (1.7 if dr > 0 else 1.0))
            out = _band(d, 1.0, PYRO)
            lick = vnoise(ph * 6.0, r * 14.0)
            if dr > 0 and lick > 0.55 and d < 2.6:
                al = 0.8 * (1 - smooth(1.0, 2.6, d)) * smooth(0.55, 0.75, lick)
                if al > out[3]:
                    out = ramp(PYRO, 0.7) + (al,)
            if r < 0.66 and out[3] < 0.2:                    # faint heat inside the ring
                g = 0.18 * smooth(0.2, 0.66, r)
                out = ramp(PYRO, 0.6) + (g,)
        # the scythe: haft along x through the centre, the crescent blade at +x curving back over the haft
        hd = seg_dist(x, y, -0.62, 0.0, 0.6, 0.0)
        if hd < 0.045:
            out = over(mix('#3A0A10', '#8A1426', 1 - hd / 0.045) + (1.0,), out)
        e = crescent(x, y, 0.25, 0.0, 0.42, 0.25, -0.12, 0.38)
        if e > 0:
            out = over(mix('#5A0A16', '#FF5A60', e) + (1.0,), out)
        return out
    return paint


# ----------------------------------------------------------------------------- projectiles / props
def paint_crescent(a, b):
    """P2 thrown crescent (Q1 h3, Q3; face, a -1..1, b -0.5..0.5): a wide flame bow, white-hot leading edge on top,
    orange flame and red-orange tips trailing down (ref p2_Q1_twin.jpg v4 31.7-33.9)."""
    u = a
    if abs(u) > 1:
        return CLEAR
    top = 0.28 - 0.55 * u * u
    thick = 0.22 * (1 - u * u) ** 0.6 + 0.02
    dy = top - b
    if dy < -0.06:
        return CLEAR
    n = fbm(u * 6.0, b * 5.0)
    d = (dy + 0.04) / (thick + 1e-6) / (0.75 + 0.5 * n)
    if d > 1.3:
        return CLEAR
    return ramp(PYRO, min(1.0, d)) + (1 - smooth(0.75, 1.25, d),)


def paint_feather(a, b):
    """Q6 crimson feather bolt (face, a -0.25..0.25, b -0.5..0.5): a slim blade-feather pointing down (-b), dark crimson
    vane, a black spine, bright crimson edges."""
    t = (0.5 - b)                                   # 0 at the top (quill) .. 1 at the tip (bottom)
    if t < 0 or t > 1:
        return CLEAR
    w = 0.21 * math.sin(math.pi * min(1.0, t * 1.15)) ** 0.7 * (1 - 0.25 * t)
    if abs(a) > w + 0.01:
        return CLEAR
    e = abs(a) / (w + 1e-6)
    if abs(a) < 0.018:
        return mix('#120406', '#3A0610', t) + (1.0,)
    barb = 0.5 + 0.5 * math.sin((t * 26.0 + abs(a) * 40.0))
    c = mix(mix('#5A0812', '#C0122C', e), '#FF4A58', smooth(0.75, 1.0, e))
    c = mix(c, '#2A0408', 0.25 * barb * (1 - e))
    return c + (1 - smooth(0.95, 1.05, e),)


def paint_orb(a, b):
    """Q6 crimson orb (face, BX): pink-white core, crimson body, a dark rim and a soft red halo."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    if r < 0.62:
        n = fbm(a * 4 + 2, b * 4 + 7)
        c = ramp(CRIM, clamp01(r / 0.62 * 0.85 + 0.15 * n))
        return c + (1.0,)
    if r < 0.7:
        return mix('#7A0A1A', '#2A0408', (r - 0.62) / 0.08) + (1.0,)
    return hexc('#FF3A4A') + (0.55 * (1 - smooth(0.7, 1.0, r)),)


def paint_blade(a, b):
    """G giant crimson blade (face, a -0.125..0.125, b 0..1; base at b 0): a long curved crimson spike, broad base
    tapering to a hooked tip, bright crimson-pink edges, deep crimson body with black veins (ref p1_G_blades.jpg)."""
    t = b
    if t < 0 or t > 1:
        return CLEAR
    bend = 0.035 * math.sin(math.pi * t) + 0.03 * t * t      # the blade leans and hooks a little
    w = 0.115 * (1 - t) ** 0.85 + 0.004
    x = a - bend
    if abs(x) > w:
        return CLEAR
    e = abs(x) / w
    n = fbm(a * 30 + 4, t * 9)
    vein = smooth(0.62, 0.7, vnoise(t * 22 + 3, a * 60)) * (1 - e)
    c = mix(ramp(CRIM, 0.85 - 0.5 * smooth(0.6, 1.0, e)), '#FF8A94', smooth(0.82, 1.0, e) * (0.6 + 0.4 * n))
    c = mix(c, '#140406', 0.55 * vein)
    if x < 0:
        c = mix(c, '#3A0610', 0.35 * (1 - e))                # the shaded half
    al = 1 - smooth(0.9, 1.0, e)
    if t < 0.04:                                              # the base melts into crimson glow
        al *= 0.6 + 10 * t
    return c + (al,)


def _clone_mask(a, b):
    """the leaping silhouette (a -0.25..0.25, b 0..1): her figure leaning forward (+a), coat flaring back, the scythe
    raised over the head with its crescent: 1 inside, 0 outside"""
    if math.hypot(a - 0.05, b - 0.86) < 0.05:                                    # head
        return 1.0
    if poly_dist(a, b, [(0.045, 0.8), (0.02, 0.62), (-0.01, 0.47)]) < 0.055:      # torso
        return 1.0
    # the coat tails flaring back (a wedge)
    if b < 0.5 and b > 0.18 and -0.2 + 0.3 * (b - 0.18) / 0.32 < a < 0.03 - 0.02 * (0.5 - b) / 0.32:
        return 1.0
    if poly_dist(a, b, [(0.0, 0.45), (0.1, 0.28), (0.06, 0.04)]) < 0.03:          # front leg
        return 1.0
    if poly_dist(a, b, [(-0.02, 0.45), (-0.07, 0.25), (-0.15, 0.08)]) < 0.026:    # back leg
        return 1.0
    if poly_dist(a, b, [(0.04, 0.76), (0.13, 0.82), (0.15, 0.9)]) < 0.022:        # arms up to the haft
        return 1.0
    if seg_dist(a, b, 0.21, 0.6, -0.12, 0.99) < 0.016:                            # the haft
        return 1.0
    if crescent(a, b, -0.02, 0.9, 0.17, -0.0, 0.85, 0.15) > 0:                    # the crescent
        return 1.0
    return 0.0


def paint_clone(a, b):
    """H crimson shadow clone (face, a -0.25..0.25, b 0..1, feet at b 0): her silhouette leaping with the scythe raised,
    a translucent black-crimson body with a bright crimson rim, smoke trailing at the feet (ref p1_H_launch.jpg)."""
    cov = _clone_mask(a, b)
    if cov <= 0:
        # rim glow: distance to the silhouette via a small sample ring
        best = 0.0
        for dx, dy in ((0.02, 0), (-0.02, 0), (0, 0.02), (0, -0.02), (0.014, 0.014), (-0.014, -0.014)):
            if _clone_mask(a + dx, b + dy) > 0:
                best = 1.0
                break
        if best:
            return hexc('#FF3A4A') + (0.85,)
        sm = _smoke(a * 2, b, 4, 0.8 * (1 - smooth(0.0, 0.3, b)) * (1 - smooth(0.0, 0.2, abs(a))))
        return sm if sm[3] > 0.03 else CLEAR
    n = fbm(a * 20, b * 12)
    c = mix('#1A0306', '#6A0A18', 0.3 + 0.5 * n)
    al = 0.82 * (0.35 + 0.65 * smooth(0.0, 0.25, b))
    return c + (al,)


def make_wisp(k):
    """Frame k of the flame spirit (face, BX; white, tinted white or red): a round flame body with a pointed tip swaying
    (k), a bright core and a soft glow halo (ref intro_v5_approach.jpg)."""
    sway = (-0.14, 0.0, 0.14)[k]

    def paint(a, b):
        y = b + 0.15
        if y < -0.85:
            return CLEAR
        if y <= 0:
            body = math.hypot(a, y) / 0.5
        else:
            x = a - sway * (y / 0.85) ** 1.5
            wdt = 0.5 * (1 - y / 0.85) ** 0.9 + 1e-3 if y < 0.85 else 1e-3
            body = abs(x) / wdt if y < 0.85 else 9.0
            body = max(body, 0.0)
        if body <= 1.0:
            core = 1 - smooth(0.0, 0.6, math.hypot(a, b + 0.25) / 0.45)
            c = mix('#E8F0FF', WHITE, core)
            return c + (0.9 - 0.25 * smooth(0.7, 1.0, body),)
        g = 0.35 * (1 - smooth(0.0, 0.85, math.hypot(a, b + 0.1) - 0.45))
        return (WHITE + (g,)) if g > 0.05 else CLEAR
    return paint


def paint_halo(a, b):
    """The red-moon halo (face, BX): a thin bright crimson ring on r 0.66, soft bloom out to 1.0, a faint red wash
    inside (the moon itself is the arena's; this card circles it)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    ring = math.exp(-((r - 0.66) / 0.022) ** 2)
    bloom = 0.5 * math.exp(-((r - 0.68) / 0.14) ** 2)
    inner = 0.18 * (1 - smooth(0.3, 0.64, r)) if r < 0.66 else 0.0
    n = fbm(math.atan2(a, b) * 3 + 5, r * 6)
    al = max(ring, bloom * (0.7 + 0.6 * n), inner) * (1 - smooth(0.92, 1.0, r))
    if al < 0.03:
        return CLEAR
    c = mix('#C0122C', '#FFC8CE', ring)
    return c + (min(1.0, al),)


def paint_claw(a, b):
    """B2 grab: the crimson claw (face, BX): four hooked crimson talons curling in toward the centre from the top and
    the sides, a red glow between them."""
    out = CLEAR
    g = 0.45 * (1 - smooth(0.0, 0.7, math.hypot(a, b)))
    if g > 0.03:
        out = hexc('#FF3A4A') + (g,)
    for k, ang in enumerate((-130, -50, 50, 130)):
        th = math.radians(ang)
        sx, sy = math.sin(th) * 0.92, math.cos(th) * 0.92 + 0.05
        # a talon: arc from the start point curling toward the centre
        pts = []
        for j in range(9):
            u = j / 8
            rr = 0.92 - 0.62 * u
            aa = th + (0.55 if ang < 0 else -0.55) * u
            pts.append((math.sin(aa) * rr, math.cos(aa) * rr + 0.05 * (1 - u)))
        d = poly_dist(a, b, pts)
        tip = clamp01(math.hypot(a - pts[-1][0], b - pts[-1][1]) / 0.6)
        w = 0.025 + 0.06 * tip
        if d < w:
            e = d / w
            out = over(mix('#FFB0B8', '#8A0A1E', e) + (1.0,), out)
        del sx, sy, k
    return out


def paint_thread(a, b):
    """A crimson thread from the sky (face, a -1/16..1/16, b 0..1): a thin bright line with a crimson glow, slight
    kinks, fading toward the top."""
    x = a - 0.012 * math.sin(b * 23.0) - 0.006 * math.sin(b * 61.0)
    d = abs(x)
    core = 1 - smooth(0.006, 0.014, d)
    halo = 0.6 * math.exp(-(d / 0.03) ** 2)
    al = max(core, halo) * (0.35 + 0.65 * (1 - smooth(0.7, 1.0, b)))
    if al < 0.04:
        return CLEAR
    return mix('#FF3A4A', '#FFD0D6', core) + (al,)


def paint_thorn(a, b):
    """A crimson thorn (face, a -0.25..0.25, b 0..1, base at b 0): a curved spike, black-crimson body, bright edges."""
    bend = 0.06 * b * b
    w = 0.2 * (1 - b) ** 1.2 + 0.004
    x = a - bend
    if abs(x) > w or b < 0 or b > 1:
        return CLEAR
    e = abs(x) / w
    c = mix(mix('#1A0306', '#7A0A1A', 0.4 + 0.6 * b), '#FF4A58', smooth(0.7, 1.0, e))
    return c + (1 - smooth(0.9, 1.0, e),)


_WEB = random.Random(31)


def _web_lines():
    polys = []
    spokes = [2 * math.pi * k / 9 + _WEB.uniform(-0.12, 0.12) for k in range(9)]
    for s in spokes:
        polys.append(jag(_WEB, 0, 0, 0.97 * math.sin(s), 0.97 * math.cos(s), 6, 0.03))
    for ring in (0.28, 0.46, 0.63, 0.8, 0.93):
        pts = []
        for k in range(10):
            s = spokes[k % 9]
            rr = ring * _WEB.uniform(0.9, 1.04)
            pts.append((rr * math.sin(s), rr * math.cos(s)))
        polys.append(pts)
    return make_lines(polys)


WEB_LINES = _web_lines()


def paint_web(a, b):
    """H crimson web (flat, UNIT): spokes and sagging rings of glowing crimson threads."""
    if math.hypot(a, b) > 1.0:
        return CLEAR
    d = lines_dist(a, b, WEB_LINES, 0.05)
    core = 1 - smooth(0.006, 0.016, d)
    halo = 0.45 * math.exp(-(d / 0.035) ** 2)
    al = max(core, halo)
    if al < 0.04:
        return CLEAR
    return mix('#C0122C', '#FFC0C8', core) + (al,)


def paint_stroke(a, b):
    """One carved slash stroke (face, a -0.125..0.125, b -0.5..0.5): a crimson line, white-hot core, tapered ends, a red
    glow; two crossed at +-45 degrees make the red X (Q5B x_mark, brand_x)."""
    t = abs(b) / 0.5
    if t > 1:
        return CLEAR
    w = 0.05 * (1 - t ** 3) + 0.004
    d = abs(a + 0.01 * math.sin(b * 18))
    core = 1 - smooth(w * 0.35, w, d)
    halo = 0.55 * math.exp(-(d / (w * 2.2 + 0.02)) ** 2) * (1 - t ** 2)
    al = max(core, halo)
    if al < 0.04:
        return CLEAR
    return mix('#E0182E', '#FFE4E8', core * (1 - t * 0.7)) + (al,)


def paint_brand(a, b):
    """The crimson sigil ring of the forced bond (flat, UNIT; ref p1_F_sigil.jpg): two thin rings (0.92, 0.74), twelve
    rune ticks between them, four diamonds on the inner ring, a red glow."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    ph = math.degrees(math.atan2(a, b)) % 360
    al = 0.0
    for rr, w in ((0.92, 0.012), (0.74, 0.01)):
        al = max(al, math.exp(-((r - rr) / w) ** 2))
    if 0.77 < r < 0.89:
        m = (ph + 15) % 30
        if abs(m - 15) < 2.2 * (1.0 if (int((ph + 15) // 30) % 2) else 0.6):
            al = max(al, 0.85)
    for k in range(4):
        da = math.radians((ph - 90 * k + 180) % 360 - 180)
        dx, dy = da * 0.74, r - 0.74
        if abs(dx) + abs(dy) < 0.06:
            al = max(al, 1.0)
    al = max(al, 0.35 * math.exp(-((r - 0.83) / 0.12) ** 2))
    if al < 0.04:
        return CLEAR
    return mix('#C0122C', '#FFD0D6', al ** 2) + (min(1.0, al),)


def paint_reticle(a, b):
    """Q4 aim reticle (face, BX; ref p2_Q4_beam.jpg v6 17.25): a red ring (0.7), a small inner ring (0.22), four ticks
    crossing the ring, a faint glow."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    al = max(math.exp(-((r - 0.7) / 0.03) ** 2), math.exp(-((r - 0.22) / 0.02) ** 2))
    for x, y in ((a, b), (b, a)):
        if abs(x) < 0.025 and 0.45 < abs(y) < 0.95:
            al = max(al, 1.0)
    al = max(al, 0.25 * (1 - smooth(0.0, 0.9, r)))
    if al < 0.04:
        return CLEAR
    return mix('#E0182E', '#FFD8DC', al ** 2) + (min(1.0, al),)


def paint_beam(a, b):
    """Q4 beam (lance, a -0.5..0.5 across, b 0..1 along; symmetric both ways): a white-pink core, a crimson body, streaky
    edges."""
    d = abs(a) / 0.5
    if d > 1:
        return CLEAR
    n = fbm(b * 9.0, a * 3.0 + 2.0)
    core = 1 - smooth(0.08, 0.3, d)
    body = 1 - smooth(0.45 + 0.25 * n, 1.0, d)
    if body <= 0.02:
        return CLEAR
    end = smooth(0.0, 0.06, b) * smooth(0.0, 0.06, 1 - b)
    c = mix(ramp(CRIM, 0.3 + 0.5 * d), '#FFF0F2', core)
    return c + (body * (0.6 + 0.4 * end),)


def paint_aim(a, b):
    """Q4 aim line (lance, a -0.5..0.5, b 0..1): a thin red line with a soft glow."""
    d = abs(a) / 0.5
    core = 1 - smooth(0.12, 0.3, d)
    halo = 0.45 * (1 - smooth(0.2, 1.0, d))
    al = max(core, halo)
    if al < 0.04:
        return CLEAR
    return mix('#FF2A3A', '#FFC0C6', core) + (al,)


def paint_streak(a, b):
    """A soft streak (lance, a -0.5..0.5, b 0..1; symmetric along b; warm white, tinted): dashes, dives, zig-zags."""
    d = abs(a) / 0.5
    if d > 1:
        return CLEAR
    n = fbm(b * 7.0, a * 4.0 + 9.0)
    taper = smooth(0.0, 0.3, b) * smooth(0.0, 0.3, 1 - b)
    core = 1 - smooth(0.1, 0.35, d)
    al = (1 - smooth(0.4 + 0.3 * n, 1.0, d)) * taper
    if al < 0.03:
        return CLEAR
    return ramp(WARM, 1 - core) + (al,)


def paint_flame(a, b):
    """A flame tongue, root at b 0 (face, a -0.25..0.25, b 0..1; warm white, tinted)."""
    if b < 0 or b > 1:
        return CLEAR
    sway = 0.05 * math.sin(b * 7.0)
    w = 0.2 * (1 - b) ** 0.8 * (0.6 + 0.4 * smooth(0.0, 0.25, b))
    x = a - sway * b
    n = fbm(a * 9 + 1, b * 5)
    d = abs(x) / (w * (0.8 + 0.4 * n) + 1e-4)
    if d > 1.1:
        return CLEAR
    c = ramp(WARM, d)
    return c + ((1 - smooth(0.7, 1.1, d)) * (1 - smooth(0.75, 1.0, b)),)


def paint_ember(a, b):
    """A glowing ember fleck (face, BX; warm white, tinted)."""
    r = math.hypot(a, b * 1.3)
    if r > 1.0:
        return CLEAR
    return ramp(WARM, r) + ((1 - smooth(0.2, 1.0, r)),)


def paint_smoke(a, b):
    """A black-crimson smoke puff (face, BX)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    n = fbm(a * 3 + 8, b * 3 + 2)
    al = (1 - smooth(0.3, 1.0, r + 0.3 * (n - 0.5))) * 0.85
    if al < 0.03:
        return CLEAR
    return mix('#100406', '#4A0A12', n) + (al,)


def paint_burst(a, b):
    """A starburst (face, BX; warm white, tinted): a bright core and eight tapering rays."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    ph = math.atan2(a, b)
    ray = abs(math.cos(4 * ph)) ** 18 * (1 - smooth(0.2, 1.0, r))
    ray2 = abs(math.cos(4 * ph + math.pi / 4)) ** 30 * (1 - smooth(0.1, 0.6, r)) * 0.7
    core = 1 - smooth(0.05, 0.35, r)
    al = max(core, ray, ray2)
    if al < 0.03:
        return CLEAR
    return ramp(WARM, 1 - core) + (al,)


def paint_pillar(a, b):
    """The crimson flame column of T (cross, a -0.125..0.125, b 0..1): a bright crimson core, flame tongues licking up
    the edges, smoke-black top."""
    if b < 0 or b > 1:
        return CLEAR
    n = fbm(a * 24 + 3, b * 6 - 1)
    w = 0.12 * (0.75 + 0.35 * n) * (1 - 0.35 * b)
    d = abs(a) / w
    if d > 1.15:
        return CLEAR
    top = smooth(0.7, 1.0, b)
    c = ramp(CRIM, clamp01(0.15 + 0.85 * d))
    c = mix(c, SMOKE, 0.7 * top)
    return c + ((1 - smooth(0.8, 1.15, d)) * (1 - smooth(0.88, 1.0, b)),)


# ----------------------------------------------------------------------------- floor decals (flat, unit radius / length)
def paint_flood(a, b):
    """F the red flood (and the E70 pool, tinted darker): a translucent crimson wash, a brighter rim band near r 0.95,
    darker veins (ref p1_F_field.jpg v3 15.15-17.4)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    n = fbm(a * 4 + 1, b * 4 + 9)
    vein = 1 - smooth(0.0, 0.03, abs(fbm(a * 5 + 2, b * 5 + 5) - 0.5))
    al = 0.42 + 0.12 * n + 0.35 * math.exp(-((r - 0.95) / 0.04) ** 2)
    al *= 1 - smooth(0.97, 1.0, r)
    c = mix('#B0102A', '#FF3A4A', 0.4 * n + 0.6 * math.exp(-((r - 0.95) / 0.05) ** 2))
    c = mix(c, '#5A0812', 0.45 * vein)
    return c + (clamp01(al + 0.1 * vein),)


_CR = random.Random(77)


def _crack_lines():
    polys = []
    for k in range(13):
        th = 2 * math.pi * k / 13 + _CR.uniform(-0.15, 0.15)
        r0, r1 = _CR.uniform(0.0, 0.25), _CR.uniform(0.75, 0.98)
        pts = jag(_CR, r0 * math.sin(th), r0 * math.cos(th), r1 * math.sin(th), r1 * math.cos(th), 9, 0.05)
        polys.append(pts)
        for _ in range(3):
            i = _CR.randrange(2, len(pts) - 1)
            x, y = pts[i]
            ang = th + _CR.choice((-1, 1)) * _CR.uniform(0.4, 1.0)
            ln = _CR.uniform(0.08, 0.2)
            polys.append(jag(_CR, x, y, x + ln * math.sin(ang), y + ln * math.cos(ang), 4, 0.2))
    for ring in (0.38, 0.62, 0.86):
        pts = []
        a0 = _CR.uniform(0, 6.28)
        for j in range(22):
            th = a0 + 2 * math.pi * j / 21
            rr = ring * _CR.uniform(0.95, 1.05)
            pts.append((rr * math.sin(th), rr * math.cos(th)))
        cut = _CR.randrange(4, 18)
        polys.append(pts[:cut])
        polys.append(pts[cut + 2:])
    return make_lines([p for p in polys if len(p) > 1])


CRACK_LINES = _crack_lines()


def paint_cracks(a, b):
    """F after hit 2: glowing crimson cracks over the floor (flat, UNIT; ref p1_F_field.jpg v3 20.4-21.4)."""
    if math.hypot(a, b) > 1.0:
        return CLEAR
    d = lines_dist(a, b, CRACK_LINES, 0.03)
    core = 1 - smooth(0.003, 0.008, d)
    halo = 0.5 * math.exp(-(d / 0.02) ** 2)
    al = max(core, halo)
    if al < 0.04:
        return CLEAR
    return mix('#B0102A', '#FFB8C0', core) + (al,)


def paint_strip(a, b):
    """G strip (flat, a -0.5..0.5 across, b -0.5..0.5 along): a translucent red band with bright rails on both long
    edges, ends softened (ref p1_G_cross.jpg v3 34.8-36.0)."""
    d = abs(a) / 0.5
    t = abs(b) / 0.5
    if d > 1 or t > 1:
        return CLEAR
    rail = math.exp(-((d - 0.9) / 0.06) ** 2)
    n = fbm(b * 10 + 3, a * 2)
    al = max(0.32 + 0.1 * n, rail) * (1 - smooth(0.9, 1.0, t)) * (1 - smooth(0.96, 1.0, d))
    return mix('#C0122C', '#FF8A94', rail) + (al,)


def paint_band(a, b):
    """G rim tint band (flat, UNIT): a red annulus 0.7 .. 1.0 (soft edges); nested bands make the tint grow inward."""
    r = math.hypot(a, b)
    if r > 1.0 or r < 0.66:
        return CLEAR
    n = fbm(a * 5 + 2, b * 5)
    al = 0.42 * smooth(0.66, 0.72, r) * (1 - smooth(0.97, 1.0, r)) * (0.8 + 0.4 * n)
    return mix('#A00E24', '#E0283A', n) + (al,)


def paint_ring(a, b):
    """Q5A ring outline (flat, UNIT; ref p2_Q5_banquet_b.jpg v7 4.2-12.3): a thin bright red line at r 0.985, a soft
    glow falling off inward, nothing else."""
    r = math.hypot(a, b)
    if r > 1.0 or r < 0.8:
        return CLEAR
    line = math.exp(-((r - 0.975) / 0.014) ** 2)
    glow = 0.45 * math.exp(-((0.975 - r) / 0.08) ** 2) if r < 0.975 else 0.0
    al = max(line, glow)
    if al < 0.03:
        return CLEAR
    return mix('#E0182E', '#FFC8CE', line) + (al,)


# ----------------------------------------------------------------------------- gate icon
def paint_gate_icon(a, b):
    """Gate label icon (face, BX): a crimson scythe across a red moon."""
    r = math.hypot(a + 0.1, b - 0.12)
    out = CLEAR
    if r < 0.62:
        n = fbm(a * 3 + 2, b * 3)
        out = mix('#E0283A', '#7A0A1A', smooth(0.2, 0.62, r) * 0.8 + 0.2 * n) + (1.0,)
    elif r < 0.75:
        out = hexc('#FF3A4A') + (0.5 * (1 - smooth(0.62, 0.75, r)),)
    # haft: lower-left to upper-right
    d = seg_dist(a, b, -0.78, -0.82, 0.6, 0.72)
    if d < 0.055:
        out = over(mix('#2A0408', '#5A0A16', 1 - d / 0.055) + (1.0,), out)
    # the crescent blade at the top end, curving back to the left
    e = crescent(a, b, 0.3, 0.5, 0.48, 0.32, 0.36, 0.42)
    if e > 0:
        out = over(mix('#4A0812', '#FF6A72', e) + (1.0,), out)
    return out


# ----------------------------------------------------------------------------- HUD glyphs (x right, y up, -1..1)
def glyph_badge(x, y):
    """◆ of the 선혈의 충격 badge: a crimson diamond with a bright crimson rim and a pale core spark."""
    d = abs(x) + abs(y)
    if d > 1.0:
        return CLEAR
    if d > 0.78:
        return hexc('#FF5A64') + (1.0,)
    core = 1 - smooth(0.0, 0.45, d)
    return mix('#B0102A', '#FFD0D6', core) + (1.0,)
