kill @e[tag=rlk_jelly]
summon minecraft:item_display ~ ~1.6 ~ {Tags:["rlk_jelly","rlk_isn"],brightness:{sky:15,block:15},billboard:"center",item:{id:"minecraft:heart_of_the_sea",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.9f,0.9f,0.9f]}}
scoreboard players operation @e[tag=rlk_isn] life = #jellyDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
execute unless score #k196 snd matches 1 run function rlk:snd/f212
