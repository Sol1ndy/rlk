# HCUT pattern tick 10
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3941f,0.543f,0.0056f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_2]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_4] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
