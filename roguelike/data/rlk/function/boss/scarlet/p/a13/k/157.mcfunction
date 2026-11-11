# A13 pattern tick 157.
function rlk:boss/scarlet/g/cut/aim {s:170}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b139] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0671f,1.3979f,0.3968f],left_rotation:[-0.5792f,-0.0616f,0.4056f,0.7044f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_149]
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_151] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_153] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_155] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_156,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0947f,1.2372f,0.3602f],left_rotation:[-0.3677f,-0.1598f,0.6508f,0.6448f],scale:[0.7603f,0.22f,1.7479f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_156,tag=rlk_hr_tr_i1] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.0498f,1.2553f,0.3753f],left_rotation:[-0.5123f,0.0222f,0.6267f,0.5868f],scale:[0.7523f,0.22f,1.7305f],right_rotation:[0f,0f,0f,1f]}}
