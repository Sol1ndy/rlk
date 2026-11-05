"""Arena theme `hr_field` 「달빛 억새밭」: the moonlit silver-grass field where 홍련 (the special boss, module `scarlet`)
waits (scratchpad hr/PLAN.md §6; mood sheets hr/ref/arena_*.jpg, understand/arena.md). An original composition in the
footage's mood: an asymmetric field with a lotus pond to the north, one old pine leaning over the water, a stone lantern
on a rock islet, the moon low over the far end in open sky; no stair, no pair of tall masses framing the moon, no glyphs,
no monoliths.

Theme module (scratchpad az/contract/theme.md): plain Python, stdlib only, deterministic, no side effects on import,
never writes files. The arena generator (tools/build_mboss_arena.py) imports `arena_layout`, `slices`, `look_lines`,
`SENTINEL` and `CHECK`; the module generator (api.deco()) reads `DECO`; the tests and renders read `POINTS`, the
constants and `look_cells`. The constants copied from tools/mboss_scarlet/api.py (MOON_POS, SEAT_POS, LOOK_ID,
DARK_SLICES, DARK_LIGHT) are asserted equal by HR/tests/test_arena_hr.py.

Coordinates: the centre C (880, 201, 8) is a block corner, floor blocks at y 200, stand height 201. A cell (x, z) is "at
distance d" when its centre (x + 0.5, z + 0.5) is d blocks from (880, 8) horizontally; bearings are compass bearings
(0 north = -z: the moon side, 90 east = +x, 180 south = the arrival).

  walk (d <= 25)          y 200 flat full blocks: mycelium 70 %, pale moss 12 %, coarse dirt 10 %, tuff 8 % (flush
                          stones), patchy; short dry grass on 25 % and tall dry grass on 12 % of the mycelium cells (no
                          collision, #rlk:dash_pass); a foot-level light grid at y 201 in grass-free cells (light 15,
                          dark 9) and the light layer y 206 (15, dark 6): the floor >= 12 (moon, crimson) / >= 6 (dark).
                          Nothing else above the walk disc below y 226. The seat clearing round api.SEAT_POS.
  ring (25 < d <= 27)     the same floor; barrier y 201..215 (closed)
  north (300..60 deg)     the lotus pond r 27-36 (irregular; water 1 deep over mud, packed-mud / mud-brick rim, lily
                          pads, big dripleaf leaves; the 8 kit lotus props at DECO), a flat rock islet at 28 deg / r 31
                          with the lotus stone lantern (6 b: petal base, post, upturned cup, a four-window firebox,
                          a curved roof, a bud finial), the far bank r 36-41 (mossy tuff boulders, dry grass, 1-3 b), and
                          the one old pine at 322 deg / r 38 on its boulder, 14 b, its trunk leaning in steps out over
                          the water toward the moon, its flat cloud-layer crowns ending at ~353 deg
  sides (60..300 via S)   low dry-stone walls at r 27-28.4 (1-2 b, moss carpet), small stone lanterns every 30 deg
                          (warm ochre froglight fireboxes), a 3-b gap at the arrival (x 879..881); the outer field
                          (moss, coarse dirt, mycelium, podzol; dry grass), bamboo groves r 30-37, six cherry trees at
                          70 / 110 / 140 / 220 / 250 / 290 deg, r 32-35
  beyond (r 38-46)        tuff / deepslate outcrops (<= 6 b) and dark tree masses (spruce, dark oak) outside the moon's
                          +-25 deg sector, the ground rising to the dome base
  sky                     a block dome (superellipse p 4, r 46 at the base, top y 250) in elevation bands from the eye
                          at C: horizon light-blue terracotta, body blue terracotta, a dithered zenith with black
                          terracotta; a painted band of ridges (gray / black terracotta) and mist on its base; lit from
                          inside by light stripes on its skin (no world-time dependence); light on its outer roof
  moon                    a vertical block disc r 5 facing south, centre api.MOON_POS (889, 218, -34): bearing 12,
                          elevation 22 from C, in open sky right of the pine crown; white concrete face, light-gray
                          maria, snow highlights, a pearlescent froglight rim (the kit moon_halo card 1 b before it)

Looks (PLAN §6.3-§6.5): `moon` (P1, the default the framework's ensure restores), `crimson` (P2: dry grass -> crimson
roots, mycelium -> crimson nylium, pale moss -> nether wart block, the dome to crimson planks / purple terracotta, the moon
pink with red maria, cherry crowns -> nether wart block), `dark` (the gauntlets, from crimson: the dome, the moon and the
lantern fireboxes black, the walk light layer 6, the foot grid 9, the decor lights 0; DARK_LIGHT false = fallback B: the
dome / moon / lanterns only). `look_lines(look)` = absolute fills of every cell any look changes (the union), in its
state in `look`, merged into boxes of equal blocks: block-exact from any source look; 4 real slices (far dome + moon,
near dome, the outer field / crowns / lanterns / decor lights, the walk floor + grass + its light); `dark` puts two empty
padding slices after each real one but the last, so its real slices land 3 t apart (api.DARK_SLICES). A plant and its
support always change in the same slice (floor rows first), so every plant stands on a valid support at every tick.
"""
import math

THEME = 'hr_field'
AID = 'hr_field'

CX, CY, CZ = 880, 201, 8
RAD, WALK, SAFE = 28, 25, 23
BOX = {'x0': 832, 'y0': 190, 'z0': -40, 'x1': 928, 'y1': 250, 'z1': 56}
START = {'x': 880.5, 'y': 201.0, 'z': 31.5, 'yaw': 180.0, 'pitch': 0.0}
LOOKS = ('moon', 'crimson', 'dark')
CHECK = {'n': 5, 'theme': THEME, 'ver': 1, 'cx': CX, 'cy': CY, 'cz': CZ, 'r': RAD, 'walk': WALK, 'safe': SAFE,
         'start': dict(START), 'box': dict(BOX), 'looks': list(LOOKS), 'oob': {'y0': 198, 'y1': 236}}

# copied from tools/mboss_scarlet/api.py (asserted equal by HR/tests/test_arena_hr.py)
MOON_POS = (889.0, 218.0, -34.0)
MOON_BEARING, MOON_ELEV, MOON_R = 12, 22, 5
SEAT_POS = (884.0, 201.0, 5.0)    # I1b (lead decision 1): 5 b nearer start on the same line (D0: 884.5 201 0)
LOOK_ID = {'moon': 1, 'crimson': 2, 'dark': 3}
DARK_SLICES = (-17, -14, -11, -8)
DARK_LIGHT = True

