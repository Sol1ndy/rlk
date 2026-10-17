# pull tick 34 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 6 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.624 ^1.098 ^0.602 0.08 0.08 0.08 0 2 force @a[tag=player]
scoreboard players set @a[tag=player] vBig 10
title @a[tag=player] times 0 3 0
title @a[tag=player] title [{"text":"\ue510\ue5f0\ue511\ue5f1\ue512\ue5f0\ue513\ue5f0","font":"rlk:mboss_gd","color":"white","shadow_color":0}]
