# 위치 = 균열이 생길 곳
summon minecraft:item_display ~ ~ ~ {Tags:["rlk_rift","rlk_riftn"],billboard:"center",brightness:{sky:15,block:15},Glowing:1b,glow_color_override:11829503,item:{id:"minecraft:echo_shard",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
scoreboard players operation @e[tag=rlk_riftn] life = #skRiftLife tmp
tag @e[tag=rlk_riftn] remove rlk_riftn
playsound minecraft:block.respawn_anchor.deplete master @a ~ ~ ~ 0.6 1.6
particle minecraft:reverse_portal ~ ~ ~ 0.2 0.2 0.2 0.1 25
