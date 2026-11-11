# A13 pattern tick 147.
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b140] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5837f,1.2475f,-0.3982f],left_rotation:[-0.7697f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_141] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_146,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.6845f,1.4091f,-0.4156f],left_rotation:[-0.523f,0.7807f,-0.0817f,0.3321f],scale:[0.1819f,0.22f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.683 ^1.284 ^-0.525 run function rlk:boss/scarlet/core/sw/rib
