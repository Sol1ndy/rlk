# A13 pattern tick 148.
execute rotated as @e[type=minecraft:marker,tag=rlk_hr_gst,limit=1] run tp @s ~ ~ ~ ~ 0
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_a13b140] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.5837f,1.2475f,-0.3982f],left_rotation:[-0.7698f,0.539f,-0.1962f,0.2802f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_140]
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_a13_146] remove rlk_hr_trr
execute at @s rotated as @s rotated ~ 0 positioned ^0.683 ^1.284 ^-0.525 run function rlk:boss/scarlet/core/sw/rib
