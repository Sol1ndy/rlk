kill @e[tag=rlk_gflag]
summon minecraft:item_display ~ ~1.2 ~ {Tags:["rlk_gflag","rlk_isn"],brightness:{sky:15,block:15},billboard:"vertical",item:{id:"minecraft:white_banner",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[1.2f,1.2f,1.2f]}}
scoreboard players operation @e[tag=rlk_isn] life = #gflagDur tmp
tag @e[tag=rlk_isn] remove rlk_isn
playsound minecraft:block.anvil.land master @a ~ ~ ~ 0.3 1.4
