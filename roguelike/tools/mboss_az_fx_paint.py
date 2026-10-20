"""Painted sprites of the 야타용왕 (Azhdaha) fx kit (tools/build_mboss_az_fx.py). Stdlib only.

The chapter-1 boss is 야타용왕, the sealed rock-dragon king: Geo gold crystal blades and cracks, dust and rock slabs in
phase 1, then the absorbed elements (Pyro / Hydro legs in phase 2, Cryo / Electro back and tail in phase 3). Every hex
value below comes from the footage notes (scratchpad az/understand/v1-v9.md, the per-clip "FX palette" sections, quoted
in each painter's docstring).

Every painter takes card coordinates (a, b) inside its kind's painter box and returns straight-alpha (r, g, b, alpha)
floats. The conventions are the field generator kit's (tools/mboss_fg_fx_paint.py): +a is the card's local -x (the
right when seen from behind or from above), +b is up (face cards) or forward (flat cards); cross kinds paint +b along
their long axis; the band kind paints its flat strip in v > 0 and its wall in v < 0; the box kind paints one face texture
used on all six faces; the prism kind paints one wall texture used on its eight walls.

Neutral sprites (white or near white with a baked dark outline) are tinted per spawn by the item definitions'
minecraft:custom_model_data tint, which multiplies the texture colour: the telegraphs (every `el` palette and the
undodgeable red-amber) and the element-neutral fx (blades, cracks, dust, beams, vortex, crystals, the water sheet).

The shared helpers (noise, ramps, the telegraph rim / fill / ring / lane profiles, the neutral glow / glint / mote /
streak / ripple) are copies of the field generator painter's, so the kits can change apart.
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


CLEAR = (0.0, 0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)
DARK = (0.055, 0.035, 0.05)          # telegraph outline (stays dark under any tint)

# ----------------------------------------------------------------------------- noise and geometry
_R = random.Random(20261019)
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


def pnoise(x, y, period):
    """value noise that tiles with the given integer period (the water sheet's seamless tiles)"""
    ix, iy = math.floor(x), math.floor(y)
    fx, fy = x - ix, y - iy
    ux, uy = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy)

    def lat(i, j):
        return _lat(i % period, j % period)
    a, b = lat(ix, iy), lat(ix + 1, iy)
    c, d = lat(ix, iy + 1), lat(ix + 1, iy + 1)
    return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy


def pfbm(x, y, period, octaves=3):
    s, amp, f, tot = 0.0, 0.5, 1, 0.0
    for _ in range(octaves):
        s += amp * pnoise(x * f, y * f, period * f)
        tot += amp
        amp *= 0.5
        f *= 2
    return s / tot


def seg_dist(px, py, ax, ay, bx, by):
    vx, vy = bx - ax, by - ay
    t = clamp01(((px - ax) * vx + (py - ay) * vy) / (vx * vx + vy * vy + 1e-12))
    return math.hypot(px - ax - vx * t, py - ay - vy * t)


def poly_dist(px, py, pts):
    """distance to a polyline"""
    return min(seg_dist(px, py, ax, ay, bx, by) for (ax, ay), (bx, by) in zip(pts, pts[1:]))


def make_lines(polys):
    out = []
    for pts in polys:
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        out.append(((min(xs), min(ys), max(xs), max(ys)), pts))
    return out


def lines_dist(px, py, lines, pad=0.1):
    """distance to the nearest of several polylines (lines = make_lines(...))"""
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
    """4-point star intensity (0..1) with rays along the card axes."""
    def ray(u, v):
        f = 1 - abs(u) / length
        if f <= 0:
            return 0.0
        return f ** 1.4 * math.exp(-(v / (width * f + 0.012)) ** 2)
    return max(ray(a, b), ray(b, a))


def rock_poly(rnd, n, irr=0.35):
    """irregular convex-ish polygon around the origin, unit size: list of (angle, radius); the angles are evenly spaced
    with jitter so the rock always surrounds its centre"""
    angs = sorted((2 * math.pi * (k + rnd.uniform(-0.3, 0.3)) / n) % (2 * math.pi) for k in range(n))
    return [(t, 1.0 - irr * rnd.random()) for t in angs]


def in_rock(x, y, poly):
    """(inside?, edge margin 0..1) of a point in a rock_poly (straight facets between its vertices)"""
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


def glow_stroke(d, core, body, col_core, col_body, halo=0.0, outline=0.0, out_col=DARK, halo_col=None):
    """colour of a glowing stroke at distance d: white-hot core, coloured body, optional dark outline, soft halo"""
    if d < core:
        return mix(col_core, col_body, d / core * 0.4) + (1.0,)
    if d < body:
        return mix(col_core, col_body, 0.4 + 0.6 * (d - core) / (body - core)) + (1.0,)
    if outline and d < body + outline:
        return (out_col if isinstance(out_col, tuple) else hexc(out_col)) + (0.92,)
    if halo:
        g = 0.55 * math.exp(-((d - body) / halo) ** 2)
        if g > 0.02:
            hc = halo_col if halo_col is not None else col_body
            return (hc if isinstance(hc, tuple) else hexc(hc)) + (g,)
    return CLEAR


def ngon(n, r, rot=0.0):
    return [(r * math.sin(rot + 2 * math.pi * k / n), r * math.cos(rot + 2 * math.pi * k / n)) for k in range(n)]


# ----------------------------------------------------------------------------- neutral (copies of the fg kit, tint them)
def paint_glow(a, b):
    """Neutral soft glow disc (flashes, ground glow, rune glow); tint it."""
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
    """Neutral mote: a soft dot with a faint cross glint (embers, gold motes, frost glints)."""
    r = math.hypot(a, b)
    i = max(math.exp(-(r / 0.28) ** 2), 0.55 * star4(a, b, 0.95, 0.06))
    halo = 0.35 * math.exp(-(r / 0.6) ** 2)
    return (1.0, 1.0, 1.0, clamp01(max(i * 1.2, halo)))


def paint_streak(a, b):
    """Neutral long thin streak tapered at both ends (speed lines, wave streaks, ribbons, meteor trails)."""
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
    """Near-white ripple / shock ring (roar domes, absorb ring flash, recolour wave); tint it."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    i = math.exp(-((r - 0.88) / 0.022) ** 2) + 0.5 * math.exp(-((r - 0.88) / 0.07) ** 2)
    i = max(i, 0.45 * math.exp(-((r - 0.70) / 0.02) ** 2))
    for rk, a0, ln in ((0.80, 0.3, 1.3), (0.62, 2.4, 1.1), (0.94, 4.0, 1.5), (0.76, 5.2, 0.9)):
        d = (th - a0) % (2 * math.pi)
        if d < ln:
            f = math.sin(math.pi * d / ln)
            i = max(i, 0.7 * f * math.exp(-((r - rk) / 0.014) ** 2))
    v = 0.86 + 0.14 * min(1.0, i)
    return (v * 0.97, v, v * 0.95, clamp01(i))


def paint_spark(a, b):
    """Neutral spark star (impacts, Electro sparks, gold flashes); tint it."""
    r = math.hypot(a, b)
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(star4(a, b, 0.97, 0.075), 0.5 * star4(d1, d2, 0.5, 0.045), math.exp(-(r / 0.13) ** 2))
    halo = 0.3 * math.exp(-(r / 0.4) ** 2)
    v = 0.8 + 0.2 * clamp01(i)
    return (v, v, v, clamp01(max(i * 1.3, halo)))


def paint_beam(a, b):
    """Neutral light beam / column (cross kind, foot at b 0): white core, soft body, flared foot, fading top (light
    shafts, spark columns, bolt columns, the cure beam); tint it."""
    if b < 0 or b > 1:
        return CLEAR
    flare = 1 + 0.6 * math.exp(-(b / 0.06) ** 2)
    core = math.exp(-(a / (0.12 * flare)) ** 2)
    body = math.exp(-(a / (0.32 * flare)) ** 2)
    n = fbm(a * 6 + 2, b * 3, 2)
    fade = (1 - smooth(0.55, 1.0, b)) * smooth(0.0, 0.03, b)
    v = 0.82 + 0.18 * core
    return (v, v, v, clamp01((core * 0.95 + body * (0.35 + 0.25 * n)) * fade))


def paint_vortex(a, b):
    """Neutral absorb vortex swirl (flat, unit radius): three spiral arms that thin toward the centre, a bright inner
    ring (v4 A 'water vortex', v5 A Pyro swirl, v6 A Electro discharge, v7 C Cryo gather); tint it."""
    r = math.hypot(a, b)
    if r > 1 or r < 0.08:
        return CLEAR
    th = math.atan2(b, a)
    i = 0.0
    for k in range(3):
        ph = (th - 2.6 * math.log(r + 0.05) - k * 2 * math.pi / 3) % (2 * math.pi)
        d = min(ph, 2 * math.pi - ph)
        w = 0.25 + 0.4 * r
        i = max(i, math.exp(-(d / w) ** 2) * (1 - smooth(0.75, 1.0, r)))
    i = max(i, 0.8 * math.exp(-((r - 0.22) / 0.04) ** 2))
    v = 0.85 + 0.15 * i
    return (v, v, v, clamp01(i * (0.55 + 0.45 * fbm(a * 4, b * 4, 2))))


# ----------------------------------------------------------------------------- telegraphs (neutral, tinted)
def _band(r, bands):
    for lo, hi, col, al in bands:
        if lo <= r < hi:
            return col + (al,)
    return CLEAR


RIM_BANDS = ((0.900, 0.915, DARK, 0.7), (0.915, 0.955, WHITE, 1.0), (0.955, 0.99, DARK, 0.92))
RIM_BANDS_S = ((0.66, 0.72, DARK, 0.7), (0.72, 0.86, WHITE, 1.0), (0.86, 0.99, DARK, 0.92))
RING_BANDS = ((0.930, 0.942, DARK, 0.6), (0.942, 0.974, WHITE, 1.0), (0.974, 0.995, DARK, 0.92))


def paint_t_rim(a, b):
    """Telegraph rim (unit radius): dark outline, saturated (tinted) band, thin dark inner line."""
    return _band(math.hypot(a, b), RIM_BANDS)


def paint_t_rim_s(a, b):
    """Thick telegraph rim for small discs (r <= 2.5)."""
    return _band(math.hypot(a, b), RIM_BANDS_S)


def paint_t_ring(a, b):
    """Thin travelling ring (wave fronts and band edges, the meteor halo): a narrow tinted band between dark lines."""
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
    """Progress fill (unit radius): translucent tinted disc with a bright leading edge between dark lines."""
    return _fill(math.hypot(a, b))


def make_t_sf(half):
    """Sector-slice progress fill, half-angle `half` degrees, apex at the origin (no radial edge lines, so slices of a
    fan join without seams)."""
    def fill(a, b):
        phi = math.degrees(math.atan2(a, b))
        if abs(phi) > half + 0.3:
            return CLEAR
        return _fill(math.hypot(a, b))
    fill.__doc__ = f'Sector-slice progress fill ({2 * half:g} degrees wide, unit radius, apex at the origin).'
    return fill


def make_t_sa(half, edges=''):
    """Sector-slice rim: the outer arc band, plus radial edge lines on the left ('l', -a) and / or right ('r', +a)."""
    def rim(a, b):
        r = math.hypot(a, b)
        phi = math.degrees(math.atan2(a, b))
        best = CLEAR
        if abs(phi) <= half + 0.3:
            best = _band(r, RIM_BANDS)
        for side in edges:
            s = 1 if side == 'r' else -1
            t = math.radians(half) * s
            ux, uy = math.sin(t), math.cos(t)
            along = a * ux + b * uy
            if 0.0 <= along <= 0.99:
                perp = (a * uy - b * ux) * s            # > 0 outside the slice
                if -0.016 < perp < 0.004:
                    return WHITE + (1.0,)
                if -0.034 < perp < 0.02 and best[3] == 0:
                    best = DARK + (0.92,)
        return best
    rim.__doc__ = f'Sector-slice rim ({2 * half:g} degrees, unit radius), outer arc' + \
        (f' + radial edges {edges}' if edges else '') + '.'
    return rim


def make_t_band(rho, edge):
    """Annular slice fill (15 degrees, inner radius rho, outer 1): `edge` = the leading-edge profile of the progress
    fill (the outer band of an annular wedge), else a plain translucent band (the inner band)."""
    def band(a, b):
        r = math.hypot(a, b)
        phi = math.degrees(math.atan2(a, b))
        if abs(phi) > 7.8 or r < rho or r > 0.995:
            return CLEAR
        if edge:
            return _fill(r)
        return WHITE + (0.2,)
    band.__doc__ = (f'Annular 15-degree slice fill, radii {rho:g} .. 1, ' +
                    ('with the leading edge (outer band)' if edge else 'plain (inner band)') + '.')
    return band


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


def paint_t_frame(a, b):
    """Strip outline (field-pool strips): a thin tinted frame with a dark outer line, transparent inside."""
    m = min(0.5 - abs(a), b, 1 - b)
    if m < 0 or m > 0.05:
        return CLEAR
    if m < 0.012:
        return DARK + (0.9,)
    return WHITE + (1.0,)


# 回 mark: an outer square, an inner square and the short ticks of the kit's meander frame
HUI_OUT, HUI_IN = 0.62, 0.26


def _hui_dist(x, y, s=1.0):
    ax, ay = abs(x) / s, abs(y) / s
    d_out = abs(max(ax, ay) - HUI_OUT)
    d_in = abs(max(ax, ay) - HUI_IN)
    return min(d_out, d_in) * s


def paint_t_nd(a, b):
    """The undodgeable mark (plan rule 6): a 回 glyph inside a diamond, white core with a dark outline; tinted the
    shared red-amber #FF5A1E (every #hzNoDodge decal carries it at its centre, along lines every 4 b)."""
    dia = abs(abs(a) + abs(b) - 0.92)
    d = min(_hui_dist(a, b, 0.62), dia)
    if d < 0.045:
        return WHITE + (1.0,)
    if d < 0.085:
        return DARK + (0.95,)
    if abs(a) + abs(b) < 0.92:
        return WHITE + (0.22,)
    return CLEAR