FLOOR_Y = CY - 1                 # 200: the floor top
SENT_Y = 196                     # the sentinel cell (polished tuff under the centre)
LIGHT_Y = 206                    # the light layer over the walk disc
CLEAR_Y = (201, 225)             # above the walk disc: only the light layer (and the foot grid at y 201)
BARRIER_R, BARRIER_Y = 27.0, (201, 215)
WALL_R = (27.0, 28.4)            # the dry-stone walls (sides and south)
DOME_R, DOME_Y0, DOME_TOP, DOME_P = 46.0, 190, 249, 4.0     # interior y 191..249, the roof shell up to y 250
EYE = CY + 1.62
MOON_Z = -35                     # the moon plate cells (their south face at z -34 = MOON_POS z)
FLOOR_MIN = {'moon': 12, 'crimson': 12, 'dark': 6}         # block light on the walk cells (y 201)
SPAWN_MIN = 1                    # block light on every other spawnable cell (vanilla: monsters need block light 0)
HIDDEN_LV = 7                    # the spawn-proofing lights outside the walk (the same in every look)
# light levels per look (moon, crimson, dark) of the light kinds
LV = {'lay': (15, 15, 6), 'grid': (15, 15, 9), 'decor': (12, 12, 0), 'skin': (15, 15, 0)}
DARK_PAD = 2
MAX_FILL = 32768
SENTINEL = ((CX, SENT_Y, CZ), 'minecraft:polished_tuff')

B = 'minecraft:'


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


def yaw_to(src, dst):
    """Minecraft yaw from src (x, _, z) toward dst"""
    return round(math.degrees(math.atan2(-(dst[0] - src[0]), dst[2] - src[2])) % 360, 2)


# ---------------------------------------------------------------------------------------------------------------
# blocks

def _leaves(kind):
    return _p(f'{kind}_leaves[distance=1,persistent=true,waterlogged=false]')


def _stairs(kind, facing, half):
    return _p(f'{kind}_stairs[facing={facing},half={half},shape=straight,waterlogged=false]')


def _wall(kind):
    return _p(f'{kind}_wall[east=none,north=none,south=none,up=true,waterlogged=false,west=none]')


def _bars(ew):
    return _p(f'iron_bars[east={"true" if ew else "false"},north={"false" if ew else "true"},'
              f'south={"false" if ew else "true"},waterlogged=false,west={"true" if ew else "false"}]')


def _bamboo(leaves, age):
    return _p(f'bamboo[age={age},leaves={leaves},stage=0]')


def _light(lv):
    return _p(f'light[level={lv}]')


WATER = _p('water')
BARRIER = _p('barrier')
LIGHT_HID = _light(HIDDEN_LV)
LOG_Y = {k: _p(f'{k}_log[axis=y]') for k in ('spruce', 'cherry', 'dark_oak')}

# block classes for light (opaque blocks stop it; leaves and water dampen it by one more) and spawning (free cells: no
# collision, no fluid)
_PLANT = {'short_dry_grass', 'tall_dry_grass', 'crimson_roots'}
_FREE = {'air', 'light'} | _PLANT
_SEE = _FREE | {'barrier'}                                    # what a sight line passes (invisible / no-collision blocks)
_THIN = ('_wall', '_stairs', '_slab', 'iron_bars', 'moss_carpet', 'lily_pad', 'big_dripleaf', 'bamboo')
_DAMP = ('_leaves', 'water')


def _bid(b):
    return b.split('[', 1)[0][len(B):]


def _opaque(b):
    """blocks light and counts as a spawn floor (full, solid, opaque)"""
    if b is None:
        return False
    n = _bid(b)
    return not (n in _FREE or n == 'barrier' or n.endswith(_THIN) or n.endswith(_DAMP))


def _damp(b):
    return b is not None and _bid(b).endswith(_DAMP)


EMIT = {'ochre_froglight': 15, 'pearlescent_froglight': 15}


def _emits(b):
    n = _bid(b)
    if n == 'light':
        return int(b[b.index('level=') + 6:].split(',')[0].rstrip(']'))
    return EMIT.get(n, 0)


# ---------------------------------------------------------------------------------------------------------------
# the field: walk floor, ground, pond

WALK_SHARE = (('tuff', 0.08), ('coarse_dirt', 0.10), ('pale_moss_block', 0.12))      # the rest mycelium (70 %)


def _walk_cells():
    return [(x, z) for z in range(CZ - 26, CZ + 26) for x in range(CX - 26, CX + 26) if _d(x, z) <= WALK]


def _ring_cells():
    return [(x, z) for z in range(CZ - 28, CZ + 28) for x in range(CX - 28, CX + 28) if WALK < _d(x, z) <= BARRIER_R]


def _floor_palette(cells, seed):
    """{cell: block id} with exact shares by quantiles of smooth noise (patches): the flush stones, the coarse dirt and
    the pale moss as clusters, mycelium elsewhere"""
    out = {c: 'mycelium' for c in cells}
    free = list(cells)
    for k, (blk, share) in enumerate(WALK_SHARE):
        n = int(round(share * len(cells)))
        sc = 2.2 if blk == 'tuff' else 3.4
        ranked = sorted(free, key=lambda c: (-(_vnoise(c[0], c[1], sc, seed + 11 * k)
                                               + 0.25 * _mix(c[0], c[1], seed + 7 * k)), c))
        for c in ranked[:n]:
            out[c] = blk
        taken = set(ranked[:n])
        free = [c for c in free if c not in taken]
    return out


# the pond (north): bearings within +-60 of north, from the barrier ring out to an irregular shore
POND_HALF = 60.0


def _pond_env(br):
    return _smooth(POND_HALF, POND_HALF - 16.0, abs(_angdiff(br, 0.0)))


def pond_outer(br):
    """the pond's outer shore radius on a bearing (27.9 at its ends .. ~37)"""
    e = _pond_env(br)
    return 27.9 + e * (6.6 + 2.6 * _vnoise(br / 9.0, 0.0, 1.0, 41))


ISLET_C = polar_point(31.0, 28.0)                 # the rock islet of the stone lantern
ISLET_R = 2.4
LANTERN_CELL = (math.floor(ISLET_C[0]), math.floor(ISLET_C[2]))


def _islet(x, z):
    return math.hypot(x + 0.5 - ISLET_C[0], z + 0.5 - ISLET_C[2]) <= ISLET_R


def _pond_kind(x, z):
    """'rim' / 'water' / 'islet' / None (not pond) for a cell outside the barrier ring"""
    d, br = _d(x, z), _bearing(x, z)
    if d <= BARRIER_R or abs(_angdiff(br, 0.0)) >= POND_HALF:
        return None
    ro = pond_outer(br)
    if d > ro:
        return None
    if _islet(x, z):
        return 'islet'
    if d <= 27.9 or d > ro - 0.6:
        return 'rim'
    return 'water'


def ground_top(x, z):
    """the ground top y of a cell outside the ring (the pond: 200, its water level), None outside the dome base"""
    d, br = _d(x, z), _bearing(x, z)
    if d > DOME_R + 0.5:
        return None
    if _pond_kind(x, z):
        return FLOOR_Y
    rise = 0.0
    north = abs(_angdiff(br, 0.0)) < POND_HALF + 8
    if north:
        ro = pond_outer(br)
        bank = _smooth(ro, ro + 3.0, d) * (1.2 + 1.6 * _fbm(x, z, 5.0, 43))
        rise = max(rise, bank)
    rise += 4.5 * _smooth(39.5, 46.0, d) * (0.7 + 0.6 * _fbm(x, z, 7.0, 47))
    rise += 0.6 * _smooth(30.0, 36.0, d) * (_fbm(x, z, 4.0, 49) - 0.3)
    return FLOOR_Y + max(0, int(math.floor(rise + 0.15)))


