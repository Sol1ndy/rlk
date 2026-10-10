# 포탄을 포구에 숨겨 둠(크기 0). 대포병과 연결(rlk_cmlink) → 발사 전에 죽으면 함께 사라짐
summon minecraft:block_display ~ ~ ~ {Tags:["rlk_cmcbw","rlk_cmlink","rlk_cmpnew"],teleport_duration:1,block_state:{id:"minecraft:coal_block"},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]}}
scoreboard players operation @e[tag=rlk_cmpnew] cmId = #cid tmp
execute as @e[tag=rlk_cmpnew] run function rlk:cm/cn/arc
tag @e[tag=rlk_cmpnew] remove rlk_cmpnew
execute unless score #k91 snd matches 1 run function rlk:snd/f98
