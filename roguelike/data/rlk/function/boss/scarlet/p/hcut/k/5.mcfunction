# HCUT pattern tick 5
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3896f,0.5586f,0.0124f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_1] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_3] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_4,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1f,0.6616f,0.1703f],left_rotation:[0.1286f,0.791f,-0.0728f,0.5937f],scale:[0.7032f,0.22f,1.8789f],right_rotation:[0f,0f,0f,1f]}}