def _outer_top_block(x, z, top):
    """the top block of the outer field (sides / south / beyond) or the bank"""
    d, br = _d(x, z), _bearing(x, z)
    north = abs(_angdiff(br, 0.0)) < POND_HALF + 8
    v = _fbm(x, z, 3.0, 53)
    if north and top > FLOOR_Y:
        return 'moss_block' if v > 0.42 else 'tuff' if v > 0.25 else 'mossy_cobblestone'
    if d > 39.0 and _mix(x, z, 55) < 0.25:
        return 'coarse_dirt'
    if v > 0.62:
        return 'moss_block'
    if v > 0.45:
        return 'mycelium'
    if v > 0.30:
        return 'coarse_dirt'
    return 'podzol'


# ---------------------------------------------------------------------------------------------------------------
# small builders

def _put(g, x, y, z, b, force=False):
    if not _in_box(x, y, z):
        return
    if force or (x, y, z) not in g:
        g[(x, y, z)] = b


WALL_GAP = (879, 881)            # x of the 3-b gap at the arrival (south)
WALL_LANTERNS = (75, 105, 135, 165, 195, 225, 255, 285)


def _wall_sector(br):
    return abs(_angdiff(br, 0.0)) >= POND_HALF


def _walls(g):
    """the dry-stone walls (1-2 b, moss carpet on most tops) and the small lanterns every 30 deg"""
    lantern_cells = {}
    for b in WALL_LANTERNS:
        best = None
        for z in range(CZ - 30, CZ + 30):
            for x in range(CX - 30, CX + 30):
                d = _d(x, z)
                if WALL_R[0] < d <= WALL_R[1]:
                    k = (abs(d - 27.7) + 0.05 * abs(_angdiff(_bearing(x, z), b)) * d * math.pi / 180, x, z)
                    if abs(_angdiff(_bearing(x, z), b)) < 3.0 and (best is None or k < best):
                        best = k
        lantern_cells[(best[1], best[2])] = b
    for z in range(CZ - 30, CZ + 30):
        for x in range(CX - 30, CX + 30):
            d, br = _d(x, z), _bearing(x, z)
            if not (WALL_R[0] < d <= WALL_R[1]) or not _wall_sector(br):
                continue
            if z > CZ and WALL_GAP[0] <= x <= WALL_GAP[1]:
                continue
            if (x, z) in lantern_cells:
                g[(x, 201, z)] = _p('stone_bricks')
                g[(x, 202, z)] = ('fire',)
                g[(x, 203, z)] = _p('deepslate_tile_slab[type=bottom,waterlogged=false]')
                continue
            h = 2 if _vnoise(x, z, 3.0, 61) > 0.52 else 1
            for y in range(201, 201 + h):
                v = _mix(x, y, z, 63)
                g[(x, y, z)] = _p('cobblestone' if v < 0.45 else 'mossy_cobblestone' if v < 0.78 else 'tuff')
            if _mix(x, z, 65) < 0.72:
                g[(x, 201 + h, z)] = _p('moss_carpet')
    return lantern_cells


def _stone_lantern(g):
    """the lotus stone lantern (6 b) on the islet: petal base, post, upturned cup, firebox with four windows, roof,
    bud finial"""
    lx, lz = LANTERN_CELL
    out = {'n': (0, -1), 's': (0, 1), 'e': (1, 0), 'w': (-1, 0)}
    names = {'n': 'north', 's': 'south', 'e': 'east', 'w': 'west'}
    inward = {'n': 'south', 's': 'north', 'e': 'west', 'w': 'east'}
    for k, (dx, dz) in out.items():
        g[(lx + dx, 201, lz + dz)] = _stairs('stone_brick', names[k], 'top')           # drooping petals
        g[(lx + dx, 203, lz + dz)] = _stairs('stone_brick', names[k], 'bottom')        # the upturned cup
        g[(lx + dx, 204, lz + dz)] = _bars(k in ('n', 's'))                            # the windows
        g[(lx + dx, 205, lz + dz)] = _stairs('deepslate_tile', inward[k], 'bottom')    # the roof
    for dx, dz in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        g[(lx + dx, 201, lz + dz)] = _p('polished_andesite')
        g[(lx + dx, 204, lz + dz)] = _p('polished_andesite')
        g[(lx + dx, 205, lz + dz)] = _p('deepslate_tile_slab[type=bottom,waterlogged=false]')
    g[(lx, 201, lz)] = _p('chiseled_stone_bricks')
    g[(lx, 202, lz)] = _wall('andesite')
    g[(lx, 203, lz)] = _p('polished_andesite')
    g[(lx, 204, lz)] = ('fire',)
    g[(lx, 205, lz)] = _p('deepslate_tiles')
    g[(lx, 206, lz)] = _wall('andesite')


# the old pine: rooted on a boulder at 322 deg / r 38, the trunk leaning in steps toward the moon over the water
PINE_BASE = polar_point(38.0, 322.0)
PINE_AIM = polar_point(33.0, 345.0)
PINE_H = 13                      # trunk cells above the boulder (y 203..215)


def _pine_dir():
    ux, uz = PINE_AIM[0] - PINE_BASE[0], PINE_AIM[2] - PINE_BASE[2]
    n = math.hypot(ux, uz)
    return ux / n, uz / n


def pine_trunk():
    """[(x, y, z)] trunk cells (connected) from the boulder top up"""
    ux, uz = _pine_dir()
    cells = []
    prev = None
    for t in range(PINE_H):
        s = 0.85 * t * (0.6 + 0.4 * t / PINE_H)
        c = (math.floor(PINE_BASE[0] + ux * s), 203 + t, math.floor(PINE_BASE[2] + uz * s))
        if prev and (c[0], c[2]) != (prev[0], prev[2]):
            cells.append((c[0], prev[1], c[2]))         # a horizontal step at the old height: the trunk stays connected
        cells.append(c)
        prev = c
    return cells


