# pull tick 84 (@s = body, at the body).
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb00]
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb01]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^0.643 ^4.409 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^4.193 ^1.235 ^1.362 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^2.592 ^2.193 ^-3.567 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-2.592 ^2.193 ^-3.567 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-4.193 ^1.235 ^1.362 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.5 ^0 3 0.3 3 0 3 force @a[tag=player]
