# pull tick 14 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 8 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.049 ^0.519 ^-1.409 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-1.201 ^1.391 ^0.75 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^1.04 ^2.547 ^0.553 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.514 ^1.434 ^0.749 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.555 ^1.771 ^0.52 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.558 ^2.005 ^0.179 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.53 ^2.137 ^-0.222 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.476 ^2.166 ^-0.631 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.405 ^2.092 ^-0.996 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.322 ^1.916 ^-1.264 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.235 ^1.638 ^-1.384 0 0 0 0 1 force @a[tag=player]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4k10] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.0851f,1.9076f,-0.2698f],left_rotation:[-0.0441f,-0.2843f,-0.0349f,0.9571f],scale:[0.44f,0.44f,0.44f],right_rotation:[0f,0f,0f,1f]}}
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.2} ~ ~1.1 ~ 0.45 0.8 0.45 0 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.38f,0f,0.02f],scale:1.5} ~ ~1.1 ~ 0.55 0.9 0.55 0 2 force @a[tag=player]
# Screen overlay: every frame is a title of 4 glyph tiles (one flat glyph for the flash).
scoreboard players set @a[tag=player] vBig 22
title @a[tag=player] times 0 3 0
title @a[tag=player] title [{"text":"\ue500\ue5f0\ue501\ue5f1\ue502\ue5f0\ue503\ue5f0","font":"rlk:mboss_gd","color":"white","shadow_color":0}]