def _pine(g):
    bx, bz = math.floor(PINE_BASE[0]), math.floor(PINE_BASE[2])
    for dz in range(-3, 4):
        for dx in range(-3, 4):
            r = math.hypot(dx, dz)
            for y in range(201, 203):
                lim = 2.6 if y == 201 else 1.8
                if r <= lim and _mix(bx + dx, y, bz + dz, 71) > 0.08:
                    v = _mix(bx + dx, y, bz + dz, 73)
                    _put(g, bx + dx, y, bz + dz, _p('tuff' if v < 0.5 else 'mossy_cobblestone' if v < 0.8 else 'andesite'),
                         force=True)
    trunk = pine_trunk()
    for i, (x, y, z) in enumerate(trunk):
        nxt = trunk[i + 1] if i + 1 < len(trunk) else None
        axis = 'y'
        if nxt and nxt[1] == y:
            axis = 'x' if nxt[0] != x else 'z'
        g[(x, y, z)] = _p(f'spruce_log[axis={axis}]')
    ux, uz = _pine_dir()
    tx, ty, tz = trunk[-1]
    # (centre along the lean from the trunk top / a side, y, half length along u, half width, kind)
    crowns = ((3.5, 0.0, 215, 6.0, 3.6), (3.0, 0.0, 214, 4.2, 2.6), (1.5, -2.4, 211, 3.4, 2.2), (-2.0, 1.5, 209, 2.6, 1.8))
    for along, side, y, hl, hw in crowns:
        cx, cz = tx + 0.5 + ux * along - uz * side, tz + 0.5 + uz * along + ux * side
        for dz in range(-8, 9):
            for dx in range(-8, 9):
                px, pz = math.floor(cx) + dx, math.floor(cz) + dz
                rx, rz = px + 0.5 - cx, pz + 0.5 - cz
                a, w = rx * ux + rz * uz, -rx * uz + rz * ux
                e = (a / hl) ** 2 + (w / hw) ** 2
                if e <= 1.0 and _mix(px, y, pz, 75) > 0.06 + 0.3 * e:
                    _put(g, px, y, pz, _leaves('spruce' if _mix(px, y, pz, 77) < 0.6 else 'dark_oak'))
                    if e < 0.45 and _mix(px, y + 1, pz, 79) < 0.55:
                        _put(g, px, y + 1, pz, _leaves('spruce'))
        # a branch from the trunk to the crown centre
        for k in range(1, 8):
            f = k / 8
            bxp = math.floor(tx + 0.5 + (cx - tx - 0.5) * f)
            bzp = math.floor(tz + 0.5 + (cz - tz - 0.5) * f)
            if (bxp, y - 1, bzp) not in g and y - 1 > 203:
                _put(g, bxp, y - 1, bzp, _p('spruce_log[axis=x]' if abs(ux) > abs(uz) else 'spruce_log[axis=z]'))


CHERRIES = ((70.0, 34.0, 5), (110.0, 33.0, 4), (140.0, 35.0, 5), (220.0, 34.0, 5), (250.0, 33.0, 4), (290.0, 35.0, 5))


def _cherry(g, tops, b, r, h):
    x0, z0 = polar_cell(r, b)
    base = tops.get((x0, z0), FLOOR_Y) + 1
    for y in range(base, base + h):
        g[(x0, y, z0)] = LOG_Y['cherry']
    # one short branch leaning outward
    bx, bz = (1 if _mix(x0, z0, 81) < 0.5 else -1), (1 if _mix(x0, z0, 83) < 0.5 else -1)
    g[(x0 + bx, base + h - 1, z0)] = _p('cherry_log[axis=x]')
    g[(x0 + bx, base + h, z0 + bz)] = LOG_Y['cherry']
    top = base + h
    cx, cz = x0 + 0.5 + 0.6 * bx, z0 + 0.5 + 0.5 * bz
    for y in range(top - 1, top + 4):
        rad = (3.6, 3.9, 3.6, 3.0, 1.9)[y - (top - 1)]
        for dz in range(-5, 6):
            for dx in range(-5, 6):
                px, pz = x0 + dx, z0 + dz
                dd = math.hypot(px + 0.5 - cx, pz + 0.5 - cz)
                if dd <= rad and _mix(px, y, pz, 85) > 0.07 + 0.25 * (dd / rad) ** 3 and _d(px, pz) > BARRIER_R + 1.0:
                    if (px, y, pz) not in g:
                        g[(px, y, pz)] = ('crown',)
    # a few hanging tips below the crown
    for dz in range(-4, 5):
        for dx in range(-4, 5):
            px, pz = x0 + dx, z0 + dz
            dd = math.hypot(px + 0.5 - cx, pz + 0.5 - cz)
            if 2.0 < dd <= 3.4 and _mix(px, pz, 87) < 0.22 and (px, top - 2, pz) not in g and _d(px, pz) > BARRIER_R + 1.0:
                g[(px, top - 2, pz)] = ('crown',)


BAMBOO = ((88.0, 101.0, 30.5, 37.0), (121.0, 132.0, 30.0, 36.0), (228.0, 241.0, 30.5, 37.0), (262.0, 279.0, 30.0, 36.5))


def _bamboo_groves(g, tops):
    for b0, b1, r0, r1 in BAMBOO:
        for z in range(BOX['z0'], BOX['z1'] + 1):
            for x in range(BOX['x0'], BOX['x1'] + 1):
                d, br = _d(x, z), _bearing(x, z)
                if not (r0 <= d <= r1 and b0 <= br <= b1) or (x, z) not in tops:
                    continue
                if _mix(x, z, 91) > 0.34:
                    continue
                top = tops[(x, z)]
                h = 6 + int(_mix(x, z, 93) * 7)
                col = [(x, y, z) for y in range(top + 1, top + 1 + h)]
                if any(c in g for c in col) or any((x, y, z) in g for y in range(top + 1 + h, top + 4 + h)):
                    continue
                g[(x, top, z)] = _p('podzol' if _mix(x, z, 95) < 0.5 else 'moss_block')
                age = 1 if h >= 9 else 0
                for i, c in enumerate(col):
                    left = h - 1 - i
                    leaves = 'large' if left <= 1 else 'small' if left == 2 else 'none'
                    g[c] = _bamboo(leaves, age)


# beyond: (kind, bearing, r, height); none inside the moon's +-25 deg sector (bearings -13..37)
TREES = (('dark_oak', 63.0, 42.0, 9), ('spruce', 81.0, 43.0, 11), ('spruce', 158.0, 43.0, 10), ('dark_oak', 171.0, 41.5, 8),
         ('spruce', 198.0, 42.5, 11), ('dark_oak', 236.0, 42.0, 9), ('spruce', 268.0, 43.0, 12), ('dark_oak', 306.0, 42.5, 8))
OUTCROPS = ((47.0, 40.5, 2.6, 4), (100.0, 40.0, 3.0, 5), (148.0, 40.5, 2.4, 4), (207.0, 41.5, 3.0, 5), (246.0, 39.5, 2.0, 3),
            (282.0, 40.5, 3.0, 6), (340.0, 42.5, 2.0, 3), (352.0, 39.5, 1.6, 2))


def _tree_spruce(g, x, z, base_y, h, seed):
    for y in range(base_y, base_y + h):
        _put(g, x, y, z, LOG_Y['spruce'], force=True)
    top = base_y + h
    for y in range(base_y + 3, top + 2):
        k = (top + 1 - y)
        rad = min(3.2, 0.6 + k * 0.42) if (y - base_y) % 2 == 0 else min(2.4, 0.3 + k * 0.32)
        for dz in range(-4, 5):
            for dx in range(-4, 5):
                if (dx or dz) and math.hypot(dx, dz) <= rad and _mix(x + dx, y, z + dz, seed) > 0.08:
                    _put(g, x + dx, y, z + dz, _leaves('spruce'))
    _put(g, x, top, z, _leaves('spruce'))
    _put(g, x, top + 1, z, _leaves('spruce'))


def _tree_dark(g, x, z, base_y, h, seed):
    for y in range(base_y, base_y + h):
        for dx in (0, 1):
            for dz in (0, 1):
                _put(g, x + dx, y, z + dz, LOG_Y['dark_oak'], force=True)
    for y in range(base_y + h - 2, base_y + h + 2):
        rad = 3.6 if y < base_y + h + 1 else 2.4
        for dz in range(-4, 6):
            for dx in range(-4, 6):
                dd = math.hypot(dx - 0.5, dz - 0.5)
                if dd <= rad and _mix(x + dx, y, z + dz, seed) > 0.1:
                    _put(g, x + dx, y, z + dz, _leaves('dark_oak'))


