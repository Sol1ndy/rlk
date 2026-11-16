# A4 월하 낙참 · 공중 원륜: one pattern tick (#pt hr = 1..46); events in k/<t>.
execute if score #pt hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 6..11 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 21..26 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 35..45 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 39..45 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_a4","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_a4b2"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.2082f,0.7878f,0.2432f],left_rotation:[-0.1946f,0.3182f,-0.0682f,-0.9253f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16771496]}}}}
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a4/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/a4/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/a4/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a4/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/a4/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a4/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a4/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a4/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a4/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a4/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a4/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a4/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a4/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a4/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a4/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a4/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/a4/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a4/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a4/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a4/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a4/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/a4/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a4/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/a4/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a4/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a4/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a4/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a4/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a4/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/a4/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/a4/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a4/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/a4/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/a4/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/a4/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/a4/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/a4/k/38
execute if score #pt hr matches 39 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_31]
execute if score #pt hr matches 40 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a4_32]
execute if score #pt hr matches 46 run scoreboard players set #done hr 1
