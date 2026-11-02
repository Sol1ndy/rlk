# Q2 stage main tick 34
execute at @s run playsound minecraft:entity.blaze.shoot hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:entity.phantom.swoop hostile @a[tag=player] ~ ~ ~ 0.5 1.6 0.17
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1 ~ run particle minecraft:flame ~ ~ ~ 0.4 0.5 0.4 0.06 16 force @a[tag=player]