def paint_t_ndj(a, b):
    """The undodgeable + jumpable mark: the 回 diamond (smaller, low) with a double jump chevron above it."""
    x, y = a / 0.72, (b + 0.3) / 0.72
    dia = abs(abs(x) + abs(y) - 0.92) * 0.72
    d = min(_hui_dist(x, y, 0.62) * 0.72, dia)
    for cy in (0.42, 0.72):
        d = min(d, seg_dist(a, b, -0.4, cy - 0.22, 0.0, cy), seg_dist(a, b, 0.0, cy, 0.4, cy - 0.22))
    if d < 0.045:
        return WHITE + (1.0,)
    if d < 0.085:
        return DARK + (0.95,)
    if abs(x) + abs(y) < 0.92:
        return WHITE + (0.22,)
    return CLEAR


def _double_lines(a, b, segs, gap=0.022, w=0.009):
    """distance-like value for doubled straight lines (the seal decals' twin strokes)"""
    best = 9.0
    for (x0, y0), (x1, y1) in segs:
        dx, dy = x1 - x0, y1 - y0
        ln = math.hypot(dx, dy)
        nx, ny = -dy / ln, dx / ln
        for s in (-1, 1):
            best = min(best, seg_dist(a, b, x0 + nx * gap * s, y0 + ny * gap * s, x1 + nx * gap * s, y1 + ny * gap * s))
    return best


def _seal_px(d, w=0.011, halo=0.035):
    if d < w:
        return WHITE + (1.0,)
    if d < w + 0.008:
        return DARK + (0.8,)
    g = 0.45 * math.exp(-((d - w) / halo) ** 2)
    return WHITE + (g,) if g > 0.03 else CLEAR


def _meander_cap(a, b, cx, cy, ang, s):
    """a small square hook (the meander caps at the star tips): distance to its strokes"""
    c, sn = math.cos(ang), math.sin(ang)
    x, y = ((a - cx) * c - (b - cy) * sn) / s, ((a - cx) * sn + (b - cy) * c) / s
    pts = [(-1, -1), (1, -1), (1, 1), (-0.4, 1), (-0.4, -0.2), (0.3, -0.2)]
    return poly_dist(x, y, pts) * s


# runes as stroke lists in -1..1 (x right, y up)
RUNES = {
    # 大巛: a broad cross with legs + three wavy verticals (the Cryo floor / brand rune)
    'cryo': [[(-0.95, 0.35), (-0.05, 0.35)], [(-0.5, 0.8), (-0.5, 0.35), (-0.85, -0.6)], [(-0.5, 0.35), (-0.15, -0.6)],
             [(0.15, 0.8), (0.28, 0.2), (0.15, -0.3), (0.28, -0.8)], [(0.45, 0.8), (0.58, 0.2), (0.45, -0.3), (0.58, -0.8)],
             [(0.75, 0.8), (0.88, 0.2), (0.75, -0.3), (0.88, -0.8)]],
    # the Electro square rune: a framed square spiral with a bolt stroke (v7 hexagram centre, v6 marker glyph)
    'electro': [[(-0.8, 0.8), (0.8, 0.8), (0.8, -0.8), (-0.8, -0.8), (-0.8, 0.45)], [(-0.45, 0.45), (0.45, 0.45),
                (0.45, -0.45), (-0.2, -0.45), (-0.2, 0.1)], [(-0.05, 0.25), (0.15, 0.0), (-0.05, -0.05), (0.15, -0.3)]],
    # )火( : the Pyro brand / seal rune
    'pyro': [[(-0.95, 0.75), (-0.7, 0.0), (-0.95, -0.75)], [(0.95, 0.75), (0.7, 0.0), (0.95, -0.75)],
             [(0.0, 0.85), (0.0, -0.1), (-0.45, -0.8)], [(0.0, -0.1), (0.45, -0.8)], [(-0.4, 0.45), (-0.25, 0.2)],
             [(0.4, 0.45), (0.25, 0.2)]],
    # ccc / ||| : the Hydro brand rune (three crescents over three bars)
    'hydro': [[(-0.45, 0.85), (-0.7, 0.62), (-0.45, 0.4)], [(0.05, 0.85), (-0.2, 0.62), (0.05, 0.4)],
              [(0.55, 0.85), (0.3, 0.62), (0.55, 0.4)], [(-0.55, 0.15), (-0.55, -0.85)], [(0.0, 0.15), (0.0, -0.85)],
              [(0.55, 0.15), (0.55, -0.85)]],
    # Geo: a diamond crystal with a 回 core (the Geo emblem)
    'geo': [[(0.0, 0.9), (0.62, 0.0), (0.0, -0.9), (-0.62, 0.0), (0.0, 0.9)], [(-0.22, 0.22), (0.22, 0.22),
            (0.22, -0.22), (-0.22, -0.22), (-0.22, 0.22)], [(0.0, 0.9), (0.0, 0.5)], [(0.0, -0.9), (0.0, -0.5)]],
    # 火 (Pyro sigil)
    'fire': [[(0.0, 0.9), (0.0, 0.0), (-0.65, -0.85)], [(0.0, 0.0), (0.65, -0.85)], [(-0.6, 0.55), (-0.35, 0.15)],
             [(0.6, 0.55), (0.35, 0.15)]],
    # 水 (Hydro sigil)
    'water': [[(0.0, 0.9), (0.0, -0.85), (-0.2, -0.7)], [(-0.75, 0.4), (-0.25, 0.4), (-0.7, -0.6)],
              [(0.7, 0.55), (0.2, 0.05)], [(0.2, 0.05), (0.75, -0.75)]],
    # ⚡ (Electro sigil)
    'bolt': [[(0.25, 0.95), (-0.4, 0.0), (0.15, 0.0), (-0.3, -0.95)]],
    # ❄ (Cryo sigil)
    'snow': [[(0.0, 0.92), (0.0, -0.92)], [(-0.8, 0.46), (0.8, -0.46)], [(-0.8, -0.46), (0.8, 0.46)],
             [(-0.2, 0.78), (0.0, 0.58), (0.2, 0.78)], [(-0.2, -0.78), (0.0, -0.58), (0.2, -0.78)],
             [(0.55, 0.62), (0.5, 0.3), (0.78, 0.17)], [(-0.55, -0.62), (-0.5, -0.3), (-0.78, -0.17)],
             [(-0.55, 0.62), (-0.5, 0.3), (-0.78, 0.17)], [(0.55, -0.62), (0.5, -0.3), (0.78, -0.17)]],
}
RUNE_LINES = {k: make_lines(v) for k, v in RUNES.items()}


