"""Painted sprites of the 아펩의 오아시스 파수꾼 fx kit (tools/build_mboss_ap_fx.py). Stdlib only.

The chapter-3 boss is a Dendro warden of a forest oasis: its effects are leaves (pale green, lime, black flakes, gold
embers), white-gold crystal blades and gold glow in phase 1 (the withered olive field), lime / yellow-green light in
phase 3 (the lush lake), thorn wheels, seed orbs, light columns, the 종말의 여파 field and domes. Every hex value below
was sampled from the footage notes (scratchpad ap/understand/v1-v6w.md: §FX colours, the per-event rows) and the plan
(scratchpad ap/plan.md §8).

Only Apep's own shapes are painted here (plan §5.4: <= 0.35 M new px). The generic telegraph textures (rims, fills,
rings, lane bars) and the neutral glow / glint / mote / streak / ripple / spark / smoke kinds are the field generator
kit's (tools/mboss_fg_fx_paint.py), referenced by the Apep item models, not painted again.

Card coordinates follow the fg kit: every painter takes (a, b) inside its kind's painter box and returns straight-alpha
(r, g, b, alpha) floats; +a is the card's local -x (the right when seen from behind or from above), +b is up (face
cards) or forward (flat cards). Cross kinds paint +b along their long axis. Neutral sprites (white or near white) are
tinted per spawn by the item definition's minecraft:custom_model_data tint, which multiplies the texture colour (a dark
tint darkens them: the black leaf flakes are the neutral leaf tinted near-black).

The helpers (noise, ramps, the telegraph band profiles) are copies of the fg painter's so the kits can change apart
(fg_fx_api.md §13 plans one shared module).
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
DARK_G = hexc('#14200A')             # dark green outline of the painted decals

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
    """value noise that tiles with an integer period (the seamless water and flood tiles)"""
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


def lines_dist(px, py, lines, pad=0.08):
    """distance to the nearest of several polylines (lines from make_lines)"""
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


def leaf_shape(u, v, w=0.42, tip=1.0):
    """(inside 0..1 soft mask, edge distance) of a pointed leaf along +v from v = -1 (stem) to v = tip, half width w
    at v = -0.2: a lens shape (two circular arcs) with a slightly rounded base."""
    t = (v + 1) / (tip + 1)                    # 0 at the stem, 1 at the tip
    if t < 0 or t > 1:
        return 0.0, -1.0
    hw = w * math.sin(math.pi * t ** 0.85) ** 0.9
    if hw <= 1e-4:
        return 0.0, -1.0
    e = 1 - abs(u) / hw
    return (1.0 if e > 0 else 0.0), e


# ----------------------------------------------------------------------------- telegraph bands (fg kit profiles)
def _band(r, bands):
    for lo, hi, col, al in bands:
        if lo <= r < hi:
            return col + (al,)
    return CLEAR


RIM_BANDS = ((0.900, 0.915, DARK, 0.7), (0.915, 0.955, WHITE, 1.0), (0.955, 0.99, DARK, 0.92))
RIM_BANDS_S = ((0.66, 0.72, DARK, 0.7), (0.72, 0.86, WHITE, 1.0), (0.86, 0.99, DARK, 0.92))


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


# Sector / wedge pieces. A shape of full angle F is drawn as n = ceil(F / M) equal pieces of width P = F / n (M = 32
# degrees, or 64 for radii <= 3.5 b); each piece is the family member W >= P (PIECES) squeezed across by
# k = tan(P / 2) / tan(W / 2) (the card's x scale), which keeps its two edges exactly P apart and its arc at radius 1 on
# the centre line; the arc dips by cos(W / 2) / cos(P / 2) at the edges (<= 1.2 % up to 32 degrees, <= 4 % for the wide
# small-radius pieces, at most 0.14 b), so a piece never reaches beyond its hazard. A one-piece sector of radius
# <= 3.5 b draws its rim with both radial edges painted in (t_pe), so a small cone is two cards.
PIECES = (2, 4, 8, 16, 22, 27, 32, 40, 48, 56, 64)
PIECES_NARROW = tuple(w for w in PIECES if w <= 32)


def piece_half_width(w_deg):
    """half width (a units at radius 1) of a piece of full angle w_deg"""
    return math.sin(math.radians(w_deg / 2))


def make_t_pf(w_deg):
    half = w_deg / 2

    def fill(a, b):
        phi = math.degrees(math.atan2(a, b))
        if abs(phi) > half or b <= 0:
            return CLEAR
        return _fill(math.hypot(a, b))
    fill.__doc__ = f'Sector / wedge progress-fill piece, full angle {w_deg} deg (unit radius, apex at the origin, no edges).'
    return fill


def make_t_pa(w_deg, thick=False, edges=False):
    half = w_deg / 2
    bands = RIM_BANDS_S if thick else RIM_BANDS

    def rim(a, b):
        phi = math.degrees(math.atan2(a, b))
        if abs(phi) > half or b <= 0:
            return CLEAR
        r = math.hypot(a, b)
        if edges and r < 0.99:
            # the radial edges, drawn just inside the piece: a white core and a dark outline toward the inside
            t = math.radians(half)
            inward = min(r * math.sin(t - math.radians(abs(phi))), 9.0)
            if inward < 0.045:
                return WHITE + (1.0,)
            if inward < 0.075:
                return DARK + (0.92,)
        if r < 0.05 and edges:
            return DARK + (1.0,)
        return _band(r, bands)
    rim.__doc__ = (f'Sector / wedge rim-arc piece, full angle {w_deg} deg' + (' (thick, r <= 3.5)' if thick else '') +
                   (', both radial edges painted (a one-piece small sector)' if edges else
                    ': dark outline, tinted band, dark inner line; no radial edges (t_bar cards draw them)') + '.')
    return rim


def paint_t_jump(a, b):
    """Jump chevron decal (nd 2, the undodgeable-and-jumpable mark): two stacked white chevrons pointing forward with a
    dark outline; tinted the undodgeable red."""
    d = 9.0
    for cy in (-0.32, 0.18):
        d = min(d, seg_dist(a, b, -0.55, cy - 0.3, 0.0, cy + 0.12), seg_dist(a, b, 0.0, cy + 0.12, 0.55, cy - 0.3))
    if d < 0.085:
        return WHITE + (1.0,)
    if d < 0.15:
        return DARK + (0.9,)
    return CLEAR


_CR = random.Random(41)
CRACK_MAIN = jag(_CR, 0.0, 0.0, 0.0, 1.0, 14, 0.035)
CRACK_SIDE = []
for _k in range(7):
    _t = 0.08 + 0.13 * _k + _CR.uniform(-0.03, 0.03)
    _s = 1 if _k % 2 else -1
    _x0 = CRACK_MAIN[min(len(CRACK_MAIN) - 1, int(_t * 14))][0]
    CRACK_SIDE.append(jag(_CR, _x0, _t, _x0 + _s * _CR.uniform(0.18, 0.34), _t + _CR.uniform(0.02, 0.07), 3, 0.15))
CRACK_LINES = make_lines([CRACK_MAIN] + CRACK_SIDE)
CRACK_SPARK = [(_CR.uniform(-0.3, 0.3), _CR.uniform(0.03, 0.97)) for _ in range(14)]


def paint_t_crack(a, b):
    """生命의 손 crack-line strip (P2; unit length along +b, a = -0.5..0.5 across the 3 b strip): a jagged white-gold
    glowing crack with short side cracks and sparkles (v1 k_f1344: 'thin white-gold glowing crack-lines'), core
    #FFFBE0, glow #F2D27A; painted (the look is fixed gold)."""
    if b < 0 or b > 1:
        return CLEAR
    d = poly_dist(a, b, CRACK_MAIN)
    ds = lines_dist(a, b, CRACK_LINES[1:])
    core = math.exp(-(d / 0.022) ** 2)
    side = 0.75 * math.exp(-(ds / 0.016) ** 2)
    glow = 0.55 * math.exp(-(d / 0.12) ** 2) + 0.3 * math.exp(-(ds / 0.06) ** 2)
    sp = 0.0
    for x, y in CRACK_SPARK:
        sp = max(sp, star4(a - x, b - y, 0.07, 0.008))
    i = max(core, side, sp)
    al = clamp01(max(i, glow * 0.8))
    if al < 0.04:
        return CLEAR
    col = mix('#E7B24A', '#F2D27A', glow / 0.85)
    col = mix(col, '#FFFBE0', i)
    return col + (al,)


