# As the boss at its feet: #rdSgRear 1 when the player is within 8 b and more than 120 deg off her facing.
scoreboard players set #rdSgRear rd 0
execute unless entity @e[tag=rlk_body,distance=..8,limit=1] run return 0
execute store result score #rdSgY0 rd run data get entity @s Rotation[0] 100
summon minecraft:marker ~ ~ ~ {Tags:["rlk_rd_sgface","rlk_rd_tmp","rlk_raiden_aux","rlk_room"]}
execute as @e[tag=rlk_rd_sgface,limit=1] at @s facing entity @e[tag=rlk_body,limit=1] feet run tp @s ~ ~ ~ ~ 0
execute store result score #rdSgY1 rd run data get entity @e[tag=rlk_rd_sgface,limit=1] Rotation[0] 100
kill @e[tag=rlk_rd_sgface]
scoreboard players operation #rdSgY1 rd -= #rdSgY0 rd
execute if score #rdSgY1 rd matches 18000.. run scoreboard players remove #rdSgY1 rd 36000
execute if score #rdSgY1 rd matches ..-18001 run scoreboard players add #rdSgY1 rd 36000
execute if score #rdSgY1 rd matches 18000.. run scoreboard players remove #rdSgY1 rd 36000
execute if score #rdSgY1 rd matches ..-18001 run scoreboard players add #rdSgY1 rd 36000
execute if score #rdSgY1 rd matches 12001.. run scoreboard players set #rdSgRear rd 1
execute if score #rdSgY1 rd matches ..-12001 run scoreboard players set #rdSgRear rd 1
