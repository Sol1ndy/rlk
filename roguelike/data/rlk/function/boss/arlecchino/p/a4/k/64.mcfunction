# A4 pattern tick 64
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^1.98 run particle minecraft:sweep_attack ~ ~ ~ 1.08 0.15 1.08 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^1.98 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.08 0.2 1.08 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^1.98 run particle minecraft:flame ~ ~ ~ 0.9 0.2 0.9 0.02 8 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.6 run particle minecraft:explosion ~ ~ ~ 0.55 0.1 0.55 0 2 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.6 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 0.88 0.2 0.88 0 24 force @a[tag=player]
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.7 1.2 0.23
execute at @s run playsound minecraft:block.anvil.land hostile @a[tag=player] ~ ~ ~ 0.4 0.6 0.13
