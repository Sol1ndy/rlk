# D4 pattern tick 39
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1563f,1.715f,0.3477f],left_rotation:[-0.8032f,0f,0f,0.5957f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_31]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_33] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_35] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
