# NB pattern tick 12
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3619f,1.8897f,0.7179f],left_rotation:[-0.6823f,-0.1243f,0.391f,0.6051f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_4]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_6] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
