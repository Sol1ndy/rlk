#!/usr/bin/env python3
"""Circular mid-boss arena (중간보스 경기장) generator.

    python3 tools/build_mboss_arena.py

Writes F:mboss/arena/** (F = data/rlk/function) from tools/mboss_registry.json "arena":
centre (cx, cy, cz) is a block CORNER (like Raiden's (0,201,0)); stand height cy, floor blocks at
cy-1 (pattern) and cy-2 (base); a disc of radius r (block-centre test), walkable radius walk
(the wall ring walk < d <= r is 7 blocks high), barrier cap on the wall ring up to cy+14 and a
light layer at cy+5 over the walkable disc (floor block light about 10, so nothing spawns at night).

Theme "plaza" follows understand/m2.md §2 (the Corrupted Guardian's plaza): pale marble (calcite with
warmer smooth-quartz patches), three faint engraved rings (white concrete, one block wide) with gold
studs on the outer one, a central rose four-point star with long thin points (pink concrete, a thin
crimson pink-terracotta outline, a small light pink-wool heart), eight slender rose blades that swirl
around it (pink-terracotta outline around a pale pink concrete-powder core; each one detached from the
star, tapered at both ends and bending at most about 35 degrees, so the floor reads as a whirl and never
as a cross with hooked arms), and twelve gold lamp spires on the white wall (gold column, ochre
froglight core, end-rod star).

Runtime files:
  arena/ensure   rebuild when storage rlk:mboss built != "<theme>@<ver>" or the sentinel block is wrong
  arena/build    clear + build the current theme, set built
  arena/build_<theme>, arena/rebuild (forced), arena/clear (air over the whole box, for room/remove)
Run with "in minecraft:overworld" (callers do). layout() is importable for offline renders.
"""
import math
import mboss_lib as L

REG = L.load_registry()
A = REG['arena']
CX, CY, CZ = A['cx'], A['cy'], A['cz']
RAD, WALK = A['r'], A['walk']
THEME, VER = A['theme'], A['ver']
X0, X1, Z0, Z1 = CX - 24, CX + 23, CZ - 24, CZ + 23
YF, YB = CY - 1, CY - 2              # pattern floor, base floor
YW0, YW1 = CY, CY + 6                # wall 201..207
YC0, YC1 = CY + 7, CY + 14           # barrier cap 208..215
YLIGHT = CY + 5
YTOP = CY + 35

STAR_R = 13.0         # four-point star tip radius (points on the axes)
STAR_P = 0.62         # superellipse exponent (< 1 = concave sides, long thin points)
STAR_COVER = 0.4      # a cell belongs to the star when this share of it is inside (keeps the thin points)
HEART = 3.0           # light heart: |u| + |v| <= HEART
# Swirl blades: BLADES ribbons, the k-th one starting at radius B_R0 on the bearing B_A0 + k * 360 / BLADES,
# heading B_LEAN degrees off the outward direction, turning B_TURN degrees over B_LEN blocks (gentle, the
# same way round for all), width B_W in the middle tapering to B_WMIN at both ends.
BLADES, B_A0, B_R0, B_LEAN, B_TURN, B_LEN, B_W, B_WMIN = 8, 0.0, 12.0, 40.0, 35.0, 12.0, 3.6, 1.0
RINGS = (12.6, 16.8, 19.3)                                     # engraved grooves (white concrete)
LAMPS = 12


def cell_polar(x, z):
    u, v = x + 0.5 - CX, z + 0.5 - CZ
    return u, v, math.hypot(u, v), math.degrees(math.atan2(v, u)) % 360


def _hash(x, z, s=0):
    h = (x * 374761393 + z * 668265263 + s * 1442695041) & 0xffffffff
    h = ((h ^ (h >> 13)) * 1274126177) & 0xffffffff
    return (h ^ (h >> 16)) / 0xffffffff


