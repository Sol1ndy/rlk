# Q3 stage cut tick 30
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.48 run particle minecraft:sweep_attack ~ ~ ~ 1.35 0.15 1.35 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.48 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.35 0.2 1.35 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.48 run particle minecraft:flame ~ ~ ~ 1.12 0.2 1.12 0.02 8 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.48 run particle minecraft:sweep_attack ~ ~ ~ 1.35 0.15 1.35 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.48 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.35 0.2 1.35 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.48 run particle minecraft:flame ~ ~ ~ 1.12 0.2 1.12 0.02 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 1 0.7 0.33
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.5 0.9 0.17
