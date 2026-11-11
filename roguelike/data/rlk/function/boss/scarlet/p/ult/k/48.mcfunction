# ULT pattern tick 48
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2782f,0.805f,0.1458f],left_rotation:[-0.6846f,0.5948f,0.1769f,-0.3824f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_42] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_44] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_46] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_47,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.1052f,0.8802f,0.2855f],left_rotation:[0.8058f,-0.0077f,-0.5725f,0.1516f],scale:[0.4915f,0.3f,1.7788f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_47,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.1467f,0.8648f,0.2659f],left_rotation:[0.8757f,-0.0162f,-0.451f,0.172f],scale:[0.485f,0.3f,1.7553f],right_rotation:[0f,0f,0f,1f]}}