def _rock(x, y, z):
    v = _mix(x, y, z, 97)
    return _p('tuff' if v < 0.4 else 'deepslate' if v < 0.65 else 'cobbled_deepslate' if v < 0.85 else 'andesite')


def _outcrop(g, tops, b, r, rad, h):
    cx, _, cz = polar_point(r, b)
    for dz in range(-4, 5):
        for dx in range(-4, 5):
            x, z = math.floor(cx) + dx, math.floor(cz) + dz
            if (x, z) not in tops:
                continue
            dd = math.hypot(x + 0.5 - cx, z + 0.5 - cz)
            if dd > rad:
                continue
            hh = int(round(h * (1 - (dd / rad) ** 2) * (0.75 + 0.5 * _mix(x, z, 99))))
            for y in range(tops[(x, z)] + 1, tops[(x, z)] + 1 + hh):
                _put(g, x, y, z, _rock(x, y, z), force=True)


# ---------------------------------------------------------------------------------------------------------------
# the dome and the moon

def _dome_in(x, y, z):
    """interior cell of the dome (y DOME_Y0 + 1 .. DOME_TOP)"""
    if not (DOME_Y0 < y <= DOME_TOP):
        return False
    h = (y + 0.5 - DOME_Y0) / (DOME_TOP + 1 - DOME_Y0)
    return (_d(x, z) / DOME_R) ** DOME_P + h ** DOME_P <= 1.0


def _elev(x, y, z):
    return math.degrees(math.atan2(y + 0.5 - EYE, _d(x, z)))


def _sky(x, y, z):
    """the sky band key of a dome shell cell: 'hor' / 'body' / 'zen' / 'far' (ridge) or a plain block (black
    terracotta: the near ridges and the zenith dither, the same in every look)"""
    br, el = _bearing(x, z), _elev(x, y, z)
    # the painted band on the base: near ridges, far ridges, mist
    near = 202.5 + 3.2 * _fbm(br / 4.0, 0.0, 1.0, 101) + 1.2 * _vnoise(br / 1.3, 0.0, 1.0, 103)
    far = near + 1.5 + 4.5 * _fbm(br / 6.5, 3.0, 1.0, 107) ** 1.4
    if y <= near:
        return _p('black_terracotta')
    if y <= far:
        return 'far'
    if el <= 6.0:
        return 'hor'
    if el <= 60.0:
        if el > 52.0 and _mix(x, y, z, 109) < (el - 52.0) / 16.0:
            return 'zen'
        return 'body'
    return _p('black_terracotta') if _mix(x, y, z, 113) < 0.35 else 'zen'


SKY = {'hor': ('light_blue_terracotta', 'crimson_planks', 'black_concrete'),
       'body': ('blue_terracotta', 'purple_terracotta', 'black_concrete'),
       'zen': ('blue_terracotta', 'blue_terracotta', 'black_concrete'),
       'far': ('gray_terracotta', 'gray_terracotta', 'black_concrete')}
MOON = {'face': ('white_concrete', 'pink_concrete', 'black_concrete'),
        'maria': ('light_gray_concrete', 'red_terracotta', 'black_concrete'),
        'high': ('snow_block', 'pink_concrete', 'black_concrete'),
        'rim': ('pearlescent_froglight[axis=y]', 'pearlescent_froglight[axis=y]', 'black_concrete')}


def moon_cells():
    """{(x, y, z): part} of the moon plate (z MOON_Z, centre MOON_POS, r MOON_R)"""
    out = {}
    mx, my = MOON_POS[0], MOON_POS[1]
    for y in range(int(my - MOON_R) - 1, int(my + MOON_R) + 2):
        for x in range(int(mx - MOON_R) - 1, int(mx + MOON_R) + 2):
            u, v = x + 0.5 - mx, y + 0.5 - my
            rr = math.hypot(u, v)
            if rr > MOON_R:
                continue
            if rr > MOON_R - 1.0:
                part = 'rim'
            elif rr < 3.7 and _fbm(x * 1.0, y * 1.0, 2.6, 117) > 0.58:
                part = 'maria'
            elif u > 0.6 and v > 0.6 and rr > 1.8 and _mix(x, y, 119) < 0.7:
                part = 'high'
            else:
                part = 'face'
            out[(x, y, MOON_Z)] = part
    return out


def _dome(g):
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
# light: the walk grid, the flood, spawn cells, hidden lights

def foot_grid(walk, blocked=()):
    """the foot-level light cells (y 201) on the walk: the L1 radius-3 lattice x + 7 z = 0 (mod 25) inside the walk,
    then greedy extra cells for the walk cells no lattice cell reaches within L1 3 (the edge)"""
    ws = set(walk)
    grid = {c for c in walk if (c[0] + 7 * c[1]) % 25 == 0 and c not in blocked}

    def covered(c):
        return any((c[0] + dx, c[1] + dz) in grid for dx in range(-3, 4) for dz in range(-3 + abs(dx), 4 - abs(dx)))
    todo = sorted(c for c in walk if not covered(c))
    while todo:
        c = todo[0]
        best = None
        for dx in range(-3, 4):
            for dz in range(-3 + abs(dx), 4 - abs(dx)):
                q = (c[0] + dx, c[1] + dz)
                if q not in ws or q in blocked:
                    continue
                gain = sum(1 for t in todo if abs(t[0] - q[0]) + abs(t[1] - q[1]) <= 3)
                k = (-gain, _d(*q), q)
                if best is None or k < best:
                    best = k
        grid.add(best[2])
        todo = [t for t in todo if not covered(t)]
    return grid


class _Grid:
    """dense flat index over the box with a 1-cell opaque margin (no light leaks in, indices never wrap)"""

    def __init__(self):
        self.x0, self.y0, self.z0 = BOX['x0'] - 1, BOX['y0'] - 1, BOX['z0'] - 1
        self.nx, self.ny, self.nz = BOX['x1'] - BOX['x0'] + 3, BOX['y1'] - BOX['y0'] + 3, BOX['z1'] - BOX['z0'] + 3
        self.N = self.nx * self.ny * self.nz
        self.offs = (self.ny * self.nz, -self.ny * self.nz, self.nz, -self.nz, 1, -1)

    def idx(self, x, y, z):
        return ((x - self.x0) * self.ny + (y - self.y0)) * self.nz + (z - self.z0)

    def classes(self, cells):
        """(opaque, damp) bytearrays"""
        opq = bytearray(self.N)
        dmp = bytearray(self.N)
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
            elif _damp(b):
                dmp[self.idx(x, y, z)] = 1
        return opq, dmp

    def flood(self, opq, dmp, lv, seeds):
        buckets = [[] for _ in range(16)]
        for i in seeds:
            buckets[lv[i]].append(i)
        N, offs = self.N, self.offs
        for L in range(15, 1, -1):
            for i in buckets[L]:
                if lv[i] != L:
                    continue
                for o in offs:
                    j = i + o
                    if 0 <= j < N and not opq[j]:
                        nl = L - 1 - dmp[j]
                        if nl > lv[j]:
                            lv[j] = nl
                            buckets[nl].append(j)

    def light(self, cells):
        opq, dmp = self.classes(cells)
        lv = bytearray(self.N)
        seeds = []
        for (x, y, z), b in cells.items():
            e = _emits(b)
            if e:
                i = self.idx(x, y, z)
                lv[i] = max(lv[i], e)
                seeds.append(i)
        self.flood(opq, dmp, lv, seeds)
        return opq, dmp, lv


