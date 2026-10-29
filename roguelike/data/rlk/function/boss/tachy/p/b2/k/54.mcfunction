# B2 pattern tick 54
execute at @s rotated as @s rotated ~ 0 positioned ^ ^1.1 ^1.76 run particle minecraft:sweep_attack ~ ~ ~ 0.96 0.15 0.96 0 4 force @a[tag=player]
execute if score #el tk matches 1 at @s rotated as @s rotated ~ 0 positioned ^ ^1.0 ^1.76 run particle minecraft:flame ~ ~ ~ 0.96 0.2 0.96 0.02 16 force @a[tag=player]
execute if score #el tk matches 3 at @s rotated as @s rotated ~ 0 positioned ^ ^1.0 ^1.76 run particle minecraft:electric_spark ~ ~ ~ 0.96 0.2 0.96 0.02 16 force @a[tag=player]
playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.8 1 0.27
