"""Build Narukami's yaw-locked ground warnings and matching hit volumes.

Runtime: as an entity at a ground point, call hazard/create with
{shape:1,tell:24,damage:12,life:32}. Root ticks rlk_rd_hazard markers.
The only damage API is boss/raiden/hurt. Display meshes never change terrain.
"""
from pathlib import Path
import math
from build_raiden_fx_textures import RING_END, RING_FRAMES

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data/rlk/function/boss/raiden/hazard"
OUT.mkdir(parents=True, exist_ok=True)


def write(name, lines):
    path = OUT / (name + ".mcfunction")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def line(x0, z0, x1, z1, spacing=.8):
    count = max(1, math.ceil(math.hypot(x1-x0, z1-z0) / spacing))
    return [(x0 + (x1-x0)*i/count, z0 + (z1-z0)*i/count) for i in range(count+1)]


def arc(radius, start, end, spacing=.75):
    count = max(1, math.ceil(math.radians(end-start)*radius/spacing))
    return [(radius*math.sin(math.radians(start+(end-start)*i/count)),
             radius*math.cos(math.radians(start+(end-start)*i/count))) for i in range(count+1)]


def disk(radius):
    return arc(radius, -180, 180)


def sector(radius, half_angle):
    x, z = radius*math.sin(math.radians(half_angle)), radius*math.cos(math.radians(half_angle))
    return line(0, 0, -x, z) + arc(radius, -half_angle, half_angle) + line(x, z, 0, 0)


def rectangle(length, width):
    h = width/2
    return line(-h, 0, -h, length) + line(-h, length, h, length) + line(h, length, h, 0) + line(h, 0, -h, 0)


def rotate(points, angle):
    s, c = math.sin(math.radians(angle)), math.cos(math.radians(angle))
    return [(x*c+z*s, z*c-x*s) for x, z in points]


def particles(points, strike=False, height=.08):
    # Unique positions avoid double-bright corners and duplicate origins.
    points = sorted({(round(x, 3), round(z, 3)) for x, z in points})
    color = "[0.93f,0.25f,0.90f]" if not strike else "[0.91f,0.87f,1.0f]"
    size = "0.85f" if not strike else "1.25f"
    return [f'particle minecraft:dust{{color:{color},scale:{size}}} ^{x:.3f} ^{height:.3f} ^{z:.3f} 0 0 0 0 1 force' for x, z in points]


descriptions = {
    1: "Forward sector radius6, 120 degrees", 2: "Thrust length12, width2.2",
    3: "Target disk radius3", 4: "Armored sector radius12, 140 degrees",
    5: "Great cleave length20, width3.6", 6: "Hand slam disk radius5",
    7: "Hand clap length8, width8", 8: "Omni disk radius6",
    9: "Five bolts length18, width0.9, yaw -40/-20/0/20/40",
    10: "Horizontal wave length18, width7",
    11: f"Jumpable expanding annulus radius2 to{RING_END} over{RING_FRAMES}ticks, half-width0.7",
    12: "Orb disk radius12",
    13: "Illusion sword wave length22, width2.4",
    14: "Calamity disk radius19 (몽상의 일심)",
}
outlines = {
    1: sector(6, 60), 2: rectangle(12, 2.2), 3: disk(3),
    4: sector(12, 70), 5: rectangle(20, 3.6), 6: disk(5),
    7: rectangle(8, 8), 8: disk(6),
    9: sum((rotate(rectangle(18, .9), a) for a in (-40, -20, 0, 20, 40)), []),
    10: rectangle(18, 7), 11: disk(1.3) + disk(2.7), 12: disk(12),
    13: rectangle(22, 2.4), 14: disk(19),
}

for shape, outline in outlines.items():
    write(f"warning/s{shape}", ["# " + descriptions[shape]] + particles(outline))
    if shape == 11:
        continue
    fill = list(outline)
    if shape in (1, 4):
        radius, angle = (6, 60) if shape == 1 else (12, 70)
        fill += arc(radius*.4, -angle, angle, 1) + arc(radius*.7, -angle, angle, 1)
    elif shape in (3, 6, 8, 12, 14):
        radius = {3: 3, 6: 5, 8: 6, 12: 12, 14: 19}[shape]
        fill += disk(radius*.5)
    elif shape == 9:
        fill += sum((rotate(line(0, 0, 0, 18, 1), a) for a in (-40, -20, 0, 20, 40)), [])
    else:
        length = {2: 12, 5: 20, 7: 8, 10: 18, 13: 22}[shape]
        fill += line(0, 0, 0, length, .6)
    write(f"strike/s{shape}", ["# " + descriptions[shape]] + particles(fill, True, .16))

