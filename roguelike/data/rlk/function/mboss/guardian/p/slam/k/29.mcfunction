# slam tick 29 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p3pil] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0f,4.2f,0f],left_rotation:[0f,0f,0f,1f],scale:[0.01f,8.4f,1f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:wax_on ~ ~0.8 ~ 1.4 0.6 1.4 0 3 force @a[tag=player]
execute rotated as @s rotated ~ 0 positioned ^0 ^0 ^3.1 positioned ~ 201 ~ run particle minecraft:dust{color:[0.86f,0.78f,0.45f],scale:1.1} ~ ~0.4 ~ 1.6 0.3 1.6 0 4 force @a[tag=player]
