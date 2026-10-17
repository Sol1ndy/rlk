# pull tick 7 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 5 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.999 ^1.223 ^-0.017 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.438 ^1.677 ^-0.729 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.473 ^2.151 ^0.854 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc0] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[0.7974f,2.4801f,-0.8376f],left_rotation:[-0.1567f,0.28f,0.0943f,0.9424f],scale:[0.3363f,0.3363f,0.3363f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4rc","rlk_mb_gd_p4rc1","rlk_mb_gd_p4new"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,block_state:{id:"minecraft:red_stained_glass"},transformation:{translation:[-0.663f,2.142f,-1.4945f],left_rotation:[0.2284f,0.232f,-0.0035f,0.9455f],scale:[0.02f,0.02f,0.02f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
playsound minecraft:entity.illusioner.prepare_mirror hostile @a[tag=player] ~ ~ ~ 0.7 0.8 0.23
execute at @e[tag=rlk_body,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cage","rlk_mb_gd_p4k0"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,block_state:{id:"minecraft:black_concrete"},transformation:{translation:[0.0929f,0.2369f,0.0754f],left_rotation:[0.0588f,0.061f,0.0194f,0.9962f],scale:[0.05f,0.05f,0.05f],right_rotation:[0f,0f,0f,1f]},Glowing:1b,glow_color_override:12070714}
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:black_concrete"} ~0.12 ~0.26 ~0.1 0.15 0.15 0.15 0 3 force @a[tag=player]
