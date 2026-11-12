"""Arena theme `fl_ruins` "영락한 폐허": the round Fontaine-ruins plaza where 아를레키노 (chapter-4 boss) waits
(scratchpad ar/PLAN.md §8; footage sheet ar/ref/arena.jpg: v5 13 / 16 / 2, v1 33.2 / 27.8, v3 38.6, v4 14 / 16.5 / 24,
v7 36).

Theme module (scratchpad az/contract/theme.md): plain Python, stdlib only, deterministic, no side effects on import,
never writes files. The arena generator (tools/build_mboss_arena.py) imports `arena_layout`, `slices`, `look_lines`,
`SENTINEL` and `CHECK`; tools/build_cboss_rooms.py imports `entrance_layout`; the module generator and the tests import
`POINTS`, `props` and the constants.

Coordinates: the centre (760, 201, 8) is a block corner, floor blocks at y 200, stand height 201. A cell (x, z) is "at
distance d" when its centre (x + 0.5, z + 0.5) is d blocks from (760, 8) horizontally; bearings are compass bearings
(0 north = -z, 90 east = +x, 180 south = the arrival).

  plaza (d <= 26)        y 200 flat full blocks: pale stone tiles (smooth stone, polished diorite, calcite) with carved
                         concentric bands (the footage's rings): the centre star r 3 (chiseled stone bricks), grooves at
                         r 3.5, 6.5, 10 + 11.5 (double), 16, 22 + 23.5 (double), radial spokes every 30 deg in the
                         bands r 11.5..16 and 16..22 (offset 15 deg) and every 45 deg in r 3.5..6.5; cracked tiles and
                         moss in the seams. Solid stone below down to y 190 (the sentinel layer y 196)
  rim (26 < d <= 27.6)   the curb (y 200) and a broken balustrade at y 201 (stone-brick / diorite wall runs, quartz posts
                         every 12 deg, two gaps); the invisible barrier ring y 201..216 wherever no balustrade block is
  posts (d ~ 28)         the three wisp posts at bearings 0 / 150 / 210 (POINTS['wisps'], api.WISP_POSTS)
  beyond (27.6 < d < 44) grass and purple / white flowers, Fontaine ruins (a round-window wall arc behind the boss, an
                         arch gate, a tower stump, column groups, fallen drums: stone bricks, quartz bricks, polished
                         deepslate trim, oxidized copper caps, light-blue glass in the round windows), dark spruce / dark
                         oak trees (persistent leaves), rock outcrops; rocky slopes rising to the dome in the north-west, a
                         cliff edge in the south-east falling to the sea (y 190) below the painted dome base
  sky                    a block dome (superellipse p 4, r 44 at the floor, top y 248) of concrete / wool bands (white
                         horizon, pale blue, blue, a dithered zenith), white wool clouds, a painted mountain / sea band on
                         its base in the south-east; lit from inside by light blocks on its inner skin (stripes), so no
                         sky light and no world-time dependence; light blocks on the outer roof keep its tops lit
  light                  the light layer y 206 (level 15) over the walk disc: floor block light 10 (15 - 5, the most a
                         layer at y 206 gives; nothing else is above the walk disc below y 226); hidden light[level=15]
                         blocks wherever another spawnable cell of the box would be below 12 (both looks)

Looks: 'day' (P1, the default restored by the framework's ensure) and 'crimson' (P2, the T 'dark' job): the dome bands
-> pink concrete / magenta terracotta / red concrete with a dark crimson zenith (red concrete + brown terracotta
dither), clouds -> pink terracotta, mountains / snow / sea -> dark terracotta tones, the red moon (r 6, red concrete
face, redstone-block rim, shroomlight glow ring) on the north dome wall, a few grass patches -> red terracotta and a few
round-window panes -> red stained glass. The walk floor never changes. `look_lines(look)` turns any built look into
`look`: `fill ... replace` boxes per 8 x 8 column tile (one-to-one block pairs, each box <= 32 768 blocks), then
absolute spans for the cells a pair cannot express (the moon, the patches, the panes); <= 4 slices.
"""
import math

THEME = 'fl_ruins'
AID = 'fl_ruins'

CX, CY, CZ = 760, 201, 8
RAD, WALK, SAFE = 30, 26, 24
BOX = {'x0': 712, 'y0': 190, 'z0': -40, 'x1': 808, 'y1': 250, 'z1': 56}
START = {'x': 760.5, 'y': 201.0, 'z': 30.5, 'yaw': 180.0, 'pitch': 0.0}
CHECK = {'n': 4, 'theme': THEME, 'ver': 1, 'cx': CX, 'cy': CY, 'cz': CZ, 'r': RAD, 'walk': WALK, 'safe': SAFE,
         'box': dict(BOX), 'start': dict(START), 'looks': ['day', 'crimson'], 'oob': {'y0': 198, 'y1': 230}}
LOOKS = ('day', 'crimson')

FLOOR_Y = CY - 1                 # 200: the floor top
SENT_Y = 196                     # the sentinel layer (polished deepslate under the plaza)
LIGHT_Y, LIGHT_LV = 206, 15      # the light layer over the walk disc
CLEAR_Y = (201, 225)             # above the walk disc: only the light layer (PLAN §8.2)
RIM_R = 27.6                     # the balustrade / barrier ring WALK < d <= RIM_R
BARRIER_Y = (201, 216)
WISP_BEARINGS, WISP_R = (0, 150, 210), 28.0
DOME_R, DOME_Y0, DOME_TOP, DOME_P = 44.0, 190, 248, 4.0
SEA_Y = 190                      # the sea plane below the south-east cliff (the box floor)
FLOOR_LIGHT_MIN, SPAWN_LIGHT_MIN = 10, 12
MAX_FILL, MAX_LOOK_SLICES, TILE = 32768, 4, 8

SENTINEL = ((CX, SENT_Y, CZ), 'minecraft:polished_deepslate')

B = 'minecraft:'
LIGHT15 = B + 'light[level=15]'


def _p(n):
    return B + n


# ---------------------------------------------------------------------------------------------------------------
# deterministic helpers

def _mix(*ints):
    h = 0x9E3779B1
    for v in ints:
        h = (h ^ (v & 0xffffffff)) * 0x85EBCA77 & 0xffffffff
        h ^= h >> 13
    h = h * 0xC2B2AE3D & 0xffffffff
    return (h ^ (h >> 16)) / 0xffffffff


def _vnoise(x, z, scale, seed):
    fx, fz = x / scale, z / scale
    ix, iz = math.floor(fx), math.floor(fz)
    tx, tz = fx - ix, fz - iz
    tx, tz = tx * tx * (3 - 2 * tx), tz * tz * (3 - 2 * tz)
    a, b = _mix(ix, iz, seed), _mix(ix + 1, iz, seed)
    c, d = _mix(ix, iz + 1, seed), _mix(ix + 1, iz + 1, seed)
    return (a * (1 - tx) + b * tx) * (1 - tz) + (c * (1 - tx) + d * tx) * tz


def _fbm(x, z, scale, seed):
    return 0.6 * _vnoise(x, z, scale, seed) + 0.4 * _vnoise(x, z, scale / 2.3, seed + 17)


def _d(x, z):
    return math.hypot(x + 0.5 - CX, z + 0.5 - CZ)


def _bearing(x, z):
    """compass bearing of a cell centre: 0 north (-z), 90 east (+x), 180 south (+z)"""
    return math.degrees(math.atan2(x + 0.5 - CX, -(z + 0.5 - CZ))) % 360


def _angdiff(a, b):
    return (a - b + 180) % 360 - 180


