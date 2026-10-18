"""Painted sprites of the Moonlit Butterfly's fx kit (tools/build_mboss_bf_fx.py). Stdlib only.

Every painter takes card coordinates (a, b) inside its kind's painter box and returns straight-alpha
(r, g, b, alpha) floats. Card coordinates follow Navia's cards (tools/build_navia_fx_cards.py): +a is the card's
local -x (the player's right when seen from behind or from above), +b is up (face cards) or forward (flat cards).
Colours are the hex values sampled from the reference videos (scratchpad mb2/understand/v1-v4.md).

The energy sprites are built as layers composited back to front (over()): a soft saturated halo whose alpha falls
off smoothly (the vanilla item shader discards alpha < 0.1, so every falloff is shaped to fade before that cut), a
translucent streaked body, then a near-white core. Items cannot glow additively, so each sprite also carries a thin
darker under-tone (teal for Dendro, mauve for Pyro, dark gold for the cure) that keeps it readable on the white
marble, while the saturated body carries it on the pink floor and the dark cave.

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


def gauss(d, w):
    return math.exp(-(d / w) ** 2)


def over(dst, src):
    """straight-alpha RGBA src composited over dst"""
    sa = src[3]
    if sa <= 0.0:
        return dst
    da = dst[3] * (1 - sa)
    oa = sa + da
    return ((src[0] * sa + dst[0] * da) / oa, (src[1] * sa + dst[1] * da) / oa, (src[2] * sa + dst[2] * da) / oa, oa)


def rgba(col, al):
    return (col[0], col[1], col[2], clamp01(al))


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


def needles(a, b, rays):
    """intensity of thin tapered rays [(angle deg, length, width)] from the origin (angle 0 = +b, 90 = +a)"""
    r = math.hypot(a, b)
    if r < 1e-6:
        return 1.0
    phi = math.atan2(a, b)
    best = 0.0
    for deg, ln, w in rays:
        if r >= ln:
            continue
        d = (phi - math.radians(deg) + math.pi) % (2 * math.pi) - math.pi
        if abs(d) > 1.2:
            continue
        f = 1 - r / ln
        perp = r * math.sin(abs(d))
        best = max(best, f ** 1.2 * math.exp(-(perp / (w * f + 0.006)) ** 2))
    return best


def _lens(px, py, ox, oy, ux, uy, length, hw):
    """inside a lens (leaf / shard / feather) from (ox, oy) along unit (ux, uy): (u 0..1, |v| / width, signed v),
    or None outside"""
    dx, dy = px - ox, py - oy
    u = (dx * ux + dy * uy) / length
    if u <= 0 or u >= 1:
        return None
    sv = -dx * uy + dy * ux
    w = hw * math.sin(math.pi * u ** 0.75) ** 0.9
    if abs(sv) >= w:
        return None
    return u, abs(sv) / w, sv


# ----------------------------------------------------------------------------- crescents
CRES_SPAN = 80.0      # half-angle of the arc, degrees either side of forward (as Navia's crescent)
CRES_RO = 0.955       # outer edge radius in painter units (0.48 x size in blocks)

CRES = {
    # body ramp across the ribbon (0 = outer edge .. 1 = inner edge), under-tone ribbon (colour, alpha), halos,
    # rim line, feather ramp (0 root .. 1 tip) and feather edge
    'lime': dict(
        body=rmp((0, '#FBFFF0'), (0.05, '#EDF9DA'), (0.12, '#E2F9B4'), (0.22, '#D7F899'), (0.34, '#C1F788'),
                 (0.46, '#A6E35E'), (0.58, '#89D175'), (0.70, '#5AA86A'), (0.82, '#3A765D'), (1.0, '#2E647D')),
        under=(hexc('#297272'), 0.88), halo=hexc('#C8F57A'), inner_halo=hexc('#3A765D'), line=hexc('#F7FCD8'),
        alpha=(0.92, 0.12), tail=0.42,
        spike=rmp((0, '#3E8E5A'), (0.3, '#7FCB55'), (0.62, '#B8F060'), (1, '#E5FBC8')), spike_edge=hexc('#26675B')),
    'cyan': dict(
        body=rmp((0, '#FFFFFF'), (0.07, '#F9FDFC'), (0.2, '#E2FAF4'), (0.36, '#BAF3E3'), (0.52, '#9BE7DD'),
                 (0.66, '#78D8D1'), (0.80, '#39B4C1'), (1.0, '#22788F')),
        under=(hexc('#1E5F7A'), 0.82), halo=hexc('#D4F8EE'), inner_halo=hexc('#2C7F92'), line=hexc('#FFFFFF'),
        alpha=(0.86, 0.14), tail=0.45,
        spike=rmp((0, '#39B4C1'), (0.4, '#78D8D1'), (0.75, '#BAF3E3'), (1, '#F9FDFC')), spike_edge=hexc('#1E5F7A')),
    'fire': dict(
        body=rmp((0, '#FFFCEE'), (0.05, '#FDF6DC'), (0.14, '#F9E38E'), (0.26, '#F8D486'), (0.38, '#F4BA33'),
                 (0.52, '#EB9F26'), (0.66, '#ED7C59'), (0.80, '#DE7A8A'), (1.0, '#CC6976')),
        under=(hexc('#E0708A'), 0.72), halo=hexc('#F48A9A'), inner_halo=hexc('#E26E8A'), line=hexc('#FFF8DA'),
        alpha=(0.9, 0.12), tail=0.5,
        spike=rmp((0, '#E8607A'), (0.3, '#ED7C59'), (0.6, '#F4BA33'), (1, '#FDF6DC')), spike_edge=hexc('#C2507A')),
}


def _spikes(seed, n, lo, hi, w0, w1, tilt0, tilt1):
    """inner-edge feathers along the arc: (centre angle deg, length, half width, lean toward the tail deg)"""
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        s = 0.14 + (k + rnd.uniform(0.2, 0.8)) * 0.8 / n          # 0 tail .. 1 head
        c = CRES_SPAN - 2 * CRES_SPAN * s
        out.append((c, rnd.uniform(lo, hi) * (0.6 + 0.55 * s), rnd.uniform(w0, w1), rnd.uniform(tilt0, tilt1)))
    return out


_SP = {'lime': _spikes(11, 11, 0.22, 0.36, 0.034, 0.054, 52, 66),
       'cyan': _spikes(12, 8, 0.14, 0.26, 0.022, 0.034, 40, 58),
       'fire': _spikes(13, 15, 0.26, 0.46, 0.016, 0.026, 66, 78)}


def _thick(sc):
    """ribbon thickness along the arc (sc 0 tail .. 1 head): thin tail, heavy body, pointed head"""
    return 0.30 * math.sin(math.pi * sc ** 1.35) ** 0.6 + 0.004


def crescent(a, b, mode, seed):
    """Energy slash crescent in the swing plane (Navia's shape: pivot = card origin, head at -a, tail fading to
    +a). Layers: a soft halo outside the outer edge, a streaked body ramping from the white-hot outer edge through
    the bright and saturated colours to a darker under-tone ribbon at the inner edge, a second energy line, feathers
    (leaf blades / crystal shards / flame licks) trailing inward from the inner edge, and a wispy broken tail."""
    pal = CRES[mode]
    r = math.hypot(a, b)
    if r < 0.15 or r > 1.0:
        return CLEAR
    phi = math.degrees(math.atan2(a, b))              # 0 forward, + toward +a (right)
    s = (CRES_SPAN - phi) / (2 * CRES_SPAN)           # 0 tail (right) .. 1 head (left)
    if s <= -0.04 or s >= 1.03:
        return CLEAR
    sc = min(max(s, 0.0), 1.0)
    n = fbm(phi * 0.05 + seed * 13.1, r * 5.0 + seed, 3)
    wob = 0.012 * (fbm(phi * 0.21 + seed, 3.3, 2) - 0.5)
    ro = CRES_RO - 0.018 * (1 - sc) + wob
    T = _thick(sc)
    ri = ro - T
    tailfade = smooth(-0.03, pal['tail'], s) * (1 - smooth(0.985, 1.03, s))
    px = CLEAR
    if r > ro:                                         # outer halo
        g = 0.5 * gauss(r - ro, 0.016 + 0.016 * sc) * tailfade
        return rgba(pal['halo'], g) if g > 0.03 else CLEAR
    if r < ri:                                         # haze under the ribbon
        g = 0.26 * gauss(ri - r, 0.04) * tailfade * smooth(0.1, 0.5, sc)
        if g > 0.03:
            px = rgba(pal['inner_halo'], g)
    if r >= ri:
        px = over(px, _ribbon(pal, mode, seed, r, ri, T, ro, sc, s, n, tailfade))
    return _feathers(px, a, b, phi, s, mode, pal)


def _ribbon(pal, mode, seed, r, ri, T, ro, sc, s, n, tailfade):
    w = (ro - r) / T                                    # 0 outer edge .. 1 inner edge
    streak = fbm(w * 6.5 + seed * 3.1, sc * 3.6 + seed, 3)
    fine = fbm(w * 19.0 + seed, sc * 11.0 + 0.4 * streak, 2)
    col = ramp(pal['body'], clamp01(w * 0.98 + (n - 0.5) * 0.14 + (fine - 0.5) * 0.12))
    col = mix(col, WHITE, 0.18 * smooth(0.55, 0.85, fine) * (1 - w) ** 1.2)
    uc, ua = pal['under']
    under = smooth(0.6, 0.92, w + 0.1 * (streak - 0.5))
    col = mix(col, uc, under * 0.85)
    a0, a1 = pal['alpha']
    alpha = a0 + a1 * (smooth(0.4, 0.7, streak) - 0.5) + 0.1 * smooth(0.55, 0.85, fine)
    alpha = alpha * (1 - under) + ua * under
    rim = gauss(w, 0.06)                                # white-hot rim along the outer edge
    line2 = 0.6 * gauss(w - 0.3 - 0.08 * (streak - 0.5), 0.05) * smooth(0.25, 0.7, sc)
    col = mix(col, pal['line'], max(rim, line2))
    alpha = max(alpha, rim, line2)
    brk = smooth(0.32, 0.68, streak + 0.4 * sc)         # the tail breaks up into streaks
    alpha *= tailfade * (0.2 + 0.8 * (brk + (1 - brk) * smooth(0.15, 0.6, sc)))
    alpha *= smooth(0.0, 0.03 if mode != 'fire' else 0.07, r - ri)
    return rgba(col, alpha)


def _feathers(px, a, b, phi, s, mode, pal):
    for c, ln, hw, tilt in _SP[mode]:                  # feathers from the inner edge, leaning toward the tail
        if abs(phi - c) > 45:
            continue
        sk = (CRES_SPAN - c) / (2 * CRES_SPAN)
        t = math.radians(c)
        rr = CRES_RO - 0.018 * (1 - sk) - _thick(sk) + 0.03
        ox, oy = rr * math.sin(t), rr * math.cos(t)
        inx, iny = -math.sin(t), -math.cos(t)          # toward the pivot
        tgx, tgy = math.cos(t), -math.sin(t)           # toward the tail
        lt = math.radians(tilt)
        ux, uy = inx * math.cos(lt) + tgx * math.sin(lt), iny * math.cos(lt) + tgy * math.sin(lt)
        hit = _lens(a, b, ox, oy, ux, uy, ln, hw)
        if not hit:
            continue
        u, v, sv = hit
        if mode == 'cyan':                              # straight crystal shard: hard edge, bright ridge
            col = ramp(pal['spike'], 1 - u * 0.8)
            col = mix(col, WHITE, 0.6 * gauss(v, 0.25))
            al = 0.92
            if v > 0.8:
                col, al = mix(col, pal['spike_edge'], 0.7), 0.95
        elif mode == 'fire':                            # flame lick: hot root, pink wisp tip
            col = ramp(pal['spike'], clamp01(1 - u * 1.05 - v * 0.25))
            al = (0.9 - 0.62 * u ** 1.3) * (1 - 0.5 * v ** 2)
        else:                                           # leaf blade: bright midrib, two-tone, teal edge
            col = ramp(pal['spike'], (0.9 - 0.55 * u) if sv > 0 else (0.62 - 0.5 * u))
            col = mix(col, hexc('#EDF9DA'), 0.8 * gauss(v, 0.14) * (1 - 0.7 * u))
            al = 0.97 - 0.42 * u ** 2
            if v > 0.76:
                col, al = mix(col, pal['spike_edge'], 0.8), 0.92
        px = over(px, rgba(col, al * smooth(0.0, 0.5, s + 0.2)))
        break
    return px


def paint_cres_lime(a, b):
    """Lime kick / vacuum-blade crescent: #EDF9DA / #E5FBC8 white-hot edge, #D7F899 / #C1F788 / #BFF191 body,
    #89D175 / #8DCA85 edge, teal #297272 / #2E647D under-ribbon, leaf-blade feathers (v1 §5, v2 dash ring)."""
    return crescent(a, b, 'lime', 1)


