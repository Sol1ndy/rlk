# thrust clip tick 43
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q1a]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p1bar] run data merge entity @s {start_interpolation:0,interpolation_duration:15,transformation:{translation:[-1.04f,0.034f,0f],left_rotation:[0f,0f,0f,1f],scale:[2.08f,0.012f,7f],right_rotation:[0f,0f,0f,1f]}}
execute at @s facing entity @e[type=minecraft:marker,tag=rlk_mb_gd_p1u,limit=1] feet run tp @s ~ ~ ~ ~ 0
