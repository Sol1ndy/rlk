# E1 pattern tick 76
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.86 run particle minecraft:sweep_attack ~ ~ ~ 1.56 0.15 1.56 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.86 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.56 0.2 1.56 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.86 run particle minecraft:flame ~ ~ ~ 1.3 0.2 1.3 0.02 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
