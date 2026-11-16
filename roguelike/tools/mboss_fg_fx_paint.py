"""Painted sprites of the field generator's fx kit (tools/build_mboss_fg_fx.py). Stdlib only.

The third mid-boss is 실험성 역장 발생 장치 (nameplate 브레게 프로토타입): a floating brass gravity device. Its effects are
gold and brass (bombs, columns, lasers, drill missiles, crystal bursts, the gravity-wave fire band) plus the violet
Ousia field (column, glitch streaks) and a white-cyan warp. Every hex value below was sampled from the reference
videos (scratchpad mb3/understand/v1-v4.md, §5 / §7 / §4 palettes and the per-event notes).

Every painter takes card coordinates (a, b) inside its kind's painter box and returns straight-alpha
(r, g, b, alpha) floats. Card coordinates follow the butterfly kit (tools/mboss_bf_fx_paint.py): +a is the card's
local -x (the right when seen from behind or from above), +b is up (face cards) or forward (flat cards). Cross
kinds (two crossed quads) paint +b along their long axis; the band kind paints its flat strip in v > 0 and its
flame wall in v < 0 (see paint_wave_band); the box kind paints one face texture used on all six faces.

Neutral sprites (white or near white) are tinted per spawn by the item definitions' minecraft:custom_model_data
tint, which multiplies the texture colour.

The shared helpers (noise, ramps, the telegraph textures, the neutral glow / glint / mote / streak / ripple) are
copies of the butterfly painter's, so the two kits can change apart; fg_fx_api.md §12 describes the later
refactor into one shared module.
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
    """ramp stops from (t, '#hex') pairs"""
    return [(t, hexc(h)) for t, h in pairs]


def even(*hexes):
    """ramp stops evenly spaced over 0..1"""
    n = len(hexes) - 1
    return [(k / n, hexc(h)) for k, h in enumerate(hexes)]


CLEAR = (0.0, 0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)
DARK = (0.055, 0.035, 0.05)          # telegraph outline (stays dark under any tint)

# ----------------------------------------------------------------------------- noise and geometry
_R = random.Random(20261018)
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
    """distance to a polyline"""
    return min(seg_dist(px, py, ax, ay, bx, by) for (ax, ay), (bx, by) in zip(pts, pts[1:]))


def lines_dist(px, py, lines, box=None):
    """distance to the nearest of several polylines (lines = [(bbox, pts), ...] from make_lines)"""
    best = 9.0
    for (x0, y0, x1, y1), pts in lines:
        if px < x0 - 0.08 or px > x1 + 0.08 or py < y0 - 0.08 or py > y1 + 0.08:
            continue
        best = min(best, poly_dist(px, py, pts))
    return best


def make_lines(polys):
    out = []
    for pts in polys:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        out.append(((min(xs), min(ys), max(xs), max(ys)), pts))
    return out


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
    """4-point star intensity (0..1) with rays along the card axes."""
    def ray(u, v):
        f = 1 - abs(u) / length
        if f <= 0:
            return 0.0
        return f ** 1.4 * math.exp(-(v / (width * f + 0.012)) ** 2)
    return max(ray(a, b), ray(b, a))


def rock_poly(rnd, n, irr=0.35):
    """irregular convex-ish polygon around the origin, unit size: list of (angle, radius)"""
    angs = sorted(rnd.uniform(0, 2 * math.pi) for _ in range(n))
    return [(t, 1.0 - irr * rnd.random()) for t in angs]


def in_rock(x, y, poly):
    """(inside?, edge margin 0..1) of a point in a rock_poly: a star-shaped polygon with straight edges between its
    vertices (angle, radius), so rocks read as faceted chunks, not blobs"""
    th = math.atan2(y, x) % (2 * math.pi)
    r = math.hypot(x, y)
    n = len(poly)
    for k in range(n):
        t0, r0 = poly[k - 1]
        t1, r1 = poly[k]
        if k == 0:
            t0 -= 2 * math.pi
        if t0 <= th <= t1 or (k == 0 and th - 2 * math.pi >= t0):
            px, py = r0 * math.cos(t0), r0 * math.sin(t0)
            qx, qy = r1 * math.cos(t1), r1 * math.sin(t1)
            dx, dy = qx - px, qy - py
            ux, uy = math.cos(th), math.sin(th)
            den = ux * dy - uy * dx
            edge = (px * dy - py * dx) / den if abs(den) > 1e-9 else min(r0, r1)
            return r < edge, (edge - r) / max(edge, 1e-9)
    return False, 0.0


# ----------------------------------------------------------------------------- palettes (sampled hex)
GOLD_BODY = rmp((0, '#5E4232'), (0.2, '#79592C'), (0.42, '#A3875C'), (0.62, '#C1AD8B'), (0.8, '#EBC263'),
                (1, '#F6E5B8'))
COLUMN = rmp((0, '#C3A48C'), (0.35, '#E0BE98'), (0.65, '#FBEBB8'), (0.85, '#FDFBD1'), (1, '#FFFFFF'))
LASER_GLOW = rmp((0, '#A97A3A'), (0.3, '#D4A558'), (0.65, '#E4BB76'), (1, '#FCD88F'))
WAVE_FIRE = rmp((0, '#FFFFF0'), (0.06, '#FDFBD1'), (0.14, '#FDF3AA'), (0.24, '#FBE483'), (0.36, '#F2BB68'),
                (0.5, '#E4A568'), (0.64, '#D29253'), (0.8, '#B86A3A'), (1, '#8C4A2A'))
FLAME_G = rmp((0, '#C36439'), (0.2, '#DE864D'), (0.45, '#F1BF71'), (0.7, '#FADE8E'), (0.88, '#FEF5AD'),
              (1, '#FFFFF0'))
VIOLET = rmp((0, '#3A2290'), (0.18, '#4430CA'), (0.36, '#543CAC'), (0.55, '#7562D0'), (0.72, '#957FDF'),
             (0.86, '#CCB7E2'), (1, '#E6DDF6'))
WARP = rmp((0, '#9FCBEA'), (0.3, '#C2E1F5'), (0.62, '#DFF6FB'), (0.85, '#F7FCFD'), (1, '#FFFFFF'))
ROCK_LIT = rmp((0, '#5E4232'), (0.25, '#A88263'), (0.5, '#CF9E87'), (0.72, '#D5AC82'), (0.88, '#DCA977'),
               (1, '#E7B683'))
CRYSTAL_LIT = rmp((0, '#EDCBA1'), (0.55, '#FBEEC8'), (1, '#FFFFFF'))
CRYSTAL_SHADE = rmp((0, '#9A7454'), (0.5, '#D2AB8C'), (1, '#EDCBA1'))


# ----------------------------------------------------------------------------- bombs and missiles
def paint_bomb(a, b):
    """Gold bomb (C1 일점 상쇄): dark core #743B01 / #78470A, glowing equator ring #E1BC7E / #FCE8AE / #E8CA85 with
    three port glows, a warm halo (v1 §5 'Bombs', zoom_f0480)."""
    r = math.hypot(a, b)
    R = 0.6
    if r > 1:
        return CLEAR
    if r < R:
        nz = math.sqrt(max(0.0, 1 - (r / R) ** 2))
        nx, ny = a / R, b / R
        lam = clamp01(0.3 + 0.7 * (-0.42 * nx + 0.5 * ny + 0.72 * nz))
        col = ramp(rmp((0, '#241000'), (0.4, '#4E2602'), (0.7, '#743B01'), (0.88, '#78470A'), (1, '#A8742A')), lam)
        yb = b - 0.12 * a + 0.03
        hw = 0.07 * nz + 0.012
        d = abs(yb)
        if d < hw:
            col = mix('#E1BC7E', '#FCE8AE', 1 - d / hw)
            col = mix(col, WHITE, 0.4 * (1 - d / hw) ** 3)
        elif d < hw + 0.025:
            col = mix(col, '#E8CA85', 0.6 * (1 - (d - hw) / 0.025))
        for px, py in ((-0.28, 0.22), (0.02, 0.27), (0.31, 0.2)):
            dp = math.hypot(a - px, (b - py) * 1.4)
            if dp < 0.075:
                col = mix('#E8CA85', '#FFF4C8', 1 - dp / 0.075) if dp < 0.05 else hexc('#2A1200')
        spec = math.exp(-(((a + 0.22) / 0.11) ** 2 + ((b - 0.34) / 0.07) ** 2))
        col = mix(col, '#FFF1D0', 0.55 * spec)
        return col + (1.0,)
    g = 0.55 * (1 - (r - R) / (1 - R)) ** 2
    return hexc('#E8CA85') + (g,) if g > 0.02 else CLEAR


_BB = random.Random(1300)
BOMB_SPIKES = [(k * 30 + _BB.uniform(-9, 9), _BB.uniform(0.62, 0.98), _BB.uniform(0.07, 0.12)) for k in range(12)] + \
              [(k * 30 + 15 + _BB.uniform(-6, 6), _BB.uniform(0.32, 0.55), _BB.uniform(0.045, 0.07)) for k in range(12)]


def _spiky(a, b, spikes):
    r = math.hypot(a, b)
    phi = math.atan2(a, b)
    inside, edge = False, 1.0
    for deg, length, w0 in spikes:
        if r >= length:
            continue
        dphi = (phi - math.radians(deg) + math.pi) % (2 * math.pi) - math.pi
        if abs(dphi) > math.pi / 2:
            continue
        perp = r * math.sin(abs(dphi))
        w = w0 * (1 - r / length) + 0.004
        if perp < w:
            inside = True
            edge = min(edge, (w - perp) / w)
    return r, inside, edge


def paint_bomb_burst(a, b):
    """Bomb burst r 1.3 (C1): gold spiky starburst #FAE1B2 / #E4C09A / #CAA481 with dark flecks #793D15 and a
    warm haze #F8E0B0 (v1 §3 A, §5)."""
    r, inside, edge = _spiky(a, b, BOMB_SPIKES)
    if r < 0.17 or inside:
        col = ramp(rmp((0, '#B8875A'), (0.3, '#CAA481'), (0.5, '#E4C09A'), (0.72, '#FAE1B2'), (0.88, '#FFFBEA'),
                       (1, '#FFFFFF')), 1 - r)
        if r >= 0.17 and edge < 0.3:
            col = mix(col, '#9A6A3A', (0.3 - edge) / 0.3 * 0.55)
        return col + (1.0,)
    if 0.25 < r < 0.95 and vnoise(a * 15 + 3, b * 15 + 3) > 0.83:
        return hexc('#793D15') + (0.92,)
    haze = 0.42 * math.exp(-(r / 0.42) ** 2)
    return (hexc('#F8E0B0') + (haze,)) if haze > 0.02 else CLEAR


