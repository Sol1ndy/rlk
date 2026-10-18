"""Painted sprites of the Moonlit Butterfly's fx kit (tools/build_mboss_bf_fx.py). Stdlib only.

Every painter takes card coordinates (a, b) inside its kind's painter box and returns straight-alpha
(r, g, b, alpha) floats. Card coordinates follow Navia's cards (tools/build_navia_fx_cards.py): +a is the card's
local -x (the player's right when seen from behind or from above), +b is up (face cards) or forward (flat cards).
Colours are the hex values sampled from the reference videos (scratchpad mb2/understand/v1-v4.md).

Neutral sprites (white or near-white) are meant to be tinted per spawn: the item definitions carry a
minecraft:custom_model_data tint (default white), which multiplies the texture colour.
"""
import math
import random


def hexc(h):
    return tuple(int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))


def clamp01(x):
    return 0.0 if x < 0 else 1.0 if x > 1 else x


def mix(a, b, t):
    t = clamp01(t)
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

# ----------------------------------------------------------------------------- value noise
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


def star4(a, b, length, width):
    """4-point star intensity (0..1) with rays along the card axes."""
    def ray(u, v):
        f = 1 - abs(u) / length
        if f <= 0:
            return 0.0
        return f ** 1.4 * math.exp(-(v / (width * f + 0.012)) ** 2)
    return max(ray(a, b), ray(b, a))


# ----------------------------------------------------------------------------- crescents
CRES_SPAN = 80.0      # half-angle of the arc, degrees either side of forward (as Navia's crescent)

PAL_LIME = rmp((0, '#FBFFF2'), (0.07, '#EDF9DA'), (0.18, '#E5FBC8'), (0.30, '#D7F899'), (0.45, '#C1F788'),
               (0.60, '#AEE08B'), (0.74, '#8DCA85'), (0.86, '#4BA2A5'), (1.0, '#2E647D'))
UNDER_LIME = hexc('#297272')
PAL_CYAN = rmp((0, '#FFFFFF'), (0.08, '#F9FDFC'), (0.22, '#E2FAF4'), (0.38, '#BAF3E3'), (0.55, '#8EE2DA'),
               (0.70, '#78D8D1'), (0.85, '#39B4C1'), (1.0, '#22788F'))
UNDER_CYAN = hexc('#1E5F7A')
PAL_FIRE = rmp((0, '#FFFBEA'), (0.07, '#FDF6DC'), (0.17, '#F9E38E'), (0.30, '#F8D486'), (0.44, '#F4BA33'),
               (0.58, '#EB9F26'), (0.70, '#ED7C59'), (0.82, '#CC6976'), (1.0, '#A26A7A'))
UNDER_FIRE = hexc('#C680A2')


def _blades(seed, n, lo, hi):
    """leaf blades / shards / flame licks along the arc: (centre angle, length, half width, tilt deg)"""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        c = -CRES_SPAN * 0.85 + (k + rnd.uniform(0.15, 0.85)) * 1.7 * CRES_SPAN / n
        out.append((c, rnd.uniform(lo, hi), rnd.uniform(0.022, 0.04), rnd.uniform(18, 40)))
    return out


_BL = {1: _blades(11, 7, 0.14, 0.26), 2: _blades(12, 7, 0.12, 0.22), 3: _blades(13, 11, 0.06, 0.14)}


def _lens(px, py, ox, oy, ux, uy, length, hw):
    """inside a lens (leaf / shard) from (ox, oy) along unit (ux, uy): returns (u 0..1, |v|/width) or None"""
    dx, dy = px - ox, py - oy
    u = (dx * ux + dy * uy) / length
    if u <= 0 or u >= 1:
        return None
    v = abs(-dx * uy + dy * ux)
    w = hw * math.sin(math.pi * u ** 0.8) ** 0.9
    if v >= w:
        return None
    return u, v / w


