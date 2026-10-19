"""Arena theme `ap_oasis`: the forest lake of 아펩의 오아시스 파수꾼 (Guardian of Apep's Oasis), chapter-3 boss.

Theme module (S:az/contract/theme.md, S:ap/ap_contract.md §0.6): plain Python, stdlib only, deterministic, no side
effects on import, never writes files. The arena generator (tools/build_mboss_arena.py) imports `arena_layout`,
`slices`, `look_lines`, `SENTINEL`; the room generator (tools/build_cboss_rooms.py) imports `entrance_layout`; the boss
module imports `props`, `POINTS` and the constants.

The place (plan §4, footage v1-v5): a round clearing in a giant forest, ringed by huge leaning trees whose buttress roots
arch over the shore, under a vault of enormous translucent veined leaves with a sky shaft over the centre. Phase 1 is
withered and olive-yellow, phase 3 lush and green (the lake: the kit's water-sheet props over the same floor).

  floor (r <= 26)       solid y 192..200 of full opaque blocks; moss cells 2-4 b split by packed-mud / rooted-dirt
                        crack lines and dark-oak root veins (from the trees inward, and a ring of leaf cells around the
                        Heart spot), pale moss at r 24-26. Identical in both looks
  bank (26 < r <= 29.6) a low lip (0-1) inside the barrier ring, rock / soil 1-3 high behind it, mangrove-root tangles,
                        dry grass / dead bushes / leaf litter (withered) <-> azalea / flowers / moss carpet (lush), the
                        ember twig; the invisible barrier ring (centre distance 26.9..28.3, y 201..215)
  trees (r 33-36.5)     9 leaning giant trunks (jungle / mangrove / pale oak) with buttress fins, root arches looping
                        over the shore above y 207, shelf mushrooms and froglight bulbs (ochre <-> verdant) at their feet,
                        limbs arching under the vault toward the shaft with moss clumps (pale moss <-> flowering azalea)
  canopy (y 225..250)   three rings of giant leaves (lanceolate, moss midrib and laterals, stained-glass windows yellow
                        <-> lime with green cells, leafy margins pale oak <-> azalea), foliage between them, the shaft
                        r <= 8 open
  forest floor / wall   fallen mossy logs, giant brown mushrooms, bushes, secondary trunks and a foliage curtain closed
                        by a wood / moss column at the box edge, up to the canopy
  lights                the light layer y 206 over r <= 25.5 (level 12 withered, 14 lush); hidden light[level=15]
                        blocks wherever a block-light flood of either look leaves a hostile spawn cell dark (~130)

Coordinates: the centre (440, 201, 8) is a block corner, floor blocks at y 200, stand height 201. A cell (x, z) is "at
distance d" when its centre (x + 0.5, z + 0.5) is d blocks from (440, 8) horizontally. Compass bearings (POINTS):
0 = north (-z), 90 = east (+x), 180 = south (+z, the arrival). Yaw is Minecraft's (0 faces +z, 90 faces -x).

Looks: 'withered' (phase 1 and 2, the default restored by `ensure`) and 'lush' (phase 3, from the CS white-out). The
floor is identical in both; the looks differ only in swapped block types (canopy glass / leaves / clumps, bank plants,
froglight bulbs) and the level of the light layer. `look_lines(look)` turns any built look (or any mix of the two) into
`look` with `fill <box> <new> replace <old>` commands (each box <= 32 768 blocks, <= 24 ticks). Plain `replace`: the
`replace <filter> strict` form is not relied on (ap_contract.md §0.6.5 / O5; every swapped block is a full block,
persistent leaves, glass, a light block or a plant on an unchanged support, so neighbour updates do nothing).
"""
import math

THEME = 'ap_oasis'
AID = 'ap_oasis'

# Registry values this theme was written for (ap_contract.md §0.3.6; the generator asserts equality with CHECK).
CX, CY, CZ = 440, 201, 8
RAD, WALK, SAFE = 29, 26, 24
BOX = {'x0': 396, 'y0': 190, 'z0': -36, 'x1': 484, 'y1': 250, 'z1': 52}
START = {'x': 440.5, 'y': 201.0, 'z': 24.5, 'yaw': 180.0, 'pitch': 0.0}
CHECK = {'cx': CX, 'cy': CY, 'cz': CZ, 'r': RAD, 'walk': WALK, 'safe': SAFE, 'box': dict(BOX), 'start': dict(START)}
LOOKS = ['withered', 'lush']
GEOMETRY = 'full'             # 'day1' (ap_contract.md §0.6.9) or 'full'

FLOOR_Y, SOLID_Y0 = 200, 192  # full opaque blocks only, solid y 192..200 inside r 26 (the rig root sinks to y 195)
RIM = (26, 29)                # the root / rock bank
BARRIER = {'r0': 27, 'r1': 28, 'y0': 201, 'y1': 215}
BARRIER_D = (26.9, 28.3)      # barrier cells: centre distance in (26.9, 28.3] (a closed 8-connected ring, r 27..28)
BANK_D = 29.6                 # the bank band ends here; tree parts below y 207 stay beyond it
ROOT_Y = 207                  # buttress roots may cross over the bank band only above this height
CLEAR_Y = (201, 224)          # inside r 26 only air and the light layer
CANOPY_Y = (225, 250)
SHAFT_R = 8
LIGHT_Y = 206
LIGHT = {'withered': 12, 'lush': 14}
LIGHT_R = 25.5                # the light layer covers cells with centre distance <= 25.5
WATER_Y, DECAL_Y_MIN = 201.005, 201.035
MAX_LOOK_SLICES, SLICE_MS = 24, 20
MAX_FILL = 32768
LOOK_CELLS = 1400             # at most this many swapped cells per look command (spreads the swap over the ticks)
LOOK_STRICT = False           # `replace <filter> strict` is not relied on (ap_contract.md §0.6.5, O5): plain replace

SENTINEL = ((CX, 193, CZ), 'minecraft:packed_mud')

B = 'minecraft:'
PROP_EL = 7                   # Dendro: one fixed look for every prop


# ---------------------------------------------------------------------------------------------------------------
# deterministic helpers

def _mix(*ints):
    """splitmix64-style hash of integers -> float in [0, 1)."""
    h = 0x9E3779B97F4A7C15
    for i in ints:
        h = (h ^ (int(i) & 0xFFFFFFFFFFFFFFFF)) & 0xFFFFFFFFFFFFFFFF
        h = (h * 0xBF58476D1CE4E5B9) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 31
        h = (h * 0x94D049BB133111EB) & 0xFFFFFFFFFFFFFFFF
        h ^= h >> 29
    return (h >> 11) / float(1 << 53)


def _vnoise(x, z, scale, seed):
    """Smooth 2-D value noise in [0, 1] (bilinear smoothstep over a lattice of `scale` blocks)."""
    fx, fz = x / scale, z / scale
    ix, iz = math.floor(fx), math.floor(fz)
    tx, tz = fx - ix, fz - iz
    tx, tz = tx * tx * (3 - 2 * tx), tz * tz * (3 - 2 * tz)
    a, b = _mix(ix, iz, seed), _mix(ix + 1, iz, seed)
    c, d = _mix(ix, iz + 1, seed), _mix(ix + 1, iz + 1, seed)
    return (a * (1 - tx) + b * tx) * (1 - tz) + (c * (1 - tx) + d * tx) * tz


def _fbm(x, z, seed):
    return 0.62 * _vnoise(x, z, 7.0, seed) + 0.38 * _vnoise(x, z, 2.6, seed + 1)


def cell_polar(x, z):
    """(u, v, d, bearing) of the cell centre: u = east offset, v = south offset, compass bearing in degrees."""
    u, v = x + 0.5 - CX, z + 0.5 - CZ
    return u, v, math.hypot(u, v), math.degrees(math.atan2(u, -v)) % 360.0


def _d(x, z):
    return math.hypot(x + 0.5 - CX, z + 0.5 - CZ)


def polar_point(d, bearing):
    """(x, z) of the point at distance d and compass bearing (floats)."""
    a = math.radians(bearing)
    return CX + d * math.sin(a), CZ - d * math.cos(a)


def yaw_facing(dx, dz):
    """Minecraft yaw whose look vector is (dx, dz) (horizontal)."""
    return _norm_yaw(math.degrees(math.atan2(-dx, dz)))


def _norm_yaw(a):
    a = (a + 180.0) % 360.0 - 180.0
    return 180.0 if abs(a + 180.0) < 1e-9 else round(a, 4)


def _r(v, nd=3):
    return round(float(v), nd)


def _in_box(x, y, z):
    return BOX['x0'] <= x <= BOX['x1'] and BOX['y0'] <= y <= BOX['y1'] and BOX['z0'] <= z <= BOX['z1']


def _edge(x, z):
    """Columns from the box edge (0 = the outermost column)."""
    return min(x - BOX['x0'], BOX['x1'] - x, z - BOX['z0'], BOX['z1'] - z)


class Lk(tuple):
    """A look-dependent cell value: Lk((withered, lush)); None = air in that look."""
    __slots__ = ()


def lk(withered, lush):
    return withered if withered == lush else Lk((withered, lush))


# ---------------------------------------------------------------------------------------------------------------
# Materials (the look pairs are exclusive: a withered block of a pair never appears where it stays unchanged, so each
# swap is a handful of big `fill ... replace` boxes)

def _p(n, s=''):
    return B + n + s


