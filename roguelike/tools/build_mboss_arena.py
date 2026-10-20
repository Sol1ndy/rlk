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

Chapter arenas (AZ-CM, scratchpad az/contract/cm.md 6.3 / theme.md 3): every registry arenas{} entry whose theme module
tools/mboss_arena_<theme>.py exists gets sliced jobs (one slice per tick, #mbArBuild = slices left, rlk:mboss arjob):
  arena/<aid>/ensure   1 when built in its default look (stamp built_<aid> = "<aid>@<ver>:<looks[0]>", sentinel) and
                       loaded; else fail, and a build / look / verify job runs (one job at a time)
  arena/<aid>/build    start a full build job (s/<i> slices, done); rebuild = drop the stamp + build; clear = air over
                       the box when loaded + no stamp; sweep {y0,y1} = barriers -> air in row spans inside walk - 0.5
  arena/<aid>/look/<look>  start a look job (l/<look>/<i> slices: the theme's look_lines(look) or the cell diff)
  arena/job_tick (the scheduler), arena/abort (drop the running job), arena/clear_all (every arena's clear)
An arena whose theme module is missing gets stub functions (ensure stamps "<aid>@0:stub" and returns 1). emit(aid) gives
the command lists without writing (theme.md 3; S1-ARENA's test_arena_az.py reproduces it).
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


# =============================================================================================
# Chapter arenas (arenas{}): sliced builds, looks, stamps (cm.md 6.3-6.5, theme.md 3)
MAX_SLICES, MAX_FILL, MAX_CMDS = 40, 32768, 8000


def _vol(b):
    (x0, y0, z0), (x1, y1, z1) = b
    return (x1 - x0 + 1) * (y1 - y0 + 1) * (z1 - z0 + 1)


def _span_lines(cells):
    """Row spans of {(x, y, z): block} (y ascending, z ascending, x runs of equal blocks): fill / setblock ... strict."""
    by_y = {}
    for (x, y, z), b in cells.items():
        by_y.setdefault(y, {})[(x, z)] = b
    lines = []
    for y in sorted(by_y):
        for z, xa, xb, b in spans(by_y[y]):
            if xa == xb:
                lines.append(f'setblock {xa} {y} {z} {b} strict')
            else:
                lines.append(f'fill {xa} {y} {z} {xb} {y} {z} {b} strict')
    return lines


def _in(c, b):
    (x0, y0, z0), (x1, y1, z1) = b
    return x0 <= c[0] <= x1 and y0 <= c[1] <= y1 and z0 <= c[2] <= z1


def emit(aid, reg=None):
    """{'build': [[cmd]], 'looks': {look: [[cmd]]}, 'clear': [cmd]} of a chapter arena with a theme module (no file
    writes): build slices (air + row spans, theme.md 3.1; the done call is added by the writer), look jobs (the theme's
    look_lines or the cell diff against looks[0], grouped by the slices() boxes, theme.md 3.3), the clear fills."""
    reg = reg or REG
    a = reg['arenas'][aid]
    th = L.theme_module(a['theme'])
    assert th is not None, f'{aid}: theme module mboss_arena_{a["theme"]} missing'
    assert th.THEME == a['theme'] and th.AID == aid, (th.THEME, th.AID)
    for k, v in getattr(th, 'CHECK', {}).items():
        assert a[k] == v, f'{aid}: registry {k} {a[k]} != theme CHECK {v}'
    bx = a['box']
    box = ((bx['x0'], bx['y0'], bx['z0']), (bx['x1'], bx['y1'], bx['z1']))
    sl = th.slices()
    assert 1 <= len(sl) <= MAX_SLICES, f'{aid}: {len(sl)} slices'
    assert sum(_vol(b) for b in sl) == _vol(box), f'{aid}: the slices do not cover the box'
    for i, b in enumerate(sl):
        assert _vol(b) <= MAX_FILL, f'{aid}: slice {i} has {_vol(b)} blocks'
        assert _in(b[0], box) and _in(b[1], box), f'{aid}: slice {i} outside the box'
        for j in range(i):
            o = sl[j]
            assert any(b[1][k] < o[0][k] or o[1][k] < b[0][k] for k in range(3)), f'{aid}: slices {j} and {i} overlap'
    looks = a['looks']
    lay0 = th.arena_layout(looks[0])
    for c in lay0:
        assert _in(c, box), f'{aid}: block {c} outside the box'
    (sx, sy, sz), sb = th.SENTINEL
    assert lay0.get((sx, sy, sz)) == sb, f'{aid}: the sentinel is not in the default layout'
    build = []
    for i, b in enumerate(sl):
        (x0, y0, z0), (x1, y1, z1) = b
        cmds = [f'fill {x0} {y0} {z0} {x1} {y1} {z1} minecraft:air strict']
        cmds += _span_lines({c: v for c, v in lay0.items() if _in(c, b)})
        assert len(cmds) <= MAX_CMDS, f'{aid}: build slice {i} has {len(cmds)} commands'
        build.append(cmds)
    out_looks = {}
    for look in looks:
        if len(looks) == 1:
            break
        if hasattr(th, 'look_lines'):
            groups = [list(g) for g in th.look_lines(look)]
        else:
            lay = th.arena_layout(look)
            diff = {c for c in set(lay) | set(lay0) if lay.get(c) != lay0.get(c)}
            if look == looks[0]:
                # the default look from any other look: every cell any other look changes, back to the default
                diff = set()
                for other in looks[1:]:
                    lo = th.arena_layout(other)
                    diff |= {c for c in set(lo) | set(lay0) if lo.get(c) != lay0.get(c)}
            groups = []
            for b in sl:
                cells = {c: lay.get(c, 'minecraft:air') for c in diff if _in(c, b)}
                if cells:
                    groups.append(_span_lines(cells))
        assert 1 <= len(groups) <= MAX_SLICES, f'{aid}: look {look} has {len(groups)} slices'
        for g in groups:
            assert len(g) <= MAX_CMDS
            for cmd in g:
                if cmd.startswith('fill '):
                    t = cmd.split()
                    v = (abs(int(t[4]) - int(t[1])) + 1) * (abs(int(t[5]) - int(t[2])) + 1) * (abs(int(t[6]) - int(t[3])) + 1)
                    assert v <= MAX_FILL, f'{aid}: look {look} fill of {v} blocks'
        out_looks[look] = groups
    clear = [f'fill {b[0][0]} {b[0][1]} {b[0][2]} {b[1][0]} {b[1][1]} {b[1][2]} minecraft:air strict' for b in sl]
    return {'build': build, 'looks': out_looks, 'clear': clear}


def sweep_rows(a):
    """[(z, x0, x1)] rows of the cells with centre distance <= walk - 0.5 (the barrier sweep, cm.md 6.3)."""
    rows = {}
    rr = a['walk'] - 0.5
    for z in range(a['box']['z0'], a['box']['z1'] + 1):
        for x in range(a['box']['x0'], a['box']['x1'] + 1):
            if math.hypot(x + 0.5 - a['cx'], z + 0.5 - a['cz']) <= rr:
                rows.setdefault(z, []).append(x)
    return [(z, min(xs), max(xs)) for z, xs in sorted(rows.items())]


def write_chapter_arenas(out):
    """Every arenas{} entry: real sliced functions when its theme module exists, else the stub set (cm.md 6.3)."""
    real = []
    for aid, a in L.arenas(REG):
        if aid == 'plaza':
            continue
        P = f'mboss/arena/{aid}/'
        F = f'rlk:mboss/arena/{aid}/'
        ver, look0 = a['ver'], a['looks'][0]
        stamp0 = f'{aid}@{ver}:{look0}'
        if L.theme_module(a['theme']) is None:
            print(f'WARN theme {a["theme"]} missing: stub arena {aid}')
            out.write(P + 'ensure', [f'# STUB (theme module tools/mboss_arena_{a["theme"]}.py missing): nothing is built; the stamp says so.',
                                     f'data modify storage rlk:mboss built_{aid} set value "{aid}@0:stub"', 'return 1'])
            for fn in ('build', 'clear', 'done'):
                out.write(P + fn, [f'# STUB (theme module tools/mboss_arena_{a["theme"]}.py missing): no-op.'])
            # the dev view (ar/<aid>/test: fl_on + rebuild) builds nothing here, so its forceload goes at once outside a run
            out.write(P + 'rebuild', [f'# STUB (theme module tools/mboss_arena_{a["theme"]}.py missing): nothing is built; outside a run the',
                                      '# forceload the dev view added goes again.',
                                      f'execute unless score #active room matches 1 unless score #mbLive mb matches 1 run function rlk:mboss/ar/{aid}/fl_off'])
            out.write(P + 'sweep', [f'# STUB (theme module tools/mboss_arena_{a["theme"]}.py missing): no-op ({{y0,y1}} kept).',
                                    '$data modify storage rlk:mboss arsw set value {y0:$(y0),y1:$(y1)}'])
            continue
        real.append((aid, a))
        th = L.theme_module(a['theme'])
        (sx, sy, sz), sb = th.SENTINEL
        em = emit(aid)
        n = len(em['build'])
        others = a['looks'][1:]
        bx = a['box']
        for i, cmds in enumerate(em['build']):
            tail = [f'function {F}done with storage rlk:mboss arjob'] if i == n - 1 else []
            out.write(P + f's/{i}', [f'# GENERATED build slice {i + 1}/{n} of {aid} (in minecraft:overworld, the box loaded).'] + cmds + tail)
        out.write(P + 'ensure', [
            f'# 1 when no arena job runs, the box of {aid} is loaded, the stamp is "{stamp0}" and the sentinel is right.',
            '# Otherwise fail, after making sure a job runs: a wrong / missing version -> build; the right version in another',
            '# look -> the default look job; built but not loaded -> a verify job (waits for the chunks). While another',
            "# arena's job runs nothing starts. Run in minecraft:overworld.",
            'execute if score #mbArBuild mb matches 1.. run return fail',
            f'execute unless data storage rlk:mboss {{built_{aid}:"{stamp0}"}} run function {F}restore',
            f'execute unless data storage rlk:mboss {{built_{aid}:"{stamp0}"}} run return fail',
            f'execute unless function rlk:mboss/ar/{aid}/loaded run function {F}verify',
            'execute if score #mbArBuild mb matches 1.. run return fail',
            f'execute unless block {sx} {sy} {sz} {sb} run function {F}build',
            'execute if score #mbArBuild mb matches 1.. run return fail',
            'return 1'])
        out.write(P + 'restore', [f'# The stamp of {aid} is not the default look: the right version in another look -> the look job back to',
                                  f'# "{look0}"; anything else (no stamp, an old version, a stub) -> a full build.']
                  + [f'execute if data storage rlk:mboss {{built_{aid}:"{aid}@{ver}:{lk}"}} run return run function {F}look/{look0}' for lk in others]
                  + [f'function {F}build'])
        def start(kind, look, nsl):
            return [f'execute if score #mbArBuild mb matches 1.. run return fail',
                    f'data modify storage rlk:mboss arjob set value {{aid:"{aid}",kind:"{kind}",look:"{look}",i:0,n:{nsl},wait:0}}',
                    f'scoreboard players set #mbArBuild mb {nsl}',
                    'schedule function rlk:mboss/arena/job_tick 1t replace']
        out.write(P + 'build', [f'# Start a full build job of {aid} ({n} slices, one per tick; the stamp goes until done).']
                  + start('build', look0, n)[:1] + [f'data remove storage rlk:mboss built_{aid}'] + start('build', look0, n)[1:])
        out.write(P + 'rebuild', [f'# Dev / test: drop the stamp of {aid} and build it again (a running job of another arena blocks it).',
                                  f'execute if score #mbArBuild mb matches 1.. run return fail', f'data remove storage rlk:mboss built_{aid}',
                                  f'function {F}build'])
        out.write(P + 'verify', [f'# The stamp of {aid} is right but the box is not loaded: a 1-slice job that waits for the chunks, then checks',
                                 '# the sentinel (done -> stamp kept; wrong -> a full build).'] + start('verify', look0, 1))
        # outside a run and a fight (the dev view ar/<aid>/test) a finished job releases the forceload it needed; inside a
        # run the entrance prep's forceload stays for the fight (cb/won, mboss/cleanup, cb/remove release it)
        idle = 'unless score #active room matches 1 unless score #mbLive mb matches 1'
        out.write(P + 'vdone', [f'# Verify job of {aid}: the chunks are loaded. Outside a run, the forceload goes when nothing is rebuilt.',
                                'scoreboard players set #mbArBuild mb 0', 'data remove storage rlk:mboss arjob',
                                f'execute unless block {sx} {sy} {sz} {sb} run function {F}build',
                                f'execute if score #mbArBuild mb matches 0 {idle} run function rlk:mboss/ar/{aid}/fl_off'])
        out.write(P + 'clear', [f'# Air over the box of {aid} when it is loaded (room/remove -> cb/remove), and no stamp.',
                                f'execute if data storage rlk:mboss arjob{{aid:"{aid}"}} run function rlk:mboss/arena/abort',
                                f'data remove storage rlk:mboss built_{aid}',
                                f'execute unless function rlk:mboss/ar/{aid}/loaded run return fail'] + em['clear'] + ['return 1'])
        rows = sweep_rows(a)
        out.write(P + 'sweep', [f'# {{y0,y1}} (absolute y): barriers -> air in {len(rows)} row spans inside walk - 0.5 of {aid} (never a',
                                '# rectangle: blocks outside the disc are not touched). Only while the box is loaded.',
                                f'execute unless function rlk:mboss/ar/{aid}/loaded run return fail']
                  + [f'$fill {x0} $(y0) {z} {x1} $(y1) {z} minecraft:air replace minecraft:barrier' for z, x0, x1 in rows] + ['return 1'])
        out.write(P + 'done', [f'# (macro arjob) The last slice of a job of {aid}: the stamp of the look just built, the sentinel check (a wrong',
                               '# sentinel restarts one full build: #arRedo). Outside a run (the dev view) the forceload goes once it is built.',
                               'scoreboard players set #mbArBuild mb 0',
                               'data remove storage rlk:mboss arjob',
                               f'$data modify storage rlk:mboss built_{aid} set value "{aid}@{ver}:$(look)"',
                               'scoreboard players set #arOk mb 0',
                               f'execute if block {sx} {sy} {sz} {sb} run scoreboard players set #arOk mb 1',
                               f'execute if score #arOk mb matches 1 {idle} run function rlk:mboss/ar/{aid}/fl_off',
                               'execute if score #arOk mb matches 1 run return run scoreboard players set #arRedo mb 0',
                               f'data remove storage rlk:mboss built_{aid}',
                               'execute if score #arRedo mb matches 1 run return run scoreboard players set #arRedo mb 0',
                               'scoreboard players set #arRedo mb 1',
                               f'function {F}build'])
        for look, groups in em['looks'].items():
            m = len(groups)
            out.write(P + f'look/{look}', [f'# Start the look job "{look}" of {aid} ({m} slices; the stamp goes until done stamps "{aid}@{ver}:{look}").',
                                           'execute if score #mbArBuild mb matches 1.. run return fail',
                                           f'data remove storage rlk:mboss built_{aid}'] + start('look', look, m)[1:])
            for i, cmds in enumerate(groups):
                tail = [f'function {F}done with storage rlk:mboss arjob'] if i == m - 1 else []
                out.write(P + f'l/{look}/{i}', [f'# GENERATED look slice {i + 1}/{m} of {aid} -> {look}.'] + cmds + tail)
        # job tick of this arena: wait for the chunks (<= 200 t, then abort), else the next slice
        tick = [f'# @s = the server (arena/job_tick), in minecraft:overworld: one step of the running job of {aid}.',
                f'execute unless function rlk:mboss/ar/{aid}/loaded run return run function {F}wait',
                'data modify storage rlk:mboss arjob.wait set value 0',
                f'execute if data storage rlk:mboss arjob{{kind:"verify"}} run return run function {F}vdone',
                'execute store result score #arI mb run data get storage rlk:mboss arjob.i',
                'scoreboard players remove #mbArBuild mb 1',
                'execute store result storage rlk:mboss arjob.i int 1 run scoreboard players add #arI mb 1',
                'scoreboard players remove #arI mb 1']
        tick += [f'execute if data storage rlk:mboss arjob{{kind:"build"}} if score #arI mb matches {i} run function {F}s/{i}' for i in range(n)]
        for look, groups in em['looks'].items():
            tick += [f'execute if data storage rlk:mboss arjob{{kind:"look",look:"{look}"}} if score #arI mb matches {i} run function {F}l/{look}/{i}'
                     for i in range(len(groups))]
        out.write(P + 'tick', tick)
        out.write(P + 'wait', [f'# The box of {aid} is not loaded yet: wait (forceloaded chunks load within a few ticks); 200 t -> abort.',
                               'execute store result score #arW mb run data get storage rlk:mboss arjob.wait',
                               'scoreboard players add #arW mb 1',
                               'execute store result storage rlk:mboss arjob.wait int 1 run scoreboard players get #arW mb',
                               'execute if score #arW mb matches 200.. run function rlk:mboss/arena/abort'])
    out.write('mboss/arena/job_tick', ['# The one running arena job (rlk:mboss arjob, #mbArBuild = slices left): one step per tick, re-scheduled while',
                                       '# it runs (mboss/init re-arms it after /reload).',
                                       'execute unless score #mbArBuild mb matches 1.. run return run data remove storage rlk:mboss arjob']
              + [f'execute if data storage rlk:mboss arjob{{aid:"{aid}"}} in minecraft:overworld run function rlk:mboss/arena/{aid}/tick' for aid, _ in real]
              + ['execute unless data storage rlk:mboss arjob run scoreboard players set #mbArBuild mb 0',
                 'execute if score #mbArBuild mb matches 1.. run schedule function rlk:mboss/arena/job_tick 1t replace'])
    out.write('mboss/arena/abort', ['# Drop the running arena job (cb/remove, uninstall, a 200-t chunk wait): no job, the half-built arena loses its stamp.']
              + [f'execute if data storage rlk:mboss arjob{{aid:"{aid}"}} run data remove storage rlk:mboss built_{aid}' for aid, _ in real]
              + ['scoreboard players set #mbArBuild mb 0', 'data remove storage rlk:mboss arjob', 'schedule clear rlk:mboss/arena/job_tick'])
    out.write('mboss/arena/clear_all', ['# Every arena cleared (the plaza and every chapter arena; when loaded). Not called by the game files.',
                                        'function rlk:mboss/arena/clear']
              + [f'function rlk:mboss/arena/{aid}/clear' for aid, _ in L.arenas(REG) if aid != 'plaza'])
    return real


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
    real = write_chapter_arenas(out)
    removed = out.clean()
    n = len(body)
    print(f'mboss arena: {THEME}@{VER}, centre ({CX},{CY},{CZ}) r {RAD} walk {WALK}, {n} build commands, '
          f'{len(layout())} blocks, sentinel {sentinel()}; chapter arenas: '
          f'{", ".join(aid for aid, _ in real) or "none built"}; {removed} stale removed.')


if __name__ == '__main__':
    main()
