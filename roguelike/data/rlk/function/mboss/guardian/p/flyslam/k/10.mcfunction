# flyslam clip tick 10
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c2_1]
kill @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c4_0]
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c10_0,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[0.288f,2.524f,0.154f],left_rotation:[0.543f,-0.54f,0.532f,-0.362f],scale:[0.01f,0.01f,0.01f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c10_1,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:5,transformation:{translation:[0.389f,2.837f,0.231f],left_rotation:[0.379f,-0.657f,0.631f,-0.162f],scale:[0.019f,0.019f,0.019f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:block_display,tag=rlk_mb_gd_q5c12_0,limit=1] run data merge entity @s {start_interpolation:0,interpolation_duration:6,transformation:{translation:[-0.19f,2.424f,-0.201f],left_rotation:[0.055f,-0.176f,-0.856f,-0.484f],scale:[0.013f,0.013f,0.013f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^-0.48 ^2.71 ^0.48 positioned ^0.02 ^-0.287 ^-0.052 run summon minecraft:block_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p5","rlk_mb_gd_q5c12","rlk_mb_gd_q5c12_1"],block_state:{id:"minecraft:brown_terracotta"},brightness:{sky:11,block:11},view_range:0.7f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0.087f,0.034f,0.028f],left_rotation:[0.165f,-0.781f,0.553f,0.241f],scale:[0.113f,0.113f,0.113f],right_rotation:[0f,0f,0f,1f]}}
execute at @s rotated as @s rotated ~ 0 positioned ^0.987 ^0.25 ^0.359 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.912 ^0.721 ^-0.445 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.302 ^1.193 ^-0.931 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.443 ^1.664 ^-0.832 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.872 ^2.136 ^-0.25 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.755 ^2.607 ^0.436 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.202 ^3.079 ^0.811 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.424 ^3.55 ^0.678 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.987 ^0.25 ^-0.359 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.912 ^0.721 ^0.445 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.302 ^1.193 ^0.931 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.443 ^1.664 ^0.832 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.872 ^2.136 ^0.25 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.755 ^2.607 ^-0.436 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^0.202 ^3.079 ^-0.811 run particle minecraft:dust{color:[0.976f,0.91f,0.647f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
execute at @s rotated as @s rotated ~ 0 positioned ^-0.424 ^3.55 ^-0.678 run particle minecraft:dust{color:[0.796f,0.647f,0.51f],scale:0.9} ~ ~ ~ 0.02 0.02 0.02 0 1 force @a[tag=player]