def _free(cells, c):
    b = cells.get(c)
    return b is None or _bid(b) in _FREE


def spawn_cells(cells):
    """feet cells a hostile mob could spawn in: an opaque floor block below, two free cells (inside the box)"""
    out = []
    for (x, y, z), b in cells.items():
        if not _opaque(b) or y + 2 > BOX['y1']:
            continue
        if _free(cells, (x, y + 1, z)) and _free(cells, (x, y + 2, z)):
            out.append((x, y + 1, z))
    return sorted(out, key=lambda c: (c[1], c[2], c[0]))


def walk_cell(c):
    return c[1] == FLOOR_Y + 1 and _d(c[0], c[2]) <= WALK


def _protected(c):
    """cells a hidden light may not take: the walk column below y 226 and the barrier ring"""
    return _d(c[0], c[2]) <= BARRIER_R + 0.5 and CLEAR_Y[0] <= c[1] <= CLEAR_Y[1] + 1


def _hidden_lights(looks):
    """light[level=HIDDEN_LV] cells, the same in every look, so every spawn cell outside the walk has block light >=
    SPAWN_MIN in every look (the walk cells are the foot grid's: asserted, never patched here); greedy, deterministic:
    the light goes into the dark cell or the first air cell above / beside it"""
    G = _Grid()
    added = []
    states = []
    for lk, cells in looks.items():
        opq, dmp, lv = G.light(cells)
        states.append((lk, cells, opq, dmp, lv))
    for lk, cells, opq, dmp, lv in states:
        for c in spawn_cells(cells):
            if walk_cell(c):
                assert lv[G.idx(*c)] >= FLOOR_MIN[lk], f'{lk}: dark walk cell {c} ({lv[G.idx(*c)]})'
                continue
            if lv[G.idx(*c)] >= SPAWN_MIN:
                continue
            x, y, z = c
            spot = None
            for q in ((x, y, z), (x, y + 1, z), (x, y + 2, z), (x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)):
                if q not in cells and _in_box(*q) and not _protected(q):
                    spot = q
                    break
            assert spot, f'no spot for a hidden light at {c}'
            added.append(spot)
            for _lk, cs, opq2, dmp2, lv2 in states:
                cs[spot] = LIGHT_HID
                i = G.idx(*spot)
                if lv2[i] < HIDDEN_LV:
                    lv2[i] = HIDDEN_LV
                    G.flood(opq2, dmp2, lv2, [i])
    return added


# ---------------------------------------------------------------------------------------------------------------
# the layout

_CACHE = {}
GRASS_SUPPORT = ('mycelium', 'moss_block', 'coarse_dirt', 'podzol')   # dry grass (moon) and crimson roots: valid on all
SEAT_CLEAR = 1.8                 # no grass / grid light within this of the seat point (the seat rock prop stands there)
LOTUS_TARGETS = ((316.0, 29.6), (330.0, 31.4), (343.0, 29.3), (356.0, 31.8), (8.0, 29.4), (40.0, 30.0), (47.0, 32.6),
                 (22.0, 28.8))


