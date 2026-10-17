# flyslam clip tick 24
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1.5} ~ ~9.382 ~ 0.3 0.6 0.3 0 5 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~9.182 ~ 0.25 0.4 0.25 0 3 force @a[tag=player]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_3,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:11,transformation:{translation:[-0.467f,-0.043f,0.612f],left_rotation:[-0.63f,-0.436f,0.212f,0.606f],scale:[0.019f,0.019f,0.019f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_4,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:10,transformation:{translation:[0.116f,-0.045f,0.586f],left_rotation:[0.488f,0.576f,-0.104f,0.647f],scale:[0.02f,0.02f,0.02f],right_rotation:[0f,0f,0f,1f]}}
particle minecraft:dust_color_transition{from_color:[0.99f,0.33f,0.33f],to_color:[0.39f,0.12f,0.1f],scale:1.3} ~ ~9.782 ~ 0.25 0.35 0.25 0 3 force @a[tag=player]
particle minecraft:block{block_state:"minecraft:black_concrete"} ~ ~9.382 ~ 0.2 0.3 0.2 0 2 force @a[tag=player]
particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:1} ~ ~10.582 ~ 0.3 0.3 0.3 0 2 force @a[tag=player]
