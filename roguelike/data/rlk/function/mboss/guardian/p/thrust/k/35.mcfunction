# thrust clip tick 35
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p1bar] run data merge entity @s {start_interpolation:0,interpolation_duration:11,transformation:{translation:[-1.29f,0.034f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.58f,0.012f,8.4f],right_rotation:[0f,0f,0f,1f]}}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] feet run tp @s ~ ~ ~ ~ 0
