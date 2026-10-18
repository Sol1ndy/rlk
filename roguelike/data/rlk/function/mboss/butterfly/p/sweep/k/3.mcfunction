# sweep clock 3
function rlk:mboss/butterfly/rig/face/track
execute rotated as @s rotated ~ 0 positioned ^2.442 ^6.428 ^-1.424 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-2.442 ^6.428 ^-1.424 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
