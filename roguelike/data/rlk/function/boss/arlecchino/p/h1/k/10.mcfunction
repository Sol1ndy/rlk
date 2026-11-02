# H1 pattern tick 10
execute at @s run playsound minecraft:entity.spider.ambient hostile @a[tag=player] ~ ~ ~ 0.5 0.6 0.17
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.5 ~ run particle minecraft:white_ash ~ ~ ~ 1.5 0.2 1.5 0 30 force @a[tag=player]
