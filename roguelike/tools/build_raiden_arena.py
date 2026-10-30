"""Generate the Narukami boss room: the Plane of Euthymia field, its entrance and the sliced backdrop build.

Run from any directory (no resource pack needed; the panel models come from build_raiden_backdrop.py).
Runtime hooks stay in the shared room files, so generating the arena cannot overwrite unrelated room system changes.

THE FIELD (centre (0, 201, 0), the corner between four blocks; walk radius 23, as before)
  * Water: one floor layer (y 200) of full, solid, non-slippery blocks out to the horizon (r 60). Near water
    (r < ~46) is calm light-blue powder crossed by thin darker ripple arcs, rings around the centre (horizontal
    streaks from the player's eye, whichever way they look; none at the very centre) and single twinkling
    prismarine; the lines thin out on a band toward the vortex; the far water dithers into pale wool haze, with
    sea-lantern glints on the vortex's reflection path beyond r 30 (never inside the walk area, no bright spot on
    the stage).
  * Boundary: invisible barriers on the old wall ring (r 23..24, y 201..210) and around the entrance pier.
  * Sky: a block dome (superellipse, r 60 at the water, top y 229) of concrete and wool, lit only by light blocks
    on its inner skin: a bright band at the horizon fading upward, a teal glow behind the vortex, dark teal above.
    It shuts out the overworld sky, sun and sky light; ~330 light blocks on the outside of the roof keep every
    exposed top lit (no mob spawns on the roof; checked by a light flood fill). Display panels
    (build_raiden_backdrop.py) add the stars, the horizon mist ring, the vortex (slowly turning) and its wisps:
    12 entities.
  * Light: light[level=15] at y 204 (floor light 12, above the boss's air checks at y 201-202): a full layer over
    the walk circle, every other row out to r 50; the sky skin in stripes one level up (rings on the walls, rows
    under the roof): 13 at the horizon, 7 walls / 8 top, up to 10 behind the vortex. Smooth lighting averages the
    stripes to an even level with half the blocks. The generator floods the light and asserts every floor block is
    lit (no spawns); no visible light source inside the walk area.
  * Entrance: a dark stone pier with a vermilion torii; the native door fills the torii (black, open, bars).
LOOKS: look_tenma / look_shogun swap the four near-water blocks by `replace ... strict` fills over x / z -47..46 at
y 200 (one tick, ~5.5k blocks, ~3 ms on the 26.3 server); the far haze, the glints, the pier and the sky stay.
TIMING (framework rules: forceloaded dungeon box, slices <= 32768 blocks, one per tick; here <= 4000 blocks and
<= 600 commands per slice, 20 slices, ~44k blocks; measured on the 26.3 server: ~4 ms per slice warm):
  * room/raiden/foyer (zone 1, at map generation): pier, torii, barriers, light; tags the zone marker
    rlk_rd_bgzone and starts the backdrop job.
  * room/raiden/bg/tick: one slice per tick (bg/s/<i>), aborts when the boss map is gone (no rlk_rd_bgzone
    marker) or after 200 t of unloaded chunks; the last slice summons the panels and starts bg/spin.
  * room/raiden/arena (zone 2, at the door reveal / test start): the walk square (floor, barrier ring, light) and
    the arena marker (~5 ms); restarts the backdrop job if it never ran or was aborted.
CLEANUP: zone 1 lists the foyer cell plus eleven 128 x 12 strips over the whole dungeon box (x0 -64, so the screen
minimap ignores them; entry / interior bounds empty), so the native zone erase clears the dome (~5 ms); the panels
carry rlk_room.
"""
from pathlib import Path
import json
import math
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data/rlk/function/room/raiden'
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_raiden_backdrop as BD  # noqa: E402

# ------------------------------------------------------------------------------------------------ constants
FLOOR_Y = 200
WALK_R, RING_R = 23, 24          # walk circle / outer edge of the barrier ring (block centres)
BAR_TOP = 210
LIGHT_Y = 204
OUTER_LIGHT_R = 50           # the outer water's light layer stops under the mist ring (the dome wall stays dark)
DOME_R, DOME_TOP, DOME_P = 60.0, 228, 8      # interior air y 201..228; (d/R)^8 + (h/H)^8 <= 1
FOYER = (-6, 24, 5, 39)          # zone 1 cell
PIER = (-5, 24, 4, 38)           # the stone pier inside it
DOOR = (-2, 1, 23, 24)           # x0, x1, z0, z1 of the native door
TORII_X = (-3, 2)
SWAP_BOX = (-47, 46)             # x / z range of the near-water look swap
ARENA_SQ = (-24, 23)
BOX = (-64, 63)                  # the forceloaded dungeon box
MAX_FILL = 32768
SLICE_BLOCKS = 4000              # blocks per backdrop slice (one slice per tick)
SLICE_CMDS = 600                # and commands per slice