def _noise(x, z, scale=5.0, s=0):
    """Smooth value noise in [0,1] (bilinear over a coarse lattice)."""
    fx, fz = x / scale, z / scale
    ix, iz = math.floor(fx), math.floor(fz)
    tx, tz = fx - ix, fz - iz
    tx, tz = tx * tx * (3 - 2 * tx), tz * tz * (3 - 2 * tz)
    a, b = _hash(ix, iz, s), _hash(ix + 1, iz, s)
    c, d = _hash(ix, iz + 1, s), _hash(ix + 1, iz + 1, s)
    return (a * (1 - tx) + b * tx) * (1 - tz) + (c * (1 - tx) + d * tx) * tz


def _angdiff(a, b):
    return (a - b + 180) % 360 - 180


def star_value(u, v):
    """< 1 inside the four-point star."""
    return (abs(u) ** STAR_P + abs(v) ** STAR_P) / (STAR_R ** STAR_P)


def _outline(cells):
    n4 = ((1, 0), (-1, 0), (0, 1), (0, -1))
    return {c for c in cells if any((c[0] + dx, c[1] + dz) not in cells for dx, dz in n4)}


def _star():
    """Cells of the star by coverage (4 x 4 samples per cell), so the long thin points survive."""
    cells = set()
    for z in range(Z0, Z1 + 1):
        for x in range(X0, X1 + 1):
            k = sum(star_value(x + (i + 0.5) / 4 - CX, z + (j + 0.5) / 4 - CZ) <= 1.0
                    for i in range(4) for j in range(4))
            if k >= STAR_COVER * 16:
                cells.add((x, z))
    return cells


def _blades():
    """Cells of the swirl blades: each follows a circular arc (constant turn rate) from its start point,
    tapering sin-shaped from B_WMIN to B_W and back. {(x, z)}."""
    cells = set()
    steps = 400
    ds = B_LEN / steps
    k_turn = math.radians(B_TURN) / B_LEN
    for k in range(BLADES):
        a = math.radians(B_A0 + 360.0 / BLADES * k)
        x, z = B_R0 * math.cos(a), B_R0 * math.sin(a)
        h = a + math.radians(B_LEAN)
        for i in range(steps + 1):
            t = i / steps
            half = (B_WMIN + (B_W - B_WMIN) * math.sin(math.pi * t) ** 0.8) / 2
            for gx in range(math.floor(x - half - 1), math.ceil(x + half + 1) + 1):
                for gz in range(math.floor(z - half - 1), math.ceil(z + half + 1) + 1):
                    if math.hypot(gx + 0.5 - x, gz + 0.5 - z) <= half:
                        cells.add((CX + gx, CZ + gz))
            x += math.cos(h) * ds
            z += math.sin(h) * ds
            h += k_turn * ds
    return cells


def _drop_specks(cells, keep=6):
    """Removes 4-connected pieces smaller than `keep` cells (thin blade ends cut off by the taper or the rim)."""
    left, out = set(cells), set()
    while left:
        stack, comp = [left.pop()], []
        while stack:
            c = stack.pop()
            comp.append(c)
            for dx, dz in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                n = (c[0] + dx, c[1] + dz)
                if n in left:
                    left.remove(n)
                    stack.append(n)
        if len(comp) >= keep:
            out.update(comp)
    return out


def _rose():
    """Star and blades. The star: light heart, thin crimson outline, rose fill. The blades (never
    touching the star): crimson outline around a pale pink core. Returns {(x, z): block}."""
    star = _star()
    star_ol = _outline(star)
    blades = {c for c in _blades() - star if cell_polar(*c)[2] <= WALK - 0.6}
    blades = _drop_specks(blades)
    blade_ol = _outline(blades)
    out = {}
    for (x, z) in blades:
        out[(x, z)] = 'minecraft:pink_terracotta' if (x, z) in blade_ol else 'minecraft:pink_concrete_powder'
    for (x, z) in star:
        u, v, _, _ = cell_polar(x, z)
        if abs(u) + abs(v) <= HEART:
            out[(x, z)] = 'minecraft:pink_wool'
        elif (x, z) in star_ol:
            out[(x, z)] = 'minecraft:pink_terracotta'
        else:
            out[(x, z)] = 'minecraft:pink_concrete'
    return out


