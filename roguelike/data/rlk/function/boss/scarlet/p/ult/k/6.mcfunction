# ULT pattern tick 6
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2587f,0.7601f,0.1225f],left_rotation:[-0.6272f,-0.7056f,0.3265f,0.0463f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_2] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_4] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_5,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.1854f,0.8794f,0.2255f],left_rotation:[0.9286f,-0.0355f,-0.2991f,0.2166f],scale:[0.1868f,0.22f,1.7301f],right_rotation:[0f,0f,0f,1f]}}
