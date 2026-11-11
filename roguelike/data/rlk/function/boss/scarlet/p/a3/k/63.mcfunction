# A3 pattern tick 63
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5673f,1.0257f,-0.3235f],left_rotation:[0.3519f,-0.8496f,0.363f,-0.1504f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_55]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_57] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_59] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a3_61] remove rlk_hr_trr