def paint_missile(a, b):
    """Gold drill missile (C4 바위 폭탄), nose at +b: spiral-grooved gold body #C1AD8B / #A3875C / #79592C with an
    #EBC263 highlight, a hot nose glow #FEFBDC, a bronze collar and a short exhaust (v1 §3 M, zoom_f1686)."""
    if b > 0.5 or b < -0.5:
        return CLEAR
    if b >= -0.22:
        t = (b + 0.22) / 0.72
        hw = 0.122 * (1 - t) ** 0.8 + 0.004
        if abs(a) <= hw:
            u = a / hw
            shade = clamp01(0.62 - 0.38 * u + 0.12 * (1 - abs(u)))
            col = ramp(GOLD_BODY, shade)
            groove = math.sin(b * 52 + u * 2.6)
            if groove > 0.55:
                col = mix(col, '#79592C', 0.7)
            elif groove < -0.8 and u < 0.2:
                col = mix(col, '#F6E5B8', 0.45)
            col = mix(col, '#FEFBDC', smooth(0.72, 1.0, t))
            return col + (1.0,)
        if t > 0.6:
            g = 0.55 * math.exp(-((abs(a) - hw) / 0.035) ** 2) * smooth(0.6, 1.0, t)
            return hexc('#FEFBDC') + (g,) if g > 0.02 else CLEAR
        return CLEAR
    if b >= -0.32:
        if abs(a) <= 0.13:
            col = mix('#583412', '#94704A', 0.5 - 0.5 * a / 0.13)
            if abs(b + 0.27) < 0.018:
                col = hexc('#F6E5B8')
            return col + (1.0,)
        return CLEAR
    t = (-0.32 - b) / 0.18
    hw = 0.085 * (1 - 0.6 * t)
    if abs(a) > hw:
        return CLEAR
    u = abs(a) / hw
    col = ramp(rmp((0, '#FFFFF0'), (0.35, '#FFF4C8'), (0.7, '#F2B65C'), (1, '#E09A45')), max(u, t))
    return col + (clamp01((1 - t) * (1 - 0.5 * u) * 1.2),)


def paint_smoke(a, b):
    """Missile smoke puff (C4 trails): blue-white #E2E8EC / #B8DDFB, soft and ragged (v1 §5 'Missiles')."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    edge = 0.72 + 0.22 * fbm(math.cos(th) * 1.6 + 3, math.sin(th) * 1.6 + 3, 3)
    if r > edge:
        return CLEAR
    u = r / edge
    n = fbm(a * 3 + 7, b * 3 + 7, 3)
    col = mix('#F2F5F7', '#B8DDFB', u * 0.75 + (n - 0.5) * 0.4)
    return col + (clamp01((1 - u ** 2) * (0.5 + 0.4 * n)),)


# ----------------------------------------------------------------------------- columns, beams, lasers
def paint_column(a, b):
    """Gold light column (slam tell, wave beam, vent shaft, up-beam; cross kind, foot at b = 0): white-gold core
    #FDFBD1 / #FBEBB8, body #E0BE98, edge #C3A48C, soft vertical streaks, a flared foot (v1 §5 'Slam column',
    v2 §7, v4 §5)."""
    if b < 0 or b > 1:
        return CLEAR
    flare = 1.0 + 0.55 * math.exp(-b / 0.06)
    x = a / flare
    core = math.exp(-(x / 0.12) ** 2)
    body = math.exp(-(x / 0.32) ** 2)
    streak = fbm(a * 13 + 2, b * 1.6, 2)
    i = max(core, 0.78 * body * (0.62 + 0.38 * streak))
    col = ramp(COLUMN, i)
    alpha = clamp01(i * 1.15) * (1 - smooth(0.86, 1.0, b))
    if alpha < 0.02:
        return CLEAR
    return col + (alpha,)


def paint_laser_core(a, b):
    """Laser beam core (C3 레이저 빔; cross kind along -b from the muzzle at b = 0): white #FFF6DA centre fading to
    #FADEA8 (v1 §3 L: core #FADEA8, edge #D4A558)."""
    if b > 0 or b < -1:
        return CLEAR
    core = math.exp(-(a / 0.2) ** 2)
    hot = math.exp(-(a / 0.07) ** 2)
    sh = 0.93 + 0.07 * math.sin(b * 23 + 3 * fbm(a * 3, b * 5, 2))
    col = mix(mix('#FADEA8', '#FFF6DA', core), WHITE, hot * 0.7)
    alpha = clamp01(core * 1.25 * sh)
    return col + (alpha,) if alpha > 0.02 else CLEAR


def paint_laser_glow(a, b):
    """Laser beam glow sleeve (cross kind along -b): gold #FCD88F / #E4BB76 fading to #D4A558 / #A97A3A; scale it
    to bloom the beam width 0.5 -> 1.0 -> 0.5 b (v1 §3 L)."""
    if b > 0 or b < -1:
        return CLEAR
    g = math.exp(-(a / 0.36) ** 2)
    n = fbm(a * 4 + 9, b * 7, 2)
    col = ramp(LASER_GLOW, g)
    alpha = 0.62 * g * (0.82 + 0.18 * n)
    return col + (alpha,) if alpha > 0.02 else CLEAR


def paint_muzzle(a, b):
    """Laser muzzle ring (C3, at the medallion): gold ring #FADBA0 / #E2BB81 around a dark emitter #8A5325 with a hot
    centre #FFF6DA (v1 §5 'Lasers')."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r < 0.36:
        return mix('#FFFFFF', '#FADEA8', r / 0.36) + (clamp01(1.0 - 0.3 * r / 0.36),)
    if r < 0.48:
        return mix('#8A5325', '#793000', (r - 0.36) / 0.12) + (0.95,)
    if r < 0.74:
        w = abs(r - 0.61) / 0.13
        return mix('#FADBA0', '#E2BB81', w) + (1.0,)
    if r < 0.78:
        return hexc('#5E3A18') + (0.9,)
    g = 0.5 * (1 - (r - 0.78) / 0.22) ** 2
    return hexc('#FADBA0') + (g,)


def paint_scorch(a, b):
    """Floor scorch (laser floor spots, bomb marks): dark brown burn with a glowing gold centre #FADEA8 (v1 §3 L
    'scorch + sparks')."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    edge = 0.78 + 0.2 * fbm(math.cos(th) * 1.8 + 1, math.sin(th) * 1.8 + 1, 3)
    if r > edge:
        return CLEAR
    u = r / edge
    n = fbm(a * 5 + 4, b * 5 + 4, 3)
    col = ramp(rmp((0, '#FFF6DA'), (0.18, '#FADEA8'), (0.4, '#B87A3A'), (0.62, '#8A5325'), (1, '#3A2414')),
               u + (n - 0.5) * 0.15)
    return col + (clamp01(0.85 * (1 - u ** 1.6) + 0.1 * n),)


