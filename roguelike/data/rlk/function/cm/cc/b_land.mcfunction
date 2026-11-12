particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.7 0.3 0.1 30
particle minecraft:witch ~ ~1 ~ 0.3 0.6 0.3 0 10
tp @s @e[tag=rlk_c2cur,limit=1]
execute at @s run particle minecraft:reverse_portal ~ ~1 ~ 0.3 0.7 0.3 0.1 30
execute at @s run playsound minecraft:entity.enderman.teleport master @a ~ ~ ~ 1 1.3
# dazed after the blink: 20 t, no cast, staggerable (the punish window)
scoreboard players set @s cmS 4
scoreboard players set @s cmT 20
scoreboard players set @s cmCd2 100
tag @s remove rlk_cmch
