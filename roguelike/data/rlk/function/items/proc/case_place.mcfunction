kill @e[tag=rlk_case]
summon minecraft:item_display ~ ~0.7 ~ {Tags:["rlk_case","rlk_isn"],brightness:{sky:15,block:15},billboard:"vertical",item:{id:"minecraft:lily_of_the_valley",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]}}
scoreboard players operation @e[tag=rlk_isn] life = #caseDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
execute unless score #k136 snd matches 1 run function rlk:snd/f144