def crescent(a, b, pal, under, seed, mode):
    """Energy slash crescent in the swing plane (Navia's shape: pivot = card origin, head at -a, tail fading to
    +a): a white-hot outer edge, a streaked translucent body, a darker underlay ribbon inside, and per mode
    leaf blades (lime), crystal shards (cyan) or flame licks on the outer edge (fire)."""
    r = math.hypot(a, b)
    if r < 0.30 or r > 1.0:
        return CLEAR
    phi = math.degrees(math.atan2(a, b))              # 0 forward, + toward +a (right)
    s = (CRES_SPAN - phi) / (2 * CRES_SPAN)           # 0 tail (right) .. 1 head (left)
    if s <= -0.02 or s >= 1:
        return CLEAR
    sc = min(max(s, 0.0), 1.0)
    n = fbm(phi * 0.06 + seed * 13.1, r * 6.0 + seed, 3)
    ro = 0.965 - 0.025 * (1 - sc)
    thick = 0.30 * math.sin(math.pi * sc ** 1.25) ** 0.75 + 0.003
    lick = 0.0
    if mode == 'fire':
        for c, ln, hw, tilt in _BL[seed]:
            d = phi - c                                   # + toward the tail
            lead, trail = hw * 90, hw * 260               # licks lean back toward the tail
            if -lead < d < trail:
                f = 1 - (-d / lead if d < 0 else d / trail)
                lick = max(lick, ln * f ** 1.6 * math.sin(math.pi * sc) ** 0.6)
    ri = ro - thick
    blade = None
    if mode in ('lime', 'cyan'):
        for c, ln, hw, tilt in _BL[seed]:
            if not (0.08 < (CRES_SPAN - c) / (2 * CRES_SPAN) < 0.97):
                continue
            t = math.radians(c)
            rr = ro - thick * 0.55
            ox, oy = rr * math.sin(t), rr * math.cos(t)
            ang = t + math.pi + math.radians(tilt)       # inward, leaning toward the tail
            hit = _lens(a, b, ox, oy, math.sin(ang), math.cos(ang), ln, hw * (1.3 if mode == 'cyan' else 1.0))
            if hit:
                blade = hit
                break
    if blade:
        u, v = blade
        if v > 0.72:
            return under + (0.95,)
        col = ramp(pal, 0.25 + 0.35 * u) if mode == 'lime' else ramp(pal, 0.1 + 0.3 * u)
        if mode == 'cyan' and v < 0.25:
            col = mix(col, WHITE, 0.6)
        return col + (0.95,)
    if r > ro + lick or r < ri:
        return CLEAR
    w = (ro - r) / thick                              # 0 outer edge .. 1 inner edge (< 0 inside a flame lick)
    if w < 0:
        k = clamp01(-w * thick / max(lick, 1e-3))     # 0 at the edge .. 1 at the lick tip
        col = ramp(rmp((0, '#FDF6DC'), (0.35, '#F9E38E'), (0.7, '#F4BA33'), (1, '#ED7C59')), k)
        return col + (clamp01(0.95 - 0.5 * k ** 2) * smooth(-0.02, 0.42, s),)
    stripes = math.sin(w * 31.0 + 6.0 * fbm(phi * 0.03 + seed, w * 2.0, 2))
    stripes = stripes * stripes
    col = ramp(pal, clamp01(w * 0.95 + (n - 0.5) * 0.16))
    col = mix(col, WHITE, 0.18 * stripes * (1 - w))
    if w > 0.74:
        col = mix(col, under, smooth(0.74, 1.0, w) * 0.85)
    if w < 0.10:
        alpha = 1.0
    else:
        alpha = 0.50 + 0.38 * stripes + 0.12 * (1 - w)
        if w > 0.74:
            alpha = max(alpha, 0.78)
    alpha *= smooth(-0.02, 0.42, s)                   # the tail fades out
    alpha *= 0.30 + 0.70 * smooth(0.30, 0.62, n + s * 0.75)   # and breaks up into streaks
    return col + (clamp01(alpha),)


def paint_cres_lime(a, b):
    """Lime kick / vacuum-blade crescent: #EDF9DA core, #D7F899 / #BFF191 body, teal #297272 underlay (v1 §5)."""
    return crescent(a, b, PAL_LIME, UNDER_LIME, 1, 'lime')


def paint_cres_cyan(a, b):
    """Cyan-white crescent: cocoon burst / wind crescents, #F9FDFC / #BAF3E3 / #78D8D1 / #39B4C1 (v1 §5)."""
    return crescent(a, b, PAL_CYAN, UNDER_CYAN, 2, 'cyan')


def paint_cres_fire(a, b):
    """Fire crescent / flame sheet: gold #F9E38E / #F8D486 to orange #EB9F26 to magenta #CC6976 / #C680A2 rims
    (v3 §5 날개탄)."""
    return crescent(a, b, PAL_FIRE, UNDER_FIRE, 3, 'fire')


def paint_fire_claw(a, b):
    """Camera-facing fire crescent projectile: a golden claw / feather 'C' (opening right) with flame licks on its
    back and a soft glow, so it reads from every side (v3 k_f0309)."""
    cx, cy, R = 0.22, 0.0, 0.58
    dx, dy = a - cx, b - cy
    rr = math.hypot(dx, dy)
    th = math.degrees(math.atan2(dy, dx)) % 360               # 180 = left
    u = (th - 95) / 170                                       # 0 top end .. 1 bottom end (arc on the left)
    glow = 0.0
    if 0 < u < 1:
        n = fbm(th * 0.05, rr * 6, 3)
        t = 0.28 * math.sin(math.pi * u) ** 0.8 + 0.01
        ro = R + t * 0.5 + 0.10 * n * math.sin(math.pi * u)  # flame licks on the convex (outer) side
        ri = R - t * 0.5
        if ri <= rr <= ro:
            w = (ro - rr) / (ro - ri)                         # 0 outer .. 1 inner
            col = ramp(rmp((0, '#ED7C59'), (0.18, '#F4BA33'), (0.42, '#F9E38E'), (0.62, '#FFFBEA'),
                           (0.82, '#F8D486'), (1.0, '#CC6976')), w)
            al = 0.9 + 0.1 * math.sin(w * 9 + n * 5)
            if w < 0.18:
                al *= 0.55 + 0.45 * smooth(0.0, 0.18, w)
            return col + (clamp01(al),)
        glow = 0.42 * math.exp(-((rr - R) / 0.2) ** 2) * math.sin(math.pi * u) ** 0.6
    if glow < 0.02:
        return CLEAR
    return ramp(rmp((0, '#ED7C59'), (0.5, '#F4BA33'), (1, '#F9E38E')), glow * 2) + (glow * 0.8,)