# near water, Shogun look -> Tenma look (index-wise; the two sets are disjoint and used nowhere else at y 200)
SHOGUN = ['minecraft:light_blue_concrete_powder', 'minecraft:cyan_concrete_powder', 'minecraft:cyan_concrete',
          'minecraft:prismarine']
TENMA = ['minecraft:light_blue_concrete', 'minecraft:blue_concrete_powder', 'minecraft:blue_concrete',
         'minecraft:lapis_block']
FAR_BASE, FAR_HAZE, GLINT = 'minecraft:light_blue_wool', 'minecraft:white_wool', 'minecraft:sea_lantern'
SKY_HIGH, SKY_GLOW, SKY_TEAL, SKY_HAZE = ('minecraft:light_blue_concrete', 'minecraft:light_blue_wool',
                                          'minecraft:cyan_wool', 'minecraft:white_wool')
BARRIER, AIR = 'minecraft:barrier', 'minecraft:air'
PIER_EDGE, PIER_IN, PIER_PATH = 'minecraft:polished_deepslate', 'minecraft:dark_prismarine', 'minecraft:deepslate_tiles'
TORII_RED, TORII_TOP = 'minecraft:red_concrete', 'minecraft:black_concrete'


def light(n):
    return f'minecraft:light[level={n}]'


def d2(x, z):
    return (x + 0.5) ** 2 + (z + 0.5) ** 2


def walk(x, z):
    return d2(x, z) <= WALK_R ** 2


def ring(x, z):
    return WALK_R ** 2 < d2(x, z) <= RING_R ** 2


def in_rect(x, z, r):
    return r[0] <= x <= r[2] and r[1] <= z <= r[3]


def in_dome(x, y, z):
    if not (FLOOR_Y + 1 <= y <= DOME_TOP):
        return False
    h = (y + 0.5 - (FLOOR_Y + 1)) / (DOME_TOP + 1 - (FLOOR_Y + 1))
    return (math.sqrt(d2(x, z)) / DOME_R) ** DOME_P + h ** DOME_P <= 1.0


def door_cell(x, z):
    return DOOR[0] <= x <= DOOR[1] and DOOR[2] <= z <= DOOR[3]


# ------------------------------------------------------------------------------------------------ the water
def _smooth(e0, e1, v):
    t = max(0.0, min(1.0, (v - e0) / (e1 - e0)))
    return t * t * (3 - 2 * t)


def water(x, z):
    """Floor block (Shogun look) at column (x, z): calm base water crossed by thin wavy ripple lines that run
    east-west (horizontal streaks from the player's eye), a brighter glinting band toward the vortex, pale haze far
    out."""
    d = math.sqrt(d2(x, z))
    h = BD._hash(x, z, 211)
    # the vortex's reflection band (north), widening with distance
    band = 0.0
    if z < -1:
        width = 1.6 + 0.10 * (-z)
        band = max(0.0, 1.0 - abs(x + 0.5) / width) * _smooth(-1.0, -9.0, z)
    if band > 0.15 and d >= 30 and h < 0.05 + 0.25 * band:
        return GLINT                              # sea-lantern glints on the vortex's reflection path
    if BD._hash(x, z, 223) < _smooth(37.0, 48.0, d):           # far water: pale haze
        return FAR_HAZE if BD._hash(x, z, 227) < _smooth(48.0, 58.0, d) * 0.75 else FAR_BASE
    # ripple lines: rings around the centre (so they cross the view as horizontal streaks from anywhere on the
    # stage) whose phase wanders with the angle, broken into arcs by noise along the ring
    ang = math.atan2(z + 0.5, x + 0.5)
    phase = d * 1.05 + 4.0 * BD.fbm(math.cos(ang) * 3.0 + 7.0, math.sin(ang) * 3.0 + d * 0.03, 101, 3)
    s = math.sin(phase)
    seg = BD.fbm(ang * d * 0.16 + 3.0, d * 0.55, 103, 3)
    # fewer lines on the stage, on the bright band and none at the very centre (tight rings would close into shapes)
    calm = (0.5 if walk(x, z) else 0.42) + 0.35 * band + 0.6 * _smooth(11.0, 5.0, d)
    if BD._hash(x, z, 107) < 0.022:
        return SHOGUN[3]                          # prismarine twinkles (animated texture), single blocks
    if s < -0.93 and seg > calm:
        return SHOGUN[2] if (seg > calm + 0.18 and d > 12) else SHOGUN[1]
    if s < -0.6 and seg > calm + 0.1:
        return SHOGUN[1]
    return SHOGUN[0]