def paint_t_wash(a, b):
    """종말의 여파 field wash (unit radius, one floor-wide card; tinted the el 24 field fill): a near-white translucent
    disc with faint concentric ripples, glitter flecks and a brighter rim band, so the floor reads 'tinted' (w1 field:
    #9BBE61 / #ACD075 / #C5E892)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    rip = 0.5 + 0.5 * math.cos(r * 38 + 2 * fbm(a * 3, b * 3, 2))
    gl = 0.0
    n = vnoise(a * 41 + 7, b * 41 - 3)
    if n > 0.86:
        gl = (n - 0.86) / 0.14
    rim = math.exp(-((r - 0.965) / 0.022) ** 2)
    al = 0.22 + 0.05 * rip + 0.25 * gl + 0.45 * rim
    v = 0.86 + 0.08 * rip + 0.06 * max(gl, rim)
    return (v, v, v * 0.97, clamp01(al * (1 - smooth(0.985, 1.0, r))))


def paint_t_safe(a, b):
    """소생의 찬가 보호막 footprint (unit radius = the dome radius): a pale lime rim ring with a bright edge #F5FFD4 over
    #E4F69D, a dark green outline, a faint inner ring and 12 leaf-sprig ticks on the rim (v5 / w1 dome: rim
    #E3FBA7 / #F5FFD4, base ring of small leaf sprigs); painted (the safe look never takes an attack palette)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(a, b)
    best = CLEAR
    if 0.86 <= r < 0.885:
        best = DARK_G + (0.75,)
    elif 0.885 <= r < 0.93:
        best = hexc('#E4F69D') + (1.0,)
    elif 0.93 <= r < 0.955:
        best = hexc('#F8FFE2') + (1.0,)
    elif 0.955 <= r < 0.985:
        best = DARK_G + (0.85,)
    elif 0.74 <= r < 0.765:
        best = hexc('#D6F08C') + (0.55,)
    k = (th / (2 * math.pi) * 12) % 1
    u = (k - 0.5) * 2 * math.pi * r / 12
    if 0.66 <= r <= 0.88:
        m, e = leaf_shape(u * 3.2, (r - 0.77) / 0.11, 0.38)
        if m:
            return (mix('#9CCB52', '#E8F8B0', e) if e > 0.18 else DARK_G) + (1.0,)
    return best


def paint_t_dome(a, b):
    """The dome glyph at a footprint's centre (unit radius): a white-lime half-dome outline over a base line with a
    sprout on top and a vertical light seam, dark green outline (the dome = safe)."""
    if math.hypot(a, b) > 1:
        return CLEAR
    y = b + 0.32
    arc = abs(math.hypot(a, y) - 0.62) if y >= 0 else 9.0
    base = seg_dist(a, b, -0.78, -0.32, 0.78, -0.32)
    seam = seg_dist(a, b, 0.0, -0.32, 0.0, 0.3)
    sprout = min(seg_dist(a, b, 0.0, 0.3, 0.0, 0.52), seg_dist(a, b, 0.0, 0.46, -0.2, 0.62),
                 seg_dist(a, b, 0.0, 0.42, 0.18, 0.56))
    d = min(arc, base, sprout)
    if d < 0.06:
        return hexc('#F8FFE2') + (1.0,)
    if seam < 0.035:
        return hexc('#E4F69D') + (0.9,)
    if d < 0.11:
        return DARK_G + (0.95,)
    if y >= 0 and math.hypot(a, y) < 0.62:
        return hexc('#B5DA72') + (0.35,)
    return CLEAR


def paint_t_target(a, b):
    """증폭의 풀 following target ring (unit radius; tinted #C1E6A8): a soft translucent disc that brightens to a rim
    at r 0.9 with a dark outline, no progress edge (it is not a hazard decal)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.965:
        return DARK + (0.55 * (1 - smooth(0.985, 1.0, r)),)
    rim = math.exp(-((r - 0.9) / 0.04) ** 2)
    v = 0.9 + 0.1 * rim
    return (v, v, v, clamp01(0.2 + 0.18 * r * r + 0.6 * rim))


def paint_t_wall(a, b):
    """둥지 wall-blade footprint (1.4 x 0.5 b at scale 1: a in -0.7..0.7, b in -0.25..0.25): a pale yellow-green leaf
    bar #E6F08A with a darker midrib #A9C24E and a dark outline (v3 / v4 walls: translucent yellow-green blades)."""
    m, e = leaf_shape(b / 0.25 * 0.42, a / 0.7, 0.42)
    if not m:
        return CLEAR
    if e < 0.12:
        return DARK_G + (0.9,)
    rib = abs(b) < 0.018
    col = mix('#C8DC6A', '#EEF6A6', e)
    if rib:
        col = hexc('#A9C24E')
    return col + (0.85,)


# ----------------------------------------------------------------------------- phase-2 dressing and the flood
_SW = [(2 * math.pi * k / 7, 0.55 + 0.1 * (k % 3)) for k in range(7)]


