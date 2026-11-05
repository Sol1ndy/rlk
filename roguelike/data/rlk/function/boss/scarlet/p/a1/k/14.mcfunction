# A1 pattern tick 14
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~ run particle minecraft:dust{color:[0.79,0.49,0.87],scale:1.2} ~ ~ ~ 1.4 0.25 1.4 0 18 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.3 ~ run particle minecraft:sweep_attack ~ ~ ~ 1 0.1 1 0 2 force @a[tag=player]
execute at @s run playsound minecraft:entity.breeze.wind_burst hostile @a[tag=player] ~ ~ ~ 0.4 1.5 0.13
execute at @s run playsound minecraft:block.amethyst_block.resonate hostile @a[tag=player] ~ ~ ~ 0.5 1.7 0.17
