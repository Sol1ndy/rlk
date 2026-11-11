# TRI pattern tick 13
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2608f,1.0398f,0.8153f],left_rotation:[0f,0f,0f,1f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_11] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_12,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.3369f,0.9471f,0.4585f],left_rotation:[-0.0464f,-0.031f,-0.9945f,0.0882f],scale:[0.199f,0.26f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.261 ^1.04 ^0.98 run function rlk:boss/scarlet/core/sw/rib