# ------------------------------------------------------------------------------------------------ voxel sets
def dome_cells():
    """interior air, the shell (sky blocks) and the glass cap."""
    lo, hi = -62, 61
    interior = set()
    for x in range(lo, hi + 1):
        for z in range(lo, hi + 1):
            if d2(x, z) > (DOME_R + 1) ** 2:
                continue
            for y in range(FLOOR_Y + 1, DOME_TOP + 1):
                if in_dome(x, y, z):
                    interior.add((x, y, z))
    shell = set()
    for (x, y, z) in interior:
        for dx, dy, dz in ((1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1), (0, 1, 0)):
            p = (x + dx, y + dy, z + dz)
            if p not in interior:
                shell.add(p)
    cap = set()
    for (x, y, z) in shell:
        p = (x, y + 1, z)
        if p not in shell and p not in interior:
            cap.add(p)
    return interior, shell, cap


def azimuth(x, z):
    """degrees from north (-z), positive toward east."""
    return math.degrees(math.atan2(x + 0.5, -(z + 0.5)))


def vortex_glow(x, y, z):
    a = azimuth(x, z)
    return math.exp(-(a / 22.0) ** 2) * math.exp(-((y - 215.0) / 7.5) ** 2)


def sky_block(x, y, z):
    g = vortex_glow(x, y, z)
    h = BD._hash(x * 7 + y, z, 301)
    neb = BD.fbm(math.radians(azimuth(x, z)) * 6.0, y * 0.18, 307, 3)
    if y <= FLOOR_Y + 2:                         # the horizon (behind the mist ring): white only under the vortex
        return SKY_HAZE if h < 0.15 + 0.8 * g else (SKY_GLOW if h < 0.7 else SKY_TEAL)
    if y <= FLOOR_Y + 7 or g > 0.35:
        return SKY_GLOW if h < 0.55 else SKY_TEAL
    if y <= FLOOR_Y + 12:
        return SKY_TEAL if h < 0.45 else SKY_HIGH
    if neb > 0.66 or g > 0.12:
        return SKY_TEAL
    return SKY_HIGH


def skin_level(x, y, z, below_roof):
    lv = 13 if y <= FLOOR_Y + 2 else (8 if below_roof else 7)
    return max(lv, int(round(10 * vortex_glow(x, y, z))))


def flood(sources, passable, lo, hi):
    """Vanilla-style block light: each source spreads level - 1 per step through passable cells (6-neighbours).
    sources {(x, y, z): level}; passable(p) -> bool; lo / hi: inclusive (x, y, z) bounds. Returns {cell: level}."""
    L = dict(sources)
    buckets = [[] for _ in range(16)]
    for p, lv in sources.items():
        buckets[lv].append(p)
    for lv in range(15, 1, -1):
        for p in buckets[lv]:
            if L.get(p) != lv:
                continue
            x, y, z = p
            for q in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
                if not (lo[0] <= q[0] <= hi[0] and lo[1] <= q[1] <= hi[1] and lo[2] <= q[2] <= hi[2]):
                    continue
                if L.get(q, 0) < lv - 1 and passable(q):
                    L[q] = lv - 1
                    buckets[lv - 1].append(q)
    return L


