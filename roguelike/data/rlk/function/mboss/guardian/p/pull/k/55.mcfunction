# pull tick 55 (@s = body, at the body).
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_p4ar]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.86f,0.45f],scale:0.8} ^1.89 ^2.771 ^-0.525 0.4 0.25 0.3 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^2.7 ^3.26 ^-0.75 0.2 0.2 0.2 0 1 force @a[tag=player]