# ----------------------------------------------------------------------------- flares, glints, bursts
def paint_star4(a, b):
    """Lime 4-point star flare with a white core and faint diagonal rays (v2 tell glint, v3/v4 release flare
    #F8FCE7 / #D8F2BC / #AEE76F)."""
    r = math.hypot(a, b)
    i = star4(a, b, 0.98, 0.07)
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(i, 0.5 * star4(d1, d2, 0.45, 0.045))
    i = max(i, math.exp(-(r / 0.12) ** 2))
    halo = 0.30 * math.exp(-(r / 0.42) ** 2)
    col = ramp(rmp((0, '#7EC866'), (0.25, '#9ADB6A'), (0.45, '#AEE76F'), (0.65, '#D8F2BC'), (0.82, '#F8FCE7'),
                   (1, '#FFFFFF')), max(i, halo))
    return col + (clamp01(max(i * 1.3, halo)),)


def paint_glint(a, b):
    """Neutral white 4-point glint (sparkles; tint gold, cyan or lime)."""
    r = math.hypot(a, b)
    i = max(star4(a, b, 0.98, 0.08), math.exp(-(r / 0.14) ** 2))
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(i, 0.45 * star4(d1, d2, 0.4, 0.05))
    halo = 0.22 * math.exp(-(r / 0.35) ** 2)
    v = 0.88 + 0.12 * i
    return (v, v, v, clamp01(max(i * 1.3, halo)))


BURST_SPIKES = ((8, 0.98, 0.115), (98, 0.94, 0.11), (188, 0.97, 0.115), (278, 0.92, 0.11),
                (52, 0.70, 0.085), (143, 0.66, 0.08), (233, 0.72, 0.085), (322, 0.64, 0.08),
                (30, 0.46, 0.06), (120, 0.50, 0.06), (208, 0.44, 0.06), (300, 0.48, 0.06),
                (75, 0.36, 0.05), (255, 0.38, 0.05), (170, 0.55, 0.06), (350, 0.58, 0.065))


def paint_burst(a, b):
    """Lime-white spiky starburst (kick impacts, orb bursts, cocoon burst core): #FBFDF4 core, #E4F8CC / #C1F59D
    spikes, #A2ECA3 fringe (v1 §5, v2 dash burst)."""
    r = math.hypot(a, b)
    phi = math.atan2(a, b)
    inside, edge = 0.0, 1.0
    for deg, length, w0 in BURST_SPIKES:
        if r >= length:
            continue
        dphi = (phi - math.radians(deg) + math.pi) % (2 * math.pi) - math.pi
        if abs(dphi) > math.pi / 2:
            continue
        perp = r * math.sin(abs(dphi))
        w = w0 * (1 - r / length) + 0.004
        if perp < w:
            inside = 1.0
            edge = min(edge, (w - perp) / w)
    if r < 0.2 or inside:
        col = ramp(rmp((0, '#74E542'), (0.25, '#A2ECA3'), (0.45, '#C1F59D'), (0.68, '#E4F8CC'), (0.82, '#FBFDF4'),
                       (1, '#FFFFFF')), 1 - r)
        if r >= 0.2 and edge < 0.25:
            col = mix(col, hexc('#5DBE3A'), (0.25 - edge) / 0.25 * 0.5)
        return col + (1.0,)
    haze = 0.4 * math.exp(-(r / 0.38) ** 2)
    return mix(hexc('#C1F59D'), hexc('#F2FDE2'), haze) + (haze,)


def paint_glow(a, b):
    """Neutral soft glow disc (flashes, ground glow, core glow); tint it."""
    r = math.hypot(a, b)
    if r >= 1:
        return CLEAR
    v = 0.9 + 0.1 * (1 - r)
    return (v, v, v, 0.95 * (1 - r) ** 1.4)


def paint_mote(a, b):
    """Neutral moonlight mote: a soft dot with a faint cross glint (tint lime, cyan or gold)."""
    r = math.hypot(a, b)
    i = max(math.exp(-(r / 0.28) ** 2), 0.55 * star4(a, b, 0.95, 0.06))
    halo = 0.35 * math.exp(-(r / 0.6) ** 2)
    return (1.0, 1.0, 1.0, clamp01(max(i * 1.2, halo)))


