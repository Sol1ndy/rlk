# A9 pattern tick 14
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2836f,0.755f,0.1411f],left_rotation:[-0.6645f,-0.6964f,0.2418f,0.1228f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_6]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_8] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