def rune_dist(x, y, name, s=1.0, cx=0.0, cy=0.0):
    return lines_dist((x - cx) / s, (y - cy) / s, RUNE_LINES[name], 0.15) * s


HEPT = ngon(7, 0.93)
HEPT_SEGS = [(HEPT[k], HEPT[(k + 2) % 7]) for k in range(7)]


def paint_t_hept(a, b):
    """서리 습격 star (41): a {7/2} heptagram of twin white strokes, square meander hooks at the seven tips, the 大巛
    rune in the middle (v8 k_f0540: lines #BBE0F7 on #4A7697, glyph #C9F1FB); neutral, tinted by `el` (Cryo)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    d = _double_lines(a, b, HEPT_SEGS)
    for k, (x, y) in enumerate(HEPT):
        ang = -2 * math.pi * k / 7
        d = min(d, _meander_cap(a, b, x * 1.0, y * 1.0, ang, 0.045))
    d = min(d, rune_dist(a, b, 'cryo', 0.2))
    return _seal_px(d)


HEX = ngon(6, 0.94)
HEX_SEGS = [(HEX[k], HEX[(k + 2) % 6]) for k in range(6)]


def paint_t_hex(a, b):
    """천동만상 – 번개 가시 hexagram (46): two triangles of twin strokes, meander hooks at the tips, the square 번개
    rune in the middle (v7 k_f0612 / k_f0804: lines #EACDFC on #675AB1); neutral, tinted by `el` (Electro)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    d = _double_lines(a, b, HEX_SEGS, 0.026, 0.011)
    for k, (x, y) in enumerate(HEX):
        d = min(d, _meander_cap(a, b, x, y, -2 * math.pi * k / 6, 0.05))
    d = min(d, rune_dist(a, b, 'electro', 0.26))
    return _seal_px(d, 0.013)


OCT = ngon(8, 0.93)
OCT_SEGS = [(OCT[k], OCT[(k + 3) % 8]) for k in range(8)]


def paint_t_star(a, b):
    """천동만상 – 얼음 가시 star seal (45): a thin circle with an {8/3} star and the ❄ rune, white (v8 D 'star / hail field
    under the player', v9 A 'Cryo 大巛 white rune inside the white seal'); neutral, tinted by `el`."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    d = min(_double_lines(a, b, OCT_SEGS, 0.018), abs(r - 0.95), abs(r - 0.885))
    d = min(d, rune_dist(a, b, 'snow', 0.24))
    return _seal_px(d, 0.010)


SQ1 = ngon(4, 0.93, math.pi / 4)
SQ2 = ngon(4, 0.93)
SEAL8_SEGS = [(SQ1[k], SQ1[(k + 1) % 4]) for k in range(4)] + [(SQ2[k], SQ2[(k + 1) % 4]) for k in range(4)]


def paint_t_seal8(a, b):
    """운석 낙하 seal (32): two overlapping squares of twin strokes (the 8-point seal), an inner circle and the )火(
    runes (v5 k_f0500: seal lines #EA8128 / #E89A1C, core #F9E8E0); neutral, tinted by `el` (Pyro)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    d = min(_double_lines(a, b, SEAL8_SEGS, 0.024), abs(r - 0.55))
    d = min(d, rune_dist(a, b, 'pyro', 0.26))
    return _seal_px(d, 0.012)


def paint_t_mask(a, b):
    """벼락 습격 strike wash (42): one floor-wide violet light card (unit radius) - a soft translucent wash with faint
    crackle streaks and a brighter wall rim (v6 B2 'strike zones marked with purple light', fill #6736C3 / #885AD3);
    neutral, tinted Electro."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    n = fbm(a * 4 + 3, b * 4 + 3, 3)
    streak = smooth(0.6, 0.75, fbm(a * 7 + 1, b * 7 + 7, 2))     # low frequency: no texel-scale speckle at 18 b
    rim = math.exp(-((r - 0.975) / 0.025) ** 2)
    al = 0.2 + 0.05 * n + 0.08 * streak + 0.14 * smooth(0.55, 1.0, r) + 0.6 * rim
    v = 0.86 + 0.14 * max(streak, rim)
    return (v, v, v, clamp01(al))


def paint_t_safe(a, b):
    """벼락 습격 safe circle (42): a broad green ring with a dark outline and the safe glyph (a circle with an up stroke,
    the shield) in the middle; neutral, tinted the safe green."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if 0.86 <= r < 0.98:
        return (DARK + (0.85,)) if r >= 0.955 or r < 0.875 else WHITE + (1.0,)
    d = min(abs(r - 0.3), seg_dist(a, b, 0.0, -0.18, 0.0, 0.42), seg_dist(a, b, -0.16, 0.26, 0.0, 0.42),
            seg_dist(a, b, 0.16, 0.26, 0.0, 0.42))
    if d < 0.035:
        return WHITE + (1.0,)
    if d < 0.06:
        return DARK + (0.8,)
    return WHITE + (0.1,) if r < 0.86 else CLEAR


_CR = random.Random(81)
CRATER_ROCKS = [(_CR.uniform(0, 2 * math.pi), _CR.uniform(0.66, 0.98), _CR.uniform(0.05, 0.11), rock_poly(_CR, 6, 0.4))
                for _ in range(46)]


def paint_t_crater(a, b):
    """B3 crater at the floor cut (also the crater prop, UUID 0x81): a dark pit #1E1810 / #2D2215 with a churned rim of
    rubble #6B5948 / #4D3B2C / #372318 lit #BDA878, olive dust #7A6F59 (v3 §4.2 boulders, v6 §4.3 dust, v8 B3)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    for t, rr, s, poly in CRATER_ROCKS:
        x, y = a - rr * math.cos(t), b - rr * math.sin(t)
        if abs(x) < s * 1.1 and abs(y) < s * 1.1:
            ins, m = in_rock(x / s, y / s, poly)
            if ins:
                col = mix('#4D3B2C', '#6B5948', fbm(a * 9, b * 9, 2))
                if y * 0.7 - x * 0.5 > s * 0.2:
                    col = mix(col, '#BDA878', 0.45)
                if m < 0.18:
                    col = mix(col, '#211810', 0.7)
                return col + (1.0,)
    n = fbm(a * 5 + 2, b * 5 + 2, 3)
    if r < 0.6:
        col = mix('#120E09', '#2D2215', smooth(0.2, 0.6, r) + 0.2 * (n - 0.5))
        return col + (clamp01(0.95 - 0.1 * n),)
    col = mix('#57513E', '#7A6F59', n)
    return col + (clamp01((1 - smooth(0.82, 1.0, r)) * (0.85 + 0.15 * n)),)


_GC = [(2 * math.pi * k / 8 + math.pi / 8) for k in range(8)]


def paint_t_gcircle(a, b):
    """Intro seal floor glyph circle (decor): gold rings #B6A666 / #C5B577 with a meander band, eight bright 回 glyphs
    #EDE0A9 around it and a pale floor ring #F4E8CD (v1 §5.2 'Seal (intro)')."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    if abs(r - 0.97) < 0.02 or abs(r - 0.6) < 0.015:
        return hexc('#F4E8CD') + (0.95,)
    if 0.84 < r < 0.92:
        seg = (th * 24 / (2 * math.pi)) % 1
        u = (r - 0.84) / 0.08
        on = (seg < 0.15) or (seg > 0.85) or abs(u - 0.5) > 0.4 or (0.4 < seg < 0.6 and u > 0.3)
        return (hexc('#C5B577') + (0.9,)) if on else (hexc('#5A4B32') + (0.35,))
    for t in _GC:
        cx, cy = 0.72 * math.cos(t), 0.72 * math.sin(t)
        if abs(a - cx) < 0.09 and abs(b - cy) < 0.09:
            d = _hui_dist(a - cx, b - cy, 0.12)
            if d < 0.012:
                return hexc('#EDE0A9') + (1.0,)
    if r < 0.6:
        d = rune_dist(a, b, 'geo', 0.32)
        if d < 0.02:
            return hexc('#EDE0A9') + (0.95,)
        return hexc('#B6A666') + (0.12 + 0.1 * smooth(0.3, 0.6, r),)
    return hexc('#B6A666') + (0.18,)


def paint_t_wall(a, b):
    """Dust wall standing on a flank strip's outer rail (성동격서, lane_side; face kind, foot at b 0): cream-gold dust
    #9D8558 / #B79C62 rising and thinning (v3 §4.2 'Dust walls'); near-neutral, tinted by `el`."""
    if b < 0 or b > 1:
        return CLEAR
    n = fbm(a * 5 + 1, b * 3, 3)
    h = 0.55 + 0.4 * fbm(a * 3 + 7, 1.3, 2)
    if b > h:
        return CLEAR
    f = b / h
    v = 0.78 + 0.22 * (1 - f)
    return (v, v * 0.97, v * 0.9, clamp01((0.75 - 0.6 * f ** 1.3) * (0.6 + 0.4 * n)))


# ----------------------------------------------------------------------------- the field pool (lingering decals)
_FB = random.Random(33)
FIRE_SPECKS = [(_FB.uniform(-0.8, 0.8), _FB.uniform(-0.8, 0.8), _FB.uniform(0.02, 0.05)) for _ in range(40)]


def make_fld(el):
    """Lingering field disc (N6, unit radius) per element."""
    def fld(a, b):
        r = math.hypot(a, b)
        if r > 1:
            return CLEAR
        th = math.atan2(b, a)
        n = fbm(a * 4 + el, b * 4 - el, 3)
        if el == 1:
            # Pyro (33 화염 잠식 / meteor fields): scorched floor, embers, a flame ring (v9 #F47B09 / #F8CE0B / #F9F2AE)
            ring = math.exp(-((r - 0.88) / (0.07 + 0.04 * fbm(th * 3, 1, 2))) ** 2)
            for x, y, s in FIRE_SPECKS:
                if (a - x) ** 2 + (b - y) ** 2 < s * s and r < 0.85:
                    return mix('#F8CE0B', '#F9F2AE', 0.5) + (0.95,)
            lick = smooth(0.45, 0.8, fbm(th * 6 + 2, r * 6, 2))
            col = mix('#5A1A08', '#CC4410', 0.4 * n)
            col = mix(col, mix('#F47B09', '#F8CE0B', lick), ring)
            return col + (clamp01(0.35 + 0.2 * n + 0.55 * ring),)
        if el == 2:
            # Hydro pool: ripples #13BDDE / #1C74AC, foam rim #D4E6F3
            rip = 0.5 + 0.5 * math.sin(r * 26 + 3 * n)
            col = mix('#1C74AC', '#13BDDE', rip * 0.6 + 0.2 * n)
            rim = math.exp(-((r - 0.93) / 0.04) ** 2)
            return mix(col, '#D4E6F3', rim) + (clamp01(0.35 + 0.15 * rip + 0.5 * rim),)
        if el == 3:
            # Electro field: violet #6736C3 / #885AD3 with magenta crackle #D569E2 (v6 §4.3, v7 k_f1356)
            arc = abs(fbm(a * 7 + 3, b * 7 + 3, 3) - 0.5)
            col = mix('#4E22A6', '#885AD3', n)
            if arc < 0.025:
                col = mix('#FFFFFF', '#D569E2', arc / 0.025)
                return col + (0.95,)
            rim = math.exp(-((r - 0.93) / 0.04) ** 2)
            return mix(col, '#C18AEA', rim) + (clamp01(0.3 + 0.15 * n + 0.55 * rim),)
        if el == 4:
            # Cryo hail field: frost floor #C2EEFB with twin white circles and the 大巛 rune (v9 A, v8 D)
            d = min(abs(r - 0.95), abs(r - 0.88), rune_dist(a, b, 'cryo', 0.3))
            if d < 0.014:
                return hexc('#F2FCFF') + (1.0,)
            if d < 0.024:
                return hexc('#4A7697') + (0.7,)
            frost = smooth(0.55, 0.8, fbm(a * 9 + 5, b * 9 + 1, 3))
            col = mix('#8FC6E9', '#E4F6FC', 0.5 * n + 0.5 * frost)
            return col + (clamp01(0.28 + 0.4 * frost),)
        # Geo: amber wash with gold cracks
        crack = abs(fbm(a * 5 + 9, b * 5 + 9, 3) - 0.5)
        if crack < 0.018:
            return hexc('#FFE8A0') + (0.95,)
        rim = math.exp(-((r - 0.93) / 0.04) ** 2)
        col = mix('#8D6C3F', '#D27A0C', n)
        return mix(col, '#F0A93A', rim) + (clamp01(0.3 + 0.15 * n + 0.55 * rim),)
    fld.__doc__ = f'Lingering field disc, element {el} (unit radius).'
    return fld


def make_fst(el):
    """Lingering element strip (N6; flat, a -0.5..0.5 across, b 0..1 along): Electro crackle or Cryo frost."""
    def fst(a, b):
        if abs(a) > 0.5 or b < 0 or b > 1:
            return CLEAR
        edge = 0.5 - abs(a)
        n = fbm(a * 6 + el, b * 14, 3)
        if el == 3:
            arc = abs(fbm(a * 9 + 3, b * 26, 3) - 0.5)
            if arc < 0.03:
                return mix('#FFFFFF', '#D569E2', arc / 0.03) + (0.95,)
            col = mix('#4E22A6', '#885AD3', n)
            rim = math.exp(-(edge / 0.05) ** 2)
            return mix(col, '#C18AEA', rim) + (clamp01(0.3 + 0.15 * n + 0.6 * rim),)
        frost = smooth(0.55, 0.8, fbm(a * 12 + 5, b * 30, 3))
        if frost > 0.8 and fbm(a * 20, b * 50, 1) > 0.6:
            return hexc('#F2FCFF') + (0.95,)
        col = mix('#8FC6E9', '#E4F6FC', 0.5 * n + 0.5 * frost)
        rim = math.exp(-(edge / 0.05) ** 2)
        return mix(col, '#F2FCFF', rim) + (clamp01(0.3 + 0.35 * frost + 0.6 * rim),)
    fst.__doc__ = f'Lingering strip, element {el}.'
    return fst


# ----------------------------------------------------------------------------- cracks, blades, dust, rocks (Geo base)
_CK = random.Random(1201)
CRACK_RAYS = make_lines([jag(_CK, 0.0, 0.0, L * math.cos(t), L * math.sin(t), 7, 0.13)
                         for t, L in ((2 * math.pi * k / 11 + _CK.uniform(-0.2, 0.2), _CK.uniform(0.7, 0.98))
                                      for k in range(11))] +
                        [jag(_CK, 0.5 * math.cos(t), 0.5 * math.sin(t), 0.85 * math.cos(t + 0.5), 0.85 * math.sin(t + 0.5),
                             4, 0.15) for t in (0.4, 2.2, 3.9, 5.3)])


def paint_cracks(a, b):
    """Radial floor cracks (flat, unit radius): white-hot crack cores #FFF2C0 with a dark gap line, a soft glow
    (v2 §5.2 crack lines #E7C683 / #C7A463 with a hot-white centre; v3 stomp radial cracks); near-neutral, tinted
    gold / cyan / lava / frost / violet per element."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    d = lines_dist(a, b, CRACK_RAYS, 0.12)
    w = 0.022 * (1 - 0.6 * r)
    if d < w * 0.45:
        return WHITE + (1.0,)
    if d < w:
        return (0.92, 0.9, 0.86, 1.0)
    if d < w + 0.012:
        return DARK + (0.85,)
    g = 0.4 * math.exp(-((d - w) / 0.05) ** 2) * (1 - r)
    return (0.95, 0.93, 0.9, g) if g > 0.03 else CLEAR


_CF = random.Random(1202)
FAN_RAYS = make_lines([jag(_CF, 0.0, 0.0, L * math.sin(t), L * math.cos(t), 7, 0.12)
                       for t, L in ((math.radians(-32 + 64 * k / 6 + _CF.uniform(-4, 4)), _CF.uniform(0.7, 0.98))
                                    for k in range(7))] +
                      [jag(_CF, 0.4 * math.sin(t), 0.4 * math.cos(t), 0.75 * math.sin(t + 0.3), 0.75 * math.cos(t + 0.3), 3,
                           0.2) for t in (-0.35, 0.05, 0.4)])


def paint_crackfan(a, b):
    """갈라지는 봉인의 땅 crack fan (flat, apex at b 0, about ±32 degrees forward): jagged glowing crack lines spreading
    from the impact (v2 C 'crack fan r 6 m', crack lines #E7C683 / #C7A463, hot core #FFF2C0); tinted per element."""
    r = math.hypot(a, b)
    if r > 1 or b < -0.02:
        return CLEAR
    d = lines_dist(a, b, FAN_RAYS, 0.1)
    w = 0.03 * (1 - 0.55 * r)
    if d < w * 0.45:
        return WHITE + (1.0,)
    if d < w:
        return (0.92, 0.9, 0.86, 1.0)
    if d < w + 0.014:
        return DARK + (0.85,)
    g = 0.45 * math.exp(-((d - w) / 0.06) ** 2) * (1 - r * 0.8)
    return (0.95, 0.93, 0.9, g) if g > 0.03 else CLEAR


def paint_blade(a, b):
    """Translucent crystal blade (the Geo crown of 8-12 blades, Electro / Cryo crystal bursts, seal-prism glass): a
    tall faceted shard, white ridge, light / shade facets, dark edge (v1 §5.2 blades #E6DB82 / #D8B757 / #AF8947,
    v3 §4.2 hot #E5E3C4); near-neutral, tinted per element (gold #F0C860, ice, violet, white-gold)."""
    t = b + 0.5
    if t <= 0 or t >= 1:
        return CLEAR
    wide = 0.28
    half = 0.24 * (t / wide if t < wide else (1 - t) / (1 - wide)) ** 0.85
    m = half - abs(a)
    if m <= 0:
        return CLEAR
    if m < 0.03:
        return (0.42, 0.38, 0.34, 0.95)
    if abs(a) < 0.016:
        return WHITE + (0.95,)
    v = 0.98 - 0.15 * t if a < 0 else 0.7 + 0.15 * t
    return (v, v, v, 0.78 + 0.15 * (a < 0))


def paint_dust(a, b):
    """Dust puff (toon cloud): near-white lit top, grey-beige shade, ragged edge (v2 §5.2 dust #7C725A / #5C5745, v3
    dust walls #9D8558 / #B79C62); tinted khaki / gold / white foam / ash per element."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    edge = 0.7 + 0.25 * fbm(math.cos(th) * 1.5 + 5, math.sin(th) * 1.5 + 5, 3)
    if r > edge:
        return CLEAR
    u = r / edge
    n = fbm(a * 3.5 + 11, b * 3.5 + 11, 3)
    lit = clamp01(0.5 + 0.6 * b + 0.3 * (n - 0.5))
    v = 0.62 + 0.38 * lit
    return (v, v * 0.98, v * 0.94, clamp01((1 - u ** 1.8) * (0.62 + 0.3 * n)))


_BD = random.Random(77)
BOULDER_POLY = rock_poly(_BD, 7, 0.32)


def paint_boulder(a, b):
    """Thrown boulder / rubble chunk: dark rounded rock #6B5948 / #4D3B2C / #372318 with a lit edge #BDA878 and a thin
    gold vein (v3 §4.2 'Thrown boulders')."""
    ins, m = in_rock(a / 0.92, b / 0.92, BOULDER_POLY)
    if not ins:
        return CLEAR
    n = fbm(a * 6 + 2, b * 6 + 2, 2)
    lit = clamp01(0.5 + 0.55 * b - 0.35 * a)
    col = ramp(rmp((0, '#2A1A10'), (0.35, '#4D3B2C'), (0.7, '#6B5948'), (1, '#9C8A6A')), lit + 0.2 * (n - 0.5))
    if m < 0.1:
        col = mix(col, '#BDA878', 0.5) if lit > 0.6 else mix(col, '#1A120B', 0.6)
    if seg_dist(a, b, -0.4, -0.25, 0.1, 0.05) < 0.035:
        col = mix(col, '#E7C683', 0.7)
    return col + (1.0,)


def paint_slab(a, b):
    """Rock slab torn out of the floor (one texture on every face of the box): olive slab #555448 / #3A2E1D faces with
    darker cracks and a gold crack rim #E7C683 (v4 §5 'rock slabs #2D2215 / #3A2E1D / #555448', v2 crack gold)."""
    edge = 1 - max(abs(a), abs(b))
    n = fbm(a * 2.6 + 1, b * 2.6 + 1, 3)
    if edge < 0.06:
        return mix('#E7C683', '#FFF2C0', edge / 0.06) + (1.0,)
    if edge < 0.13:
        return mix('#C7A463', '#555448', (edge - 0.06) / 0.07) + (1.0,)
    col = mix('#3A2E1D', '#555448', n)
    if abs(fbm(a * 2 + 5, b * 2 + 5, 2) - 0.5) < 0.014:
        col = mix(col, '#1A140C', 0.8)
    return col + (1.0,)


def paint_mound(a, b):
    """Dust mound / dig plume (face kind, foot at b 0): an olive-khaki heap of dust #7A6F59 / #8B8164 / #82785E with a
    dark base and rock flecks (v6 §4.3 'Dust (tail sink / mound)')."""
    if b < 0 or b > 0.5:
        return CLEAR
    h = 0.48 * (1 - (a / 0.5) ** 2) ** 0.5 * (0.82 + 0.3 * fbm(a * 5 + 3, 0.5, 2)) if abs(a) < 0.5 else 0
    if b > h:
        return CLEAR
    n = fbm(a * 7 + 1, b * 7 + 3, 3)
    f = b / max(h, 1e-6)
    lit = clamp01(0.35 + 0.6 * f - 0.4 * a)
    col = ramp(rmp((0, '#2E2820'), (0.35, '#57513E'), (0.7, '#7A6F59'), (1, '#A39878')), lit + (n - 0.5) * 0.3)
    if n > 0.74:
        col = mix(col, '#2A2218', 0.65)
    edge = h - b
    return col + (clamp01(1.0 if edge > 0.03 else 0.6 + 10 * edge),)


def paint_cone(a, b):
    """Planted stone cone (꼬리찍기 spikes left for 60 t; face kind, foot at b 0): grey-cream stone #C9C2A8 / #A39C84
    with a darker base #5E584A and a lit edge (v3 §4.2 'planted grey-cream stone cones')."""
    if b < 0 or b > 1:
        return CLEAR
    hw = 0.36 * (1 - b) ** 0.95 + 0.004
    if abs(a) > hw:
        return CLEAR
    u = a / hw
    n = fbm(a * 9, b * 6, 2)
    col = mix('#A39C84', '#E2DCC4', clamp01(0.55 - 0.45 * u + 0.25 * (n - 0.5)))
    col = mix(col, '#5E584A', smooth(0.3, 0.0, b) * 0.7)
    if abs(u) > 0.88:
        col = mix(col, '#3B372E', 0.6)
    return col + (1.0,)


def paint_leaf(a, b):
    """Orange tail leaf (꼬리찍기 leaf burst; v3 §4.2 'orange leaf burst'): a pointed leaf #E8892A / #C8641A with a pale
    midrib."""
    x, y = a / 0.45, b / 0.9
    if abs(x) > (1 - y * y) ** 0.8 if abs(y) < 1 else True:
        return CLEAR
    col = mix('#C8641A', '#F0A040', 0.5 + 0.5 * y)
    if abs(x) < 0.08:
        col = mix(col, '#FBD58A', 0.6)
    return col + (1.0,)


def paint_gold_leaf(a, b):
    """Gold leaf (intro roar radial gold leaves, death gold motes): a gold leaf #F2B53A / #C8781E with a bright
    edge."""
    x, y = a / 0.45, b / 0.9
    if abs(y) >= 1 or abs(x) > (1 - y * y) ** 0.8:
        return CLEAR
    col = mix('#C8781E', '#FFE8A0', 0.5 + 0.5 * y - 0.3 * x)
    if abs(x) < 0.07:
        col = mix(col, '#FFF6D0', 0.7)
    return col + (1.0,)


# ----------------------------------------------------------------------------- Hydro
def paint_splash(a, b):
    """Hydro splash (face kind, foot at b 0): a crown of water jets and droplets, white foam core #E5EAF1 / #CEDEE3,
    blue body #4FB8FF / #13BDDE, shade #1C74AC (v4 §5 'Hydro splash / spray', v9 §5.5 water ring)."""
    if b < 0 or b > 1:
        return CLEAR
    best = 0.0
    for k in range(7):
        ang = math.radians(-50 + 100 * k / 6)
        ln = 0.75 + 0.22 * math.cos(k * 1.7)
        ux, uy = math.sin(ang), math.cos(ang)
        along = a * ux + b * uy
        if 0 < along < ln:
            perp = abs(a * uy - b * ux)
            w = 0.07 * (1 - along / ln) + 0.01
            best = max(best, clamp01(1 - perp / w) * (1 - (along / ln) ** 3))
    for k in range(9):
        x, y = -0.6 + 1.2 * ((k * 0.37) % 1), 0.45 + 0.5 * ((k * 0.61) % 1)
        if math.hypot(a - x, b - y) < 0.04:
            best = 1.0
    base = math.exp(-((a / 0.5) ** 2 + (b / 0.16) ** 2))
    i = max(best, base)
    if i < 0.05:
        return CLEAR
    col = mix('#1C74AC', '#4FB8FF', i)
    col = mix(col, '#E5EAF1', smooth(0.6, 1.0, i))
    return col + (clamp01(0.4 + 0.6 * i),)


def paint_geyser(a, b):
    """Hydro geyser column (갈라지는 봉인의 땅 Hydro, cross kind, foot at b 0): a churning water column, foam core
    #E5EDF1, body #71D5E2 / #4DB5CF, edges #1C74AC, a spray head (v4 C 'geyser', v5 k_f1176)."""
    if b < 0 or b > 1:
        return CLEAR
    head = 1 + 0.9 * smooth(0.7, 1.0, b)
    w = 0.28 * head * (0.85 + 0.3 * fbm(b * 9, 1, 2))
    if abs(a) > w:
        return CLEAR
    u = abs(a) / w
    n = fbm(a * 9 + 3, b * 7, 3)
    col = ramp(rmp((0, '#E5EDF1'), (0.35, '#9DDFE5'), (0.65, '#4DB5CF'), (1, '#1C74AC')), u * 0.8 + (n - 0.5) * 0.3)
    al = (1 - u ** 3) * (0.75 + 0.25 * n) * (1 - smooth(0.85, 1.0, b))
    return col + (clamp01(al),)


def paint_orb(a, b):
    """격류 범람 Hydro orb (31): a water sphere, core #79E3E5, mid #93DAE9, rim #82C1D6, highlight #D4E3EA, a swirl band
    and a faint outer glow (v4 §5 'Hydro orb', v9 orbs #82D8E8 / #60D0E3 / #AFE0EB)."""
    r = math.hypot(a, b)
    R = 0.82
    if r > 1:
        return CLEAR
    if r > R:
        g = 0.4 * (1 - (r - R) / (1 - R)) ** 2
        return hexc('#60D0E3') + (g,)
    q = r / R
    col = ramp(rmp((0, '#C8F4F6'), (0.35, '#79E3E5'), (0.7, '#60D0E3'), (0.92, '#82C1D6'), (1, '#395D7A')), q)
    sw = math.sin(math.atan2(b, a) * 3 + q * 7)
    col = mix(col, '#D4E3EA', 0.35 * smooth(0.6, 1.0, sw) * q)
    spec = math.exp(-(((a + 0.28) / 0.14) ** 2 + ((b - 0.32) / 0.1) ** 2))
    col = mix(col, '#FFFFFF', 0.75 * spec)
    return col + (0.9,)


def paint_water(a, b):
    """The arena's shallow-water sheet (14-b tiles at y 201.005; flat, seamless): a near-white ripple pattern with
    caustic lines at about 40 % alpha (v2 §2 / v4 §2 shallow water); tinted per element look (geo / hydro / pyro /
    cryo / electro)."""
    x, y = (a + 0.5) * 4, (b + 0.5) * 4
    n = pfbm(x, y, 4, 3)
    c = abs(pfbm(x * 2 + 0.5, y * 2 + 0.25, 8, 2) - 0.5)
    caustic = math.exp(-(c / 0.035) ** 2)
    v = 0.78 + 0.12 * n + 0.1 * caustic
    return (v, v, v, clamp01(0.32 + 0.1 * n + 0.22 * caustic))


# ----------------------------------------------------------------------------- Pyro
def paint_flame(a, b):
    """Pyro flame tongue (footfall flame splash, fire walls, meteor flames; pivot at its root): white-hot core
    #F9F2AE, body #F8CE0B / #F47B09, fringe #CC4410 (v9 §5.5 fire #F47B09 / #F8CE0B / #F9F2AE)."""
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
    col = ramp(rmp((0, '#AE2503'), (0.25, '#CC4410'), (0.5, '#F47B09'), (0.75, '#F8CE0B'), (0.92, '#F9F2AE'),
                   (1, '#FFFFF0')), clamp01(1.0 - u * 0.7 - b * 0.42 + (n - 0.5) * 0.2))
    alpha = (1 - 0.35 * u) * (1 - smooth(0.78, 1.0, b))
    return col + (clamp01(alpha),)


def paint_fire_dome(a, b):
    """Meteor impact fire dome (half dome, pivot at the base centre): white-hot core, orange body, red rim and flame
    licks (v5 M 'dome r 5-6 m', fire #F47B09 / #F8CE0B)."""
    if b < 0:
        return CLEAR
    r = math.hypot(a / 0.5, b / 0.5)
    th = math.atan2(b, a)
    edge = 0.85 + 0.15 * fbm(th * 4 + 2, 1, 2)
    if r > edge:
        return CLEAR
    q = r / edge
    n = fbm(a * 7, b * 7, 3)
    col = ramp(rmp((0, '#FFFFF0'), (0.3, '#F9F2AE'), (0.55, '#F8CE0B'), (0.8, '#F47B09'), (1, '#AE2503')), q + (n - 0.5) * 0.2)
    return col + (clamp01((0.95 - 0.5 * q ** 3) * (0.8 + 0.2 * n)),)


_LV = random.Random(55)
LAVA_POLY = rock_poly(_LV, 7, 0.3)


def paint_lava(a, b):
    """Molten rock (Pyro lumps, meteor bodies): dark crust #3A1206 split by glowing cracks #CC4410 / #F5C22F with a hot
    halo (v9 §5.5 molten rock #AE2503 / #CC4410 with #F5C22F edges)."""
    r = math.hypot(a, b)
    ins, m = in_rock(a / 0.78, b / 0.78, LAVA_POLY)
    if not ins:
        g = 0.5 * math.exp(-((r - 0.6) / 0.18) ** 2)
        return hexc('#F47B09') + (g,) if g > 0.03 else CLEAR
    n = fbm(a * 6 + 1, b * 6 + 1, 3)
    crack = abs(fbm(a * 4 + 3, b * 4 + 7, 2) - 0.5)
    if crack < 0.04:
        return mix('#FFF2B0', '#F5C22F', crack / 0.04) + (1.0,)
    if crack < 0.08:
        return mix('#CC4410', '#AE2503', (crack - 0.04) / 0.04) + (1.0,)
    col = mix('#1E0A04', '#5A1A08', n + 0.3 * b)
    if m < 0.12:
        col = mix(col, '#F47B09', 0.6)
    return col + (1.0,)


def paint_meteor(a, b):
    """운석 낙하 meteor (32; face kind, falling along -b): a molten rock head at the bottom with a flame trail streaming
    up (v5 k_f0520 / k_f0536, molten #AE2503 / #CC4410, flames #F47B09 / #F8CE0B)."""
    head = paint_lava(a / 0.55, (b + 0.5) / 0.55)
    if head[3] >= 0.9:
        return head
    if b < -0.5 or b > 1:
        return head
    t = (b + 0.2) / 1.2
    if t < 0:
        return head
    w = 0.42 * (1 - t) ** 0.8
    n = fbm(a * 8, b * 5, 3)
    if abs(a) > w * (0.8 + 0.3 * n):
        return head
    u = abs(a) / max(w, 1e-6)
    col = ramp(rmp((0, '#FFFFF0'), (0.3, '#F8CE0B'), (0.65, '#F47B09'), (1, '#AE2503')), u * 0.6 + t * 0.5)
    al = (1 - u ** 2) * (1 - t) ** 0.8 * (0.7 + 0.3 * n)
    return col + (clamp01(max(al, head[3])),)


def paint_smoke(a, b):
    """Smoke / steam puff (meteor trails, extinguished fire): grey #8A8478 to pale #D8D2C8, soft and ragged."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    edge = 0.72 + 0.22 * fbm(math.cos(th) * 1.6 + 3, math.sin(th) * 1.6 + 3, 3)
    if r > edge:
        return CLEAR
    u = r / edge
    n = fbm(a * 3 + 7, b * 3 + 7, 3)
    col = mix('#D8D2C8', '#8A8478', u * 0.75 + (n - 0.5) * 0.4)
    return col + (clamp01((1 - u ** 2) * (0.45 + 0.35 * n)),)


# ----------------------------------------------------------------------------- Cryo
def paint_ice_spike(a, b):
    """Cryo ice spike (frost bursts, ice walls, icicle bursts; cross kind, foot at b 0): a faceted ice crystal, white
    ridge #E4F6FC, lit facet #A2DAEF, shade #42BCF4 / #2C4F76 (v9 §5.5 ice #ABF3FC / #85DCF7 / #42BCF4)."""
    if b < 0 or b > 1:
        return CLEAR
    hw = 0.3 * (1 - b) ** 0.9 + 0.003
    if abs(a) > hw:
        return CLEAR
    u = a / hw
    if abs(u) > 0.9:
        return hexc('#2C4F76') + (0.95,)
    if abs(u) < 0.08:
        return hexc('#F2FCFF') + (0.97,)
    col = mix('#A2DAEF', '#E4F6FC', b) if u < 0 else mix('#42BCF4', '#85DCF7', b)
    return col + (0.88,)


def paint_frost(a, b):
    """Frost mist puff (Cryo footfalls, bursts, the absorb gather): pale #E4F6FC to #8FC6E9 with ice glints."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    edge = 0.72 + 0.22 * fbm(math.cos(th) * 1.6 + 9, math.sin(th) * 1.6 + 9, 3)
    if r > edge:
        return CLEAR
    u = r / edge
    n = fbm(a * 4 + 2, b * 4 + 2, 3)
    if star4(a - 0.25, b - 0.2, 0.25, 0.03) > 0.5 or star4(a + 0.3, b + 0.25, 0.18, 0.03) > 0.5:
        return hexc('#FFFFFF') + (1.0,)
    col = mix('#F2FCFF', '#8FC6E9', u * 0.8 + (n - 0.5) * 0.3)
    return col + (clamp01((1 - u ** 2) * (0.5 + 0.35 * n)),)


def paint_icicle(a, b):
    """Ice lance / icicle (서리 습격 icicle, 쏟아지는 천화 lances; cross kind, tip at +b): a long ice spear #ABF3FC /
    #85DCF7 / #42BCF4 with a white core and a frosty tail (v9 §5.5 lance)."""
    if b < -0.5 or b > 0.5:
        return CLEAR
    t = b + 0.5
    hw = 0.12 * (1 - t) ** 0.6 * smooth(0.0, 0.15, t) + 0.004
    if abs(a) > hw:
        g = 0.4 * math.exp(-((abs(a) - hw) / 0.03) ** 2) * (1 - t)
        return hexc('#85DCF7') + (g,) if g > 0.03 else CLEAR
    u = abs(a) / hw
    col = ramp(rmp((0, '#FFFFFF'), (0.3, '#ABF3FC'), (0.7, '#85DCF7'), (1, '#42BCF4')), u)
    return col + (0.95,)


def paint_ice_sphere(a, b):
    """쏟아지는 천화 spiky ice sphere (43): a pale sphere #B9F1FB / #84DAF4 with ice spikes around it, dark limb
    #60AAD5 (v9 §5.5 sphere #A0EEFB / #B8F7FD / #60AAD5)."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    spike = 0.0
    for k in range(12):
        d = (th - 2 * math.pi * k / 12 + math.pi) % (2 * math.pi) - math.pi
        ln = 0.98 if k % 2 == 0 else 0.84
        w = 0.17 * (1 - (r - 0.5) / (ln - 0.5)) if 0.5 < r < ln else 0
        if abs(d) < w:
            spike = 1.0
    if r < 0.58:
        q = r / 0.58
        col = ramp(rmp((0, '#F2FCFF'), (0.45, '#B8F7FD'), (0.8, '#84DAF4'), (1, '#60AAD5')), q)
        spec = math.exp(-(((a + 0.18) / 0.1) ** 2 + ((b - 0.2) / 0.07) ** 2))
        return mix(col, '#FFFFFF', 0.8 * spec) + (0.95,)
    if spike:
        return mix('#A0EEFB', '#F2FCFF', 0.5 + 0.5 * math.cos(th * 6)) + (0.95,)
    g = 0.35 * math.exp(-((r - 0.6) / 0.15) ** 2)
    return hexc('#84DAF4') + (g,) if g > 0.03 else CLEAR


# ----------------------------------------------------------------------------- Electro
_BL = random.Random(3)
BOLT_MAIN = jag(_BL, 0.0, 1.0, 0.02, 0.0, 12, 0.1)
BOLT_LINES = make_lines([BOLT_MAIN, jag(_BL, *BOLT_MAIN[3], 0.22, 0.45, 4, 0.25),
                         jag(_BL, *BOLT_MAIN[6], -0.2, 0.25, 3, 0.25)])


def paint_bolt(a, b):
    """Electro lightning bolt (sky bolts, bolt discs, the hexagram lumps; face kind, foot at b 0): a jagged branching
    bolt, white core, violet body #D569E2 / #DB8BE4, glow #C18AEA (v6 §4.3 lightning #DB8BE4 / #E3ADE9 / #D569E2 /
    #D33EE1 with white cores)."""
    if b < -0.02 or b > 1.02:
        return CLEAR
    d = lines_dist(a, b, BOLT_LINES, 0.12)
    return glow_stroke(d, 0.012, 0.03, WHITE, hexc('#DB8BE4'), halo=0.07, halo_col=hexc('#C18AEA'))


_AR = random.Random(321)
ARC_MAIN = jag(_AR, -0.48, 0.0, 0.48, 0.02, 10, 0.09)
ARC_LINES = make_lines([ARC_MAIN, jag(_AR, *ARC_MAIN[3], -0.08, 0.2, 3, 0.25), jag(_AR, *ARC_MAIN[7], 0.3, -0.19, 3, 0.25)])


def paint_arc(a, b):
    """Neutral electric arc (Electro crackle, tail sparks, the absorb discharge): a jagged branching arc with a white
    core; tint violet."""
    d = lines_dist(a, b, ARC_LINES)
    if d < 0.011:
        return WHITE + (1.0,)
    if d < 0.024:
        return (0.9, 0.9, 0.95, 1.0)
    g = 0.55 * math.exp(-(d / 0.045) ** 2)
    return (0.85, 0.85, 0.9, g) if g > 0.02 else CLEAR


def paint_shell(a, b):
    """번개의 가루 shell (44): a violet sphere #4948A1 / #6349C1 with a glowing square glyph #D7B6F6 and a bright rim
    (v7 §5 'Electro shell #4948A1 / #6349C1 body, glyph #D7B6F6')."""
    r = math.hypot(a, b)
    R = 0.8
    if r > 1:
        return CLEAR
    if r > R:
        g = 0.5 * (1 - (r - R) / (1 - R)) ** 2
        return hexc('#C58BFF') + (g,)
    q = r / R
    d = rune_dist(a, b, 'electro', 0.42)
    if d < 0.03:
        return mix('#FFFFFF', '#D7B6F6', d / 0.03) + (1.0,)
    col = ramp(rmp((0, '#8A6FE0'), (0.5, '#6349C1'), (0.85, '#4948A1'), (1, '#C58BFF')), q)
    return col + (0.95,)


# ----------------------------------------------------------------------------- element sprites (sigils, runes, glyphs, fronts)
EL_GLOW = {1: ('#FFD2A0', '#FF8A3D', '#AE2503'), 2: ('#CDEBFF', '#4FB8FF', '#1C74AC'),
           3: ('#EEDDFF', '#C58BFF', '#6A3FC8'), 4: ('#F2FCFF', '#9FE8F5', '#3AA6C0'),
           5: ('#FFE8A0', '#F0C860', '#8D6C3F')}
SIGIL_RUNE = {1: 'fire', 2: 'water', 3: 'bolt', 4: 'snow', 5: 'geo'}
BRAND_RUNE = {1: 'pyro', 2: 'hydro', 3: 'electro', 4: 'cryo'}


def make_sigil(el):
    """Absorb sigil card (화 / 水 / ⚡ / ❄ / Geo): a glowing element glyph in a thin circle."""
    hot, body, deep = EL_GLOW[el]
    rune = SIGIL_RUNE[el]

    def sigil(a, b):
        r = math.hypot(a, b)
        if r > 1:
            return CLEAR
        d = min(rune_dist(a, b, rune, 0.62), abs(r - 0.9) + 0.004)
        return glow_stroke(d, 0.025, 0.06, hexc(hot), hexc(body), halo=0.12, halo_col=hexc(body))
    sigil.__doc__ = f'Absorb sigil, element {el} ({rune}) in {body} with a {hot} core (v5 A 火 sigils, v5 §4.2 Hydro sigils).'
    return sigil


def make_rune(el):
    """Brand rune over the player's chest (plan §4.10-5)."""
    hot, body, deep = EL_GLOW[el]
    rune = BRAND_RUNE[el]

    def rn(a, b):
        d = rune_dist(a, b, rune, 0.85)
        return glow_stroke(d, 0.03, 0.065, hexc(hot), hexc(body), halo=0.13, halo_col=hexc(body))
    rn.__doc__ = (f'Brand rune, element {el} ({rune}): {body} with a white core (v5 §4.3 Pyro ")火(", v9 §5.3 Hydro '
                  '"ccc / |||", v8 Cryo "大巛", v7 Electro square rune).')
    return rn


GLYPH_RUNE = {1: 'fire', 2: 'water', 3: 'bolt', 4: 'snow', 5: 'geo'}


def make_glyph(el):
    """Stele / arrival glyph prop (flame, water curl, bolt, snowflake, Geo emblem): the element glyph carved in gold,
    glowing in the element colour, on a dark round plate."""
    hot, body, deep = EL_GLOW[el]
    rune = GLYPH_RUNE[el]

    def gl(a, b):
        r = math.hypot(a, b)
        if r > 1:
            return CLEAR
        d = rune_dist(a, b, rune, 0.6)
        if d < 0.07:
            return glow_stroke(d, 0.03, 0.07, hexc(hot), hexc(body))
        if r > 0.9:
            return mix('#C8781E', '#F2B53A', 0.5 + 0.5 * math.sin(math.atan2(b, a) * 12)) + (1.0,)
        if r > 0.86:
            return hexc('#241A10') + (1.0,)
        col = mix('#2E2619', '#4C3A24', fbm(a * 4, b * 4, 2))
        col = mix(col, hexc(body), 0.35 * math.exp(-(d / 0.12) ** 2))
        return col + (1.0,)
    gl.__doc__ = f'Glyph prop, element {el} ({rune}): gold-rimmed dark plate, the glyph glowing {body}.'
    return gl


def paint_gate_icon(a, b):
    """The gate label icon (registry icon.model): a gold seal ring with the 回 meander, two forward-sweeping gold horns
    and a red eye gem (the 야타용왕 crest: gold horns, red eyes, v1 §5.1)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    # horns
    for s in (-1, 1):
        d = abs(math.hypot(a - 0.55 * s, b + 0.1) - 0.55)
        if d < 0.07 and b > -0.05 and a * s > 0.05:
            return mix('#C8781E', '#FFE8A0', clamp01(0.5 + b)) + (1.0,)
    d = _hui_dist(a, b + 0.05, 0.55)
    if d < 0.035:
        return hexc('#FFE8A0') + (1.0,)
    if math.hypot(a, b + 0.05) < 0.1:
        return mix('#F67677', '#9D1C22', math.hypot(a, b + 0.05) / 0.1) + (1.0,)
    if r > 0.88:
        return mix('#8D6C3F', '#F2B53A', 0.5 + 0.5 * b) + (1.0,)
    if r > 0.83:
        return hexc('#241A10') + (1.0,)
    return mix('#2E2619', '#5A4B32', fbm(a * 3, b * 3, 2)) + (0.95,)


# fronts: the band kind (v > 0 flat strip, b = v - 1 from the front (0) to the inner edge (-1); v < 0 the wall)
FRONT_STRIP = {5: ('#E9D9A2', '#BEAC73', '#856D3C'), 2: ('#E5EAF1', '#4FB8FF', '#1C74AC'),
               1: ('#F9F2AE', '#F47B09', '#AE2503'), 4: ('#F2FCFF', '#9FE8F5', '#3AA6C0'),
               3: ('#EEDDFF', '#C58BFF', '#6A3FC8')}
FRONT_WALL = {5: ('#B79C62', '#817252'), 2: ('#E5EAF1', '#4DB5CF'), 1: ('#F8CE0B', '#CC4410'),
              4: ('#F2FCFF', '#8FC6E9'), 3: ('#EEDDFF', '#885AD3')}
_FR = random.Random(5150)
FRONT_ROCKS = [(-0.42 + 0.84 * (k + _FR.uniform(0.2, 0.8)) / 7, _FR.uniform(0.25, 0.65), _FR.uniform(0.08, 0.13),
                _FR.uniform(0, 3), rock_poly(_FR, 6, 0.4)) for k in range(7)]


def make_front(el):
    """Wave front segment (band kind) of the N10 fronts (산사태, jump, stomp, frost ring): a streaky element-coloured
    strip with tumbling rock slabs and a standing wall (Geo dust, Hydro water, Pyro fire, Cryo frost, Electro sparks)
    (v4 §5 wave gold streak #E9D9A2 / #BEAC73 / #856D3C, dust #746E5F, slabs #2D2215; v5 T Hydro walls)."""
    hot, mid, deep = FRONT_STRIP[el]
    w_top, w_bot = FRONT_WALL[el]

    def front(a, v):
        end = 1 - smooth(0.38, 0.5, abs(a))
        if end <= 0:
            return CLEAR
        if v >= 0:
            u = 1 - v
            for x0, y0, s, rot, poly in FRONT_ROCKS:
                dx, dy = (a - x0) / (s * 0.42), (u - y0) / s
                if abs(dx) < 1.2 and abs(dy) < 1.2:
                    c, sn = math.cos(rot), math.sin(rot)
                    ins, m = in_rock(dx * c + dy * sn, -dx * sn + dy * c, poly)
                    if ins and el in (5, 1, 2):
                        col = mix('#2D2215', '#555448', 0.5 + 0.5 * dy) if m > 0.15 else hexc('#1A140C')
                        return col + (clamp01(end),)
            streak = fbm(a * 30 + el, u * 2.5, 3)
            col = ramp(rmp((0, hot), (0.35, mid), (1, deep)), clamp01(u * 1.1 + (streak - 0.5) * 0.4))
            alpha = (1 - smooth(0.55, 1.0, u)) * (0.6 + 0.4 * streak)
            if u < 0.1:
                alpha = max(alpha, 0.95)
            return col + (clamp01(alpha * end),)
        y = v + 1
        n = fbm(a * 7 + 5 + el, y * 2.2, 3)
        h = 0.35 + 0.55 * fbm(a * 9 + 11 + el, 0.7, 3)
        if y > h:
            return CLEAR
        f = y / h
        col = mix(w_top, w_bot, f + (n - 0.5) * 0.3)
        if el == 3 and abs(fbm(a * 16, y * 6, 2) - 0.5) < 0.03:
            col = hexc('#FFFFFF')
        alpha = (0.9 - 0.55 * f ** 1.4) * (0.7 + 0.3 * n)
        return col + (clamp01(alpha * end),)
    front.__doc__ = f'Wave front band segment, element {el}: strip {hot} / {mid} / {deep}, wall {w_top} -> {w_bot}.'
    return front


# ----------------------------------------------------------------------------- props: spikes, shards, crystals, seal
def make_spike(kind):
    """천동만상 spike prop (cross kind, foot at b 0, tip at +b)."""
    pal = {'geo': ('#FFF2C0', '#E7C683', '#251B0D', '#917D49'),        # v1: planted shard body #251B0D, cracks #917D49
           'cryo': ('#EBF1F9', '#AFF5FC', '#0D1424', '#42BCF4'),       # v9: dark spike #0D1424, white rim #EBF1F9
           'electro': ('#EEDDFF', '#C58BFF', '#1E1238', '#B666EB')}[kind]   # v6: black-violet #412592, cracks #B666EB
    rim, glow, body, crack = pal

    def spike(a, b):
        if b < 0 or b > 1:
            return CLEAR
        hw = 0.3 * (1 - b) ** 1.05 + 0.004
        if abs(a) > hw + 0.04:
            return CLEAR
        if abs(a) > hw:
            g = 0.7 * (1 - (abs(a) - hw) / 0.04)
            return hexc(glow) + (g * (0.4 + 0.6 * b),)
        u = a / hw
        if abs(u) > 0.82:
            return mix(glow, rim, b) + (1.0,)
        n = fbm(a * 14, b * 9, 2)
        col = mix(body, '#3A2E20' if kind == 'geo' else body, n)
        if abs(fbm(a * 6 + 2, b * 5, 2) - 0.5) < 0.03:
            col = hexc(crack)
        if b > 0.9:
            col = mix(col, rim, (b - 0.9) / 0.1)
        return col + (1.0,)
    spike.__doc__ = f'{kind} spike: body {body}, glowing cracks {crack}, rim {rim} / glow {glow}.'
    return spike


def make_shard(el):
    """응결 결정 crystal shard pickup (plan §4.10-4): a gold-amber crystal with the element colour glowing inside."""
    hot, body, deep = EL_GLOW[el]

    def shard(a, b):
        t = b + 0.5
        if t <= 0 or t >= 1:
            g = 0.0
        else:
            half = 0.36 * (t / 0.4 if t < 0.4 else (1 - t) / 0.6) ** 0.8
            m = half - abs(a)
            if m > 0:
                if m < 0.035:
                    return hexc('#7C4A10') + (1.0,)
                core = math.exp(-((a / 0.12) ** 2 + ((t - 0.42) / 0.16) ** 2))
                col = mix('#F2B53A', '#FFE8A0', 0.5 - a) if abs(a) > 0.02 else hexc('#FFF6D0')
                col = mix(col, hexc(body), 0.75 * core)
                col = mix(col, hexc(hot), 0.5 * core ** 3)
                return col + (0.95,)
        r = math.hypot(a, (b + 0.05) * 0.8)
        g = 0.45 * math.exp(-(r / 0.35) ** 2)
        return hexc(body) + (g,) if g > 0.03 else CLEAR
    shard.__doc__ = f'응결 결정, element {el}: gold-amber #F2B53A shell, {body} core.'
    return shard


_CY = random.Random(616)
CRYSTALS = [(0.0, 0.0, 1.0, 0.17), (-0.12, -22, 0.72, 0.13), (0.13, 24, 0.66, 0.12), (-0.24, -38, 0.48, 0.1),
            (0.26, 40, 0.44, 0.1), (0.05, 8, 0.55, 0.09), (-0.05, -10, 0.38, 0.08)]


def paint_crystal(a, b):
    """Arena crystal cluster (16 per fight on the hanging clusters and the rim; cross kind, foot at b 0): pale faceted
    crystals with white ridges, dark edges and a glowing core; near-neutral, tinted geo gold / hydro / pyro / cryo /
    electro (plan §2.6, theme.md §6.3)."""
    if b < 0 or b > 1:
        return CLEAR
    best = None
    for x0, deg, ln, w0 in CRYSTALS:
        t = math.radians(deg)
        ux, uy = math.sin(t), math.cos(t)
        along = (a - x0) * ux + b * uy
        if along <= 0 or along >= ln:
            continue
        perp = (a - x0) * uy - b * ux
        hw = w0 * min(1.0, (ln - along) / (0.3 * ln))
        if abs(perp) < hw:
            q = perp / hw
            if best is None or w0 > best[2]:
                best = (q, along / ln, w0)
    if best:
        q, f, _w = best
        if abs(q) > 0.85:
            return (0.35, 0.32, 0.3, 1.0)
        if abs(q) < 0.1:
            return WHITE + (1.0,)
        v = 0.95 - 0.1 * f if q < 0 else 0.68 + 0.12 * f
        return (v, v, v, 0.92)
    g = math.exp(-((a / 0.4) ** 2 + (b / 0.15) ** 2))
    return (1.0, 1.0, 1.0, clamp01(0.6 * g)) if g > 0.05 else CLEAR


def paint_stele(a, b):
    """Intro seal stele (box kind; one texture on every face): dark red-brown stone #4C2F1E / #60391E / #3E271A with a
    carved meander frame and diamond lattice, glowing vertical gold cracks #CBA340 (v1 §5.2 'Steles')."""
    edge = 0.5 - max(abs(a), abs(b))
    n = fbm(a * 4 + 3, b * 4 + 3, 3)
    col = mix('#3E271A', '#60391E', n)
    if edge < 0.04:
        return mix(col, '#221208', 0.6) + (1.0,)
    if edge < 0.09:
        if (int((a + b) * 30) % 2) == 0:
            col = mix(col, '#B6A666', 0.5)
        return col + (1.0,)
    lat = abs(((a + b) * 6) % 1 - 0.5) < 0.05 or abs(((a - b) * 6) % 1 - 0.5) < 0.05
    if lat:
        col = mix(col, '#241408', 0.55)
    for x0 in (-0.12, 0.15):
        if abs(a - x0 - 0.03 * math.sin(b * 20)) < 0.012:
            return mix('#FFE8A0', '#CBA340', 0.4) + (1.0,)
    return col + (1.0,)


def paint_prism(a, b):
    """Intro seal prism wall (prism kind, 8 walls): translucent gold glyph wall #B6A666 / #C5B577 with bright glyph
    strokes #EDE0A9 and a bright base band #F4E8CD (v1 §5.2 'Seal (intro)')."""
    if abs(a) > 0.5 or b < 0 or b > 1:
        return CLEAR
    n = fbm(a * 5 + 1, b * 5, 2)
    gx, gy = (a * 4) % 1 - 0.5, (b * 6) % 1 - 0.5
    glyph = _hui_dist(gx * 2.2, gy * 2.2, 0.62) < 0.08
    if b < 0.04:
        return hexc('#F4E8CD') + (0.95,)
    if glyph:
        return hexc('#EDE0A9') + (0.85 * (1 - b * 0.4),)
    al = (0.22 + 0.1 * n) * (1 - 0.5 * b)
    return mix('#B6A666', '#C5B577', n) + (clamp01(al),)


def paint_cure_burst(a, b):
    """Brand cleanse burst (butterfly-style cure fx): a white-gold burst sphere with a gold ring (the butterfly kit's
    cure_burst look)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    ring = math.exp(-((r - 0.82) / 0.05) ** 2)
    core = math.exp(-(r / 0.45) ** 2)
    i = max(ring, core)
    col = mix('#F2B53A', '#FFFDF0', core)
    return col + (clamp01(i),)


# ----------------------------------------------------------------------------- HUD glyphs (x right, y up, -1..1)
def glyph_badge(x, y):
    """Badge ◈ (name line): a white diamond outline around a white diamond core with a dark outline; tinted by the text
    component colour (dim #707070 until absorbed, then the element colour)."""
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


def glyph_brand(x, y):
    """Brand badge (◈낙인): a white seal circle with a branded mark (a 回 inside a flame-like crown); tinted by the
    component colour."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    d = min(abs(r - 0.82), _hui_dist(x, y + 0.1, 0.55))
    d = min(d, seg_dist(x, y, -0.3, 0.45, 0.0, 0.75), seg_dist(x, y, 0.0, 0.75, 0.3, 0.45))
    if d < 0.08:
        return WHITE + (1.0,)
    if d < 0.15:
        return (0.12, 0.12, 0.12, 1.0)
    return (0.12, 0.12, 0.12, 0.55) if r < 0.82 else CLEAR


def make_glyph_el(el):
    """Element mini-icon (sub-line): the element sigil in its colour on a dark round plate."""
    hot, body, deep = EL_GLOW[el]
    rune = SIGIL_RUNE[el]

    def g(x, y):
        r = math.hypot(x, y)
        if r > 1:
            return CLEAR
        d = rune_dist(x, y, rune, 0.62)
        if d < 0.1:
            return mix(hot, body, d / 0.1) + (1.0,)
        if r > 0.86:
            return hexc(body) + (1.0,)
        if r > 0.78:
            return hexc('#141414') + (1.0,)
        return hexc(deep) + (0.85,)
    g.__doc__ = f'Element mini-icon {el}: {rune} in {body}.'
    return g


def glyph_safe(x, y):
    """Safe-zone icon (안전 지대 line): a green ring with the safe glyph, dark outline."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    d = min(abs(r - 0.78), seg_dist(x, y, 0.0, -0.4, 0.0, 0.42), seg_dist(x, y, -0.25, 0.18, 0.0, 0.42),
            seg_dist(x, y, 0.25, 0.18, 0.0, 0.42))
    if d < 0.1:
        return hexc('#8CF0A0') + (1.0,)
    if d < 0.18:
        return hexc('#0E2A14') + (1.0,)
    return hexc('#1E5A2A') + (0.6,) if r < 0.78 else CLEAR


# "점프!" drawn with strokes (x -1..1 across, y -0.5..0.5): ㅈ ㅓ / ㅁ (점), ㅍ / ㅡ (프), !
JUMP_STROKES = [
    [(-0.95, 0.42), (-0.62, 0.42)], [(-0.78, 0.42), (-0.95, 0.08)], [(-0.78, 0.42), (-0.6, 0.08)],     # ㅈ
    [(-0.42, 0.48), (-0.42, 0.02)], [(-0.58, 0.26), (-0.42, 0.26)],                                      # ㅓ
    [(-0.9, -0.08), (-0.48, -0.08), (-0.48, -0.46), (-0.9, -0.46), (-0.9, -0.08)],                       # ㅁ
    [(-0.15, 0.44), (0.42, 0.44)], [(-0.05, 0.44), (-0.05, 0.1)], [(0.32, 0.44), (0.32, 0.1)],
    [(-0.18, 0.1), (0.45, 0.1)],                                                                          # ㅍ
    [(-0.22, -0.2), (0.5, -0.2)],                                                                         # ㅡ
    [(0.8, 0.46), (0.8, -0.12)], [(0.8, -0.38), (0.8, -0.42)]]                                            # !
JUMP_LINES = make_lines(JUMP_STROKES)


def glyph_jump(x, y):
    """The "점프!" big cue (title line, 12 t at each landslide wave - 8): bold gold-white strokes with a dark outline and
    an amber glow, a double up-chevron underneath."""
    yy = y / 0.5 * 0.5
    d = lines_dist(x, yy, JUMP_LINES, 0.1)
    if d < 0.05:
        return mix('#FFFFFF', '#FFE8A0', d / 0.05) + (1.0,)
    if d < 0.085:
        return (0.1, 0.05, 0.02, 1.0)
    g = 0.5 * math.exp(-((d - 0.085) / 0.06) ** 2)
    return hexc('#FF8A3D') + (g,) if g > 0.04 else CLEAR


def glyph_chevron(x, y):
    """Jump chevron (a double up-chevron; the low-band / jumpable cue and the nd 2 look on the HUD)."""
    d = 9.0
    for cy in (-0.25, 0.25):
        d = min(d, seg_dist(x, y, -0.6, cy - 0.35, 0.0, cy + 0.15), seg_dist(x, y, 0.0, cy + 0.15, 0.6, cy - 0.35))
    if d < 0.12:
        return mix('#FFFFFF', '#FFD2A0', d / 0.12) + (1.0,)
    if d < 0.2:
        return (0.12, 0.05, 0.02, 1.0)
    return CLEAR


def glyph_hui(x, y):
    """回 mark (hint lines; the undodgeable language): red-amber #FF5A1E squares with a dark outline."""
    d = _hui_dist(x, y, 1.2)
    if d < 0.09:
        return hexc('#FF8A5A') + (1.0,)
    if d < 0.16:
        return (0.1, 0.04, 0.02, 1.0)
    return CLEAR


def glyph_orn(side):
    """Banner ornament: a gold meander scroll ending in a 回 hook, pointing toward the banner text."""
    def g(x, y):
        x = x * side
        pts = [(-0.95, 0.0), (0.2, 0.0), (0.2, 0.4), (-0.25, 0.4), (-0.25, -0.35), (0.6, -0.35), (0.6, 0.0), (0.95, 0.0)]
        d = poly_dist(x, y, pts)
        if d < 0.07:
            return mix('#FFE8A0', '#F2B53A', d / 0.07) + (1.0,)
        if d < 0.12:
            return (0.12, 0.08, 0.02, 1.0)
        return CLEAR
    g.__doc__ = 'Banner ornament ' + ('left' if side > 0 else 'right') + ': a gold meander scroll.'
    return g
