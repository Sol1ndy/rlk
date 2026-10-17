# pull tick 23 (@s = body, at the body).
playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.8 1 0.3
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 8 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.985 ^0.503 ^-1.057 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.397 ^1.447 ^1.297 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^1.051 ^2.625 ^-0.243 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.2} ~ ~1.1 ~ 0.45 0.8 0.45 0 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.38f,0f,0.02f],scale:1.5} ~ ~1.1 ~ 0.55 0.9 0.55 0 2 force @a[tag=player]
execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_p4v0] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[0.6053f,-0.2234f,0f],left_rotation:[0f,0f,-0.3827f,0.9239f],scale:[17.12f,6.4f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_p4v1] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[0.2234f,0.6053f,0f],left_rotation:[0f,0f,0.3827f,0.9239f],scale:[17.12f,6.4f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_p4v2] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[-0.6053f,0.2234f,0f],left_rotation:[0f,0f,0.9239f,0.3827f],scale:[17.12f,6.4f,1f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:text_display,tag=rlk_mb_gd_p4v3] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[-0.2234f,-0.6053f,0f],left_rotation:[0f,0f,0.9239f,-0.3827f],scale:[17.12f,6.4f,1f],right_rotation:[0f,0f,0f,1f]}}
