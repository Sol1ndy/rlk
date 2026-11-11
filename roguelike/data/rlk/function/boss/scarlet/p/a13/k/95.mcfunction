# A13 pattern tick 95.
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_87]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_89] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_91] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_93] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_94,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0771f,0.8643f,-0.2874f],left_rotation:[0.7308f,-0.0895f,0.6696f,0.0977f],scale:[0.6119f,0.22f,1.797f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_94,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.1258f,0.837f,-0.2695f],left_rotation:[0.6034f,-0.1052f,0.7864f,0.0806f],scale:[0.5768f,0.22f,1.6929f],right_rotation:[0f,0f,0f,1f]}}
