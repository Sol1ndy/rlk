# TRI pattern tick 14
execute at @s run function rlk:boss/scarlet/fx/snd/a2_hit
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2577f,1.0442f,0.96f],left_rotation:[0f,0f,0f,1f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_12] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^0.258 ^1.044 ^1.125 run function rlk:boss/scarlet/core/sw/rib