def paint_d_swirl(a, b):
    """The Heart's gold swirl ring (unit radius; drawn r 3.5 at the centre): seven gold spiral arms sweeping into a
    bright ring at r 0.86, gold #EBC55A / #FFF4C8 with a soft glow (v2 / v3 phase-2 floor around the Heart)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    ring = math.exp(-((r - 0.86) / 0.028) ** 2)
    ring2 = 0.5 * math.exp(-((r - 0.93) / 0.012) ** 2)
    arm = 0.0
    for t0, w in _SW:
        # a log-spiral arm from r 0.25 to the ring
        phase = (th - t0 - 2.2 * math.log(max(r, 0.05) / 0.25)) % (2 * math.pi)
        dph = min(phase, 2 * math.pi - phase)
        if 0.22 < r < 0.88:
            arm = max(arm, math.exp(-(dph * r / (0.035 * w)) ** 2) * smooth(0.22, 0.4, r))
    glow = 0.35 * math.exp(-((r - 0.86) / 0.12) ** 2)
    i = max(ring, ring2, arm)
    al = clamp01(max(i, glow))
    if al < 0.04:
        return CLEAR
    col = mix('#B07A1E', '#EBC55A', clamp01(glow * 2 + i))
    col = mix(col, '#FFF4C8', i ** 1.5)
    return col + (al,)


_LY = random.Random(77)
LEY_MAIN = jag(_LY, 0.0, 0.0, 0.0, 1.0, 16, 0.03)
LEY_BRANCH = make_lines([jag(_LY, LEY_MAIN[k][0], LEY_MAIN[k][1], LEY_MAIN[k][0] + (0.22 if k % 2 else -0.22),
                             LEY_MAIN[k][1] + 0.07, 3, 0.2) for k in (3, 6, 9, 12)])


def paint_d_ley(a, b):
    """지맥 이상 ley-line crack strip (unit length along +b, a = -0.5..0.5): a jagged orange-gold glowing crack with a
    few short branches, core #FFE08A, glow #E8A53A; it fades out at both ends (the strips pulse by their width)."""
    if b < 0 or b > 1:
        return CLEAR
    d = poly_dist(a, b, LEY_MAIN)
    db = lines_dist(a, b, LEY_BRANCH)
    core = math.exp(-(d / 0.03) ** 2)
    br = 0.7 * math.exp(-(db / 0.02) ** 2)
    glow = 0.5 * math.exp(-(d / 0.16) ** 2)
    end = smooth(0.0, 0.08, b) * (1 - smooth(0.9, 1.0, b))
    i = max(core, br) * end
    al = clamp01(max(i, glow * end))
    if al < 0.04:
        return CLEAR
    col = mix('#C2701E', '#E8A53A', clamp01(glow * 2))
    col = mix(col, '#FFE08A', i)
    return col + (al,)


def paint_fl_tile(a, b):
    """종말의 여파 flood tile (seamless square; tiles abut on a 7.5 b grid): yellow flood #FBFAA4 / #DFEA59 / #E8E63E with
    bright glints #F5F573, about 55 % alpha (w1 k_w1_f0280)."""
    x, y = (a + 0.5) * 3, (b + 0.5) * 3
    n = pfbm(x, y, 3, 3)
    c = abs(pfbm(x * 2 + 0.5, y * 2 + 0.25, 6, 2) - 0.5)
    caustic = math.exp(-(c / 0.04) ** 2)
    col = ramp(rmp((0, '#DFEA59'), (0.5, '#E8E63E'), (0.8, '#FBFAA4'), (1, '#FFFFE6')), n * 0.7 + caustic * 0.4)
    return col + (clamp01(0.48 + 0.12 * n + 0.25 * caustic),)


# ----------------------------------------------------------------------------- leaves, blades, pools
def paint_leaf(a, b):
    """Neutral leaf (tint it: pale green ghost leaves, black flakes #2A2A10, gold embers #EBC55A): a pointed leaf with
    a midrib and two vein pairs, light shading 0.78-1.0 and a thin darker edge."""
    m, e = leaf_shape(a, b * 1.05, 0.46, 0.95)
    if not m:
        return CLEAR
    rib = abs(a) < 0.035 and b < 0.85
    vein = False
    for vy in (-0.35, 0.05, 0.42):
        if abs(abs(a) * 0.9 - (b - vy)) < 0.035 and abs(a) < 0.36:
            vein = True
    v = 0.84 + 0.16 * (0.5 + 0.5 * a / 0.46)
    if e < 0.1:
        v *= 0.72
    if rib or vein:
        v *= 0.8
    return (v, v, v, 1.0)


def paint_leaf_blade(a, b):
    """Neutral glowing leaf blade (tint it): a long pointed blade with a bright white core along the midrib and a soft
    halo; the rosette petals, the sweep-ring and skim blades, the upthrust leaf spikes (v5 / v6 #E0F996 / #A2CA6C)."""
    u, v = a / 0.5, b / 0.5
    m, e = leaf_shape(u, v, 0.34, 0.98)
    halo = 0.0
    m2, e2 = leaf_shape(u * 0.7, v, 0.34, 0.98)
    if m2:
        halo = 0.35 * clamp01(e2 * 2)
    if not m:
        return (1.0, 1.0, 1.0, halo) if halo > 0.03 else CLEAR
    core = math.exp(-(a / 0.05) ** 2)
    val = 0.8 + 0.2 * max(core, e)
    return (val, val, val, clamp01(0.75 + 0.25 * e))


def paint_blade(a, b):
    """Neutral crystal blade (tint white-gold #F0F2BB, gold #EBC55A or lime): a long faceted shard, its lit facet
    white, the shade facet grey 0.66, a bright edge line and a soft glow (v1 k_f0534 radial gold crystal blades)."""
    hw = 0.22 * (1 - abs(b) ** 1.6) * (1 - 0.5 * (b > 0) * b)
    if hw <= 0:
        return CLEAR
    if abs(a) > hw:
        g = 0.3 * math.exp(-((abs(a) - hw) / 0.05) ** 2) * (1 - abs(b))
        return (1.0, 1.0, 1.0, g) if g > 0.04 else CLEAR
    lit = a < 0.02 * b
    v = 1.0 if lit else 0.68
    if abs(a - 0.02 * b) < 0.018:
        v = 1.0
    return (v, v, v * 0.98, 0.95)


_PL = random.Random(3)
POOL_LEAVES = [(_PL.uniform(0, 2 * math.pi), _PL.uniform(0.15, 0.62), _PL.uniform(0.18, 0.3)) for _ in range(26)]


