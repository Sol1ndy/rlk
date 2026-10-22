"""Arena theme "cp_test": the chapter proto boss's test arena (scratchpad az/contract/theme.md 7).

Imported by tools/build_mboss_arena.py (arena_layout, slices, SENTINEL), tools/build_cboss_rooms.py (entrance_layout)
and the chapter-mode tests. Stdlib only, deterministic, no side effects on import, never writes files.

A flat smooth-stone floor (y 200) over a polished-deepslate base (y 199) on the disc r <= 12, a 3-high stone-brick wall
11 < d <= 12, a hidden light layer at y 206 over the walk disc. Two looks: "plain" (the default) and "lit" (the floor
ring 6 < d <= 10 becomes gold blocks and the light layer goes from level 9 to level 15), so the chapter mode's look
jobs, per-look stamps and the default restore of ensure are exercised on a small box (2 build slices, a 1-slice diff).
"""
import math

THEME = 'cp_test'
AID = 'cp_test'
CX, CY, CZ = 540, 201, 8
R, WALK, SAFE = 12, 11, 9
BOX = (524, 196, -8, 556, 216, 24)
LOOKS = ('plain', 'lit')
CHECK = {'cx': CX, 'cy': CY, 'cz': CZ, 'r': R, 'walk': WALK, 'safe': SAFE,
         'box': {'x0': BOX[0], 'y0': BOX[1], 'z0': BOX[2], 'x1': BOX[3], 'y1': BOX[4], 'z1': BOX[5]},
         'start': {'x': 540.5, 'y': 201.0, 'z': 17.5, 'yaw': 180.0, 'pitch': 0.0}}
SENTINEL = ((CX, CY - 2, CZ), 'minecraft:polished_deepslate')
POINTS = {'spawn': (540.0, 201.0, 8.0, 0.0)}


def _d(x, z):
    return math.hypot(x + 0.5 - CX, z + 0.5 - CZ)


def arena_layout(look=None):
    """{(x, y, z): block} of every non-air block of the box in `look` (None = 'plain')."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    out = {}
    x0, y0, z0, x1, y1, z1 = BOX
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            d = _d(x, z)
            if d > R:
                continue
            out[(x, CY - 2, z)] = 'minecraft:polished_deepslate'
            out[(x, CY - 1, z)] = 'minecraft:gold_block' if (look == 'lit' and 6 < d <= 10) else 'minecraft:smooth_stone'
            if d > WALK:
                for y in range(CY, CY + 3):
                    out[(x, y, z)] = 'minecraft:stone_bricks'
            elif d <= WALK - 0.5:
                out[(x, CY + 5, z)] = 'minecraft:light[level=15]' if look == 'lit' else 'minecraft:light[level=9]'
    return out


def slices():
    """Two build slices (y 196..206 with every block, and the empty air above, 207..216): disjoint, covering the box,
    each <= 32 768 blocks; the look diff (floor ring, light layer) lies in the first, so a look job is one slice."""
    x0, y0, z0, x1, y1, z1 = BOX
    return [((x0, y0, z0), (x1, 206, z1)), ((x0, 207, z0), (x1, y1, z1))]


def props(look=None):
    """Two test props per look with vanilla kinds (theme.md 7): 'plain' glass, 'lit' gold blocks (group 'test', el 5,
    no fixed UUID); cproto spawns them at fight start and after its own look calls (tag prefix rlk_mb_cp_ap_test)."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    item = 'minecraft:glass' if look == 'plain' else 'minecraft:gold_block'
    return [{'name': f'{look}_{i}', 'kind': 'item:' + item, 'group': 'test', 'pos': (CX - 3.0 + 6.0 * i, 202.5, float(CZ - 4)),
             'yaw': 0.0, 'pitch': 0.0, 'scale': 0.8, 'el': 5, 'uuid': None} for i in range(2)]


