# slam tick 25 (@s = body, at the body).
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3pil]
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p3fl]
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:wax_on ~ ~0.8 ~ 1.4 0.6 1.4 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:dust{color:[0.86f,0.78f,0.45f],scale:1.1} ~ ~0.4 ~ 1.92 0.3 1.92 0 4 force @a[tag=player]
