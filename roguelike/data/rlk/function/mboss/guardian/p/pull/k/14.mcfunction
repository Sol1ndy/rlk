# pull tick 14 (@s = body, at the body).
playsound minecraft:block.respawn_anchor.charge hostile @a[tag=player] ~ ~ ~ 0.6 1.3 0.3
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 6 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.475 ^1.034 ^-0.705 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.428 ^1.455 ^0.878 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^1.259 ^2.102 ^-0.088 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.514 ^1.434 ^0.749 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.555 ^1.771 ^0.52 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.558 ^2.005 ^0.179 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.53 ^2.137 ^-0.222 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.476 ^2.166 ^-0.631 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.405 ^2.092 ^-0.996 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.322 ^1.916 ^-1.264 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.235 ^1.638 ^-1.384 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:crimson_spore ^0 ^1.8 ^0 1.2 1.2 1.2 0 4 force @a[tag=player]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc1] run data merge entity @s {start_interpolation:0,interpolation_duration:19,transformation:{translation:[-0.5397f,1.4321f,-1.7203f],left_rotation:[0.317f,0.6941f,-0.6311f,-0.1395f],scale:[0.3361f,0.3361f,0.3361f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc3] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.9079f,0.7361f,1.5984f],left_rotation:[0.2294f,0.2662f,0.2312f,0.9072f],scale:[0.3849f,0.3849f,0.3849f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4rc","rlk_mb_gd_p4rc4","rlk_mb_gd_p4new"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,block_state:{id:"minecraft:red_stained_glass"},transformation:{translation:[0.3827f,2.7434f,1.5282f],left_rotation:[0.0293f,0.101f,0.0401f,0.9936f],scale:[0.02f,0.02f,0.02f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4k2] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0.0118f,0.4157f,-0.4734f],left_rotation:[-0.0589f,0.0179f,-0.0223f,0.9979f],scale:[0.46f,0.46f,0.46f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4k3] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.4332f,0.4544f,0.1628f],left_rotation:[-0.0616f,0.1414f,-0.015f,0.9879f],scale:[0.5f,0.5f,0.5f],right_rotation:[0f,0f,0f,1f]}}
execute at @e[tag=rlk_body,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cage","rlk_mb_gd_p4k4"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,block_state:{id:"minecraft:black_concrete"},transformation:{translation:[-0.3621f,0.9537f,0.0536f],left_rotation:[-0.0457f,-0.0795f,-0.0226f,0.9955f],scale:[0.05f,0.05f,0.05f],right_rotation:[0f,0f,0f,1f]},Glowing:1b,glow_color_override:12070714}
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:black_concrete"} ~-0.34 ~0.98 ~0.08 0.15 0.15 0.15 0 3 force @a[tag=player]
