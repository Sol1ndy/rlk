# pull tick 72 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb20] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,1.5f,0f],left_rotation:[-0.0413f,0.8984f,0.0865f,-0.4285f],scale:[0.2742f,0.2742f,0.2742f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb21] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,1.5f,0f],left_rotation:[-0.0413f,0.8984f,0.0865f,-0.4285f],scale:[0.2139f,0.2139f,0.2139f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^0.612 ^4.567 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^4.343 ^1.226 ^1.411 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^2.684 ^2.218 ^-3.694 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-2.684 ^2.218 ^-3.694 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-4.343 ^1.226 ^1.411 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.5 ^0 3.709 0.3 3.709 0 3 force @a[tag=player]
