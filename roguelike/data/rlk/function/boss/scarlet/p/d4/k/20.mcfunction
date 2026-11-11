# D4 pattern tick 20
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0935f,1.005f,0.5354f],left_rotation:[-0.2483f,-0.2718f,0.9269f,-0.0731f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_12]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_14] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_16] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_18] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_19,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2776f,1.2257f,0.2223f],left_rotation:[0.2095f,0.25f,-0.9344f,0.1435f],scale:[0.4637f,0.22f,1.9604f],right_rotation:[0f,0f,0f,1f]}}
