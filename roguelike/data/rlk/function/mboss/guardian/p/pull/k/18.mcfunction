# pull tick 18 (@s = body, at the body).
playsound minecraft:block.fire.ambient hostile @a[tag=player] ~ ~ ~ 0.8 0.9 0.3
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 8 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.329 ^0.723 ^1.014 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.901 ^1.303 ^-1.001 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-1.415 ^2.247 ^-0.301 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.611 ^2.813 ^-0.693 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.396 ^3.063 ^-0.783 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.084 ^3.244 ^-0.828 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-0.279 ^3.356 ^-0.832 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.645 ^3.399 ^-0.8 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.968 ^3.373 ^-0.734 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-1.202 ^3.279 ^-0.641 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-1.299 ^3.115 ^-0.523 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.75f,0.8f],scale:0.6} ^-0.3 ^2.95 ^0.9 0.03 0.03 0.03 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:crimson_spore ^0 ^1.8 ^0 1.2 1.2 1.2 0 4 force @a[tag=player]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4rc5] run data merge entity @s {start_interpolation:0,interpolation_duration:15,transformation:{translation:[1.7465f,1.5925f,0.4104f],left_rotation:[-0.3189f,0.8091f,0.4236f,-0.2535f],scale:[0.3615f,0.3615f,0.3615f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_p4k7] run data merge entity @s {start_interpolation:0,interpolation_duration:2,transformation:{translation:[-0.0899f,1.3294f,0.0631f],left_rotation:[-0.002f,-0.1188f,-0.0011f,0.9929f],scale:[0.46f,0.46f,0.46f],right_rotation:[0f,0f,0f,1f]}}
execute if entity @e[tag=rlk_av,limit=1] at @e[tag=rlk_body,limit=1] run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cage","rlk_mb_gd_p4k8"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:0,block_state:{id:"minecraft:black_concrete"},transformation:{translation:[-0.3334f,1.7783f,0.0431f],left_rotation:[0.1002f,0.2141f,0.0165f,0.9715f],scale:[0.05f,0.05f,0.05f],right_rotation:[0f,0f,0f,1f]},Glowing:1b,glow_color_override:12070714}
execute at @e[tag=rlk_body,limit=1] run particle minecraft:block{block_state:"minecraft:black_concrete"} ~-0.3 ~1.8 ~0.06 0.15 0.15 0.15 0 3 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.2} ~ ~1.1 ~ 0.45 0.8 0.45 0 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.38f,0f,0.02f],scale:1.5} ~ ~1.1 ~ 0.55 0.9 0.55 0 2 force @a[tag=player]
