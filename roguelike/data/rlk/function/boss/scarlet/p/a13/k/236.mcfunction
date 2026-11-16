# A13 pattern tick 236.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b225] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0587f,2.149f,0.4021f],left_rotation:[-0.8505f,0.002f,-0.0037f,0.5259f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_228]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_232] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_235,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0619f,2.1335f,0.4099f],left_rotation:[-0.5631f,0.625f,0.3966f,0.3674f],scale:[0.1444f,0.22f,1.6381f],right_rotation:[0f,0f,0f,1f]}}