def _cell(x0, z0, x1, z1, m=3):
    """A room cell record in the conventions of F:room/raiden/layout and room/data (inner box -1, entry box (x100)
    `m` blocks in from the west / north edge and m - 1 from the east / south edge, spawn box m in)."""
    return {'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'ix0': x0 + 1, 'iz0': z0 + 1, 'ix1': x1 - 1, 'iz1': z1 - 1,
            'ex0': (x0 + m) * 100, 'ez0': (z0 + m) * 100, 'ex1': (x1 - m + 1) * 100, 'ez1': (z1 - m + 1) * 100,
            'sx0': x0 + m, 'sz0': z0 + m, 'sx1': x1 - m, 'sz1': z1 - m}


def _zone(zid, kind, x0, z0, x1, z1):
    return {'id': zid, 'kind': kind, 'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'cx': (x0 + x1 + 1) // 2, 'cz': (z0 + z1 + 1) // 2,
            'mn': 1, 'mx': 1, 'nc': 1, 'ncm': 0, 'cells': [_cell(x0, z0, x1, z1, 2 if zid == 1 else 3)],
            'by': 0, 'cy': 201, 'sd': 0, 'pits': []}


def _room(blocks, x0, z0, x1, z1, wall, floor):
    for z in range(z0, z1 + 1):
        for x in range(x0, x1 + 1):
            blocks[(x, 199, z)] = 'minecraft:polished_blackstone'
            blocks[(x, 200, z)] = floor
            if x in (x0, x1) or z in (z0, z1):
                for y in range(201, 208):
                    blocks[(x, y, z)] = wall
    for z in range(z0 + 1, z1):
        for x in range(x0 + 1, x1):
            blocks[(x, 218, z)] = 'minecraft:light[level=15]'


def entrance_layout():
    """The domain entrance of cproto: zone 1 = a 12 x 16 foyer (Raiden's foyer box x -6..5, z 24..39), its door, zone 2 =
    one kind-9 cell x -10..9, z 4..23 with the gate at its centre (0, 201, 14)."""
    z1 = _zone(1, 0, -6, 24, 5, 39)
    z2 = _zone(2, 9, -10, 4, 9, 23)
    cur = {'n': 2, 'zones': [z1, z2],
           'doors': [{'a': 1, 'b': 2, 'x0': -2, 'x1': 1, 'z0': 23, 'z1': 24, 'mx': 0, 'mz': 24, 'ya': 0, 'yb': 180, 'h': 0,
                      'y0': 201, 'y1': 205, 'l0': 206, 'l1': 207, 'my': 201, 'tx0': -2, 'tx1': 1, 'tz0': 24, 'tz1': 24, 'tm': 210}],
           'spawn': {'x': 0, 'z': 33, 'yaw': 180}, 'spot': {'x': 0, 'z': 33}}
    b1, b2 = {}, {}
    _room(b1, -6, 24, 5, 39, 'minecraft:stone_bricks', 'minecraft:smooth_stone')
    _room(b2, -10, 4, 9, 23, 'minecraft:stone_bricks', 'minecraft:polished_andesite')
    for z in range(10, 19):          # a 9 x 9 ring of chiseled bricks around the gate
        for x in range(-4, 5):
            if max(abs(x), abs(z - 14)) == 4:
                b2[(x, 200, z)] = 'minecraft:chiseled_stone_bricks'
    for y in range(201, 204):        # the stele west of the gate (3 high)
        b2[(-4, y, 14)] = 'minecraft:chiseled_stone_bricks'
    return {'cur': cur, 'blocks': {1: b1, 2: b2},
            'clear': {1: [(-6, 199, 24, 5, 230, 39)], 2: [(-10, 199, 4, 9, 230, 23)]},
            'gate': (0, 201, 14), 'glyphs': {'upper': (-3.45, 203.2, 14.0, 90.0), 'lower': (-3.45, 202.2, 14.0, 90.0)},
            'stele_glow': (-3.4, 202.5, 14.0), 'th': {'lb': 'minecraft:stone_bricks', 'lb2': 'minecraft:stone_bricks'}}


def render_hints():
    return {'top': {'centre': (CX, CZ), 'r': R + 2}}
