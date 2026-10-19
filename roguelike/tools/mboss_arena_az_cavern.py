"""Arena theme `az_cavern`: 「복룡목」 아래, the earth-core rock bed of 야타용왕 (Azhdaha), chapter-1 boss.

Theme module (S:az/contract/theme.md): plain Python, stdlib only, deterministic, no side effects on import, never
writes files. The arena generator (tools/build_mboss_arena.py) imports `arena_layout`, `slices`, `SENTINEL`; the room
generator (tools/build_cboss_rooms.py) imports `entrance_layout`; the boss module imports `props` and `POINTS`.

The cavern (plan §2.2): a dark rock bed under the Dragon-Queller tree. Walk disc r 28 of full opaque floor blocks at
y 200 (tuff, polished tuff, smooth basalt, mud, packed mud, andesite pebbles, mossy cobblestone at the rim, a smooth-basalt
rock bed under the centre and yellow-terracotta Geo cracks) over a solid bowl (y 192..199 under r <= 20, the burrow sink
depth); a rough rock wall 28 < d <= 33 of tilted tuff / deepslate / smooth-basalt / dripstone strata whose face never
steps back below y 208 (no ledge a player can climb, no reachable cell beyond d 29.2, so nobody walks out of the oob
band) with the barrier cap filling every open ring cell at y 208..215; a vault (apex ~238, y 214 at r 30) roughened by
noise; 6 massive irregular pillars (deepslate bricks / polished blackstone bricks / tuff bricks, zigzag gold veins, a
plinth and a capital flaring into the vault) half sunk in the wall at r 30.7-31.2; 8 carved steles (3 x 5, chiseled tuff /
stone bricks, gold and glazed inlays) at the rim with open cells in front of their faces, the two southern ones carrying
the arrival glyphs; 3 broken drums at the wall foot (beyond the walk disc: the clearance rule wins over plan §2.2's
"r 25-27"); 16 gold crystal outcrops in alcoves on the cliff (froglight cores, glass shells, spikes; the six lower ones
hold the rim element-crystal props); 26 hanging gold-crystal clusters from the vault (tips >= y 216, denser to the north,
raw gold / gold cores, ochre-froglight or shroomlight glow, yellow / orange glass shells, pointed-dripstone tips);
golden roots (stripped jungle wood, mangrove roots) down the north wall and across the vault; five 1-deep rim pools of
real water in wall-foot recesses beyond r 28 (contained on every side); the hidden light[level=9] layer at y 206 over
r <= 27.5. No mob can spawn (the pack never turns natural spawning off): every open ring cell from y 208 up is barrier,
the rock envelope is a solid cylinder up to y 240 whose top layer is tinted glass, and every other upward surface in
the box has block light >= 1 (test_arena_az.py checks it with a light flood). The shallow-water look, the element crystals and the arrival glyphs are props (props(), theme.md §4.1).

The entrance (plan §2.3, entrance_layout()): Raiden's foyer box as zone 1 in plain Liyue stonework, and the kind-9 hall
x -10..9, z 4..23: a Liyue stone arch (andesite columns, dark-oak beam, gold trim, tiled roof, hanging lanterns) over the
gate at (0, 201, 14), gold Geo cracks radiating over the floor, a rough cliff with golden roots and the dark mouth of
the domain at the north side, and the tall dark glyph stele 3.5 b west of the gate (glyph spots on its south face).

Coordinates: the centre (320, 201, 8) is a block corner, floor blocks at y 200, stand height 201. A cell (x, z) is "at
distance d" when its centre (x + 0.5, z + 0.5) is d blocks from (320, 8) horizontally. Compass bearings (POINTS):
0 = north (-z), 90 = east (+x), 180 = south (+z, the arrival). Yaw is Minecraft's (0 faces +z, 90 faces -x).
"""
import math

THEME = 'az_cavern'
AID = 'az_cavern'

# Registry values this theme was written for (theme.md §6.1; the generator asserts equality when CHECK is present).
CX, CY, CZ = 320, 201, 8
WALK, SAFE, RAD = 28, 26, 33
BOX = {'x0': 280, 'y0': 190, 'z0': -32, 'x1': 360, 'y1': 240, 'z1': 48}
START = {'x': 320.5, 'y': 201.0, 'z': 34.5, 'yaw': 180.0, 'pitch': 0.0}
CHECK = {'cx': CX, 'cy': CY, 'cz': CZ, 'r': RAD, 'walk': WALK, 'safe': SAFE, 'box': dict(BOX), 'start': dict(START)}
LOOKS = ['default']
GEOMETRY = 'full'           # 'day1' (theme.md §6.5 flat floor, first commit) or 'full'

YF = CY - 1                 # floor blocks (y 200)
YLIGHT = 206                # hidden light layer
LIGHT = 'minecraft:light[level=9]'
SENTINEL = ((CX, 195, CZ), 'minecraft:smooth_basalt')

B = 'minecraft:'


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


def cell_polar(x, z):
    """(u, v, d, bearing) of the cell centre: u = east offset, v = south offset, compass bearing in degrees."""
    u, v = x + 0.5 - CX, z + 0.5 - CZ
    return u, v, math.hypot(u, v), math.degrees(math.atan2(u, -v)) % 360.0


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


# ---------------------------------------------------------------------------------------------------------------
# Rim and ceiling features (planned once, shared by the layout, the points and the props)

PILLAR_BEARINGS = (45.0, 90.0, 135.0, 225.0, 270.0, 315.0)
STELE_BEARINGS = (22.5, 67.5, 112.5, 157.5, 202.5, 247.5, 292.5, 337.5)
ARRIVAL_STELES = {'upper': 202.5, 'lower': 157.5}      # tail element on the west one, leg element on the east one
SEAL_BEARINGS = tuple(30.0 + 60.0 * k for k in range(6))
SEAL_R = 8.0
STELE_W, STELE_H = 3, 5                                 # carved face 3 wide x 5 high (y 201..205)


def _cardinal_inward(bearing):
    """Axis-aligned facing (dx, dz) closest to the direction from the rim point at `bearing` toward the centre."""
    a = math.radians((bearing + 180.0) % 360.0)
    fx, fz = math.sin(a), -math.cos(a)
    return (int(math.copysign(1, fx)), 0) if abs(fx) >= abs(fz) else (0, int(math.copysign(1, fz)))