def roof_lights(interior, shell):
    """light[level=15] on the outside of the dome, one per 6 x 6 columns on that column's exposed top, plus any top
    the flood does not reach: every exposed top gets block light >= 1, so nothing spawns on the roof (instead of
    capping each of the ~11.6k tops with glass)."""
    tops = {}
    for (x, y, z) in shell:
        q = (x, y + 1, z)
        if q not in shell and q not in interior:
            tops[q] = max(tops.get(q, 0), 0)
    src = {p: 15 for p in tops if p[0] % 6 == 0 and p[2] % 6 == 0}

    def passable(q):
        return q not in shell and q not in interior and q[1] >= FLOOR_Y
    lo, hi = (BOX[0], FLOOR_Y, BOX[0]), (BOX[1], 231, BOX[1])
    while True:
        lit = flood(src, passable, lo, hi)
        dark = sorted(p for p in tops if lit.get(p, 0) < 1)
        if not dark:
            return src
        src[dark[0]] = 15


def backdrop_blocks():
    """Everything the sliced job places: water (but the foyer cell), the dome, its roof lights, the skin lights and
    the light layer over the water (never on the barrier ring, the door or inside the foyer cell). Light sources sit
    in stripes one level above the wanted level: every cell between two stripes gets the wanted level, and smooth
    lighting averages the faces to an even glow with half the blocks (stripes merge into long fills)."""
    interior, shell, _cap = dome_cells()
    B = {}
    for (x, y, z) in shell:
        if y == FLOOR_Y:
            continue
        B[(x, y, z)] = sky_block(x, y, z)
    for p in roof_lights(interior, shell):
        B[p] = light(15)
    # skin lights: interior cells touching the shell (not the floor), in stripes: under the roof every other x row
    # (lines along z), on the walls every other y level (rings)
    for (x, y, z) in interior:
        if in_rect(x, z, FOYER):
            continue
        roof = (x, y + 1, z) in shell
        side = any(p in shell for p in ((x + 1, y, z), (x - 1, y, z), (x, y, z + 1), (x, y, z - 1)))
        if not (roof or side) or (x % 2 if roof else y % 2):
            continue
        B[(x, y, z)] = light(min(15, skin_level(x, y, z, roof) + 1))
    # floor
    for x in range(-61, 61):
        for z in range(-61, 61):
            if (x, FLOOR_Y + 1, z) in interior or (x, FLOOR_Y + 1, z) in shell:
                if not in_rect(x, z, FOYER):
                    B[(x, FLOOR_Y, z)] = water(x, z)
    # light layer over the water: full over the walk circle, every other z row beyond it
    for x in range(-61, 61):
        for z in range(-61, 61):
            p = (x, LIGHT_Y, z)
            if p not in interior or in_rect(x, z, FOYER) or ring(x, z) or d2(x, z) > OUTER_LIGHT_R ** 2:
                continue
            if not walk(x, z) and z % 2:
                continue
            lv = 15
            cur = B.get(p)
            if cur and cur.startswith('minecraft:light['):
                lv = max(lv, int(cur.split('=')[1].rstrip(']')))
            B[p] = light(lv)
    return B


def floor_light_report(B, A, F):
    """Block light on top of every floor block inside the dome (the built field: backdrop B, arena square A, foyer
    F). Asserts >= 1 everywhere (no natural spawns); returns (min, mean) over the walk circle and the whole floor."""
    W = dict(B)
    W.update(A)
    W.update(F)
    interior, shell, _cap = dome_cells()
    src = {}
    for p, b in W.items():
        if b.startswith('minecraft:light['):
            src[p] = int(b.split('=')[1].rstrip(']'))
        elif b == GLINT:
            src[p] = 15
        elif b == 'minecraft:soul_lantern':
            src[p] = 10
    see_through = ('minecraft:light[', BARRIER, 'minecraft:soul_lantern', GLINT)

    def passable(q):
        b = W.get(q)
        return q in interior and (b is None or b.startswith(see_through))
    lit = flood(src, passable, (-62, FLOOR_Y, -62), (61, DOME_TOP, 61))
    walk_l, all_l = [], []
    for (x, y, z), b in W.items():
        if y != FLOOR_Y or (x, y + 1, z) not in interior or b == GLINT:
            continue
        top = W.get((x, y + 1, z))
        if top and not top.startswith('minecraft:light['):
            continue                                # covered (barrier ring, pier furniture)
        lv = lit.get((x, y + 1, z), 0)
        all_l.append(lv)
        if walk(x, z):
            walk_l.append(lv)
    assert min(all_l) >= 1, 'a floor block is dark (mobs could spawn)'
    return (min(walk_l), sum(walk_l) / len(walk_l), max(walk_l)), (min(all_l), sum(all_l) / len(all_l))


