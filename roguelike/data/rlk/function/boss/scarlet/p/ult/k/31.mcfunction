# ULT pattern tick 31
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7096f,1.1326f,-0.0992f],left_rotation:[-0.3524f,-0.7467f,-0.365f,-0.4302f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_23]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_25] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
