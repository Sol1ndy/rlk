# BLUE pattern tick 12
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blueb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.436f,1.2955f,0.1248f],left_rotation:[-0.2067f,0.0862f,-0.6762f,0.7018f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_8] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_10] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_blue_11,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4852f,1.3004f,0.2167f],left_rotation:[-0.2718f,-0.0347f,-0.9093f,0.3133f],scale:[0.3303f,0.22f,1.5414f],right_rotation:[0f,0f,0f,1f]}}
