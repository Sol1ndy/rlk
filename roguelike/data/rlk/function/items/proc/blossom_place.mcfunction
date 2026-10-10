kill @e[tag=rlk_blossom]
summon minecraft:item_display ~ ~0.6 ~ {Tags:["rlk_blossom","rlk_blnew"],billboard:"vertical",brightness:{sky:15,block:15},item:{id:"minecraft:torchflower",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.1f,1.1f,1.1f]}}
scoreboard players operation @e[tag=rlk_blnew] life = #blossomDur tmp
tag @e[tag=rlk_blnew] remove rlk_blnew
execute unless score #k194 snd matches 1 run function rlk:snd/f210
