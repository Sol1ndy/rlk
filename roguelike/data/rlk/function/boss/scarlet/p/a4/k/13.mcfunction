# A4 pattern tick 13
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 0.4 0.6 0.4 0 16 force @a[tag=player]
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.5 1.4 0.17