def paint_cres_cyan(a, b):
    """Cyan-white crescent: cocoon burst / wind crescents, #F9FDFC / #BAF3E3 / #78D8D1 / #39B4C1 with crystal
    feathers (v1 §5)."""
    return crescent(a, b, 'cyan', 2)


def paint_cres_fire(a, b):
    """Fire crescent / flame sheet: #FDF6DC core, gold #F9E38E / #F8D486, #F4BA33 / #EB9F26, orange #ED7C59,
    magenta #CC6976 edges in a pink haze, with flame licks trailing toward the tail (v3 §5 날개탄)."""
    return crescent(a, b, 'fire', 3)


_CLAW = (0.30, -0.06, 0.60, 92.0, 268.0)               # centre x, y, radius, arc from / to (deg; 180 = left)


def paint_fire_claw(a, b):
    """Camera-facing fire crescent projectile: a golden claw / feather hook '(' (opening right) with a white-hot
    head blob at the top, flame licks on its back that trail toward the tip, and a pink-magenta haze around the
    hook, so it reads from every side (v3 k_f0309 / k_f0516)."""
    cx, cy, R, t0, t1 = _CLAW
    dx, dy = a - cx, b - cy
    rr = math.hypot(dx, dy)
    th = math.degrees(math.atan2(dy, dx)) % 360
    u = (th - t0) / (t1 - t0)                                 # 0 top end (head) .. 1 bottom tip
    uc = clamp01(u)
    ta = math.radians(t0 + uc * (t1 - t0))
    dist = math.hypot(a - (cx + R * math.cos(ta)), b - (cy + R * math.sin(ta)))   # to the arc, round caps
    px = CLEAR
    hz = 0.48 * gauss(dist, 0.05 + 0.07 * (1 - uc) ** 1.5)
    if hz > 0.06:
        px = rgba(mix(hexc('#E26E8A'), hexc('#F49A5A'), 0.4 * (1 - uc)), hz)
    if 0 < u < 1:
        n = fbm(th * 0.06, rr * 7, 3)
        t = 0.30 * (1 - u) ** 0.85 * smooth(0.0, 0.05, u) + 0.012
        ro = R + t * 0.55 + 0.15 * (n - 0.35) * (1 - u) * smooth(0.04, 0.2, u)   # flame licks on the convex back
        ri = R - t * 0.45
        if ri <= rr <= ro:
            w = (ro - rr) / (ro - ri)                         # 0 outer (back) .. 1 inner
            col = ramp(rmp((0, '#E8707A'), (0.14, '#ED7C59'), (0.30, '#F4BA33'), (0.5, '#F9E38E'), (0.68, '#FFFBEA'),
                           (0.86, '#F8D486'), (1.0, '#E59546')), w)
            al = 0.96 if w > 0.16 else 0.45 + 3.2 * w
            px = over(px, rgba(col, al))
    hx, hy = cx + R * math.cos(math.radians(t0 + 8)), cy + R * math.sin(math.radians(t0 + 8))
    hb = gauss(math.hypot(a - hx, b - hy), 0.085)
    if hb > 0.05:
        px = over(px, rgba(mix(hexc('#F9E38E'), WHITE, hb), clamp01(hb * 1.5)))
    return px if px[3] > 0.03 else CLEAR