ROSE = _rose()


def floor_block(x, z):
    u, v, r, phi = cell_polar(x, z)
    if r > WALK:
        return 'minecraft:polished_diorite'
    if (x, z) in ROSE:
        return ROSE[(x, z)]
    for rr in RINGS:
        if abs(r - rr) < 0.5:
            # gold studs on the outer groove, one in front of every lamp spire
            if rr == RINGS[-1] and abs(_angdiff(phi, 15 + round((phi - 15) / 30) * 30)) * math.pi / 180 * r < 0.5:
                return 'minecraft:gold_block'
            return 'minecraft:white_concrete'
    n = _noise(x, z, 4.0, 1)
    if n > 0.88 or n < 0.08:
        return 'minecraft:smooth_quartz'
    return 'minecraft:calcite'


def lamp_cells():
    """Wall columns that carry a lamp spire: nearest wall cell to (r - 0.5, 15 + 30 k degrees)."""
    out = []
    for k in range(LAMPS):
        a = math.radians(15 + 30 * k)
        tx, tz = CX + (RAD - 0.5) * math.cos(a), CZ + (RAD - 0.5) * math.sin(a)
        out.append((math.floor(tx), math.floor(tz), 15 + 30 * k))
    return out


def layout():
    """{(x, y, z): block} of everything the build places (air not listed)."""
    blocks = {}
    lamps = {(x, z): a for x, z, a in lamp_cells()}
    wall = []
    for z in range(Z0, Z1 + 1):
        for x in range(X0, X1 + 1):
            _, _, r, phi = cell_polar(x, z)
            if r > RAD:
                continue
            blocks[(x, YB, z)] = 'minecraft:polished_blackstone'
            blocks[(x, YF, z)] = floor_block(x, z)
            if r > WALK:
                wall.append((x, z, phi))
    for x, z, phi in wall:
        if (x, z) in lamps:
            for y in range(YW0, YW1 + 2):
                blocks[(x, y, z)] = 'minecraft:gold_block'
            continue
        pil = abs(_angdiff(phi, round(phi / 15) * 15)) * math.pi / 180 * RAD < 0.55
        blocks[(x, YW0, z)] = 'minecraft:polished_diorite'
        for y in range(YW0 + 1, YW1 - 1):
            blocks[(x, y, z)] = 'minecraft:quartz_pillar' if pil else 'minecraft:calcite'
        blocks[(x, YW1 - 1, z)] = 'minecraft:chiseled_quartz_block'
        blocks[(x, YW1, z)] = 'minecraft:smooth_quartz'
    # lamp spire tops: froglight core one above the column, end-rod star around it, rod on top
    for (x, z), a in lamps.items():
        yc = YW1 + 2
        blocks[(x, yc, z)] = 'minecraft:ochre_froglight'
        blocks[(x, yc + 1, z)] = 'minecraft:end_rod[facing=up]'
        for dx, dz, f in ((1, 0, 'east'), (-1, 0, 'west'), (0, 1, 'south'), (0, -1, 'north')):
            blocks[(x + dx, yc, z + dz)] = f'minecraft:end_rod[facing={f}]'
    return blocks


def spans(cells):
    """Row spans [(z, x0, x1, block)] from {(x, z): block} at one y."""
    out = []
    rows = {}
    for (x, z), b in cells.items():
        rows.setdefault(z, []).append((x, b))
    for z in sorted(rows):
        row = sorted(rows[z])
        start, prev, cur = row[0][0], row[0][0], row[0][1]
        for x, b in row[1:]:
            if x == prev + 1 and b == cur:
                prev = x
                continue
            out.append((z, start, prev, cur))
            start, prev, cur = x, x, b
        out.append((z, start, prev, cur))
    return out


def sentinel():
    return floor_block(CX, CZ)


