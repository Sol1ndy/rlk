# HCUT 황광 섬월: one pattern tick (#pt hr = 1..38); events in k/<t>.
execute if score #pt hr matches 1..18 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..37 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 31..37 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/hcut/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/hcut/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/hcut/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/hcut/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/hcut/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/hcut/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/hcut/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/hcut/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/hcut/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/hcut/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/hcut/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/hcut/k/12
execute if score #pt hr matches 13 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3973f,0.5315f,0.0001f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 14 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3983f,0.5276f,-0.0017f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 15 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3994f,0.5238f,-0.0035f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/hcut/k/16
execute if score #pt hr matches 17 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4015f,0.5161f,-0.0072f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 18 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4026f,0.5123f,-0.009f],left_rotation:[-0.5572f,0.646f,-0.4353f,0.2876f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/hcut/k/19
execute if score #pt hr matches 20 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3995f,0.5039f,-0.0453f],left_rotation:[-0.5791f,0.6557f,-0.4055f,0.2649f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 21 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3969f,0.4984f,-0.0703f],left_rotation:[-0.5935f,0.6618f,-0.3845f,0.2491f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 22 as @e[type=minecraft:item_display,tag=rlk_hr_tr_hcutb1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3949f,0.4963f,-0.0817f],left_rotation:[-0.5997f,0.6645f,-0.3747f,0.2418f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/hcut/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/hcut/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/hcut/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/hcut/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/hcut/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/hcut/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/hcut/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/hcut/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/hcut/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/hcut/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/hcut/k/33
execute if score #pt hr matches 34 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_26]
execute if score #pt hr matches 35 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_hcut_27]
execute if score #pt hr matches 38 run scoreboard players set #done hr 1
