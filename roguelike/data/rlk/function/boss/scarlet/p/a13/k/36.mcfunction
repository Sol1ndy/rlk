# A13 pattern tick 36.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b16] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2297f,1.0507f,-0.0507f],left_rotation:[-0.3696f,-0.8924f,0.2391f,0.099f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_28]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_30] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_32] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_34] remove rlk_hr_trr