def arena_blocks():
    """The walk square (zone 2 cells, x / z -24..23): water, barrier ring (y 201..210), light layer."""
    B = {}
    lo, hi = ARENA_SQ
    for x in range(lo, hi + 1):
        for z in range(lo, hi + 1):
            B[(x, FLOOR_Y, z)] = water(x, z)
            if ring(x, z):
                for y in range(FLOOR_Y + 1, BAR_TOP + 1):
                    B[(x, y, z)] = BARRIER
            else:
                B[(x, LIGHT_Y, z)] = light(15)
    return B


def foyer_blocks():
    """Pier, torii, stone lanterns, barriers and light inside the foyer cell (x -6..5, z 24..39)."""
    B = {}
    x0, z0, x1, z1 = FOYER
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            if in_rect(x, z, PIER):
                edge = x in (PIER[0], PIER[2]) or z == PIER[3]
                B[(x, FLOOR_Y, z)] = PIER_EDGE if edge else (PIER_PATH if DOOR[0] <= x <= DOOR[1] else PIER_IN)
            else:
                B[(x, FLOOR_Y, z)] = water(x, z)
    # barriers: the cell's rim, except the torii line's gate (pillars are solid) and the door
    for x in range(x0, x1 + 1):
        for z in range(z0, z1 + 1):
            rim = x in (x0, x1) or z in (z0, z1)
            if not rim or (z == z0 and TORII_X[0] <= x <= TORII_X[1]):
                continue
            for y in range(FLOOR_Y + 1, BAR_TOP + 1):
                B[(x, y, z)] = BARRIER
    # light inside the pier
    for x in range(PIER[0], PIER[2] + 1):
        for z in range(PIER[1] + 1, PIER[3] + 1):
            B[(x, LIGHT_Y, z)] = light(15)
    # torii on the door line (z 24): pillars, nuki (the door lintel itself is the native th.lb), shimaki, kasagi
    for px in TORII_X:
        for y in range(FLOOR_Y + 1, 210):
            B[(px, y, z0)] = TORII_RED
    for x in range(-4, 4):
        if not (DOOR[0] <= x <= DOOR[1]):
            B[(x, 207, z0)] = TORII_RED
    for x in range(-5, 5):
        B[(x, 209, z0)] = TORII_RED
    for x in range(-6, 6):
        B[(x, 210, z0)] = TORII_TOP
    for x in (-1, 0):
        B[(x, 208, z0)] = TORII_TOP
    # stone lanterns (soul fire) on the pier edges
    for lx in (PIER[0], PIER[2]):
        B[(lx, 201, 25)] = 'minecraft:chiseled_stone_bricks'
        B[(lx, 202, 25)] = 'minecraft:soul_lantern'
    return B


# ------------------------------------------------------------------------------------------------ commands
def greedy(cells):
    """Same-block cells -> boxes (x, then z, then y), each <= MAX_FILL blocks."""
    keys = sorted(cells, key=lambda p: (p[1], p[2], p[0]))
    used = set()
    out = []
    for p in keys:
        if p in used:
            continue
        x, y, z = p
        b = cells[p]

        def ok(q):
            return q in cells and q not in used and cells[q] == b
        x1 = x
        while ok((x1 + 1, y, z)):
            x1 += 1
        z1 = z
        while all(ok((xx, y, z1 + 1)) for xx in range(x, x1 + 1)) and (x1 - x + 1) * (z1 - z + 2) <= MAX_FILL:
            z1 += 1
        y1 = y
        while (all(ok((xx, y1 + 1, zz)) for xx in range(x, x1 + 1) for zz in range(z, z1 + 1))
               and (x1 - x + 1) * (z1 - z + 1) * (y1 - y + 2) <= MAX_FILL):
            y1 += 1
        for xx in range(x, x1 + 1):
            for zz in range(z, z1 + 1):
                for yy in range(y, y1 + 1):
                    used.add((xx, yy, zz))
        out.append((x, y, z, x1, y1, z1, b))
    return out


def cmd(box):
    x, y, z, x1, y1, z1, b = box
    if (x, y, z) == (x1, y1, z1):
        return f'setblock {x} {y} {z} {b} strict'
    return f'fill {x} {y} {z} {x1} {y1} {z1} {b} strict'


