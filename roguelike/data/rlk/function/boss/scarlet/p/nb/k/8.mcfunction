# NB pattern tick 8
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3679f,1.9054f,0.6971f],left_rotation:[-0.6823f,-0.1243f,0.391f,0.6051f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_2] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_4] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_6] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_7,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0542f,2.252f,0.7052f],left_rotation:[-0.4684f,0.4868f,0.7361f,0.0426f],scale:[0.1521f,0.22f,1.1271f],right_rotation:[0f,0f,0f,1f]}}
