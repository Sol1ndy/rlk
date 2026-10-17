# pull tick 12 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 6 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.686 ^1.17 ^-0.618 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.82 ^1.598 ^-0.266 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.222 ^2.119 ^1.043 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-0.283 ^2.45 ^0.418 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.15 ^2.673 ^0.504 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.035 ^2.783 ^0.569 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.245 ^2.782 ^0.61 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.454 ^2.669 ^0.627 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.634 ^2.443 ^0.616 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.759 ^2.106 ^0.575 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.804 ^1.656 ^0.503 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.75f,0.8f],scale:0.6} ^-0.3 ^2.95 ^0.9 0.03 0.03 0.03 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:crimson_spore ^0 ^1.8 ^0 1.2 1.2 1.2 0 4 force @a[tag=player]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc1] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.9134f,1.0027f,-1.7491f],left_rotation:[0.1252f,0.2741f,-0.2492f,0.9204f],scale:[0.3361f,0.3361f,0.3361f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4rc","rlk_mb_gd_p4rc2","rlk_mb_gd_p4new"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,block_state:{id:"minecraft:black_concrete"},transformation:{translation:[-1.9267f,2.9004f,-0.4339f],left_rotation:[0.2003f,0.3387f,-0.1294f,0.9102f],scale:[0.02f,0.02f,0.02f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4k0] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.2219f,0.0101f,-0.0531f],left_rotation:[0.0324f,0.2014f,0.0058f,0.979f],scale:[0.52f,0.52f,0.52f],right_rotation:[0f,0f,0f,1f]}}
execute at @e[tag=rlk_body,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cage","rlk_mb_gd_p4k1"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,block_state:{id:"minecraft:black_concrete"},transformation:{translation:[-0.3334f,0.2763f,-0.174f],left_rotation:[0.0429f,0.219f,0.0069f,0.9748f],scale:[0.05f,0.05f,0.05f],right_rotation:[0f,0f,0f,1f]},Glowing:1b,glow_color_override:12070714}
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:black_concrete"} ~-0.3 ~0.3 ~-0.16 0.15 0.15 0.15 0 3 force @a[tag=player]
