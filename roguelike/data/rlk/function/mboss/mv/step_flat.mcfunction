# {spd} (blocks per call, a decimal: L.step_flat; cm.md 13.12) as @s = a ground walker (an aux husk, a marker), rotated =
# its heading (the caller faces the target: execute as <e> at @s facing entity <target> feet run function
# rlk:mboss/mv/step_flat {spd:0.3}): turns to the heading (yaw only), steps forward, stands on the fight arena's floor
# (the y of its rlk_mb_arena marker), is pulled inside walk - 0.7 (ar/clampw). No collision test: the arena floor is flat.
$execute rotated ~ 0 positioned ^ ^ ^$(spd) run tp @s ~ ~ ~ ~ 0
execute store result entity @s Pos[1] double 0.001 run data get entity @e[type=minecraft:marker,tag=rlk_mb_arena,limit=1] Pos[1] 1000
function rlk:mboss/ar/clampw
