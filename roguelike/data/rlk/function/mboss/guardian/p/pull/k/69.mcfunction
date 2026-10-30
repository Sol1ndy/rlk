# pull tick 69 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb20] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,1.5f,0f],left_rotation:[-0.0413f,0.8984f,0.0865f,-0.4285f],scale:[13.7113f,13.7113f,13.7113f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb21] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,1.5f,0f],left_rotation:[-0.0413f,0.8984f,0.0865f,-0.4285f],scale:[10.6948f,10.6948f,10.6948f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^3.533 ^0.555 ^4.863 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^5.716 ^1.861 ^-1.857 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^2.668 ^-6.01 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-5.716 ^1.861 ^-1.857 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-3.533 ^0.555 ^4.863 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.5 ^0 3.709 0.3 3.709 0 3 force @a[tag=player]
