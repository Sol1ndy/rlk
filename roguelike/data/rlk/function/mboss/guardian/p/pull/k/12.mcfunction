# pull tick 12 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 8 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.921 ^0.664 ^0.69 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.167 ^1.301 ^-1.393 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-1.308 ^2.304 ^0.559 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-0.283 ^2.45 ^0.418 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.15 ^2.673 ^0.504 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.035 ^2.783 ^0.569 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.245 ^2.782 ^0.61 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.454 ^2.669 ^0.627 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.634 ^2.443 ^0.616 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.759 ^2.106 ^0.575 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.804 ^1.656 ^0.503 0 0 0 0 1 force @a[tag=player]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc4] run data merge entity @s {start_interpolation:0,interpolation_duration:13,transformation:{translation:[0.7405f,1.6767f,2.5044f],left_rotation:[0.3076f,0.7533f,-0.5621f,0.1482f],scale:[0.2668f,0.2668f,0.2668f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4k7] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.2202f,1.3163f,0.244f],left_rotation:[-0.0589f,0.1948f,-0.011f,0.979f],scale:[0.46f,0.46f,0.46f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4k8] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.5764f,1.5589f,-0.1702f],left_rotation:[0.0289f,0.0645f,0.0094f,0.9975f],scale:[0.5f,0.5f,0.5f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @e[tag=rlk_av,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cage","rlk_mb_gd_p4k9"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,block_state:{id:"minecraft:black_concrete"},transformation:{translation:[0.2293f,1.8735f,-0.2352f],left_rotation:[-0.0576f,0.1208f,-0.0153f,0.9909f],scale:[0.05f,0.05f,0.05f],right_rotation:[0f,0f,0f,1f]},Glowing:1b,glow_color_override:12070714}
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:black_concrete"} ~0.26 ~1.9 ~-0.22 0.15 0.15 0.15 0 3 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.2} ~ ~1.1 ~ 0.45 0.8 0.45 0 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.38f,0f,0.02f],scale:1.5} ~ ~1.1 ~ 0.55 0.9 0.55 0 2 force @a[tag=player]
