# Q pattern tick 18
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3532f,1.0992f,-0.1236f],left_rotation:[-0.6974f,0.7038f,-0.1167f,0.0678f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_16] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^0.396 ^1.088 ^-0.283 run function rlk:boss/scarlet/core/sw/rib
