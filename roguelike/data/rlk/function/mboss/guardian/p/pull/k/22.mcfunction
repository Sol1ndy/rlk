# pull tick 22 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 8 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.049 ^0.519 ^-1.409 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-1.201 ^1.391 ^0.75 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^1.04 ^2.547 ^0.553 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.064 ^2.433 ^0.59 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.178 ^2.598 ^0.488 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.309 ^2.67 ^0.313 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.44 ^2.649 ^0.094 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.559 ^2.536 ^-0.139 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.648 ^2.33 ^-0.356 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.693 ^2.032 ^-0.527 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.68 ^1.64 ^-0.623 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:crimson_spore ^0 ^1.8 ^0 1.2 1.2 1.2 0 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.2} ~ ~1.1 ~ 0.45 0.8 0.45 0 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.38f,0f,0.02f],scale:1.5} ~ ~1.1 ~ 0.55 0.9 0.55 0 2 force @a[tag=player]
# Screen overlay: every frame is a title of 4 glyph tiles (one flat glyph for the flash).
scoreboard players set @a[tag=player] vBig 22
title @a[tag=player] times 0 3 0
title @a[tag=player] title [{"text":"\ue500\ue5f0\ue501\ue5f1\ue502\ue5f0\ue503\ue5f0","font":"rlk:mboss_gd","color":"white","shadow_color":0}]
