# A8 pattern tick 111.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b79] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.6163f,0.918f,0.2833f],left_rotation:[-0.3705f,-0.18f,-0.3599f,-0.8371f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_107] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_109] remove rlk_hr_trr