for i in range(RING_FRAMES):
    radius = 2 + (RING_END-2)*i/(RING_FRAMES-1)
    # Exact same radii are used for runtime damage. Two clear rims enclose the
    # dangerous band; its center is deliberately not an invisible hit area.
    write(f"ring/f{i:02}", [f"# Active wave radius {radius:.4f}, band +/-0.7."] +
          particles(disk(radius-.7) + disk(radius+.7), True, .22))

write("create", [
    '# Called as the boss/aim marker at floor height. Pitch is flattened, yaw frozen.',
    'summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_hazard","rlk_raiden_aux","rlk_room","rlk_rd_hnew"]}',
    'data modify entity @e[tag=rlk_rd_hnew,limit=1] Rotation set from entity @s Rotation',
    'data modify entity @e[tag=rlk_rd_hnew,limit=1] Rotation[1] set value 0f',
    '$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdShape $(shape)',
    '$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdWind $(tell)',
    '$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdDamage $(damage)',
    '$scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHLife $(life)',
    '# World ticks newly spawned hazards in the creation frame: -1 -> 0.',
    'scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHAge -1',
    'scoreboard players set @e[tag=rlk_rd_hnew,limit=1] rdHHit 0',
    'scoreboard players set @e[tag=rlk_rd_hnew,limit=1] mlv 1',
    'execute if entity @e[tag=rlk_raiden,limit=1] run scoreboard players operation @e[tag=rlk_rd_hnew,limit=1] mlv = @e[tag=rlk_raiden,limit=1] mlv',
    'execute as @e[tag=rlk_rd_hnew,limit=1] at @s rotated as @s run function rlk:boss/raiden/hazard/init',
    'tag @e[tag=rlk_rd_hnew] remove rlk_rd_hnew',
])

write("init", [
    '# Keep every telegraph and strike alive, even with a too-short caller life.',
    'scoreboard players set #rdOne rd 1',
    'scoreboard players operation @s rdWind > #rdOne rd',
    'scoreboard players operation #rdMinLife rd = @s rdWind',
    'scoreboard players add #rdMinLife rd 10',
    'execute if score @s rdShape matches 11 run scoreboard players add #rdMinLife rd 24',
    'scoreboard players operation @s rdHLife > #rdMinLife rd',
    '# Cache the local-forward vector without trigonometric runtime functions.',
    'execute positioned ^ ^ ^1 run summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_haxis","rlk_raiden_aux","rlk_room"]}',
    'execute store result score #rdOX rd run data get entity @s Pos[0] 1000',
    'execute store result score #rdOZ rd run data get entity @s Pos[2] 1000',
    'execute store result score @s rdFX run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[0] 1000',
    'execute store result score @s rdFZ run data get entity @e[tag=rlk_rd_haxis,limit=1] Pos[2] 1000',
    'scoreboard players operation @s rdFX -= #rdOX rd',
    'scoreboard players operation @s rdFZ -= #rdOZ rd',
    'kill @e[tag=rlk_rd_haxis]',
    'function rlk:boss/raiden/hazard/warning',
])

write("tick", [
    '# Root only needs to select the marker; position and rotation belong to it.',
    'execute at @s rotated as @s run function rlk:boss/raiden/hazard/tick_at',
])
write("tick_at", [
    '# Advance this hazard at its fixed origin and frozen yaw.',
    'scoreboard players add @s rdHAge 1',
    'execute if score @s rdHAge >= @s rdHLife run return run kill @s',
    'scoreboard players operation #rdMod rd = @s rdHAge',
    'scoreboard players set #rdFour rd 4',
    'scoreboard players operation #rdMod rd %= #rdFour rd',
    'execute if score @s rdHAge matches 1.. if score @s rdHAge < @s rdWind if score #rdMod rd matches 0 rotated as @s run function rlk:boss/raiden/hazard/warning',
    'execute unless score @s rdShape matches 11 if score @s rdHAge = @s rdWind rotated as @s run function rlk:boss/raiden/hazard/strike',
    'execute if score @s rdShape matches 11 if score @s rdHAge >= @s rdWind rotated as @s run function rlk:boss/raiden/hazard/ring_tick',
])
write("warning", [f'execute if score @s rdShape matches {s} run function rlk:boss/raiden/hazard/warning/s{s}' for s in descriptions])
write("strike", [f'execute if score @s rdShape matches {s} run function rlk:boss/raiden/hazard/strike/s{s}' for s in descriptions if s != 11] + [
    'function rlk:boss/raiden/hazard/hit',
])

