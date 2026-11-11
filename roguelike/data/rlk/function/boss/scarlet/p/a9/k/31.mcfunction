# A9 pattern tick 31
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4325f,0.9089f,-0.1268f],left_rotation:[-0.6801f,-0.6438f,-0.1936f,-0.2925f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_25] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_27] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_29] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_30,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1692f,0.9509f,0.1875f],left_rotation:[0.0102f,0.9157f,-0.0697f,0.3956f],scale:[0.4787f,0.26f,1.999f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9r0r26] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_1"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9w0w] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_rib_2"
