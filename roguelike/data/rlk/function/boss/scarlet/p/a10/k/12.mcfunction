# A10 pattern tick 12
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0081f,1.7412f,0.6948f],left_rotation:[-0.7373f,0f,0f,0.6756f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_4]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_6] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
