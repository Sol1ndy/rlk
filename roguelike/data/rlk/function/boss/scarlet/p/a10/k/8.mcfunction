# A10 pattern tick 8
execute at @s rotated as @s rotated ~ 0 positioned ~ ~1.2 ~ run function rlk:boss/scarlet/fx/p/afterimage {len:15}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.018f,1.7273f,0.6903f],left_rotation:[-0.7373f,-0.0018f,-0.002f,0.6756f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_2] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_4] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_6] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_7,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1112f,1.8575f,0.6479f],left_rotation:[-0.1353f,-0.7259f,-0.6632f,0.1219f],scale:[0.1828f,0.18f,1.435f],right_rotation:[0f,0f,0f,1f]}}
