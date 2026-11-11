# A13 pattern tick 21.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b16] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4509f,1.4929f,-0.0171f],left_rotation:[-0.933f,0.25f,-0.067f,0.25f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.492 ^1.564 ^-0.16 run function rlk:boss/scarlet/core/sw/rib
