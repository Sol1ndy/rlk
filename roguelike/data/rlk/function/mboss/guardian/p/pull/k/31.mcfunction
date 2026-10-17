# pull tick 31 (@s = body, at the body).
execute rotated as @s rotated ~ 0 run particle minecraft:dust_color_transition{from_color:[0.75f,0.1f,0.18f],to_color:[0.39f,0.12f,0.1f],scale:1.6} ^0 ^1.9 ^-0.8 0.7 0.9 0.35 0 8 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.174 ^0.867 ^-0.897 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^-0.654 ^2.017 ^0.569 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.62f,0.27f,0.35f],scale:1.3} ^1.022 ^2.876 ^0.352 0.08 0.08 0.08 0 2 force @a[tag=player]
execute rotated as @s rotated ~ 0 run particle minecraft:dust{color:[0.9f,0.2f,0.3f],scale:1} ^-0.3 ^2.95 ^0.9 0.1 0.1 0.1 0 2 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.72f,0.18f,0.23f],scale:1.2} ~ ~1.1 ~ 0.45 0.8 0.45 0 4 force @a[tag=player]
execute at @e[tag=rlk_body,limit=1] run particle minecraft:dust{color:[0.38f,0f,0.02f],scale:1.5} ~ ~1.1 ~ 0.55 0.9 0.55 0 2 force @a[tag=player]
kill @e[type=minecraft:text_display,tag=rlk_mb_gd_p4o]
kill @e[type=minecraft:item_display,tag=rlk_mb_gd_p4st]
execute as @a[tag=player,limit=1] at @s anchored eyes positioned ^ ^ ^0.35 run summon minecraft:text_display ~ ~ ~ {Tags:["rlk_room","rlk_mb_aux","rlk_mb_gd_p4","rlk_mb_gd_p4scr","rlk_mb_gd_p4d"],billboard:"center",brightness:{sky:15,block:15},view_range:2f,teleport_duration:1,interpolation_duration:0,background:-944165831,text:{text:" "},transformation:{translation:[0.08f,-0.1201f,0f],left_rotation:[0f,0f,0.3827f,0.9239f],scale:[2.264f,1.132f,1f],right_rotation:[0f,0f,0f,1f]}}
playsound minecraft:entity.illusioner.mirror_move hostile @a[tag=player] ~ ~ ~ 1 1 0.3
