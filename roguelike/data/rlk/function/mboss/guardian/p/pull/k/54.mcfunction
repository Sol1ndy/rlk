# pull tick 54 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4ca00] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,1.9f,0f],left_rotation:[0f,-0.4384f,0f,0.8988f],scale:[-0.2742f,0.2742f,0.2742f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cr","rlk_mb_gd_p4ca20","rlk_mb_gd_p4new"],billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,1.9f,0f],left_rotation:[0f,-0.9903f,0f,-0.1392f],scale:[-13.7113f,13.7113f,13.7113f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:navia_fx/crescent"}}}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^1.9 ^4.914 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^4.674 ^1.9 ^1.519 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^2.888 ^1.9 ^-3.976 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-2.888 ^1.9 ^-3.976 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-4.674 ^1.9 ^1.519 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.9 ^0 3.709 0.3 3.709 0 3 force @a[tag=player]
