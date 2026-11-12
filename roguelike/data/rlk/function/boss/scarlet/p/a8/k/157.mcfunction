# A8 pattern tick 157.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5807f,1.4997f,-0.2849f],left_rotation:[-0.7697f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_155] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^0.68 ^1.536 ^-0.411 run function rlk:boss/scarlet/core/sw/rib
