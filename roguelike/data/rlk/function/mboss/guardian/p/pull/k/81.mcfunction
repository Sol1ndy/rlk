# pull tick 81 (@s = body, at the body).
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb00] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0939f,-0.1985f,-0.0191f,0.9754f],scale:[0.2206f,0.2206f,0.2206f],right_rotation:[0f,0f,0f,1f]}}
execute as @e[type=minecraft:item_display,tag=rlk_mb_gd_p4cb01] run data merge entity @s {start_interpolation:0,interpolation_duration:3,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0939f,-0.1985f,-0.0191f,0.9754f],scale:[0.1721f,0.1721f,0.1721f],right_rotation:[0f,0f,0f,1f]}}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cr","rlk_mb_gd_p4cb20","rlk_mb_gd_p4new"],billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0622f,0.7569f,0.0729f,0.6465f],scale:[11.0309f,11.0309f,11.0309f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:navia_fx/crescent"}}}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4cr","rlk_mb_gd_p4cb21","rlk_mb_gd_p4new"],billboard:"fixed",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:0,interpolation_duration:0,transformation:{translation:[0f,1.5f,0f],left_rotation:[0.0622f,0.7569f,0.0729f,0.6465f],scale:[8.6041f,8.6041f,8.6041f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:navia_fx/crescent"}}}
execute positioned ~ 201 ~ rotated as @s rotated ~ 0 run tp @e[tag=rlk_mb_gd_p4new] ~ ~ ~ ~ 0
tag @e[tag=rlk_mb_gd_p4new] remove rlk_mb_gd_p4new
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^2.417 ^0.853 ^3.327 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^3.911 ^1.747 ^-1.271 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:falling_dust{block_state:"minecraft:black_concrete"} ^0 ^2.299 ^-4.112 0.2 0.1 0.2 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-3.911 ^1.747 ^-1.271 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:wax_on ^-2.417 ^0.853 ^3.327 0.3 0.2 0.3 0 1 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.23f,0.15f,0.12f],scale:0.9} ^0 ^1.5 ^0 3 0.3 3 0 3 force @a[tag=player]
