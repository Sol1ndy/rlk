# B3 pattern tick 100
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.1 ^1.76 run particle minecraft:sweep_attack ~ ~ ~ 0.96 0.15 0.96 0 4 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.0 ^1.76 run particle minecraft:flame ~ ~ ~ 0.96 0.2 0.96 0.02 16 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2 run particle minecraft:explosion ~ ~ ~ 0.2 0.1 0.2 0 1 force @a[tag=player]
playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
function rlk:boss/tachy/el/edge
