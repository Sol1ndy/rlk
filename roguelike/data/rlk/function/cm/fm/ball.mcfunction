summon minecraft:item_display ~ ~2.2 ~ {Tags:["rlk_cmlink","rlk_cmfbh","rlk_cmnew2"],teleport_duration:2,billboard:"center",brightness:{sky:15,block:15},item:{id:"minecraft:fire_charge",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.75f,0.75f,0.75f]}}
scoreboard players operation @e[tag=rlk_cmnew2] cmId = #cid tmp
$scoreboard players set @e[tag=rlk_cmnew2] cmN $(n)
tag @e[tag=rlk_cmnew2] remove rlk_cmnew2
execute unless score #k89 snd matches 1 run function rlk:snd/f96
