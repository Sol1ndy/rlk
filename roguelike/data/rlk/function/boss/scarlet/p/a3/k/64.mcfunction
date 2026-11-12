# A3 pattern tick 64
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5635f,1.0232f,-0.3284f],left_rotation:[0.353f,-0.8523f,0.3566f,-0.1477f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_56]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_58] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_60] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
