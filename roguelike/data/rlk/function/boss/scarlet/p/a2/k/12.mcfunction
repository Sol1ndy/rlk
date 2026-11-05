# A2 pattern tick 12
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.26 0.25 1.26 0 18 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~ run particle minecraft:sweep_attack ~ ~ ~ 0.9 0.1 0.9 0 2 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.7 1.5 0.23
