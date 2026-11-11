# ULT 공간 참: one pattern tick (#pt hr = 1..58); events in k/<t>.
execute if score #pt hr matches 1..17 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 47..57 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 51..57 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/ult/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/ult/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/ult/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/ult/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/ult/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/ult/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/ult/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/ult/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/ult/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/ult/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/ult/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/ult/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/ult/k/13
execute if score #pt hr matches 14 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.7245f,0.1203f],left_rotation:[-0.6342f,-0.7058f,0.3121f,0.0469f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 15 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.7223f,0.1196f],left_rotation:[-0.6344f,-0.7058f,0.3116f,0.0474f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 16 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.7201f,0.1189f],left_rotation:[-0.6346f,-0.7058f,0.3111f,0.0479f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 17 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.718f,0.1182f],left_rotation:[-0.6349f,-0.7058f,0.3107f,0.0484f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 18 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.7158f,0.1174f],left_rotation:[-0.6351f,-0.7057f,0.3102f,0.0489f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 19 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.7136f,0.1167f],left_rotation:[-0.6353f,-0.7057f,0.3097f,0.0494f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 20 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2548f,0.7115f,0.116f],left_rotation:[-0.6355f,-0.7057f,0.3093f,0.05f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/ult/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/ult/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/ult/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/ult/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/ult/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/ult/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/ult/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/ult/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/ult/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/ult/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/ult/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/ult/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/ult/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/ult/k/34
execute if score #pt hr matches 35 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7089f,1.135f,-0.1041f],left_rotation:[-0.6322f,0.5347f,-0.3167f,0.4627f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 36 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7082f,1.1375f,-0.109f],left_rotation:[-0.6344f,0.5358f,-0.3123f,0.4615f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 37 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7076f,1.14f,-0.1139f],left_rotation:[-0.6365f,0.5368f,-0.308f,0.4602f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 38 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7063f,1.1434f,-0.1207f],left_rotation:[-0.6394f,0.5383f,-0.3018f,0.4585f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 39 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7051f,1.1469f,-0.1276f],left_rotation:[-0.6423f,0.5398f,-0.2957f,0.4568f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 40 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7039f,1.1503f,-0.1344f],left_rotation:[-0.6451f,0.5412f,-0.2895f,0.455f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 41 as @e[type=minecraft:item_display,tag=rlk_hr_tr_ultb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.7034f,1.1514f,-0.1364f],left_rotation:[-0.646f,0.5417f,-0.2876f,0.4545f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/ult/k/42
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/ult/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/ult/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/ult/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/ult/k/46
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/ult/k/47
execute if score #pt hr matches 48 run function rlk:boss/scarlet/p/ult/k/48
execute if score #pt hr matches 49 run function rlk:boss/scarlet/p/ult/k/49
execute if score #pt hr matches 50 run function rlk:boss/scarlet/p/ult/k/50
execute if score #pt hr matches 51 run function rlk:boss/scarlet/p/ult/k/51
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/ult/k/52
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/ult/k/53
execute if score #pt hr matches 54 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_46]
execute if score #pt hr matches 55 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_ult_47]
execute if score #pt hr matches 58 run scoreboard players set #done hr 1