def paint_streak(a, b):
    """Neutral long thin streak tapered at both ends (the cyan X glint, slash and speed lines)."""
    t = abs(a)
    if t >= 1:
        return CLEAR
    hw = (1 - t ** 2.2) + 0.02
    core = math.exp(-(b / (0.30 * hw)) ** 2)
    halo = 0.45 * math.exp(-(b / (0.9 * hw)) ** 2)
    i = max(core, halo) * (1 - t ** 8)
    v = 0.85 + 0.15 * core
    return (v, v, v, clamp01(i * 1.2))


def paint_leaf(a, b):
    """Neutral leaf / petal flake (tint lime for drifting leaves, amber for the embers after the blast)."""
    t = (b + 0.92) / 1.84
    if t <= 0 or t >= 1:
        return CLEAR
    half = 0.48 * math.sin(math.pi * t ** 0.8) ** 0.9
    x = a - 0.12 * math.sin(math.pi * t)
    m = half - abs(x)
    if m <= 0:
        return CLEAR
    if m < 0.06:
        return (0.62, 0.64, 0.6, 1.0)
    if abs(x) < 0.05 and 0.1 < t < 0.85:
        return (1.0, 1.0, 1.0, 1.0)
    v = 0.78 + 0.2 * t + 0.06 * (1 if x < 0 else -1)
    return (v, v, v * 0.97, 1.0)


def paint_bfly(a, b):
    """Neutral small butterfly outline glyph (floats around her during 달빛 해제, v3 zoom_f2022; tint lime)."""
    best = 9.0
    inside = False
    for sx in (-1, 1):
        for (cx, cy, rx, ry, rot) in ((0.42, 0.28, 0.42, 0.30, 35), (0.32, -0.36, 0.28, 0.22, -30)):
            x, y = sx * a - cx, b - cy
            t = math.radians(rot)
            u, v = x * math.cos(t) + y * math.sin(t), -x * math.sin(t) + y * math.cos(t)
            d = math.hypot(u / rx, v / ry)
            best = min(best, abs(d - 1) * min(rx, ry))
            inside = inside or d < 1
    body = abs(a) < 0.05 and abs(b) < 0.5
    if best < 0.035 or body:
        return (1.0, 1.0, 1.0, 1.0)
    if inside:
        return (0.92, 0.96, 0.9, 0.22)
    return CLEAR


# ----------------------------------------------------------------------------- rings, discs, spheres
def paint_disc_lime(a, b):
    """Dendro disc ('풀 원판', H2): flat glowing lime disc with a bright rim and a swirl (v1: rim #C2ECB0, fill
    #A6E282 / #84C75D, core #F5FCE8)."""
    r = math.hypot(a, b)
    if r >= 1:
        return CLEAR
    th = math.atan2(b, a)
    n = fbm(a * 3 + 5, b * 3 + 5, 3)
    sw = 0.5 + 0.5 * math.sin(3 * th + r * 10.0 + n * 4)
    if r > 0.955:
        g = (1 - r) / 0.045
        return hexc('#C2ECB0') + (0.5 * g,)
    if r > 0.84:
        w = abs(r - 0.9) / 0.06
        col = mix(hexc('#F5FCE8'), hexc('#C2ECB0'), w)
        return col + (1.0,)
    if r > 0.81:
        return hexc('#4E9A3C') + (0.9,)
    col = mix(hexc('#84C75D'), hexc('#A6E282'), sw * 0.9)
    col = mix(col, hexc('#F5FCE8'), math.exp(-(r / 0.16) ** 2))
    col = mix(col, hexc('#C2ECB0'), smooth(0.6, 0.81, r) * 0.5)
    return col + (0.72 + 0.2 * sw,)


def paint_ripple(a, b):
    """Near-white ripple / wind ring (transformation ripples #D0F2B9 / #BDE592, wind crescents #E4F8CC,
    shock rings); tint it."""
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


