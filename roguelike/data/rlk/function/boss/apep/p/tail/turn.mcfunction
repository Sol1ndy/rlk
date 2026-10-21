# @s = body (t1-8): turn the tail root toward the player (the back to it) by <= 5 deg/t.
execute store result score #apq5Y mb run data get entity @s Rotation[0] 100
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p5t]
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ~ 201 ~ run summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_pat","rlk_mb_ap_p5","rlk_mb_ap_p5t"]}
execute at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 positioned ~ 201 ~ run tp @e[type=minecraft:marker,tag=rlk_mb_ap_p5t,limit=1] ~ ~ ~ ~ 0
execute store result score #apq5D mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_ap_p5t,limit=1] Rotation[0] 100
kill @e[type=minecraft:marker,tag=rlk_mb_ap_p5t]
scoreboard players operation #apq5D mb -= #apq5Y mb
scoreboard players add #apq5D mb 90000
scoreboard players operation #apq5D mb %= #c36000 mb
scoreboard players remove #apq5D mb 18000
scoreboard players set #apq5M mb 500
scoreboard players operation #apq5D mb < #apq5M mb
scoreboard players set #apq5M mb -500
scoreboard players operation #apq5D mb > #apq5M mb
scoreboard players operation #apq5Y mb += #apq5D mb
execute store result entity @s Rotation[0] float 0.01 run scoreboard players get #apq5Y mb
# TODO(I2) requests/ap-p1.md RP1-1: the clip's yaw schedule pins Rotation to #apYaw0 every tick (core yaw/tick);
# the pre-swing turn moves that start with it (an api helper would own this line).
scoreboard players operation #apYaw0 mb = #apq5Y mb
