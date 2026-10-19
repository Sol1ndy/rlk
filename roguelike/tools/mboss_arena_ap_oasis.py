"""Arena theme `ap_oasis`: the forest lake of 아펩의 오아시스 파수꾼 (Guardian of Apep's Oasis), chapter-3 boss.

Theme module (S:az/contract/theme.md, S:ap/ap_contract.md §0.6): plain Python, stdlib only, deterministic, no side
effects on import, never writes files. The arena generator (tools/build_mboss_arena.py) imports `arena_layout`,
`slices`, `look_lines`, `SENTINEL`; the room generator (tools/build_cboss_rooms.py) imports `entrance_layout`; the boss
module imports `props`, `POINTS` and the constants.

DAY-1 VERSION (ap_contract.md §0.6.9): the full interface with simple geometry: a flat moss floor at y 200 over solid
packed mud y 192..199 inside r 26, a mossy-cobblestone bank 26 < r <= 29, the rim barrier wall, the light layer, and a
flat canopy at y 230 outside the sky shaft whose leaf type is the look diff (pale oak <-> azalea).

Coordinates: the centre (440, 201, 8) is a block corner, floor blocks at y 200, stand height 201. A cell (x, z) is "at
distance d" when its centre (x + 0.5, z + 0.5) is d blocks from (440, 8) horizontally. Compass bearings (POINTS):
0 = north (-z), 90 = east (+x), 180 = south (+z, the arrival). Yaw is Minecraft's (0 faces +z, 90 faces -x).

Looks: 'withered' (phase 1 and 2, the default restored by `ensure`) and 'lush' (phase 3, from the CS white-out). The
floor is identical in both; the looks differ only in swapped block types (canopy leaves / glass, bank decor, bulbs) and
the light level of the hidden light layer. `look_lines(look)` turns any built look (or any mix of the two) into `look`
with `fill <box> <new> replace <old>` commands (each box <= 32 768 blocks, <= 24 ticks).
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
GEOMETRY = 'day1'             # 'day1' (ap_contract.md §0.6.9) or 'full'

FLOOR_Y, SOLID_Y0 = 200, 192  # full opaque blocks only, solid y 192..200 inside r 26 (the rig root sinks to y 195)
RIM = (26, 29)                # the root / rock bank
BARRIER = {'r0': 27, 'r1': 28, 'y0': 201, 'y1': 215}
BARRIER_D = (26.9, 28.3)      # barrier cells: centre distance in (26.9, 28.3] (a closed 8-connected ring, r 27..28)
CLEAR_Y = (201, 224)          # inside r 26 only air and the light layer
CANOPY_Y = (225, 250)
SHAFT_R = 8
LIGHT_Y = 206
LIGHT = {'withered': 12, 'lush': 14}
LIGHT_R = 25.5                # the light layer covers cells with centre distance <= 25.5
WATER_Y, DECAL_Y_MIN = 201.005, 201.035
MAX_LOOK_SLICES, SLICE_MS = 24, 20
MAX_FILL = 32768
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


class Lk(tuple):
    """A look-dependent cell value: Lk((withered, lush)); None = air in that look."""
    __slots__ = ()


def lk(withered, lush):
    return withered if withered == lush else Lk((withered, lush))


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


EMBER_TWIG = (432.6, 203.5, -19.6)          # a bank twig at r ~28.6, compass 345 (behind the boss for the arrival)

# day-1 trees: 9 trunks at r 30-38 (the full geometry keeps the list)
TREES = [(_r(polar_point(34.0 + 3.0 * math.sin(k * 1.7), 20.0 + 40.0 * k)[0], 2),
          _r(polar_point(34.0 + 3.0 * math.sin(k * 1.7), 20.0 + 40.0 * k)[1], 2), 2.5) for k in range(9)]


def _bank_crystals():
    """12 gold crystal spikes on the bank (r 27.2-28.6, between the barrier cells' centres), both looks."""
    out = []
    for k in range(12):
        b = 15.0 + 30.0 * k + 8.0 * (_mix(k, 71) - 0.5)
        d = 27.4 + 1.0 * _mix(k, 72)
        x, z = polar_point(d, b)
        out.append((_r(x, 2), float(CY), _r(z, 2)))
    return out


def _pond_props():
    """Lush pond dressing beyond r 22: lily pads on the water sheet (r 22.5-25.5) and bell / bulb flowers on the bank."""
    out = []
    for k in range(20):
        b = 9.0 + 18.0 * k + 10.0 * (_mix(k, 81) - 0.5)
        d = 22.6 + 2.8 * _mix(k, 82)
        x, z = polar_point(d, b)
        out.append(('lily_pad', (_r(x, 2), 201.012, _r(z, 2))))
    for k in range(10):
        b = 30.0 + 36.0 * k + 12.0 * (_mix(k, 83) - 0.5)
        d = 26.3 + 0.5 * _mix(k, 84)
        x, z = polar_point(d, b)
        out.append(('bell_flower', (_r(x, 2), float(CY), _r(z, 2))))
    for k in range(6):
        b = 60.0 * k + 40.0 + 10.0 * (_mix(k, 85) - 0.5)
        d = 26.2 + 0.4 * _mix(k, 86)
        x, z = polar_point(d, b)
        out.append(('bulb_flower', (_r(x, 2), float(CY), _r(z, 2))))
    return out


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
    'pond_props': [p for _, p in _pond_props()],
    'bank_crystals': _bank_crystals(),
    'trees': list(TREES),
    'motes': _motes(),
}


# ---------------------------------------------------------------------------------------------------------------
# Layout

_CACHE = {}