def paint_gyro(a, b):
    """Lime gyroscope ring (orb rings, the 달빛 해제 ring cage): #DCFA9A core line, #ADE87F / #91CF7E body,
    #26666A dark edges, two brighter spinning arcs and four beads (v3 k_f2133, v4 k_f0372)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    for k in range(4):
        bx, by = 0.9 * math.cos(k * math.pi / 2 + math.pi / 4), 0.9 * math.sin(k * math.pi / 2 + math.pi / 4)
        d = math.hypot(a - bx, b - by)
        if d < 0.05:
            return (mix(hexc('#F2FDE2'), hexc('#91CF7E'), d / 0.05) + (1.0,)) if d < 0.038 else hexc('#26666A') + (1.0,)
    d = abs(r - 0.9)
    lead = max(math.cos(th - 0.5), math.cos(th - 0.5 - math.pi)) ** 9
    if d < 0.03:
        if d > 0.021:
            return hexc('#26666A') + (0.95,)
        col = mix(hexc('#ADE87F'), hexc('#DCFA9A'), 1 - d / 0.021)
        col = mix(col, hexc('#F2FDE2'), lead * 0.8)
        return col + (1.0,)
    if 0.80 < r < 0.84 and (math.degrees(th) % 15) < 1.6:
        return hexc('#91CF7E') + (0.6,)
    g = 0.38 * math.exp(-(d / 0.07) ** 2) * (0.6 + 0.4 * lead)
    if g < 0.02:
        return CLEAR
    return hexc('#91CF7E') + (g,)


def paint_sphere(a, b):
    """Light sphere (transformation r 2.5, flash shells): translucent, limb-brightened, white-yellow core
    #F8FDBB / #FAFCD4 / #EFFDA2, rim #CFF489 (v2 k_f1464)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.955:
        return hexc('#CFF489') + (0.35 * (1 - r) / 0.045,)
    limb = smooth(0.45, 0.95, r)
    rim = math.exp(-((r - 0.93) / 0.02) ** 2)
    band = math.exp(-((b - 0.3 * math.sin(2.4 * a + 0.5)) / 0.08) ** 2) * (1 - r ** 3)
    core = math.exp(-(r / 0.33) ** 2)
    col = ramp(rmp((0, '#FAFCD4'), (0.4, '#F8FDBB'), (0.75, '#EFFDA2'), (1, '#CFF489')), limb)
    col = mix(col, WHITE, max(rim, core * 0.8, band * 0.5))
    alpha = 0.2 + 0.55 * limb ** 2 + 0.35 * rim + 0.3 * core + 0.2 * band
    return col + (clamp01(alpha),)


def paint_dome(a, b, hi):
    """Dome shell segment (달빛 해제 lime dome r 10): translucent lime #77D04C / #9FED6B with swirling wind bands
    #C2F999 and a bright ground band #F1FDD9 / #C9F899 (v3 k_f2182, v4 k_f0476). Trapezoid mask so that 8 per
    band close the dome; hi = the upper band (narrow top)."""
    v = (b + 1) / 2                                         # 0 bottom .. 1 top of the card
    hw = (1.0 + (0.78 - 1.0) * v) if not hi else (0.80 + (0.20 - 0.80) * v)
    if abs(a) > hw:
        return CLEAR
    edge = smooth(0.0, 0.12, (hw - abs(a)) / hw)
    n = fbm(a * 2.2 + (7 if hi else 0), b * 2.2, 3)
    sw = math.sin((a * 1.4 + b * 2.4) * 4.2 + n * 5.0)
    band = smooth(0.82, 0.98, sw)
    col = mix(hexc('#77D04C'), hexc('#9FED6B'), 0.3 + 0.7 * n)
    col = mix(col, hexc('#C2F999'), band)
    alpha = 0.30 + 0.12 * n + 0.32 * band
    if not hi:
        g = smooth(0.16, 0.0, v)
        col = mix(col, ramp(rmp((0, '#F1FDD9'), (1, '#C9F899')), v / 0.16), g)
        alpha = max(alpha, 0.85 * g)
    else:
        top = smooth(0.7, 1.0, v)
        col = mix(col, hexc('#C9F899'), top * 0.6)
        alpha = alpha * (1 - 0.5 * smooth(0.9, 1.0, v)) + 0.15 * top
    return col + (clamp01(alpha * edge),)


def paint_dome_lo(a, b):
    return paint_dome(a, b, False)


def paint_dome_hi(a, b):
    return paint_dome(a, b, True)


# ----------------------------------------------------------------------------- fire
FIRE_RAMP = rmp((0, '#8C5436'), (0.15, '#A46076'), (0.32, '#ED7C59'), (0.5, '#F88F39'), (0.68, '#F09A5F'),
                (0.82, '#F7CC9C'), (0.92, '#F9E38E'), (1, '#FDF6DC'))


def paint_fan_fire(a, b):
    """180-degree flame fan sheet on the floor (날개 휩쓸개 eruption footprint): scorched centre #585542 with
    #EDC30B embers, orange #F88F39 / #F09A5F tongues, #F7CC9C front, magenta-mauve #A46076 rims (v3 k_f0785)."""
    if b < 0:
        return CLEAR
    r = math.hypot(a, b)
    if r >= 1:
        return CLEAR
    phi = math.degrees(math.atan2(a, b))
    n = fbm(phi * 0.06 + 3, r * 2.5, 3)
    rf = 0.80 + 0.17 * fbm(phi * 0.11, 1.7, 2)
    if r > rf:
        g = 0.4 * math.exp(-((r - rf) / 0.05) ** 2)
        return hexc('#A46076') + (g,) if g > 0.03 else CLEAR
    u = r / rf
    tongue = fbm(phi * 0.20, r * 1.6 - 0.3, 3)
    if u < 0.28:
        col = mix(hexc('#3E3A2C'), hexc('#585542'), u / 0.28)
        if vnoise(a * 22, b * 22) > 0.78:
            col = hexc('#EDC30B')
        return col + (0.55 + 0.3 * u,)
    t = (u - 0.28) / 0.72
    col = ramp(FIRE_RAMP, clamp01(0.25 + 0.75 * t * (0.6 + 0.6 * tongue)))
    if u > 0.93:
        col = mix(col, hexc('#A46076'), (u - 0.93) / 0.07)
    alpha = 0.7 + 0.3 * tongue
    return col + (clamp01(alpha),)


