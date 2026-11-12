# NB pattern tick 26
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5638f,2.0514f,0.0057f],left_rotation:[-0.6928f,0.1311f,-0.3887f,0.5931f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_18]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_20] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_22] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
