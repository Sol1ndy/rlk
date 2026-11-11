# A9 pattern tick 10
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2814f,0.7618f,0.1426f],left_rotation:[-0.6645f,-0.6964f,0.2418f,0.1228f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_2]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_4] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_6] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_8] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_9,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0581f,0.9944f,0.4498f],left_rotation:[0.9438f,0.0116f,-0.3189f,0.0865f],scale:[0.5558f,0.22f,2.0365f],right_rotation:[0f,0f,0f,1f]}}