# ----------------------------------------------------------------------------- rings, discs, spheres
_SR = random.Random(70)
SLAM_FLECKS = [(_SR.uniform(0, 2 * math.pi), _SR.uniform(0.74, 0.97), _SR.uniform(0.02, 0.045)) for _ in range(30)]


def paint_slam_ring(a, b):
    """Slam shock ring (C1 / C2 slam r 5; unit radius): a bright gold band #FFF8E6 / #F9DFAD / #E4BA87 at r 0.86, a
    dusty fringe #CAA376 / #B48F64 outside, crystal flecks #FDE8A2 (v1 §5 'Slam column / impact')."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    for t, rr, s in SLAM_FLECKS:
        x, y = rr * math.cos(t), rr * math.sin(t)
        if abs(a - x) < s and abs(b - y) < s and abs(a - x) + abs(b - y) < s * 1.2:
            return hexc('#FDE8A2') + (1.0,)
    d = r - 0.86
    core = math.exp(-(d / 0.03) ** 2)
    wide = math.exp(-(d / 0.085) ** 2)
    if d > 0:
        n = fbm(th * 5 + 1, r * 9, 3)
        dust = 0.75 * n * (1 - d / 0.14) if d < 0.14 else 0.0
        if core > 0.4:
            return mix('#F9DFAD', '#FFF8E6', core) + (1.0,)
        return mix('#B48F64', '#CAA376', n) + (clamp01(max(dust, wide * 0.8)),)
    if core > 0.35:
        return mix('#E4BA87', '#FFF8E6', core) + (1.0,)
    wash = 0.16 * (r / 0.86) ** 3
    col = mix('#F9DFAD', '#E4BA87', 1 - wide)
    return col + (clamp01(max(wash, wide * 0.75)),)


def paint_dust(a, b):
    """Tan dust puff (slam dust ring, impacts): lit #E4BA87, mid #CAA376, shade #B48F64 (v1 §5)."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    edge = 0.7 + 0.25 * fbm(math.cos(th) * 1.5 + 5, math.sin(th) * 1.5 + 5, 3)
    if r > edge:
        return CLEAR
    u = r / edge
    n = fbm(a * 3.5 + 11, b * 3.5 + 11, 3)
    lit = clamp01(0.5 + 0.6 * b + 0.3 * (n - 0.5))
    col = ramp(rmp((0, '#9C7650'), (0.35, '#B48F64'), (0.65, '#CAA376'), (1, '#E4BA87')), lit)
    return col + (clamp01((1 - u ** 1.8) * (0.62 + 0.3 * n)),)


def paint_charge_sphere(a, b):
    """Gravity-wave charge sphere (「인력 충격파」): bright yellow #FDEEAA core, #F5CF88 / #E2AE66 limb, #BC8354 rim,
    three orbit-swirl lines #FDFBD1 (v2 §3 B1 'bright yellow sphere ... with orbit-swirl lines')."""
    r = math.hypot(a, b)
    R = 0.88
    if r > 1:
        return CLEAR
    if r > R:
        g = 0.45 * (1 - (r - R) / (1 - R)) ** 2
        return hexc('#F5CF88') + (g,)
    q = r / R
    limb = smooth(0.35, 0.98, q)
    col = ramp(rmp((0, '#FFFDE8'), (0.3, '#FDEEAA'), (0.62, '#F5CF88'), (0.84, '#E2AE66'), (1, '#BC8354')),
               0.15 + 0.85 * limb)
    line = 0.0
    for tilt in (0.35, -0.55, 1.25):
        c, s = math.cos(tilt), math.sin(tilt)
        x, y = (a * c + b * s) / 0.8, (-a * s + b * c) / 0.26
        e = math.hypot(x, y)
        line = max(line, math.exp(-((e - 1) / 0.07) ** 2) * (0.5 + 0.5 * (y > -0.2)))
    col = mix(col, '#FDFBD1', line * 0.9)
    core = math.exp(-(q / 0.35) ** 2)
    alpha = 0.5 + 0.35 * limb + 0.3 * core + 0.4 * line
    return col + (clamp01(alpha),)


def paint_flare_dome(a, b):
    """Burst flare dome (「인력 충격파」 impact, a white-gold dome about 4 m wide and 2 m tall; face kind, pivot at the
    base centre): #FDFBD1 / #FDF3AA core, #F2BB68 mid, #CE9361 edge, ragged top (v2 §3 B1, §7)."""
    if b < 0:
        return CLEAR
    x, y = a / 0.5, b / 0.5
    rr = math.hypot(x, y)
    th = math.atan2(y, x)
    edge = 0.92 - 0.1 * fbm(th * 3.2 + 4, 1.7, 3)
    if rr > edge + 0.08:
        return CLEAR
    if rr > edge:
        g = 0.4 * (1 - (rr - edge) / 0.08)
        return hexc('#F2BB68') + (g,)
    u = rr / edge
    n = fbm(x * 3 + 2, y * 3 + 9, 2)
    col = ramp(rmp((0, '#FFFFFF'), (0.25, '#FDFBD1'), (0.5, '#FDF3AA'), (0.78, '#F2BB68'), (1, '#CE9361')),
               u ** 1.25 + (n - 0.5) * 0.12)
    alpha = 0.97 - 0.42 * u ** 2
    if u > 0.9:
        col = mix(col, '#FDF3AA', 0.6)
        alpha = max(alpha, 0.8)
    return col + (clamp01(alpha),)


def paint_fire_disc(a, b):
    """Filled fire disc (wave start r 1.8, the 파쇄 flame band under the ring): #F8EACF / #FDEEB0 centre, #FADC9F /
    #EFC78D body, rim glow #E6A55F, ragged flame edge (v2 §3 B1, v3 §4 'Flame band' #FEF5AD / #DE864D)."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    edge = 0.8 + 0.16 * fbm(math.cos(th) * 2.2 + 5, math.sin(th) * 2.2 + 5, 3)
    if r > edge:
        g = 0.45 * math.exp(-((r - edge) / 0.05) ** 2)
        return hexc('#DE864D') + (g,) if g > 0.02 and r <= 1 else CLEAR
    u = r / edge
    n = fbm(a * 3 + 2, b * 3 + 2, 3)
    sw = math.sin(4 * th + r * 9 + n * 5)
    col = ramp(rmp((0, '#FFF8E6'), (0.2, '#F8EACF'), (0.4, '#FDEEB0'), (0.6, '#FADC9F'), (0.8, '#EFC78D'),
                   (0.93, '#E6A55F'), (1, '#DE864D')), u * 0.95 + (n - 0.5) * 0.18)
    col = mix(col, '#FEF5AD', 0.3 * smooth(0.6, 1.0, sw) * (1 - u))
    alpha = 0.9 - 0.25 * u + 0.1 * n
    return col + (clamp01(alpha),)


_ER = random.Random(281)
ERUPT_CRACKS = []
for _k in range(9):
    _t = _ER.uniform(0, 2 * math.pi)
    _r0 = _ER.uniform(0.0, 0.35)
    _r1 = _ER.uniform(0.55, 0.88)
    _p = jag(_ER, _r0 * math.cos(_t), _r0 * math.sin(_t), _r1 * math.cos(_t + _ER.uniform(-0.4, 0.4)),
             _r1 * math.sin(_t + _ER.uniform(-0.4, 0.4)), 6, 0.12)
    ERUPT_CRACKS.append(_p)
ERUPT_CRACKS = make_lines(ERUPT_CRACKS)


def paint_erupt_disc(a, b):
    """Dark eruption disc (감소 영역 zones, r 2.8; 지면 충격 marker): a dark translucent fill (the floor about 35 %
    darker), thin gold crack lines #E4C5AA, an amber rim #CF9062 / #ED9A6B (v2 §7 'Zones', v3 §4, v4 §5)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.965:
        return hexc('#ED9A6B') + (0.55 * (1 - (r - 0.965) / 0.035),)
    if r > 0.925:
        return mix('#ED9A6B', '#CF9062', (r - 0.925) / 0.04) + (1.0,)
    if r > 0.905:
        return hexc('#3A2418') + (0.75,)
    d = lines_dist(a, b, ERUPT_CRACKS)
    if d < 0.011:
        return hexc('#F2D7B8') + (0.9,)
    if d < 0.03:
        return hexc('#E4C5AA') + (0.45 * (1 - (d - 0.011) / 0.019),)
    n = fbm(a * 4 + 1, b * 4 + 1, 3)
    return mix('#1E1612', '#3A2C24', n) + (clamp01(0.36 + 0.1 * n + 0.08 * smooth(0.6, 0.9, r)),)


