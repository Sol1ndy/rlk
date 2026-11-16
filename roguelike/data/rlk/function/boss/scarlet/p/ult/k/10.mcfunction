# ULT pattern tick 10
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.7359f,0.1225f],left_rotation:[-0.6331f,-0.7059f,0.3145f,0.0442f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_2]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_4] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
