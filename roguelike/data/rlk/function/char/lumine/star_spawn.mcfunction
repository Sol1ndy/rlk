# 혹한의 별: 12초 동안 플레이어 곁을 맴돌며 2초마다 얼음 결정 발사 (@s = 플레이어, at @s)
kill @e[tag=rlk_lstar]
summon minecraft:item_display ~ ~2.3 ~ {Tags:["rlk_lstar"],billboard:"center",teleport_duration:2,brightness:{sky:15,block:15},item:{id:"minecraft:nether_star",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.55f,0.55f,0.55f]}}
scoreboard players set @e[tag=rlk_lstar] life 240
scoreboard players set @e[tag=rlk_lstar] pcVal 0
execute unless score #k343 snd matches 1 run function rlk:snd/f406