def paint_flame_tongue(a, b):
    """One vertical flame tongue (pivot at its root): yellow-white core, orange body, magenta edges, dark base
    (날개 휩쓸개 flame wall, landing flame streaks, v3 §5)."""
    if b <= 0 or b >= 1:
        return CLEAR
    x0 = 0.22 * math.sin(b * 5.5 + 0.7) * b
    hw = 0.92 * (1 - b) ** 0.75 * (0.55 + 0.45 * math.sin(math.pi * min(1.0, b * 2.4 + 0.25)))
    n = fbm(a * 3 + 1, b * 4, 3)
    hw *= 0.85 + 0.3 * n
    d = abs(a - x0)
    if d > hw:
        return CLEAR
    u = d / hw
    col = ramp(FIRE_RAMP, clamp01(1.0 - u * 0.75 - b * 0.35 + (n - 0.5) * 0.2))
    if u > 0.78:
        col = mix(col, hexc('#C680A2'), (u - 0.78) / 0.22)
    if b < 0.07:
        col = mix(col, hexc('#8C5436'), (0.07 - b) / 0.07 * 0.6)
    alpha = (1 - 0.35 * u) * (1 - smooth(0.8, 1.0, b))
    return col + (clamp01(alpha),)


def paint_flame_puff(a, b):
    """Soft flame puff (the low glide's flame trail, landing splashes)."""
    r = math.hypot(a, b)
    th = math.atan2(b, a)
    re = 0.72 + 0.22 * fbm(math.cos(th) * 1.5 + 2, math.sin(th) * 1.5 + 2, 3)
    if r > re:
        return CLEAR
    u = r / re
    n = fbm(a * 3, b * 3, 2)
    col = ramp(FIRE_RAMP, clamp01(1.0 - u * 0.6 + (n - 0.5) * 0.25))
    if u > 0.8:
        col = mix(col, hexc('#C680A2'), (u - 0.8) / 0.2)
    return col + (clamp01((1 - u ** 2) * (0.75 + 0.25 * n)),)


# ----------------------------------------------------------------------------- blades and shards
def paint_blade(a, b):
    """Radial ground blade (orb burst, ground wave): a curved V / leaf blade rising from its root, #B4EB68 /
    #80BD77 facets, #EAFDD9 tip and midrib, #2C686D / #356F64 dark edges (v3 k_f1373)."""
    if b <= 0 or b >= 1:
        return CLEAR
    hw = 0.95 * (b / 0.32) ** 0.7 if b < 0.32 else 0.95 * ((1 - b) / 0.68) ** 0.95
    x0 = 0.25 * b * b
    u = (a - x0) / max(hw, 1e-6)
    if abs(u) >= 1:
        return CLEAR
    if abs(u) > 0.80:
        return mix(hexc('#356F64'), hexc('#2C686D'), (abs(u) - 0.8) / 0.2) + (1.0,)
    if abs(u) < 0.08 and b > 0.1:
        return mix(hexc('#D6F5A8'), hexc('#EAFDD9'), b) + (1.0,)
    col = hexc('#B4EB68') if u < 0 else hexc('#80BD77')
    col = mix(col, hexc('#EAFDD9'), smooth(0.7, 1.0, b) * 0.8)
    col = mix(col, hexc('#4E8C55'), smooth(0.25, 0.0, b) * 0.5)
    return col + (1.0,)


def paint_shard(a, b):
    """White / cyan crystal shard: lit facet #F9FDFC / #BAF3E3, shadow facet #78D8D1 / #39B4C1, white ridge,
    #1E5F7A edge (cocoon burst, wing shatter, death)."""
    t = (b + 1) / 2
    if t <= 0 or t >= 1:
        return CLEAR
    wide = 0.36
    half = 0.95 * (t / wide if t < wide else (1 - t) / (1 - wide)) ** 0.9
    m = half - abs(a)
    if m <= 0:
        return CLEAR
    if m < 0.13:
        return hexc('#1E5F7A') + (1.0,)
    if abs(a) < 0.07:
        return mix(hexc('#FFFFFF'), hexc('#E2FAF4'), t) + (1.0,)
    if a < 0:
        col = ramp(rmp((0, '#BAF3E3'), (0.5, '#F9FDFC'), (1, '#E2FAF4')), t)
    else:
        col = ramp(rmp((0, '#39B4C1'), (0.6, '#78D8D1'), (1, '#BAF3E3')), t)
    return col + (1.0,)


