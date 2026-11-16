# KCUT 황광 난참: one pattern tick (#pt hr = 1..34); events in k/<t>.
execute if score #pt hr matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 23..33 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..33 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/kcut/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/kcut/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/kcut/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/kcut/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/kcut/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/kcut/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/kcut/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/kcut/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/kcut/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/kcut/k/10
execute if score #pt hr matches 11 as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2723f,0.7785f,-0.118f],left_rotation:[-0.954f,0.0204f,0.0667f,0.2917f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/kcut/k/12
execute if score #pt hr matches 13 as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.274f,0.7798f,-0.132f],left_rotation:[-0.954f,0.0204f,0.0667f,0.2917f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 14 as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2742f,0.7714f,-0.139f],left_rotation:[-0.954f,0.0204f,0.0667f,0.2917f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/kcut/k/15
execute if score #pt hr matches 16 as @e[type=minecraft:item_display,tag=rlk_hr_tr_kcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.2742f,0.791f,-0.139f],left_rotation:[-0.954f,0.0204f,0.0667f,0.2917f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/kcut/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/kcut/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/kcut/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/kcut/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/kcut/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/kcut/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/kcut/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/kcut/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/kcut/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/kcut/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/kcut/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/kcut/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/kcut/k/29
execute if score #pt hr matches 30 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_kcut_22]
execute if score #pt hr matches 34 run scoreboard players set #done hr 1