def paint_pool(a, b):
    """The dark olive leaf pool the boss sinks into (flat, unit radius 0.5 box): overlapping black-olive leaves
    #2D2A04 / #3F3C15 with a soft ragged edge and a darker centre (v1 k_f0000, the pool 6-8 m)."""
    r = math.hypot(a, b) * 2
    if r > 1:
        return CLEAR
    edge = 0.78 + 0.18 * fbm(math.atan2(b, a) * 2 + 3, 1.5, 2)
    if r > edge:
        return CLEAR
    shade = 0.0
    for th, rr, s in POOL_LEAVES:
        cx, cy = rr * math.cos(th), rr * math.sin(th)
        dx, dy = (a * 2 - cx), (b * 2 - cy)
        ca, sa = math.cos(th), math.sin(th)
        u, v = (dx * -sa + dy * ca) / s, (dx * ca + dy * sa) / s
        m, e = leaf_shape(u, v, 0.45)
        if m:
            shade = max(shade, 0.4 + 0.6 * e)
    col = mix('#1E1C03', '#3F3C15', shade * (1 - 0.5 * r))
    col = mix(col, '#55511E', 0.25 * fbm(a * 9, b * 9, 2))
    return col + (clamp01(0.95 * (1 - smooth(edge - 0.12, edge, r))),)


def paint_pad(a, b):
    """Translucent leaf pad of the underground trail (flat, unit radius 0.5): a round leaf with a notch, radial veins,
    green #8FC25A / #C9E58E at about 55 % alpha (v5 / v6 'leaf-pad trail, translucent green 2-3 m pads')."""
    r = math.hypot(a, b) * 2
    th = math.atan2(a, b)
    if r > 1 or abs(th) < 0.18:
        return CLEAR
    vein = 0.0
    for k in range(9):
        t = -math.pi + 0.35 + k * (2 * math.pi - 0.7) / 8
        vein = max(vein, math.exp(-(((th - t + math.pi) % (2 * math.pi) - math.pi) * r / 0.025) ** 2))
    col = mix('#8FC25A', '#C9E58E', 0.5 + 0.5 * r)
    col = mix(col, '#E8F6B8', 0.6 * vein)
    rim = smooth(0.9, 1.0, r)
    return mix(col, '#5E8A2C', rim) + (clamp01(0.5 + 0.3 * rim + 0.15 * vein),)


def paint_mound(a, b):
    """Leaf mound where the boss sinks in phase 3 (face, foot at b 0, a -0.5..0.5, b 0..0.5): a heap of lime leaves
    #B1CE71 / #7FA543 with white spray tips #F2FAE2 (v5 M 'leaf mound lime #B1CE71 + white spray')."""
    if b < 0:
        return CLEAR
    h = 0.42 * (1 - (a / 0.5) ** 2) ** 0.7 * (0.85 + 0.25 * fbm(a * 10, 2, 2))
    if b > h + 0.06:
        spray = 0.0
        for k in range(6):
            x = -0.35 + 0.14 * k
            spray = max(spray, math.exp(-(((a - x) / 0.012) ** 2 + ((b - h - 0.05) / 0.03) ** 2)))
        return (0.95, 0.98, 0.89, spray) if spray > 0.05 else CLEAR
    if b > h:
        return hexc('#F2FAE2') + (0.7,)
    n = fbm(a * 14, b * 14, 3)
    col = ramp(rmp((0, '#3E5A1E'), (0.4, '#7FA543'), (0.8, '#B1CE71'), (1, '#D8EBA0')), n * 0.6 + b / h * 0.5)
    return col + (1.0,)


def paint_root_chunk(a, b):
    """Brown root chunk with gold glints (burrow-relocate, T1 sink; face, unit 0.5): a knobbly root lump #4A3220 /
    #7A5634 with two gold flecks #F2C95A."""
    r = math.hypot(a / 0.46, b / 0.36)
    edge = 0.8 + 0.18 * fbm(math.atan2(b, a) * 1.6, 0.3, 2)
    if r > edge:
        return CLEAR
    n = fbm(a * 12, b * 12, 3)
    col = mix('#3A2616', '#8A6440', clamp01(0.5 - 0.6 * b + 0.4 * a + 0.3 * n))
    for gx, gy in ((0.12, 0.1), (-0.15, -0.06)):
        if math.hypot(a - gx, b - gy) < 0.045:
            col = hexc('#F2C95A')
    if r > edge - 0.08:
        col = mix(col, '#20140A', 0.6)
    return col + (1.0,)


# ----------------------------------------------------------------------------- props: wheels, orbs, balls
_TW = [(2 * math.pi * k / 9 + 0.12 * math.sin(k * 2.3), 0.95 + 0.08 * math.cos(k * 1.7)) for k in range(9)]


def _wheel(a, b, body, rim, core, thorn, thorn_tip, flare=None):
    """a thorn wheel (unit radius): a translucent bubble sphere r 0.66 with a curled thorn ring (9 hooked thorns out
    to r 0.98), an inner swirl and a specular band; colours given as hexes."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    out = CLEAR
    # thorns: curved hooks from r 0.6 to their tip
    for t0, ln in _TW:
        for k in range(10):
            s = k / 9
            rr = 0.58 + (ln - 0.58) * s
            tt = t0 + 0.42 * s * s
            px, py = rr * math.cos(tt), rr * math.sin(tt)
            w = 0.075 * (1 - s) + 0.012
            d = math.hypot(a - px, b - py)
            if d < w:
                col = mix(thorn, thorn_tip, s)
                return mix(col, '#1A2408', 0.5 if d > 0.72 * w else 0) + (1.0,)
    if r > 0.7:
        g = 0.35 * math.exp(-((r - 0.7) / 0.08) ** 2)
        out = hexc(rim) + (g,) if g > 0.03 else CLEAR
        return out
    q = r / 0.66 if r < 0.66 else 1.0
    if r >= 0.66:
        return mix(rim, '#1A2408', 0.4) + (1.0,)
    sw = math.sin(th * 2 + q * 6.0)
    col = mix(core, body, q ** 1.4)
    col = mix(col, rim, smooth(0.78, 1.0, q))
    col = mix(col, '#FFFFFF', 0.25 * smooth(0.55, 1.0, sw) * q)
    spec = math.exp(-(((a + 0.22) / 0.13) ** 2 + ((b - 0.28) / 0.08) ** 2))
    col = mix(col, '#FFFFFF', 0.8 * spec)
    al = 0.55 + 0.4 * q ** 3 + 0.3 * spec
    if flare is not None:
        f = star4(a, b, 0.62, 0.05)
        f2 = 0.55 * star4((a + b) / math.sqrt(2), (a - b) / math.sqrt(2), 0.34, 0.035)
        fi = max(f, f2, math.exp(-(r / 0.12) ** 2))
        col = mix(col, flare, clamp01(fi * 1.2))
        col = mix(col, '#FFF0E0', clamp01(math.exp(-(r / 0.07) ** 2)))
        al = max(al, fi)
    return col + (clamp01(al),)


def paint_thorn_wheel(a, b):
    """Carpet thorn wheel (P3; prop Ø 1.6 / carpet cards): a pale-green translucent bubble with nine curled thorns,
    body #D5EBB2, rim #A6CF74, core #F4FBE6, thorns #E6F2CC -> #FFFFFF (v1 k_f2286 / f2310 'carpet of thorn wheels')."""
    return _wheel(a, b, '#D5EBB2', '#A6CF74', '#F4FBE6', '#C9E2A0', '#F8FFEC')


