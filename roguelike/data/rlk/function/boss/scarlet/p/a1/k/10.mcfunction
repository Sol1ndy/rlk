# A1 pattern tick 10
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.85 ^1.2 run particle minecraft:dust{color:[0.88,0.25,0.62],scale:1.2} ~ ~ ~ 0.3 0.8 0.3 0 14 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