def _smooth(e0, e1, v):
    t = max(0.0, min(1.0, (v - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def _in_box(x, y, z):
    return BOX['x0'] <= x <= BOX['x1'] and BOX['y0'] <= y <= BOX['y1'] and BOX['z0'] <= z <= BOX['z1']


def polar_point(d, bearing, y=201.0):
    """absolute (x, y, z) of the point d blocks from the centre on a compass bearing"""
    a = math.radians(bearing)
    return (round(CX + d * math.sin(a), 3), y, round(CZ - d * math.cos(a), 3))


def polar_cell(d, bearing):
    x, _, z = polar_point(d, bearing)
    return math.floor(x), math.floor(z)


def yaw_facing_centre(x, z):
    """Minecraft yaw of a thing at (x, z) facing the arena centre"""
    return round(math.degrees(math.atan2(-(CX - x), CZ - z)) % 360, 2)


# ---------------------------------------------------------------------------------------------------------------
# the plaza floor (y 200, d <= WALK): every block full and opaque

GROOVES = (3.5, 6.5, 10.0, 11.5, 16.0, 22.0, 23.5)
DOUBLE_FILL = ((10.0, 11.5), (22.0, 23.5))      # calcite between the two grooves of a double ring


def _spoke(d, br, r0, r1, step, off, hw=0.45):
    if not (r0 < d < r1):
        return False
    k = round((br - off) / step)
    return abs(_angdiff(br, off + k * step)) * math.pi / 180 * d < hw


def floor_top(x, z):
    """the block at y 200 of a plaza cell (d <= WALK)"""
    d, br = _d(x, z), _bearing(x, z)
    # the centre star: eight points (long on the axes, short on the diagonals) of chiseled stone bricks on diorite
    if d <= 3.0:
        k = round(br / 45.0)
        reach = 3.0 if k % 2 == 0 else 2.2
        w = abs(_angdiff(br, k * 45.0)) * math.pi / 180 * d
        if d <= 1.25 or (d <= reach and w < 0.62 * (1 - d / (reach + 0.6)) + 0.18):
            return _p('chiseled_stone_bricks')
        return _p('polished_diorite')
    for g in GROOVES:
        if abs(d - g) < 0.5:
            return _p('stone_bricks') if g in (6.5, 16.0) else _p('polished_andesite')
    for a, b in DOUBLE_FILL:
        if a < d < b:
            return _p('calcite')
    if _spoke(d, br, 11.5, 16.0, 30.0, 0.0) or _spoke(d, br, 3.5, 6.5, 45.0, 22.5):
        return _p('polished_andesite')
    if _spoke(d, br, 16.0, 22.0, 30.0, 15.0):
        return _p('stone_bricks')
    # tiles: 3 x 3 slabs of pale stone (mostly polished diorite, some calcite / smooth stone), a few cracked tiles and
    # moss in a few seams: low contrast, so the carved rings read
    tx, tz = (x - CX) // 3, (z - CZ) // 3
    seam = (x - CX) % 3 == 0 or (z - CZ) % 3 == 0
    h = _mix(tx, tz, 11)
    if seam and _fbm(x, z, 6.0, 13) > 0.68 and _mix(x, z, 15) < 0.5:
        return _p('moss_block') if _mix(x, z, 17) < 0.55 else _p('mossy_stone_bricks')
    if _mix(x, z, 19) < 0.025:
        return _p('cracked_stone_bricks')
    if h < 0.66:
        return _p('polished_diorite')
    if h < 0.88:
        return _p('calcite')
    return _p('smooth_stone')


# ---------------------------------------------------------------------------------------------------------------
# the rim: curb, balustrade, barrier, wisp posts

POST_STEP = 12.0
GAPS = ((60.0, 74.0), (282.0, 300.0))            # broken stretches of the balustrade (barrier only)


def _wall_cells():
    """{(x, z): kind} of the balustrade cells at y 201 ('wall_s' stone brick wall, 'wall_d' diorite wall, 'post')"""
    out = {}
    for z in range(CZ - 30, CZ + 30):
        for x in range(CX - 30, CX + 30):
            d = _d(x, z)
            if not (WALK + 0.25 < d <= WALK + 1.25):
                continue
            br = _bearing(x, z)
            if any(a <= br <= b for a, b in GAPS):
                continue
            k = round(br / POST_STEP)
            if abs(_angdiff(br, k * POST_STEP)) * math.pi / 180 * d < 0.55:
                out[(x, z)] = 'post'
            elif _mix(x, z, 23) < 0.08:
                continue                                       # a missing baluster
            else:
                out[(x, z)] = 'wall_d' if (k // 2) % 2 else 'wall_s'
    return out


def _wall_state(name, x, z, cells):
    side = {}
    for nm, dx, dz in (('north', 0, -1), ('south', 0, 1), ('east', 1, 0), ('west', -1, 0)):
        side[nm] = 'low' if (x + dx, z + dz) in cells else 'none'
    straight = (side['north'] == side['south'] == 'low' and side['east'] == side['west'] == 'none') or \
               (side['east'] == side['west'] == 'low' and side['north'] == side['south'] == 'none')
    up = 'false' if straight else 'true'
    return (f'{_p(name)}[east={side["east"]},north={side["north"]},south={side["south"]},up={up},'
            f'waterlogged=false,west={side["west"]}]')


WISP_CELLS = [polar_cell(WISP_R + 0.4, b) for b in WISP_BEARINGS]     # the post cell: its centre ~ r 28.5, outside the ring
assert all(_d(x, z) > RIM_R + 0.5 for x, z in WISP_CELLS)


# ---------------------------------------------------------------------------------------------------------------
# terrain beyond the rim: grass ground, the rocky north-west, the south-east cliff

def _nw(br):
    """0..1: the rocky rising sector (north-west, bearings ~215..70 through north)"""
    a = (br - 322.5 + 540) % 360 - 180            # centred on 322.5
    return 1.0 - _smooth(55.0, 85.0, abs(a))


def _se(br):
    """0..1: the cliff sector (south-east, bearings ~85..205)"""
    return 1.0 - _smooth(52.0, 70.0, abs(_angdiff(br, 145.0)))


def edge_r(br):
    """the cliff edge radius in the south-east"""
    return 34.0 + 2.6 * _vnoise(br / 9.0, 0.0, 1.0, 71)


def ground_top(x, z):
    """the top block y of the ground column at a cell beyond the rim (None = the sea, nothing above y 190)"""
    d, br = _d(x, z), _bearing(x, z)
    se = _se(br)
    if se > 0.5 and d > edge_r(br):
        return None
    nw = _nw(br)
    rise = nw * max(0.0, d - 34.5) * (1.7 + 1.0 * _fbm(x, z, 7.0, 31)) + nw * 3.0 * _fbm(x, z, 5.0, 37) * _smooth(31, 36, d)
    bump = 0.0
    for b0, r0, h0, w0 in OUTCROPS:
        dd = math.hypot(*(a - b for a, b in zip(polar_point(r0, b0)[::2], (x + 0.5, z + 0.5))))
        if dd < w0:
            bump = max(bump, h0 * (1 - (dd / w0) ** 2) * (0.75 + 0.5 * _mix(x, z, 41)))
    cap = 12.0 if abs(_angdiff(br, MOON['bearing'])) < 24 else 18.0     # the moon stays clear of the north slope
    top = FLOOR_Y + int(round(min(cap, rise + bump)))
    return min(top, dome_ceiling(x, z))


def dome_ceiling(x, z):
    """the highest interior y of the dome over a column (DOME_Y0 when it has none)"""
    d = _d(x, z)
    if d >= DOME_R:
        return DOME_Y0
    hmax = (1.0 - (d / DOME_R) ** DOME_P) ** (1.0 / DOME_P) * (DOME_TOP + 1 - DOME_Y0)
    y = math.floor(DOME_Y0 + hmax - 0.5)
    while y > DOME_Y0 and not _dome_in(x, y, z):
        y -= 1
    return y


OUTCROPS = ((78.0, 33.0, 3.0, 3.2), (168.0, 31.5, 2.0, 2.4), (262.0, 33.5, 4.0, 3.6), (22.0, 37.0, 5.0, 4.0),
            (200.0, 32.5, 2.5, 2.6))


def _rock(x, y, z):
    n = _fbm(x * 1.3 + y * 0.7, z * 1.3 - y * 0.5, 4.0, 43)
    if n > 0.68:
        return _p('mossy_cobblestone')
    if n > 0.55:
        return _p('andesite')
    if n < 0.22:
        return _p('tuff')
    return _p('stone')


FLOWERS = ('cornflower', 'allium', 'azure_bluet', 'oxeye_daisy', 'lily_of_the_valley')


def _patch(x, z):
    """a grass cell that turns red terracotta in the crimson look (a few patches beyond the rim)"""
    return _d(x, z) > RIM_R + 1.5 and _fbm(x, z, 5.0, 141) > 0.72


def _plant(x, z, top):
    """the plant on a grass top (or None); lilac is two cells"""
    d, br = _d(x, z), _bearing(x, z)
    if d < RIM_R + 0.6:
        return None
    meadow = _fbm(x, z, 6.0, 51)
    h = _mix(x, z, 53)
    if meadow > 0.6 and h < 0.55:
        if h < 0.12 and top < 214:
            return 'lilac'
        return FLOWERS[0] if h < 0.3 else FLOWERS[1] if h < 0.42 else FLOWERS[2 + int(_mix(x, z, 55) * 3)]
    if h < 0.32:
        return 'short_grass'
    return None


# ---------------------------------------------------------------------------------------------------------------
# ruins, columns, trees

def _put(g, x, y, z, b, force=False):
    if not _in_box(x, y, z):
        return
    if force or (x, y, z) not in g or g[(x, y, z)] in (_p('short_grass'),) or g[(x, y, z)].startswith(_p('lilac')):
        g[(x, y, z)] = b


def _stone(x, y, z, base='stone_bricks'):
    h = _mix(x, y, z, 61)
    if h < 0.14:
        return _p('mossy_stone_bricks')
    if h < 0.24:
        return _p('cracked_stone_bricks')
    return _p(base)


WINDOW_GLASS = _p('light_blue_stained_glass')
RED_GLASS = _p('red_stained_glass')


def _window_wall(g, b0, b1, r, base_y, top_y, windows, trim_y, seed):
    """an arc wall (2 thick) from bearing b0 to b1 at radius r; broken top; round windows (bearing, centre y, radius)"""
    n = int(abs(b1 - b0) * math.pi / 180 * r * 3) + 2
    done = set()
    for i in range(n + 1):
        br = b0 + (b1 - b0) * i / n
        for dr in (0.0, 0.9):
            x, z = polar_cell(r + dr, br)
            if (x, z) in done:
                continue
            done.add((x, z))
            brk = top_y - int(round(7 * _fbm(br * 0.35, 0.0, 1.0, seed) ** 1.6)) - (2 if _mix(x, z, seed) < 0.15 else 0)
            for y in range(base_y, brk + 1):
                blk = _stone(x, y, z)
                if y == trim_y:
                    blk = _p('polished_deepslate')
                for wb, wy, wr in windows:
                    s = _angdiff(br, wb) * math.pi / 180 * r
                    rr = math.hypot(s, y + 0.5 - wy)
                    if rr <= wr - 0.9:
                        blk = WINDOW_GLASS if dr == 0.0 else None
                    elif rr <= wr + 0.2:
                        blk = _p('quartz_bricks')
                if blk:
                    _put(g, x, y, z, blk, force=True)
                elif (x, y, z) in g:
                    del g[(x, y, z)]
    # pilasters at both ends, quartz with an oxidized copper cap
    for br in (b0, b1):
        x, z = polar_cell(r + 0.45, br)
        for dx in (0, 1):
            for y in range(base_y, top_y + 2):
                _put(g, x + dx, y, z, _p('quartz_bricks') if y <= top_y else _p('oxidized_copper'), force=True)


def _arch(g, br, r, half, base_y, seed):
    """an arch gate facing the centre: two 3-wide piers beside an opening of 2 * half - 1 cells, a round arch (radius
    half - 0.5, springing 4 b over the base) with a polished deepslate trim course, stone above, an oxidized copper cap"""
    a = math.radians(br)
    ux, uz = math.cos(a), math.sin(a)          # the tangent (left / right of the axis)
    rx, rz = math.sin(a), -math.cos(a)         # the radial direction (depth)
    cx, _, cz = polar_point(r, br)
    spring, R = base_y + 4, half - 0.5
    top = spring + half + 2
    for s in range(-half - 2, half + 3):
        for t in (0.0, 0.9):
            x, z = math.floor(cx + ux * s + rx * t), math.floor(cz + uz * s + rz * t)
            u = abs(s + 0.5 - 0.5) if s >= 0 else abs(s)
            for y in range(base_y, top + 1):
                if abs(s) >= half:
                    blk = _p('quartz_bricks') if abs(s) == half else _stone(x, y, z)
                    if y == top:
                        blk = _p('oxidized_copper')
                    _put(g, x, y, z, blk, force=True)
                    continue
                curve = spring + math.sqrt(max(0.0, R * R - u * u))
                if y + 0.5 < curve:
                    continue
                if y == top:
                    if _mix(x, z, seed) > 0.25:
                        _put(g, x, y, z, _p('oxidized_copper'), force=True)
                elif y + 0.5 < curve + 1.0:
                    _put(g, x, y, z, _p('polished_deepslate'), force=True)
                else:
                    _put(g, x, y, z, _stone(x, y, z), force=True)


def _column(g, x, z, base_y, h, cap=True):
    for dx in (-1, 0, 1):
        for dz in (-1, 0, 1):
            _put(g, x + dx, base_y, z + dz, _p('stone_bricks') if (dx or dz) else _p('chiseled_stone_bricks'), force=True)
    for y in range(base_y + 1, base_y + 1 + h):
        _put(g, x, y, z, _p('quartz_pillar[axis=y]'), force=True)
    if cap:
        _put(g, x, base_y + 1 + h, z, _p('oxidized_copper') if h >= 6 else _p('chiseled_quartz_block'), force=True)


def _drum(g, x, z, y, axis, n):
    for i in range(n):
        if axis == 'x':
            _put(g, x + i, y, z, _p('quartz_pillar[axis=x]'), force=True)
        else:
            _put(g, x, y, z + i, _p('quartz_pillar[axis=z]'), force=True)


def _tower(g, br, r, rad, base_y, top_y, seed):
    cx, _, cz = polar_point(r, br)
    for z in range(math.floor(cz - rad - 1), math.ceil(cz + rad + 2)):
        for x in range(math.floor(cx - rad - 1), math.ceil(cx + rad + 2)):
            dd = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
            if dd > rad + 0.5:
                continue
            ang = math.degrees(math.atan2(x + 0.5 - cx, -(z + 0.5 - cz))) % 360
            brk = top_y - int(round(9 * _fbm(ang / 25.0, 0.0, 1.0, seed) ** 1.4))
            for y in range(base_y, brk + 1):
                if dd > rad - 0.5:
                    blk = _stone(x, y, z)
                    if y in (base_y + 5, base_y + 13):
                        blk = _p('polished_deepslate')
                    face = abs(_angdiff(ang, (br + 180) % 360))
                    if face < 30 and math.hypot(face * math.pi / 180 * rad, y + 0.5 - (base_y + 9)) <= 1.6:
                        blk = WINDOW_GLASS
                    _put(g, x, y, z, blk, force=True)
                elif y == base_y:
                    _put(g, x, y, z, _p('stone_bricks'), force=True)


def _tree_spruce(g, x, z, base_y, h, seed):
    for y in range(base_y, base_y + h):
        _put(g, x, y, z, _p('spruce_log[axis=y]'), force=True)
    top = base_y + h
    for y in range(base_y + 3, top + 2):
        k = (top + 1 - y)
        rad = min(3.2, 0.6 + k * 0.42) if (y - base_y) % 2 == 0 else min(2.4, 0.3 + k * 0.32)
        for dz in range(-4, 5):
            for dx in range(-4, 5):
                if (dx or dz) and math.hypot(dx, dz) <= rad and _mix(x + dx, y, z + dz, seed) > 0.08:
                    _put(g, x + dx, y, z + dz, _p('spruce_leaves[distance=1,persistent=true,waterlogged=false]'))
    _put(g, x, top, z, _p('spruce_leaves[distance=1,persistent=true,waterlogged=false]'))
    _put(g, x, top + 1, z, _p('spruce_leaves[distance=1,persistent=true,waterlogged=false]'))


def _tree_dark(g, x, z, base_y, h, seed):
    for y in range(base_y, base_y + h):
        for dx in (0, 1):
            for dz in (0, 1):
                _put(g, x + dx, y, z + dz, _p('dark_oak_log[axis=y]'), force=True)
    for y in range(base_y + h - 2, base_y + h + 2):
        rad = 3.6 if y < base_y + h + 1 else 2.4
        for dz in range(-4, 6):
            for dx in range(-4, 6):
                dd = math.hypot(dx - 0.5, dz - 0.5)
                if dd <= rad and _mix(x + dx, y, z + dz, seed) > 0.1:
                    _put(g, x + dx, y, z + dz, _p('dark_oak_leaves[distance=1,persistent=true,waterlogged=false]'))


# (kind, bearing, radius, height): trees beyond the rim; none overhangs d <= RIM_R + 1
TREES = (('spruce', 18.0, 39.0, 15), ('dark', 52.0, 36.0, 8), ('spruce', 118.0, 31.5, 11), ('spruce', 136.0, 32.0, 9),
         ('dark', 196.0, 31.8, 7), ('spruce', 236.0, 36.5, 13), ('spruce', 252.0, 39.5, 16), ('dark', 300.0, 36.0, 9),
         ('spruce', 330.0, 40.0, 14), ('spruce', 344.0, 37.0, 12), ('dark', 88.0, 32.5, 8))
COLUMNS = ((310.0, 31.5, 8), (318.0, 34.0, 4), (304.0, 35.5, 11), (228.0, 31.0, 6), (240.0, 32.5, 3),
           (96.0, 31.0, 7), (104.0, 32.6, 2), (166.0, 30.6, 5), (32.0, 31.0, 9), (150.0, 32.0, 3))
DRUMS = ((322.0, 32.0, 'x', 3), (234.0, 34.0, 'z', 3), (100.0, 32.0, 'x', 2), (176.0, 31.8, 'x', 3))


def _ruins(g, tops):
    def base(br, r):
        x, z = polar_cell(r, br)
        t = tops.get((x, z))
        return (t if t is not None else FLOOR_Y) + 1
    # the round-window wall behind the boss (north), a little arc of three windows
    _window_wall(g, -26.0, 24.0, 34.5, base(0, 34.5) - 1, 217, ((-13.0, 209.0, 2.6), (0.0, 210.0, 3.2), (13.0, 209.0, 2.6)),
                 205, 81)
    _arch(g, 44.0, 33.0, 3, base(44, 33.0) - 1, 83)
    _arch(g, 218.0, 34.0, 2, base(218, 34.0) - 1, 85)
    _tower(g, 276.0, 37.0, 3.6, base(276, 37.0) - 1, 224, 87)
    for br, r, h in COLUMNS:
        x, z = polar_cell(r, br)
        _column(g, x, z, base(br, r) - 1, h, cap=_mix(x, z, 91) > 0.3)
    for br, r, axis, n in DRUMS:
        x, z = polar_cell(r, br)
        _drum(g, x, z, base(br, r), axis, n)
    for kind, br, r, h in TREES:
        x, z = polar_cell(r, br)
        (_tree_spruce if kind == 'spruce' else _tree_dark)(g, x, z, base(br, r), h, int(br))


# ---------------------------------------------------------------------------------------------------------------
# the sky dome

def _dome_in(x, y, z):
    """interior cell of the dome (y DOME_Y0 + 1 .. DOME_TOP)"""
    if not (DOME_Y0 < y <= DOME_TOP):
        return False
    h = (y + 0.5 - DOME_Y0) / (DOME_TOP + 1 - DOME_Y0)
    return (_d(x, z) / DOME_R) ** DOME_P + h ** DOME_P <= 1.0


BANDS = ((211, 'white_concrete'), (236, 'light_blue_concrete_powder'), (243, 'light_blue_concrete'), (999, 'zenith'))
# one-to-one dome / backdrop pairs day -> crimson (no block of either side is used anywhere else in the box)
PAIRS = {
    'white_concrete': 'pink_concrete',                       # the horizon band
    'light_blue_concrete_powder': 'magenta_terracotta',      # the low sky
    'light_blue_concrete': 'red_concrete',                   # the high sky
    'light_blue_wool': 'brown_terracotta',                   # the zenith dither (with light_blue_concrete)
    'white_wool': 'pink_terracotta',                         # clouds
    'light_blue_terracotta': 'gray_terracotta',              # far mountains
    'cyan_terracotta': 'black_terracotta',                   # near ridges
    'white_concrete_powder': 'light_gray_terracotta',        # snow on the peaks
    'cyan_concrete': 'purple_terracotta',                    # the sea
    'cyan_concrete_powder': 'red_concrete_powder',           # glints on the sea
}
MOON = {'bearing': 0.0, 'y': 226.0, 'r': 6.0}


def _sky_day(x, y, z):
    """the day block of a dome shell cell"""
    d, br = _d(x, z), _bearing(x, z)
    se = _se(br)
    # the painted band on the dome base (south-east): sea, then the mountain silhouettes
    if se > 0.15:
        sea_top = 197 + int(round(2 * _vnoise(br / 6.0, 0.0, 1.0, 101)))
        if y <= sea_top:
            return 'cyan_concrete_powder' if _mix(x, y, z, 103) < 0.06 else 'cyan_concrete'
        far = sea_top + 5 + 10 * _fbm(br / 3.0, 0.0, 1.0, 107) ** 1.3 * se
        near = sea_top + 2 + 7 * _fbm(br / 2.0, 5.0, 1.0, 109) * se
        if y <= near:
            return 'cyan_terracotta'
        if y <= far:
            return 'white_concrete_powder' if y >= far - 1.2 and far > sea_top + 12 else 'light_blue_terracotta'
    # clouds: soft patches in the low / high sky
    if 212 <= y <= 244:
        c = _fbm(br * 0.9, y * 2.2, 9.0, 111) + 0.15 * _vnoise(br * 2.0, y * 4.0, 5.0, 113)
        if c > 0.66:
            return 'white_wool'
    for top, blk in BANDS:
        if y <= top:
            if blk == 'zenith':
                return 'light_blue_wool' if _mix(x, y, z, 117) < 0.5 else 'light_blue_concrete'
            if blk == 'light_blue_concrete_powder' and y > 231 and _mix(x, y, z, 119) < (y - 231) / 6.0:
                return 'light_blue_concrete'                 # the band edges dither
            if blk == 'white_concrete' and y > 206 and _mix(x, y, z, 121) < (y - 206) / 6.0:
                return 'light_blue_concrete_powder'
            return blk
    return 'light_blue_concrete'


def _moon(x, y, z):
    """'face' / 'rim' / 'glow' or None for a dome shell cell (the crimson red moon on the north wall)"""
    br = _bearing(x, z)
    if abs(_angdiff(br, MOON['bearing'])) > 20:
        return None
    s = _angdiff(br, MOON['bearing']) * math.pi / 180 * _d(x, z)
    rr = math.hypot(s, y + 0.5 - MOON['y'])
    if rr <= MOON['r'] - 1.0:
        return 'face'
    if rr <= MOON['r']:
        return 'rim'
    if rr <= MOON['r'] + 0.9:
        return 'glow'
    return None


MOON_BLOCK = {'face': 'red_concrete', 'rim': 'redstone_block', 'glow': 'shroomlight'}


def _dome(g):
    """the dome shell (look-neutral keys 'sky:<day block>'), the inner skin lights, the outer roof lights"""
    interior = set()
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            if _d(x, z) > DOME_R + 1:
                continue
            for y in range(DOME_Y0 + 1, DOME_TOP + 1):
                if _dome_in(x, y, z):
                    interior.add((x, y, z))
    shell = set()
    for (x, y, z) in interior:
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0)):
            p = (x + dx, y + dy, z + dz)
            if p not in interior:
                shell.add(p)
    return interior, shell


# ---------------------------------------------------------------------------------------------------------------
# light: flood, spawn cells, hidden lights

EMIT = {'shroomlight': 15, 'light': None}
_TRANSPARENT = ('_leaves', '_stained_glass')
_FREE = {'air', 'light', 'short_grass', 'lilac', 'cornflower', 'allium', 'azure_bluet', 'oxeye_daisy', 'lily_of_the_valley'}
_THIN = ('_wall',)


def _bid(b):
    return b.split('[', 1)[0][len(B):]


def _opaque(b):
    """blocks light and counts as a spawn floor (full, solid, opaque)"""
    if b is None:
        return False
    n = _bid(b)
    return not (n in _FREE or n == 'barrier' or n.endswith(_TRANSPARENT) or n.endswith(_THIN))


def _emits(b):
    n = _bid(b)
    if n == 'light':
        return int(b[b.index('level=') + 6:].rstrip(']'))
    return EMIT.get(n) or 0


class _Grid:
    """dense flat index over the box with a 1-cell opaque margin (no light leaks in, indices never wrap)"""

    def __init__(self):
        self.x0, self.y0, self.z0 = BOX['x0'] - 1, BOX['y0'] - 1, BOX['z0'] - 1
        self.nx, self.ny, self.nz = BOX['x1'] - BOX['x0'] + 3, BOX['y1'] - BOX['y0'] + 3, BOX['z1'] - BOX['z0'] + 3
        self.N = self.nx * self.ny * self.nz
        self.offs = (self.ny * self.nz, -self.ny * self.nz, self.nz, -self.nz, 1, -1)

    def idx(self, x, y, z):
        return ((x - self.x0) * self.ny + (y - self.y0)) * self.nz + (z - self.z0)

    def opaque(self, cells):
        opq = bytearray(self.N)
        for xi in range(self.nx):
            for yi in range(self.ny):
                base = (xi * self.ny + yi) * self.nz
                if xi in (0, self.nx - 1) or yi in (0, self.ny - 1):
                    opq[base:base + self.nz] = b'\x01' * self.nz
                else:
                    opq[base] = opq[base + self.nz - 1] = 1
        for (x, y, z), b in cells.items():
            if _opaque(b):
                opq[self.idx(x, y, z)] = 1
        return opq

    def flood(self, opq, lv, seeds):
        buckets = [[] for _ in range(16)]
        for i in seeds:
            buckets[lv[i]].append(i)
        N, offs = self.N, self.offs
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

    def light(self, cells, opq=None):
        opq = opq if opq is not None else self.opaque(cells)
        lv = bytearray(self.N)
        seeds = []
        for (x, y, z), b in cells.items():
            e = _emits(b)
            if e:
                i = self.idx(x, y, z)
                lv[i] = e
                seeds.append(i)
        self.flood(opq, lv, seeds)
        return opq, lv


def _free(cells, c):
    b = cells.get(c)
    return b is None or _bid(b) in _FREE


def spawn_cells(cells):
    """feet cells a hostile mob could spawn in: an opaque, non-barrier floor block below, two free cells (inside the box)"""
    out = []
    for (x, y, z), b in cells.items():
        if not _opaque(b) or y + 2 > BOX['y1']:
            continue
        if _free(cells, (x, y + 1, z)) and _free(cells, (x, y + 2, z)):
            out.append((x, y + 1, z))
    return sorted(out, key=lambda c: (c[1], c[2], c[0]))


def _walk_cell(c):
    return _d(c[0], c[2]) <= WALK + 0.5 and c[1] == FLOOR_Y + 1


def _hidden_lights(looks):
    """light[level=15] cells, the same in every look, so every spawn cell of every look has block light >= 12 (the walk
    floor >= 10 from the y-206 layer: nothing may stand above it); greedy and deterministic: a light goes 1 b above a
    dark spawn cell (or into it when that cell is not free), then the flood is updated"""
    G = _Grid()
    added = []
    states = []
    for cells in looks:
        opq, lv = G.light(cells)
        states.append((cells, opq, lv))
    for k, (cells, opq, lv) in enumerate(states):
        for c in spawn_cells(cells):
            need = FLOOR_LIGHT_MIN if _walk_cell(c) else SPAWN_LIGHT_MIN if _dome_in(*c) else 1
            if lv[G.idx(*c)] >= need:
                continue
            x, y, z = c
            assert not (_d(x, z) <= WALK + 0.5 and CLEAR_Y[0] <= y <= CLEAR_Y[1] + 1), f'dark walk cell {c}'
            spot = (x, y + 1, z) if _free(cells, (x, y + 1, z)) and (x, y + 1, z) not in cells and y + 1 <= BOX['y1'] \
                else (x, y, z)
            if spot in cells and _bid(cells[spot]) != 'air':
                spot = (x, y + 1, z)
            added.append(spot)
            for cs, opq2, lv2 in states:
                cs[spot] = LIGHT15
                i = G.idx(*spot)
                lv2[i] = 15
                G.flood(opq2, lv2, [i])
    return added


# ---------------------------------------------------------------------------------------------------------------
# the layout

_CACHE = {}


def _base():
    """{cell: block or ('sky', day block) / ('moon', part, day block) / ('patch', ...) / ('pane', ...)}: the look-neutral
    layout, the look markers resolved by _resolve"""
    g = {}
    tops = {}
    # ground columns
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            d = _d(x, z)
            if d > DOME_R + 0.5:
                continue
            if d <= RIM_R:
                for y in range(DOME_Y0, FLOOR_Y):
                    if y == SENT_Y:
                        blk = _p('polished_deepslate')
                    elif y >= FLOOR_Y - 2:
                        blk = _p('polished_andesite') if d > WALK else _p('stone_bricks')
                    else:
                        blk = _p('stone')
                    g[(x, y, z)] = blk
                g[(x, FLOOR_Y, z)] = floor_top(x, z) if d <= WALK else _p('polished_andesite')
                continue
            top = ground_top(x, z)
            if top is not None and dome_ceiling(x, z) <= DOME_Y0:
                continue                                          # outside the dome (its base ring is shell)
            if top is None:                                       # the sea below the south-east cliff
                g[(x, SEA_Y, z)] = ('sky', 'cyan_concrete_powder' if _mix(x, z, 131) < 0.05 else 'cyan_concrete')
                continue
            tops[(x, z)] = top
            se = _se(_bearing(x, z))
            for y in range(DOME_Y0, top + 1):
                if y == top:
                    steep = top > FLOOR_Y + 3 and _mix(x, z, 133) < 0.35
                    blk = _rock(x, y, z) if steep else _p('grass_block[snowy=false]')
                elif y >= top - 2 and y >= FLOOR_Y - 3:
                    blk = _p('dirt') if se < 0.5 or d < edge_r(_bearing(x, z)) - 1.5 else _rock(x, y, z)
                else:
                    blk = _rock(x, y, z)
                g[(x, y, z)] = blk
    # plants on grass (none on the crimson look's red patches)
    for (x, z), top in tops.items():
        if _bid(g[(x, top, z)]) != 'grass_block':
            continue
        if _patch(x, z):
            g[(x, top, z)] = ('patch', _p('grass_block[snowy=false]'))
            continue
        p = _plant(x, z, top)
        if p == 'lilac':
            g[(x, top + 1, z)] = _p('lilac[half=lower]')
            g[(x, top + 2, z)] = _p('lilac[half=upper]')
        elif p:
            g[(x, top + 1, z)] = _p(p)
    # the rim: balustrade and wisp posts
    wc = _wall_cells()
    for (x, z), kind in wc.items():
        if kind == 'post':
            g[(x, 201, z)] = _p('quartz_pillar[axis=y]')
            g[(x, 202, z)] = _p('chiseled_quartz_block')
        else:
            g[(x, 201, z)] = _wall_state('stone_brick_wall' if kind == 'wall_s' else 'diorite_wall', x, z, wc)
    for (x, z) in WISP_CELLS:
        g[(x, FLOOR_Y, z)] = _p('polished_andesite')
        g[(x, 201, z)] = _p('polished_diorite')
        g[(x, 202, z)] = _p('quartz_pillar[axis=y]')
        g[(x, 203, z)] = _p('chiseled_quartz_block')
        g.pop((x, 204, z), None)
    # ruins and trees (never over the rim ring: they stand at d >= 30)
    _ruins(g, tops)
    # the barrier ring
    for z in range(CZ - 30, CZ + 30):
        for x in range(CX - 30, CX + 30):
            d = _d(x, z)
            if not (WALK < d <= RIM_R):
                continue
            for y in range(BARRIER_Y[0], BARRIER_Y[1] + 1):
                if (x, y, z) not in g:
                    g[(x, y, z)] = _p('barrier')
    # the light layer over the walk disc
    for z in range(CZ - 27, CZ + 27):
        for x in range(CX - 27, CX + 27):
            if _d(x, z) <= WALK:
                g[(x, LIGHT_Y, z)] = _p(f'light[level={LIGHT_LV}]')
    # the dome: shell blocks where nothing else stands, the inner skin lights in stripes, the outer roof lights
    interior, shell = _dome(g)
    for c in list(g):
        if c[1] > DOME_Y0 and c not in interior and c not in shell:
            del g[c]                                  # nothing pokes out of the dome (a crown, a tower top)
    for c in shell:
        if c in g and not _opaque(g[c]):
            del g[c]                                  # leaves / glass / plants in the shell would let the sky light in
        if c in g or not _in_box(*c):
            continue
        x, y, z = c
        if y <= SEA_Y:
            continue
        g[c] = ('sky', _sky_day(x, y, z))
    for (x, y, z) in interior:
        if (x, y, z) in g:
            continue
        roof = (x, y + 1, z) in shell
        side = any(p in shell for p in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)))
        if not (roof or side) or (x % 2 if roof else y % 2):
            continue
        if any(isinstance(g.get(p), tuple) for p in ((x, y + 1, z), (x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1))):
            g[(x, y, z)] = LIGHT15
    _roof_lights(g, interior, shell)
    # the crimson look's extra cells: the moon on the dome, a few grass patches, a few window panes
    for c, v in list(g.items()):
        if isinstance(v, tuple) and v[0] == 'sky':
            m = _moon(*c)
            if m:
                g[c] = ('moon', m, v[1])
    # orphan halves of a lilac a ruin cut
    for c, v in list(g.items()):
        if isinstance(v, str) and v.startswith(_p('lilac')):
            other = (c[0], c[1] + (1 if 'lower' in v else -1), c[2])
            if not (isinstance(g.get(other), str) and g[other].startswith(_p('lilac'))):
                del g[c]
    for c, v in list(g.items()):
        if v == WINDOW_GLASS and _mix(*c, 143) < 0.3:
            g[c] = ('pane',)
    return g


