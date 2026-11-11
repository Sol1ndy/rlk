# Q pattern tick 51
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0307f,1.7876f,0.4139f],left_rotation:[-0.4639f,-0.4639f,0.5337f,-0.5337f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_43]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_45] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_47] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #q_hit hr matches 1 run tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_49] remove rlk_hr_trr
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_50,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0337f,1.678f,0.4652f],left_rotation:[0.0532f,-0.6557f,0.7524f,0.0337f],scale:[0.131f,0.18f,1.5278f],right_rotation:[0f,0f,0f,1f]}}
