# A3 pattern tick 9
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4285f,1.6796f,-0.0881f],left_rotation:[-0.8779f,0f,0f,0.4788f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_3] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