def _roof_lights(g, interior, shell):
    """light[level=15] on the outside of the dome, one per 6 x 6 columns on that column's exposed top, then one on each
    top the flood leaves dark: every outer top gets block light >= 1 (Raiden's roof lights)"""
    tops = []
    for (x, y, z) in shell:
        q = (x, y + 1, z)
        if q not in shell and q not in interior and _in_box(*q) and q not in g:
            tops.append(q)
    tops.sort(key=lambda c: (c[1], c[2], c[0]))
    src = {p for p in tops if p[0] % 6 == 0 and p[2] % 6 == 0}
    for p in src:
        g[p] = LIGHT15


def _resolve(base, look):
    out = {}
    for c, v in base.items():
        if not isinstance(v, tuple):
            out[c] = v
            continue
        kind = v[0]
        if kind == 'sky':
            out[c] = _p(v[1] if look == 'day' else PAIRS[v[1]])
        elif kind == 'moon':
            out[c] = _p(v[2] if look == 'day' else MOON_BLOCK[v[1]])
        elif kind == 'patch':
            out[c] = v[1] if look == 'day' else _p('red_terracotta')
        elif kind == 'pane':
            out[c] = WINDOW_GLASS if look == 'day' else RED_GLASS
    return out


def _build():
    if 'all' not in _CACHE:
        base = _base()
        lays = [_resolve(base, lk) for lk in LOOKS]
        hidden = _hidden_lights(lays)
        _CACHE['all'] = (dict(zip(LOOKS, lays)), hidden)
    return _CACHE['all']