def _stele_plan(bearing):
    """Tablet cells of the stele at `bearing`: the innermost axis-aligned 3-wide row whose cells are all beyond the walk
    disc (d > WALK + 0.3), so its carved face stands at the rim. Returns dict(face=(dx, dz), front=[(x, z)] (3 cells,
    the carved layer), back=[(x, z)], centre face point (x, z), yaw)."""
    fx, fz = _cardinal_inward(bearing)
    px, pz = polar_point(WALK + 1.0, bearing)
    wx, wz = -fz, fx                                     # width axis (perpendicular to the facing)
    cxi, czi = math.floor(px), math.floor(pz)
    # walk the tablet row outward (against the facing) until every cell clears the disc
    for step in range(0, 8):
        mx, mz = cxi - fx * step, czi - fz * step
        row = [(mx + wx * k, mz + wz * k) for k in (-1, 0, 1)]
        if all(cell_polar(x, z)[2] > WALK + 0.3 for x, z in row):
            break
    back = [(x - fx, z - fz) for x, z in row]
    # face plane: the boundary of the front cells on the facing side
    mx, mz = row[1]
    face_x = mx + 0.5 + 0.5 * fx
    face_z = mz + 0.5 + 0.5 * fz
    return {'face': (fx, fz), 'front': row, 'back': back, 'centre': (face_x, face_z),
            'yaw': yaw_facing(fx, fz), 'bearing': bearing}


STELES = [_stele_plan(b) for b in STELE_BEARINGS]


def _vnoise(x, z, scale, seed):
    """Smooth 2-D value noise in [0, 1] (bilinear smoothstep over a lattice of `scale` blocks)."""
    fx, fz = x / scale, z / scale
    ix, iz = math.floor(fx), math.floor(fz)
    tx, tz = fx - ix, fz - iz
    tx, tz = tx * tx * (3 - 2 * tx), tz * tz * (3 - 2 * tz)
    a, b = _mix(ix, iz, seed), _mix(ix + 1, iz, seed)
    c, d = _mix(ix, iz + 1, seed), _mix(ix + 1, iz + 1, seed)
    return (a * (1 - tx) + b * tx) * (1 - tz) + (c * (1 - tx) + d * tx) * tz


DOME_R = 30.0


def dome_y(x, z):
    """Ceiling height over the cell column (x, z): the dome (apex ~238, y 214 at d 30, rough by +-1.5 b) and beyond
    d 30 the low spring of the vault over the wall ring (214 falling 1.5 b per b). None beyond the ring. Cells with
    y + 0.5 < dome_y are under the ceiling (open where the wall allows, wall_r)."""
    d = cell_polar(x, z)[2]
    if d > RAD + 0.5:
        return None
    if d >= DOME_R:
        return 214.0 - 1.5 * (d - DOME_R)
    base = 214.0 + 24.0 * math.sqrt(1.0 - (d / DOME_R) ** 2)
    n = (_vnoise(x, z, 5.0, 3) - 0.5) * 3.0 + (_vnoise(x, z, 2.0, 4) - 0.5) * 0.8
    return min(238.4, base + n * min(1.0, (DOME_R - d) / 3.0))


def dome_top(x, z):
    """Highest cavity cell y in column (x, z) under the dome (None beyond the dome)."""
    y = dome_y(x, z)
    return None if y is None else math.ceil(y - 0.5) - 1


def _clusters():
    """Hanging gold-crystal clusters over the walk disc: [(x, z, top_y, tip_y, radius)] with integer column (x, z), top
    = the dome's lowest cavity cell above it, tip = the lowest block (>= y 216). Denser to the north (the root side),
    spaced >= 5.5 b, none within 4 b of the centre column."""
    out = []
    k = 0
    while len(out) < 26 and k < 4000:
        k += 1
        d = 4.0 + 23.5 * math.sqrt(_mix(k, 11))
        b = 360.0 * _mix(k, 12)
        w = 0.5 + 0.5 * math.cos(math.radians(b))     # north (b 0) about three times as likely as south
        if _mix(k, 13) > 0.35 + 0.65 * w:
            continue
        px, pz = polar_point(d, b)
        x, z = math.floor(px), math.floor(pz)
        if cell_polar(x, z)[2] > WALK - 0.5:
            continue
        if any(math.hypot(x - ox, z - oz) < 5.5 for ox, oz, *_ in out):
            continue
        top = dome_top(x, z)
        room = top - 216 + 1
        if room < 3:
            continue
        length = max(3, min(room, int(round(3 + 9 * _mix(k, 14) * min(1.0, room / 12.0)))))
        tip = top - length + 1
        rad = 1.0 + 1.3 * _mix(k, 15) * min(1.0, length / 8.0)
        out.append((x, z, top, tip, round(rad, 3)))
    return out


CLUSTERS = _clusters()

# Rim crystal outcrops: (bearing, y) on the wall between pillars and steles (the full version carves alcoves there).
RIM_CRYSTALS = ((5.0, 207), (100.0, 205), (192.0, 209), (238.0, 206), (282.0, 208), (348.0, 206))
# further gold outcrops high on the cliff (no props): (bearing, base y)
CLIFF_CRYSTALS = ((30.0, 211), (56.0, 212), (80.0, 210), (124.0, 212), (147.0, 211), (213.0, 212), (258.0, 211),
                  (302.0, 210), (326.0, 212), (355.0, 213))


def _crystal_points():
    """16 arena_crystal prop points: 10 hanging from the cluster tips with the most headroom (the prop hangs down from
    the block tip, scale <= tip - 216.2 so its own tip stays >= y 216), 6 in the rim crystal alcoves (r 28.9, on the
    alcove floor in front of the gold outcrop)."""
    pts = []
    cand = [c for c in CLUSTERS if c[3] >= 218]
    hang = [max(cand, key=lambda c: (cell_polar(c[0], c[1])[2], -c[0], -c[1]))]
    while len(hang) < 10:               # greedy farthest-point pick, so the element crystals spread over the ceiling
        hang.append(max((c for c in cand if c not in hang),
                        key=lambda c: (min(math.hypot(c[0] - h[0], c[1] - h[1]) for h in hang), c[3], -c[0], -c[1])))
    hang.sort(key=lambda c: (cell_polar(c[0], c[1])[3], c[0], c[1]))
    for x, z, top, tip, rad in hang:
        pts.append({'pos': (x + 0.5, float(tip), z + 0.5), 'hang': True, 'scale': _r(min(2.2, tip - 216.2), 2)})
    for i, (b, y) in enumerate(RIM_CRYSTALS):
        px, pz = polar_point(28.9, b)
        pts.append({'pos': (_r(px), float(y), _r(pz)), 'hang': False, 'scale': _r(1.6 + 0.6 * _mix(i, 41), 2),
                    'yaw': yaw_facing(CX - px, CZ - pz), 'pitch': _r(-12.0 - 10.0 * _mix(i, 42), 1)})
    return pts


