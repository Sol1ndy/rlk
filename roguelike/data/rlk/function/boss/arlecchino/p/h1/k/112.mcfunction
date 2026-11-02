# H1 pattern tick 112
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.75 run particle minecraft:sweep_attack ~ ~ ~ 1.5 0.15 1.5 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.75 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.5 0.2 1.5 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.75 run particle minecraft:flame ~ ~ ~ 1.25 0.2 1.25 0.02 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.6 0.33