def arena_layout(look=None):
    """{(x, y, z): block} of every non-air block of the box in `look` (None = 'day')."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    return dict(_build()[0][look])


def hidden_lights():
    return list(_build()[1])


def slices():
    """21 build slices: 3-layer slabs of the whole box from y 190 up (the last one layer), each 97 x 3 x 97 = 28 227
    blocks <= 32 768; disjoint, covering the box."""
    out = []
    y = BOX['y0']
    while y <= BOX['y1']:
        y1 = min(BOX['y1'], y + 2)
        out.append(((BOX['x0'], y, BOX['z0']), (BOX['x1'], y1, BOX['z1'])))
        y = y1 + 1
    return out


# ---------------------------------------------------------------------------------------------------------------
# looks

def look_cells():
    """{cell: {look: block or None}} of every cell some look changes"""
    lays = {lk: arena_layout(lk) for lk in LOOKS}
    cells = set()
    for lk in LOOKS[1:]:
        cells |= {c for c in set(lays[lk]) | set(lays[LOOKS[0]]) if lays[lk].get(c) != lays[LOOKS[0]].get(c)}
    return {c: {lk: lays[lk].get(c) for lk in LOOKS} for c in sorted(cells)}


def _spans(cells):
    """row spans along x of {(x, y, z): block}: fill / setblock ... strict (y, z ascending)"""
    out = []
    rows = {}
    for (x, y, z), b in cells.items():
        rows.setdefault((y, z), []).append((x, b))
    for (y, z) in sorted(rows):
        xs = sorted(rows[(y, z)])
        i = 0
        while i < len(xs):
            j = i
            while j + 1 < len(xs) and xs[j + 1][0] == xs[j][0] + 1 and xs[j + 1][1] == xs[i][1]:
                j += 1
            x0, x1, b = xs[i][0], xs[j][0], xs[i][1]
            out.append(f'setblock {x0} {y} {z} {b} strict' if x0 == x1 else f'fill {x0} {y} {z} {x1} {y} {z} {b} strict')
            i = j + 1
    return out


def _pair_jobs(look):
    """[(box, new, old)]: per 8 x 8 column tile and per pair, the y range of the cells that pair turns into `look` (from
    the other look); every old-block cell inside such a box wants exactly `new` in `look` (the pairs are one-to-one and
    their blocks are used nowhere else), so the replace never touches a wrong cell"""
    lc = look_cells()
    other = LOOKS[1] if look == LOOKS[0] else LOOKS[0]
    want = {}
    for c, per in lc.items():
        a, b = per[other], per[look]
        if a is None or b is None:
            continue
        an, bn = _bid(a), _bid(b)
        if (look == 'crimson' and PAIRS.get(an) == bn) or (look == 'day' and PAIRS.get(bn) == an):
            want.setdefault((c[0] // TILE, c[2] // TILE, an, bn), []).append(c[1])
    jobs = []
    for (tx, tz, an, bn), ys in sorted(want.items()):
        x0, z0 = max(BOX['x0'], tx * TILE), max(BOX['z0'], tz * TILE)
        x1, z1 = min(BOX['x1'], tx * TILE + TILE - 1), min(BOX['z1'], tz * TILE + TILE - 1)
        jobs.append((((x0, min(ys), z0), (x1, max(ys), z1)), _p(bn), _p(an)))
    return jobs


def look_lines(look):
    """[[cmd]]: the job that turns any built look into `look`: the pair replaces (`fill <tile box> <new> replace <old>`)
    in 3 slices, then the absolute spans of every changed cell the pairs leave wrong (the moon, the grass patches, the
    window panes) in the last slice; idempotent on `look` itself."""
    assert look in LOOKS, look
    jobs = _pair_jobs(look)
    # the cells the replaces leave wrong (from the other look): the spans fix them
    lc = look_cells()
    other = LOOKS[1] if look == LOOKS[0] else LOOKS[0]
    fixed = {}
    for c, per in lc.items():
        a, b = per[other], per[look]
        an = _bid(a) if a else None
        after = a
        if an in PAIRS and look == 'crimson':
            after = _p(PAIRS[an])
        elif an in PAIRS.values() and look == 'day':
            after = _p(next(k for k, v in PAIRS.items() if v == an))
        if after != b:
            fixed[c] = b or 'minecraft:air'
    cmds = [f'fill {b[0][0]} {b[0][1]} {b[0][2]} {b[1][0]} {b[1][1]} {b[1][2]} {new} replace {old}' for b, new, old in jobs]
    n = len(cmds)
    k = max(1, MAX_LOOK_SLICES - 1)
    groups = [cmds[i * n // k:(i + 1) * n // k] for i in range(k)]
    groups = [gp for gp in groups if gp]
    groups.append(_spans(fixed))
    return [gp for gp in groups if gp]


def props(look=None):
    """No arena display props (the wisps and the moon halo are kit props the module spawns at POINTS)."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    return []


