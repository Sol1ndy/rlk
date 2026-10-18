# sweep clock 9
function rlk:mboss/butterfly/rig_stub/face/track
execute rotated as @s rotated ~ 0 positioned ^3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^-3.13 ^5.99 ^-1.33 run particle minecraft:flame ~ ~ ~ 0.2 0.2 0.2 0.01 2 force @a[tag=player]
