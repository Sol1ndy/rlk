# A8 pattern tick 26.
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b19] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4588f,1.3485f,-0.363f],left_rotation:[-0.933f,0.25f,-0.067f,0.25f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_25,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4961f,1.4889f,-0.333f],left_rotation:[-0.5961f,0.76f,0.0965f,0.2402f],scale:[0.2944f,0.18f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.5 ^1.42 ^-0.506 run function rlk:boss/scarlet/core/sw/rib