# ----------------------------------------------------------------------------- flares, glints, bursts
_STAR_NEEDLES = [(deg, ln, w) for deg, ln, w in
                 ((18, 0.62, 0.020), (63, 0.45, 0.018), (108, 0.58, 0.020), (153, 0.40, 0.016), (198, 0.66, 0.020),
                  (242, 0.42, 0.016), (290, 0.55, 0.019), (333, 0.48, 0.017), (35, 0.30, 0.014), (125, 0.33, 0.014),
                  (215, 0.28, 0.013), (305, 0.31, 0.014))]


def paint_star4(a, b):
    """Lime 4-point star flare: white core, four long rays and four shorter diagonal ones, jagged thin needles and
    a lime glow that ends before the alpha cut (H2 star flash #FBFDF4 / #DAF7B2, release flare #F8FCE7 / #D8F2BC
    / #AEE76F, glow #7EC866)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    main = star4(a, b, 0.98, 0.055)
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    diag = 0.7 * star4(d1, d2, 0.55, 0.04)
    ndl = 0.75 * needles(a, b, _STAR_NEEDLES)
    core = gauss(r, 0.10)
    i = max(main, diag, ndl, core)
    px = CLEAR
    glow = 0.62 * gauss(r, 0.24) + 0.35 * star4(a, b, 0.9, 0.12)
    if glow > 0.06:
        px = rgba(mix(hexc('#8FD45E'), hexc('#C6EE8E'), clamp01(glow * 1.4)), glow)
    if i > 0.04:
        col = ramp(rmp((0, '#9ADB6A'), (0.25, '#AEE76F'), (0.45, '#D8F2BC'), (0.7, '#F8FCE7'), (1, '#FFFFFF')), i)
        px = over(px, rgba(col, clamp01(i * 1.25)))
    return px


def paint_glint(a, b):
    """Neutral white 4-point glint (sparkles; tint gold, cyan or lime): white core, tapered rays, faint diagonal
    rays and a small soft halo (white, so a tint stays clean)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    main = star4(a, b, 0.98, 0.06)
    d1, d2 = (a + b) / math.sqrt(2), (a - b) / math.sqrt(2)
    i = max(main, 0.5 * star4(d1, d2, 0.42, 0.04), gauss(r, 0.13))
    halo = 0.42 * gauss(r, 0.22)
    px = (1.0, 1.0, 1.0, halo) if halo > 0.06 else CLEAR
    if i > 0.03:
        px = over(px, (1.0, 1.0, 1.0, clamp01(i * 1.3)))
    return px


def _burst_spikes(seed, n):
    rnd = random.Random(seed)
    out = []
    for k in range(n):
        deg = (k + rnd.uniform(-0.3, 0.3)) * 360 / n
        big = k % 3 == 0
        out.append((deg, rnd.uniform(0.80, 0.98) if big else rnd.uniform(0.40, 0.72),
                    rnd.uniform(0.10, 0.13) if big else rnd.uniform(0.06, 0.09)))
    return out


BURST_SPIKES = _burst_spikes(36, 24)


