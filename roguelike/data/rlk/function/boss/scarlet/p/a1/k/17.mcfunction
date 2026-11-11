# A1 pattern tick 17
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5905f,0.9226f,-0.1537f],left_rotation:[-0.5553f,-0.516f,-0.4378f,-0.4835f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_11] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_13] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_15] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_16,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.3857f,0.9526f,0.009f],left_rotation:[0.0401f,0.7287f,-0.0135f,0.6835f],scale:[0.5704f,0.3f,2.5971f],right_rotation:[0f,0f,0f,1f]}}
