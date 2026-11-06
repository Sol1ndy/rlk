"""Painted sprites of the 타키 (Tachy) fx kit (tools/build_mboss_tk_fx.py). Stdlib only, deterministic (fixed seeds).

Tachy (Stellar Blade) fights with one long sword whose edge burns orange (Pyro) or crackles white-gold (Electro): wide
flame arcs, golden crescent waves, golden lightning from the sky, a red-amber chest core / visor flare, a gold glint on
the blade, black metallic blade-feathers. Colours from the footage sheets (scratchpad tk/ref/fx_a.jpg, t_*.jpg; PLAN
§1-§5). The player's own effects (blue-white rings, white pillars, crossing white beams; ref/x_player_fx_v2.jpg) are not
painted here.

Card coordinates follow the fg / Apep kits: every painter takes (a, b) inside its kind's painter box and returns
straight-alpha (r, g, b, alpha) floats; +a is the card's local -x (the right seen from behind or from above), +b is up
(face cards) or forward (flat cards). Most sprites are near white / warm white so the item tint (custom_model_data)
gives the element colour: Pyro orange, Electro gold-white, the core flare amber / red / gold.

The helpers (noise, polylines, ramps) are copies of the Apep painter's so the kits can change apart.
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

_R = random.Random(20261029)
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


def star4(a, b, length, width):
    def ray(u, v):
        f = 1 - abs(u) / length
        if f <= 0:
            return 0.0
        return f ** 1.4 * math.exp(-(v / (width * f + 0.012)) ** 2)
    return max(ray(a, b), ray(b, a))


def glow_line(d, core, glow):
    """(core 0..1, halo 0..1) of a lightning line at distance d"""
    return (1.0 if d < core else math.exp(-((d - core) / (core * 0.6 + 1e-6)) ** 2)), math.exp(-(d / glow) ** 2)


# ----------------------------------------------------------------------------- flame ramp (warm white: tinted per element)
FIRE = rmp((0.0, '#FFFFFF'), (0.35, '#FFF4CC'), (0.65, '#FFCF86'), (1.0, '#FF9A48'))
GOLD = rmp((0.0, '#FFFFFF'), (0.4, '#FFF2B8'), (1.0, '#F0C04A'))


def _fire_px(d, alpha):
    """colour + alpha at the normalised distance d (0 core .. 1 edge) of a flame band"""
    if d >= 1.25 or alpha <= 0:
        return CLEAR
    c = ramp(FIRE, d)
    return c + (alpha * (1 - smooth(0.72, 1.22, d)),)


# ----------------------------------------------------------------------------- slash arcs (flat, a -1..1, b 0..1)
ARC_T0, ARC_T1 = -78.0, 78.0          # sweep bearings (degrees from +b toward +a)
ARC_RC = 0.80                         # band centre radius (unit radius = the hit reach at scale r)
ARC_F = (0.34, 0.60, 0.84, 1.0)       # head position of frames 0..3 (fraction of the sweep)


def make_arc(k):
    """Slash-arc sweep frame k: a flame band on the circle of radius ARC_RC, from the start bearing up to the head of
    frame k (the leading edge thick and white-hot, the tail thinner and fading); frame 3 = the whole arc, tail faded."""
    th = ARC_T0 + (ARC_T1 - ARC_T0) * ARC_F[k]

    def paint(a, b):
        r = math.hypot(a, b)
        if r < 0.4 or r > 1.0:
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
        px = _fire_px(d, fac)
        # flame licks trailing outward (streaks along the sweep)
        lick = vnoise(ph * 0.35 + 3.1 * k, r * 22.0)
        if dr > 0 and d < 2.2 and lick > 0.62:
            al = fac * 0.75 * (1 - smooth(1.0, 2.2, d)) * smooth(0.62, 0.8, lick)
            if al > px[3]:
                return ramp(FIRE, 0.75) + (al,)
        return px
    return paint


_ARE = random.Random(5)


def _arc_crackle():
    polys = []
    for j in range(3):
        rr = ARC_RC + (j - 1) * 0.07
        pts = []
        ph = ARC_T0 + 4
        while ph < ARC_T1 - 4:
            r = rr + _ARE.uniform(-0.06, 0.06)
            pts.append((r * math.sin(math.radians(ph)), r * math.cos(math.radians(ph))))
            ph += _ARE.uniform(5, 10)
        polys.append(pts)
        for _ in range(4):
            i = _ARE.randrange(1, len(pts) - 1)
            x, y = pts[i]
            ang = math.atan2(x, y) + _ARE.uniform(-0.25, 0.25)
            ln = _ARE.uniform(0.08, 0.16) * (1 if _ARE.random() < 0.5 else -1)
            polys.append(jag(_ARE, x, y, x + ln * math.sin(ang), y + ln * math.cos(ang), 3, 0.25))
    return make_lines(polys)


ARC_E_LINES = _arc_crackle()


def paint_arc_e(a, b):
    """Electro crackle over a slash arc: white-gold jagged filaments along the arc band (tint gold-white)."""
    if b < 0.05:
        return CLEAR
    d = lines_dist(a, b, ARC_E_LINES, 0.05)
    core, halo = glow_line(d, 0.0085, 0.03)
    al = max(core, 0.65 * halo)
    if al < 0.05:
        return CLEAR
    return mix('#FFF0B0', WHITE, core) + (al,)


# ----------------------------------------------------------------------------- crescent projectiles
def paint_crescent_h(a, b):
    """W1 ground crescent (a -0.5..0.5 wide, b -0.5..0.5): a wide shallow golden-flame bow ⌒, white-hot leading edge,
    flame licks trailing down / back."""
    u = a / 0.5
    if abs(u) > 1:
        return CLEAR
    top = 0.32 - 0.62 * u * u            # the bow: highest in the middle
    thick = 0.22 * (1 - u * u) ** 0.6 + 0.02
    dy = top - b
    if dy < -0.06:
        return CLEAR
    d = (dy + 0.04) / (thick + 1e-6)
    n = fbm(u * 6.0, b * 5.0)
    d = d / (0.75 + 0.5 * n)
    if d > 1.3:
        return CLEAR
    c = ramp(rmp((0.0, '#FFFFFF'), (0.25, '#FFF6CE'), (0.6, '#FFD27C'), (1.0, '#FF9C40')), d)
    return c + (1 - smooth(0.75, 1.25, d),)


def paint_crescent_v(a, b):
    """W2 air crescent (a -0.5..0.5, b -0.5..0.5): an upright crescent ( bowing toward -a, white-hot edge, flame back."""
    v = b / 0.5
    if abs(v) > 1:
        return CLEAR
    edge = -0.30 + 0.62 * v * v
    thick = 0.24 * (1 - v * v) ** 0.6 + 0.02
    dx = a - edge
    if dx < -0.06:
        return CLEAR
    n = fbm(v * 6.0 + 4.0, a * 5.0)
    d = (dx + 0.04) / (thick + 1e-6) / (0.75 + 0.5 * n)
    if d > 1.3:
        return CLEAR
    c = ramp(rmp((0.0, '#FFFFFF'), (0.25, '#FFF6CE'), (0.6, '#FFD27C'), (1.0, '#FF9C40')), d)
    return c + (1 - smooth(0.75, 1.25, d),)


# ----------------------------------------------------------------------------- rings (flat, unit radius)
def paint_spin_ring(a, b):
    """C1 spin: a full ring of fire (unit radius), wisps swirling clockwise; warm white (tinted per element)."""
    r = math.hypot(a, b)
    if r > 1.0 or r < 0.5:
        return CLEAR
    ph = math.atan2(a, b)
    sw = ph * 3.0 + r * 9.0
    n = fbm(math.cos(sw) * 2.0 + 5.0, math.sin(sw) * 2.0 + r * 4.0)
    rc = 0.80
    ht = 0.07 + 0.05 * n
    dr = r - rc
    d = abs(dr) / (ht * (1.6 if dr > 0 else 1.0))
    px = _fire_px(d, 1.0)
    lick = vnoise(ph * 9.0, r * 18.0)
    if dr > 0 and lick > 0.6 and d < 2.4:
        al = 0.7 * (1 - smooth(1.0, 2.4, d)) * smooth(0.6, 0.78, lick)
        if al > px[3]:
            return ramp(FIRE, 0.8) + (al,)
    return px


_SH = random.Random(17)


def _shock_lines():
    polys = []
    for k in range(14):
        a0 = 2 * math.pi * k / 14 + _SH.uniform(-0.12, 0.12)
        r0, r1 = _SH.uniform(0.55, 0.7), _SH.uniform(0.92, 0.99)
        polys.append(jag(_SH, r0 * math.sin(a0), r0 * math.cos(a0), r1 * math.sin(a0 + 0.08), r1 * math.cos(a0 + 0.08),
                         5, 0.18))
    pts = []
    for k in range(49):
        ph = 2 * math.pi * k / 48
        r = 0.86 + _SH.uniform(-0.035, 0.035)
        pts.append((r * math.sin(ph), r * math.cos(ph)))
    polys.append(pts)
    return make_lines(polys)


SHOCK_LINES = _shock_lines()


def paint_shock_ring(a, b):
    """L shock: a golden electric shock ring (unit radius): a crackling band at r 0.86, jagged filaments reaching in
    from it, a soft halo; warm white (tint gold)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    d = lines_dist(a, b, SHOCK_LINES, 0.05)
    core, halo = glow_line(d, 0.012, 0.04)
    band = math.exp(-((r - 0.86) / 0.07) ** 2) * 0.85
    al = max(core, 0.7 * halo, band)
    if al < 0.05:
        return CLEAR
    return mix('#FFE7A0', WHITE, max(core, band * 0.6)) + (al,)


# ----------------------------------------------------------------------------- lightning (bolt: cross, b 0..1, a +-0.25)
def make_bolt(seed):
    rnd = random.Random(seed)
    main = jag(rnd, rnd.uniform(-0.05, 0.05), 1.0, 0.0, 0.0, 12, 0.07)
    polys = [main]
    for _ in range(4):
        i = rnd.randrange(2, 10)
        x, y = main[i]
        x1 = max(-0.22, min(0.22, x + rnd.uniform(-0.18, 0.18)))
        polys.append(jag(rnd, x, y, x1, y - rnd.uniform(0.12, 0.25), 4, 0.15))
    lines = make_lines(polys)

    def paint(a, b):
        d = lines_dist(a, b, lines, 0.04)
        core, halo = glow_line(d, 0.012, 0.045)
        al = max(core, 0.7 * halo)
        if al < 0.05:
            return CLEAR
        return mix('#FFE08A', WHITE, core) + (al,)
    return paint


def make_sky_arc(seed):
    """K sky arcs: a thin golden arc crawling down from the top (b 0) to b -1, forking near its end."""
    rnd = random.Random(seed)
    main = jag(rnd, rnd.uniform(-0.06, 0.06), 0.0, rnd.uniform(-0.1, 0.1), -0.8, 10, 0.09)
    polys = [main]
    x, y = main[-1]
    for k in range(3):
        polys.append(jag(rnd, x, y, x + (k - 1) * 0.1 + rnd.uniform(-0.03, 0.03), -0.99, 3, 0.2))
    for _ in range(2):
        i = rnd.randrange(2, 8)
        x0, y0 = main[i]
        polys.append(jag(rnd, x0, y0, max(-0.23, min(0.23, x0 + rnd.uniform(-0.15, 0.15))), y0 - 0.15, 3, 0.2))
    lines = make_lines(polys)

    def paint(a, b):
        d = lines_dist(a, b, lines, 0.04)
        core, halo = glow_line(d, 0.009, 0.03)
        al = max(core, 0.6 * halo)
        if al < 0.05:
            return CLEAR
        return mix('#FFE08A', WHITE, core) + (al,)
    return paint


# ----------------------------------------------------------------------------- glints, flares (face, painter box -1..1)
def paint_glint_star(a, b):
    """The blade glint: a bold gold 4-point star (long rays), four short diagonal rays, a ring and a white-hot core."""
    r = math.hypot(a, b)

    def ray(u, v, ln, w):
        f = 1 - abs(u) / ln
        if f <= 0:
            return 0.0
        return f ** 0.75 * math.exp(-(v / (w * f + 0.02)) ** 2)
    s = max(ray(a, b, 1.0, 0.13), ray(b, a, 1.0, 0.13))
    d = max(ray((a + b) * 0.7071, (a - b) * 0.7071, 0.55, 0.08), ray((a - b) * 0.7071, (a + b) * 0.7071, 0.55, 0.08))
    ring = math.exp(-((r - 0.42) / 0.035) ** 2) * 0.9
    core = math.exp(-(r / 0.24) ** 2)
    al = clamp01(max(s, d * 0.85, ring, core * 1.2))
    if al < 0.04:
        return CLEAR
    return mix('#FFD860', WHITE, max(core, s ** 1.5)) + (al,)


def paint_core_flare(a, b):
    """The chest core / visor flare: a radial burst of 10 rays of uneven length around a hot core (white; tinted
    amber / red / gold)."""
    r = math.hypot(a, b)
    if r > 1.0:
        return CLEAR
    ph = math.atan2(a, b)
    rays = 0.0
    for k in range(10):
        ang = 2 * math.pi * k / 10 + 0.17 * math.sin(k * 2.7)
        ln = 0.55 + 0.4 * ((k * 7) % 5) / 4
        dph = math.atan2(math.sin(ph - ang), math.cos(ph - ang))
        w = 0.07 * (1 - r / ln) if r < ln else 0
        if w > 0:
            rays = max(rays, math.exp(-(dph * r / (w + 1e-6)) ** 2) * (1 - r / ln))
    glow = math.exp(-(r / 0.3) ** 2)
    core = math.exp(-(r / 0.12) ** 2)
    al = clamp01(max(rays, glow * 0.9))
    if al < 0.04:
        return CLEAR
    return mix('#FFD8B0', WHITE, max(core, rays * 0.5)) + (al,)


# ----------------------------------------------------------------------------- cocoon (face, a +-0.5, b -1..1)
def _cocoon_shape(a, b):
    v = b / 1.0
    hw = 0.48 * (1 - abs(v) ** 2.2) ** 0.55 * (1.0 if v < 0.6 else 1 - 0.3 * (v - 0.6))
    return hw


def paint_cocoon(a, b):
    """The overload mantle: the black blade-feather wings wrapped into a tall cocoon, overlapping metallic feather
    plates with bronze-gold edges, orange and gold energy veins and a gold rim (painted colours; tint white)."""
    hw = _cocoon_shape(a, b)
    if hw <= 0.01 or abs(a) > hw:
        return CLEAR
    e = 1 - abs(a) / hw
    if e < 0.06:
        return hexc('#D9A84A') + (1.0,)
    # feathers: bands slanting down and out from the centre seam
    s = b + abs(a) * 0.9
    band = (s * 6.5) % 1.0
    plate = mix('#14100E', '#3B2C22', 0.4 + 0.6 * (1 - band) * e)
    if band < 0.08:
        plate = mix(plate, hexc('#B98A3A'), 0.85)
    if abs(a) < 0.015:
        plate = hexc('#5A3E26')
    # veins
    n = fbm(a * 5.0 + 11.0, b * 3.5)
    vein = math.exp(-((n - 0.5) / 0.018) ** 2)
    n2 = fbm(a * 4.0 - 3.0, b * 4.5 + 7.0)
    vein2 = math.exp(-((n2 - 0.52) / 0.016) ** 2)
    if vein > 0.25:
        plate = mix(plate, hexc('#FF8A3D'), vein)
    if vein2 > 0.25:
        plate = mix(plate, hexc('#F4D45A'), vein2)
    return plate + (1.0,)


_CC = random.Random(23)


def _crack_lines():
    polys = []
    for k in range(9):
        ang = 2 * math.pi * k / 9 + _CC.uniform(-0.2, 0.2)
        x1, y1 = 0.42 * math.sin(ang), 0.95 * math.cos(ang)
        p = jag(_CC, _CC.uniform(-0.03, 0.03), _CC.uniform(-0.1, 0.2), x1, y1, 7, 0.12)
        polys.append(p)
        i = _CC.randrange(2, 6)
        x, y = p[i]
        polys.append(jag(_CC, x, y, x + _CC.uniform(-0.18, 0.18), y + _CC.uniform(-0.25, 0.25), 3, 0.2))
    return make_lines(polys)


CRACK_LINES = _crack_lines()


def paint_cocoon_crack(a, b):
    """Cracks of light over the cocoon (same extent): white-hot jagged lines with a glow (tint: the crack brightness)."""
    hw = _cocoon_shape(a, b)
    if hw <= 0.01 or abs(a) > hw * 0.98:
        return CLEAR
    d = lines_dist(a, b, CRACK_LINES, 0.05)
    core, halo = glow_line(d, 0.011, 0.04)
    al = max(core, 0.7 * halo)
    if al < 0.05:
        return CLEAR
    return mix('#FFE6A0', WHITE, core) + (al,)


# ----------------------------------------------------------------------------- feathers, embers, ash, flame
def _feather(a, b, glow):
    v = (b + 0.5) / 1.0                  # 0 quill .. 1 tip
    if v < 0 or v > 1:
        return CLEAR
    hw = 0.2 * math.sin(math.pi * min(1.0, v * 1.05) ** 0.75) ** 0.8
    if v < 0.12:
        hw = 0.025
    if abs(a) > hw:
        return CLEAR
    e = 1 - abs(a) / (hw + 1e-6)
    if glow:
        c = mix('#FFE07A', WHITE, e ** 1.5)
        return c + (0.6 + 0.4 * e,)
    spine = abs(a) < 0.018
    barb = ((v * 26 + abs(a) * 18) % 1.0) < 0.18
    c = mix('#120E0C', '#4A3A2E', 0.3 + 0.7 * e * (1 - v * 0.5))
    if barb:
        c = mix(c, hexc('#6A5440'), 0.5)
    if spine:
        c = hexc('#C89A3A')
    if e < 0.18:
        c = mix(c, hexc('#D8A84A'), 0.8)
    return c + (1.0,)


def paint_feather(a, b):
    """A black metallic blade-feather with a bronze-gold edge and spine (wings, death, blink)."""
    return _feather(a, b, False)


def paint_feather_glow(a, b):
    """A glowing gold-white feather (the mantle's falling feathers, Electro)."""
    return _feather(a, b, True)


def paint_ember(a, b):
    """A glowing ember fleck: white-hot core, warm edge, a slightly irregular outline (tinted)."""
    r = math.hypot(a, b) * (1 + 0.25 * (vnoise(a * 4 + 9, b * 4) - 0.5))
    if r > 0.95:
        return CLEAR
    c = ramp(rmp((0.0, '#FFFFFF'), (0.4, '#FFE6B0'), (1.0, '#FFB060')), r)
    return c + (1 - smooth(0.55, 0.95, r),)


def paint_ash(a, b):
    """A grey-black ash flake with a dim ember edge (death dissolve, T2 dark)."""
    r = math.hypot(a * 1.3, b) * (1 + 0.45 * (fbm(a * 3 + 2, b * 3 + 5) - 0.5))
    if r > 0.9:
        return CLEAR
    c = mix('#2E2A28', '#6E6863', fbm(a * 6, b * 6))
    if r > 0.74:
        c = mix(c, hexc('#B0502A'), 0.6)
    return c + (1.0,)


def paint_flame(a, b):
    """A flame tongue rising from its root (b 0) to b 1, white-hot core (tinted)."""
    if b < 0 or b > 1:
        return CLEAR
    w = 0.22 * (1 - b) ** 0.7 * (0.4 + 0.6 * math.sin(math.pi * min(1.0, b * 2.2)) ** 0.5)
    sway = 0.05 * math.sin(b * 7.0) * b
    x = a - sway
    if abs(x) > w + 0.02 or w <= 0:
        return CLEAR
    d = abs(x) / (w + 1e-6)
    n = vnoise(a * 9.0, b * 6.0 - 3.0)
    d = d / (0.8 + 0.4 * n)
    if d > 1.2:
        return CLEAR
    return ramp(FIRE, d) + (1 - smooth(0.7, 1.2, d),)


# ----------------------------------------------------------------------------- the rift tear fallback (face 64 x 96)
_TR = random.Random(31)
TEAR_EDGE = [(_TR.uniform(-0.05, 0.05)) for _ in range(40)]


def paint_tear(a, b):
    """Fallback of the arrival tear (used only while S1's rlk:rift/* models are absent): a black void lens with a
    jagged edge and a pale glow rim (the dungeon rift's colours)."""
    v = b / 0.5
    if abs(v) > 1:
        return CLEAR
    k = int((v + 1) * 19.5)
    hw = 0.3 * (1 - v * v) ** 0.7 + TEAR_EDGE[k] * (1 - v * v)
    e = abs(a) - hw
    if e < 0:
        return hexc('#05030A') + (1.0,)
    if e < 0.05:
        return mix('#F2F4FF', '#8A7CFF', e / 0.05) + (1.0 - e * 8,)
    return CLEAR


# ----------------------------------------------------------------------------- gate icon (face 64 x 64, box -1..1)
def paint_gate_icon(a, b):
    """The gate label icon: Tachy's long sword (diagonal from the lower left to the upper right, glowing yellow edge,
    round orange-ringed guard) behind a glowing yellow-orange skull (the visor skull of the intro), dark outlines
    (painted; tint white)."""
    sx, sy = (a + 0.12) / 0.78, (b + 0.2) / 0.78          # the skull: lower left of centre, radius ~0.42
    head = (sx / 0.52) ** 2 + ((sy - 0.08) / 0.5) ** 2
    jaw = abs(sx) < 0.3 and -0.66 < sy < -0.25
    if head <= 1.08 or (jaw and abs(sx) < 0.33):
        if head > 1.0 and not jaw or (jaw and abs(sx) >= 0.3):
            return hexc('#1A0C04') + (1.0,)
        eye = min(math.hypot(sx - 0.2, sy + 0.02), math.hypot(sx + 0.2, sy + 0.02))
        if eye < 0.13:
            return hexc('#2A0A04') + (1.0,)
        if abs(sx) < 0.05 and -0.27 < sy < -0.12:
            return hexc('#2A0A04') + (1.0,)
        if jaw and abs(sy + 0.47) < 0.035:
            return hexc('#2A0A04') + (1.0,)
        if jaw and sy < -0.62:
            return hexc('#1A0C04') + (1.0,)
        g = 1 - min(1.0, head)
        return mix('#FF7A1E', '#FFE680', g) + (1.0,)
    u = (a + b) * 0.7071                                  # along the sword (-1.3 .. 1.3)
    w = (a - b) * 0.7071
    if -1.25 < u < 1.3:
        guard = math.hypot(u + 0.62, w)
        if guard < 0.2:
            if guard > 0.17:
                return hexc('#1A1410') + (1.0,)
            return (hexc('#FF8A2A') if 0.1 < guard < 0.16 else hexc('#3A3634')) + (1.0,)
        if u > -0.62:
            hw = 0.11 * (1 - max(0.0, u - 1.0) / 0.3)
            if abs(w) < hw + 0.05 and hw > 0:
                if abs(w) >= hw:
                    return hexc('#1A1410') + (1.0,)
                if w > hw * 0.3:
                    return hexc('#FFE070') + (1.0,)
                return mix('#4A4A50', '#A0A0AA', (hw - abs(w)) / hw) + (1.0,)
        elif abs(w) < 0.07:
            return (hexc('#1A1410') if abs(w) > 0.045 else hexc('#5A4030')) + (1.0,)
    return CLEAR


# ----------------------------------------------------------------------------- HUD glyphs (x right, y up, -1..1)
def glyph_badge(x, y):
    """Badge ◈ (boss-bar name line): a white diamond outline around a white diamond core with dark outlines; tinted by
    the text component colour (the element colour)."""
    m = abs(x) + abs(y)
    if m > 0.98:
        return CLEAR
    if m > 0.86:
        return (0.12, 0.12, 0.12, 1.0)
    if m > 0.68:
        return WHITE + (1.0,)
    if m > 0.52:
        return (0.12, 0.12, 0.12, 1.0)
    if m > 0.42:
        return CLEAR
    if m > 0.32:
        return (0.12, 0.12, 0.12, 1.0)
    return WHITE + (1.0,)


def pixel_cell(state):
    """Mantle gauge cell, 4 x 8 px RGBA rows: 0 empty (dim bronze), 1 full (gold #F2C230 with a light top row and a
    darker base), 2 the left cap, 3 the right cap (a 1 px dark outline column); every cell has the dark top / bottom
    outline, so cells abut into one bar."""
    w, h = 4, 8
    out = hexc('#2A1E08')
    rows = []
    for j in range(h):
        row = []
        for i in range(w):
            edge = j in (0, h - 1)
            if state in (2, 3):
                col_on = (i == w - 1) if state == 2 else (i == 0)
                row.append(out + (1.0,) if col_on else CLEAR)
                continue
            if edge:
                row.append(out + (1.0,))
            elif state == 1:
                row.append((hexc('#FFF0A8') if j == 1 else hexc('#F2C230') if j < 5 else hexc('#C8962A')) + (1.0,))
            else:
                row.append(hexc('#4A3A1C') + (0.85,))
        rows.append(row)
    return w, h, rows