# ----------------------------------------------------------------------------- cure (gold)
GOLD_LINE = hexc('#E2D9A2')
GOLD_DEEP = hexc('#9A8430')


def paint_cure_beam(a, b):
    """Pale-gold beam coming down on the cured player (core #FFF8F3, #F4EDC9, gold #E2D9A2; v4 k_f1556)."""
    if b <= 0 or b >= 1:
        return CLEAR
    core = math.exp(-(a / 0.22) ** 2)
    glow = 0.7 * math.exp(-(a / 0.6) ** 2)
    fade = smooth(0.0, 0.06, b) * (1 - smooth(0.78, 1.0, b))
    sp = 0.0
    if vnoise(a * 10 + 3, b * 40) > 0.86 and abs(a) < 0.7:
        sp = 0.8
    i = max(core, glow, sp * glow * 2)
    col = ramp(rmp((0, '#E2D9A2'), (0.5, '#F4EDC9'), (0.85, '#FFF8F3'), (1, '#FFFFFF')), i)
    return col + (clamp01(i * fade * 1.1),)


def paint_cure_burst(a, b):
    """White-gold burst sphere with a gold ring outline (#F6F5EE / #E8E4C3, ring #E0DD9C; v4 k_f1566)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    ring = math.exp(-((r - 0.88) / 0.025) ** 2)
    rd = 0.0 if r > 0.95 else math.exp(-((r - 0.95) / 0.02) ** 2)
    if ring > 0.5:
        return mix(hexc('#E0DD9C'), WHITE, (ring - 0.5) * 1.2) + (1.0,)
    core = math.exp(-(r / 0.45) ** 2)
    rays = 0.6 * star4(a, b, 0.85, 0.05)
    i = max(core, rays, ring, rd * 0.6)
    col = ramp(rmp((0, '#E0DD9C'), (0.4, '#E8E4C3'), (0.8, '#F6F5EE'), (1, '#FFFFFF')), i)
    return col + (clamp01(max(i, 0.18 * smooth(0.95, 0.5, r))),)


def _arc_dist(x, y, cx, cy, R, a0, a1):
    """distance to a circular arc from angle a0 to a1 (degrees, ccw)"""
    th = math.degrees(math.atan2(y - cy, x - cx)) % 360
    lo, hi = a0 % 360, (a0 % 360) + ((a1 - a0) % 360)
    if lo <= th <= hi or lo <= th + 360 <= hi:
        return abs(math.hypot(x - cx, y - cy) - R)
    pts = [(cx + R * math.cos(math.radians(t)), cy + R * math.sin(math.radians(t))) for t in (a0, a1)]
    return min(math.hypot(x - px, y - py) for px, py in pts)


def paint_cure_emblem(a, b):
    """Gold emblem above the cured player: a tall spire with a star on top, two scroll arms and a crescent base
    (an ornate crown / fleur-de-lis, lines #D5DD81 / #E2D9A2, dark gold outline; v4 k_f1600)."""
    x, y = a, b
    d = 9.0
    # spire (a long thin diamond) and its crossguard
    y0, y1 = -1.15, 1.05
    if y0 <= y <= y1:
        t = (y - y0) / (y1 - y0)
        half = 0.13 * (t / 0.38) ** 0.6 if t < 0.38 else 0.13 * (1 - (t - 0.38) / 0.62)
        d = min(d, abs(x) - half)
    d = min(d, seg_dist(x, y, -0.3, -0.18, 0.3, -0.18) - 0.035)
    # scroll arms (mirrored): an outward arc curling back in
    for sx in (-1, 1):
        d = min(d, _arc_dist(sx * x, y, 0.38, 0.08, 0.30, 200, 470) - 0.032)
        d = min(d, _arc_dist(sx * x, y, 0.52, 0.18, 0.10, 90, 300) - 0.028)
    # crescent base
    d = min(d, _arc_dist(x, y, 0.0, -0.5, 0.62, 200, 340) - 0.045)
    # star on top
    s = star4(x, y - 1.24, 0.30, 0.07)
    if s > 0.35:
        return mix(hexc('#F4EDC9'), WHITE, s) + (1.0,)
    if d < 0:
        return mix(GOLD_LINE, hexc('#FFF8F3'), 0.35) + (1.0,)
    if d < 0.035:
        return GOLD_DEEP + (1.0,)
    g = 0.35 * math.exp(-(d / 0.12) ** 2)
    if s > 0.02:
        g = max(g, s)
    return hexc('#F4EDC9') + (g,) if g > 0.02 else CLEAR


def paint_dew_orb(a, b):
    """'달빛 이슬' moon-dew heal orb: a pale cyan-white glowing orb with a crescent moon inside, a sparkle and a
    soft mint halo."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.62:
        g = 0.55 * math.exp(-((r - 0.62) / 0.16) ** 2)
        return hexc('#BFF5E4') + (g,) if g > 0.02 else CLEAR
    moon = math.hypot(a + 0.10, b - 0.10) < 0.30 and math.hypot(a + 0.0, b - 0.19) > 0.27
    if moon:
        return hexc('#FFFFF2') + (1.0,)
    sp = star4(a - 0.27, b - 0.27, 0.16, 0.04)
    if sp > 0.3:
        return WHITE + (1.0,)
    rim = math.exp(-((r - 0.58) / 0.03) ** 2)
    col = ramp(rmp((0, '#F4FFFB'), (0.45, '#C8F5E6'), (0.8, '#9FE2C8'), (1, '#8FE0D0')), r / 0.62)
    col = mix(col, WHITE, rim)
    return col + (clamp01(0.62 + 0.3 * r / 0.62 + 0.3 * rim),)


# ----------------------------------------------------------------------------- telegraphs (neutral, tinted)
def _band(r, bands):
    for lo, hi, col, al in bands:
        if lo <= r < hi:
            return col + (al,)
    return CLEAR


RIM_BANDS = ((0.900, 0.915, DARK, 0.7), (0.915, 0.955, WHITE, 1.0), (0.955, 0.99, DARK, 0.92))
RIM_BANDS_S = ((0.66, 0.72, DARK, 0.7), (0.72, 0.86, WHITE, 1.0), (0.86, 0.99, DARK, 0.92))


def paint_t_rim(a, b):
    """Telegraph rim (unit radius): dark outline, saturated (tinted) band, thin dark inner line."""
    return _band(math.hypot(a, b), RIM_BANDS)


def paint_t_rim_s(a, b):
    """Thick telegraph rim for small discs (r <= 2.5)."""
    return _band(math.hypot(a, b), RIM_BANDS_S)


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
            ux, uy = math.sin(t), math.cos(t)                 # ray direction in (a, b)
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
def glyph_coc(x, y):
    """달빛 고치 badge: maroon #8C525C disc, salmon-red #D06A60 rim, salmon #ED928C / #E8858A double-hook swirl,
    dark outline (v2 k_f1560, v3 icons_zoom)."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    if r > 0.9:
        return hexc('#3A1A20') + (1.0,)
    if r > 0.77:
        return mix(hexc('#E07A70'), hexc('#B8564E'), (r - 0.77) / 0.13) + (1.0,)
    # the swirl: two hooks with 180-degree symmetry
    d = 9.0
    for sg in (1, -1):                                   # S-swirl: a diagonal spine with a curled hook at each end
        px, py = sg * x, sg * y
        pts = [(-0.20, -0.12)]
        for i in range(25):
            t = i / 24
            ang = math.radians(-40 + 235 * t)
            rad = 0.24 - 0.09 * t
            pts.append((0.06 + rad * math.cos(ang), 0.26 + rad * math.sin(ang)))
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            d = min(d, seg_dist(px, py, ax, ay, bx, by))
    if d < 0.075:
        return mix(hexc('#F6A8A0'), hexc('#E8858A'), d / 0.075) + (1.0,)
    if d < 0.11:
        return hexc('#4A2028') + (1.0,)
    return mix(hexc('#9C5E68'), hexc('#6A3A44'), r / 0.77) + (1.0,)


def glyph_buff(x, y):
    """달빛 축복 받음 (reward buff) badge: dark gold disc, gold rim #E0DD9C / #D5B84A, a gold-white 4-point star and
    a small crescent moon."""
    r = math.hypot(x, y)
    if r > 1:
        return CLEAR
    if r > 0.9:
        return hexc('#2A200A') + (1.0,)
    if r > 0.77:
        return mix(hexc('#F2E3A0'), hexc('#C9A23E'), (r - 0.77) / 0.13) + (1.0,)
    s = star4(x - 0.08, y - 0.04, 0.62, 0.11)
    if s > 0.3:
        return mix(hexc('#F4D77C'), hexc('#FFF8E0'), (s - 0.3) / 0.7) + (1.0,)
    moon = math.hypot(x + 0.36, y + 0.30) < 0.24 and math.hypot(x + 0.27, y + 0.24) > 0.21
    if moon:
        return hexc('#F6E7A8') + (1.0,)
    return mix(hexc('#6A5420'), hexc('#3E3010'), r / 0.77) + (1.0,)


def glyph_dew(x, y):
    """Small moon-dew drop icon for hint lines."""
    yy = y + 0.15
    r = math.hypot(x, yy)
    tip = y > 0.2 and abs(x) < 0.55 * (1 - (y - 0.2) / 0.75)
    if (r < 0.6 or tip) and y < 0.95:
        if r < 0.6 and math.hypot(x + 0.15, yy - 0.12) < 0.18:
            return (1.0, 1.0, 1.0, 1.0)
        return mix(hexc('#C8F5E6'), hexc('#7FD8C0'), (r / 0.6)) + (1.0,)
    if r < 0.7 or (tip and y < 1.0):
        return hexc('#1E4A40') + (1.0,)
    return CLEAR
