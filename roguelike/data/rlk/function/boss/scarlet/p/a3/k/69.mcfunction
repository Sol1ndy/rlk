# A3 pattern tick 69
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.5 0.7 0.5 0 20 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.6 0.2
execute at @s run playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.5 1 0.17
