# D4 pattern tick 22
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0836f,0.9965f,0.5465f],left_rotation:[-0.2485f,-0.2688f,0.9278f,-0.0723f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_14]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_16] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_18] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
