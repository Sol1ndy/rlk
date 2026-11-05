# A9 pattern tick 8
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run particle minecraft:dust{color:[1.0,0.88,0.29],scale:1.6} ~ ~ ~ 0.5 0.6 0.5 0 30 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.0 ~ run particle minecraft:end_rod ~ ~ ~ 1.2 0.05 0.05 0 8 force @a[tag=player]
execute at @s run playsound minecraft:block.bell.use hostile @a[tag=player] ~ ~ ~ 0.6 1.5 0.2
execute at @s run playsound minecraft:block.beacon.power_select hostile @a[tag=player] ~ ~ ~ 0.5 1.9 0.17