def paint_burst(a, b):
    """Lime-white spiky starburst (kick impacts, orb bursts, cocoon burst core): a white-hot core, 24 jagged
    spikes with white-yellow midlines (#FBFDF4 / #E4F8CC) and saturated #C1F59D / #8BE04A / #74E542 flanks, and a
    soft lime glow behind (v1 §5, v2 dash burst #F9FDE0 / #EAFDB2 / #A2ECA3)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    phi = math.atan2(a, b)
    best, mid = 0.0, 0.0
    for deg, length, w0 in BURST_SPIKES:
        if r >= length:
            continue
        d = (phi - math.radians(deg) + math.pi) % (2 * math.pi) - math.pi
        if abs(d) > 1.0:
            continue
        perp = r * math.sin(abs(d))
        f = 1 - r / length
        w = w0 * f ** 0.85 + 0.004
        if perp < w:
            best = max(best, f)
            mid = max(mid, (1 - perp / w) * (0.35 + 0.65 * f))
    px = CLEAR
    glow = 0.62 * gauss(r, 0.30)
    if glow > 0.06:
        px = rgba(mix(hexc('#9BE84A'), hexc('#D2F7A0'), glow), glow)
    core = gauss(r, 0.17)
    if best > 0:
        col = ramp(rmp((0, '#6ED83A'), (0.18, '#8BE04A'), (0.38, '#C1F59D'), (0.6, '#E4F8CC'), (0.8, '#FBFDF4'),
                       (1, '#FFFFFF')), max(mid, core))
        px = over(px, rgba(col, 0.96))
    if core > 0.08:
        px = over(px, rgba(mix(hexc('#F4FDE0'), WHITE, core), clamp01(core * 1.5)))
    return px


def paint_glow(a, b):
    """Neutral soft glow disc (flashes, ground glow, core glow); tint it. A hot core over a gaussian body and a
    wide faint skirt."""
    r = math.hypot(a, b)
    if r >= 1:
        return CLEAR
    al = 0.95 * gauss(r, 0.34) + 0.30 * (1 - r * r) ** 1.6
    v = 0.9 + 0.1 * gauss(r, 0.3)
    return (v, v, v, clamp01(al))


def paint_mote(a, b):
    """Neutral moonlight mote: a hot dot with a faint cross glint and a soft halo, slightly drawn out vertically
    like the rising charge motes (v2 #C7DB75 / #E6F6F8; tint lime, cyan or gold)."""
    r = math.hypot(a, b * 0.8)
    i = max(gauss(r, 0.2), 0.6 * star4(a, b, 0.95, 0.05))
    halo = 0.5 * gauss(r, 0.36)
    px = (1.0, 1.0, 1.0, halo) if halo > 0.06 else CLEAR
    if i > 0.03:
        px = over(px, (1.0, 1.0, 1.0, clamp01(i * 1.3)))
    return px


def paint_streak(a, b):
    """Neutral long thin streak tapered at both ends (the cyan X glint, slash and speed lines): a white core line
    over a soft white halo, brightest in the middle third."""
    t = abs(a)
    if t >= 1:
        return CLEAR
    hw = (1 - t ** 2.2) + 0.02
    core = gauss(b, 0.22 * hw)
    halo = 0.55 * gauss(b, 0.55 * hw)
    k = (1 - t ** 6) * (0.75 + 0.25 * gauss(t, 0.45))
    px = (1.0, 1.0, 1.0, clamp01(halo * k)) if halo * k > 0.06 else CLEAR
    if core * k > 0.03:
        px = over(px, (1.0, 1.0, 1.0, clamp01(core * k * 1.25)))
    return px


def paint_leaf(a, b):
    """Neutral leaf / petal flake (tint lime for drifting leaves, amber for the embers after the blast): a curved
    leaf with a bright midrib, a lighter and a darker half and a soft darker rim."""
    t = (b + 0.92) / 1.84
    if t <= 0 or t >= 1:
        return CLEAR
    half = 0.5 * math.sin(math.pi * t ** 0.8) ** 0.85
    x = a - 0.14 * math.sin(math.pi * t)
    m = half - abs(x)
    if m <= -0.04:
        return CLEAR
    if m <= 0:
        return (0.6, 0.6, 0.58, 0.5 * (1 + m / 0.04))
    if m < 0.07:
        return (0.66, 0.67, 0.64, 1.0)
    if abs(x) < 0.04 and 0.08 < t < 0.88:
        return (1.0, 1.0, 1.0, 1.0)
    v = 0.8 + 0.18 * t + (0.05 if x < 0 else -0.06) + 0.04 * (vnoise(a * 9, b * 9) - 0.5)
    return (v, v, v * 0.97, 1.0)


def paint_bfly(a, b):
    """Neutral small butterfly outline glyph (floats around her during 달빛 해제, v3 zoom_f2022 #B8E04C; tint
    lime): a bright outline with a soft glow and translucent wings."""
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
    body = abs(a) < 0.045 and abs(b) < 0.48
    if best < 0.032 or body:
        return (1.0, 1.0, 1.0, 1.0)
    g = 0.5 * gauss(best, 0.05)
    if inside:
        return (1.0, 1.0, 1.0, max(0.24, g))
    return (1.0, 1.0, 1.0, g) if g > 0.06 else CLEAR


# ----------------------------------------------------------------------------- rings, discs, spheres
def paint_disc_lime(a, b):
    """Dendro disc ('풀 원판', H2): a flat glowing lime vortex: three spiral arms (#E8FBD0 / #C2ECB0) over a
    #84C75D / #A6E282 body, a white-hot centre #F5FCE8, a bright #F5FCE8 / #C2ECB0 rim with a soft outer glow and
    a dark green line inside it for the white marble (v1 k_f1684 / k_f1688, v4 k_f1868 #A9E180)."""
    r = math.hypot(a, b)
    if r >= 1:
        return CLEAR
    th = math.atan2(b, a)
    n = fbm(a * 3 + 5, b * 3 + 5, 3)
    if r > 0.93:
        g = 0.55 * gauss(r - 0.93, 0.03)
        return rgba(hexc('#B6F07A'), g) if g > 0.03 else CLEAR
    if r > 0.84:
        w = abs(r - 0.885) / 0.045
        return rgba(mix(hexc('#FAFFF0'), hexc('#B9E99E'), w ** 1.5), 1.0)
    if r > 0.805:
        return rgba(mix(hexc('#3E8A34'), hexc('#5DAF4E'), (r - 0.805) / 0.035), 0.92)
    arm = 0.5 + 0.5 * math.cos(3 * (th + 2.2 * math.log(r + 0.05)) + n * 2.2)
    arm = smooth(0.4, 0.95, arm)
    edge = gauss(0.5 + 0.5 * math.cos(3 * (th + 2.2 * math.log(r + 0.05)) + n * 2.2) - 0.32, 0.08)
    col = mix(hexc('#6DB84E'), hexc('#9EDC72'), 0.3 + 0.7 * n)
    col = mix(col, hexc('#4E9A3C'), edge * 0.45 * smooth(0.15, 0.5, r))
    col = mix(col, mix(hexc('#D8F79A'), hexc('#F1FCD8'), arm ** 3), arm * (0.4 + 0.6 * smooth(0.08, 0.5, r)))
    col = mix(col, hexc('#B9E99E'), smooth(0.6, 0.8, r) * 0.35)
    core = gauss(r, 0.17)
    col = mix(col, hexc('#F5FCE8'), core)
    return rgba(col, 0.78 + 0.16 * arm + 0.1 * core)


_RIPPLE_ARCS = ((0.80, 0.3, 1.5), (0.64, 2.4, 1.2), (0.95, 4.0, 1.7), (0.74, 5.1, 1.0), (0.56, 3.6, 0.8))


def paint_ripple(a, b):
    """Near-white ripple / wind ring (transformation ripples #D0F2B9 / #BDE592, wind arcs #E4F8CC / #A3BBA6,
    shock rings); tint it. A bright main ring with a soft glow, a faint inner ring and tapered wind arcs that
    thicken toward their heads."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    core = gauss(r - 0.885, 0.018)
    glow = 0.45 * gauss(r - 0.885, 0.06)
    i = max(core, 0.4 * gauss(r - 0.70, 0.016))
    for rk, a0, ln in _RIPPLE_ARCS:
        d = (th - a0) % (2 * math.pi)
        if d < ln:
            f = (d / ln) ** 0.7 * smooth(1.0, 0.85, d / ln)          # thin tail .. thick head
            i = max(i, 0.85 * f * gauss(r - rk, 0.008 + 0.012 * f))
            glow = max(glow, 0.3 * f * gauss(r - rk, 0.04))
    px = (0.8, 0.82, 0.8, clamp01(glow)) if glow > 0.03 else CLEAR
    if i > 0.03:
        v = 0.88 + 0.12 * min(1.0, i)
        px = over(px, (v * 0.98, v, v * 0.96, clamp01(i * 1.1)))
    return px


def paint_gyro(a, b):
    """Lime gyroscope ring (orb rings, the 달빛 해제 ring cage): a thin white-lime core line #F2FDE2 / #DCFA9A in
    a glowing #ADE87F / #91CF7E band and a #64B360 haze, two bright comet heads with fading tails (it reads as
    spinning), four small beads, and faint #26666A edge lines for the white marble (v3 k_f2133, v4 k_f0372)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    d = r - 0.9
    lead = 0.0
    for h0 in (0.5, 0.5 + math.pi):
        x = (h0 - th) % (2 * math.pi)                       # 0 at the head, growing along the tail
        lead = max(lead, math.exp(-x / 1.3) if x < 5.5 else 0.0)
    k = 0.55 + 0.45 * lead
    px = CLEAR
    haze = 0.32 * gauss(d, 0.07) * k
    if haze > 0.02:
        px = rgba(hexc('#64B360'), haze)
    edge = 0.5 * (gauss(abs(d) - 0.034, 0.008)) * (1 - 0.5 * lead)
    if edge > 0.03:
        px = over(px, rgba(hexc('#26666A'), edge))
    band = gauss(d, 0.026)
    if band > 0.04:
        px = over(px, rgba(mix(hexc('#91CF7E'), hexc('#ADE87F'), lead), band * (0.7 + 0.3 * k)))
    core = gauss(d, 0.009) * k
    if core > 0.04:
        px = over(px, rgba(mix(hexc('#DCFA9A'), hexc('#F2FDE2'), lead), clamp01(core * 1.3)))
    for kb in range(4):
        bx, by = 0.9 * math.cos(kb * math.pi / 2 + math.pi / 4), 0.9 * math.sin(kb * math.pi / 2 + math.pi / 4)
        bd = math.hypot(a - bx, b - by)
        if bd < 0.06:
            px = over(px, rgba(mix(hexc('#F2FDE2'), hexc('#91CF7E'), bd / 0.045), 1.0 if bd < 0.045 else
                               (0.06 - bd) / 0.015))
    return px


