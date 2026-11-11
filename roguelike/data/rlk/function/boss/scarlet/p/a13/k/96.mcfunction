# A13 pattern tick 96.
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_88]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_90] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_92] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_94] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_95,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.2438f,0.8643f,-0.1706f],left_rotation:[0.9157f,-0.0507f,0.3793f,0.1224f],scale:[0.6119f,0.22f,1.797f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_95,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[-0.0769f,0.837f,-0.2873f],left_rotation:[0.836f,-0.0712f,0.5326f,0.1118f],scale:[0.5768f,0.22f,1.6929f],right_rotation:[0f,0f,0f,1f]}}