PERSIST = '[persistent=true]'
LEAF = lk(_p('pale_oak_leaves', PERSIST), _p('azalea_leaves', PERSIST))            # foliage, leaf margins
GLASS = lk(_p('yellow_stained_glass'), _p('lime_stained_glass'))                    # leaf windows
GLASS2 = _p('green_stained_glass')                                                  # darker leaf cells (both looks)
VEIN = _p('moss_block')                                                             # midribs, laterals, shaft collar
CLUMP = lk(_p('pale_moss_block'), _p('flowering_azalea_leaves', PERSIST))           # crown clumps on the limbs
BULB = lk(_p('ochre_froglight'), _p('verdant_froglight'))                           # glowing bulbs at the tree feet
LIGHT_BLOCK = lk(_p('light[level=%d]' % LIGHT['withered']), _p('light[level=%d]' % LIGHT['lush']))
HIDDEN_LIGHT = _p('light[level=15]')                                                # the anti-spawn lattice
PLANTS = (  # (withered, lush, weight): bank plants on dirt-tag supports
    (_p('dead_bush'), _p('azalea'), 0.22),
    (_p('tall_dry_grass'), _p('flowering_azalea'), 0.18),
    (_p('short_dry_grass'), _p('dandelion'), 0.32),
    (_p('leaf_litter[facing=north,segment_amount=4]'), _p('moss_carpet'), 0.28),
)
DIRT_TOPS = {_p('moss_block'), _p('rooted_dirt'), _p('pale_moss_block'), _p('podzol'), _p('coarse_dirt')}
SPECIES = {
    'jungle': {'log': _p('jungle_log[axis=y]'), 'wood': _p('jungle_wood'), 'root': _p('jungle_wood')},
    'mangrove': {'log': _p('mangrove_log[axis=y]'), 'wood': _p('mangrove_wood'), 'root': _p('mangrove_roots')},
    'pale_oak': {'log': _p('pale_oak_log[axis=y]'), 'wood': _p('pale_oak_wood'), 'root': _p('pale_oak_wood')},
}


# ---------------------------------------------------------------------------------------------------------------
# Heights

def canopy_y(d):
    """Height of the leaf vault over distance d: y 246.5 at the shaft rim, 239 at r 20, 230 at r 40, 225.5 at r 60."""
    s = min(1.0, max(0.0, (d - 8.0) / 52.0))
    return 225.5 + 21.0 * (1.0 - s) ** 1.6


TWIG_CELL = (432, 203, -20)                     # the ember twig block (POINTS['ember_twig'] = a point inside it)


def bank_h(x, z):
    """Bank height above the floor (0..3) for 26 < d <= BANK_D: a low lip inside the barrier ring, 1-2 in the ring,
    1-3 rocks / soil behind it."""
    d = _d(x, z)
    if (x, z) == (TWIG_CELL[0], TWIG_CELL[2]):
        return 2
    n = _fbm(x, z, 31)
    if d <= BARRIER_D[0]:
        return 1 if (n > 0.6 and d > 26.4) else 0
    if d <= BARRIER_D[1]:
        return 1 + (n > 0.55)
    return max(1, min(3, int(round(1.0 + 2.4 * n + 0.6 * (d - BARRIER_D[1])))))


def ground_top(x, z):
    """Top block y of the ground column (the floor, the bank, the outer ground)."""
    d = _d(x, z)
    if d <= WALK:
        return FLOOR_Y
    if d <= BANK_D:
        return FLOOR_Y + bank_h(x, z)
    g = (d - 31.5) * 0.17 + 2.6 * (_fbm(x, z, 37) - 0.45)
    e = _edge(x, z)
    if e < 7:
        g += (7 - e) * 0.55
    lo = 1 if _under_water_tiles(x, z) else 0      # the lush water tiles (y 201.005) reach r 39.6 at their corners:
    return FLOOR_Y + max(lo, min(7, int(round(g))))  # the ground they cover beyond the bank rises over them


def _under_water_tiles(x, z):
    """True for a column under the 4 x 4 lush water-sheet tiles (x / z within CX / CZ +- 28)."""
    return CX - 28 <= x <= CX + 27 and CZ - 28 <= z <= CZ + 27


# ---------------------------------------------------------------------------------------------------------------
# Trees (planned once; the layout, the points and the props share them)

_TREE_PLAN = (  # bearing, distance, trunk radius, species, inward lean at the crown
    (5.0, 34.0, 2.6, 'jungle', 3.6), (45.0, 36.0, 2.9, 'mangrove', 4.0), (85.0, 33.0, 2.3, 'jungle', 3.2),
    (125.0, 36.5, 2.8, 'pale_oak', 4.2), (165.0, 33.5, 2.4, 'jungle', 3.4), (205.0, 35.5, 2.7, 'mangrove', 3.8),
    (245.0, 33.0, 2.5, 'jungle', 3.0), (285.0, 36.5, 3.0, 'pale_oak', 4.4), (325.0, 34.5, 2.4, 'jungle', 3.6),
)


def _tree(k):
    b, d, R, sp, lean = _TREE_PLAN[k]
    b += 4.0 * (_mix(k, 1) - 0.5)
    bx, bz = polar_point(d, b)
    top = int(round(canopy_y(d - lean) - 2.0))
    return {'k': k, 'bearing': b, 'd': d, 'R': R, 'species': sp, 'lean': lean, 'x': bx, 'z': bz, 'top': top,
            'mat': SPECIES[sp]}


TREES_FULL = [_tree(k) for k in range(len(_TREE_PLAN))]
TREES = [(_r(t['x'], 2), _r(t['z'], 2), t['R']) for t in TREES_FULL]


def _trunk_axis(t, y):
    """(x, z) of the trunk axis at height y: leans toward the centre (t^1.8) with a slight sideways sway."""
    f = max(0.0, min(1.0, (y - 199.0) / float(t['top'] - 199)))
    a = math.radians(t['bearing'])
    inx, inz = -math.sin(a), math.cos(a)                 # unit vector toward the centre
    sx, sz = -inz, inx                                   # sideways
    sway = 0.9 * math.sin(2.3 * f + t['k'])
    lean = t['lean'] * f ** 1.8
    return t['x'] + inx * lean + sx * sway * f, t['z'] + inz * lean + sz * sway * f


def _trunk_r(t, y):
    f = max(0.0, min(1.0, (y - 199.0) / float(t['top'] - 199)))
    flare = 1.0 + 0.45 * max(0.0, 1.0 - (y - 200.0) / 4.0) ** 2
    return t['R'] * flare * (1.0 - 0.28 * f)


# ---------------------------------------------------------------------------------------------------------------
# Canopy leaves (planned once)

def _leaves():
    """Giant leaves of the vault: three rings, bases outside, tips toward the shaft. Each: base (x, z), unit axis toward
    the tip, length, half width, ring, vertical offset, id."""
    out = []
    rings = ((0, 10, 25.5, 9.4, 5.2, 6.0, 18.0, 0.0), (1, 14, 42.0, 20.5, 6.4, 7.4, 5.0, -0.6),
             (2, 18, 63.0, 37.0, 6.8, 8.2, 13.0, -1.2))
    lid = 0
    for ring, n, d0, d1, w0, w1, off, dy in rings:
        for k in range(n):
            b = off + 360.0 * k / n + (360.0 / n) * 0.18 * (_mix(ring, k, 3) - 0.5)
            skew = 9.0 * (_mix(ring, k, 4) - 0.5)
            bx, bz = polar_point(d0 + 1.5 * (_mix(ring, k, 5) - 0.5), b)
            tx, tz = polar_point(d1 + 1.0 * (_mix(ring, k, 6) - 0.5), b + skew)
            L = math.hypot(tx - bx, tz - bz)
            out.append({'id': lid, 'ring': ring, 'bx': bx, 'bz': bz, 'ax': (tx - bx) / L, 'az': (tz - bz) / L, 'L': L,
                        'w': w0 + (w1 - w0) * _mix(ring, k, 7), 'dy': dy, 'nv': 4 + int(2 * _mix(ring, k, 8))})
            lid += 1
    return out


LEAVES = _leaves()


