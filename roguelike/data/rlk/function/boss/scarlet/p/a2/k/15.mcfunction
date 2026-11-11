# A2 pattern tick 15
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a2b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.633f,0.9854f,0.0894f],left_rotation:[-0.5754f,-0.1585f,-0.52f,-0.6111f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a2_9] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a2_11] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a2_13] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a2_14,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3071f,1.1723f,-0.0197f],left_rotation:[0.1778f,0.7195f,-0.2101f,0.6377f],scale:[0.4174f,0.26f,1.9918f],right_rotation:[0f,0f,0f,1f]}}