CRYSTAL_POINTS = _crystal_points()


def _water_tiles():
    return [(float(x), 201.005, float(z)) for z in (-13, 1, 15, 29) for x in (299, 313, 327, 341)]


def _seal_steles():
    out = []
    for b in SEAL_BEARINGS:
        px, pz = polar_point(SEAL_R, b)
        out.append((_r(px), 201.0, _r(pz), _norm_yaw(b)))
    return out


def _stele_points():
    out = []
    for s in STELES:
        fx, fz = s['centre']
        out.append((_r(fx), 203.5, _r(fz), s['yaw']))
    return out


def _arrival_glyphs():
    out = {}
    for key, b in ARRIVAL_STELES.items():
        s = STELES[STELE_BEARINGS.index(b)]
        fx, fz = s['centre']
        dx, dz = s['face']
        out[key] = (_r(fx + 0.03 * dx), 203.5, _r(fz + 0.03 * dz), s['yaw'])
    return out


def _motes():
    big = sorted(CLUSTERS, key=lambda c: (-(c[2] - c[3]), c[0], c[1]))[:12]
    return [(c[0] + 0.5, float(c[3]) - 1.0, c[1] + 0.5) for c in big]


POINTS = {
    'spawn': (float(CX), float(CY), float(CZ), 0.0),
    'water_tiles': _water_tiles(),
    'crystals': [tuple(p['pos']) for p in CRYSTAL_POINTS],
    'steles': _stele_points(),
    'arrival_glyphs': _arrival_glyphs(),
    'seal_steles': _seal_steles(),
    'seal_prism': (float(CX), float(CY), float(CZ)),
    'crater': (float(CX), float(CY), float(CZ)),
    'motes': _motes(),
}


# ---------------------------------------------------------------------------------------------------------------
# Layout (full cavern geometry)
#
# The cavern = an open region carved from a rock envelope (every cell with d <= 33 from y 200 up to the roof, plus the
# bowl of fill under the floor). Open cells: y >= 201, under the dome surface (dome_y), and inside the walk disc or
# inside the wall face radius wall_r(bearing, y). At reachable heights (y 201..207) the face stays within d 29.2 and
# never steps back as it rises (the open cells at y + 1 are a subset of those at y), so the player can neither climb
# the rim nor walk out of the oob band (walk + 1.5); from y 208 to 215 the face may recede (rough overhangs) because the barrier cap
# fills every open ring cell there. Decor then overrides cells: pillars, steles (+ the open cells in front of their
# faces), stubs, rim crystal alcoves, golden roots, hanging gold crystal clusters, the floor and its Geo cracks, the
# rim pools, the light layer and the barrier cap. Rock that no open cell touches is plain tuff (fewer build commands).

PILLAR_MATS = ('deepslate_bricks', 'polished_blackstone_bricks', 'tuff_bricks',
               'deepslate_bricks', 'tuff_bricks', 'polished_blackstone_bricks')
STUB_BEARINGS = (32.0, 122.0, 304.0)
POOL_SECTORS = ((56.0, 61.5), (75.5, 84.0), (166.5, 175.5), (255.5, 264.0), (320.5, 330.0))
ROOT_WALL_BEARINGS = (347.0, 351.3, 355.6, 359.9, 4.2, 8.5, 12.8)
ROOT_DOME_BEARINGS = (350.0, 357.0, 4.0, 11.0)
STRATA = ('tuff', 'deepslate', 'tuff', 'smooth_basalt', 'tuff', 'dripstone_block', 'deepslate', 'tuff',
          'cobbled_deepslate', 'smooth_basalt', 'tuff', 'deepslate', 'tuff', 'dripstone_block')
NON_OPAQUE = ('light', 'barrier', 'water', 'yellow_stained_glass', 'orange_stained_glass', 'pointed_dripstone',
              'mangrove_roots')


def _vnoise3(x, y, z, scale, seed):
    """Smooth 3-D value noise in [0, 1] (trilinear smoothstep)."""
    fx, fy, fz = x / scale, y / scale, z / scale
    ix, iy, iz = math.floor(fx), math.floor(fy), math.floor(fz)
    tx, ty, tz = fx - ix, fy - iy, fz - iz
    tx, ty, tz = tx * tx * (3 - 2 * tx), ty * ty * (3 - 2 * ty), tz * tz * (3 - 2 * tz)
    acc = 0.0
    for dx, wx in ((0, 1 - tx), (1, tx)):
        for dy, wy in ((0, 1 - ty), (1, ty)):
            for dz, wz in ((0, 1 - tz), (1, tz)):
                acc += wx * wy * wz * _mix(ix + dx, iy + dy, iz + dz, seed)
    return acc


def _arc(b, scale, seed, y=None, r=28.6):
    """Noise along the rim circle (continuous across bearing 0 / 360); with y, 3-D over (circle, height)."""
    a = math.radians(b)
    if y is None:
        return _vnoise(r * math.cos(a), r * math.sin(a), scale, seed)
    return _vnoise3(r * math.cos(a), y * 1.0, r * math.sin(a), scale, seed)


def _in_sector(b, lo, hi):
    return (b - lo) % 360.0 <= (hi - lo) % 360.0


