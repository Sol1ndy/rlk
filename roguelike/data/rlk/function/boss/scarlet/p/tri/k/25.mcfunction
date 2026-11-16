# TRI pattern tick 25
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1514f,1.4373f,0.5803f],left_rotation:[-0.7497f,-0.4156f,0.2497f,0.4505f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_17]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_21] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_23] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_24,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0573f,1.6433f,0.476f],left_rotation:[-0.7425f,0.4047f,0.5321f,0.0436f],scale:[0.1261f,0.22f,1.3018f],right_rotation:[0f,0f,0f,1f]}}