_EB = random.Random(98)
ERUPT_CHUNKS = []
for _k in range(15):
    _y = _EB.uniform(0.12, 0.92)
    _x = _EB.uniform(-1, 1) * (0.1 + 0.32 * _y)
    ERUPT_CHUNKS.append((_x, _y, _EB.uniform(0.06, 0.12) * (1.25 - 0.45 * _y), _EB.uniform(0, math.pi),
                         rock_poly(_EB, 5, 0.42)))


def paint_erupt_burst(a, b):
    """Gold eruption burst with floor chunks (감소 영역; face kind, pivot at the floor): a gold glow fan #FCEBBC /
    #E3C794 / #D3B28B and tumbling sandy-gold chunks #F2CBA2 / #DBB49D / #CA9E80 with orange cracks #EAC99F (v2 §7,
    v3 §4 'Eruption mound')."""
    if b < 0 or b > 1:
        return CLEAR
    for x, y, s, rot, poly in ERUPT_CHUNKS:
        dx, dy = (a - x) / s, (b - y) / s
        if abs(dx) > 1.2 or abs(dy) > 1.2:
            continue
        c, sn = math.cos(rot), math.sin(rot)
        u, v = dx * c + dy * sn, -dx * sn + dy * c
        ins, m = in_rock(u, v, poly)
        if ins:
            if dy > 0.15 - 0.3 * dx:
                col = mix('#F2CBA2', '#F1D6BF', 0.5 + 0.5 * dy)
            elif dx > 0:
                col = mix('#A8805E', '#CA9E80', 0.3)
            else:
                col = hexc('#DBB49D')
            if m < 0.14:
                col = mix(col, '#5E4232', 0.65)
            if abs(u * 0.6 + v + 0.1) < 0.09 and m > 0.18:
                col = hexc('#EAC99F')
            return col + (1.0,)
    w = 0.1 + 0.4 * b
    if abs(a) > w:
        return CLEAR
    f = abs(a) / w
    n = fbm(a * 6 + 3, b * 5, 3)
    rays = fbm(math.atan2(a, b + 0.25) * 9 + 5, 0.5, 2)       # streaks bursting up from the base
    i = (1 - f ** 1.6) * (1 - b) ** 0.7 * (0.6 + 0.4 * n) * (0.7 + 0.6 * smooth(0.45, 0.75, rays))
    i = max(i, math.exp(-((a / 0.22) ** 2 + (b / 0.16) ** 2)))
    col = ramp(rmp((0, '#C9A06E'), (0.3, '#D3B28B'), (0.55, '#E3C794'), (0.8, '#FCEBBC'), (1, '#FFFBEA')), i)
    return col + (clamp01(i * 1.35),) if i > 0.04 else CLEAR


_CK = random.Random(33)
CHUNK_POLY = rock_poly(_CK, 6, 0.42)


def paint_chunk(a, b):
    """Floor chunk / rock (eruptions, blast rocks, debris): lit tan #DCA977 / #D5AC93, shade #A88263, dark outline,
    a glowing orange crack #EAC99F (v4 §5 'Rocks', v2 §7)."""
    ins, m = in_rock(a / 0.92, b / 0.92, CHUNK_POLY)
    if not ins:
        return CLEAR
    n = fbm(a * 6 + 2, b * 6 + 2, 2)
    if b - 0.35 * a > 0.12:
        col = mix('#DCA977', '#E7B683', n)            # lit top facet
    elif a > 0.05:
        col = mix('#A88263', '#8E6A50', n)            # shaded side
    else:
        col = mix('#CF9E87', '#D5AC93', n)            # front facet
    if m < 0.12:
        col = mix(col, '#4A3426', 0.7)
    if seg_dist(a, b, -0.45, -0.2, 0.15, 0.1) < 0.06 or seg_dist(a, b, 0.15, 0.1, 0.4, 0.45) < 0.05:
        col = mix('#EAC99F', '#FFF1D0', 0.4)
    return col + (1.0,)


_PB = random.Random(44)
PEBBLE_POLY = rock_poly(_PB, 6, 0.4)


def paint_pebble(a, b):
    """Floating pebble (low-gravity field cue, debris): grey-tan stone #B99177 / #9E8C80 with a dark shade #74686E
    (v1 §3 F 'small pebbles float', v2 §7 dark rocks #74686E / #705355)."""
    ins, m = in_rock(a / 0.85, b / 0.85, PEBBLE_POLY)
    if not ins:
        return CLEAR
    if b - 0.3 * a > 0.1:
        col = mix('#9E8C80', '#C9A88E', 0.5 + 0.5 * b)
    elif a > 0.1:
        col = hexc('#5E4E54')
    else:
        col = mix('#74686E', '#705355', 0.5)
    if m < 0.12:
        col = mix(col, '#2E2628', 0.6)
    return col + (1.0,)


_SF = random.Random(400)
FAN_SPIKES = [(-48 + _SF.uniform(-5, 5), 0.62, 0.075), (-28 + _SF.uniform(-4, 4), 0.84, 0.09),
              (-9 + _SF.uniform(-3, 3), 0.98, 0.1), (11 + _SF.uniform(-3, 3), 0.9, 0.095),
              (30 + _SF.uniform(-4, 4), 0.76, 0.085), (50 + _SF.uniform(-5, 5), 0.58, 0.07),
              (-62, 0.4, 0.06), (66, 0.42, 0.06)]


def paint_spike_fan(a, b):
    """Floor-burst crystal-spike fan (파쇄 bursts, missile / column impacts; face kind, pivot at the floor): faceted
    crystals #FBEEC8 / #EDCBA1 / #D2AB8C with white ridges and a gold base glow #FDE8A2 (v3 §4 'Floor burst
    crystals', v4 §5 'Floor impact shards')."""
    if b < -0.02 or b > 1:
        return CLEAR
    best = None
    for deg, ln, w0 in FAN_SPIKES:
        t = math.radians(deg)
        ux, uy = math.sin(t), math.cos(t)
        along = a * ux + (b + 0.02) * uy
        if along <= 0 or along >= ln:
            continue
        perp = a * uy - (b + 0.02) * ux
        hw = w0 * (1 - along / ln) ** 0.9
        if abs(perp) < hw:
            q = perp / hw
            if best is None or along < best[0]:
                best = (along, q, along / ln)
    if best:
        _al, q, f = best
        if abs(q) > 0.86:
            return hexc('#7A5A40') + (1.0,)
        if abs(q) < 0.08:
            return mix('#FFFFFF', '#FBEEC8', f * 0.5) + (1.0,)
        col = ramp(CRYSTAL_LIT, 1 - f * 0.6) if q < 0 else ramp(CRYSTAL_SHADE, 0.3 + 0.7 * (1 - f))
        return col + (1.0,)
    g = math.exp(-((a / 0.42) ** 2 + (b / 0.13) ** 2))
    return hexc('#FDE8A2') + (clamp01(0.8 * g),) if g > 0.03 else CLEAR


def _shard(a, b, lit, shade, ridge, edge, alpha=1.0):
    t = (b + 0.5)
    if t <= 0 or t >= 1:
        return CLEAR
    wide = 0.36
    half = 0.24 * (t / wide if t < wide else (1 - t) / (1 - wide)) ** 0.9
    m = half - abs(a)
    if m <= 0:
        return CLEAR
    if m < 0.032:
        return hexc(edge) + (alpha,)
    if abs(a) < 0.018:
        return hexc(ridge) + (alpha,)
    col = ramp(lit, t) if a < 0 else ramp(shade, t)
    return col + (alpha,)


