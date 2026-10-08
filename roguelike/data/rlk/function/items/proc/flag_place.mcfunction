kill @e[tag=rlk_flag]
summon minecraft:item_display ~ ~1.2 ~ {Tags:["rlk_flag","rlk_flagnew"],billboard:"vertical",brightness:{sky:15,block:15},item:{id:"minecraft:red_banner",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]}}
scoreboard players operation @e[tag=rlk_flagnew] life = #flagDur tmp
tag @e[tag=rlk_flagnew] remove rlk_flagnew
playsound minecraft:block.beacon.power_select master @a ~ ~ ~ 0.6 1.4
