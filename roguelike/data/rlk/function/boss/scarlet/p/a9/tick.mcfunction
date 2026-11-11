# A9 황광 원참: one pattern tick (#pt hr = 1..40); events in k/<t>.
execute if score #pt hr matches 1..20 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 29..39 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 33..39 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/a9/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a9/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/a9/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/a9/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a9/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/a9/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a9/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a9/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a9/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a9/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a9/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a9/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a9/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a9/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a9/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a9/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a9/k/17
execute if score #pt hr matches 18 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2853f,0.7424f,0.1349f],left_rotation:[-0.6645f,-0.6964f,0.2418f,0.1228f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 19 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2855f,0.7378f,0.1323f],left_rotation:[-0.6645f,-0.6964f,0.2418f,0.1228f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 20 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2857f,0.7331f,0.1296f],left_rotation:[-0.6645f,-0.6964f,0.2418f,0.1228f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a9/k/21
execute if score #pt hr matches 22 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2926f,0.7465f,0.137f],left_rotation:[-0.6668f,-0.6975f,0.2354f,0.116f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 23 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a9b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.2765f,0.7482f,0.2382f],left_rotation:[-0.6733f,-0.7006f,0.2159f,0.0957f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a9/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/a9/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a9/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a9/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a9/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a9/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a9/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/a9/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/a9/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a9/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/a9/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/a9/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/a9/k/36
execute if score #pt hr matches 37 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_29]
execute if score #pt hr matches 38 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a9_30]
execute if score #pt hr matches 40 run scoreboard players set #done hr 1
