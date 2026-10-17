# flyslam clip tick 10
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c2_1]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c4_0]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c8_1,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[-0.294f,2.787f,0.295f],left_rotation:[-0.692f,0.243f,-0.407f,-0.544f],scale:[0.012f,0.012f,0.012f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.525 ^3.509 ^0.445 run particle minecraft:dust_color_transition{from_color:[0.36f,0.22f,0.16f],to_color:[0.23f,0.15f,0.13f],scale:0.8} ~ ~ ~ 0.05 0.12 0.05 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.574 ^4.48 ^0.396 run particle minecraft:dust_color_transition{from_color:[0.36f,0.22f,0.16f],to_color:[0.23f,0.15f,0.13f],scale:0.8} ~ ~ ~ 0.05 0.12 0.05 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.623 ^5.451 ^0.347 run particle minecraft:dust_color_transition{from_color:[0.36f,0.22f,0.16f],to_color:[0.23f,0.15f,0.13f],scale:0.8} ~ ~ ~ 0.05 0.12 0.05 0 1 force @a[tag=player]
