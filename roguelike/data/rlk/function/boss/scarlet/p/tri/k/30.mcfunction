# TRI pattern tick 30
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1203f,1.4566f,0.5801f],left_rotation:[-0.7497f,-0.4156f,0.2497f,0.4505f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_22]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_24] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
