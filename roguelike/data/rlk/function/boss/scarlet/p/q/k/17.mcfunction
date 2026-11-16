# Q pattern tick 17
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3523f,1.0979f,-0.1131f],left_rotation:[-0.6974f,0.7038f,-0.1167f,0.0678f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
tag @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_15] remove rlk_hr_trr
execute as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0_16,tag=rlk_hr_tr_i0] run data merge entity @s {start_interpolation:0,transformation:{translation:[0.4113f,1.0152f,-0.2902f],left_rotation:[0.6549f,0.7436f,0.0597f,0.121f],scale:[0.1363f,0.22f,1.435f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.395 ^1.086 ^-0.272 run function rlk:boss/scarlet/core/sw/rib
