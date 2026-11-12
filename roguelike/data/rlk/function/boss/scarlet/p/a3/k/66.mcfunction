# A3 pattern tick 66
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5574f,0.9988f,-0.3361f],left_rotation:[0.3548f,-0.8566f,0.3461f,-0.1434f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_58]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_60] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