# ---------------------------------------------------------------------------------------------------------------
# named points (absolute world coordinates)

POINTS = {
    'centre': (float(CX), float(CY), float(CZ), 0.0),
    'spawn': (float(CX), float(CY), float(CZ), 0.0),            # the boss anchor (yaw 0 faces south, the arrival)
    'start': (START['x'], START['y'], START['z'], START['yaw']),
    # the three white wisps float over their rim posts (bearings 0 / 150 / 210, r 28; api.WISP_POSTS)
    'wisps': tuple((x + 0.5, 204.6, z + 0.5, yaw_facing_centre(x + 0.5, z + 0.5)) for x, z in WISP_CELLS),
    'moon': (*polar_point(DOME_R - 2.5, MOON['bearing'], MOON['y'])[0:1], MOON['y'],
             polar_point(DOME_R - 2.5, MOON['bearing'])[2], 180.0),   # the moon disc centre (crimson), just inside the wall
}


def render_hints():
    return {'top': {'centre': (CX, CZ), 'r': 46}, 'eye': START, 'boss': (CX, CY, CZ)}


# ---------------------------------------------------------------------------------------------------------------
# the domain entrance (chapter-4 dungeon, theme.md §5): the gravestone with the crimson flames

FOYER = (-6, 24, 5, 39)                  # zone 1 (Raiden's foyer box), the player's spawn zone
HALL = (-10, 4, 9, 23)                   # zone 2 (kind 9): the domain entrance, the gate at its centre
GATE = (0, 201, 14)
DOOR = {'a': 1, 'b': 2, 'x0': -2, 'x1': 1, 'z0': 23, 'z1': 24, 'mx': 0, 'mz': 24, 'ya': 0, 'yb': 180, 'h': 0,
        'y0': 201, 'y1': 205, 'l0': 206, 'l1': 207, 'my': 201, 'tx0': -2, 'tx1': 1, 'tz0': 24, 'tz1': 24, 'tm': 210}
