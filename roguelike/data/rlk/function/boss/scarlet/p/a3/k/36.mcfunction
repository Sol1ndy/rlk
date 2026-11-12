# A3 pattern tick 36
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0921f,1.0186f,0.5367f],left_rotation:[-0.248f,-0.2766f,0.9255f,-0.0739f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_28]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
