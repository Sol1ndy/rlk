# MX pattern tick 31
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mxb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0192f,1.0053f,0.3401f],left_rotation:[-0.2636f,-0.4167f,0.6561f,0.5713f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_23]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_25] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_27] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_29] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_30,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1234f,1.085f,0.2363f],left_rotation:[0.1298f,-0.631f,-0.0183f,0.7646f],scale:[0.6442f,0.26f,1.8169f],right_rotation:[0f,0f,0f,1f]}}
