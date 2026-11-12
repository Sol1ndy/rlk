# A3S pattern tick 27
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3sb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.49f,1.5448f,-0.3888f],left_rotation:[-0.8304f,0.344f,-0.1678f,0.405f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3s_19]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3s_21] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