def _bdiff(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


def wall_r(b, y):
    """Radius of the rock face at bearing b and height y: cells with WALK < d <= wall_r are open."""
    low = 28.05 + 1.1 * _arc(b, 4.0, 61)
    if any(_in_sector(b, lo, hi) for lo, hi in POOL_SECTORS):
        low = 29.15
    low = min(low, 29.2)
    if y <= 203:
        return low
    if y <= 207:
        return low - 0.2 * (y - 203) * _arc(b, 3.0, 62)
    if y <= 215:
        return 28.2 + 1.3 * _arc(b, 6.0, 63, y)
    return 28.5 + 1.4 * _arc(b, 6.0, 64, y)


def _roof(x, z):
    """Top of the rock column (x, z): the whole envelope is a solid cylinder up to the box top, so the outside of the
    cavern has no ledge or dome step; its only upward faces are the y 240 layer, capped with tinted glass (no mob
    spawns on it, no light through it)."""
    return BOX['y1']


def _shell_top(x, z):
    """Where decor that runs up into the vault (pillar capitals) stops: two blocks into the rock above the cavity."""
    return min(BOX['y1'] - 1, math.floor(dome_y(x, z)) + 2)


def _rock(x, y, z):
    """Exposed rock: thick tilted strata of tuff / deepslate / smooth basalt / dripstone, rough clumps, moss at the foot."""
    s = y + 6.0 * (_vnoise(x, z, 14.0, 71) - 0.5) + 2.0 * (_vnoise(x + 2 * y, z - y, 6.0, 72) - 0.5)
    m = STRATA[int(_mix(math.floor(s / 4.5), 73) * len(STRATA))]
    h = _mix(x // 3, y // 3, z // 3, 74)
    if h < 0.07:
        m = 'cobbled_deepslate' if m != 'cobbled_deepslate' else 'tuff'
    elif h > 0.96:
        m = 'smooth_basalt' if m != 'smooth_basalt' else 'deepslate'
    if y <= 202 and _vnoise(x, z, 5.0, 75) > 0.62:
        m = 'mossy_cobblestone'
    return B + m


def _cracks():
    """Geo crack lines on the floor (yellow terracotta): 9 meandering cracks, some branching."""
    cells = set()
    for k in range(9):
        d0 = 4.5 + 17.0 * _mix(k, 101)
        b0 = 360.0 * _mix(k, 102)
        px, pz = polar_point(d0, b0)
        h = math.radians(360.0 * _mix(k, 103))
        n = 9 + int(9 * _mix(k, 104))
        branch = n // 2 if _mix(k, 105) < 0.5 else -1
        stack = [(px, pz, h, n, k * 100)]
        while stack:
            x, z, hd, steps, seed = stack.pop()
            for i in range(steps):
                c = (math.floor(x), math.floor(z))
                if cell_polar(*c)[2] <= WALK - 1.0:
                    cells.add(c)
                if i == branch and seed < 1000:
                    stack.append((x, z, hd + (0.9 if _mix(seed, 106) < 0.5 else -0.9), 5, seed + 1000))
                hd += (_mix(seed, i, 107) - 0.5) * 0.9
                x += math.cos(hd) * 0.9
                z += math.sin(hd) * 0.9
    return cells


CRACKS = frozenset(_cracks())


def _floor(x, z, d):
    if (x, z) in CRACKS:
        return B + 'yellow_terracotta'
    h = _mix(x, z, 23)
    if d <= 5.5:
        return B + ('smooth_basalt' if h < 0.88 else 'polished_tuff')
    if d <= 6.6:
        return B + 'polished_tuff'
    n1, n2 = _vnoise(x, z, 7.0, 21), _vnoise(x, z, 3.0, 22)
    if h < 0.035:
        return B + 'andesite'
    if d > 25.5 and n2 > 0.55:
        return B + 'mossy_cobblestone'
    if n1 > 0.74:
        return B + 'smooth_basalt'
    if n1 > 0.58 and n2 > 0.62:
        return B + 'mud'
    if n2 < 0.1:
        return B + 'packed_mud'
    if n1 > 0.45:
        return B + 'polished_tuff'
    return B + 'tuff'


def _pillars():
    out = []
    for i, b in enumerate(PILLAR_BEARINGS):
        rc = 30.7 + 0.5 * _mix(i, 81)
        rp = 2.6 + 0.6 * _mix(i, 82)
        out.append({'bearing': b, 'centre': polar_point(rc, b), 'r': rp, 'mat': PILLAR_MATS[i], 'seed': 800 + i,
                    'veins': [360.0 * _mix(i, j, 83) for j in range(3)]})
    return out


PILLARS = _pillars()


def _stubs():
    out = []
    for i, b in enumerate(STUB_BEARINGS):
        out.append({'bearing': b, 'centre': polar_point(29.15, b), 'r': 1.4, 'seed': 900 + i})
    return out


STUBS = _stubs()

_CACHE = {}


def _build_full():
    X0, X1, Z0, Z1, Y1 = BOX['x0'], BOX['x1'], BOX['z0'], BOX['z1'], BOX['y1']
    blocks, opened = {}, set()
    pol = {}
    # 1. rock envelope, fill and the open cavern
    for x in range(X0, X1 + 1):
        for z in range(Z0, Z1 + 1):
            u, v, d, b = cell_polar(x, z)
            if d > RAD:
                continue
            pol[(x, z)] = (d, b)
            dy = dome_y(x, z)
            roof = _roof(x, z)
            ybot = 192 if d <= 20.0 else int(round(192 + (d - 20.0) * 5.0 / 13.0))
            for y in range(ybot, 200):
                blocks[(x, y, z)] = B + ('smooth_basalt' if d <= 2.5 else 'tuff')
            for y in range(200, roof + 1):
                if 201 <= y < BOX['y1'] and y + 0.5 < dy and (d <= WALK or d <= wall_r(b, y)):
                    opened.add((x, y, z))
                else:
                    blocks[(x, y, z)] = 'R'

    def put(c, blk):
        if c[0] < X0 or c[0] > X1 or c[2] < Z0 or c[2] > Z1 or c[1] > Y1 or (c[0], c[2]) not in pol:
            return
        blocks[c] = blk
        opened.discard(c)

    def carve(c):
        if (c[0], c[2]) not in pol:
            return
        opened.add(c)
        blocks.pop(c, None)

    def guard(c):
        """Decor may not enter the walk disc below y 216."""
        return not (c[1] <= 215 and pol.get((c[0], c[2]), (0, 0))[0] <= WALK)

    # 2. rim crystal alcoves (carved first so pillars and steles keep their shapes): the six with element-crystal props
    #    and the higher cliff outcrops
    alcoves = []
    for i, (b0, y0) in enumerate(RIM_CRYSTALS + CLIFF_CRYSTALS):
        cells = []
        for (x, z), (d, b) in pol.items():
            if not (WALK < d <= 31.3) or _bdiff(b, b0) > 14.0:
                continue
            lat = d * math.radians(_bdiff(b, b0))
            for y in range(y0, y0 + 6):
                if lat <= 2.9 - 0.32 * (y - y0) + 0.5 * _mix(x, y, z, 111):
                    carve((x, y, z))
                    cells.append((x, y, z, d, lat))
        # a rock sill under the alcove mouth (the alcove never opens into the reachable band below)
        for (x, z), (d, b) in pol.items():
            if WALK < d <= 31.3 and _bdiff(b, b0) <= 14.0 and d * math.radians(_bdiff(b, b0)) <= 3.4:
                if (x, y0 - 1, z) in opened:
                    put((x, y0 - 1, z), 'R')
        alcoves.append((b0, y0, cells))

    # 3. pillars: irregular, half sunk in the wall, plinth below, capital flaring into the dome, gold vein lines
    for p in PILLARS:
        pcx, pcz = p['centre']
        base = B + p['mat']
        alt = {'deepslate_bricks': ('polished_deepslate', 'cracked_deepslate_bricks'),
               'polished_blackstone_bricks': ('polished_blackstone', 'cracked_polished_blackstone_bricks'),
               'tuff_bricks': ('polished_tuff', 'chiseled_tuff')}[p['mat']]
        for x in range(math.floor(pcx - 6), math.floor(pcx + 7)):
            for z in range(math.floor(pcz - 6), math.floor(pcz + 7)):
                if (x, z) not in pol:
                    continue
                dx, dz = x + 0.5 - pcx, z + 0.5 - pcz
                dist = math.hypot(dx, dz)
                ang = math.atan2(dz, dx)
                rr = p['r'] * (1.0 + 0.24 * (_vnoise(math.cos(ang) * 3 + 10, math.sin(ang) * 3, 1.6, p['seed']) - 0.5))
                top = _shell_top(x, z)
                for y in range(201, top + 1):
                    rad = rr + (0.7 if y <= 202 else 0.0) + (0.32 * (y - 211) if y > 211 else 0.0)
                    if dist > rad or not guard((x, y, z)):
                        continue
                    blk = base
                    if y % 5 == 0:
                        blk = B + alt[0]
                    elif _mix(x, y, z, p['seed']) < 0.16:
                        blk = B + alt[1]
                    if dist > rad - 1.0:
                        for j, va in enumerate(p['veins']):
                            vang = va + 40.0 * (_vnoise(y / 3.0, j * 5.0, 1.0, p['seed'] + 7) - 0.5)
                            if abs((math.degrees(ang) - vang + 180.0) % 360.0 - 180.0) * math.pi / 180.0 * rad < 0.42:
                                blk = B + ('gold_block' if _mix(x, y, z, 84) < 0.7 else 'raw_gold_block')
                    put((x, y, z), blk)

    # 4. stubs: broken drums of fallen pillars at the wall foot (h 1-2, beyond the walk disc)
    for s in STUBS:
        scx, scz = s['centre']
        for x in range(math.floor(scx - 3), math.floor(scx + 4)):
            for z in range(math.floor(scz - 3), math.floor(scz + 4)):
                if (x, z) not in pol or pol[(x, z)][0] <= WALK:
                    continue
                dist = math.hypot(x + 0.5 - scx, z + 0.5 - scz)
                if dist <= s['r']:
                    h = 2 if _mix(x, z, s['seed']) < 0.6 else 1
                    for y in range(201, 201 + h):
                        put((x, y, z), B + ('cracked_deepslate_bricks' if _mix(x, y, z, 85) < 0.4 else 'deepslate_bricks'))
                elif dist <= s['r'] + 1.2 and _mix(x, z, s['seed'] + 1) < 0.35:
                    put((x, 201, z), B + 'cobbled_deepslate')

    # 5. steles: carved 3 x 5 tablets at the rim, the cells in front of each face open
    for i, s in enumerate(STELES):
        fx, fz = s['face']
        chis = 'chiseled_tuff_bricks' if i % 2 == 0 else 'chiseled_stone_bricks'
        face = {205: (chis, 'chiseled_tuff', chis), 204: ('polished_tuff', 'gold_block', 'polished_tuff'),
                203: ('chiseled_tuff', 'yellow_glazed_terracotta', 'chiseled_tuff'),
                202: ('polished_tuff', chis, 'polished_tuff'), 201: ('tuff_bricks', 'tuff_bricks', 'tuff_bricks')}
        for k, (x, z) in enumerate(s['front']):
            for y in range(201, 206):
                put((x, y, z), B + face[y][k])
                carve((x + fx, y, z + fz))
            put((x, 206, z), B + 'tuff_bricks')
            put((x, 200, z), B + 'polished_tuff')
        for (x, z) in s['back']:
            for y in range(201, 207):
                put((x, y, z), B + 'polished_tuff')
        mx, mz = s['front'][1]
        put((mx, 207, mz), B + 'chiseled_tuff')

    # 6. rim crystal outcrops inside the alcoves: gold core and froglight at the back, glass shell, spikes fanning out
    for i, (b0, y0, cells) in enumerate(alcoves):
        for (x, y, z, d, lat) in cells:
            if d >= 30.2 and y <= y0 + 2 and lat <= 1.6:
                put((x, y, z), B + ('ochre_froglight' if (y == y0 + 1 and lat <= 0.7) else
                                    ('raw_gold_block' if _mix(x, y, z, 121) < 0.6 else 'gold_block')))
            elif d >= 29.5 and y <= y0 + 3 and lat <= 2.2 - 0.3 * (y - y0) and _mix(x, y, z, 122) < 0.75:
                put((x, y, z), B + ('yellow_stained_glass' if _mix(x, y, z, 123) < 0.7 else 'orange_stained_glass'))
        for sgn in (-1, 0, 1):
            for j in range(5 if sgn == 0 else 4):
                d = 30.6 - 0.42 * j
                bb = b0 + sgn * math.degrees((1.1 + 0.25 * j) / d)
                cx_, cz_ = polar_point(d, bb)
                c = (math.floor(cx_), y0 + 1 + j, math.floor(cz_))
                if pol.get((c[0], c[2]), (0, 0))[0] > WALK + 0.3:
                    put(c, B + ('gold_block' if j == 0 else 'yellow_stained_glass' if j < 3 else 'orange_stained_glass'))

    # 7. golden roots: strands down the north wall face, strands along the dome, root tendrils
    for k, b0 in enumerate(ROOT_WALL_BEARINGS):
        thick = 2 if k % 2 == 0 else 1
        mat = B + ('stripped_jungle_wood' if k % 2 == 0 else 'mangrove_roots')
        y_end = 203 + int(4 * _mix(k, 131))
        for y in range(222, y_end - 1, -1):
            w = 2.2 * (_vnoise(y / 4.0, k * 7.0, 1.0, 132) - 0.5)
            for t in range(thick):
                bb = b0 + math.degrees((w + t) / 28.6)
                for dd in [28.0 + 0.25 * q for q in range(1, 15)]:
                    cx_, cz_ = polar_point(dd, bb)
                    c = (math.floor(cx_), y, math.floor(cz_))
                    if c in blocks and blocks[c] == 'R':
                        put(c, B + 'gold_block' if _mix(c[0], c[1], c[2], 133) < 0.04 else mat)
                        break
                    if c in blocks:
                        break
    for k, b0 in enumerate(ROOT_DOME_BEARINGS):
        dirn = 1 if k % 2 == 0 else -1
        for i in range(0, 90):
            s_ = i / 89.0
            dd = 29.0 - 21.0 * s_
            bb = b0 + dirn * 22.0 * math.sin(math.pi * s_)
            for t in range(2 if k < 2 else 1):
                cx_, cz_ = polar_point(dd, bb + math.degrees(t / max(dd, 4.0)))
                x, z = math.floor(cx_), math.floor(cz_)
                if (x, z) not in pol:
                    continue
                top = dome_top(x, z)
                c = (x, top + 1, z)
                if c in blocks:
                    put(c, B + 'stripped_jungle_wood')
                if i % 9 == 4 and t == 0:
                    for j in range(1 + int(3 * _mix(k, i, 134))):
                        if top - j >= 217:
                            put((x, top - j, z), B + 'mangrove_roots')

    # 8. hanging gold crystal clusters (tips >= 216 over the walk disc) and their satellites
    prop_tips = {(round(p['pos'][0] - 0.5), round(p['pos'][2] - 0.5)) for p in CRYSTAL_POINTS if p['hang']}
    for ci, (cx_, cz_, top, tip, rad) in enumerate(CLUSTERS):
        length = top - tip + 1
        lean = (0.8 * (_mix(ci, 141) - 0.5), 0.8 * (_mix(ci, 142) - 0.5))
        glow = 'shroomlight' if ci % 3 == 2 else 'ochre_froglight'
        for x in range(cx_ - 4, cx_ + 5):
            for z in range(cz_ - 4, cz_ + 5):
                if (x, z) not in pol:
                    continue
                ct = dome_top(x, z)
                for y in range(ct, tip - 1, -1):
                    t = min(1.0, max(0.0, (top - y) / float(length)))
                    ax, az = cx_ + 0.5 + lean[0] * t, cz_ + 0.5 + lean[1] * t
                    dist = math.hypot(x + 0.5 - ax, z + 0.5 - az)
                    r = rad * (1.0 - t) ** 0.75 + 0.3
                    if (x, z) == (cx_, cz_) and dist > r:
                        dist = 0.0
                    if dist > r or y < 216:
                        continue
                    h = _mix(x, y, z, 143)
                    if dist < 0.45 * r:
                        blk = 'raw_gold_block' if h < 0.7 else 'gold_block'
                        if (x, z) == (cx_, cz_) and (top - y) % 3 == 1 and y > tip:
                            blk = glow
                    else:
                        blk = ('yellow_stained_glass' if h < 0.55 else 'orange_stained_glass' if h < 0.75
                               else 'gold_block' if h < 0.87 else 'raw_gold_block')
                    put((x, y, z), B + blk)
        if (cx_, cz_) not in prop_tips:
            put((cx_, tip, cz_), B + 'pointed_dripstone[thickness=tip,vertical_direction=down]')
        if rad >= 1.5:
            for si in range(2):
                ox = int(round(2.4 * math.cos(6.283 * _mix(ci, si, 144))))
                oz = int(round(2.4 * math.sin(6.283 * _mix(ci, si, 144))))
                x, z = cx_ + ox, cz_ + oz
                if (x, z) not in pol:
                    continue
                ct = dome_top(x, z)
                ln = 2 + int(3 * _mix(ci, si, 145))
                for j in range(ln):
                    y = ct - j
                    if y < 217:
                        break
                    put((x, y, z), B + ('gold_block' if j == 0 else 'yellow_stained_glass'))
                if ct - ln >= 216:
                    put((x, ct - ln, z), B + 'pointed_dripstone[thickness=tip,vertical_direction=down]')

    # 9. floor, rim floor and pools
    for (x, z), (d, b) in pol.items():
        c = (x, 200, z)
        if d <= WALK:
            blocks[c] = _floor(x, z, d)
        elif (x, 201, z) in opened and blocks.get(c) in (None, 'R'):
            if any(_in_sector(b, lo, hi) for lo, hi in POOL_SECTORS):
                blocks[c] = B + 'water'
            else:
                h = _mix(x, z, 151)
                blocks[c] = B + ('mossy_cobblestone' if h < 0.5 else 'mud' if h < 0.75 else 'tuff')
    for (x, z), (d, b) in pol.items():         # pool edges: wet mud / moss on the walk side
        if d <= WALK and any(blocks.get((x + dx, 200, z + dz)) == B + 'water'
                             for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1))):
            if (x, z) not in CRACKS:
                blocks[(x, 200, z)] = B + ('mud' if _mix(x, z, 152) < 0.5 else 'mossy_cobblestone')

    # 10. rock materials: exposed rock gets the strata, hidden rock plain tuff
    nonop = {B + n for n in NON_OPAQUE}
    for c, blk in list(blocks.items()):
        if blk != 'R':
            continue
        x, y, z = c
        exposed = False
        for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
            if n in opened or (n in blocks and blocks[n].split('[')[0] in nonop):
                exposed = True
                break
        blocks[c] = _rock(x, y, z) if exposed else B + 'tuff'

    # 11. hidden light layer, the barrier cap and the roof cap. The cap fills every open ring cell from y 208 up (the
    #     plaza's band 208..215 and the dark recesses of the vault spring above it): nothing can climb or spawn there.
    for (x, z), (d, b) in pol.items():
        if d <= WALK - 0.5:
            blocks[(x, YLIGHT, z)] = LIGHT
        elif d > WALK:
            for y in range(208, BOX['y1'] + 1):
                if (x, y, z) in opened:
                    blocks[(x, y, z)] = B + 'barrier'
        blocks[(x, BOX['y1'], z)] = B + 'tinted_glass'
    return blocks


