# The props of look plain (@s any): the old ones go first.
kill @e[tag=rlk_mb_ar_cp_test]
execute in minecraft:overworld run summon minecraft:item_display 537 202.5 4 {Tags:["rlk_mb_aux","rlk_mb_arena_prop","rlk_mb_ar_cp_test","rlk_mb_cp_ap_test"],Rotation:[0f,0f],brightness:{sky:15,block:15},item:{id:"minecraft:glass",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
execute in minecraft:overworld run summon minecraft:item_display 543 202.5 4 {Tags:["rlk_mb_aux","rlk_mb_arena_prop","rlk_mb_ar_cp_test","rlk_mb_cp_ap_test"],Rotation:[0f,0f],brightness:{sky:15,block:15},item:{id:"minecraft:glass",count:1},transformation:{translation:[0f,0f,0f],left_rotation:[0f,0f,0f,1f],right_rotation:[0f,0f,0f,1f],scale:[0.8f,0.8f,0.8f]}}
scoreboard players set #cpLook mb 0
