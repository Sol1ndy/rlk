# pull tick 55 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4ca20] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,1.9f,0f],left_rotation:[0f,-0.1736f,0f,-0.9848f],scale:[-13.7113f,13.7113f,13.7113f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^2.535 ^1.9 ^3.489 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^4.102 ^1.9 ^-1.333 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^1.9 ^-4.313 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-4.102 ^1.9 ^-1.333 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-2.535 ^1.9 ^3.489 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.9 ^0 3.709 0.3 3.709 0 3 force @a[tag=player]