def paint_sphere(a, b):
    """Light sphere (transformation r 2.5, flash shells, the orb prop when tinted): translucent, limb-brightened
    #EFFDA2 / #CFF489 with a white rim line, faint radial light streaks, a white-yellow #FAFCD4 / #F8FDBB core
    and a soft outer glow (v2 k_f1464)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.95:
        g = 0.5 * gauss(r - 0.95, 0.025)
        return rgba(hexc('#CFF489'), g) if g > 0.03 else CLEAR
    th = math.atan2(b, a)
    limb = smooth(0.4, 0.95, r)
    rim = gauss(r - 0.925, 0.018)
    rays = smooth(0.62, 0.92, vnoise(th * 7.0 + 3, 0.5)) * smooth(0.15, 0.5, r) * (1 - limb * 0.6)
    core = gauss(r, 0.30)
    swirl = smooth(0.7, 0.95, 0.5 + 0.5 * math.sin(th * 2 + r * 6 + 2 * fbm(a * 2 + 9, b * 2, 2))) * (1 - r ** 4) * 0.5
    col = ramp(rmp((0, '#FAFCD4'), (0.4, '#F8FDBB'), (0.75, '#EFFDA2'), (1, '#CFF489')), limb)
    col = mix(col, WHITE, max(rim, core * 0.85, rays * 0.6, swirl * 0.5))
    col = mix(col, hexc('#F4FBC4'), 0.35 * (1 - limb))
    alpha = 0.42 + 0.45 * limb ** 2.2 + 0.4 * rim + 0.5 * core + 0.22 * rays + 0.12 * swirl
    return rgba(col, alpha)


def paint_dome(a, b, hi):
    """Dome shell segment (달빛 해제 lime dome r 10): translucent saturated lime #77D04C / #87F155 / #5CD63D with
    swirling wind bands #C2F999 / #F8FDDA edged by dark #397731 lines, and a bright ground band #F1FDD9 / #C9F899
    (v3 k_f2182, v4 k_f0476). Trapezoid mask so that 8 per band close the dome (the sides feather over the small
    overlap of neighbours); hi = the upper band (narrow top)."""
    v = (b + 1) / 2                                         # 0 bottom .. 1 top of the card
    hw = (1.0 + (0.78 - 1.0) * v) if not hi else (0.80 + (0.20 - 0.80) * v)
    if abs(a) > hw:
        return CLEAR
    edge = smooth(0.0, 0.07, (hw - abs(a)) / hw)
    n = fbm(a * 2.2 + (7 if hi else 0), b * 2.2, 3)
    sw = math.sin((a * 1.3 + b * 2.5) * 4.0 + n * 5.5 + 1.3 * math.sin(a * 2.1 - b * 1.4))
    band = smooth(0.80, 0.97, sw)
    dark = gauss(sw - 0.6, 0.07) * 0.8
    col = mix(hexc('#5CD63D'), hexc('#87F155'), 0.25 + 0.75 * n)
    col = mix(col, hexc('#3F9A34'), dark * 0.4)
    col = mix(col, mix(hexc('#C2F999'), hexc('#F8FDDA'), smooth(0.93, 1.0, sw)), band)
    alpha = 0.56 + 0.12 * n + 0.3 * band + 0.08 * dark
    if not hi:
        g = smooth(0.17, 0.0, v)
        col = mix(col, ramp(rmp((0, '#F8FDDA'), (0.6, '#F1FDD9'), (1, '#C9F899')), v / 0.17), g)
        alpha = max(alpha, 0.9 * g)
        ln = gauss(v - 0.185, 0.012)
        col = mix(col, hexc('#3F9A34'), ln * 0.6)
        alpha = max(alpha, 0.8 * ln)
    else:
        top = smooth(0.7, 1.0, v)
        col = mix(col, hexc('#C9F899'), top * 0.6)
        alpha = alpha * (1 - 0.45 * smooth(0.9, 1.0, v)) + 0.15 * top
    return rgba(col, alpha * edge)


def paint_dome_lo(a, b):
    return paint_dome(a, b, False)


def paint_dome_hi(a, b):
    return paint_dome(a, b, True)


# ----------------------------------------------------------------------------- fire
FLAME = rmp((0, '#C2507A'), (0.18, '#E8607A'), (0.34, '#ED7C59'), (0.5, '#F88F39'), (0.66, '#F4BA33'),
            (0.8, '#F9E38E'), (0.92, '#FDF6DC'), (1, '#FFFFF4'))


def paint_fan_fire(a, b):
    """180-degree flame fan on the floor (날개 휩쓸개 eruption footprint, seen from above): radial flame tongues
    with a white-yellow #FDF6DC / #F9E38E root ring, an orange #F88F39 / #F09A5F body and magenta-pink #E8607A /
    #A46076 tips fading into a pink haze, around a scorched #585542 centre with #EDC30B embers (v3 k_f0779 /
    k_f0785)."""
    if b < -0.02:
        return CLEAR
    r = math.hypot(a, b)
    if r >= 1:
        return CLEAR
    phi = math.degrees(math.atan2(a, b))
    edge = smooth(-0.02, 0.06, b)                     # the straight back edge
    tip = 0.70 + 0.27 * fbm(phi * 0.13 + 4, 1.7, 2)
    tongue = fbm(phi * 0.22, r * 1.8 - 0.4, 3)
    px = CLEAR
    if r > tip:
        g = 0.5 * gauss(r - tip, 0.06) * edge
        return rgba(hexc('#E8707A'), g) if g > 0.03 else CLEAR
    if r < 0.2:
        col = mix(hexc('#3E3A2C'), hexc('#585542'), r / 0.2)
        ex, ey = a * 26, b * 26                          # ember specks: one small dot in some noise cells
        cx_, cy_ = math.floor(ex), math.floor(ey)
        h = _lat(cx_ + 7, cy_ + 3)
        if h > 0.55 and math.hypot(ex - cx_ - 0.5, ey - cy_ - 0.5) < 0.22 + 0.15 * (h - 0.55):
            col = mix(hexc('#EDC30B'), hexc('#FFE87A'), h)
        px = rgba(col, (0.5 + 0.3 * r / 0.2) * edge)
        if r < 0.15:
            return px
    u = (r - 0.2) / (tip - 0.2)
    heat = 1 - u
    lick = smooth(0.25, 0.75, tongue + 0.3 * (1 - u))
    col = ramp(FLAME, clamp01(0.15 + 0.85 * heat ** 0.9 * (0.65 + 0.5 * lick)))
    col = mix(col, hexc('#FFFDF0'), gauss(u - 0.08, 0.07) * 0.8)
    alpha = (0.62 + 0.38 * lick) * (1 - 0.35 * smooth(0.75, 1.0, u)) * smooth(0.15, 0.24, r)
    return over(px, rgba(col, alpha * edge))


def paint_flame_tongue(a, b):
    """One vertical flame tongue (pivot at its root): a white-yellow core, a gold-orange body, magenta-pink edges
    and a soft pink haze, a forked flickering tip and a dark ember base (날개 휩쓸개 flame wall, landing flame
    streaks; v3 §5 #F09A5F / #F7CC9C / #A46076 / #8C5436)."""
    if b <= 0 or b >= 1:
        return CLEAR
    x0 = 0.2 * math.sin(b * 5.2 + 0.7) * b
    hw = 0.8 * (1 - b) ** 0.7 * (0.5 + 0.5 * math.sin(math.pi * min(1.0, b * 2.3 + 0.22)))
    n = fbm(a * 3 + 1, b * 4.5, 3)
    hw *= 0.82 + 0.36 * n
    d = abs(a - x0)
    px = CLEAR
    hz = 0.42 * gauss(max(0.0, d - hw), 0.12) * (1 - smooth(0.75, 1.0, b)) * smooth(0.0, 0.08, b)
    if hz > 0.03:
        px = rgba(hexc('#E8707A'), hz)
    if d > hw:
        return px if px[3] > 0.03 else CLEAR
    u = d / hw
    fork = 0.0
    if b > 0.55:                                       # a notch splits the tip
        fork = gauss(a - x0 - 0.05, 0.08 + 0.1 * (1 - b)) * smooth(0.55, 0.85, b)
    col = ramp(FLAME, clamp01(1.02 - u * 0.78 - b * 0.26 + (n - 0.5) * 0.22))
    if b < 0.07:
        col = mix(col, hexc('#8C5436'), (0.07 - b) / 0.07 * 0.6)
    alpha = (1 - 0.35 * u ** 2) * (1 - smooth(0.78, 1.0, b)) * (1 - 0.8 * fork) * smooth(0.0, 0.03, b)
    return over(px, rgba(col, alpha))


def paint_flame_puff(a, b):
    """Soft flame puff (the low glide's flame trail #E04040 / #F06A30, B2 crescent trails, landing splashes): a
    gold-white core, an orange body and red-magenta wisps fading out smoothly (no rim)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    th = math.atan2(b, a)
    re = 0.72 + 0.26 * fbm(math.cos(th) * 1.6 + 2, math.sin(th) * 1.6 + 2, 3)
    u = r / re
    n = fbm(a * 3.2, b * 3.2, 3)
    al = 0.95 * gauss(u, 0.6 + 0.12 * n)
    if al < 0.04:
        return CLEAR
    col = ramp(rmp((0, '#C8406A'), (0.2, '#E04848'), (0.38, '#F06A30'), (0.56, '#F88F39'), (0.74, '#F9C85A'),
                   (0.9, '#FDEBA8'), (1, '#FFF8E0')), clamp01(1.05 - u * 0.95 + (n - 0.5) * 0.3))
    return rgba(col, al)


# ----------------------------------------------------------------------------- blades and shards
def paint_blade(a, b):
    """Radial ground blade (orb burst, ground wave, the vacuum spike): a long, slightly curved lance rising from
    its root, widest near the floor and tapering to a needle tip: a white-lime midrib #EAFDD9, a lit #B4EB68 /
    #D6F5A8 half, a shaded #80BD77 / #5DBE3A half, thin dark #2C686D / #356F64 edges and a soft lime glow (v3
    k_f1373 / k_f1377)."""
    if b <= 0 or b >= 1:
        return CLEAR
    hw = 0.36 * (b / 0.08) ** 0.5 if b < 0.08 else 0.36 * ((1 - b) / 0.92) ** 1.1
    x0 = 0.24 * b * b
    d = a - x0
    px = CLEAR
    g = 0.38 * gauss(max(0.0, abs(d) - hw), 0.1 + 0.08 * (1 - b)) * smooth(0.0, 0.08, b) * (1 - smooth(0.85, 1.0, b))
    if g > 0.03:
        px = rgba(hexc('#8FE04A'), g)
    if abs(d) >= hw:
        return px if px[3] > 0.03 else CLEAR
    u = d / max(hw, 1e-6)
    if abs(u) > 0.8:
        col = mix(hexc('#356F64'), hexc('#2C686D'), (abs(u) - 0.8) / 0.2)
        return over(px, rgba(col, 0.92))
    if abs(u) < 0.14:
        col = mix(hexc('#D6F5A8'), hexc('#F6FEEA'), b)
    elif u < 0:
        col = mix(hexc('#B4EB68'), hexc('#E6FBAA'), smooth(0.2, 1.0, b))
    else:
        col = mix(hexc('#5DBE3A'), hexc('#80BD77'), smooth(0.1, 0.8, b))
    col = mix(col, hexc('#4E8C55'), smooth(0.18, 0.0, b) * 0.45)
    al = (0.82 + 0.18 * b) * smooth(0.0, 0.04, b)
    return over(px, rgba(col, al))


def paint_shard(a, b):
    """White / cyan crystal shard: an elongated, slightly asymmetric crystal with a lit facet #F9FDFC / #E2FAF4,
    a shadow facet #78D8D1 / #39B4C1, a white ridge and a secondary facet line, a thin #1E5F7A edge and a soft
    cyan glow (cocoon burst #BAF3E3, wing shatter (tinted lime), death)."""
    t = (b + 1) / 2
    if t <= 0 or t >= 1:
        return CLEAR
    wide = 0.32
    half = 0.86 * (t / wide if t < wide else (1 - t) / (1 - wide)) ** 0.85
    sk = 0.1 * (t - wide)                                  # a slight lean
    x = a - sk
    m = half - abs(x)
    px = CLEAR
    g = 0.34 * gauss(max(0.0, -m), 0.13)
    if g > 0.03:
        px = rgba(hexc('#BAF3E3'), g)
    if m <= 0:
        return px if px[3] > 0.03 else CLEAR
    if m < 0.07:
        return over(px, rgba(hexc('#1E5F7A'), 0.95))
    if abs(x) < 0.06:
        return over(px, rgba(mix(WHITE, hexc('#E2FAF4'), t), 1.0))
    if x < 0:
        col = ramp(rmp((0, '#BAF3E3'), (0.45, '#F9FDFC'), (1, '#E2FAF4')), t)
        if abs(x + half * 0.5) < 0.035:
            col = mix(col, hexc('#9BE7DD'), 0.6)            # a secondary facet edge
    else:
        col = ramp(rmp((0, '#39B4C1'), (0.55, '#78D8D1'), (1, '#BAF3E3')), t)
        col = mix(col, hexc('#2C9AAE'), 0.3 * smooth(0.3, 0.0, m))
    return over(px, rgba(col, 0.96))


# ----------------------------------------------------------------------------- cure (gold)
GOLD_DEEP = hexc('#8C7428')


def paint_cure_beam(a, b):
    """Pale-gold beam coming down on the cured player (core #FFF8F3, #F4EDC9, gold #E2D9A2; v4 k_f1556): a
    white-hot core line, a glowing spire lens high on the beam with gold filigree edges, sparkle specks and a
    wide gold haze, fading at both ends."""
    if b <= 0 or b >= 1:
        return CLEAR
    fade = smooth(0.0, 0.07, b) * (1 - smooth(0.82, 1.0, b))
    lens = 0.0
    lw = 0.0
    if 0.48 < b < 0.92:
        lw = 0.42 * math.sin(math.pi * (b - 0.48) / 0.44) ** 0.9
        lens = smooth(lw, lw * 0.6, abs(a)) if lw > 0 else 0.0
    core = gauss(a, 0.12)
    glow = 0.6 * gauss(a, 0.42)
    haze = 0.3 * gauss(a, 0.85)
    sp = 0.0
    if abs(a) < 0.8 and vnoise(a * 11 + 3, b * 46) > 0.84:
        sp = 0.85 * gauss(a, 0.5)
    i = max(core, glow, lens * 0.95, sp)
    px = rgba(hexc('#E2D9A2'), haze * fade) if haze * fade > 0.03 else CLEAR
    if lw > 0:
        fil = gauss(abs(a) - lw, 0.03)
        if fil > 0.05:
            px = over(px, rgba(mix(hexc('#C9A23E'), hexc('#F4E4A0'), 0.4), fil * fade))
    if i > 0.03:
        col = ramp(rmp((0, '#E2D9A2'), (0.5, '#F4EDC9'), (0.85, '#FFF8F3'), (1, '#FFFFFF')), i)
        px = over(px, rgba(col, clamp01(i * fade * 1.1)))
    return px


def paint_cure_burst(a, b):
    """White-gold burst sphere with a gold ring outline (#F6F5EE / #E8E4C3 core, smoky #E8D58A / #F4EDC9 haze,
    ring #E0DD9C / #C9A23E with a white core and a fainter second ring; v4 k_f1566)."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    n = fbm(a * 3 + 7, b * 3 + 1, 3)
    px = CLEAR
    smoke = 0.5 * smooth(0.95, 0.35, r) * (0.4 + 0.6 * n)
    if smoke > 0.05:
        px = rgba(mix(hexc('#D9C26A'), hexc('#F4EDC9'), n), smoke)
    core = gauss(r, 0.40)
    rays = 0.55 * star4(a, b, 0.85, 0.045)
    i = max(core, rays)
    if i > 0.03:
        col = ramp(rmp((0, '#E0DD9C'), (0.4, '#E8E4C3'), (0.8, '#F6F5EE'), (1, '#FFFFFF')), i)
        px = over(px, rgba(col, clamp01(i * 1.05)))
    ring = gauss(r - 0.88, 0.026)
    ring2 = 0.55 * gauss(r - 0.955, 0.012)
    if max(ring, ring2) > 0.05:
        px = over(px, rgba(hexc('#C9A23E'), max(ring * 0.95, ring2)))
        if ring > 0.45:
            px = over(px, rgba(mix(hexc('#E0DD9C'), hexc('#FFF8E0'), (ring - 0.45) * 1.8), (ring - 0.45) * 1.8))
    return px


def _arc_dist(x, y, cx, cy, R, a0, a1):
    """distance to a circular arc from angle a0 to a1 (degrees, ccw)"""
    th = math.degrees(math.atan2(y - cy, x - cx)) % 360
    lo, hi = a0 % 360, (a0 % 360) + ((a1 - a0) % 360)
    if lo <= th <= hi or lo <= th + 360 <= hi:
        return abs(math.hypot(x - cx, y - cy) - R)
    pts = [(cx + R * math.cos(math.radians(t)), cy + R * math.sin(math.radians(t))) for t in (a0, a1)]
    return min(math.hypot(x - px, y - py) for px, py in pts)


def paint_cure_emblem(a, b):
    """Gold emblem above the cured player: a tall spire lens with a crossguard and a star on top, two scroll arms
    and a crescent base (an ornate crown / fleur-de-lis) in glowing gold lines #D5DD81 / #E2D9A2 with white-gold
    cores, a thin dark-gold outline and a soft #F4EDC9 glow (v4 k_f1576 / k_f1600)."""
    x, y = a, b
    d = 9.0
    # spire (a long thin lens) and its crossguard
    y0, y1 = -1.15, 1.05
    if y0 <= y <= y1:
        t = (y - y0) / (y1 - y0)
        half = 0.15 * (t / 0.4) ** 0.6 if t < 0.4 else 0.15 * (1 - (t - 0.4) / 0.6) ** 0.9
        d = min(d, abs(x) - half)
    d = min(d, seg_dist(x, y, -0.32, -0.18, 0.32, -0.18) - 0.04)
    for sx in (-1, 1):
        d = min(d, _arc_dist(sx * x, y, 0.38, 0.08, 0.30, 200, 470) - 0.038)
        d = min(d, _arc_dist(sx * x, y, 0.52, 0.18, 0.10, 90, 300) - 0.032)
    d = min(d, _arc_dist(x, y, 0.0, -0.5, 0.62, 200, 340) - 0.05)
    s = star4(x, y - 1.24, 0.32, 0.07)
    px = CLEAR
    g = 0.42 * gauss(max(0.0, d), 0.13) + 0.5 * gauss(math.hypot(x, y - 1.24), 0.16)
    if g > 0.03:
        px = rgba(hexc('#F4EDC9'), g)
    if d < 0.03:
        px = over(px, rgba(GOLD_DEEP, 0.95 * smooth(0.03, 0.015, d) if d > 0 else 0.95))
    if d < 0:
        inner = clamp01(-d / 0.03)
        px = over(px, rgba(mix(hexc('#D5DD81'), hexc('#FFF8F3'), inner * 0.8), 1.0))
    if s > 0.25:
        px = over(px, rgba(mix(hexc('#F4EDC9'), WHITE, s), clamp01(s * 1.3)))
    return px if px[3] > 0.02 else CLEAR


def paint_dew_orb(a, b):
    """'달빛 이슬' moon-dew heal orb: a pale cyan-white glowing orb (#F4FFFB core to #9FE2C8) with a thin darker teal
    rim for the white marble, a soft-glowing white crescent moon inside, a sparkle and a soft mint halo."""
    r = math.hypot(a, b)
    if r > 1:
        return CLEAR
    if r > 0.62:
        g = 0.55 * gauss(r - 0.62, 0.15)
        px = rgba(hexc('#BFF5E4'), g) if g > 0.03 else CLEAR
        ln = gauss(r - 0.635, 0.012) * 0.75
        if ln > 0.05:
            px = over(px, rgba(hexc('#2F8F86'), ln))
        return px if px[3] > 0.03 else CLEAR
    rim = gauss(r - 0.58, 0.03)
    col = ramp(rmp((0, '#F4FFFB'), (0.45, '#C8F5E6'), (0.8, '#9FE2C8'), (1, '#7FD8C0')), r / 0.62)
    col = mix(col, WHITE, rim)
    px = rgba(col, 0.62 + 0.3 * r / 0.62 + 0.3 * rim)
    m1 = math.hypot(a + 0.10, b - 0.10) - 0.30
    m2 = math.hypot(a + 0.0, b - 0.19) - 0.27
    moon = min(-m1, m2)                                    # > 0 inside the crescent
    mg = 0.6 * gauss(max(0.0, -moon), 0.06)
    if mg > 0.03:
        px = over(px, rgba(hexc('#FFFFF2'), mg))
    if moon > 0:
        px = over(px, rgba(hexc('#FFFFF6'), smooth(0.0, 0.02, moon)))
    sp = star4(a - 0.27, b - 0.27, 0.18, 0.035)
    if sp > 0.1:
        px = over(px, rgba(WHITE, clamp01(sp * 1.4)))
    return px


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
