# sweep_g clip tick 21
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p11w1]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p11b3]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q11c_2,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:12,transformation:{translation:[-0.38f,0.794f,0.077f],left_rotation:[-0.164f,0.131f,-0.659f,0.722f],scale:[0.031f,0.031f,0.031f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q11c_6,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:13,transformation:{translation:[-0.398f,1.429f,-0.805f],left_rotation:[0.679f,-0.315f,0.329f,0.576f],scale:[0.018f,0.018f,0.018f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^ ^0.6 ^4.32 run particle minecraft:wax_on ~ ~ ~ 2.88 0.4 1.68 0 3 force @a[tag=player]