GSH_LIT = rmp((0, '#E9B685'), (0.5, '#FDE8A2'), (1, '#FFF6D8'))
GSH_SHADE = rmp((0, '#9A7454'), (0.6, '#BE9176'), (1, '#E9B685'))


def paint_gold_shard(a, b):
    """Gold crystal shard (slam / floor-hit / blast bursts): lit facet #FDE8A2, shadow facet #BE9176 / #E9B685,
    white ridge, dark-gold edge #7C5C2E (v1 §3 A 'gold crystal-shard burst', v4 §5)."""
    return _shard(a, b, GSH_LIT, GSH_SHADE, '#FFFFFF', '#7C5C2E')


GL_LIT = rmp((0, '#F4EDE0'), (0.6, '#FFFAF9'), (1, '#FFFFFF'))
GL_SHADE = rmp((0, '#C9B48A'), (0.5, '#D9C9A8'), (1, '#E8DFCC'))


def paint_glass_shard(a, b):
    """Bubble glass shard (the break): white-gold #FFFAF9 / #F4EDE0 with #D9C9A8 / #E8DFCC facets and a gold edge
    #B89A55, translucent (v2 §7 'Release bubble')."""
    return _shard(a, b, GL_LIT, GL_SHADE, '#FFFFFF', '#B89A55', 0.82)


# ----------------------------------------------------------------------------- the gravity wave band
_WB = random.Random(355)
WAVE_ROCKS = [(-0.42 + 0.84 * (k + _WB.uniform(0.2, 0.8)) / 8, _WB.uniform(0.2, 0.62), _WB.uniform(0.1, 0.17),
               _WB.uniform(0, 3), rock_poly(_WB, 6, 0.4)) for k in range(8)]
WALL_ROCKS = [(-0.4 + 0.8 * (k + _WB.uniform(0.2, 0.8)) / 5, _WB.uniform(0.2, 0.6), _WB.uniform(0.12, 0.2),
               _WB.uniform(0, 3), rock_poly(_WB, 5, 0.4)) for k in range(5)]


def _rocks(a, y, rocks, sx=1.0):
    for x0, y0, s, rot, poly in rocks:
        dx, dy = (a - x0) / (s * sx), (y - y0) / s
        if abs(dx) > 1.2 or abs(dy) > 1.2:
            continue
        c, sn = math.cos(rot), math.sin(rot)
        ins, m = in_rock(dx * c + dy * sn, -dx * sn + dy * c, poly)
        if ins:
            top = dy * 0.8 - dx * 0.4 > 0.05
            col = hexc('#D6A87E') if top else hexc('#AF846E') if dx > 0 else hexc('#CD9570')
            if m < 0.16:
                col = mix(col, '#3E2A1E', 0.6)
            return col
    return None


def paint_wave_band(a, v):
    """Gravity-wave band segment (「인력 충격파」, the expanding gold-fire ring; band kind). v > 0: the flat strip
    (b = v - 1: 0 = the front, -1 = the inner edge, 2.5 b deep in use): a bright front #FDFBD1 / #FDF3AA, fire
    #FBE483 / #F2BB68, the burning band #E4A568 / #D29253 fading inward, tumbling rocks #D6A87E / #CD9570 / #AF846E.
    v < 0: the flame wall standing on the front edge (y = v + 1, 0 = the floor): gold-white roots, orange tips
    (v2 §3 B1 'filled burning disc with tumbling rock chunks', 'burning band 2-3 m wide', §7). Both parts fade at the
    segment ends so neighbours overlap."""
    end = 1 - smooth(0.38, 0.5, abs(a))
    if end <= 0:
        return CLEAR
    if v >= 0:
        u = 1 - v                                     # 0 front .. 1 inner edge
        lick = 0.05 + 0.07 * fbm(a * 9 + 3, 2.1, 3)
        if u < lick * 0.35:
            return CLEAR
        rk = _rocks(a, u, WAVE_ROCKS, 0.42)
        if rk is not None and u > 0.12:
            return rk + (clamp01(end * 1.2),)
        n = fbm(a * 5 + 1, u * 4 + 1, 3)
        tongue = fbm(a * 26 + 4, u * 2.2, 3)                # flame tongues streaming outward (along u)
        t = clamp01((u - lick * 0.35) / 0.95 + (n - 0.5) * 0.2 - (tongue - 0.5) * 0.35)
        col = ramp(WAVE_FIRE, t)
        col = mix(col, '#FDF3AA', 0.35 * smooth(0.6, 0.85, tongue) * (1 - t))
        alpha = (1 - smooth(0.6, 1.0, u)) * (0.78 + 0.22 * n) * (0.75 + 0.25 * smooth(0.3, 0.7, tongue))
        if u < 0.12:
            alpha = max(alpha, 0.95)
        return col + (clamp01(alpha * end),)
    y = v + 1                                         # 0 floor .. 1 top of the wall
    rk = _rocks(a, y, WALL_ROCKS, 0.42)
    if rk is not None and y < 0.75:
        return rk + (clamp01(end),)
    n = fbm(a * 7 + 5, y * 2.2, 3)
    h = 0.32 + 0.55 * fbm(a * 9 + 11, 0.7, 3) + 0.1 * math.sin(a * 23)
    if y > h:
        return CLEAR
    f = y / h
    col = ramp(rmp((0, '#FFFFF0'), (0.1, '#FDF3AA'), (0.28, '#FBE483'), (0.5, '#F2BB68'), (0.72, '#E4A568'),
                   (0.88, '#D29253'), (1, '#B86A3A')), f + (n - 0.5) * 0.15)
    alpha = (0.95 - 0.55 * f ** 1.5) * (0.75 + 0.25 * n)
    return col + (clamp01(alpha * end),)


# ----------------------------------------------------------------------------- field: violet, warp, bubble
_OC = random.Random(9)
OUSIA_ZIGS = make_lines([jag(_OC, _OC.uniform(-0.25, 0.25), 0.0, _OC.uniform(-0.25, 0.25), -1.0, 9, 0.12)
                         for _ in range(3)])


def paint_ousia_col(a, b):
    """Violet Ousia column (field form, under the core; cross kind hanging along -b): pale core #E6DDF6 / #CCB7E2,
    body #957FDF, edge #543CAC, crackling zigzags #969CFE (v1 §5 'Warp / Ousia', v3 §4 'Violet crackle', v4 §5)."""
    if b > 0 or b < -1:
        return CLEAR
    core = math.exp(-(a / 0.13) ** 2)
    body = math.exp(-(a / 0.33) ** 2)
    n = fbm(a * 5 + 3, b * 4, 3)
    d = lines_dist(a, b, OUSIA_ZIGS)
    ends = smooth(0.0, 0.06, -b) * (1 - smooth(0.85, 1.0, -b))
    if d < 0.018:
        return mix('#E6DDF6', '#969CFE', d / 0.018) + (clamp01(0.95 * ends + 0.05),)
    i = max(core, 0.72 * body * (0.55 + 0.45 * n))
    col = ramp(VIOLET, 0.3 + 0.7 * i)
    col = mix(col, '#969CFE', 0.4 * math.exp(-(d / 0.05) ** 2))
    alpha = (0.22 + 0.6 * body * (0.6 + 0.4 * n) + 0.18 * core) * ends
    return col + (clamp01(alpha),) if alpha > 0.02 else CLEAR


_GL = random.Random(651)
GLITCH_MAIN = jag(_GL, 0.0, -0.5, 0.02, 0.5, 8, 0.11)
GLITCH_LINES = make_lines([GLITCH_MAIN, jag(_GL, *GLITCH_MAIN[3], 0.17, 0.12, 3, 0.2),
                           jag(_GL, *GLITCH_MAIN[6], -0.16, 0.38, 3, 0.2)])
GLITCH_BLOCKS = [(_GL.uniform(-0.2, 0.2), _GL.uniform(-0.45, 0.45), _GL.uniform(0.03, 0.08), _GL.uniform(0.012, 0.03))
                 for _ in range(7)]


