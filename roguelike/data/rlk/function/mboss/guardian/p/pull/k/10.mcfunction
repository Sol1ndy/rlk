# pull tick 10 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 5 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.837 ^1.264 ^0.702 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^0.151 ^1.756 ^-0.858 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.851 ^2.197 ^0.31 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.753 ^2.538 ^-0.615 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.606 ^2.615 ^-0.686 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^0.362 ^2.607 ^-0.714 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^0.061 ^2.515 ^-0.706 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.256 ^2.338 ^-0.667 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.549 ^2.076 ^-0.6 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[1f,0.82f,0.86f],scale:0.7} ^-0.777 ^1.729 ^-0.512 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.89f,0.49f,0.58f],scale:0.7} ^-0.899 ^1.297 ^-0.408 0 0 0 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:crimson_spore ^0 ^1.8 ^0 1.2 1.2 1.2 0 4 force @a[tag=player]
execute rotated as @s rotated ~ 0 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4rc","rlk_mb_gd_p4rc0","rlk_mb_gd_p4new"],brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,block_state:{id:"minecraft:red_concrete"},transformation:{translation:[1.016f,1.9322f,-1.0054f],left_rotation:[0.1637f,0.1709f,-0.1146f,0.9648f],scale:[0.02f,0.02f,0.02f],right_rotation:[0f,0f,0f,1f]}}
execute rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