def paint_thorn_wheel_hm(a, b):
    """Homing thorn wheel (P3, the readability change of plan §8 P3): gold-orange rim and core #F2A43A / #FFD27A, thorns
    #E8902A -> #FFE6A0 and a red 4-point flare #E23A2A in the middle, so it never reads as a carpet wheel."""
    return _wheel(a, b, '#F7C25E', '#E8902A', '#FFE7A8', '#E07C22', '#FFE6A0', flare='#E23A2A')


def paint_seed_bolt(a, b):
    """기본 ranged bolt (O2; prop Ø 0.6): a lime seed ball, core #F4FFD0, body #ABDE85, a soft glow #E7F99F."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.6:
        g = 0.55 * (1 - (r - 0.6) / 0.4) ** 2
        return hexc('#E7F99F') + (g,)
    q = r / 0.6
    col = ramp(rmp((0, '#F4FFD0'), (0.5, '#C9EE98'), (0.85, '#ABDE85'), (1, '#6E9E48')), q)
    spec = math.exp(-(((a + 0.18) / 0.12) ** 2 + ((b - 0.22) / 0.09) ** 2))
    return mix(col, '#FFFFFF', 0.8 * spec) + (1.0,)


def paint_seed_orb(a, b):
    """생명의 나선 seed orb (Q5; prop Ø 0.7): a glowing yellow-green ball #ABDE85 / #9CD68B with a darker green spiral
    glyph, a bright core #E6F8A5 and a flare halo #F6FBDE (v6 k_v6_f0672 'seed-orbs')."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.62:
        g = 0.6 * (1 - (r - 0.62) / 0.38) ** 2 + 0.25 * star4(a, b, 1.0, 0.03)
        return hexc('#F6FBDE') + (clamp01(g),)
    q = r / 0.62
    th = math.atan2(b, a)
    col = ramp(rmp((0, '#F4FCD2'), (0.35, '#E6F8A5'), (0.75, '#ABDE85'), (1, '#9CD68B')), q)
    sp = ((th - 3.4 * q) % (2 * math.pi)) / (2 * math.pi)
    if q > 0.18 and min(sp, 1 - sp) < 0.07:
        col = mix(col, '#4E8A1E', 0.75)
    spec = math.exp(-(((a + 0.2) / 0.12) ** 2 + ((b - 0.24) / 0.08) ** 2))
    return mix(col, '#FFFFFF', 0.7 * spec) + (1.0,)