def _leaf_part(lf, px, pz):
    """(part, |t| / w) of the point in the leaf, or None: 'margin', 'rib', 'glass', 'glass2'."""
    rx, rz = px - lf['bx'], pz - lf['bz']
    s = (rx * lf['ax'] + rz * lf['az']) / lf['L']
    if s < 0.0 or s > 1.0:
        return None
    t = rx * lf['az'] - rz * lf['ax']
    w = lf['w'] * math.sin(math.pi * s ** 0.7) ** 0.8
    at = abs(t)
    if at > w:
        return None
    q = at / w if w > 0 else 1.0
    if w - at < 0.7:
        return 'margin', q
    if at < 0.45 + 0.5 * (1.0 - s):
        return 'rib', q
    D = lf['L'] / (lf['nv'] + 1)
    u = s * lf['L'] - 0.55 * at
    if u > 0.6 and (u % D) < 0.7:
        return 'rib', q
    seg = int(u // D)
    side = 1 if t > 0 else 0
    return ('glass2' if _mix(lf['id'], seg, side, 9) < 0.25 else 'glass'), q


# ---------------------------------------------------------------------------------------------------------------
# Floor pattern

_SEED_S = 5.4


def _seed(gi, gj):
    return ((gi + 0.5 + 0.8 * (_mix(gi, gj, 11) - 0.5)) * _SEED_S, (gj + 0.5 + 0.8 * (_mix(gi, gj, 12) - 0.5)) * _SEED_S)


def _crack(x, z):
    """The crack-network material of floor cell (x, z), or None (moss): Voronoi cell borders (some edges dropped so
    cells merge into 2-6 b patches), packed mud or rooted dirt per edge."""
    px, pz = x + 0.5 - CX, z + 0.5 - CZ
    gi, gj = math.floor(px / _SEED_S), math.floor(pz / _SEED_S)
    best = []
    for a in (-1, 0, 1):
        for b in (-1, 0, 1):
            sx, sz = _seed(gi + a, gj + b)
            best.append(((px - sx) ** 2 + (pz - sz) ** 2, gi + a, gj + b))
    best.sort()
    d1, d2 = math.sqrt(best[0][0]), math.sqrt(best[1][0])
    if d2 - d1 >= 0.72:
        return None
    k1, k2 = sorted(((best[0][1], best[0][2]), (best[1][1], best[1][2])))
    h = _mix(k1[0], k1[1], k2[0], k2[1], 13)
    if h > 0.66:
        return None
    h /= 0.66
    return _p('dark_oak_wood') if h < 0.55 else (_p('rooted_dirt') if h < 0.85 else _p('packed_mud'))


def _polyline_cells(pts, width):
    """Floor cells within width / 2 of the 2-D polyline pts [(x, z)] (cell centres)."""
    out = set()
    hw = width / 2.0
    for (ax, az), (bx, bz) in zip(pts, pts[1:]):
        x0, x1 = math.floor(min(ax, bx) - hw - 1), math.floor(max(ax, bx) + hw + 1)
        z0, z1 = math.floor(min(az, bz) - hw - 1), math.floor(max(az, bz) + hw + 1)
        dx, dz = bx - ax, bz - az
        ll = dx * dx + dz * dz or 1e-9
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                cx, cz = x + 0.5, z + 0.5
                t = max(0.0, min(1.0, ((cx - ax) * dx + (cz - az) * dz) / ll))
                if math.hypot(cx - ax - t * dx, cz - az - t * dz) <= hw:
                    out.add((x, z))
    return out


def _root_veins():
    """Dark-oak root veins flush in the floor: one from every tree (continuing its bank root inward, with a branch),
    four between trees, and a broken ring of leaf cells around the Heart spot with five spokes."""
    cells = set()
    starts = [(t['bearing'], 26.4, 8.5 + 6.0 * _mix(t['k'], 21), 1.7, t['k']) for t in TREES_FULL]
    starts += [(25.0 + 90.0 * k + 20.0 * _mix(k, 22), 26.4, 13.0 + 5.0 * _mix(k, 23), 1.2, 20 + k) for k in range(4)]
    for b0, r0, r1, w, key in starts:
        pts = []
        drift = 26.0 * (_mix(key, 24) - 0.5)
        n = 14
        for i in range(n + 1):
            f = i / n
            r = r0 + (r1 - r0) * f
            b = b0 + drift * f + 7.0 * math.sin(f * 5.1 + key)
            pts.append(polar_point(r, b))
        cells |= _polyline_cells(pts[:4], w)
        cells |= _polyline_cells(pts[3:], 1.0)
        # a branch from the middle
        m = n // 2
        side = 1 if _mix(key, 25) < 0.5 else -1
        br = [pts[m]]
        for i in range(1, 6):
            r = r0 + (r1 - r0) * (m / n) - 1.4 * i
            b = b0 + drift * 0.5 + side * (4.5 * i)
            br.append(polar_point(r, b))
        cells |= _polyline_cells(br, 1.0)
    # the Heart's leaf cells: a ring at r 4.8 broken in 5 places, 5 spokes to r 9.5 between the gaps
    ring = []
    for i in range(0, 361, 6):
        if (i + 18) % 72 < 10:
            if len(ring) > 1:
                cells |= _polyline_cells(ring, 1.0)
            ring = []
            continue
        ring.append(polar_point(4.8, i))
    if len(ring) > 1:
        cells |= _polyline_cells(ring, 1.0)
    for k in range(5):
        b = 72.0 * k + 36.0 - 18.0
        cells |= _polyline_cells([polar_point(5.2, b), polar_point(7.5, b + 6.0), polar_point(9.8, b + 4.0)], 1.0)
    return cells


# ---------------------------------------------------------------------------------------------------------------
# Points (absolute world coordinates; ap_contract.md §0.6.3)

RING_BEARINGS = tuple(22.5 + 45.0 * k for k in range(8))


def _ring(d):
    out = []
    for b in RING_BEARINGS:
        x, z = polar_point(d, b)
        out.append((round(x, 2), float(CY), round(z, 2)))
    return out


def _water_tiles():
    return [(float(x), WATER_Y, float(z)) for z in (-13, 1, 15, 29) for x in (419, 433, 447, 461)]


EMBER_TWIG = (432.6, 203.5, -19.6)          # inside TWIG_CELL: a bank twig at r ~28.6, compass 345


def _near_tree(x, z, extra):
    """True when the point is within the trunk footprint of a tree (+ extra)."""
    for t in TREES_FULL:
        if math.hypot(x - t['x'], z - t['z']) <= t['R'] * 1.5 + extra:
            return True
    return False


def _bank_spot(bearing, dlo, dhi, taken, seed):
    """The bank cell nearest to the bearing (searched +-8 deg) with its centre distance in (dlo, dhi], a dirt / rock top
    and no tree, twig or other prop nearby: the prop point (centre x, top + 1, centre z)."""
    best = None
    for i in range(41):
        b = bearing + (i - 20) * 0.4
        for j in range(9):
            d = dlo + (dhi - dlo) * (j + 0.5) / 9.0
            x, z = (math.floor(v) for v in polar_point(d, b))
            dc = _d(x, z)
            if not (dlo < dc <= dhi) or (x, z) in taken or _near_tree(x + 0.5, z + 0.5, 3.0):
                continue
            if abs(x - TWIG_CELL[0]) <= 1 and abs(z - TWIG_CELL[2]) <= 1:
                continue
            score = abs(i - 20) + 0.5 * abs(j - 4) + _mix(x, z, seed)
            if best is None or score < best[0]:
                best = (score, x, z)
    _, x, z = best
    taken.add((x, z))
    return (x + 0.5, float(ground_top(x, z) + 1), z + 0.5)


def _plan_props():
    taken = set()
    crystals = [_bank_spot(15.0 + 30.0 * k + 8.0 * (_mix(k, 71) - 0.5), BARRIER_D[1] + 0.05, BANK_D - 0.1, taken, 72)
                for k in range(12)]
    pond = []
    for k in range(20):
        b = 9.0 + 18.0 * k + 10.0 * (_mix(k, 81) - 0.5)
        d = 22.6 + 2.8 * _mix(k, 82)
        x, z = polar_point(d, b)
        pond.append(('lily_pad', (_r(x, 2), 201.012, _r(z, 2))))
    for k in range(10):
        pond.append(('bell_flower', _bank_spot(30.0 + 36.0 * k + 12.0 * (_mix(k, 83) - 0.5), 26.05, BARRIER_D[0] - 0.05,
                                               taken, 84)))
    for k in range(6):
        pond.append(('bulb_flower', _bank_spot(60.0 * k + 40.0 + 10.0 * (_mix(k, 85) - 0.5), BARRIER_D[1] + 0.05,
                                               BANK_D - 0.1, taken, 86)))
    return crystals, pond, taken


BANK_CRYSTALS, POND_PROPS, _PROP_CELLS = _plan_props()


def _motes():
    out = []
    for k in range(8):
        x, z = polar_point(17.0, 45.0 * k + 10.0)
        out.append((_r(x, 2), 205.0 + (k % 3), _r(z, 2)))
    for k in range(4):
        x, z = polar_point(3.0, 90.0 * k + 45.0)
        out.append((_r(x, 2), 214.0 + 3 * k, _r(z, 2)))
    return out


POINTS = {
    'spawn': (float(CX), float(CY), float(CZ), 0.0),
    'centre': (float(CX), float(CY), float(CZ)),
    'heart': (float(CX), float(CY), float(CZ)),
    'arrival': (START['x'], START['y'], START['z'], START['yaw']),
    'org_spawn': _ring(12.0),
    'nurt_spawn': _ring(7.0),
    'ember_twig': EMBER_TWIG,
    'water_tiles': _water_tiles(),
    'pond_props': [p for _, p in POND_PROPS],
    'bank_crystals': list(BANK_CRYSTALS),
    'trees': list(TREES),
    'motes': _motes(),
}


# ---------------------------------------------------------------------------------------------------------------
# Layout

_CACHE = {}


class _Grid(dict):
    """{cell: str | Lk} with the placement masks of the layout rules."""

    def put(self, x, y, z, v, layer='decor'):
        if not _in_box(x, y, z):
            return False
        d = _d(x, z)
        if d <= WALK and y >= CLEAR_Y[0] and y <= CLEAR_Y[1]:
            return False                                # the clearance over the walk disc
        if d <= SHAFT_R + 0.6 and y >= CANOPY_Y[0]:
            return False                                # the sky shaft
        if layer != 'ground':
            if d <= WALK and y <= FLOOR_Y:
                return False                            # the floor belongs to the floor painter
            if d <= BANK_D and y < ROOT_Y:
                return False                            # the bank / barrier band below y 207
        self[(x, y, z)] = v
        return True


def _tube(g, pts, radii, mat, layer='tree', sel=None):
    """Cells within the swept radius of the 3-D polyline pts (radii per point); `sel(x, y, z, frac)` -> material or
    None overrides `mat`."""
    n = len(pts)
    for i in range(n - 1):
        (ax, ay, az), (bx, by, bz) = pts[i], pts[i + 1]
        ra, rb = radii[i], radii[i + 1]
        rm = max(ra, rb)
        dx, dy, dz = bx - ax, by - ay, bz - az
        ll = dx * dx + dy * dy + dz * dz or 1e-9
        for x in range(math.floor(min(ax, bx) - rm), math.floor(max(ax, bx) + rm) + 1):
            for y in range(math.floor(min(ay, by) - rm), math.floor(max(ay, by) + rm) + 1):
                for z in range(math.floor(min(az, bz) - rm), math.floor(max(az, bz) + rm) + 1):
                    cx, cy, cz = x + 0.5, y + 0.5, z + 0.5
                    t = max(0.0, min(1.0, ((cx - ax) * dx + (cy - ay) * dy + (cz - az) * dz) / ll))
                    ex, ey, ez = cx - ax - t * dx, cy - ay - t * dy, cz - az - t * dz
                    if ex * ex + ey * ey + ez * ez <= (ra + (rb - ra) * t) ** 2:
                        m = sel(x, y, z, (i + t) / (n - 1)) if sel else mat
                        if m is not None:
                            g.put(x, y, z, m, layer)


def _bezier(p0, p1, p2, p3, n):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append(tuple(a * p0[k] + b * p1[k] + c * p2[k] + d * p3[k] for k in range(3)))
    return out


def _paint_ground(g):
    """Floor, solid fill, bank and outer ground."""
    veins = _root_veins()
    x0, z0, x1, z1 = BOX['x0'], BOX['z0'], BOX['x1'], BOX['z1']
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            d = _d(x, z)
            if d <= WALK:
                for y in range(SOLID_Y0, FLOOR_Y):
                    g.put(x, y, z, _p('packed_mud'), 'ground')
                if (x, z) in veins:
                    top = _p('dark_oak_wood')
                else:
                    top = _crack(x, z)
                    if top is None:
                        top = _p('moss_block')
                        if d > 24.0 and _vnoise(x, z, 2.2, 41) < (d - 24.0) / 2.0 + 0.1:
                            top = _p('pale_moss_block')
                g.put(x, FLOOR_Y, z, top, 'ground')
                continue
            top = ground_top(x, z)
            for y in range(196, top):
                g.put(x, y, z, _p('packed_mud') if y < 199 else _p('rooted_dirt'), 'ground')
            if d <= BANK_D:
                rock = _vnoise(x, z, 2.4, 43) > 0.6 and d > BARRIER_D[0]
                for y in range(FLOOR_Y, top + 1):
                    if rock:
                        m = _p('mossy_cobblestone') if _mix(x, y, z, 44) < 0.75 else _p('cobblestone')
                    elif y < top:
                        m = _p('rooted_dirt')
                    else:
                        n = _vnoise(x, z, 3.0, 45)
                        m = _p('moss_block') if n < 0.55 else (_p('pale_moss_block') if n < 0.75 else _p('rooted_dirt'))
                        if d > BARRIER_D[1] + 0.3 and _vnoise(x, z, 1.8, 46) > 0.72:
                            m = _p('mangrove_roots')
                    g.put(x, y, z, m, 'ground')
                if (x, z) in veins:                     # tree roots run over the bank into the floor
                    g.put(x, top, z, _p('dark_oak_wood'), 'ground')
            else:
                n = _fbm(x, z, 47)
                if n < 0.42:
                    m = _p('moss_block')
                elif n < 0.52:
                    m = _p('rooted_dirt')
                elif n < 0.66:
                    m = _p('moss_block')
                elif n < 0.78:
                    m = _p('pale_moss_block')
                else:
                    m = _p('podzol') if _vnoise(x, z, 2.0, 48) < 0.6 else _p('coarse_dirt')
                g.put(x, top, z, m, 'ground')
    # the ember twig
    tx, ty, tz = TWIG_CELL
    g.put(tx, ty - 1, tz, _p('rooted_dirt'), 'ground')
    g.put(tx, ty, tz, _p('mangrove_roots'), 'ground')


def _paint_tree(g, t):
    mat = t['mat']
    k = t['k']
    # trunk (log core, bark of wood and moss patches low down)
    for y in range(196, t['top'] + 1):
        ax, az = _trunk_axis(t, y)
        R = _trunk_r(t, y)
        for x in range(math.floor(ax - R - 1), math.floor(ax + R + 1) + 1):
            for z in range(math.floor(az - R - 1), math.floor(az + R + 1) + 1):
                px, pz = x + 0.5 - ax, z + 0.5 - az
                a = math.atan2(pz, px)
                rr = R * (0.88 + 0.22 * _vnoise(a * 3.0 + 10.0 * k, y * 0.35, 1.0, 51))
                q = math.hypot(px, pz)
                if q > rr:
                    continue
                if y < ground_top(x, z) - 1:
                    continue
                m = mat['log']
                if q > rr - 1.1:
                    h = _mix(x, y, z, 52)
                    if y <= 203 + 3 * _vnoise(x, z, 3.0, 53) and h < 0.45:
                        m = _p('moss_block') if t['species'] != 'pale_oak' else _p('pale_moss_block')
                    elif h < 0.2:
                        m = mat['wood']
                g.put(x, y, z, m, 'tree')
    # buttress fins: mostly outward and sideways; the inner ones are clipped by the bank mask below y 207
    for j, off in enumerate((-150.0, -95.0, -40.0, 0.0, 40.0, 95.0, 150.0, 180.0)):
        ang = math.radians(t['bearing'] + off + 14.0 * (_mix(k, j, 54) - 0.5))
        ox, oz = math.sin(ang), -math.cos(ang)            # outward direction of the fin (compass)
        L = 3.0 + 3.5 * _mix(k, j, 55)
        H = 3.5 + 3.5 * _mix(k, j, 56)
        if off == 180.0:
            L, H = L * 0.7, H * 0.8                       # the inward fin is short (it meets the bank)
        R0 = t['R'] * 0.9
        for x in range(math.floor(t['x'] - R0 - L - 2), math.floor(t['x'] + R0 + L + 2) + 1):
            for z in range(math.floor(t['z'] - R0 - L - 2), math.floor(t['z'] + R0 + L + 2) + 1):
                px, pz = x + 0.5 - t['x'], z + 0.5 - t['z']
                s = px * ox + pz * oz - R0
                lat = abs(-px * oz + pz * ox)
                if s < -1.0 or s > L or lat > 0.75 + 0.35 * (1 - max(0.0, s) / L):
                    continue
                hh = H * (1.0 - max(0.0, s) / L) ** 1.4
                gt = ground_top(x, z)
                for y in range(gt - 1, int(FLOOR_Y + hh) + 1):
                    if y < gt - 1:
                        continue
                    m = mat['root'] if (t['species'] == 'mangrove' and s > L * 0.45) else mat['wood']
                    g.put(x, y, z, m, 'tree')
    # root arches over the shore (inner side, above y 207): loops from the trunk to the rim and back into the ground
    for j, side in enumerate((-1, 1)):
        if _mix(k, j, 57) < 0.25:
            continue
        b0 = t['bearing']
        ax0, az0 = _trunk_axis(t, 209)
        p0 = (ax0, 209.0, az0)
        x1, z1 = polar_point(26.6, b0 + side * 3.0)
        x2, z2 = polar_point(27.8, b0 + side * 9.0)
        x3, z3 = polar_point(31.5 + 1.5 * _mix(k, j, 58), b0 + side * 14.0)
        pts = _bezier(p0, (x1, 215.0, z1), (x2, 216.0, z2), (x3, 199.0, z3), 30)
        rad = [1.25 - 0.55 * i / 30.0 for i in range(31)]
        _tube(g, pts, rad, mat['root'] if t['species'] == 'mangrove' else mat['wood'], 'tree')
    # shelf mushrooms (outer side) and froglight bulbs at the feet
    for j in range(2 + int(_mix(k, 59) < 0.5)):
        ang = math.radians(t['bearing'] + 70.0 + 220.0 * _mix(k, j, 60))
        ys = 202 + int(7 * _mix(k, j, 61))
        ax, az = _trunk_axis(t, ys)
        R = _trunk_r(t, ys)
        cx, cz = ax + (R + 0.2) * math.sin(ang), az - (R + 0.2) * math.cos(ang)
        rs = 1.6 + 1.0 * _mix(k, j, 62)
        for x in range(math.floor(cx - rs - 1), math.floor(cx + rs + 1) + 1):
            for z in range(math.floor(cz - rs - 1), math.floor(cz + rs + 1) + 1):
                if math.hypot(x + 0.5 - cx, z + 0.5 - cz) <= rs and math.hypot(x + 0.5 - ax, z + 0.5 - az) > R - 0.3:
                    if (x, ys, z) not in g:
                        g.put(x, ys, z, _p('brown_mushroom_block'), 'tree')
        sx, sz = math.floor(cx), math.floor(cz)
        if (sx, ys - 1, sz) not in g:
            g.put(sx, ys - 1, sz, _p('mushroom_stem'), 'tree')
    for j in range(3):
        ang = math.radians(t['bearing'] + 100.0 + 160.0 * _mix(k, j, 63))
        R = _trunk_r(t, 201) + 1.0 + 1.5 * _mix(k, j, 64)
        bx, bz = math.floor(t['x'] + R * math.sin(ang)), math.floor(t['z'] - R * math.cos(ang))
        gt = ground_top(bx, bz)
        if (bx, gt + 1, bz) in g or _d(bx, bz) <= BANK_D:
            continue
        g.put(bx, gt + 1, bz, BULB, 'tree')
        if _mix(k, j, 65) < 0.5:
            g.put(bx + (1 if _mix(k, j, 66) < 0.5 else 0), gt + 1, bz + (0 if _mix(k, j, 66) < 0.5 else 1), BULB, 'tree')
        if _mix(k, j, 67) < 0.35 and (bx, gt + 2, bz) not in g:
            g.put(bx, gt + 2, bz, BULB, 'tree')


def _paint_limbs(g, t):
    """Limbs from the crown: two arch inward under the vault toward the shaft (with moss clumps), two run outward."""
    mat = t['mat']
    k = t['k']
    top = t['top']
    ax, az = _trunk_axis(t, top)
    R = _trunk_r(t, top)
    _tube(g, [(ax, top - 1.0, az), (ax, top + 1.5, az)], [R * 0.95, R * 0.8], mat['wood'], 'tree')
    tips = []
    for j, (db, d_end, outward) in enumerate(((-19.0, 13.0, False), (21.0, 16.0, False), (-38.0, 50.0, True),
                                              (34.0, 47.0, True))):
        b_end = t['bearing'] + db + 6.0 * (_mix(k, j, 70) - 0.5)
        d_end += 2.5 * (_mix(k, j, 71) - 0.5)
        ex, ez = polar_point(d_end, b_end)
        if outward:
            ex = max(BOX['x0'] + 2.5, min(BOX['x1'] - 2.5, ex))
            ez = max(BOX['z0'] + 2.5, min(BOX['z1'] - 2.5, ez))
        d_e = math.hypot(ex - CX, ez - CZ)
        ey = canopy_y(d_e) - (1.7 if not outward else 1.4)
        mx, mz = (ax + ex) / 2.0, (az + ez) / 2.0
        if not outward:                                   # bow the limb sideways (away from the straight chord)
            side = 1.0 if db > 0 else -1.0
            cx_, cz_ = ex - ax, ez - az
            ln = math.hypot(cx_, cz_) or 1.0
            mx += side * 3.5 * (-cz_ / ln)
            mz += side * 3.5 * (cx_ / ln)
        dm = math.hypot(mx - CX, mz - CZ)
        p1 = (ax + (mx - ax) * 0.5, top + 1.5, az + (mz - az) * 0.5)
        p2 = (mx + (ex - mx) * 0.4, canopy_y(dm) - 1.6, mz + (ez - mz) * 0.4)
        pts = _bezier((ax, top + 0.5, az), p1, p2, (ex, ey, ez), 26)
        r0 = R * (0.6 if not outward else 0.5)
        rad = [r0 + (0.55 - r0) * (i / 26.0) for i in range(27)]
        _tube(g, pts, rad, mat['wood'], 'tree')
        if not outward:
            tips.append(pts[-1])
            tips.append(pts[16])
    for j, (cx, cy, cz) in enumerate(tips):
        rh, rv = 1.7 + 0.8 * _mix(k, j, 72), 1.2
        for x in range(math.floor(cx - rh - 1), math.floor(cx + rh + 1) + 1):
            for y in range(math.floor(cy - rv - 1), math.floor(cy + rv + 1) + 1):
                for z in range(math.floor(cz - rh - 1), math.floor(cz + rh + 1) + 1):
                    q = ((x + 0.5 - cx) / rh) ** 2 + ((y + 0.5 - cy) / rv) ** 2 + ((z + 0.5 - cz) / rh) ** 2
                    if q <= 1.0 and _mix(x, y, z, 73) < 0.85 and not str(g.get((x, y, z), '')).endswith('wood'):
                        g.put(x, y, z, CLUMP, 'tree')


def _paint_canopy(g):
    """The vault of giant leaves (one leaf per column, the outer ring on top), foliage in the gaps, the shaft collar."""
    tops, mats = {}, {}
    order = sorted(LEAVES, key=lambda lf: (-lf['ring'], lf['id']))
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            d = _d(x, z)
            if d <= SHAFT_R + 0.6:
                continue
            px, pz = x + 0.5, z + 0.5
            hit = None
            for lf in order:
                r = _leaf_part(lf, px, pz)
                if r is not None:
                    hit = (lf, r)
                    break
            if d <= SHAFT_R + 1.9:
                y, m = int(round(canopy_y(d))), VEIN
            elif hit:
                lf, (part, q) = hit
                y = int(round(canopy_y(d) + lf['dy'] - 0.9 + 1.5 * q * q))
                m = {'margin': LEAF, 'rib': VEIN, 'glass': GLASS, 'glass2': GLASS2}[part]
            else:
                y, m = int(round(canopy_y(d) + 0.9)), LEAF
            tops[(x, z)] = min(BOX['y1'], y)
            mats[(x, z)] = (m, hit is None)
    for (x, z), y in tops.items():
        m, gap = mats[(x, z)]
        y1 = y + (1 if gap else 0)
        for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            yn = tops.get((x + dx, z + dz))
            if yn is not None:
                y1 = max(y1, yn - 1)
        for yy in range(y, min(BOX['y1'], y1) + 1):
            g.put(x, yy, z, m, 'canopy')


def _paint_wall(g):
    """The forest wall: secondary trunks and bushes beyond the giant trees, a closed leaf / wood wall at the box edge."""
    sec = []
    for k in range(16):
        b = 360.0 * k / 16 + 11.0 + 12.0 * (_mix(k, 81) - 0.5)
        a = math.radians(b)
        dmax = min(abs((BOX['x1'] - 3 - CX) / math.sin(a)) if abs(math.sin(a)) > 1e-6 else 1e9,
                   abs((BOX['z1'] - 3 - CZ) / math.cos(a)) if abs(math.cos(a)) > 1e-6 else 1e9)
        d = min(dmax, 41.0 + 14.0 * _mix(k, 82))
        x, z = polar_point(d, b)
        if any(math.hypot(x - t['x'], z - t['z']) < t['R'] + 5.0 for t in TREES_FULL):
            continue
        sec.append((x, z, 1.1 + 0.7 * _mix(k, 83), list(SPECIES)[int(3 * _mix(k, 84))]))
    for (sx, sz, R, sp) in sec:
        top = int(round(canopy_y(math.hypot(sx - CX, sz - CZ)))) + 1
        for x in range(math.floor(sx - R - 1), math.floor(sx + R + 1) + 1):
            for z in range(math.floor(sz - R - 1), math.floor(sz + R + 1) + 1):
                if math.hypot(x + 0.5 - sx, z + 0.5 - sz) <= R:
                    for y in range(ground_top(x, z), top + 1):
                        g.put(x, y, z, SPECIES[sp]['log'], 'wall')
    # fallen logs (mossy, horizontal) and giant brown mushrooms on the forest floor between the trees
    for k in range(5):
        b = 360.0 * k / 5 + 30.0 + 20.0 * (_mix(k, 95) - 0.5)
        d = 39.0 + 6.0 * _mix(k, 96)
        x, z = polar_point(d, b)
        if any(math.hypot(x - t['x'], z - t['z']) < t['R'] + 4.0 for t in TREES_FULL):
            continue
        ang = math.radians(b + 90.0 + 50.0 * (_mix(k, 97) - 0.5))
        L = 5.0 + 4.0 * _mix(k, 98)
        R = 0.9 + 0.5 * _mix(k, 99)
        sp = SPECIES[('jungle', 'pale_oak', 'jungle', 'mangrove', 'pale_oak')[k]]
        gy = ground_top(math.floor(x), math.floor(z)) + R
        p0 = (x - math.sin(ang) * L / 2, gy, z + math.cos(ang) * L / 2)
        p1 = (x + math.sin(ang) * L / 2, gy, z - math.cos(ang) * L / 2)

        def bark(xx, yy, zz, f, sp=sp, gy=gy):
            return _p('moss_block') if (yy + 0.5 > gy + 0.3 and _mix(xx, yy, zz, 100) < 0.45) else sp['wood']
        _tube(g, [p0, p1], [R, R * 0.85], sp['wood'], 'wall', sel=bark)
    for k in range(4):
        b = 360.0 * k / 4 + 75.0 + 25.0 * (_mix(k, 101) - 0.5)
        d = 38.0 + 7.0 * _mix(k, 102)
        x, z = polar_point(d, b)
        if any(math.hypot(x - t['x'], z - t['z']) < t['R'] + 3.5 for t in TREES_FULL):
            continue
        xi, zi = math.floor(x), math.floor(z)
        gy = ground_top(xi, zi)
        h = 4 + int(3 * _mix(k, 103))
        rc = 2.4 + 1.2 * _mix(k, 104)
        for y in range(gy + 1, gy + h + 1):
            g.put(xi, y, zi, _p('mushroom_stem'), 'wall')
        for xx in range(math.floor(x - rc - 1), math.floor(x + rc + 1) + 1):
            for zz in range(math.floor(z - rc - 1), math.floor(z + rc + 1) + 1):
                r = math.hypot(xx + 0.5 - x, zz + 0.5 - z)
                if r <= rc:
                    g.put(xx, gy + h + 1, zz, _p('brown_mushroom_block'), 'wall')
                    if r <= rc * 0.55:
                        g.put(xx, gy + h + 2, zz, _p('brown_mushroom_block'), 'wall')
                elif r <= rc + 0.8:
                    g.put(xx, gy + h, zz, _p('brown_mushroom_block'), 'wall')
    # bushes on the ground between the trees and the wall
    for k in range(70):
        b = 360.0 * _mix(k, 85)
        d = 37.0 + 24.0 * _mix(k, 86)
        x, z = polar_point(d, b)
        if not (BOX['x0'] <= x <= BOX['x1'] and BOX['z0'] <= z <= BOX['z1']):
            continue
        if any(math.hypot(x - t['x'], z - t['z']) < t['R'] + 2.0 for t in TREES_FULL):
            continue
        rh = 2.4 + 2.6 * _mix(k, 87)
        rv = 2.0 + 2.5 * _mix(k, 88)
        gy = ground_top(math.floor(x), math.floor(z))
        for xx in range(math.floor(x - rh - 1), math.floor(x + rh + 1) + 1):
            for zz in range(math.floor(z - rh - 1), math.floor(z + rh + 1) + 1):
                for yy in range(gy + 1, int(gy + rv * 1.6) + 1):
                    q = ((xx + 0.5 - x) / rh) ** 2 + ((yy + 0.5 - gy - 0.6) / rv) ** 2 + ((zz + 0.5 - z) / rh) ** 2
                    q += 0.35 * (_vnoise(xx * 1.7, zz * 1.7 + yy * 3.1, 1.0, 89) - 0.5)
                    if q <= 1.0 and (xx, yy, zz) not in g:
                        g.put(xx, yy, zz, LEAF, 'wall')
    # the closed wall at the box edge: wood / moss in the outermost column, then a foliage curtain whose depth (1-8)
    # varies with height and position, from the ground to the canopy
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            e = _edge(x, z)
            if e > 8:
                continue
            top = int(round(canopy_y(_d(x, z)))) + 1
            for y in range(ground_top(x, z) + 1, min(BOX['y1'], top) + 1):
                if (x, y, z) in g:
                    continue
                if e == 0:
                    m = _p('jungle_wood') if _vnoise(x + z, y, 3.0, 90) < 0.55 else _p('moss_block')
                else:
                    depth = 1.5 + 6.5 * _vnoise(x * 0.7 + z * 0.7 + y * 0.4, y * 0.9 - (x - z) * 0.3, 4.0, 94)
                    if e > depth:
                        continue
                    m = LEAF
                g.put(x, y, z, m, 'wall')


def _paint_plants(g):
    """Bank plants: on dirt-tag tops of the lip and behind the barrier ring (never in the ring), not on prop spots."""
    tw = sum(w for _, _, w in PLANTS)
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            d = _d(x, z)
            if not (WALK < d <= BANK_D) or BARRIER_D[0] < d <= BARRIER_D[1] or (x, z) in _PROP_CELLS:
                continue
            if abs(x - TWIG_CELL[0]) <= 1 and abs(z - TWIG_CELL[2]) <= 1:
                continue
            top = ground_top(x, z)
            if g.get((x, top, z)) not in DIRT_TOPS or (x, top + 1, z) in g:
                continue
            if _vnoise(x, z, 3.5, 91) + 0.35 * _mix(x, z, 92) < 0.62:
                continue
            h = tw * _mix(x, z, 93)
            for w_, l_, wt in PLANTS:
                if h < wt:
                    g[(x, top + 1, z)] = lk(w_, l_)
                    break
                h -= wt


def _paint_lights(g):
    """The light layer over the walk disc (level 12 withered, 14 lush)."""
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            if _d(x, z) <= LIGHT_R:
                g[(x, LIGHT_Y, z)] = LIGHT_BLOCK


# Light / spawn classes by block id (vanilla): transparent ids pass block light and are no spawn floor; free ids have no
# collision box a mob could not spawn in (plants and carpets count as free: the conservative reading).
_TRANSPARENT_SUFFIX = ('_leaves', '_stained_glass', 'mangrove_roots')
_FREE = {'air', 'light', 'dead_bush', 'short_dry_grass', 'tall_dry_grass', 'leaf_litter', 'azalea', 'flowering_azalea',
         'dandelion', 'moss_carpet'}
_EMIT = {'ochre_froglight': 15, 'verdant_froglight': 15, 'light': None}


def _bid(b):
    return b.split('[', 1)[0][10:]


def _opaque(b):
    n = _bid(b)
    return not (n in _FREE or n == 'barrier' or n.endswith(_TRANSPARENT_SUFFIX))


def _emits(b):
    n = _bid(b)
    if n == 'light':
        return int(b[b.index('level=') + 6:].rstrip(']'))
    return _EMIT.get(n) or 0


def _paint_spawn_lights(g):
    """Hidden light[level=15] blocks wherever a hostile mob could otherwise spawn in either look: a block-light flood
    (vanilla: -1 per step through non-opaque cells) from every light and froglight, then a light in each still-dark
    spawn cell (an opaque floor block with two free cells above), re-flooded after each one."""
    x0, y0, z0 = BOX['x0'] - 1, BOX['y0'] - 1, BOX['z0'] - 1
    nx, ny, nz = BOX['x1'] - BOX['x0'] + 3, BOX['y1'] - BOX['y0'] + 4, BOX['z1'] - BOX['z0'] + 3
    N = nx * ny * nz
    offs = (ny * nz, -ny * nz, nz, -nz, 1, -1)

    def idx(x, y, z):
        return ((x - x0) * ny + (y - y0)) * nz + (z - z0)

    def flood(opq, lv, seeds):
        buckets = [[] for _ in range(16)]
        for i in seeds:
            buckets[lv[i]].append(i)
        for L in range(15, 1, -1):
            nl = L - 1
            for i in buckets[L]:
                if lv[i] != L:
                    continue
                for o in offs:
                    j = i + o
                    if 0 <= j < N and not opq[j] and lv[j] < nl:
                        lv[j] = nl
                        buckets[nl].append(j)

    for look in (0, 1):
        cells = {c: (v[look] if isinstance(v, Lk) else v) for c, v in g.items()}
        cells = {c: v for c, v in cells.items() if v is not None}
        opq, lv = bytearray(N), bytearray(N)
        # the margin around the box (x / z sides and below) is opaque: no light leaks in from outside and the flat
        # index never wraps from one edge to the opposite one
        for xi in range(nx):
            for yi in range(ny):
                base = (xi * ny + yi) * nz
                if xi in (0, nx - 1) or yi == 0:
                    opq[base:base + nz] = b'\x01' * nz
                else:
                    opq[base] = opq[base + nz - 1] = 1
        seeds = []
        for (x, y, z), b in cells.items():
            i = idx(x, y, z)
            if _opaque(b):
                opq[i] = 1
            e = _emits(b)
            if e:
                lv[i] = e
                seeds.append(i)
        flood(opq, lv, seeds)

        def free(c):
            b = cells.get(c)
            return b is None or _bid(b) in _FREE
        spawn = sorted((x, y + 1, z) for (x, y, z), b in cells.items()
                       if opq[idx(x, y, z)] and free((x, y + 1, z)) and free((x, y + 2, z)))
        for (x, y, z) in spawn:
            if lv[idx(x, y, z)]:
                continue
            d = _d(x, z)
            if (d <= WALK and CLEAR_Y[0] <= y <= CLEAR_Y[1]) or y > BOX['y1'] or (d <= SHAFT_R + 0.6 and y >= CANOPY_Y[0]):
                continue                                # never here (the light layer / the shaft); the test reports it
            if (x, y, z) in cells:                      # a plant: the light goes into the free cell above it
                y += 1
                if (x, y, z) in cells or y > BOX['y1']:
                    continue
            g[(x, y, z)] = HIDDEN_LIGHT
            cells[(x, y, z)] = HIDDEN_LIGHT
            i = idx(x, y, z)
            lv[i] = 15
            flood(opq, lv, [i])


def _paint_barrier(g):
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            if BARRIER_D[0] < _d(x, z) <= BARRIER_D[1]:
                for y in range(BARRIER['y0'], BARRIER['y1'] + 1):
                    if (x, y, z) not in g:
                        g[(x, y, z)] = _p('barrier')


def _build_full():
    g = _Grid()
    _paint_ground(g)
    for t in TREES_FULL:
        _paint_tree(g, t)
    _paint_wall(g)
    _paint_canopy(g)
    for t in TREES_FULL:
        _paint_limbs(g, t)
    _paint_plants(g)
    _paint_lights(g)
    _paint_barrier(g)
    _paint_spawn_lights(g)
    return dict(g)


def _build_day1():
    """{cell: str | Lk} of the day-1 geometry (ap_contract.md §0.6.9)."""
    g = {}
    x0, z0, x1, z1 = (BOX[k] for k in ('x0', 'z0', 'x1', 'z1'))
    leaf = lk(B + 'pale_oak_leaves[persistent=true]', B + 'azalea_leaves[persistent=true]')
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            d = _d(x, z)
            if d <= WALK:
                for y in range(SOLID_Y0, FLOOR_Y):
                    g[(x, y, z)] = B + 'packed_mud'
                g[(x, FLOOR_Y, z)] = B + 'moss_block'
                if d <= LIGHT_R:
                    g[(x, LIGHT_Y, z)] = LIGHT_BLOCK
            elif d <= RAD + 1.0:
                top = ground_top(x, z)
                for y in range(196, top + 1):
                    g[(x, y, z)] = B + ('mossy_cobblestone' if y >= FLOOR_Y else 'packed_mud')
                if BARRIER_D[0] < d <= BARRIER_D[1]:
                    for y in range(max(top + 1, BARRIER['y0']), BARRIER['y1'] + 1):
                        g[(x, y, z)] = B + 'barrier'
            if d > SHAFT_R:
                g[(x, 230, z)] = leaf
    tx, ty, tz = TWIG_CELL
    g[(tx, ty, tz)] = B + 'mangrove_roots'
    return g


def _build():
    if 'cells' not in _CACHE:
        _CACHE['cells'] = _build_full() if GEOMETRY == 'full' else _build_day1()
    return _CACHE['cells']


def arena_layout(look=None):
    """{(x, y, z): block} of every non-air block of the arena box for `look` (None = 'withered')."""
    look = look or LOOKS[0]
    if look not in LOOKS:
        raise KeyError('ap_oasis has no look ' + repr(look))
    if look not in _CACHE:
        i = LOOKS.index(look)
        out = {}
        for c, v in _build().items():
            if isinstance(v, Lk):
                v = v[i]
            if v is not None:
                out[c] = v
        _CACHE[look] = out
    return dict(_CACHE[look])


def slices():
    """Build slices bottom up: 9 slabs over y 190..224 (4 layers, the last one 3) and 13 two-layer slabs over the canopy
    y 225..250 (its block mix needs more row spans per layer). 89 x 89 x 4 = 31 684 blocks at most."""
    out = []
    y = BOX['y0']
    while y <= BOX['y1']:
        step = 4 if y < CANOPY_Y[0] else 2
        y1 = min(y + step - 1, BOX['y1'], CANOPY_Y[0] - 1 if y < CANOPY_Y[0] else BOX['y1'])
        out.append(((BOX['x0'], y, BOX['z0']), (BOX['x1'], y1, BOX['z1'])))
        y = y1 + 1
    return out


# ---------------------------------------------------------------------------------------------------------------
# Looks: fill ... replace boxes (ap_contract.md §0.6.5)

def _vol(b):
    (x0, y0, z0), (x1, y1, z1) = b
    return (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)


def _look_pairs(look):
    """{(old, new): [cells]}: every cell whose block differs between the looks, keyed by the block it has in the other
    look (old; None = air) and the block it must get (new; None = air)."""
    i = LOOKS.index(look)
    pairs = {}
    for c, v in _build().items():
        if isinstance(v, Lk):
            pairs.setdefault((v[1 - i], v[i]), []).append(c)
    return pairs


def _cover(cells, forbidden, max_cells=None):
    """[(box, n)]: boxes (inclusive) covering every cell of `cells` (n of them in the box), none containing a cell of
    `forbidden`, each <= MAX_FILL blocks and <= max_cells cells: the bounding box, split in half along its longest axis
    until it is legal, then shrunk to its cells."""
    out = []
    todo = [list(cells)]
    while todo:
        cs = todo.pop()
        if not cs:
            continue
        lo = [min(c[k] for c in cs) for k in range(3)]
        hi = [max(c[k] for c in cs) for k in range(3)]
        box = (tuple(lo), tuple(hi))
        bad = (_vol(box) > MAX_FILL or (max_cells is not None and len(cs) > max_cells)
               or any(lo[0] <= f[0] <= hi[0] and lo[1] <= f[1] <= hi[1] and lo[2] <= f[2] <= hi[2] for f in forbidden))
        if not bad:
            out.append((box, len(cs)))
            continue
        ext = [hi[k] - lo[k] for k in range(3)]
        if max(ext) == 0:
            raise ValueError('a look cell is forbidden for its own pair: %r' % (cs[0],))
        k = ext.index(max(ext))
        mid = (lo[k] + hi[k]) // 2
        todo.append([c for c in cs if c[k] <= mid])
        todo.append([c for c in cs if c[k] > mid])
    return sorted(out)


def _look_boxes(look):
    """[(new, old, box, n)]: `fill box new replace old` commands (n = the cells it swaps) that move every cell of the other look (or of any mix of
    the two looks) to `look`. A box of the pair (old -> new) never contains a cell that may hold `old` (in either look)
    and must end as something else, so the commands commute and are idempotent."""
    i = LOOKS.index(look)
    cells = _build()
    holders = {}                       # block -> cells that hold it in some look but must end as another block
    for c, v in cells.items():
        if isinstance(v, Lk):
            holders.setdefault(v[1 - i], set()).add(c)
    out = []
    for (old, new), cs in sorted(_look_pairs(look).items(), key=lambda kv: (str(kv[0][0]), str(kv[0][1]))):
        if old is None:
            raise ValueError('ap_oasis looks only swap block types (no air -> block cells): %r' % (cs[0],))
        forb = [c for c in holders.get(old, ()) if _target(cells[c], i) != new]
        for box, n in _cover(cs, forb, LOOK_CELLS):
            out.append((new, old, box, n))
    return out


def _target(v, i):
    return v[i] if isinstance(v, Lk) else v


def look_lines(look):
    """[[cmd]] (one inner list per tick, <= 24): turns any built look into `look` (ap_contract.md §0.6.5)."""
    if look not in LOOKS:
        raise KeyError('ap_oasis has no look ' + repr(look))
    if look in _CACHE.get('lines', {}):
        return [list(t) for t in _CACHE['lines'][look]]
    mode = ' strict' if LOOK_STRICT else ''
    cmds = []
    for new, old, box, n in _look_boxes(look):
        (x0, y0, z0), (x1, y1, z1) = box
        cost = n + _vol(box) / 20.0               # swapped cells (updates) dominate; the scan of the box is cheap
        cmds.append((cost, 'fill %d %d %d %d %d %d %s replace %s%s' % (x0, y0, z0, x1, y1, z1, new, old, mode)))
    # balance: consecutive commands into ticks of about equal cost, as many ticks as the 24-tick budget allows
    budget = max(max(c for c, _ in cmds), sum(c for c, _ in cmds) / MAX_LOOK_SLICES)
    while True:
        ticks, cur, acc = [], [], 0.0
        for cost, c in cmds:
            if cur and acc + cost > budget:
                ticks.append(cur)
                cur, acc = [], 0.0
            cur.append(c)
            acc += cost
        if cur:
            ticks.append(cur)
        if len(ticks) <= MAX_LOOK_SLICES:
            break
        budget *= 1.05
    _CACHE.setdefault('lines', {})[look] = ticks
    return [list(t) for t in ticks]


# ---------------------------------------------------------------------------------------------------------------
# Props (per-fight display entities spawned by the boss module; ap_contract.md §0.6.6)

def props(look=None):
    look = look or LOOKS[0]
    if look not in LOOKS:
        raise KeyError('ap_oasis has no look ' + repr(look))
    out = []
    for i, (x, y, z) in enumerate(POINTS['bank_crystals']):
        yaw = yaw_facing(CX - x, CZ - z)
        out.append({'name': 'bank_crystal_%02d' % i, 'kind': 'bank_crystal', 'group': 'crystal', 'pos': (x, y, z),
                    'yaw': yaw, 'pitch': _r(-8.0 - 14.0 * _mix(i, 91), 1), 'scale': _r(1.1 + 0.7 * _mix(i, 92), 2),
                    'el': PROP_EL, 'uuid': 0x40 + i})
    if look == 'lush':
        for i, (x, y, z) in enumerate(POINTS['water_tiles']):
            out.append({'name': 'water_%d_%d' % (i % 4, i // 4), 'kind': 'water_sheet', 'group': 'water',
                        'pos': (x, y, z), 'yaw': 0.0, 'pitch': 0.0, 'scale': 14.0, 'el': PROP_EL, 'uuid': 0x00 + i})
        n = {}
        for i, (kind, (x, y, z)) in enumerate(POND_PROPS):
            n[kind] = n.get(kind, 0) + 1
            s = {'lily_pad': 0.9 + 0.6 * _mix(i, 93), 'bell_flower': 0.8 + 0.4 * _mix(i, 93),
                 'bulb_flower': 0.9 + 0.5 * _mix(i, 93)}[kind]
            out.append({'name': '%s_%02d' % (kind, n[kind] - 1), 'kind': kind, 'group': 'pond', 'pos': (x, y, z),
                        'yaw': _norm_yaw(360.0 * _mix(i, 94)), 'pitch': 0.0, 'scale': _r(s, 2), 'el': PROP_EL,
                        'uuid': 0x10 + i})
    return out


# ---------------------------------------------------------------------------------------------------------------
# Domain entrance (chapter-3 dungeon, theme.md §5, ap_contract.md §0.6.7)

def _cell(x0, z0, x1, z1, entry):
    ex0, ez0, ex1, ez1 = entry
    return {'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'ix0': x0 + 1, 'iz0': z0 + 1, 'ix1': x1 - 1, 'iz1': z1 - 1,
            'ex0': ex0 * 100, 'ez0': ez0 * 100, 'ex1': ex1 * 100, 'ez1': ez1 * 100,
            'sx0': x0 + 2, 'sz0': z0 + 2, 'sx1': x1 - 2, 'sz1': z1 - 2}


def _zone(zid, kind, box, centre, cells):
    x0, z0, x1, z1 = box
    return {'id': zid, 'kind': kind, 'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'cx': centre[0], 'cz': centre[1],
            'mn': 1, 'mx': 1, 'nc': len(cells), 'ncm': len(cells) - 1, 'cells': cells, 'by': 0, 'cy': 201, 'sd': 0,
            'pits': []}


FOYER = (-6, 24, 5, 39)                  # zone 1 (Raiden's foyer box), the player's spawn zone
HALL = (-10, 4, 9, 23)                   # zone 2 (kind 9): the domain entrance, gate at its centre
GATE = (0, 201, 14)
DOOR = {'a': 1, 'b': 2, 'x0': -2, 'x1': 1, 'z0': 23, 'z1': 24, 'mx': 0, 'mz': 24, 'ya': 0, 'yb': 180, 'h': 0,
        'y0': 201, 'y1': 205, 'l0': 206, 'l1': 207, 'my': 201, 'tx0': -2, 'tx1': 1, 'tz0': 24, 'tz1': 24, 'tm': 210}
ENT_CRYSTALS = {'crystal_w': (-3.5, 201.0, 12.5, 0.0), 'crystal_e': (3.5, 201.0, 12.5, 0.0)}
ENT_GLOW = (0.0, 203.5, 12.5)


def _entrance_blocks_full():
    """The chapter-3 domain entrance (Sumeru oasis gate): zone 1 a sandstone foyer with moss planters, zone 2 the gate
    hall: a mosaic plaza of rings around the gate (moss island, green tiles, sandstone with chiseled studs, a red
    sandstone ring), mud-brick walls with cut-sandstone courses and pilasters, planters of azalea along the walls, and
    on the north wall the oasis portal: a pointed arch whose panel is a giant leaf of lime / green terracotta cells with a
    glowing verdant-froglight midrib and veins, a chiseled frieze and a gold-emerald crown. Hidden light layers at y 208
    and the portal glow keep both zones lit (no spawns)."""
    out = {}
    door = {(x, z) for x in range(DOOR['x0'], DOOR['x1'] + 1) for z in range(DOOR['z0'], DOOR['z1'] + 1)}

    def walls(bl, x0, z0, x1, z1, top, pil):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if not (x in (x0, x1) or z in (z0, z1)):
                    continue
                along = z - z0 if x in (x0, x1) else x - x0
                pillar = along % pil == 0 or (x in (x0, x1) and z in (z0, z1))
                for y in range(201, top + 1):
                    if (x, z) in door:
                        if y >= DOOR['l0']:
                            bl[(x, y, z)] = B + 'cut_sandstone'
                        continue
                    if y == 201:
                        m = 'cut_sandstone'
                    elif y == top:
                        m = 'smooth_sandstone'
                    elif y == top - 1:
                        m = 'chiseled_sandstone' if pillar else 'cut_sandstone'
                    elif pillar:
                        m = 'cut_sandstone'
                    else:
                        m = 'mud_bricks'
                    bl[(x, y, z)] = B + m

    def floor(bl, x0, z0, x1, z1, pick):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                bl[(x, 199, z)] = B + 'sandstone'
                bl[(x, 200, z)] = B + pick(x, z)

    def planters(bl, cells, seed):
        for (x, z) in cells:
            bl[(x, 200, z)] = B + 'moss_block'
            h = _mix(x, z, seed)
            if h < 0.45:
                bl[(x, 201, z)] = B + 'azalea'
            elif h < 0.7:
                bl[(x, 201, z)] = B + 'flowering_azalea'
            elif h < 0.85:
                bl[(x, 201, z)] = B + 'moss_carpet'

    def lights(bl, x0, z0, x1, z1, y):
        for x in range(x0 + 2, x1 - 1, 4):
            for z in range(z0 + 2, z1 - 1, 4):
                if (x, y, z) not in bl:
                    bl[(x, y, z)] = B + 'light[level=15]'

    # zone 1: the foyer
    fx0, fz0, fx1, fz1 = FOYER
    z1 = {}

    def foyer_floor(x, z):
        if x in (fx0, fx1) or z in (fz0, fz1):
            return 'cut_sandstone'
        if x in (-1, 0):
            return 'cut_red_sandstone' if z % 3 else 'chiseled_sandstone'
        if x in (-2, 1):
            return 'cut_sandstone'
        return 'smooth_sandstone'
    floor(z1, fx0, fz0, fx1, fz1, foyer_floor)
    walls(z1, fx0, fz0, fx1, fz1, 207, 4)
    planters(z1, [(x, z) for x in (fx0 + 1, fx1 - 1) for z in range(fz0 + 2, fz1 - 1) if z % 4 != 0], 101)
    lights(z1, fx0, fz0, fx1, fz1, 208)
    out[1] = z1

    # zone 2: the gate hall
    hx0, hz0, hx1, hz1 = HALL
    gx, gz = GATE[0], GATE[2]
    z2 = {}

    def hall_floor(x, z):
        r = math.hypot(x + 0.5 - gx, z + 0.5 - gz)
        b = math.degrees(math.atan2(x + 0.5 - gx, -(z + 0.5 - gz))) % 360.0
        if x in (hx0, hx1) or z in (hz0, hz1):
            return 'cut_sandstone'
        if r <= 2.3:
            return 'moss_block'
        if r <= 3.1:
            return 'green_terracotta'
        if r <= 4.3:
            return 'chiseled_sandstone' if (b % 45.0) < 9.0 else 'smooth_sandstone'
        if r <= 5.1:
            return 'cut_red_sandstone'
        if r <= 5.9:
            return 'smooth_sandstone'
        if (x - hx0) % 5 == 0 or (z - hz0) % 5 == 0:
            return 'cut_sandstone'
        return 'smooth_sandstone'
    floor(z2, hx0, hz0, hx1, hz1, hall_floor)
    walls(z2, hx0, hz0, hx1, hz1, 208, 5)
    planters(z2, [(x, z) for x in (hx0 + 1, hx1 - 1) for z in range(hz0 + 3, hz1 - 1) if z % 5 != 4], 102)
    planters(z2, [(x, hz1 - 1) for x in range(hx0 + 2, hx1 - 1) if x not in range(DOOR['x0'] - 1, DOOR['x1'] + 2)], 103)
    # the north wall: the oasis portal (pointed arch) between two tall pillars, up to y 215
    acx = (hx0 + hx1 + 1) / 2.0                       # the arch axis x (0.0)

    def arch_top(x):
        u = abs(x + 0.5 - acx)
        return 201.0 + 9.4 - 0.22 * u * u if u <= 4.0 else None

    for x in range(hx0, hx1 + 1):
        u = abs(x + 0.5 - acx)
        for y in range(201, 216):
            at = arch_top(x)
            if u <= 4.0 and at is not None and y + 0.5 <= at:
                # the portal panel: a giant leaf (lime terracotta cells, green rim, glowing midrib and veins)
                yy = y + 0.5 - 201.0
                if u < 0.6:
                    m = 'verdant_froglight'                       # the glowing midrib
                elif at - (y + 0.5) < 1.0 or u > 3.4:
                    m = 'green_terracotta'                        # the leaf rim
                elif (yy - 0.9 * u) % 2.6 < 0.9:
                    m = 'green_terracotta'                        # lateral veins rising toward the tip
                else:
                    m = 'lime_terracotta'
                z2[(x, y, hz0)] = B + m
                continue
            if u <= 5.0 and at is not None and y + 0.5 <= at + 1.2:
                z2[(x, y, hz0)] = B + 'chiseled_sandstone'            # the arch frame
                if y < 211:
                    z2[(x, y, hz0 + 1)] = B + 'cut_sandstone'
                continue
            if 4.0 < u <= 6.0:
                m = 'chiseled_sandstone' if y in (201, 212) else 'cut_sandstone'
                z2[(x, y, hz0)] = B + m                       # the two portal pillars, two deep, up to y 212
                if y <= 212:
                    z2[(x, y, hz0 + 1)] = B + m
                continue
            if y <= 208:
                continue                                              # the plain wall (walls())
            if y <= 211 and u <= 8.0:
                z2[(x, y, hz0)] = B + ('chiseled_sandstone' if y == 211 else 'mud_bricks')
    # the crown over the portal: a frieze and a gold / emerald diamond
    for x in range(-3, 3):
        z2[(x, 212, hz0)] = B + 'chiseled_sandstone'
    for (x, y, m) in ((-1, 213, 'gold_block'), (0, 213, 'gold_block'), (-2, 213, 'smooth_sandstone'),
                      (1, 213, 'smooth_sandstone'), (-1, 214, 'emerald_block'), (0, 214, 'emerald_block'),
                      (-1, 215, 'gold_block'), (0, 215, 'gold_block')):
        z2[(x, y, hz0)] = B + m
    lights(z2, hx0, hz0, hx1, hz1, 209)
    # keep the gate column, the crystal spots and the glow point free
    for c in [(x, y, z) for x in (gx - 1, gx) for z in (gz - 1, gz) for y in range(201, 206)]:
        z2.pop(c, None)
    out[2] = z2
    return out


def _entrance_blocks_day1():
    out = {}
    for zid, (x0, z0, x1, z1) in ((1, FOYER), (2, HALL)):
        bl = {}
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                bl[(x, 199, z)] = B + 'sandstone'
                bl[(x, 200, z)] = B + ('cut_sandstone' if zid == 1 else 'smooth_sandstone')
                edge = x in (x0, x1) or z in (z0, z1)
                for y in range(201, 208):
                    if edge:
                        bl[(x, y, z)] = B + 'mud_bricks'
                if not edge:
                    bl[(x, 208, z)] = 'minecraft:light[level=15]'
        out[zid] = bl
    return out


def entrance_layout():
    """The domain entrance (theme.md §5 dict, the az_cavern key set + the optional door lintel blocks 'th')."""
    foyer = _zone(1, 0, FOYER, (0, 32), [_cell(*FOYER, (-4, 26, 4, 37))])
    hall = _zone(2, 9, HALL, (GATE[0], GATE[2]), [_cell(*HALL, (-8, 6, 8, 20))])
    cur = {'n': 2, 'zones': [foyer, hall], 'doors': [dict(DOOR)], 'spawn': {'x': 0, 'z': 33, 'yaw': 180},
           'spot': {'x': 0, 'z': 33}}
    clear = {1: [(FOYER[0], 199, FOYER[1], FOYER[2], 230, FOYER[3])],      # flat (x0, y0, z0, x1, y1, z1) boxes
             2: [(HALL[0], 199, HALL[1], HALL[2], 230, HALL[3])]}
    blocks = _entrance_blocks_full() if GEOMETRY == 'full' else _entrance_blocks_day1()
    return {'cur': cur, 'blocks': blocks, 'clear': clear, 'gate': GATE, 'glyphs': dict(ENT_CRYSTALS),
            'stele_glow': ENT_GLOW, 'th': {'lb': B + 'cut_sandstone', 'lb2': B + 'mud_bricks'}}


def render_hints():
    """Camera presets for the offline renderer (S:ap/arenarender)."""
    return {'arrival_eye': {'pos': (440.5, 202.62, 24.5), 'yaw': 180.0, 'pitch': -4.0},
            'entrance_eye': {'pos': (0.5, 202.62, 33.0), 'yaw': 180.0, 'pitch': -2.0}}
