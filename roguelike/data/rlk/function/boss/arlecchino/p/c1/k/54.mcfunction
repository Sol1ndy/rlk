# C1 pattern tick 54
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run particle minecraft:explosion ~ ~ ~ 0.9 0.1 0.9 0 2 force @a[tag=player]
execute at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.44 0.2 1.44 0 24 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.2 run particle minecraft:sweep_attack ~ ~ ~ 1.2 0.15 1.2 0 3 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.2 run particle minecraft:dust{color:[1.0,0.55,0.16],scale:1.4} ~ ~ ~ 1.2 0.2 1.2 0 14 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 rotated ~0 0 positioned ^ ^1 ^2.2 run particle minecraft:flame ~ ~ ~ 1 0.2 1 0.02 8 force @a[tag=player]
execute at @s run playsound minecraft:entity.generic.explode hostile @a[tag=player] ~ ~ ~ 0.9 1 0.3
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 0.6 0.2
