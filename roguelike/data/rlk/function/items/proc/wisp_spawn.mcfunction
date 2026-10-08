scoreboard players operation #wispCd itv = #wispCdT tmp
summon minecraft:item_display ~ ~1.0 ~ {Tags:["rlk_wisp","rlk_isn"],brightness:{sky:15,block:15},billboard:"center",item:{id:"minecraft:snowball",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
scoreboard players operation @e[tag=rlk_isn] life = #wispFuse tmp
tag @e[tag=rlk_isn] remove rlk_isn
