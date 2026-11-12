# MX pattern tick 5
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mxb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5629f,0.8983f,-0.4141f],left_rotation:[0.3576f,-0.8626f,0.3303f,-0.1376f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_mx_3] remove rlk_hr_trr
