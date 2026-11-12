# A13 pattern tick 237.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b225] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0589f,2.1426f,0.4051f],left_rotation:[-0.8481f,0.002f,-0.0037f,0.5298f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_229]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_231] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_235] remove rlk_hr_trr
