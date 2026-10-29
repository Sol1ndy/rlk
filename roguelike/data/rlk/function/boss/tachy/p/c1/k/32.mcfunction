# C1 pattern tick 32
execute if score #el tk matches 1 at @s run particle minecraft:flame ~ ~1 ~ 1.89 0.1 1.89 0.03 40 force @a[tag=player]
execute if score #el tk matches 3 at @s run particle minecraft:electric_spark ~ ~1 ~ 1.89 0.1 1.89 0.03 40 force @a[tag=player]
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
playsound minecraft:entity.iron_golem.attack hostile @a[tag=player] ~ ~ ~ 0.5 1.2 0.17
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.2 ^2.4 run particle minecraft:explosion ~ ~ ~ 0.2 0.1 0.2 0 1 force @a[tag=player]