def paint_glitch(a, b):
    """Violet glitch streak (warp-out, field idle): a jagged lightning crack, core #F0ECFF / #969CFE, glow #6C64E3,
    with offset digital 'glitch' blocks #4430CA / #CCB7E2 (v1 §3 F 'violet glitch streaks', §5)."""
    for k, (x, y, w, h) in enumerate(GLITCH_BLOCKS):
        if abs(a - x) < w and abs(b - y) < h:
            return hexc('#4430CA' if k % 2 else '#CCB7E2') + (0.85,)
    d = lines_dist(a, b, GLITCH_LINES)
    if d < 0.014:
        return hexc('#F0ECFF') + (1.0,)
    if d < 0.032:
        return mix('#969CFE', '#6C64E3', (d - 0.014) / 0.018) + (1.0,)
    g = 0.6 * math.exp(-(d / 0.06) ** 2)
    return hexc('#6C64E3') + (g,) if g > 0.02 else CLEAR


def paint_warp_pillar(a, b):
    """White-cyan warp pillar (warp-out / warp-in flash; face kind, pivot at the floor, 1.5 blocks tall at scale 1):
    core #F7FCFD, body #DFF6FB, edge #C2E1F5, wider and brighter at the foot (v1 §3 F, §5 'warp pillar')."""
    if b < 0 or b > 1.5:
        return CLEAR
    x, y = a / 0.25, b / 1.5
    hw = 0.45 + 0.55 * math.exp(-y / 0.1)
    core = math.exp(-(x / (0.3 * hw)) ** 2)
    body = math.exp(-(x / (0.75 * hw)) ** 2)
    i = max(core, 0.8 * body)
    alpha = max(i, 0.35 * math.exp(-(x / hw) ** 2)) * (1 - smooth(0.72, 1.0, y))
    col = ramp(rmp((0, '#6FAAD8'), (0.3, '#9FCBEA'), (0.55, '#C2E1F5'), (0.8, '#DFF6FB'), (0.92, '#F7FCFD'), (1, '#FFFFFF')), i)
    return col + (clamp01(alpha * 1.15),) if alpha > 0.02 else CLEAR


