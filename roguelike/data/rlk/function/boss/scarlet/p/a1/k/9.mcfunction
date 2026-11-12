# A1 pattern tick 9
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.311f,1.1049f,0.1646f],left_rotation:[-0.6861f,-0.5572f,0.1711f,0.4353f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_1]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_3] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
