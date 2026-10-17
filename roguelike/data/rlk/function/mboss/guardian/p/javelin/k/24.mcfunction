# javelin clip tick 24
execute at @s rotated as @s rotated ~ 0 positioned ^-0.9 ^1.5 ^1.2 run particle minecraft:end_rod ~ ~ ~ 0.25 0.25 0.25 0.01 1 force @a[tag=player]
playsound minecraft:block.amethyst_block.chime hostile @a[tag=player] ~ ~ ~ 0.5 1.9 0.17
function rlk:mboss/guardian/p/javelin/lock
