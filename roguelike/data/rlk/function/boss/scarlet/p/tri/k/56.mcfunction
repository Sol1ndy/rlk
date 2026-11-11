# TRI pattern tick 56
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2897f,1.5958f,0.5804f],left_rotation:[-0.7861f,-0.3834f,0.2125f,0.4357f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_48]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_50] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_52] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
