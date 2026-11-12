# A10 황광 낙참: one pattern tick (#pt hr = 1..32); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 9..13 run function rlk:boss/scarlet/p/a10/drift
execute if score #pt hr matches 9..13 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 23..31 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..31 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a10","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_a10b2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1494f,0.913f,0.5253f],left_rotation:[-0.2405f,0.2506f,-0.0645f,-0.9355f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16769354]}}}}
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a10/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/a10/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/a10/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a10/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/a10/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a10/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a10/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a10/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a10/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a10/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a10/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a10/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a10/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a10/k/15
execute if score #pt hr matches 16 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[-0.0011f,1.7042f,0.7018f],left_rotation:[-0.7373f,0f,0f,0.6756f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 17 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0027f,1.7245f,0.7027f],left_rotation:[-0.7373f,0f,0f,0.6756f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 18 as @e[type=minecraft:item_display,tag=rlk_hr_tr_a10b2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0065f,1.7449f,0.7037f],left_rotation:[-0.7373f,0f,0f,0.6756f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a10/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a10/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a10/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a10/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/a10/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a10/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/a10/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a10/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a10/k/27
execute if score #pt hr matches 28 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a10_20]
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a10/k/29
execute if score #pt hr matches 32 run scoreboard players set #done hr 1