def vol(box):
    return (box[3] - box[0] + 1) * (box[4] - box[1] + 1) * (box[5] - box[2] + 1)


def slices(B):
    """Backdrop boxes in build order (the dome from the water up, the water, then the lights), cut into slices of
    about SLICE_BLOCKS blocks."""
    def group(f):
        return {p: b for p, b in B.items() if f(p, b)}
    dome = group(lambda p, b: p[1] > FLOOR_Y and not b.startswith('minecraft:light['))
    floor = group(lambda p, b: p[1] == FLOOR_Y)
    lights = group(lambda p, b: b.startswith('minecraft:light['))
    order = []
    for part in (dome, floor, lights):
        boxes = greedy(part)
        boxes.sort(key=lambda bx: (bx[1], bx[2], bx[0]))
        order += boxes
    out, cur, n = [], [], 0
    for bx in order:
        if cur and (n + vol(bx) > SLICE_BLOCKS or len(cur) >= SLICE_CMDS):
            out.append(cur)
            cur, n = [], 0
        cur.append(bx)
        n += vol(bx)
    if cur:
        out.append(cur)
    return out


def zone(zone_id, kind, bounds, center, cells):
    x0, z0, x1, z1 = bounds
    cx, cz = center
    return dict(id=zone_id, kind=kind, boss_id="narukami", x0=x0, z0=z0, x1=x1, z1=z1, cx=cx, cz=cz, mn=1, mx=1,
                nc=len(cells), ncm=len(cells) - 1, cells=cells, by=0, cy=201, sd=0, pits=[], fn="narukami")


def cell(x0, z0, x1, z1, entry=None):
    ex0, ez0, ex1, ez1 = entry or (x0 + 1, z0 + 1, x1, z1)
    return dict(x0=x0, z0=z0, x1=x1, z1=z1, ix0=x0 + 1, iz0=z0 + 1, ix1=x1 - 1, iz1=z1 - 1, ex0=ex0 * 100,
                ez0=ez0 * 100, ex1=ex1 * 100, ez1=ez1 * 100, sx0=x0 + 2, sz0=z0 + 2, sx1=x1 - 2, sz1=z1 - 2)


def strip_cells():
    """Erase-only cells of zone 1: 128 x 12 strips over the dungeon box. x0 = -64 is outside the screen minimap's
    grid (-60..59), entry / interior bounds are empty (never entered, nothing to break), so only room/zone_erase
    uses them; each erase fill stays under the 32768-block limit (128 x 12 x 20)."""
    out = []
    z = BOX[0]
    while z <= BOX[1]:
        z1 = min(BOX[1], z + 11)
        out.append(dict(x0=BOX[0], z0=z, x1=BOX[1], z1=z1, ix0=0, iz0=0, ix1=-1, iz1=-1, ex0=1000000, ez0=1000000,
                        ex1=-1000000, ez1=-1000000, sx0=-4, sz0=26, sx1=3, sz1=37))
        z = z1 + 1
    return out


def layout():
    arena_cells = [cell(-24, -24, -1, -1, (-23, -23, 0, 0)), cell(0, -24, 23, -1, (0, -23, 23, 0)),
                   cell(-24, 0, -1, 23, (-23, 0, 0, 21)), cell(0, 0, 23, 23, (0, 0, 23, 21))]
    foyer_cells = [cell(-6, 24, 5, 39, (-4, 26, 4, 37))] + strip_cells()
    return dict(
        n=2, boss_id="narukami",
        zones=[zone(1, 0, FOYER, (0, 32), foyer_cells), zone(2, 9, (-24, -24, 23, 23), (0, 0), arena_cells)],
        # tm (the door's top marker row) sits under the pier floor, out of sight
        doors=[dict(a=1, b=2, x0=DOOR[0], x1=DOOR[1], z0=DOOR[2], z1=DOOR[3], mx=0, mz=24, ya=0, yb=180, h=0,
                    y0=201, y1=205, l0=206, l1=207, my=201, tx0=-2, tx1=1, tz0=24, tz1=24, tm=199)],
        spawn=dict(x=0, z=33, yaw=180), spot=dict(x=0, z=33),
        arena=dict(x=0, y=201, z=0, radius=23, safe_radius=21))


