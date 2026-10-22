# pull tick 6 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 5 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.514 ^1.28 ^1.028 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.494 ^1.801 ^-0.749 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.876 ^2.229 ^-0.052 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-0.492 ^1.453 ^-0.71 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.672 ^1.74 ^-0.628 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.843 ^1.958 ^-0.465 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-0.99 ^2.107 ^-0.251 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-1.101 ^2.186 ^-0.017 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-1.159 ^2.196 ^0.207 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-1.152 ^2.136 ^0.393 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-1.066 ^2.008 ^0.51 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4rc","rlk_mb_gd_p4rc0","rlk_mb_gd_p4new"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,block_state:{id:"minecraft:red_concrete"},transformation:{translation:[0.9647f,2.6969f,-0.8385f],left_rotation:[-0.1567f,0.28f,0.0943f,0.9424f],scale:[0.02f,0.02f,0.02f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
