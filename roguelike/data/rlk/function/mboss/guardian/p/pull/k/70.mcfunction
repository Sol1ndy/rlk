# pull tick 70 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb10] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0622f,0.7569f,0.0729f,0.6465f],scale:[0.2742f,0.2742f,0.2742f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb11] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0622f,0.7569f,0.0729f,0.6465f],scale:[0.2139f,0.2139f,0.2139f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^0.464 ^5.331 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^5.07 ^1.18 ^1.647 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^3.133 ^2.338 ^-4.313 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-3.133 ^2.338 ^-4.313 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-5.07 ^1.18 ^1.647 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.5 ^0 3.709 0.3 3.709 0 3 force @a[tag=player]