def paint_charge_ball(a, b):
    """증폭의 풀 light ball over the crown (Q3; prop Ø 1.6): a white-yellow core #FDFBBD fading through #E7F99F into a
    white-green halo with four soft rays (v5 k_f2070 'bright ball above the head')."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    core = math.exp(-(r / 0.28) ** 2)
    halo = 0.65 * math.exp(-(r / 0.62) ** 2)
    rays = 0.5 * star4(a, b, 0.98, 0.04) + 0.25 * star4((a + b) / 1.4142, (a - b) / 1.4142, 0.6, 0.03)
    i = clamp01(max(core, halo, rays))
    col = mix('#D2F18B', '#FDFBBD', clamp01(core * 1.4 + rays))
    col = mix(col, '#FFFFFF', core ** 2)
    return col + (i,)


def paint_dome_flare(a, b):
    """Neutral half-dome flare (face, pivot at the base centre, b 0..0.5): a translucent shell brightest at its rim and
    base (tint lime for the 파괴 blast dome, white-green for the dome pop)."""
    if b < 0:
        return CLEAR
    r = math.hypot(a, b) * 2
    if r > 1:
        return CLEAR
    rim = math.exp(-((r - 0.94) / 0.05) ** 2)
    base = math.exp(-(b / 0.04) ** 2) * (r < 0.98)
    v = 0.86 + 0.14 * max(rim, base)
    return (v, v, v, clamp01(0.18 + 0.25 * r ** 3 + 0.6 * rim + 0.4 * base))


def paint_beam(a, b):
    """Neutral light beam / column (cross, foot at b 0, unit height; tint #FDFBBD for the shell beams, white-green for
    light pillars, green-gold for the Heart beam): a white core band with soft edges, fading out toward the top."""
    if b < 0 or b > 1:
        return CLEAR
    u = abs(a) / 0.5
    if u > 1:
        return CLEAR
    core = math.exp(-(u / 0.3) ** 2)
    body = 0.55 * (1 - u ** 2)
    fade = 1 - smooth(0.6, 1.0, b)
    foot = 1 + 0.4 * math.exp(-(b / 0.06) ** 2)
    i = clamp01(max(core, body) * fade * foot)
    v = 0.9 + 0.1 * core
    return (v, v, v, i)


def paint_crescent(a, b):
    """Neutral crescent trail segment (face, a -0.5..0.5 along the arc, b -0.125..0.125): a curved streak, bright inner
    edge, tapered ends (tint white-gold for P5, #A4D6AC / #BFE682 / #EBF898 for Q4)."""
    y = b - 0.28 * (a * a - 0.08)          # the arc bows toward +b in the middle
    t = abs(a) / 0.5
    if t >= 1:
        return CLEAR
    hw = 0.085 * (1 - t ** 2.0) + 0.006
    if abs(y) > hw * 1.6:
        return CLEAR
    edge = math.exp(-((y - 0.55 * hw) / (0.3 * hw)) ** 2)
    body = math.exp(-(y / hw) ** 2)
    i = clamp01(max(edge, 0.7 * body) * (1 - t ** 6))
    v = 0.82 + 0.18 * edge
    return (v, v, v, i)


def paint_rib(a, b):
    """Pale rib afterimage of the lunge-sweep (P1; face, a -0.5..0.5, b -0.5..0.5): a spine along a with seven curved
    rib pairs, translucent white #EEF2E0 (v1 k_f0630 'pale spine/skeleton afterimage')."""
    if abs(a) > 0.5:
        return CLEAR
    spine = math.exp(-(b / 0.02) ** 2) * (1 - smooth(0.4, 0.5, abs(a)))
    rib = 0.0
    for k in range(7):
        x0 = -0.42 + 0.14 * k
        for s in (-1, 1):
            # a rib curving back from the spine
            for j in range(6):
                t = j / 5
                px, py = x0 - 0.06 * t * t, s * (0.02 + 0.32 * t * (1 - 0.15 * k / 6))
                rib = max(rib, math.exp(-(math.hypot(a - px, b - py) / (0.016 * (1 - 0.5 * t) + 0.004)) ** 2))
    i = clamp01(max(spine, rib))
    return (0.93, 0.95, 0.88, i * 0.9) if i > 0.04 else CLEAR


def paint_spiral(a, b):
    """Neutral spiral wisp (face, unit 0.5): a two-turn spiral line with a soft glow fading toward its tail (tint pale
    green #D8F2B0 for the P2 / P3 wind-up wisps)."""
    r = math.hypot(a, b) * 2
    if r > 1 or r < 0.04:
        return CLEAR
    th = math.atan2(b, a)
    best = 0.0
    for turn in range(3):
        t = (th + 2 * math.pi * turn) / (4 * math.pi)        # 0..1 over two turns
        if 0 <= t <= 1:
            rr = 0.12 + 0.86 * t
            d = abs(r - rr)
            best = max(best, math.exp(-(d / (0.035 + 0.02 * t)) ** 2) * (0.35 + 0.65 * t))
    return (1.0, 1.0, 1.0, clamp01(best)) if best > 0.03 else CLEAR


def paint_splash(a, b):
    """Water splash crown (face, foot at b 0; near-white, tint teal #CDEFE4 on the lake): a crown of jets and droplets
    with a foam base (v5 / w1 water splashes, #EDFBF0 glints over #70995F water)."""
    if b < 0 or b > 1:
        return CLEAR
    best = 0.0
    for k in range(7):
        ang = math.radians(-55 + 110 * k / 6)
        ln = 0.7 + 0.25 * math.cos(k * 1.9)
        ux, uy = math.sin(ang), math.cos(ang)
        along = a * ux + b * uy
        if 0 < along < ln:
            perp = abs(a * uy - b * ux)
            w = 0.065 * (1 - along / ln) + 0.01
            best = max(best, clamp01(1 - perp / w) * (1 - (along / ln) ** 3))
    for k in range(10):
        x, y = -0.62 + 1.24 * ((k * 0.37) % 1), 0.42 + 0.52 * ((k * 0.61) % 1)
        if math.hypot(a - x, b - y) < 0.035:
            best = 1.0
    base = math.exp(-((a / 0.5) ** 2 + (b / 0.14) ** 2))
    i = max(best, base)
    if i < 0.05:
        return CLEAR
    v = 0.84 + 0.16 * i
    return (v * 0.96, v, v * 0.97, clamp01(0.35 + 0.6 * i))


def paint_shard(a, b):
    """Neutral glass shard (face, a -0.25..0.25, b -0.5..0.5): a thin triangular translucent shard with a bright edge
    (tint lime for the dome pop shards #E3FBA7)."""
    hw = 0.2 * (0.5 - b) / 1.0
    if b < -0.5 or b > 0.5 or abs(a + 0.05 * b) > hw:
        return CLEAR
    edge = abs(a + 0.05 * b) > hw - 0.03
    v = 1.0 if edge else 0.85
    return (v, v, v, 0.95 if edge else 0.5)


def paint_wisp(a, b):
    """Black twisted wisp of the 수호 death (face, a -0.25..0.25, b -0.5..0.5): a dark smoky ribbon #18140E twisting up
    with a faint red edge #7A1E14, fading at the top."""
    if b < -0.5 or b > 0.5:
        return CLEAR
    x = 0.11 * math.sin((b + 0.5) * 9.0)
    w = 0.07 * (1 - (b + 0.5) * 0.6)
    d = abs(a - x)
    if d > w * 1.6:
        return CLEAR
    n = fbm(a * 20, b * 8, 2)
    i = clamp01((1 - d / (w * 1.6)) * (0.7 + 0.3 * n) * (1 - smooth(0.2, 0.5, b)))
    col = mix('#7A1E14', '#18140E', clamp01(1 - d / w + 0.3))
    return col + (i,)


def paint_lightning(a, b):
    """Neutral lightning ribbon (face, a -0.25..0.25, b 0..1 along the bolt; tint green #9CF04A for the CS lightning):
    a jagged white bolt with one fork and a soft glow."""
    if b < 0 or b > 1:
        return CLEAR
    d = min(poly_dist(a, b, LIGHT_MAIN), poly_dist(a, b, LIGHT_FORK))
    core = math.exp(-(d / 0.014) ** 2)
    glow = 0.5 * math.exp(-(d / 0.07) ** 2)
    i = clamp01(max(core, glow))
    return (1.0, 1.0, 1.0, i) if i > 0.04 else CLEAR


_LI = random.Random(9)
LIGHT_MAIN = jag(_LI, 0.0, 0.0, 0.02, 1.0, 9, 0.09)
LIGHT_FORK = jag(_LI, LIGHT_MAIN[4][0], LIGHT_MAIN[4][1], 0.17, 0.82, 4, 0.12)


# ----------------------------------------------------------------------------- arena props (lush look, bank, gate)
def paint_water_tile(a, b):
    """The lake's water sheet (one 14 b tile; flat, seamless): teal water #70995F / #80B07E with darker root-vein lines
    #4F7F4D and white caustic glints #EDFBF0, about 40 % alpha (v5 §4.6 / v6w §4.5 'shallow water floor')."""
    x, y = (a + 0.5) * 4, (b + 0.5) * 4
    n = pfbm(x, y, 4, 3)
    c = abs(pfbm(x * 2 + 0.5, y * 2 + 0.25, 8, 2) - 0.5)
    caustic = math.exp(-(c / 0.03) ** 2)
    vein = abs(pfbm(x * 0.5 + 2.1, y * 0.5 + 1.3, 2, 2) - 0.5)
    col = mix('#70995F', '#80B07E', n)
    col = mix(col, '#4F7F4D', 0.6 * math.exp(-(vein / 0.02) ** 2))
    col = mix(col, '#EDFBF0', 0.75 * caustic)
    return col + (clamp01(0.34 + 0.08 * n + 0.25 * caustic),)


def paint_lily_pad(a, b):
    """Lily pad (flat, unit 0.5): a round green pad #4E8A3A / #7DB55A with a notch, radial veins and a light rim, a small
    yellow-white bud on half of them is the bulb_flower prop's job."""
    r = math.hypot(a, b) * 2
    th = math.atan2(a, b)
    if r > 1 or (abs(th) < 0.22 and r > 0.08):
        return CLEAR
    vein = 0.0
    for k in range(11):
        t = -math.pi + 0.3 + k * (2 * math.pi - 0.6) / 10
        vein = max(vein, math.exp(-(((th - t + math.pi) % (2 * math.pi) - math.pi) * r / 0.02) ** 2))
    n = fbm(a * 10, b * 10, 2)
    col = mix('#3E7A30', '#7DB55A', 0.35 + 0.4 * r + 0.25 * n)
    col = mix(col, '#B7DD8A', 0.55 * vein * r)
    if r > 0.93:
        col = mix(col, '#C9E89E', 0.7)
    return col + (1.0,)


def paint_bell_flower(a, b):
    """Yellow bell flower (cross, foot at b 0, unit height; a -0.25..0.25): a thin green stalk curving over with three
    hanging yellow bells #F2D45C / #FFF0A0 and two narrow leaves (v5 / v6 lush banks 'yellow bell flowers')."""
    if b < 0 or b > 1:
        return CLEAR
    sx = 0.06 * math.sin(b * 2.6)
    if abs(a - sx) < 0.012 and b < 0.9:
        return hexc('#5E8A2C') + (1.0,)
    for lx, ly, s in ((-0.04, 0.2, 1), (0.05, 0.35, -1)):
        m, e = leaf_shape((a - lx) * s / 0.12, (b - ly) / 0.18, 0.3)
        if m:
            return mix('#4E7A28', '#8CC050', e) + (1.0,)
    for bx, by in ((0.12, 0.84), (-0.1, 0.72), (0.16, 0.6)):
        dx, dy = a - bx, b - by
        if -0.07 < dy < 0.03 and abs(dx) < 0.045 + 0.4 * max(0.0, -dy) * 0.5:
            lit = clamp01(0.5 - dx * 6)
            return mix('#D9A82E', '#FFF0A0', lit) + (1.0,)
        if abs(dx) < 0.006 and 0.03 <= dy < 0.06:
            return hexc('#5E8A2C') + (1.0,)
    return CLEAR


def paint_bulb_flower(a, b):
    """Glowing bulb flower (cross, foot at b 0; a -0.25..0.25): a stalk with two broad leaves and a glowing lemon bulb
    #EFE45B / #FFF8C0 at the top with a soft glow (the arena's glowing bulbs, v1 §5.4)."""
    if b < 0 or b > 1:
        return CLEAR
    bx, by = 0.0, 0.74
    q = math.hypot((a - bx) / 0.13, (b - by) / 0.17)
    if q < 1:
        col = mix('#FFF8C0', '#DFD74C', q ** 1.5)
        return col + (1.0,)
    if q < 1.7:
        return hexc('#F4EE8A') + (0.4 * (1 - (q - 1) / 0.7) ** 2,)
    if abs(a) < 0.014 and b < 0.6:
        return hexc('#4E7A28') + (1.0,)
    for lx, s in ((-0.02, 1), (0.02, -1)):
        m, e = leaf_shape(s * (a - lx) / 0.2 * 0.7 + 0.0, (b - 0.22) / 0.2 * 1.0 - 0.0, 0.42)
        if m and s * (a - lx) > -0.02:
            return mix('#3E6E22', '#7DB04A', e) + (1.0,)
    return CLEAR


_BC = random.Random(12)
BANK_SPIKES = [(_BC.uniform(-0.3, 0.3), _BC.uniform(0.45, 1.0), _BC.uniform(-0.35, 0.35), _BC.uniform(0.07, 0.12))
               for _ in range(6)]


def _crystal(a, b, spikes, lit, mid, shade, edge):
    best = CLEAR
    for x0, h, lean, w in spikes:
        if b < 0 or b > h:
            continue
        t = b / h
        cx = x0 + lean * t * h * 0.5
        hw = w * (1 - t ** 1.15)
        d = a - cx
        if abs(d) < hw:
            facet = d < 0
            col = mix(mid, lit, 0.5 + 0.5 * t) if facet else mix(shade, mid, t)
            if abs(d) > hw - 0.012 or abs(d) < 0.006:
                col = hexc(edge)
            best = col + (1.0,)
    return best


def paint_bank_crystal(a, b):
    """Gold crystal spikes on the bank (cross, foot at b 0, unit height; a -0.5..0.5): six leaning faceted spikes, lit
    #FFF1B0, mid #EBC55A, shade #B07A1E, bright edges #FFFBE0 (the arena's gold crystals, brightness 15)."""
    return _crystal(a, b, BANK_SPIKES, '#FFF1B0', '#EBC55A', '#B07A1E', '#FFFBE0')


GATE_SPIKES = [(0.0, 1.0, 0.0, 0.16), (-0.18, 0.62, -0.3, 0.1), (0.2, 0.7, 0.28, 0.11), (-0.06, 0.45, -0.5, 0.07),
               (0.1, 0.4, 0.55, 0.07)]


def paint_gate_crystal(a, b):
    """Gold-green gate crystal (the chapter-3 entrance, ≈ 1.5 b; cross, foot at b 0): a tall central spike with four
    side spikes, lit #F4FBC8, mid #C9D86A, shade #6E8A2A, edges #FFFFE8 (the oasis gold-green)."""
    return _crystal(a, b, GATE_SPIKES, '#F4FBC8', '#C9D86A', '#6E8A2A', '#FFFFE8')


# ----------------------------------------------------------------------------- HUD glyphs (x right, y up, -1..1)
def glyph_apep(x, y):
    """Apep badge: a lemon-shaped Heart seed #EFE45B with a leaf crown, on a dark green disc with a gold ring."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    if r > 0.88:
        return hexc('#10200A') + (1.0,)
    if r > 0.78:
        return mix('#EBC55A', '#B07A1E', (r - 0.78) / 0.1) + (1.0,)
    q = math.hypot(x / 0.36, (y + 0.08) / 0.48)
    if q < 1:
        lit = clamp01(0.6 - 0.5 * x + 0.4 * y)
        return mix('#DFD74C', '#FFF8C0', lit) + (1.0,)
    if q < 1.18:
        return hexc('#2A3A10') + (1.0,)
    for s in (-1, 1):
        m, e = leaf_shape((x - s * 0.22) * s / 0.3, (y - 0.5) / 0.28, 0.42)
        if m:
            return mix('#4E8A1E', '#A6D45A', e) + (1.0,)
    return mix('#24401A', '#16280E', r) + (1.0,)


def make_glyph_diamond(hexcol):
    def g(x, y):
        m = abs(x) + abs(y)
        if m > 0.95:
            return CLEAR
        if m > 0.78:
            return hexc('#141008') + (1.0,)
        lit = clamp01(0.55 - 0.45 * x + 0.45 * y)
        return mix(mix(hexcol, '#000000', 0.25), mix(hexcol, '#FFFFFF', 0.45), lit) + (1.0,)
    g.__doc__ = 'Special-organism badge: a faceted diamond (tinted white so the text colour sets it).'
    return g


def glyph_warn(x, y):
    """⚠ small: a gold-white triangle with a dark '!' (the failure-strike mark on the sub-line)."""
    if y < -0.8 or y > 0.9:
        return CLEAR
    hw = (0.9 - y) / 1.7 * 0.98
    if abs(x) > hw:
        return CLEAR
    inner = abs(x) < hw - 0.16 and y > -0.64 and y < 0.68
    if not inner:
        return hexc('#2A1A08') + (1.0,)
    if abs(x) < 0.09 and (-0.12 < y < 0.42 or -0.5 < y < -0.3):
        return hexc('#2A1A08') + (1.0,)
    return mix('#F2C24A', '#FFF1B0', clamp01(0.5 + y * 0.5)) + (1.0,)


def glyph_fail_small(x, y):
    """Small withered-Heart badge (failure strikes): a grey-olive seed #8A8458 with a dark crack."""
    q = math.hypot(x / 0.55, y / 0.78)
    if q > 1:
        return CLEAR
    if q > 0.85:
        return hexc('#1E1C0A') + (1.0,)
    if seg_dist(x, y, -0.05, 0.6, 0.12, 0.05) < 0.07 or seg_dist(x, y, 0.12, 0.05, -0.08, -0.5) < 0.07:
        return hexc('#2A2610') + (1.0,)
    return mix('#6E6A40', '#B0A870', clamp01(0.5 - 0.4 * x + 0.4 * y)) + (1.0,)


def glyph_t_heart(x, y):
    """Title glyph 'heart': the golden Heart seed with a leaf crown and a halo (T1 「오아시스의 심장」)."""
    r = math.hypot(x, y)
    q = math.hypot(x / 0.5, (y + 0.1) / 0.68)
    if q < 1:
        lit = clamp01(0.55 - 0.5 * x + 0.45 * y)
        col = mix('#D8C43A', '#FFF8C0', lit)
        for k in range(3):
            if abs(x - (k - 1) * 0.22 * (1 - abs(y + 0.1))) < 0.025 and q < 0.92:
                col = mix(col, '#B89A22', 0.5)
        return col + (1.0,)
    if q < 1.12:
        return hexc('#3A3410') + (1.0,)
    for s in (-1, 1):
        m, e = leaf_shape((x - s * 0.3) * s / 0.36, (y - 0.68) / 0.3, 0.42)
        if m:
            return mix('#4E8A1E', '#A6D45A', e) + (1.0,)
    if r < 1:
        return hexc('#FFF4C8') + (0.3 * (1 - r) ** 2,)
    return CLEAR


def glyph_t_warn(x, y):
    """Title glyph 'warn': a big '!' in an amber-red ring (the time-out warning)."""
    r = math.hypot(x, y)
    if r > 0.95:
        return CLEAR
    if r > 0.8:
        return hexc('#C36E5A') + (1.0,)
    if r > 0.72:
        return hexc('#2A0E08') + (1.0,)
    if abs(x) < 0.12 and (-0.05 < y < 0.58 or -0.5 < y < -0.24):
        return hexc('#FFF1D0') + (1.0,)
    if abs(x) < 0.19 and (-0.12 < y < 0.65 or -0.57 < y < -0.17):
        return hexc('#2A0E08') + (1.0,)
    return hexc('#5A1E14') + (0.55,)


def glyph_t_fail(x, y):
    """Title glyph 'fail': the withered Heart, a grey-olive seed #8A8458 cracked through, drooping dead leaves."""
    q = math.hypot(x / 0.5, (y + 0.1) / 0.68)
    if q < 1:
        if seg_dist(x, y, -0.06, 0.52, 0.12, 0.05) < 0.05 or seg_dist(x, y, 0.12, 0.05, -0.08, -0.55) < 0.05:
            return hexc('#2A2610') + (1.0,)
        return mix('#6E6A40', '#B0A870', clamp01(0.5 - 0.5 * x + 0.4 * y)) + (1.0,)
    if q < 1.12:
        return hexc('#1E1C0A') + (1.0,)
    for s in (-1, 1):
        m, e = leaf_shape((x - s * 0.42) * s / 0.3, -(y - 0.45) / 0.3, 0.4)
        if m:
            return mix('#4A4420', '#8A7E3A', e) + (1.0,)
    return CLEAR


def glyph_t_success(x, y):
    """Title glyph 'success': the green revived Heart #9CF04A / #E6FFB0 with a bright crown and a halo."""
    r = math.hypot(x, y)
    q = math.hypot(x / 0.5, (y + 0.1) / 0.68)
    if q < 1:
        lit = clamp01(0.55 - 0.5 * x + 0.45 * y)
        return mix('#5EB82A', '#E6FFB0', lit) + (1.0,)
    if q < 1.12:
        return hexc('#183008') + (1.0,)
    for s in (-1, 0, 1):
        m, e = leaf_shape((x - s * 0.3) / 0.3, (y - 0.72 + 0.08 * abs(s)) / 0.28, 0.42)
        if m:
            return mix('#4E8A1E', '#F1FFD2', e) + (1.0,)
    if r < 1:
        return hexc('#E6FFB0') + (0.4 * (1 - r) ** 2,)
    return CLEAR


def glyph_dome(x, y):
    """The dome glyph for the 종말의 여파 banner: a lime half-dome with a sprout, white rim, dark outline."""
    yy = y + 0.5
    if yy < -0.12:
        return CLEAR
    r = math.hypot(x, yy)
    if yy >= 0 and r < 0.84:
        if r > 0.72:
            return hexc('#F5FFD4') + (1.0,)
        if abs(x) < 0.05:
            return hexc('#F5FFD4') + (0.9,)
        return mix('#88BB5F', '#B5DA72', yy) + (0.95,)
    if -0.12 <= yy < 0 and abs(x) < 0.96:
        return hexc('#E4F69D') + (1.0,)
    if yy >= 0 and r < 0.96:
        return hexc('#14200A') + (1.0,)
    if seg_dist(x, y, 0.0, 0.34, 0.0, 0.62) < 0.07:
        return hexc('#A6D45A') + (1.0,)
    return CLEAR


def glyph_vignette(x, y):
    """Edge flash (flash_hit): transparent centre, a soft white-gold border."""
    e = max(abs(x), abs(y))
    t = smooth(0.72, 1.0, e)
    return hexc('#FFF4C8') + (0.38 * t,)


def pixel_cell(state):
    """Heart progress bar cell (the FN-24 fallback bar), 4 x 8 px RGBA rows: 0 empty (dim olive #4A4220), 1 full (gold
    #EDCF63 with a light top row and a darker base), 2 the left cap and 3 the right cap (a 1 px dark outline column
    with the top / bottom outline); every cell has the dark top and bottom outline, so cells abut into one bar."""
    w, h = 4, 8
    out = hexc('#2A2008')
    rows = []
    for j in range(h):
        row = []
        for i in range(w):
            edge = j in (0, h - 1)
            if state in (2, 3):
                col_on = (i == w - 1) if state == 2 else (i == 0)
                row.append(out + (1.0,) if col_on or (edge and ((state == 2 and i == w - 1) or (state == 3 and i == 0)))
                           else CLEAR)
                continue
            if edge:
                row.append(out + (1.0,))
            elif state == 1:
                row.append((hexc('#FFF2B0') if j == 1 else hexc('#EDCF63') if j < 5 else hexc('#C9A43A')) + (1.0,))
            else:
                row.append(hexc('#4A4220') + (0.85,))
        rows.append(row)
    return w, h, rows
