# 꼬리찍기 (tailslam, id 8) - start (#azPT 0; tail_slam). Pre-turn <= 15 deg (t1-10) so the rear axis points at the player
kill @e[tag=rlk_mb_az_p8m]
execute store result score #aq8A mb run data get entity @s Rotation[0] 100
summon minecraft:marker ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_az_pat","rlk_mb_az_p8","rlk_mb_az_p8m","rlk_mb_az_p8y"]}
execute as @e[type=minecraft:marker,tag=rlk_mb_az_p8y,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet rotated ~180 0 run tp @s ~ ~ ~ ~ 0
execute store result score #aq8D mb run data get entity @e[type=minecraft:marker,tag=rlk_mb_az_p8y,limit=1] Rotation[0] 100
kill @e[tag=rlk_mb_az_p8y]
scoreboard players operation #aq8D mb -= #aq8A mb
execute if score #aq8D mb matches 18001.. run scoreboard players remove #aq8D mb 36000
execute if score #aq8D mb matches ..-18001 run scoreboard players add #aq8D mb 36000
execute if score #aq8D mb matches 18001.. run scoreboard players remove #aq8D mb 36000
execute if score #aq8D mb matches ..-18001 run scoreboard players add #aq8D mb 36000
execute if score #aq8D mb matches 1501.. run scoreboard players set #aq8D mb 1500
execute if score #aq8D mb matches ..-1501 run scoreboard players set #aq8D mb -1500
scoreboard players operation #aq8D mb /= #azK10 mb
function rlk:mboss/azhdaha/fx/snd/tslam_raise