write("ring_tick", [
    'scoreboard players operation #rdElapsed rd = @s rdHAge',
    'scoreboard players operation #rdElapsed rd -= @s rdWind',
    f'execute unless score #rdElapsed rd matches 0..{RING_FRAMES-1} run return 0',
    'scoreboard players operation #rdMod rd = #rdElapsed rd',
    'scoreboard players set #rdTwo rd 2',
    'scoreboard players operation #rdMod rd %= #rdTwo rd',
    'execute if score #rdMod rd matches 0 run function rlk:boss/raiden/hazard/ring_draw',
    f'execute if score #rdElapsed rd matches {RING_FRAMES-1} run function rlk:boss/raiden/hazard/ring_draw',
    'execute unless score @s rdHHit matches 1 run function rlk:boss/raiden/hazard/hit',
])
write("ring_draw", [f'execute if score #rdElapsed rd matches {i} run function rlk:boss/raiden/hazard/ring/f{i:02}' for i in range(RING_FRAMES)])

write("hit", [
    '# Use body feet, not the displaced third-person spectator camera.',
    'scoreboard players set #rdHit rd 0',
    f'execute unless entity @e[tag=rlk_body,distance=..{RING_END+2},limit=1] run return 0',
    'execute store result score #rdDY rd run data get entity @e[tag=rlk_body,limit=1] Pos[1] 1000',
    'execute store result score #rdOY rd run data get entity @s Pos[1] 1000',
    'scoreboard players operation #rdDY rd -= #rdOY rd',
    'execute unless score #rdDY rd matches -500..3500 run return 0',
    'execute if score @s rdShape matches 11 unless score #rdDY rd matches -500..750 run return 0',
    'execute store result score #rdDX rd run data get entity @e[tag=rlk_body,limit=1] Pos[0] 1000',
    'execute store result score #rdDZ rd run data get entity @e[tag=rlk_body,limit=1] Pos[2] 1000',
    'execute store result score #rdOX rd run data get entity @s Pos[0] 1000',
    'execute store result score #rdOZ rd run data get entity @s Pos[2] 1000',
    'scoreboard players operation #rdDX rd -= #rdOX rd',
    'scoreboard players operation #rdDZ rd -= #rdOZ rd',
    'scoreboard players set #rdScale rd 1000',
    f'# Distance squared stays below {(RING_END+2)**2} million after the {RING_END+2}-block broad phase.',
    'scoreboard players operation #rdR2 rd = #rdDX rd',
    'scoreboard players operation #rdR2 rd *= #rdDX rd',
    'scoreboard players operation #rdT rd = #rdDZ rd',
    'scoreboard players operation #rdT rd *= #rdDZ rd',
    'scoreboard players operation #rdR2 rd += #rdT rd',
    '# Project onto frozen local forward and left axes (milliblocks).',
    'scoreboard players operation #rdFwd rd = #rdDX rd',
    'scoreboard players operation #rdFwd rd *= @s rdFX',
    'scoreboard players operation #rdT rd = #rdDZ rd',
    'scoreboard players operation #rdT rd *= @s rdFZ',
    'scoreboard players operation #rdFwd rd += #rdT rd',
    'scoreboard players operation #rdFwd rd /= #rdScale rd',
    'scoreboard players operation #rdSide rd = #rdDX rd',
    'scoreboard players operation #rdSide rd *= @s rdFZ',
    'scoreboard players operation #rdT rd = #rdDZ rd',
    'scoreboard players operation #rdT rd *= @s rdFX',
    'scoreboard players operation #rdSide rd -= #rdT rd',
    'scoreboard players operation #rdSide rd /= #rdScale rd',
    'scoreboard players operation #rdAbsSide rd = #rdSide rd',
    'scoreboard players set #rdNeg rd -1',
    'execute if score #rdAbsSide rd matches ..-1 run scoreboard players operation #rdAbsSide rd *= #rdNeg rd',
] + [f'execute if score @s rdShape matches {s} run function rlk:boss/raiden/hazard/hit/s{s}' for s in descriptions] + [
    'execute unless score #rdHit rd matches 1 run return 0',
    'scoreboard players set @s rdHHit 1',
    'scoreboard players operation #cmDmg tmp = @s rdDamage',
    'scoreboard players operation #cmLv tmp = @s mlv',
    'scoreboard players set #cmEl tmp 3',
    'function rlk:boss/raiden/hurt',
])

