# A3 pattern tick 30
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.4 0.25 1.4 0 18 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:sweep_attack ~ ~ ~ 1 0.1 1 0 2 force @a[tag=player]
execute at @s run playsound minecraft:entity.player.attack.sweep hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.2
