# A3 pattern tick 53
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0832f,1.6677f,0.3706f],left_rotation:[-0.8158f,0f,0f,0.5783f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_45]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_47] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_49] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_1"