def arena_layout(look=None):
    """{(x, y, z): block} of every non-air block of the arena box for `look` (None = 'default')."""
    look = look or LOOKS[0]
    if look not in LOOKS:
        raise KeyError('az_cavern has no look ' + repr(look))
    if look not in _CACHE:
        _CACHE[look] = _build_full()
    return dict(_CACHE[look])


def slices():
    """13 y-slabs of 4 layers (the last one 3) over the whole box, bottom up: 81 x 81 x 4 = 26 244 blocks each."""
    out = []
    y = BOX['y0']
    while y <= BOX['y1']:
        y1 = min(y + 3, BOX['y1'])
        out.append(((BOX['x0'], y, BOX['z0']), (BOX['x1'], y1, BOX['z1'])))
        y = y1 + 1
    return out


# ---------------------------------------------------------------------------------------------------------------
# Props (per-fight display entities, spawned by the boss module; theme.md §4.1, §6.3)

def props(look=None):
    look = look or LOOKS[0]
    if look not in LOOKS:
        raise KeyError('az_cavern has no look ' + repr(look))
    out = []
    for i, (x, y, z) in enumerate(POINTS['water_tiles']):
        out.append({'name': 'water_%d_%d' % (i % 4, i // 4), 'kind': 'water_sheet', 'group': 'water',
                    'pos': (x, y, z), 'yaw': 0.0, 'pitch': 0.0, 'scale': 14.0, 'el': 'fight', 'uuid': None})
    for i, p in enumerate(CRYSTAL_POINTS):
        s = p['scale']
        if p['hang']:
            # hanging: the kit crystal grows along local +y from its point; (s, -s, -s) turns it 180 deg about x
            rec = {'yaw': _norm_yaw(360.0 * _mix(i, 51)), 'pitch': 0.0, 'scale': (s, -s, -s)}
        else:
            rec = {'yaw': p['yaw'], 'pitch': p['pitch'], 'scale': s}
        out.append(dict({'name': 'crystal_%02d' % i, 'kind': 'arena_crystal', 'group': 'crystal',
                         'pos': p['pos'], 'el': 'fight', 'uuid': None}, **rec))
    for key in ('upper', 'lower'):
        x, y, z, yaw = POINTS['arrival_glyphs'][key]
        out.append({'name': 'glyph_' + key, 'kind': 'glyph', 'group': 'glyph_' + key, 'pos': (x, y, z),
                    'yaw': yaw, 'pitch': 0.0, 'scale': 0.9, 'el': 'fight', 'uuid': None})
    return out


# ---------------------------------------------------------------------------------------------------------------
# Domain entrance (chapter-1 dungeon, theme.md §5)

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
# the glyph stele: a tall dark obelisk 3.5 b west of the gate (left of the entering player), carved face south (z 15)
ENT_STELE = {'x': -4, 'z': 14, 'y0': 201, 'y1': 208}
ENT_GLYPHS = {'upper': (-3.5, 205.3, 15.03, 0.0), 'lower': (-3.5, 203.9, 15.03, 0.0)}
ENT_GLOW = (-3.5, 204.6, 15.4)
ARCH = {'x0': -8, 'x1': 7, 'z0': 13, 'z1': 14}            # the Liyue stone arch over the gate: columns at x0 and x1


def _box(d, x0, y0, z0, x1, y1, z1, blk):
    for x in range(min(x0, x1), max(x0, x1) + 1):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            for z in range(min(z0, z1), max(z0, z1) + 1):
                d[(x, y, z)] = blk


def _brick(x, y, z, seed):
    h = _mix(x, y, z, seed)
    return B + ('cracked_stone_bricks' if h < 0.12 else 'mossy_stone_bricks' if h < 0.22 else 'stone_bricks')


def _liyue_walls(d, x0, z0, x1, z1, seed, skip=()):
    """Perimeter wall of a zone: andesite plinth, brick courses, a dark-oak beam course, brick cap, oak corner posts."""
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if not (x in (x0, x1) or z in (z0, z1)) or (x, z) in skip:
                continue
            corner = x in (x0, x1) and z in (z0, z1)
            for y in range(201, 209):
                if corner:
                    blk = B + ('gold_block' if y == 208 else 'dark_oak_log[axis=y]')
                elif y == 201:
                    blk = B + 'polished_andesite'
                elif y == 206:
                    blk = B + ('stripped_dark_oak_log[axis=x]' if z in (z0, z1) else 'stripped_dark_oak_log[axis=z]')
                elif y == 208:
                    blk = B + 'polished_andesite'
                else:
                    blk = _brick(x, y, z, seed)
                d[(x, y, z)] = blk


def _hall_cracks():
    """Gold Geo cracks on the hall floor radiating from the gate plaza."""
    cells = {}
    for k in range(6):
        a = math.radians(30.0 + 60.0 * k + 25.0 * (_mix(k, 161) - 0.5))
        x, z = 0.0 + 3.2 * math.cos(a), 14.0 + 3.2 * math.sin(a)
        for i in range(14):
            c = (math.floor(x), math.floor(z))
            if HALL[0] + 1 <= c[0] <= HALL[2] - 1 and HALL[1] + 3 <= c[1] <= HALL[3] - 1:
                cells[c] = B + ('gold_block' if _mix(k, i, 162) < 0.12 else 'yellow_terracotta')
            a += (_mix(k, i, 163) - 0.5) * 0.8
            x += math.cos(a) * 0.9
            z += math.sin(a) * 0.9
    return cells


def _entrance_blocks():
    z1, z2 = {}, {}
    # ---- zone 1: the foyer (spawn), plain Liyue stonework
    fx0, fz0, fx1, fz1 = FOYER
    _box(z1, fx0, 199, fz0, fx1, 199, fz1, B + 'polished_andesite')
    for x in range(fx0, fx1 + 1):
        for z in range(fz0, fz1 + 1):
            edge = x in (fx0, fx1) or z in (fz0, fz1)
            if edge or x in (fx0 + 1, fx1 - 1) or z in (fz0 + 1, fz1 - 1):
                z1[(x, 200, z)] = _brick(x, 200, z, 171)
            elif -2 <= x <= 1:
                z1[(x, 200, z)] = B + ('chiseled_stone_bricks' if z % 4 == 0 else 'polished_andesite')
            else:
                z1[(x, 200, z)] = B + ('stone' if _mix(x, z, 172) < 0.5 else 'andesite')
            if not edge:
                z1[(x, 208, z)] = 'minecraft:light[level=15]'
    _liyue_walls(z1, fx0, fz0, fx1, fz1, 173)
    # ---- zone 2: the domain hall
    hx0, hz0, hx1, hz1 = HALL
    _box(z2, hx0, 199, hz0, hx1, 199, hz1, B + 'polished_andesite')
    cracks = _hall_cracks()
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            r = math.hypot(x + 0.5 - GATE[0], z + 0.5 - GATE[2])
            if (x, z) in cracks:
                blk = cracks[(x, z)]
            elif r <= 2.6:
                blk = B + ('chiseled_stone_bricks' if r <= 1.5 else 'polished_andesite')
            elif r <= 3.4:
                blk = B + 'polished_andesite'
            elif -2 <= x <= 1 and z > GATE[2]:
                blk = B + ('chiseled_stone_bricks' if z % 4 == 1 else 'polished_andesite')
            else:
                blk = _brick(x, 200, z, 181)
            z2[(x, 200, z)] = blk
            if hx0 < x < hx1 and hz0 + 2 < z < hz1:
                z2[(x, 208, z)] = 'minecraft:light[level=15]'
    _liyue_walls(z2, hx0, hz0, hx1, hz1, 182)
    # the north side: a rough rock cliff with golden roots and the dark mouth of the domain behind the gate
    for x in range(hx0, hx1 + 1):
        for z in (hz0, hz0 + 1, hz0 + 2):
            depth = z - hz0
            top = {0: 212, 1: 206 + int(5 * _vnoise(x, 0, 3.0, 191)), 2: 201 + int(4 * _vnoise(x, 7, 2.5, 192))}[depth]
            if depth == 2 and _mix(x, 193) < 0.3:
                continue
            for y in range(201, top + 1):
                h = _vnoise3(x, y, z, 2.5, 194)
                blk = 'tuff' if h < 0.45 else 'deepslate' if h < 0.7 else 'cobbled_deepslate' if h < 0.85 else 'mossy_cobblestone'
                z2[(x, y, z)] = B + blk
    for x in range(-2, 2):                       # the domain mouth: a dark niche framed with gold
        for z in (hz0 + 1, hz0 + 2):
            for y in range(201, 207):
                z2.pop((x, y, z), None)
        for y in range(201, 207):
            z2[(x, y, hz0)] = B + 'black_concrete'
    for y in range(201, 208):
        for x in (-3, 2):
            z2[(x, y, hz0 + 1)] = B + ('gold_block' if y in (201, 207) else 'polished_blackstone_bricks')
    _box(z2, -3, 207, hz0 + 1, 2, 207, hz0 + 1, B + 'polished_blackstone_bricks')
    _box(z2, -1, 207, hz0 + 1, 0, 207, hz0 + 1, B + 'gold_block')
    for k, x in enumerate((-8, -5, 4, 7)):       # root strands down the cliff
        for y in range(212, 202 + int(3 * _mix(k, 195)), -1):
            xx = x + int(round(1.2 * (_vnoise(y / 3.0, k, 1.0, 196) - 0.5)))
            for z in (hz0, hz0 + 1, hz0 + 2):
                if (xx, y, z + 1) not in z2 or z == hz0 + 2:
                    if (xx, y, z) in z2:
                        z2[(xx, y, z)] = B + 'stripped_jungle_wood'
                    break
    # the Liyue stone arch over the gate: andesite columns, oak beam, gold trim, tiled roof, hanging lanterns
    ax0, ax1, az0, az1 = ARCH['x0'], ARCH['x1'], ARCH['z0'], ARCH['z1']
    for x in (ax0, ax1):
        for z in (az0, az1):
            for y in range(201, 210):
                z2[(x, y, z)] = B + ('stone_bricks' if y == 201 else 'chiseled_stone_bricks' if y == 209
                                     else 'polished_andesite')
    for x in range(ax0 - 1, ax1 + 2):
        for z in (az0, az1):
            z2[(x, 210, z)] = B + ('gold_block' if x in (ax0 - 1, ax1 + 1) else 'stripped_dark_oak_log[axis=x]')
            z2[(x, 211, z)] = B + ('gold_block' if x in (-1, 0) and z == az1 else 'dark_oak_planks')
    for x in range(ax0 - 2, ax1 + 3):
        z2[(x, 212, az0 - 1)] = B + 'deepslate_tile_stairs[facing=south,half=bottom]'
        z2[(x, 212, az1 + 1)] = B + 'deepslate_tile_stairs[facing=north,half=bottom]'
        for z in (az0, az1):
            z2[(x, 212, z)] = B + 'deepslate_tiles'
            z2[(x, 213, z)] = B + ('gold_block' if x in (ax0 - 2, ax1 + 2) else 'deepslate_tile_slab[type=bottom]')
    for x in (-6, 5):
        z2[(x, 209, az1)] = B + 'lantern[hanging=true]'
    # the glyph stele: dark obelisk on a plinth, gilded band, gold emblem on top
    sx, sz = ENT_STELE['x'], ENT_STELE['z']
    _box(z2, sx - 1, 201, sz, sx + 1, 201, sz + 1, B + 'polished_blackstone_bricks')
    for y in range(202, ENT_STELE['y1'] + 1):
        z2[(sx, y, sz)] = B + ('gilded_blackstone' if y == 207 else 'chiseled_polished_blackstone' if y == 202
                               else 'polished_blackstone')
    z2[(sx, ENT_STELE['y1'] + 1, sz)] = B + 'gold_block'
    # a stone lantern balancing the stele east of the gate
    z2[(4, 201, 14)] = B + 'stone_bricks'
    z2[(4, 202, 14)] = B + 'polished_andesite'
    z2[(4, 203, 14)] = B + 'lantern[hanging=false]'
    return {1: z1, 2: z2}


def entrance_layout():
    foyer = _zone(1, 0, FOYER, (0, 32), [_cell(*FOYER, (-4, 26, 4, 37))])
    hall = _zone(2, 9, HALL, (GATE[0], GATE[2]), [_cell(*HALL, (-8, 6, 8, 20))])
    cur = {'n': 2, 'zones': [foyer, hall], 'doors': [dict(DOOR)], 'spawn': {'x': 0, 'z': 33, 'yaw': 180},
           'spot': {'x': 0, 'z': 33}}
    clear = {1: [(FOYER[0], 199, FOYER[1], FOYER[2], 230, FOYER[3])],      # flat (x0, y0, z0, x1, y1, z1) boxes
             2: [(HALL[0], 199, HALL[1], HALL[2], 230, HALL[3])]}
    return {'cur': cur, 'blocks': _entrance_blocks(), 'clear': clear, 'gate': GATE,
            'glyphs': dict(ENT_GLYPHS), 'stele_glow': ENT_GLOW,
            'th': {'lb': B + 'stone_bricks', 'lb2': B + 'polished_andesite'}}


def render_hints():
    """Camera presets for the offline renderer (S:az/arenarender)."""
    return {'arrival_eye': {'pos': (320.5, 202.62, 34.5), 'yaw': 180.0, 'pitch': -4.0},
            'entrance_eye': {'pos': (0.5, 202.62, 30.5), 'yaw': 180.0, 'pitch': -4.0}}
