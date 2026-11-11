# A8 pattern tick 42.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2197f,1.0586f,-0.0683f],left_rotation:[-0.3696f,-0.8924f,0.2391f,0.099f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_34]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_36] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_38] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_40] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_41,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2119f,1.1539f,0.1122f],left_rotation:[0.6193f,0.6255f,-0.4083f,0.2421f],scale:[0.7013f,0.22f,1.7527f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_41,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2388f,1.1159f,0.0561f],left_rotation:[0.5742f,0.7542f,-0.3153f,0.0455f],scale:[0.6837f,0.22f,1.7052f],right_rotation:[0f,0f,0f,1f]}}
