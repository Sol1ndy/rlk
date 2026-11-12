"""Arena theme `tk_lift`: the lift platform at the bottom of the Naytiba shaft where 타키 (Tachy) waits (PLAN §6).

Theme module (scratchpad az/contract/theme.md): plain Python, stdlib only, deterministic, no side effects on import,
never writes files. The arena generator (tools/build_mboss_arena.py) imports `arena_layout`, `slices`, `look_lines`,
`SENTINEL` and `CHECK`; the module and the tests import `POINTS`, `props` and the constants. No domain entrance (the
special boss is reached through the rift: `entrance_layout` is absent on purpose).

The place (footage v1 / v2 22-40 / v6 / v8: scratchpad tk/ref/intro_v2_overview_b.jpg, t_C1_v6_a.jpg): a round
industrial lift platform half buried in sand at the bottom of a dark shaft, in a warm orange haze, ringed by a wall with
barred windows and chain columns, red Naytiba flesh creeping over a third of it; truss towers with ochre lamps beyond
the wall; the big lamp machine of v1 hangs over the centre from the shaft ceiling, cables drooping from it.

  floor (d <= 27)       solid y 193..200 of full opaque blocks; the top (y 200) inside walk 24 is flat: smooth
                        sandstone with sandstone / cut red sandstone noise and single-layer sand drifts (on solid
                        blocks), polished-deepslate grooves at r 6 / 11 / 16 / 21, the copper centre disc (r 4), four
                        5 x 5 hatch panels at r 14 on the diagonals (polished tuff, yellow / black hazard border)
  wall (24 < d <= 27)   y 201..210 polished blackstone bricks, iron-bar windows, chain columns every 30 degrees, flesh
                        patches (nether wart block, crimson hyphae, shroomlight nodes) on a third of the ring; the
                        barrier cap y 211..225 on the wall ring
  beyond (27 < d <= 39) the shaft floor y 190..191, eight truss towers (waxed copper girders, iron bars, chains, ochre
                        froglight lamps) at r 32.5 up to y 234, flesh tendrils on the shaft wall (38 < d <= 39.6,
                        y 190..242), the dark ceiling y 242
  overhead              the lamp machine y 226..241 (cylinder r 4.5: polished deepslate, two yellow bands, an iron
                        rim, an ochre froglight ring + light blocks underneath, chains up to the ceiling) and ten
                        cables (black wool) drooping from it to the towers, never below y 226 over the walk disc
  lights                the light layer y 206 (level 15) over the walk disc (floor block light 10: no spawns); hidden
                        light[level=15] blocks wherever a spawnable cell of the box would be dark (both looks)

Coordinates: the centre (640, 201, 8) is a block corner, floor blocks at y 200, stand height 201. A cell (x, z) is "at
distance d" when its centre (x + 0.5, z + 0.5) is d blocks from (640, 8) horizontally.

Looks: 'dust' (phases 1-2, the default restored by the framework's ensure) and 'abyss' (phase 3, the T2 'dark' job):
the walk-disc floor top (sand, sandstone, copper) becomes deepslate tiles / cracked tiles / tuff bricks with red nether
brick veins and shroomlight nodes, the copper disc cracked polished blackstone bricks, more flesh on the wall.
`look_lines(look)` turns any built look into `look` with absolute setblock / fill spans (2 slices).
"""
import math

THEME = 'tk_lift'
AID = 'tk_lift'

CX, CY, CZ = 640, 201, 8
RAD, WALK, SAFE = 27, 24, 22
BOX = {'x0': 600, 'y0': 190, 'z0': -32, 'x1': 680, 'y1': 250, 'z1': 48}
START = {'x': 640.5, 'y': 201.0, 'z': 30.5, 'yaw': 180.0, 'pitch': 0.0}
CHECK = {'n': 3, 'theme': THEME, 'ver': 1, 'cx': CX, 'cy': CY, 'cz': CZ, 'r': RAD, 'walk': WALK, 'safe': SAFE,
         'box': dict(BOX), 'start': dict(START), 'looks': ['dust', 'abyss'], 'oob': {'y0': 198, 'y1': 235}}
LOOKS = ('dust', 'abyss')

