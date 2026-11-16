# RINGS pattern tick 28
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.3155f,1.1596f,0.0843f],left_rotation:[-0.5997f,-0.6243f,0.3747f,0.332f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_20]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_22] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_24] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_26] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_27,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0448f,1.172f,0.2508f],left_rotation:[0.7469f,-0.0816f,-0.6436f,0.146f],scale:[0.5123f,0.22f,1.8579f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_rings0_27,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0708f,1.1724f,0.2368f],left_rotation:[-0.8149f,-0.1621f,0.5549f,0.041f],scale:[0.5096f,0.22f,1.8496f],right_rotation:[0f,0f,0f,1f]}}
