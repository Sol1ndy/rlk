"""Arena theme `az_cavern`: 「복룡목」 아래, the earth-core rock bed of 야타용왕 (Azhdaha), chapter-1 boss.

Theme module (S:az/contract/theme.md): plain Python, stdlib only, deterministic, no side effects on import, never
writes files. The arena generator (tools/build_mboss_arena.py) imports `arena_layout`, `slices`, `SENTINEL`; the room
generator (tools/build_cboss_rooms.py) imports `entrance_layout`; the boss module imports `props` and `POINTS`.

DAY-1 VERSION (theme.md §6.5): the full interface with simple geometry so the chapter mode and the module can
integrate: a flat polished-tuff floor at y 200 over the walk disc, solid tuff y 192..199 under distance <= 14 (a
smooth-basalt core under the centre carries the sentinel), a smooth-basalt wall ring 28 < d <= 33 up to y 214 with the
barrier cap at y 215, the hidden light layer at y 206, and a plain stone-brick entrance with a dark stele block.
Points and props are at their final positions.

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
GEOMETRY = 'day1'           # 'day1' (theme.md §6.5 flat floor) or 'full'

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
    """Inner dome surface height over the cell column (x, z): apex ~238, rim y 214 at d 30, rough by +-1.5 b; None
    beyond d 30 (no dome cavity there). Cells with y + 0.5 < dome_y are inside the cavern."""
    d = cell_polar(x, z)[2]
    if d >= DOME_R:
        return None
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


def _crystal_points():
    """16 arena_crystal prop points: 10 hanging from the cluster tips with the most headroom (the prop hangs down from
    the block tip, scale <= tip - 216.2 so its own tip stays >= y 216), 6 on the rim outcrops (r 29.4)."""
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
        px, pz = polar_point(29.4, b)
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
# Layout (day-1 geometry)

_CACHE = {}


def _build_default():
    blocks = {}
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            _, _, d, _ = cell_polar(x, z)
            if d > RAD:
                continue
            if d <= 14.0:
                core = d <= 2.0
                for y in range(192, 200):
                    blocks[(x, y, z)] = B + ('smooth_basalt' if core else 'tuff')
            else:
                blocks[(x, 199, z)] = B + 'tuff'
            if d <= WALK:
                blocks[(x, YF, z)] = B + 'polished_tuff'
                if d <= WALK - 0.5:
                    blocks[(x, YLIGHT, z)] = LIGHT
            else:
                for y in range(YF, 215):
                    blocks[(x, y, z)] = B + 'smooth_basalt'
                blocks[(x, 215, z)] = B + 'barrier'
    # the stele tablets (plain on day 1: polished tuff faces)
    for s in STELES:
        for (x, z) in s['front']:
            for y in range(201, 201 + STELE_H):
                blocks[(x, y, z)] = B + 'polished_tuff'
    return blocks


def arena_layout(look=None):
    """{(x, y, z): block} of every non-air block of the arena box for `look` (None = 'default')."""
    look = look or LOOKS[0]
    if look not in LOOKS:
        raise KeyError('az_cavern has no look ' + repr(look))
    if look not in _CACHE:
        _CACHE[look] = _build_default()
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
ENT_STELE = {'x0': -5, 'x1': -4, 'z': 14, 'y0': 201, 'y1': 207}      # the glyph stele, 4 b west of the gate, face south
ENT_GLYPHS = {'upper': (-4.0, 205.2, 15.03, 0.0), 'lower': (-4.0, 203.7, 15.03, 0.0)}
ENT_GLOW = (-4.0, 204.4, 15.4)


def _entrance_blocks_day1():
    z1 = {}
    fx0, fz0, fx1, fz1 = FOYER
    for x in range(fx0, fx1 + 1):
        for z in range(fz0, fz1 + 1):
            z1[(x, 199, z)] = B + 'polished_andesite'
            z1[(x, 200, z)] = B + 'stone_bricks'
            edge = x in (fx0, fx1) or z in (fz0, fz1)
            for y in range(201, 208):
                if edge:
                    z1[(x, y, z)] = B + 'stone_bricks'
            if not edge:
                z1[(x, 218, z)] = 'minecraft:light[level=15]'
    z2 = {}
    hx0, hz0, hx1, hz1 = HALL
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            z2[(x, 199, z)] = B + 'polished_andesite'
            z2[(x, 200, z)] = B + 'stone_bricks'
            edge = x in (hx0, hx1) or z in (hz0, hz1)
            for y in range(201, 208):
                if edge:
                    z2[(x, y, z)] = B + 'stone_bricks'
            if not edge:
                z2[(x, 218, z)] = 'minecraft:light[level=15]'
    s = ENT_STELE
    for x in range(s['x0'], s['x1'] + 1):
        for y in range(s['y0'], s['y1'] + 1):
            z2[(x, y, s['z'])] = B + 'polished_blackstone'
    return {1: z1, 2: z2}


def entrance_layout():
    foyer = _zone(1, 0, FOYER, (0, 32), [_cell(*FOYER, (-4, 26, 4, 37))])
    hall = _zone(2, 9, HALL, (GATE[0], GATE[2]), [_cell(*HALL, (-8, 6, 8, 20))])
    cur = {'n': 2, 'zones': [foyer, hall], 'doors': [dict(DOOR)], 'spawn': {'x': 0, 'z': 33, 'yaw': 180},
           'spot': {'x': 0, 'z': 33}}
    clear = {1: [((FOYER[0], 201, FOYER[1]), (FOYER[2], 230, FOYER[3]))],
             2: [((HALL[0], 201, HALL[1]), (HALL[2], 230, HALL[3]))]}
    return {'cur': cur, 'blocks': _entrance_blocks_day1(), 'clear': clear, 'gate': GATE,
            'glyphs': dict(ENT_GLYPHS), 'stele_glow': ENT_GLOW}


def render_hints():
    """Camera presets for the offline renderer (S:az/arenarender)."""
    return {'arrival_eye': {'pos': (320.5, 202.62, 34.5), 'yaw': 180.0, 'pitch': -4.0},
            'entrance_eye': {'pos': (0.5, 202.62, 30.5), 'yaw': 180.0, 'pitch': -4.0}}