def _build_day1():
    """{cell: str | Lk} of the day-1 geometry (ap_contract.md §0.6.9)."""
    g = {}
    x0, y0, z0, x1, y1, z1 = (BOX[k] for k in ('x0', 'y0', 'z0', 'x1', 'y1', 'z1'))
    light = lk(B + 'light[level=%d]' % LIGHT['withered'], B + 'light[level=%d]' % LIGHT['lush'])
    leaf = lk(B + 'pale_oak_leaves[persistent=true]', B + 'azalea_leaves[persistent=true]')
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            _, _, d, _ = cell_polar(x, z)
            if d <= WALK:
                for y in range(SOLID_Y0, FLOOR_Y):
                    g[(x, y, z)] = B + 'packed_mud'
                g[(x, FLOOR_Y, z)] = B + 'moss_block'
                if d <= LIGHT_R:
                    g[(x, LIGHT_Y, z)] = light
            elif d <= RAD + 1.0:
                for y in range(196, FLOOR_Y + 1):
                    g[(x, y, z)] = B + 'packed_mud'
                top = FLOOR_Y + (1 if d > 27.5 else 0)
                for y in range(FLOOR_Y, top + 1):
                    g[(x, y, z)] = B + 'mossy_cobblestone'
                if BARRIER_D[0] < d <= BARRIER_D[1]:
                    for y in range(max(top + 1, BARRIER['y0']), BARRIER['y1'] + 1):
                        g[(x, y, z)] = B + 'barrier'
            if d > SHAFT_R:
                g[(x, 230, z)] = leaf
    # the ember twig on the bank
    tx, ty, tz = (math.floor(v) for v in EMBER_TWIG)
    g[(tx, ty - 1, tz)] = B + 'mossy_cobblestone'
    g[(tx, ty, tz)] = B + 'mangrove_roots'
    return g


def _build():
    if 'cells' not in _CACHE:
        _CACHE['cells'] = _build_day1()
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


def _cover(cells, forbidden):
    """Boxes (inclusive) covering every cell of `cells`, none containing a cell of `forbidden`, each <= MAX_FILL blocks:
    the bounding box, split in half along its longest axis until it is legal, then shrunk to its cells."""
    out = []
    todo = [list(cells)]
    while todo:
        cs = todo.pop()
        if not cs:
            continue
        lo = [min(c[k] for c in cs) for k in range(3)]
        hi = [max(c[k] for c in cs) for k in range(3)]
        box = (tuple(lo), tuple(hi))
        bad = _vol(box) > MAX_FILL or any(lo[0] <= f[0] <= hi[0] and lo[1] <= f[1] <= hi[1] and lo[2] <= f[2] <= hi[2]
                                          for f in forbidden)
        if not bad:
            out.append(box)
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
    """[(new, old, box)]: `fill box new replace old` commands that move every cell of the other look (or of any mix of
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
        for box in _cover(cs, forb):
            out.append((new, old, box))
    return out


def _target(v, i):
    return v[i] if isinstance(v, Lk) else v


def look_lines(look):
    """[[cmd]] (one inner list per tick, <= 24): turns any built look into `look` (ap_contract.md §0.6.5)."""
    if look not in LOOKS:
        raise KeyError('ap_oasis has no look ' + repr(look))
    boxes = _look_boxes(look)
    mode = ' strict' if LOOK_STRICT else ''
    cmds = []
    for new, old, ((x0, y0, z0), (x1, y1, z1)) in boxes:
        cmds.append((_vol(((x0, y0, z0), (x1, y1, z1))),
                     'fill %d %d %d %d %d %d %s replace %s%s' % (x0, y0, z0, x1, y1, z1, new or B + 'air', old, mode)))
    # balance: greedy by volume into as few ticks as the per-tick volume budget allows (<= 24)
    budget = max(MAX_FILL * 3, -(-sum(v for v, _ in cmds) // MAX_LOOK_SLICES))
    ticks, cur, acc = [], [], 0
    for v, c in cmds:
        if cur and acc + v > budget:
            ticks.append(cur)
            cur, acc = [], 0
        cur.append(c)
        acc += v
    if cur:
        ticks.append(cur)
    assert 1 <= len(ticks) <= MAX_LOOK_SLICES, len(ticks)
    return ticks


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
        for i, (kind, (x, y, z)) in enumerate(_pond_props()):
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
                    bl[(x, 218, z)] = 'minecraft:light[level=15]'
        out[zid] = bl
    return out


def entrance_layout():
    foyer = _zone(1, 0, FOYER, (0, 32), [_cell(*FOYER, (-4, 26, 4, 37))])
    hall = _zone(2, 9, HALL, (GATE[0], GATE[2]), [_cell(*HALL, (-8, 6, 8, 20))])
    cur = {'n': 2, 'zones': [foyer, hall], 'doors': [dict(DOOR)], 'spawn': {'x': 0, 'z': 33, 'yaw': 180},
           'spot': {'x': 0, 'z': 33}}
    clear = {1: [((FOYER[0], 201, FOYER[1]), (FOYER[2], 230, FOYER[3]))],
             2: [((HALL[0], 201, HALL[1]), (HALL[2], 230, HALL[3]))]}
    return {'cur': cur, 'blocks': _entrance_blocks_day1(), 'clear': clear, 'gate': GATE,
            'glyphs': dict(ENT_CRYSTALS), 'stele_glow': ENT_GLOW}


def render_hints():
    """Camera presets for the offline renderer (S:ap/arenarender)."""
    return {'arrival_eye': {'pos': (440.5, 202.62, 24.5), 'yaw': 180.0, 'pitch': -4.0},
            'entrance_eye': {'pos': (0.5, 202.62, 33.0), 'yaw': 180.0, 'pitch': -2.0}}
