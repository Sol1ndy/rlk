# Q pattern tick 9
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3868f,0.7021f,0.0332f],left_rotation:[-0.5192f,0.659f,-0.4802f,0.2561f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_3] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