def paint_warp_bloom(a, b):
    """White-cyan warp bloom (warp-in flash at the arena centre): a radial bloom with six soft rays (v1 §5)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    rays = (0.5 + 0.5 * math.cos(6 * th)) ** 6 * (1 - r) ** 1.5
    i = max(math.exp(-(r / 0.28) ** 2), 0.65 * rays, 0.35 * (1 - r) ** 2)
    return ramp(WARP, i) + (clamp01(i * 1.15),) if i > 0.02 else CLEAR


def _crack_set(seed, impacts, rays, ln):
    rnd = random.Random(seed)
    out = []
    for _ in range(impacts):
        t = rnd.uniform(0, 2 * math.pi)
        r0 = rnd.uniform(0.05, 0.62)
        cx, cy = r0 * math.cos(t), r0 * math.sin(t)
        for k in range(rays):
            th = 2 * math.pi * k / rays + rnd.uniform(-0.35, 0.35)
            L = rnd.uniform(*ln)
            ex, ey = cx + L * math.cos(th), cy + L * math.sin(th)
            er = math.hypot(ex, ey)
            if er > 0.86:
                ex, ey = ex * 0.86 / er, ey * 0.86 / er
            out.append(jag(rnd, cx, cy, ex, ey, 4, 0.14))
    return out


BUBBLE_CRACKS = [[], _crack_set(1, 1, 4, (0.18, 0.32))]
BUBBLE_CRACKS.append(BUBBLE_CRACKS[1] + _crack_set(2, 2, 5, (0.2, 0.4)))
BUBBLE_CRACKS.append(BUBBLE_CRACKS[2] + _crack_set(3, 4, 5, (0.25, 0.55)) + _crack_set(4, 2, 3, (0.5, 0.8)))
BUBBLE_CRACKS = [make_lines(c) for c in BUBBLE_CRACKS]


def make_bubble(stage):
    def paint(a, b):
        r = math.hypot(a, b)
        R = 0.9
        if r > 1:
            return CLEAR
        if r > R:
            g = 0.5 * (1 - (r - R) / (1 - R)) ** 2
            return hexc('#E8DFCC') + (g,)
        q = r / R
        if stage:
            d = lines_dist(a, b, BUBBLE_CRACKS[stage])
            if d < 0.011:
                return WHITE + (0.98,)
            if d < 0.024:
                return hexc('#8A7030') + (0.75,)
        else:
            d = 9.0
        limb = smooth(0.5, 1.0, q)
        col = mix('#FFFAF9', '#E8DFCC', limb * 0.85)
        rim = math.exp(-((q - 0.965) / 0.022) ** 2)
        spec = math.exp(-(((a + 0.34) / 0.16) ** 2 + ((b - 0.38) / 0.1) ** 2))
        glow = (0.35 + 0.15 * stage) * math.exp(-(d / 0.05) ** 2) if stage else 0.0
        col = mix(col, WHITE, max(rim, spec, glow))
        col = mix(col, '#F4D98A', 0.25 * glow)
        alpha = 0.14 + 0.5 * limb ** 2 + 0.35 * rim + 0.6 * spec + glow + 0.04 * stage
        return col + (clamp01(alpha),)
    paint.__doc__ = (f'Core bubble, crack stage {stage} (break meter 0-4 / 5-9 / 10-14 / 15-19 hits): a translucent '
                     'white-gold shell #FFFAF9 -> #E8DFCC with a bright limb and highlight' +
                     (', white cracks with dark-gold edges' if stage else ', no cracks') + ' (v2 §3 A3, §7).')
    return paint


_CR = random.Random(1212)
CRACK_RING_BR = make_lines([jag(_CR, (0.9 + _CR.uniform(-0.02, 0.02)) * math.cos(t), (0.9 + _CR.uniform(-0.02, 0.02)) * math.sin(t),
                                (0.9 + s * _CR.uniform(0.07, 0.15)) * math.cos(t + _CR.uniform(-0.06, 0.06)),
                                (0.9 + s * _CR.uniform(0.07, 0.15)) * math.sin(t + _CR.uniform(-0.06, 0.06)), 3, 0.25)
                            for t, s in ((2 * math.pi * k / 22 + _CR.uniform(-0.1, 0.1), 1 if k % 2 else -1)
                                         for k in range(22))])


def paint_crack_ring(a, b):
    """Gold crack ring (지면 충격 blast rim, the break's floor ring; unit radius): a jagged dark crack #2A1A10 with
    glowing edges #FCFDDD / #FBEE9E, short branch cracks and a gold glow #F6DD8E (v4 §3 G 'jagged crack ring at the
    rim glows gold', §5)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    rr = 0.9 + 0.018 * math.sin(th * 17 + 1) + 0.022 * (fbm(th * 2.5 + 8, 0.5, 3) - 0.5) * 2
    d = abs(r - rr)
    if r > 0.7:
        d = min(d, lines_dist(a, b, CRACK_RING_BR))
    if d < 0.006:
        return hexc('#2A1A10') + (1.0,)
    if d < 0.02:
        return mix('#FCFDDD', '#FBEE9E', (d - 0.006) / 0.014) + (1.0,)
    g = 0.55 * math.exp(-(d / 0.04) ** 2)
    return hexc('#F6DD8E') + (g,) if g > 0.02 else CLEAR


_CG = random.Random(7)
GLINT_CRACKS = make_lines([jag(_CG, 0, 0, L * math.cos(t), L * math.sin(t), 3, 0.07)
                           for t, L in ((2 * math.pi * k / 6 + _CG.uniform(-0.3, 0.3), _CG.uniform(0.45, 0.85))
                                        for k in range(6))])


def paint_crack_glint(a, b):
    """Per-hit crack glint on the core bubble (each meter count): a small star of fresh cracks (dark-gold core,
    white-gold edges #FBEE9E) around a bright glint (v2 §5 'small gold crack flash on a translucent bubble')."""
    r = math.hypot(a, b)
    s = max(star4(a, b, 0.6, 0.05), math.exp(-(r / 0.1) ** 2))
    if s > 0.35:
        return mix('#FBEE9E', WHITE, s) + (1.0,)
    d = lines_dist(a, b, GLINT_CRACKS)
    if d < 0.016:
        return hexc('#6A5020') + (1.0,)
    if d < 0.042:
        return mix('#FFFFFF', '#FBEE9E', (d - 0.016) / 0.026) + (1.0,)
    g = max(0.4 * math.exp(-(d / 0.06) ** 2), 0.5 * s)
    return hexc('#FBEE9E') + (g,) if g > 0.02 else CLEAR


# ----------------------------------------------------------------------------- sparks, arcs, flames
def paint_spark(a, b):
    """Gold spark star (charges, tip flares, impacts): core #FEFBDC, rays #F5E0A0 -> #E4BC6C, faint diagonals (v1 §3 M
    tip flares #FEFBDC / #F5E0A0 / #E4BC6C, v4 §5 sparks)."""
    r = math.hypot(a, b)
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(star4(a, b, 0.97, 0.075), 0.5 * star4(d1, d2, 0.5, 0.045), math.exp(-(r / 0.13) ** 2))
    halo = 0.3 * math.exp(-(r / 0.4) ** 2)
    col = ramp(rmp((0, '#C99A4E'), (0.3, '#E4BC6C'), (0.6, '#F5E0A0'), (0.85, '#FEFBDC'), (1, '#FFFFFF')),
               max(i, halo))
    return col + (clamp01(max(i * 1.3, halo)),)


_AR = random.Random(321)
ARC_MAIN = jag(_AR, -0.48, 0.0, 0.48, 0.02, 10, 0.09)
ARC_LINES = make_lines([ARC_MAIN, jag(_AR, *ARC_MAIN[3], -0.08, 0.2, 3, 0.25), jag(_AR, *ARC_MAIN[7], 0.3, -0.19, 3, 0.25)])


def paint_arc(a, b):
    """Electric gold arc (tip flares, core charge, up-beam crackle): a jagged branching bolt, core #FEFBDC, glow
    #E4BC6C (v1 §3 M 'electric gold arcs crawling over the ring', v4 §3 G)."""
    d = lines_dist(a, b, ARC_LINES)
    if d < 0.011:
        return WHITE + (1.0,)
    if d < 0.024:
        return mix('#FEFBDC', '#F5E0A0', (d - 0.011) / 0.013) + (1.0,)
    g = 0.55 * math.exp(-(d / 0.045) ** 2)
    return hexc('#E4BC6C') + (g,) if g > 0.02 else CLEAR


def paint_flame(a, b):
    """Gold flame tongue (vents, missile launches, flame band licks; pivot at its root): white-gold core #FEF5AD /
    #FADE8E, body #F1BF71, fringe #DE864D / #C36439 (v3 §4 'Flame band')."""
    if b <= 0 or b >= 1:
        return CLEAR
    x0 = 0.05 * math.sin(b * 6 + 0.5) * b
    hw = 0.23 * (1 - b) ** 0.7 * (0.55 + 0.45 * math.sin(math.pi * min(1.0, b * 2.4 + 0.25)))
    n = fbm(a * 12 + 1, b * 4, 3)
    hw *= 0.85 + 0.3 * n
    d = abs(a - x0)
    if d > hw:
        return CLEAR
    u = d / hw
    col = ramp(FLAME_G, clamp01(1.0 - u * 0.7 - b * 0.42 + (n - 0.5) * 0.2))
    alpha = (1 - 0.35 * u) * (1 - smooth(0.78, 1.0, b))
    return col + (clamp01(alpha),)


# ----------------------------------------------------------------------------- slab
def paint_slab(a, b):
    """Glowing floor slab (파쇄 lifted / thrown slabs; one texture on every face of the box): mauve-tan stone
    #9E8295 / #C59B91 / #B99077 with crack lines and a glowing rim #FDF957 / #FDEE89 / #FBD377 (v3 §4 'Slabs')."""
    edge = 1 - max(abs(a), abs(b))
    n = fbm(a * 2.6 + 1, b * 2.6 + 1, 3)
    if edge < 0.07:
        return mix('#FDF957', '#FDEE89', edge / 0.07) + (1.0,)
    if edge < 0.15:
        return mix('#FBD377', '#C59B91', (edge - 0.07) / 0.08) + (1.0,)
    col = mix('#9E8295', '#C59B91', n)
    col = mix(col, '#B99077', smooth(0.62, 0.75, fbm(a * 4 + 9, b * 4 + 2, 2)))
    if abs(fbm(a * 2 + 5, b * 2 + 5, 2) - 0.5) < 0.012 and fbm(a * 5, b * 5, 1) > 0.45:
        col = mix(col, '#5E4A55', 0.75)
    return col + (1.0,)


# ----------------------------------------------------------------------------- neutral (copies of the butterfly kit)
def paint_glow(a, b):
    """Neutral soft glow disc (flashes, ground glow, core glow); tint it."""
    r = math.hypot(a, b)
    if r >= 1:
        return CLEAR
    v = 0.9 + 0.1 * (1 - r)
    return (v, v, v, 0.95 * (1 - r) ** 1.4)


def paint_glint(a, b):
    """Neutral white 4-point glint (sparkles; tint gold, cyan or violet)."""
    r = math.hypot(a, b)
    i = max(star4(a, b, 0.98, 0.08), math.exp(-(r / 0.14) ** 2))
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(i, 0.45 * star4(d1, d2, 0.4, 0.05))
    halo = 0.22 * math.exp(-(r / 0.35) ** 2)
    v = 0.88 + 0.12 * i
    return (v, v, v, clamp01(max(i * 1.3, halo)))


def paint_mote(a, b):
    """Neutral mote: a soft dot with a faint cross glint (tint gold or violet)."""
    r = math.hypot(a, b)
    i = max(math.exp(-(r / 0.28) ** 2), 0.55 * star4(a, b, 0.95, 0.06))
    halo = 0.35 * math.exp(-(r / 0.6) ** 2)
    return (1.0, 1.0, 1.0, clamp01(max(i * 1.2, halo)))


def paint_streak(a, b):
    """Neutral long thin streak tapered at both ends (aim lines, speed lines, rising gold streaks)."""
    t = abs(a)
    if t >= 1:
        return CLEAR
    hw = (1 - t ** 2.2) + 0.02
    core = math.exp(-(b / (0.30 * hw)) ** 2)
    halo = 0.45 * math.exp(-(b / (0.9 * hw)) ** 2)
    i = max(core, halo) * (1 - t ** 8)
    v = 0.85 + 0.15 * core
    return (v, v, v, clamp01(i * 1.2))


def paint_ripple(a, b):
    """Near-white ripple / shock ring (floor rings, rim flares, lift-off pulses); tint it."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    i = math.exp(-((r - 0.88) / 0.022) ** 2) + 0.5 * math.exp(-((r - 0.88) / 0.07) ** 2)
    i = max(i, 0.45 * math.exp(-((r - 0.70) / 0.02) ** 2))
    for k, (rk, a0, ln) in enumerate(((0.80, 0.3, 1.3), (0.62, 2.4, 1.1), (0.94, 4.0, 1.5), (0.76, 5.2, 0.9))):
        d = (th - a0) % (2 * math.pi)
        if d < ln:
            f = math.sin(math.pi * d / ln)
            i = max(i, 0.7 * f * math.exp(-((r - rk) / 0.014) ** 2))
    v = 0.86 + 0.14 * min(1.0, i)
    return (v * 0.97, v, v * 0.95, clamp01(i))


# ----------------------------------------------------------------------------- telegraphs (neutral, tinted)
def _band(r, bands):
    for lo, hi, col, al in bands:
        if lo <= r < hi:
            return col + (al,)
    return CLEAR


RIM_BANDS = ((0.900, 0.915, DARK, 0.7), (0.915, 0.955, WHITE, 1.0), (0.955, 0.99, DARK, 0.92))
RIM_BANDS_S = ((0.66, 0.72, DARK, 0.7), (0.72, 0.86, WHITE, 1.0), (0.86, 0.99, DARK, 0.92))
RING_BANDS = ((0.950, 0.958, DARK, 0.6), (0.958, 0.978, WHITE, 1.0), (0.978, 0.995, DARK, 0.92))


def paint_t_rim(a, b):
    """Telegraph rim (unit radius): dark outline, saturated (tinted) band, thin dark inner line."""
    return _band(math.hypot(a, b), RIM_BANDS)


def paint_t_rim_s(a, b):
    """Thick telegraph rim for small discs (r <= 2.5)."""
    return _band(math.hypot(a, b), RIM_BANDS_S)


def paint_t_ring(a, b):
    """Thin travelling ring (the wave telegraph's front and band edge, r 2.5 .. 21): a narrow tinted band between
    dark lines, so the line stays about 0.4-0.6 b at the arena wall."""
    return _band(math.hypot(a, b), RING_BANDS)


def _fill(r):
    if r > 0.99:
        return CLEAR
    if r >= 0.955:
        return DARK + (0.7,)
    if r >= 0.88:
        return WHITE + (0.95,)
    if r >= 0.85:
        return DARK + (0.45,)
    return WHITE + (0.26 + 0.18 * (r / 0.85) ** 2,)


def paint_t_fill(a, b):
    """Progress fill (unit radius): translucent tinted disc with a bright leading edge and dark lines on both
    sides of it, so the edge reads on white marble and on the pink centre."""
    return _fill(math.hypot(a, b))


def make_t_sec(half):
    def rim(a, b):
        r = math.hypot(a, b)
        phi = math.degrees(math.atan2(a, b))
        best = CLEAR
        if abs(phi) <= half + 0.4:
            best = _band(r, RIM_BANDS)
        for s in (-1, 1):
            t = math.radians(half) * s
            ux, uy = math.sin(t), math.cos(t)
            along = a * ux + b * uy
            if 0.0 <= along <= 0.99:
                perp = abs(a * uy - b * ux)
                if perp < 0.019:
                    return WHITE + (1.0,)
                if perp < 0.042 and best[3] == 0:
                    best = DARK + (0.92,)
        if r < 0.035:
            return DARK + (1.0,)
        return best
    rim.__doc__ = f'Sector telegraph rim, half-angle {half} deg (unit radius, apex at the origin).'
    return rim


def make_t_secf(half):
    def fill(a, b):
        phi = math.degrees(math.atan2(a, b))
        if abs(phi) > half:
            return CLEAR
        return _fill(math.hypot(a, b))
    fill.__doc__ = f'Sector progress fill, half-angle {half} deg.'
    return fill


def paint_t_bar(a, b):
    """Lane rail / cap bar: tinted core with dark outlines along both long sides (stretched along b)."""
    return DARK + (0.92,) if abs(a) > 0.6 else WHITE + (1.0,)


def paint_t_lane(a, b):
    """Lane progress fill: translucent tinted strip with a bright leading edge at the far end (b = 1)."""
    if b >= 0.955:
        return WHITE + (0.95,)
    if b >= 0.925:
        return DARK + (0.45,)
    return WHITE + (0.26 + 0.12 * b,)


# ----------------------------------------------------------------------------- HUD glyphs (x right, y up, -1..1)
def glyph_badge(x, y):
    """역장 meter badge: a violet ring #8F6AC8 / #A572A6 around a gold core #FBD78E with an orbit band and a dark
    pupil, dark outline (v1 §5 field halo violet, v2 §7 core eye #FBD78E)."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    if r > 0.88:
        return hexc('#1C1028') + (1.0,)
    if r > 0.68:
        return mix('#B497E8', '#6E4FB0', (r - 0.68) / 0.2) + (1.0,)
    if r > 0.6:
        return hexc('#2A1A36') + (1.0,)
    if abs(y - 0.25 * x) < 0.07 and r > 0.4:
        return hexc('#C49A48') + (1.0,)
    if r < 0.44:
        if math.hypot(x + 0.05, y - 0.02) < 0.15:
            return hexc('#5A2A0C') + (1.0,)
        lit = clamp01(0.6 - 0.4 * x + 0.5 * y)
        return mix('#D9A548', '#FFF0B8', lit) + (1.0,)
    return mix('#3A2448', '#24142E', r) + (1.0,)


_BK = random.Random(5)
BREAK_LINES = make_lines([jag(_BK, 0.02, 0.0, L * math.cos(t), L * math.sin(t), 4, 0.18)
                          for t, L in ((2 * math.pi * k / 7 + _BK.uniform(-0.3, 0.3), _BK.uniform(0.5, 0.95))
                                       for k in range(7))])


def glyph_break(x, y):
    """역장 붕괴 big badge (title pop at the break): the badge with its gold core cracked open and white-gold
    cracks running through the violet ring."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    d = lines_dist(x, y, BREAK_LINES)
    if d < 0.03 and r < 0.9:
        return mix('#FFFFFF', '#FBEE9E', d / 0.03) + (1.0,)
    if d < 0.05 and r < 0.9:
        return hexc('#3A2408') + (1.0,)
    return glyph_badge(x, y)


def glyph_lowg(x, y):
    """Low-gravity icon: a violet disc #6C64E3 with a dark rim, a white double chevron pointing up and three floating
    pebbles (the field's 중력 감소 / jump-up state)."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    if r > 0.88:
        return hexc('#1A1240') + (1.0,)
    for cy in (0.05, 0.42):
        d = min(seg_dist(x, y, -0.42, cy - 0.32, 0.0, cy), seg_dist(x, y, 0.0, cy, 0.42, cy - 0.32))
        if d < 0.08:
            return mix('#FFFFFF', '#E6DDF6', d / 0.08) + (1.0,)
        if d < 0.12:
            return hexc('#2A1E70') + (1.0,)
    for px, py, s in ((-0.5, -0.45, 0.1), (0.48, -0.5, 0.08), (0.05, -0.62, 0.07)):
        if math.hypot(x - px, y - py) < s:
            return hexc('#D9CFE2') + (1.0,)
    return mix('#8775EE', '#4430CA', r / 0.88) + (1.0,)


# pixel glyphs (exact pixels, no supersampling): 5 x 7 digit masks, outlined into 7 x 9 textures
DIGITS = {
    '0': ('01110', '10001', '10011', '10101', '11001', '10001', '01110'),
    '1': ('00100', '01100', '00100', '00100', '00100', '00100', '01110'),
    '2': ('01110', '10001', '00001', '00010', '00100', '01000', '11111'),
    '3': ('11110', '00001', '00001', '01110', '00001', '00001', '11110'),
    '4': ('00010', '00110', '01010', '10010', '11111', '00010', '00010'),
    '5': ('11111', '10000', '11110', '00001', '00001', '10001', '01110'),
    '6': ('00110', '01000', '10000', '11110', '10001', '10001', '01110'),
    '7': ('11111', '00001', '00010', '00100', '01000', '01000', '01000'),
    '8': ('01110', '10001', '10001', '01110', '10001', '10001', '01110'),
    '9': ('01110', '10001', '10001', '01111', '00001', '00010', '01100'),
    '/': ('00001', '00010', '00010', '00100', '01000', '01000', '10000'),
}
PIX_GOLD_TOP, PIX_GOLD, PIX_GOLD_LOW, PIX_OUT = hexc('#FFF2C0'), hexc('#FBD78E'), hexc('#E2A84A'), hexc('#2A1A08')


def pixel_digit(ch):
    """7 x 9 RGBA rows of a gold digit (or '/') with a 1 px dark outline: the meter's 'N/20' style."""
    m = DIGITS[ch]
    w, h = 7, 9
    on = [[m[j - 1][i - 1] == '1' if 1 <= i <= 5 and 1 <= j <= 7 else False for i in range(w)] for j in range(h)]
    px = []
    for j in range(h):
        row = []
        for i in range(w):
            if on[j][i]:
                c = PIX_GOLD_TOP if j <= 2 else PIX_GOLD if j <= 5 else PIX_GOLD_LOW
                row.append(c + (1.0,))
            elif any(on[jj][ii] for jj in range(max(0, j - 1), min(h, j + 2)) for ii in range(max(0, i - 1), min(w, i + 2))):
                row.append(PIX_OUT + (1.0,))
            else:
                row.append(CLEAR)
        px.append(row)
    return w, h, px


def pixel_pip(state):
    """8 x 14 RGBA rows of a meter pip (a slanted gem): state 0 empty (dark violet outline, dim violet inside), 1 full
    (gold, light top edge), 2 just counted (white with a gold rim)."""
    w, h = 8, 14
    px = []
    for j in range(h):
        row = []
        for i in range(w):
            x, y = (i + 0.5) / w * 2 - 1, 1 - (j + 0.5) / h * 2
            sx = x - 0.18 * y
            m = 1 - max(abs(sx) / 0.78, abs(y) / 0.92)
            if m < 0:
                row.append(CLEAR)
                continue
            if m < 0.22:
                row.append((hexc('#1C1028') if state != 2 else hexc('#8A6A20')) + (1.0,))
                continue
            if state == 0:
                row.append(mix('#5C4A86', '#3A2C5C', 0.5 - 0.5 * y) + (0.85,))
            elif state == 1:
                row.append(mix('#E2A84A', '#FFF0B8', 0.5 + 0.5 * y) + (1.0,))
            else:
                row.append(mix('#FFF6D8', '#FFFFFF', 0.5 + 0.5 * y) + (1.0,))
        px.append(row)
    return w, h, px
