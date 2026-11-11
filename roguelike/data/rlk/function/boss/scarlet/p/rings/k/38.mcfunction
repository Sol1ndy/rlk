# RINGS pattern tick 38
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5654f,1.0853f,-0.0594f],left_rotation:[-0.5997f,0.6243f,-0.3747f,0.332f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_30]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_34] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_36] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_37,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1526f,1.1525f,0.1521f],left_rotation:[-0.0815f,0.7469f,-0.146f,0.6436f],scale:[0.5348f,0.18f,1.9394f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_37,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2661f,1.136f,0.1132f],left_rotation:[0.162f,0.8149f,0.041f,0.5549f],scale:[0.5188f,0.18f,1.8821f],right_rotation:[0f,0f,0f,1f]}}
