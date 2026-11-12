# Q pattern tick 53
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0341f,1.8069f,0.4095f],left_rotation:[-0.4639f,-0.4639f,0.5337f,-0.5337f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_45]
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_47] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_49] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
