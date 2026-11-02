# E1 pattern tick 92
execute at @s positioned ~ ~1.6 ~ run particle minecraft:flame ~ ~ ~ 1.89 0.1 1.89 0.03 30 force @a[tag=player]
execute at @s positioned ~ ~1.6 ~ run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 2.1 0.1 2.1 0 20 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.31 run particle minecraft:sweep_attack ~ ~ ~ 1.26 0.15 1.26 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.31 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.26 0.2 1.26 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.31 run particle minecraft:flame ~ ~ ~ 1.05 0.2 1.05 0.02 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
execute at @s run playsound minecraft:item.trident.riptide_1 hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
