# pull tick 58 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4r2] run data merge entity @s {start_interpolation:0,interpolation_duration:18,transformation:{translation:[0f,0f,0f],left_rotation:[-0.4545f,0.5417f,0.5417f,0.4545f],scale:[12.7907f,12.7907f,12.7907f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:0.8} ^1.89 ^2.771 ^-0.525 0.4 0.25 0.3 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^2.7 ^3.26 ^-0.75 0.2 0.2 0.2 0 1 force @a[tag=player]
