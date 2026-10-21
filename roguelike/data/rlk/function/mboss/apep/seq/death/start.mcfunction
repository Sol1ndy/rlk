# STUB (AP-CORE, ap_contract 1.6): the pattern stage AP-P1 replaces this file.
# @s = body (death_start): the death clip runs (core); the seed prop at the centre.
kill @e[tag=rlk_mb_ap_seed]
execute positioned 440 201.4 8 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_ap_seed"],billboard:"center",brightness:{block:15,sky:15},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0f,0f,0f]},item:{id:"minecraft:torchflower_seeds",count:1}}