GRAVE_CELL = (-1, 9)                     # the gravestone's north-west foot cell (2 wide x -1..0; the slab row z 9, base z 9..10)
GRAVE_FLAME = (0.0, 205.3, 9.5)          # the crimson flame point: centred on the slab's top face (y 205)
# the flame point relative to the kind-9 zone marker (room/gen_zone summons it at (cx.0, cy, cz.0) = the gate (0, 201, 14));
# S3's prep summons its flame anchor rlk_kn_grave at the marker + GRAVE (request R-S3-2)
GRAVE = (round(GRAVE_FLAME[0] - GATE[0], 3), round(GRAVE_FLAME[1] - GATE[1], 3), round(GRAVE_FLAME[2] - GATE[2], 3))


def _ecell(x0, z0, x1, z1, entry):
    ex0, ez0, ex1, ez1 = entry
    return {'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'ix0': x0 + 1, 'iz0': z0 + 1, 'ix1': x1 - 1, 'iz1': z1 - 1,
            'ex0': ex0 * 100, 'ez0': ez0 * 100, 'ex1': ex1 * 100, 'ez1': ez1 * 100,
            'sx0': x0 + 2, 'sz0': z0 + 2, 'sx1': x1 - 2, 'sz1': z1 - 2}


def _ezone(zid, kind, box, centre, cells):
    x0, z0, x1, z1 = box
    return {'id': zid, 'kind': kind, 'x0': x0, 'z0': z0, 'x1': x1, 'z1': z1, 'cx': centre[0], 'cz': centre[1],
            'mn': 1, 'mx': 1, 'nc': len(cells), 'ncm': len(cells) - 1, 'cells': cells, 'by': 0, 'cy': 201, 'sd': 0,
            'pits': []}