FLOOR_Y = CY - 1                # 200: the floor top
SOLID_Y0 = 193                  # platform solid y 193..200 (d <= RAD)
SHAFT_Y0, SHAFT_Y1 = 190, 191   # shaft floor
WALL_Y = (201, 210)
BARRIER_Y = (211, 225)
LIGHT_Y = 206
CLEAR_Y = (201, 225)            # above the walk disc: only the light layer
MACHINE_Y = (226, 241)
CEIL_Y = 242
SHAFT_R = (38.0, 39.6)
TOWER_R, TOWER_TOP = 32.5, 234
GROOVES = (6, 11, 16, 21)
DISC_R, DISC_CORE = 4.0, 2.5
HATCH_R = 14.0
MACHINE_R = 4.5
MAX_FILL, MAX_LOOK_SLICES = 32768, 2

SENTINEL = ((CX, 196, CZ), 'minecraft:polished_deepslate')

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


def _in_box(x, y, z):
    return BOX['x0'] <= x <= BOX['x1'] and BOX['y0'] <= y <= BOX['y1'] and BOX['z0'] <= z <= BOX['z1']


def polar_point(d, bearing, y=201.0):
    """absolute (x, y, z) of the point d blocks from the centre on a compass bearing"""
    a = math.radians(bearing)
    return (round(CX + d * math.sin(a), 3), y, round(CZ - d * math.cos(a), 3))


# ---------------------------------------------------------------------------------------------------------------
# the floor

HATCHES = []
for _k in range(4):
    _hx, _hy, _hz = polar_point(HATCH_R, 45 + 90 * _k)
    HATCHES.append((math.floor(_hx), math.floor(_hz)))


def _hatch(x, z):
    """None, 'in' or 'b0' / 'b1' (the hazard border stripes) for a cell of a 5 x 5 hatch panel"""
    for hx, hz in HATCHES:
        dx, dz = x - hx, z - hz
        if abs(dx) <= 2 and abs(dz) <= 2:
            if max(abs(dx), abs(dz)) == 2:
                return 'b0' if (dx + dz) % 2 == 0 else 'b1'
            return 'in'
    return None


def _vein(x, z):
    """the abyss floor's red veins: thin noisy lines"""
    n = _fbm(x, z, 7.0, 41)
    return abs(n - 0.5) < 0.028