for s, radius, angle in ((1, 6, 60), (4, 12, 70)):
    tangent = round(math.tan(math.radians(angle))*1000)
    write(f"hit/s{s}", [
        f'# {descriptions[s]} (radius plus analytic yaw-sector bounds).',
        f'execute unless score #rdR2 rd matches ..{radius*radius*1000000} run return 0',
        'execute unless score #rdFwd rd matches 0.. run return 0',
        'scoreboard players operation #rdLimit rd = #rdFwd rd',
        f'scoreboard players set #rdTan rd {tangent}',
        'scoreboard players operation #rdLimit rd *= #rdTan rd',
        'scoreboard players operation #rdLimit rd /= #rdScale rd',
        'execute if score #rdAbsSide rd <= #rdLimit rd run scoreboard players set #rdHit rd 1',
    ])

for s, length, halfwidth in ((2, 12, 1100), (5, 20, 1800), (7, 8, 4000), (10, 18, 3500), (13, 22, 1200)):
    write(f"hit/s{s}", [
        '# ' + descriptions[s],
        f'execute if score #rdFwd rd matches 0..{length*1000} if score #rdAbsSide rd matches ..{halfwidth} run scoreboard players set #rdHit rd 1',
    ])
for s, radius in ((3, 3), (6, 5), (8, 6), (12, 12), (14, 19)):
    write(f"hit/s{s}", ['# ' + descriptions[s], f'execute if score #rdR2 rd matches ..{radius*radius*1000000} run scoreboard players set #rdHit rd 1'])

fan = ['# ' + descriptions[9]]
for a in (-40, -20, 0, 20, 40):
    c, s = round(math.cos(math.radians(a))*1000), round(math.sin(math.radians(a))*1000)
    fan += [f'scoreboard players set #rdCos rd {c}', f'scoreboard players set #rdSin rd {s}',
            'function rlk:boss/raiden/hazard/fan_ray']
write('hit/s9', fan)
write('fan_ray', [
    'scoreboard players operation #rdRayF rd = #rdFwd rd',
    'scoreboard players operation #rdRayF rd *= #rdCos rd',
    'scoreboard players operation #rdT rd = #rdSide rd',
    'scoreboard players operation #rdT rd *= #rdSin rd',
    'scoreboard players operation #rdRayF rd += #rdT rd',
    'scoreboard players operation #rdRayF rd /= #rdScale rd',
    'execute unless score #rdRayF rd matches 0..18000 run return 0',
    'scoreboard players operation #rdRayS rd = #rdSide rd',
    'scoreboard players operation #rdRayS rd *= #rdCos rd',
    'scoreboard players operation #rdT rd = #rdFwd rd',
    'scoreboard players operation #rdT rd *= #rdSin rd',
    'scoreboard players operation #rdRayS rd -= #rdT rd',
    'scoreboard players operation #rdRayS rd /= #rdScale rd',
    'execute if score #rdRayS rd matches -450..450 run scoreboard players set #rdHit rd 1',
])
write('hit/s11', [
    '# Jumpable wave: feet more than0.75 above the ground passed the early height gate.',
    'execute if score @s rdHHit matches 1 run return 0',
    'scoreboard players operation #rdElapsed rd = @s rdHAge',
    'scoreboard players operation #rdElapsed rd -= @s rdWind',
    f'execute unless score #rdElapsed rd matches 0..{RING_FRAMES-1} run return 0',
    'scoreboard players operation #rdRadius rd = #rdElapsed rd',
    f'scoreboard players set #rdSpan rd {(RING_END-2)*1000}',
    'scoreboard players operation #rdRadius rd *= #rdSpan rd',
    f'scoreboard players set #rdSteps rd {RING_FRAMES-1}',
    'scoreboard players operation #rdRadius rd /= #rdSteps rd',
    'scoreboard players add #rdRadius rd 2000',
    'scoreboard players operation #rdInner rd = #rdRadius rd',
    'scoreboard players remove #rdInner rd 700',
    'scoreboard players operation #rdInner rd *= #rdInner rd',
    'scoreboard players operation #rdOuter rd = #rdRadius rd',
    'scoreboard players add #rdOuter rd 700',
    'scoreboard players operation #rdOuter rd *= #rdOuter rd',
    'execute if score #rdR2 rd >= #rdInner rd if score #rdR2 rd <= #rdOuter rd run scoreboard players set #rdHit rd 1',
])

from build_raiden_hazard_vfx import build as build_display_vfx
build_display_vfx(ROOT, OUT)
print(f"Generated {len(descriptions)} hazard shapes, exact floor-aligned hit areas, {RING_FRAMES} expanding-wave frames.")
