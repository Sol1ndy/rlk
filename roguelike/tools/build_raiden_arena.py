"""Generate the plain, circular Narukami boss room and its entrance.

Run from any directory. Runtime function hooks are kept separately so generating
the arena cannot overwrite unrelated room system changes.
"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/rlk/function/room/raiden"
OUT.mkdir(parents=True, exist_ok=True)


def write(name, lines):
    (OUT / (name + ".mcfunction")).write_text("\n".join(lines) + "\n", encoding="utf-8")


def cell(x0, z0, x1, z1, entry=None):
    ex0, ez0, ex1, ez1 = entry or (x0 + 1, z0 + 1, x1, z1)
    return dict(x0=x0, z0=z0, x1=x1, z1=z1, ix0=x0 + 1, iz0=z0 + 1,
                ix1=x1 - 1, iz1=z1 - 1, ex0=ex0 * 100, ez0=ez0 * 100,
                ex1=ex1 * 100, ez1=ez1 * 100, sx0=x0 + 2, sz0=z0 + 2,
                sx1=x1 - 2, sz1=z1 - 2)


def zone(zone_id, kind, bounds, center, cells):
    x0, z0, x1, z1 = bounds
    cx, cz = center
    return dict(id=zone_id, kind=kind, boss_id="narukami", x0=x0, z0=z0,
                x1=x1, z1=z1, cx=cx, cz=cz, mn=1, mx=1,
                nc=len(cells), ncm=len(cells)-1, cells=cells, by=0, cy=201,
                sd=0, pits=[], fn="narukami")


# Room markers and map-entry bounds use existing native room fields. Four
# quadrants also keep every existing erase_cell fill comfortably under 32768.
arena_cells = [cell(-24, -24, -1, -1, (-23, -23, 0, 0)),
               cell(0, -24, 23, -1, (0, -23, 23, 0)),
               cell(-24, 0, -1, 23, (-23, 0, 0, 21)),
               cell(0, 0, 23, 23, (0, 0, 23, 21))]
foyer_cells = [cell(-6, 24, 5, 39, (-4, 26, 4, 37))]
layout = dict(
    n=2, boss_id="narukami",
    zones=[zone(1, 0, (-6, 24, 5, 39), (0, 32), foyer_cells),
           zone(2, 9, (-24, -24, 23, 23), (0, 0), arena_cells)],
    doors=[dict(a=1, b=2, x0=-2, x1=1, z0=23, z1=24, mx=0, mz=24,
                ya=0, yb=180, h=0, y0=201, y1=205, l0=206, l1=207,
                my=201, tx0=-2, tx1=1, tz0=24, tz1=24, tm=210)],
    spawn=dict(x=0, z=33, yaw=180), spot=dict(x=0, z=33),
    arena=dict(x=0, y=201, z=0, radius=23, safe_radius=21))

write("layout", [
    "# All stages currently use Narukami. The boss_id gates only this encounter's geometry.",
    "data modify storage rlk:room cur set value " + json.dumps(layout, separators=(",", ":")),
    '# Match the plain perimeter when native door functions rebuild their lintels.',
    'data modify storage rlk:room th.lb set value "minecraft:polished_blackstone"',
    'data modify storage rlk:room th.lb2 set value "minecraft:polished_blackstone"',
])

write("build", [
    '# @s = room zone marker. Fixed absolute geometry stays inside normal wipe bounds.',
    'execute if score @s zid matches 1 run function rlk:room/raiden/foyer',
    'execute if score @s zkind matches 9 run function rlk:room/raiden/arena',
])

write("foyer", [
    '# Plain entrance: no biome props, vegetation, raised terrain or floor motifs.',
    'fill -6 199 24 5 199 39 minecraft:polished_blackstone',
    'fill -6 200 24 5 200 39 minecraft:light_gray_concrete',
    'fill -6 201 24 5 230 39 minecraft:air strict',
    'fill -6 201 24 -6 207 39 minecraft:polished_blackstone',
    'fill 5 201 24 5 207 39 minecraft:polished_blackstone',
    'fill -6 201 39 5 207 39 minecraft:polished_blackstone',
    'fill -6 201 24 5 207 24 minecraft:polished_blackstone',
    'fill -5 218 25 4 218 38 minecraft:light[level=15]',
])


def row_spans(xs):
    if not xs:
        return []
    spans, start, prev = [], xs[0], xs[0]
    for x in xs[1:]:
        if x != prev + 1:
            spans.append((start, prev))
            start = x
        prev = x
    spans.append((start, prev))
    return spans


arena = [
    '# Circle centered on (0,201,0): outer radius 24, free walking radius 23.',
    '# Four sections avoid the command volume limit and share native room cleanup bounds.',
]
for c in arena_cells:
    arena.append(f'fill {c["x0"]} 201 {c["z0"]} {c["x1"]} 230 {c["z1"]} minecraft:air strict')

# Floor look (rd/plan.md D.3, footage B-08): the Shogun fights on a teal floor (prismarine, animated); the
# transformation turns it dark blue-violet (look_tenma) and the return / the death turn it back (look_shogun).
FLOOR_SHOGUN, FLOOR_TENMA = 'minecraft:prismarine', 'minecraft:blue_terracotta'
look = {'shogun': ['# Shogun floor look (teal), rows of the arena circle; called by normal_return and death/finish.'],
        'tenma': ['# Tenma floor look (dark blue-violet), rows of the arena circle; called by the transformation.']}
for z in range(-24, 24):
    # Use block centers for a symmetric circle around the integer marker location.
    floor = [x for x in range(-24, 24) if (x+.5)**2 + (z+.5)**2 <= 24**2]
    wall = [x for x in floor if (x+.5)**2 + (z+.5)**2 > 23**2]
    for x0, x1 in row_spans(floor):
        arena.append(f'fill {x0} 199 {z} {x1} 199 {z} minecraft:polished_blackstone')
        arena.append(f'fill {x0} 200 {z} {x1} 200 {z} {FLOOR_SHOGUN}')
        arena.append(f'fill {x0} 218 {z} {x1} 218 {z} minecraft:light[level=15]')
        look['tenma'].append(f'fill {x0} 200 {z} {x1} 200 {z} {FLOOR_TENMA} replace {FLOOR_SHOGUN}')
        look['shogun'].append(f'fill {x0} 200 {z} {x1} 200 {z} {FLOOR_SHOGUN} replace {FLOOR_TENMA}')
    for x0, x1 in row_spans(wall):
        arena.append(f'fill {x0} 201 {z} {x1} 207 {z} minecraft:polished_blackstone')

arena += [
    '# The entry is cut/opened/sealed by native room/door_* after construction.',
    'kill @e[tag=rlk_raiden_arena]',
    'summon minecraft:marker 0 201 0 {Tags:["rlk_room","rlk_raiden_arena"],data:{boss_id:"narukami",radius:23,safe_radius:21}}',
]
write("arena", arena)
write("look_shogun", look['shogun'])
write("look_tenma", look['tenma'])
print(f"Generated Narukami arena: radius 23, center (0,201,0), {len(arena_cells)} cleanup cells.")
