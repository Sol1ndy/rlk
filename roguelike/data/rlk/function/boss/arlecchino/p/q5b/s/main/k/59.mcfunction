# Q5B stage main tick 59
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^3.03 run particle minecraft:sweep_attack ~ ~ ~ 1.65 0.15 1.65 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^3.03 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.65 0.2 1.65 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^3.03 run particle minecraft:flame ~ ~ ~ 1.38 0.2 1.38 0.02 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