def build_lines():
    blocks = layout()
    lines = [f'# GENERATED by tools/build_mboss_arena.py ({THEME}@{VER}). Run in minecraft:overworld.',
             '# 1. clear the box in four quadrants (each below the 32768-block fill limit)']
    for xa, xb in ((X0, CX - 1), (CX, X1)):
        for za, zb in ((Z0, CZ - 1), (CZ, Z1)):
            lines.append(f'fill {xa} {YB} {za} {xb} {YTOP} {zb} minecraft:air strict')
    by_y = {}
    for (x, y, z), b in blocks.items():
        by_y.setdefault(y, {})[(x, z)] = b
    lines.append('# 2. floor, wall and lamps, row spans per layer')
    for y in sorted(by_y):
        for z, xa, xb, b in spans(by_y[y]):
            if xa == xb:
                lines.append(f'setblock {xa} {y} {z} {b} strict')
            else:
                lines.append(f'fill {xa} {y} {z} {xb} {y} {z} {b} strict')
    lines.append('# 3. barrier cap over the wall ring (lamp tops keep their blocks)')
    ring = {}
    for z in range(Z0, Z1 + 1):
        for x in range(X0, X1 + 1):
            _, _, r, _ = cell_polar(x, z)
            if WALK < r <= RAD:
                ring[(x, z)] = 'barrier'
    for z, xa, xb, _ in spans(ring):
        lines.append(f'fill {xa} {YC0} {z} {xb} {YC1} {z} minecraft:barrier replace air')
    lines.append('# 4. light layer over the walkable disc (no natural spawns, bright floor at night)')
    disc = {}
    for z in range(Z0, Z1 + 1):
        for x in range(X0, X1 + 1):
            _, _, r, _ = cell_polar(x, z)
            if r <= WALK - 0.5:
                disc[(x, z)] = 'light'
    for z, xa, xb, _ in spans(disc):
        lines.append(f'fill {xa} {YLIGHT} {z} {xb} {YLIGHT} {z} minecraft:light[level=15] replace air')
    lines.append(f'data modify storage rlk:mboss built set value "{THEME}@{VER}"')
    return lines


def main():
    out = L.Out(owned_dirs=['mboss/arena'])
    body = build_lines()
    out.write(f'mboss/arena/build_{THEME}', body)
    corners = f'if loaded {X0} {CY} {Z0} if loaded {X1} {CY} {Z1} if loaded {CX} {CY} {CZ}'
    out.write('mboss/arena/ensure', [
        '# Rebuild the arena when its version string or the centre sentinel block is wrong (cheap check).',
        '# Run in minecraft:overworld; does nothing while the forceloaded chunks are not loaded yet.',
        f'execute unless loaded {X0} {CY} {Z0} run return fail',
        f'execute unless loaded {X1} {CY} {Z1} run return fail',
        f'execute unless data storage rlk:mboss {{built:"{THEME}@{VER}"}} run return run function rlk:mboss/arena/build',
        f'execute unless block {CX} {YF} {CZ} {sentinel()} run return run function rlk:mboss/arena/build',
        'return 1'])
    out.write('mboss/arena/build', [
        '# Clear and build the current theme (one tick, strict fills: no block updates).',
        f'execute {corners} run function rlk:mboss/arena/build_{THEME}'])
    out.write('mboss/arena/rebuild', [
        '# Dev: force a rebuild. /execute in minecraft:overworld run function rlk:mboss/arena/rebuild',
        'data remove storage rlk:mboss built',
        'function rlk:mboss/arena/build'])
    out.write('mboss/arena/clear', [
        '# Air over the whole arena box (room/remove). Run in minecraft:overworld.']
        + [f'fill {xa} {YB} {za} {xb} {YTOP} {zb} minecraft:air strict'
           for xa, xb in ((X0, CX - 1), (CX, X1)) for za, zb in ((Z0, CZ - 1), (CZ, Z1))]
        + ['data remove storage rlk:mboss built'])
    removed = out.clean()
    n = len(body)
    print(f'mboss arena: {THEME}@{VER}, centre ({CX},{CY},{CZ}) r {RAD} walk {WALK}, {n} build commands, '
          f'{len(layout())} blocks, sentinel {sentinel()}, {removed} stale removed.')


if __name__ == '__main__':
    main()
