# 교활한 통수 (whip, id 7) - start (#azPT 0; tail_whip_<side> by #azSide; the core drives the yaw schedule). No decal
scoreboard players operation #aq7S mb = #azSide mb
execute unless score #aq7S mb matches -1 run scoreboard players set #aq7S mb 1
kill @e[tag=rlk_mb_az_p7m]
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p7","rlk_mb_az_p7m","rlk_mb_az_p7f"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p7f,limit=1] run tp @s ~ ~ ~ ~ 0
execute store result score #aq7Y mb run data get entity @s Rotation[0]
function rlk:mboss/azhdaha/fx/snd/whip_raise
