# C1 pattern tick 8
execute at @s positioned ~ ~9 ~ run function rlk:mboss/mv/glide {t:10}
execute at @s rotated as @s rotated ~ 0 positioned ~ ~0.3 ~ run particle minecraft:flame ~ ~ ~ 0.6 0.3 0.6 0.05 20 force @a[tag=player]
execute at @s run playsound minecraft:entity.ender_dragon.flap hostile @a[tag=player] ~ ~ ~ 0.7 1.4 0.23
execute at @s run playsound minecraft:item.firecharge.use hostile @a[tag=player] ~ ~ ~ 0.6 0.8 0.2
