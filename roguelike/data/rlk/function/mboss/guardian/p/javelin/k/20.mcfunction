# javelin clip tick 20
function rlk:mboss/guardian/rig/face/track
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.25 0.25 0.25 0.01 1 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.7 0.17
