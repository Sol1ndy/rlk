# flyslam clip tick 30
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_3]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5t_7]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5po,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.4f,0f,-0.4f],left_rotation:[0f,0f,0f,1f],scale:[0.8f,14f,0.8f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p5pi,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.11f,0f,-0.11f],left_rotation:[0f,0f,0f,1f],scale:[0.22f,14f,0.22f],right_rotation:[0f,0f,0f,1f]}}
