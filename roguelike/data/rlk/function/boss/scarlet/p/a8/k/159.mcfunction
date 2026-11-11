# A8 pattern tick 159.
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8b154] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5837f,1.2475f,-0.3982f],left_rotation:[-0.7698f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_155] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_quad_1"
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a8_158,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.6819f,1.4099f,-0.4679f],left_rotation:[-0.6048f,0.7192f,-0.1173f,0.3213f],scale:[0.2745f,0.22f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.683 ^1.284 ^-0.525 run function rlk:boss/scarlet/core/sw/rib
