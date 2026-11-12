# Q pattern tick 5
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3827f,0.7211f,0.0405f],left_rotation:[-0.5174f,0.66f,-0.482f,0.2537f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_3] remove rlk_hr_trr
