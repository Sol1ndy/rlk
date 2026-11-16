# D4 pattern tick 24
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0736f,0.988f,0.5575f],left_rotation:[-0.2487f,-0.2659f,0.9286f,-0.0715f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_16]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_18] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
