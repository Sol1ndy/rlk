# 이미 3그루면 가장 오래된 것(남은 시간이 가장 짧은 것)을 없앤다
execute store result score #sakN itv if entity @e[tag=rlk_sakura]
execute if score #sakN itv matches 3.. run function rlk:items/proc/sakura_oldest
summon minecraft:item_display ~ ~0.7 ~ {Tags:["rlk_sakura","rlk_isn"],brightness:{sky:15,block:15},billboard:"vertical",item:{id:"minecraft:cherry_sapling",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.3f,1.3f,1.3f]}}
scoreboard players operation @e[tag=rlk_isn] life = #sakDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
execute unless score #k153 snd matches 1 run function rlk:snd/f162
execute unless score #k154 snd matches 1 run function rlk:snd/f163
