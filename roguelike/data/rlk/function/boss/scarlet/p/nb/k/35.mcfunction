# NB pattern tick 35
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0753f,1.7222f,0.7316f],left_rotation:[-0.4389f,-0.4389f,-0.5544f,0.5544f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_29] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_33] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_34,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1914f,1.8663f,0.7327f],left_rotation:[-0.1022f,-0.6071f,-0.7771f,0.1308f],scale:[0.251f,0.18f,1.435f],right_rotation:[0f,0f,0f,1f]}}