# ------------------------------------------------------------------------------------------------ write
def write(name, lines):
    p = OUT / (name + '.mcfunction')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def spin_quat(k):
    e = dict(BD.ENTITIES[[x['tag'] for x in BD.ENTITIES].index('vortex')])
    return BD.left_rotation(e, spin=-15.0 * k)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.rglob('*.mcfunction'):
        old.unlink()
    write('layout', [
        '# All non-chapter-boss stages use Narukami. The boss_id gates only this encounter\'s geometry. Zone 1 also',
        '# lists erase-only strips over the dungeon box (the dome lives outside the walk square).',
        'data modify storage rlk:room cur set value ' + json.dumps(layout(), separators=(',', ':')),
        '# The native door draws its lintel with th.lb: the torii\'s vermilion tie beam.',
        f'data modify storage rlk:room th.lb set value "{TORII_RED}"',
        f'data modify storage rlk:room th.lb2 set value "{TORII_RED}"',
    ])
    write('build', [
        '# @s = room zone marker (room/zone_build). Fixed absolute geometry inside the zone cells (zone 1 strips cover',
        '# the dome). The foyer starts the sliced backdrop job; the arena builds the walk square at once.',
        'execute if score @s zid matches 1 run function rlk:room/raiden/foyer',
        'execute if score @s zkind matches 9 run function rlk:room/raiden/arena',
    ])
    fb = greedy(foyer_blocks())
    write('foyer', [
        '# @s = zone 1 marker at map generation: the entrance pier with its torii (the native door fills the torii),',
        '# invisible barriers around it, its light; then the Plane of Euthymia backdrop is built in slices.',
        f'fill {FOYER[0]} 201 {FOYER[1]} {FOYER[2]} 230 {FOYER[3]} minecraft:air strict',
    ] + [cmd(b) for b in fb] + [
        'tag @s add rlk_rd_bgzone',
        'function rlk:room/raiden/bg/start',
    ])
    ab = greedy(arena_blocks())
    arena = [
        '# @s = zone 2 marker (door reveal / test start): the walk square of the circle centred on (0,201,0), walk',
        '# radius 23, invisible barriers on r 23..24 (y 201..210), light at y 204. The four quadrants are the zone',
        '# cells (native cleanup bounds and the 32768-block fill limit). The door is cut / opened / sealed by the',
        '# native room/door_* after construction.',
    ]
    for (qx, qz) in ((-24, -24), (0, -24), (-24, 0), (0, 0)):
        arena.append(f'fill {qx} 201 {qz} {qx + 23} {BAR_TOP} {qz + 23} minecraft:air strict')
    arena += [cmd(b) for b in ab]
    arena += [
        'kill @e[type=minecraft:marker,tag=rlk_raiden_arena]',
        'summon minecraft:marker 0 201 0 {Tags:["rlk_room","rlk_raiden_arena"],data:{boss_id:"narukami",radius:23,'
        'safe_radius:21}}',
        '# The backdrop job starts with the foyer; run it here if it never ran or was aborted.',
        'execute unless score #rdBgI rd matches 0.. run function rlk:room/raiden/bg/start',
    ]
    write('arena', arena)
    # ---- looks (rd/plan.md D.3): the Shogun's teal water <-> the Tenma's dark blue-violet water
    lo, hi = SWAP_BOX
    look = {'tenma': ['# Tenma look: the near water turns dark blue-violet (one replace fill per block type, y 200 only);'
                      ' called by the transformation.'],
            'shogun': ['# Shogun look: the near water back to teal; called by normal_return, death/finish, cleanup and'
                       ' reload.']}
    for s, t in zip(SHOGUN, TENMA):
        # strict: no neighbour updates / on-place logic (the powders would each schedule a falling check)
        look['tenma'].append(f'fill {lo} {FLOOR_Y} {lo} {hi} {FLOOR_Y} {hi} {t} replace {s} strict')
        look['shogun'].append(f'fill {lo} {FLOOR_Y} {lo} {hi} {FLOOR_Y} {hi} {s} replace {t} strict')
    write('look_tenma', look['tenma'])
    write('look_shogun', look['shogun'])
    # ---- the sliced backdrop job
    B = backdrop_blocks()
    SL = slices(B)
    n = len(SL) + 1                             # + the panel slice
    write('bg/start', [
        '# Start (or restart) the sliced Plane of Euthymia backdrop: #rdBgI rd = next slice (-1 aborted, '
        f'{n} done).',
        'scoreboard players set #rdBgI rd 0',
        'scoreboard players set #rdBgW rd 0',
        'schedule function rlk:room/raiden/bg/tick 1t replace',
    ])
    tick = [
        f'# One backdrop slice per tick ({n} slices: {sum(vol(b) for s in SL for b in s):,} blocks, then the panels).',
        '# Stops when the boss map is gone (the zone 1 marker carries rlk_rd_bgzone) and waits for unloaded chunks.',
        'execute unless entity @e[type=minecraft:marker,tag=rlk_rd_bgzone,limit=1] run return run scoreboard players '
        'set #rdBgI rd -1',
    ]
    for cx, cz in ((-62, -62), (61, -62), (-62, 61), (61, 61)):
        tick.append(f'execute in minecraft:overworld unless loaded {cx} {FLOOR_Y} {cz} run return run function '
                    'rlk:room/raiden/bg/wait')
    tick.append('scoreboard players set #rdBgW rd 0')
    for i in range(n):
        tick.append(f'execute if score #rdBgI rd matches {i} in minecraft:overworld run function rlk:room/raiden/bg/s/{i}')
    tick += ['scoreboard players add #rdBgI rd 1',
             f'execute if score #rdBgI rd matches 1..{n - 1} run schedule function rlk:room/raiden/bg/tick 1t replace']
    write('bg/tick', tick)
    write('bg/wait', [
        '# The dungeon box is not loaded yet (forceloaded chunks load within a few ticks): wait, 200 t -> abort.',
        'scoreboard players add #rdBgW rd 1',
        'execute if score #rdBgW rd matches 200.. run return run scoreboard players set #rdBgI rd -1',
        'schedule function rlk:room/raiden/bg/tick 1t replace',
    ])
    for i, s in enumerate(SL):
        write(f'bg/s/{i}', [f'# Backdrop slice {i + 1}/{n} ({sum(vol(b) for b in s):,} blocks).'] + [cmd(b) for b in s])
    panels = [f'# Backdrop slice {n}/{n}: the display panels ({len(BD.ENTITIES)} entities, build_raiden_backdrop.py),'
              ' then the vortex starts turning.',
              'kill @e[type=minecraft:item_display,tag=rlk_rd_bg]']
    panels += [BD.summon_line(e, ['rlk_room', 'rlk_rd_bg']) for e in BD.ENTITIES]
    panels += ['scoreboard players set #rdVx rd 0', 'schedule function rlk:room/raiden/bg/spin 100t replace']
    write(f'bg/s/{n - 1}', panels)
    spin = ['# The vortex turns 15 deg per 100 t (one turn in 2 min) by interpolated left_rotation; re-armed while it exists.',
            'execute unless entity @e[type=minecraft:item_display,tag=rlk_rd_bg_vortex,limit=1] run return 0',
            'scoreboard players add #rdVx rd 1',
            'execute if score #rdVx rd matches 24.. run scoreboard players set #rdVx rd 0']
    for k in range(24):
        q = ','.join(BD.nbt_f(c) for c in spin_quat(k))
        spin.append(f'execute if score #rdVx rd matches {k} run data merge entity @e[type=minecraft:item_display,'
                    f'tag=rlk_rd_bg_vortex,limit=1] {{start_interpolation:0,interpolation_duration:100,'
                    f'transformation:{{left_rotation:[{q}]}}}}')
    spin.append('schedule function rlk:room/raiden/bg/spin 100t replace')
    write('bg/spin', spin)
    nblk = sum(vol(b) for s in SL for b in s)
    (wmin, wmean, wmax), (amin, amean) = floor_light_report(B, arena_blocks(), foyer_blocks())
    print(f'Floor light: walk circle {wmin}..{wmax} (mean {wmean:.1f}), whole floor min {amin} (mean {amean:.1f}); '
          f'{sum(1 for b in B.values() if b.startswith("minecraft:light["))} light blocks.')
    print(f'Generated Narukami arena: radius 23, centre (0,201,0); backdrop {n} slices, {nblk:,} blocks, '
          f'{sum(len(s) for s in SL)} fills; arena square {len(ab)} fills; foyer {len(fb)} fills; '
          f'{len(BD.ENTITIES)} panels.')


if __name__ == '__main__':
    main()
