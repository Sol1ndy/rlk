# NB 낙월 사선: one pattern tick (#pt hr = 1..52); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 8..12 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 21..22 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 31..32 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 41..51 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 47..51 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_nb","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_nbb2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.1452f,0.9516f,0.5088f],left_rotation:[-0.25f,0.25f,-0.067f,-0.933f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16771496]}}}}
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/nb/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/nb/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/nb/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/nb/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/nb/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/nb/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/nb/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/nb/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/nb/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/nb/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/nb/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/nb/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/nb/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/nb/k/15
execute if score #pt hr matches 16 as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3383f,1.8823f,0.769f],left_rotation:[-0.6823f,-0.1243f,0.391f,0.6051f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 17 as @e[type=minecraft:item_display,tag=rlk_hr_tr_nbb2] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3871f,1.9082f,0.6744f],left_rotation:[-0.6823f,-0.1243f,0.391f,0.6051f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/nb/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/nb/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/nb/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/nb/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/nb/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/nb/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/nb/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/nb/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/nb/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/nb/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/nb/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/nb/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/nb/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/nb/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/nb/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/nb/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/nb/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/nb/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/nb/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/nb/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/nb/k/38
execute if score #pt hr matches 39 run function rlk:boss/scarlet/p/nb/k/39
execute if score #pt hr matches 40 run function rlk:boss/scarlet/p/nb/k/40
execute if score #pt hr matches 41 run function rlk:boss/scarlet/p/nb/k/41
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/nb/k/42
execute if score #pt hr matches 43 as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_39] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/nb/k/44
execute if score #pt hr matches 45 as @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_39] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_2"
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/nb/k/46
execute if score #pt hr matches 47 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_39]
execute if score #pt hr matches 48 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_nb_40]
execute if score #pt hr matches 52 run scoreboard players set #done hr 1
