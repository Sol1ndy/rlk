# D4 pattern tick 25
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0686f,0.9837f,0.563f],left_rotation:[-0.2488f,-0.2644f,0.929f,-0.0711f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_17]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
