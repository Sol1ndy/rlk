# A13 pattern tick 35.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b16] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2197f,1.0586f,-0.0683f],left_rotation:[-0.3696f,-0.8924f,0.2391f,0.099f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_27]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_29] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_31] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_33] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_34,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1733f,0.9804f,-0.176f],left_rotation:[0.2931f,0.8905f,-0.3382f,0.0814f],scale:[0.4591f,0.22f,1.547f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_34,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.2063f,1.0651f,-0.077f],left_rotation:[-0.4369f,-0.8545f,0.2806f,0.012f],scale:[0.4804f,0.22f,1.6188f],right_rotation:[0f,0f,0f,1f]}}
