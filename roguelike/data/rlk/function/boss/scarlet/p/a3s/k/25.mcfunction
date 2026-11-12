# A3S pattern tick 25
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3sb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5039f,1.5519f,-0.3717f],left_rotation:[-0.825f,0.3417f,-0.1723f,0.4159f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3s_17]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3s_19] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3s_21] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