def _base():
    """{cell: block or a look marker}: ('floor', id) / ('grass', id) / ('sky', key) / ('moon', part) / ('crown',) /
    ('fire',) / ('lay',) / ('grid',) / ('decor',) / ('skin',); resolved per look by _resolve"""
    g = {}
    tops = {}
    walk = _walk_cells()
    ring = _ring_cells()
    pal = _floor_palette(walk, 31)
    pal.update(_floor_palette(ring, 37))
    # ground columns
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            d = _d(x, z)
            if d > DOME_R + 0.5:
                continue
            if d <= BARRIER_R:
                for y in range(DOME_Y0, FLOOR_Y):
                    g[(x, y, z)] = _p('dirt') if y >= FLOOR_Y - 2 else _p('stone')
                blk = pal[(x, z)]
                g[(x, FLOOR_Y, z)] = ('floor', blk) if blk in ('mycelium', 'pale_moss_block') else _p(blk)
                continue
            pk = _pond_kind(x, z)
            if pk:
                for y in range(DOME_Y0, FLOOR_Y - 1):
                    g[(x, y, z)] = _p('clay') if y >= FLOOR_Y - 3 else _p('stone')
                if pk == 'water':
                    g[(x, FLOOR_Y - 1, z)] = _p('mud')
                    g[(x, FLOOR_Y, z)] = WATER
                elif pk == 'rim':
                    g[(x, FLOOR_Y - 1, z)] = _p('mud')
                    g[(x, FLOOR_Y, z)] = _p('packed_mud' if _mix(x, z, 121) < 0.6 else 'mud_bricks')
                else:
                    g[(x, FLOOR_Y - 1, z)] = _p('stone')
                    v = _mix(x, z, 123)
                    g[(x, FLOOR_Y, z)] = _p('tuff' if v < 0.45 else 'mossy_cobblestone' if v < 0.75 else 'moss_block')
                continue
            top = ground_top(x, z)
            if top is None:
                continue
            tops[(x, z)] = top
            for y in range(DOME_Y0, top):
                g[(x, y, z)] = _p('dirt') if y >= top - 2 else _p('stone')
            tb = _outer_top_block(x, z, top)
            g[(x, top, z)] = ('floor', tb) if tb == 'mycelium' else _p(tb)
    g[SENTINEL[0]] = SENTINEL[1]
    # water: every water cell has water / solid horizontal neighbours (no flow)
    changed = True
    while changed:
        changed = False
        for (x, y, z), b in list(g.items()):
            if b != WATER:
                continue
            for q in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)):
                nb = g.get(q)
                if nb is None or (isinstance(nb, str) and _bid(nb) in _FREE) or isinstance(nb, tuple) and nb[0] == 'grass':
                    g[(x, y, z)] = _p('packed_mud')
                    changed = True
                    break
    # the north: islet lantern, pine; walls and lanterns; trees, bamboo, outcrops
    _stone_lantern(g)
    _pine(g)
    _walls(g)
    for b, r, h in CHERRIES:
        _cherry(g, tops, b, r, h)
    for kind, b, r, h in TREES:
        x, z = polar_cell(r, b)
        if (x, z) not in tops:
            continue
        (_tree_spruce if kind == 'spruce' else _tree_dark)(g, x, z, tops[(x, z)] + 1, h, 131 + int(b))
    for b, r, rad, h in OUTCROPS:
        _outcrop(g, tops, b, r, rad, h)
    _bamboo_groves(g, tops)
    # boulders on the far bank (mossy tuff, 1-2 b)
    for (x, z), top in tops.items():
        if abs(_angdiff(_bearing(x, z), 0.0)) < POND_HALF and pond_outer(_bearing(x, z)) + 0.5 < _d(x, z) < 41.0:
            v = _vnoise(x, z, 2.2, 133)
            if v > 0.72 and (x, top + 1, z) not in g:
                h = 1 + (v > 0.82)
                for y in range(top + 1, top + 1 + h):
                    g[(x, y, z)] = _p('tuff' if _mix(x, y, z, 135) < 0.55 else 'mossy_cobblestone')
                if _mix(x, z, 137) < 0.6:
                    g[(x, top + h, z)] = _p('moss_block')
    # lily pads and dripleaf leaves on the pond, away from the lotus points
    lotus = lotus_cells()
    assert all(g.get((x + dx, FLOOR_Y, z + dz)) == WATER for x, z in lotus for dx in (-1, 0, 1) for dz in (-1, 0, 1))
    keep = {(x + dx, z + dz) for x, z in lotus for dx in (-1, 0, 1) for dz in (-1, 0, 1)}
    for (x, y, z), b in list(g.items()):
        if b != WATER or (x, z) in keep:
            continue
        v = _mix(x, z, 139)
        if v < 0.09 and (x, y + 1, z) not in g:
            g[(x, y + 1, z)] = _p('lily_pad')
        elif v > 0.95:
            f = ('north', 'east', 'south', 'west')[int(_mix(x, z, 141) * 4) % 4]
            g[(x, y, z)] = _p(f'big_dripleaf[facing={f},tilt=none,waterlogged=true]')
    # dry grass on the outer field and the bank (free tops only)
    for (x, z), top in tops.items():
        c = (x, top + 1, z)
        if c in g:
            continue
        tb = g.get((x, top, z))
        tid = tb[1] if isinstance(tb, tuple) else _bid(tb) if tb else None
        if tid not in ('mycelium', 'moss_block', 'coarse_dirt', 'podzol'):
            continue
        v = _mix(x, z, 143)
        if v < 0.18:
            g[c] = ('grass', 'short_dry_grass')
        elif v < 0.25:
            g[c] = ('grass', 'tall_dry_grass')
    # the barrier ring
    for (x, z) in ring:
        for y in range(BARRIER_Y[0], BARRIER_Y[1] + 1):
            g[(x, y, z)] = BARRIER
    # the walk: light layer, foot grid, grass
    for (x, z) in walk:
        g[(x, LIGHT_Y, z)] = ('lay',)
    seat = {(x, z) for (x, z) in walk if math.hypot(x + 0.5 - SEAT_POS[0], z + 0.5 - SEAT_POS[2]) <= SEAT_CLEAR}
    grid = foot_grid(walk, blocked=seat)
    for (x, z) in grid:
        g[(x, FLOOR_Y + 1, z)] = ('grid',)
    myc = [c for c in walk if pal[c] == 'mycelium' and c not in grid and c not in seat]
    ranked = sorted(myc, key=lambda c: (-(_vnoise(c[0], c[1], 2.8, 151) + 0.35 * _mix(c[0], c[1], 153)), c))
    n_myc = sum(1 for c in walk if pal[c] == 'mycelium')
    n_tall, n_short = int(round(0.12 * n_myc)), int(round(0.25 * n_myc))
    for i, (x, z) in enumerate(ranked[:n_tall + n_short]):
        g[(x, FLOOR_Y + 1, z)] = ('grass', 'tall_dry_grass' if i < n_tall else 'short_dry_grass')
    # the moon plate
    for c, part in moon_cells().items():
        g[c] = ('moon', part)
    # the dome: shell blocks where nothing else stands, the inner skin light stripes, the outer roof lights
    interior, shell = _dome(g)
    for c in list(g):
        if c[1] > DOME_Y0 and c not in interior and c not in shell:
            del g[c]                                  # nothing pokes out of the dome
    for c in shell:
        v = g.get(c)
        if v is not None and (isinstance(v, tuple) or not _opaque(v)):
            del g[c]                                  # leaves / plants / lights in the shell would let the sky in
        if c in g or not _in_box(*c):
            continue
        x, y, z = c
        if y <= DOME_Y0:
            continue
        s = _sky(x, y, z)
        g[c] = ('sky', s) if s in SKY else s
    for (x, y, z) in interior:
        if (x, y, z) in g:
            continue
        roof = (x, y + 1, z) in shell
        side = any(p in shell for p in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)))
        if not (roof or side) or (x % 4 if roof else y % 4) or _protected((x, y, z)):
            continue
        if any((p in shell and p in g) for p in ((x, y + 1, z), (x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1))):
            g[(x, y, z)] = ('skin',)
    _roof_lights(g, interior, shell)
    for (x, y, z), v in list(g.items()):
        if isinstance(v, tuple) and v[0] == 'grass':
            below = g.get((x, y - 1, z))
            bid = below[1] if isinstance(below, tuple) and below[0] == 'floor' else _bid(below) if isinstance(below, str) else None
            if bid not in GRASS_SUPPORT:
                del g[(x, y, z)]
    # decor lights over the outer field (not the walk column): the L1-3 lattice at y 204 where it is air
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            d = _d(x, z)
            if not (BARRIER_R + 1.5 < d <= 44.0) or (x + 7 * z) % 25:
                continue
            c = (x, 204, z)
            if c not in g and (x, 203, z) not in g and _dome_in(*c) and (tops.get((x, z), FLOOR_Y) < 203):
                g[c] = ('decor',)
    return g, tops


def lotus_cells():
    """the 8 lotus cells: for each target (bearing, r) the nearest pond water cell whose 3 x 3 neighbourhood is water
    (no lily pad or leaf is put there)"""
    out = []
    for b, r in LOTUS_TARGETS:
        tx, _, tz = polar_point(r, b)
        best = None
        for z in range(math.floor(tz) - 4, math.floor(tz) + 5):
            for x in range(math.floor(tx) - 4, math.floor(tx) + 5):
                if all(_pond_kind(x + dx, z + dz) == 'water' for dx in (-1, 0, 1) for dz in (-1, 0, 1)) \
                        and (x, z) not in out:
                    k = (math.hypot(x + 0.5 - tx, z + 0.5 - tz), x, z)
                    if best is None or k < best:
                        best = k
        assert best, f'no water for the lotus at {b}/{r}'
        out.append((best[1], best[2]))
    return out


def _roof_lights(g, interior, shell):
    """light[level=15] on the outside of the dome, one per 6 x 6 columns on that column's exposed top (outside the
    dome: not decor, the same in every look)"""
    for (x, y, z) in shell:
        q = (x, y + 1, z)
        if q not in shell and q not in interior and _in_box(*q) and q not in g and x % 6 == 0 and z % 6 == 0:
            g[q] = _light(15)


def _resolve(base, look):
    k = LOOKS.index(look)
    lit = DARK_LIGHT or look != 'dark'
    out = {}
    for c, v in base.items():
        if not isinstance(v, tuple):
            out[c] = v
            continue
        kind = v[0]
        if kind == 'floor':
            out[c] = _p(v[1] if look == 'moon' else {'mycelium': 'crimson_nylium', 'pale_moss_block': 'nether_wart_block'}
                        .get(v[1], v[1]))
        elif kind == 'grass':
            out[c] = _p(v[1] if look == 'moon' else 'crimson_roots')
        elif kind == 'sky':
            out[c] = _p(SKY[v[1]][k])
        elif kind == 'moon':
            out[c] = _p(MOON[v[1]][k])
        elif kind == 'crown':
            out[c] = _leaves('cherry') if look == 'moon' else _p('nether_wart_block')
        elif kind == 'fire':
            out[c] = _p('black_concrete') if look == 'dark' else _p('ochre_froglight[axis=y]')
        elif kind in LV:
            out[c] = _light(LV[kind][k if lit else 0])
        else:
            raise ValueError(v)
    return out