def _entrance_blocks():
    """zone 1: a ruined Fontaine foyer (pale tiles, stone-brick walls with quartz pilasters, moss, lilac planters); zone 2:
    the overgrown court of the gravestone: grass and white flowers around a tiled path, broken walls with a round window,
    two broken columns, and on the north side the gravestone (wiki: the stone with Cuzabina's name, crimson flames):
    a 2-wide slab of polished deepslate on a chiseled base, a carved top (chiseled polished blackstone) and a dark
    plinth; hidden light layers keep both zones lit (no spawns)"""
    out = {}
    door = {(x, z) for x in range(DOOR['x0'], DOOR['x1'] + 1) for z in range(DOOR['z0'], DOOR['z1'] + 1)}

    def walls(bl, x0, z0, x1, z1, top, pil, seed):
        for x in range(x0, x1 + 1):
            for z in range(z0, z1 + 1):
                if not (x in (x0, x1) or z in (z0, z1)):
                    continue
                along = z - z0 if x in (x0, x1) else x - x0
                pillar = along % pil == 0 or (x in (x0, x1) and z in (z0, z1))
                brk = top - (int(3 * _fbm(along * 0.7, 0.0, 1.0, seed)) if not pillar else 0)
                for y in range(201, top + 1):
                    if (x, z) in door:
                        if y >= DOOR['l0']:
                            bl[(x, y, z)] = _p('quartz_bricks')
                        continue
                    if y > brk:
                        bl[(x, y, z)] = _p('barrier')
                        continue
                    if pillar:
                        m = 'oxidized_copper' if y == top and (along // pil) % 2 == 0 else 'quartz_bricks'
                    elif y == 204:
                        m = 'polished_deepslate'
                    else:
                        h = _mix(x, y, z, seed)
                        m = 'mossy_stone_bricks' if h < 0.2 else 'cracked_stone_bricks' if h < 0.3 else 'stone_bricks'
                    bl[(x, y, z)] = _p(m)

    def lights(bl, x0, z0, x1, z1, y):
        for x in range(x0 + 2, x1 - 1, 3):
            for z in range(z0 + 2, z1 - 1, 3):
                if (x, y, z) not in bl:
                    bl[(x, y, z)] = LIGHT15

    # zone 1: the foyer
    fx0, fz0, fx1, fz1 = FOYER
    z1 = {}
    for x in range(fx0, fx1 + 1):
        for z in range(fz0, fz1 + 1):
            z1[(x, 199, z)] = _p('stone')
            if x in (fx0, fx1) or z in (fz0, fz1):
                m = 'polished_andesite'
            elif x in (-1, 0):
                m = 'chiseled_stone_bricks' if z % 4 == 0 else 'polished_diorite'
            elif (x + z) % 7 == 0 and _mix(x, z, 201) < 0.5:
                m = 'moss_block'
            else:
                m = 'smooth_stone' if _mix(x // 2, z // 2, 203) < 0.6 else 'calcite'
            z1[(x, 200, z)] = _p(m)
    walls(z1, fx0, fz0, fx1, fz1, 207, 4, 205)
    for x in (fx0 + 1, fx1 - 1):
        for z in range(fz0 + 2, fz1 - 1):
            if z % 4 != 0:
                z1[(x, 200, z)] = _p('grass_block[snowy=false]')
                h = _mix(x, z, 207)
                if h < 0.35:
                    z1[(x, 201, z)] = _p('lilac[half=lower]')
                    z1[(x, 202, z)] = _p('lilac[half=upper]')
                elif h < 0.7:
                    z1[(x, 201, z)] = _p('allium' if h < 0.5 else 'lily_of_the_valley')
    lights(z1, fx0, fz0, fx1, fz1, 205)
    out[1] = z1

    # zone 2: the gravestone court
    hx0, hz0, hx1, hz1 = HALL
    gx, gz = GATE[0], GATE[2]
    z2 = {}
    for x in range(hx0, hx1 + 1):
        for z in range(hz0, hz1 + 1):
            z2[(x, 199, z)] = _p('stone')
            edge = x in (hx0, hx1) or z in (hz0, hz1)
            path = abs(x + 0.5 - gx) <= 1.6 and z >= gz - 1
            ring = 2.6 <= math.hypot(x + 0.5 - gx, z + 0.5 - gz) <= 3.6
            if edge:
                m = 'polished_andesite'
            elif path or ring:
                m = 'polished_diorite' if (x + z) % 2 else 'smooth_stone'
            elif z <= hz0 + 7:
                m = 'calcite' if _mix(x, z, 211) < 0.3 else 'smooth_stone'
            else:
                m = 'grass_block[snowy=false]'
            z2[(x, 200, z)] = _p(m)
            if m.startswith('grass') and not edge:
                h = _mix(x, z, 213)
                if h < 0.12:
                    z2[(x, 201, z)] = _p('lily_of_the_valley')
                elif h < 0.2:
                    z2[(x, 201, z)] = _p('oxeye_daisy')
                elif h < 0.5:
                    z2[(x, 201, z)] = _p('short_grass')
    walls(z2, hx0, hz0, hx1, hz1, 208, 5, 215)
    # the north wall: a round window (quartz frame, light-blue glass) over the gravestone
    for x in range(hx0, hx1 + 1):
        for y in range(201, 214):
            rr = math.hypot(x + 0.5 - (gx + 0.0), y + 0.5 - 209.0)
            if rr <= 2.4:
                z2[(x, y, hz0)] = WINDOW_GLASS
            elif rr <= 3.4:
                z2[(x, y, hz0)] = _p('quartz_bricks')
            elif y > 209 and abs(x + 0.5 - gx) <= 4.5:
                z2[(x, y, hz0)] = _stone(x, y, hz0)
    # two broken columns flanking the court
    for cxz, h in (((-6, 9), 5), ((5, 9), 3)):
        x, z = cxz
        z2[(x, 200, z)] = _p('chiseled_stone_bricks')
        for y in range(201, 201 + h):
            z2[(x, y, z)] = _p('quartz_pillar[axis=y]')
    # the gravestone: plinth, base, slab, carved top
    gx0, gz0 = GRAVE_CELL
    for x in range(gx0 - 1, gx0 + 3):
        for z in range(gz0 - 1, gz0 + 3):
            z2[(x, 200, z)] = _p('polished_blackstone')
    for x in (gx0, gx0 + 1):
        for z in (gz0, gz0 + 1):
            z2[(x, 201, z)] = _p('chiseled_polished_blackstone')
        z2[(x, 202, gz0)] = _p('polished_deepslate')
        z2[(x, 203, gz0)] = _p('polished_deepslate')
        z2[(x, 204, gz0)] = _p('chiseled_polished_blackstone')
        z2[(x, 202, gz0 + 1)] = _p('polished_blackstone_bricks')
    lights(z2, hx0, hz0, hx1, hz1, 206)
    # keep the gate column free
    for c in [(x, y, z) for x in (gx - 1, gx) for z in (gz - 1, gz) for y in range(201, 206)]:
        z2.pop(c, None)
    out[2] = z2
    return out


def entrance_layout():
    """The domain entrance (theme.md §5): zone 1 = the foyer (kind 0, the player's spawn), zone 2 = the gravestone court
    (kind 9, the gate at its centre), one door. `stele_glow` = the crimson flame point over the gravestone (absolute; the
    module's prep starts its particle chain there), `grave` = the same point relative to the kind-9 zone marker (= GRAVE);
    no glyph props."""
    foyer = _ezone(1, 0, FOYER, (0, 32), [_ecell(*FOYER, (-4, 26, 4, 37))])
    hall = _ezone(2, 9, HALL, (GATE[0], GATE[2]), [_ecell(*HALL, (-8, 6, 8, 20))])
    cur = {'n': 2, 'zones': [foyer, hall], 'doors': [dict(DOOR)], 'spawn': {'x': 0, 'z': 33, 'yaw': 180},
           'spot': {'x': 0, 'z': 33}}
    clear = {1: [(FOYER[0], 199, FOYER[1], FOYER[2], 230, FOYER[3])],
             2: [(HALL[0], 199, HALL[1], HALL[2], 230, HALL[3])]}
    return {'cur': cur, 'blocks': _entrance_blocks(), 'clear': clear, 'gate': GATE, 'glyphs': {},
            'stele_glow': GRAVE_FLAME, 'grave': GRAVE,
            'th': {'lb': _p('quartz_bricks'), 'lb2': _p('polished_deepslate')}}
