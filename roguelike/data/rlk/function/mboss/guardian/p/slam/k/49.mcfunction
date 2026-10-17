# slam tick 49 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p3po] run data merge entity @s {start_interpolation:0,interpolation_duration:4,transformation:{translation:[0f,0.08f,0f],left_rotation:[-0.7071f,0f,0f,0.7071f],scale:[3.4f,3.4f,3.4f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.96f,0.65f],scale:0.9} ^-0.01 ^0.03 ^3.147 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.96f,0.65f],scale:0.9} ^-0.02 ^0.06 ^3.205 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.96f,0.65f],scale:0.9} ^-0.03 ^0.09 ^3.262 0.04 0.04 0.04 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.99f,0.96f,0.65f],scale:0.9} ^-0.04 ^0.12 ^3.32 0.04 0.04 0.04 0 1 force @a[tag=player]
