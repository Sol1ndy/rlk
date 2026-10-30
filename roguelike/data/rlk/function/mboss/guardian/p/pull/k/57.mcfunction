# pull tick 57 (@s = body, at the body).
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p4ca00]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^3.623 ^1.9 ^4.986 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^5.861 ^1.9 ^-1.905 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^1.9 ^-6.163 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-5.861 ^1.9 ^-1.905 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-3.623 ^1.9 ^4.986 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.9 ^0 3.709 0.3 3.709 0 3 force @a[tag=player]