def floor_top(x, z, look):
    """the block at y 200 of a cell inside the platform (d <= RAD)"""
    d = _d(x, z)
    if d > WALK:
        return _p('polished_blackstone_bricks')
    if d <= DISC_R:
        if look == 'abyss':
            return _p('cracked_polished_blackstone_bricks')
        return _p('waxed_cut_copper') if d <= DISC_CORE else _p('waxed_weathered_cut_copper')
    h = _hatch(x, z)
    if h == 'in':
        return _p('polished_tuff')
    if h in ('b0', 'b1'):
        return _p('yellow_concrete') if h == 'b0' else _p('black_concrete')
    for g in GROOVES:
        if abs(d - g) < 0.5:
            return _p('polished_deepslate')
    if look == 'abyss':
        if _vein(x, z):
            # shroomlight nodes on the veins, about every 6 b
            if _mix(x // 3, z // 3, 7) < 0.3 and _mix(x, z, 8) < 0.4:
                return _p('shroomlight')
            return _p('red_nether_bricks')
        n = _fbm(x, z, 5.0, 3)
        if n > 0.66:
            return _p('cracked_deepslate_tiles')
        if n < 0.3:
            return _p('tuff_bricks')
        return _p('deepslate_tiles')
    drift = _fbm(x, z, 9.0, 11) + 0.004 * max(0.0, d - 10)
    if drift > 0.64 and d > 6.5:
        return _p('sand')
    n = _fbm(x, z, 4.0, 5)
    if n > 0.72:
        return _p('sandstone')
    if n < 0.2:
        return _p('cut_red_sandstone')
    return _p('smooth_sandstone')


# ---------------------------------------------------------------------------------------------------------------
# the wall ring

CHAIN_BEARINGS = tuple(15 + 30 * k for k in range(12))
WINDOW_BEARINGS = tuple(30 * k for k in range(12) if k % 3 != 0)          # 8 barred windows (not at the arrival)
FLESH_ARCS = {'dust': ((95, 165), (215, 245), (295, 330)),                # ~ a third of the ring
              'abyss': ((95, 165), (215, 245), (295, 330), (35, 80), (250, 290), (170, 200), (0, 30), (335, 360))}


def _flesh(bearing, look):
    return any(a0 <= bearing <= a1 for a0, a1 in FLESH_ARCS[look])


def wall_block(x, y, z, look):
    """the wall ring (WALK < d <= RAD), y 201..210"""
    d = _d(x, z)
    br = _bearing(x, z)
    inner = d <= WALK + 1.0
    # chain columns on the inner face
    if inner and any(abs(_angdiff(br, cb)) * math.pi / 180 * d < 0.55 for cb in CHAIN_BEARINGS) and y <= 209:
        return _p('iron_chain[axis=y]')
    # barred windows through the wall (y 205..207, 3 wide)
    if 205 <= y <= 207 and any(abs(_angdiff(br, wb)) * math.pi / 180 * d < 1.6 for wb in WINDOW_BEARINGS):
        return _p('iron_bars')
    if y == WALL_Y[1]:
        return _p('polished_blackstone')
    if inner and _flesh(br, look):
        n = _fbm(br * 0.6, y * 1.7, 3.0, 23 if look == 'dust' else 29)
        if n > (0.36 if look == 'dust' else 0.3):
            if _mix(x, y, z, 31) < 0.06:
                return _p('shroomlight')
            return _p('nether_wart_block') if n > 0.55 else _p('crimson_hyphae')
    if (y - WALL_Y[0]) % 4 == 3:
        return _p('polished_blackstone')
    return _p('polished_blackstone_bricks')


# ---------------------------------------------------------------------------------------------------------------
# towers, shaft, machine, cables

TOWERS = []
for _k in range(8):
    _tx, _ty, _tz = polar_point(TOWER_R, 22.5 + 45 * _k)
    TOWERS.append((math.floor(_tx), math.floor(_tz)))


def _towers(g):
    for tx, tz in TOWERS:
        for y in range(SHAFT_Y1 + 1, TOWER_TOP + 1):
            for dx in (-1, 0, 1):
                for dz in (-1, 0, 1):
                    c = (tx + dx, y, tz + dz)
                    corner, centre = abs(dx) == 1 and abs(dz) == 1, dx == 0 and dz == 0
                    girder = (y - SHAFT_Y1) % 6 == 0
                    if corner:
                        g[c] = _p('waxed_copper_block')
                    elif centre:
                        g[c] = _p('ochre_froglight') if y in (214, 224, TOWER_TOP) else _p('iron_chain[axis=y]')
                    elif girder:
                        g[c] = _p('waxed_cut_copper')
                    elif y in (208, 220):
                        g[c] = _p('ochre_froglight')
                    else:
                        g[c] = _p('iron_bars')
        for dx in (-1, 0, 1):
            for dz in (-1, 0, 1):
                g[(tx + dx, TOWER_TOP + 1, tz + dz)] = _p('waxed_copper_block')


def _shaft(g):
    r0, r1 = SHAFT_R
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            d = _d(x, z)
            if d > r1:
                continue
            br = _bearing(x, z)
            for y in (SHAFT_Y0, SHAFT_Y1):
                g[(x, y, z)] = _p('deepslate_tiles') if y == SHAFT_Y1 else _p('cobbled_deepslate')
            g[(x, CEIL_Y, z)] = _p('blackstone')
            if d > r0:
                for y in range(SHAFT_Y1 + 1, CEIL_Y):
                    band = (y - 190) % 9 == 0
                    t = _fbm(br * 0.9, y * 0.9, 4.0, 51)
                    if t > 0.62 and _vnoise(br * 0.2, 0.0, 1.0, 53) > 0.4:
                        g[(x, y, z)] = _p('crimson_hyphae') if t < 0.7 else _p('nether_wart_block')
                    elif band:
                        g[(x, y, z)] = _p('polished_blackstone')
                    else:
                        g[(x, y, z)] = _p('deepslate_bricks') if _mix(x, y, z, 55) > 0.12 else _p('cracked_deepslate_bricks')


def _machine(g):
    y0, y1 = MACHINE_Y
    for z in range(CZ - 6, CZ + 6):
        for x in range(CX - 6, CX + 6):
            d = _d(x, z)
            if d > MACHINE_R:
                continue
            if d <= 3.5:
                g[(x, 227, z)] = LIGHT15
            for y in range(228, 241):
                if y == 228:
                    b = _p('iron_block') if d > 3.5 else _p('ochre_froglight') if d > 2.4 else _p('polished_deepslate')
                elif y in (232, 236) and d > 3.5:
                    b = _p('yellow_concrete')
                elif y == 240 and d > 3.5:
                    b = _p('iron_block')
                else:
                    b = _p('polished_deepslate')
                g[(x, y, z)] = b
    for dx, dz in ((-3, -3), (2, -3), (-3, 2), (2, 2)):          # hanging chains up to the ceiling
        g[(CX + dx, 241, CZ + dz)] = _p('iron_chain[axis=y]')


CABLE_BEARINGS = tuple(22.5 + 45 * k for k in range(8)) + (0.0, 180.0)


def cable_path(bearing, steps=120):
    """[(d, y)] of one cable from the machine rim (d 4.5, y 229) to a tower top (or the shaft wall), sagging"""
    end_d, end_y = (TOWER_R - 1.2, TOWER_TOP - 1.0) if bearing % 45 else (SHAFT_R[0] - 0.2, 236.0)
    out = []
    for i in range(steps + 1):
        t = i / steps
        d = MACHINE_R + (end_d - MACHINE_R) * t
        y = 229.5 + (end_y - 229.5) * t - 3.0 * math.sin(math.pi * t)
        out.append((d, y))
    return out


def _cables(g):
    for bearing in CABLE_BEARINGS:
        a = math.radians(bearing)
        for d, y in cable_path(bearing):
            x = math.floor(CX + d * math.sin(a))
            z = math.floor(CZ - d * math.cos(a))
            yy = math.floor(y)
            if (x, yy, z) not in g:
                g[(x, yy, z)] = _p('black_wool')
        # danglers beyond the walk disc
        for dd in (27.5, 30.0):
            if dd >= cable_path(bearing)[-1][0]:
                continue
            for d, y in cable_path(bearing):
                if abs(d - dd) < 0.12:
                    x, z = math.floor(CX + d * math.sin(a)), math.floor(CZ - d * math.cos(a))
                    for k in range(1, 4):
                        if (x, math.floor(y) - k, z) not in g:
                            g[(x, math.floor(y) - k, z)] = _p('iron_chain[axis=y]')
                    break


# ---------------------------------------------------------------------------------------------------------------
# light: the light layer, block-light flood and the hidden lights

EMIT = {'light': None, 'ochre_froglight': 15, 'shroomlight': 15}
TRANSPARENT = ('air', 'light', 'iron_chain', 'iron_bars', 'barrier')


def _bid(b):
    return b[len(B):].split('[')[0]


def _emits(b):
    i = _bid(b)
    if i == 'light':
        return int(b.split('level=')[1].rstrip(']'))
    return EMIT.get(i, 0) or 0


def _opaque(b):
    return b is not None and _bid(b) not in TRANSPARENT


def block_light(g):
    """{(x, y, z): level} of every lit non-opaque cell of the box (BFS from the emitters; full blocks stop light)"""
    lv = {}
    frontier = {}
    for c, b in g.items():
        e = _emits(b)
        if e:
            lv[c] = max(lv.get(c, 0), e)
            frontier[c] = lv[c]
    _flood(g, lv, frontier)
    return lv


def _flood(g, lv, frontier):
    level = 15
    buckets = {}
    for c, v in frontier.items():
        buckets.setdefault(v, []).append(c)
    while level > 1:
        cur = buckets.pop(level, [])
        for c in cur:
            if lv.get(c, 0) != level:
                continue
            x, y, z = c
            for n in ((x + 1, y, z), (x - 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)):
                if not _in_box(*n) or _opaque(g.get(n)):
                    continue
                if lv.get(n, 0) < level - 1:
                    lv[n] = level - 1
                    buckets.setdefault(level - 1, []).append(n)
        level -= 1


def spawn_cells(g):
    """air cells of the box a mob could spawn in: a full opaque non-barrier block below, two free cells (air / light)"""
    out = []
    for (x, y, z), b in g.items():
        if not _opaque(b) or _bid(b) == 'barrier':
            continue
        a1, a2 = g.get((x, y + 1, z)), g.get((x, y + 2, z))
        if y + 2 > BOX['y1']:
            continue
        free = lambda v: v is None or _bid(v) == 'light'
        if free(a1) and free(a2):
            out.append((x, y + 1, z))
    return sorted(out, key=lambda c: (c[1], c[2], c[0]))


def _hidden_lights(g_looks):
    """light[level=15] cells (the same in every look) so no spawn cell of any look stays dark; greedy, deterministic"""
    added = []
    for g in g_looks:
        lv = block_light(g)
        for c in spawn_cells(g):
            if lv.get(c, 0) >= 1:
                continue
            d = _d(c[0], c[2])
            assert d > WALK + 0.5 or c[1] >= MACHINE_Y[0], f'dark spawn cell over the walk disc {c}'
            added.append(c)
            for gg in g_looks:
                gg[c] = LIGHT15
            lv[c] = 15
            _flood(g, lv, {c: 15})
    return added


# ---------------------------------------------------------------------------------------------------------------
# the layout

_CACHE = {}


def _base(look):
    g = {}
    _shaft(g)
    for z in range(BOX['z0'], BOX['z1'] + 1):
        for x in range(BOX['x0'], BOX['x1'] + 1):
            d = _d(x, z)
            if d > RAD:
                continue
            for y in range(SOLID_Y0, FLOOR_Y):
                g[(x, y, z)] = _p('polished_deepslate') if y == SOLID_Y0 + 3 or d > RAD - 1 else (
                    _p('smooth_sandstone') if y == FLOOR_Y - 1 else _p('deepslate'))
            g[(x, FLOOR_Y, z)] = floor_top(x, z, look)
            if d > WALK:
                for y in range(WALL_Y[0], WALL_Y[1] + 1):
                    g[(x, y, z)] = wall_block(x, y, z, look)
                for y in range(BARRIER_Y[0], BARRIER_Y[1] + 1):
                    g[(x, y, z)] = _p('barrier')
            else:
                g[(x, LIGHT_Y, z)] = LIGHT15
    _towers(g)
    _machine(g)
    _cables(g)
    return g


def _build():
    if 'all' not in _CACHE:
        gs = [_base(look) for look in LOOKS]
        hidden = _hidden_lights(gs)
        _CACHE['all'] = (dict(zip(LOOKS, gs)), hidden)
    return _CACHE['all']


def arena_layout(look=None):
    """{(x, y, z): block} of every non-air block of the box in `look` (None = 'dust')."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    return dict(_build()[0][look])


def hidden_lights():
    return list(_build()[1])


def slices():
    """16 build slices: 4-layer slabs of the whole box from y 190 up (the last one layer), each 81 x 4 x 81 = 26 244
    blocks <= 32 768; disjoint, covering the box."""
    out = []
    y = BOX['y0']
    while y <= BOX['y1']:
        y1 = min(BOX['y1'], y + 3)
        out.append(((BOX['x0'], y, BOX['z0']), (BOX['x1'], y1, BOX['z1'])))
        y = y1 + 1
    return out


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


def look_lines(look):
    """[[cmd]]: absolute spans that turn any built look into `look` (two slices: the north half z < cz, then the
    south half); every cell any look changes is set to its block in `look`."""
    assert look in LOOKS, look
    lc = look_cells()
    groups = [{}, {}]
    for c, per in lc.items():
        groups[0 if c[2] < CZ else 1][c] = per[look] or 'minecraft:air'
    return [_spans(gp) for gp in groups if gp]


def props(look=None):
    """No arena display props (the intro cables are the rig's prop, the arrival tear the kit's preset)."""
    look = look or LOOKS[0]
    assert look in LOOKS, look
    return []


POINTS = {
    'centre': (float(CX), float(CY), float(CZ), 0.0),
    'start': (START['x'], START['y'], START['z'], START['yaw']),
    'rift': (START['x'], START['y'], START['z'] + 1.5, 0.0),          # the arrival tear, 1.5 b behind the start
    'hang': (float(CX), float(CY) + 7.0, float(CZ), 0.0),             # where Tachy hangs in the intro (7 b up)
    'machine': (float(CX), 228.0, float(CZ), 0.0),                    # the lamp machine's underside centre
    **{f'cable{k}': (*polar_point(MACHINE_R - 0.3, 60 * k, 228.0)[0:1], 228.0, polar_point(MACHINE_R - 0.3, 60 * k)[2],
                     60.0 * k) for k in range(6)},                    # the six intro cable anchors
}


def render_hints():
    return {'top': {'centre': (CX, CZ), 'r': 41}, 'eye': START, 'boss': (CX, CY, CZ)}