def _build():
    if 'all' not in _CACHE:
        base, tops = _base()
        lays = {lk: _resolve(base, lk) for lk in LOOKS}
        hidden = _hidden_lights(lays)
        _CACHE['all'] = (lays, hidden, base, tops)
    return _CACHE['all']


def arena_layout(look=None):
    """{(x, y, z): block} of every non-air block of the box in `look` (None = 'moon')."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    return dict(_build()[0][look])


def hidden_lights():
    return list(_build()[1])


def base_markers():
    """{cell: marker tuple} of the look-variant cells (renders, tests)"""
    return {c: v for c, v in _build()[2].items() if isinstance(v, tuple)}


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
    """{cell: {look: block or None}} of every cell some look changes (the union of the differences)"""
    lays = {lk: arena_layout(lk) for lk in LOOKS}
    cells = set()
    for a in LOOKS:
        for b in LOOKS:
            if a < b:
                cells |= {c for c in set(lays[a]) | set(lays[b]) if lays[a].get(c) != lays[b].get(c)}
    return {c: {lk: lays[lk].get(c) for lk in LOOKS} for c in sorted(cells)}


def _group_of(c, kind):
    """the job slice of a changed cell: 0 the far (north) dome + the moon, 1 the near (south) dome, 2 the outer field /
    crowns / lanterns / decor lights, 3 the walk and its ring (floor, grass, foot grid, light layer). A plant and its
    support (the cell below) always share the group (the walk / ring: 3, the outer field: 2)."""
    x, y, z = c
    if _d(x, z) <= BARRIER_R and FLOOR_Y <= y <= LIGHT_Y:
        return 3
    if kind == 'moon' or (kind in ('sky', 'skin') and z < CZ):
        return 0
    if kind in ('sky', 'skin'):
        return 1
    return 2


def merge_boxes(cells):
    """[(x0, y0, z0, x1, y1, z1, block)] covering exactly {cell: block} with boxes of one block (greedy: the larger of
    a column-first and a row-first growth from the lowest free cell; <= MAX_FILL blocks each)"""
    by = {}
    for c, b in cells.items():
        by.setdefault(b, set()).add(c)
    out = []
    for blk in sorted(by):
        left = by[blk]
        for c in sorted(left, key=lambda c: (c[1], c[2], c[0])):
            if c not in left:
                continue
            best = None
            for order in ('yxz', 'xzy'):
                x0, y0, z0 = c
                x1, y1, z1 = c
                for ax in order:
                    while True:
                        if ax == 'x':
                            nxt = [(x1 + 1, y, z) for y in range(y0, y1 + 1) for z in range(z0, z1 + 1)]
                        elif ax == 'y':
                            nxt = [(x, y1 + 1, z) for x in range(x0, x1 + 1) for z in range(z0, z1 + 1)]
                        else:
                            nxt = [(x, y, z1 + 1) for x in range(x0, x1 + 1) for y in range(y0, y1 + 1)]
                        vol = (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)
                        if vol + len(nxt) > MAX_FILL or not all(q in left for q in nxt):
                            break
                        if ax == 'x':
                            x1 += 1
                        elif ax == 'y':
                            y1 += 1
                        else:
                            z1 += 1
                v = (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)
                if best is None or v > best[0]:
                    best = (v, x0, y0, z0, x1, y1, z1)
            _v, x0, y0, z0, x1, y1, z1 = best
            for x in range(x0, x1 + 1):
                for y in range(y0, y1 + 1):
                    for z in range(z0, z1 + 1):
                        left.discard((x, y, z))
            out.append((x0, y0, z0, x1, y1, z1, blk))
    return out


def _cmds(boxes):
    out = []
    for x0, y0, z0, x1, y1, z1, b in sorted(boxes, key=lambda t: (t[1], t[2], t[0], t[6])):
        if (x0, y0, z0) == (x1, y1, z1):
            out.append(f'setblock {x0} {y0} {z0} {b} strict')
        else:
            out.append(f'fill {x0} {y0} {z0} {x1} {y1} {z1} {b} strict')
    return out


def look_lines(look):
    """[[cmd]]: the job that turns any built look into `look`: absolute fills (boxes of equal blocks) of every cell any
    look changes, in its `look` state (air where `look` has none), in 4 real slices (far dome + moon, near dome, the
    outer field, the walk); `dark` with DARK_PAD empty slices after each real one but the last (its real slices land
    3 t apart: api.DARK_SLICES). Floor rows come before the plant rows in a slice (y ascending)."""
    assert look in LOOKS, look
    lc = look_cells()
    mk = _build()[2]
    groups = [{} for _ in range(4)]
    for c, per in lc.items():
        v = mk.get(c)
        groups[_group_of(c, v[0] if isinstance(v, tuple) else None)][c] = per[look] or 'minecraft:air'
    real = [_cmds(merge_boxes(gp)) for gp in groups]
    if look != 'dark':
        return real
    out = []
    for i, gp in enumerate(real):
        out.append(gp)
        if i < len(real) - 1:
            out += [[] for _ in range(DARK_PAD)]
    return out


def props(look=None):
    """No arena display props (the moon halo, the lotus flowers and the seat rock are kit props the module spawns at
    DECO)."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    return []


# ---------------------------------------------------------------------------------------------------------------
# named points (absolute world coordinates) and the decor prop points (api.deco())

# the decor prop points (api.deco(): S3 spawns the kit props there): the moon halo 1 b before the moon face, the 8 lotus
# flowers on the pond water (the cell centre at the water surface y 200.9), the seat rock at api.SEAT_POS
DECO = {'moon_halo': (MOON_POS[0], MOON_POS[1], MOON_POS[2] + 1.0),
        'lotus': tuple((x + 0.5, CY - 0.1, z + 0.5) for x, z in lotus_cells()),
        'seat_rock': SEAT_POS}

POINTS = {
    'centre': (float(CX), float(CY), float(CZ), 0.0),
    'spawn': (float(CX), float(CY), float(CZ), 0.0),            # the boss anchor (yaw 0 faces south, the arrival)
    'start': (START['x'], START['y'], START['z'], START['yaw']),
    'moon': (MOON_POS[0], MOON_POS[1], MOON_POS[2], 0.0),       # the moon disc centre on its face (facing south)
    'seat': (SEAT_POS[0], SEAT_POS[1], SEAT_POS[2], yaw_to(SEAT_POS, MOON_POS)),
    'lantern': (LANTERN_CELL[0] + 0.5, 201.0, LANTERN_CELL[1] + 0.5, 0.0),
    'pine': (PINE_BASE[0], 203.0, PINE_BASE[2], 0.0),
}


def render_hints():
    return {'top': {'centre': (CX, CZ), 'r': 48}, 'eye': START, 'boss': (CX, CY, CZ), 'moon': MOON_POS}
