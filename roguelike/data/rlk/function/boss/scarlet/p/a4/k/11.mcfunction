# A4 pattern tick 11
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3376f,1.6902f,-0.1764f],left_rotation:[-0.9563f,0f,0f,0.2924f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_3]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_5] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_10,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3724f,0.9581f,0.849f],left_rotation:[-0.6686f,0.6686f,0.2302f,0.2303f],scale:[0.2041f,0.22f,2.8287f],right_rotation:[0f,0f,0f,1f]}}
