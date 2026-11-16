# TRI pattern tick 15
function rlk:boss/scarlet/core/cam_clear
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2531f,1.0505f,0.974f],left_rotation:[0f,0f,0f,1f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_11] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_1"
execute at @s rotated as @s rotated ~ 0 positioned ^0.253 ^1.051 ^1.139 run function rlk:boss/scarlet/core/sw/rib
