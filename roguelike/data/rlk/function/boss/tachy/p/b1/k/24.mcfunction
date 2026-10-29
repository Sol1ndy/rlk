# B1 pattern tick 24
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.1 ^2.09 run particle minecraft:sweep_attack ~ ~ ~ 1.14 0.15 1.14 0 4 force @a[tag=player]
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^1.0 ^2.09 run particle minecraft:flame ~ ~ ~ 1.14 0.2 1.14 0.02 16 force @a[tag=player]
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ^ ^1.0 ^2.09 run particle minecraft:electric_spark ~ ~ ~ 1.14 0.2 1.14 0.02 16 force @a[tag=player]
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
