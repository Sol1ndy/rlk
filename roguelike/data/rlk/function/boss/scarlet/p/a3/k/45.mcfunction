# A3 pattern tick 45
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.15 ^1.4 run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.2 1 0.2 0 20 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.4 0.2
