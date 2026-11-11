# TRI 돌진 삼월참: one pattern tick (#pt hr = 1..70); events in k/<t>.
execute if score #pt hr matches 1..6 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 1..11 at @s unless entity @e[tag=rlk_body,limit=1,distance=..6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 15..31 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 16..36 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 39..41 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 40..46 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 49..53 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 50..58 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 61..62 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 61..69 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 65..69 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 2 run summon minecraft:item_display ~ ~ ~ {Tags:["rlk_hr_tr","rlk_mb_part","rlk_room","rlk_mb_aux","rlk_hr_p","rlk_hr_p_tri","rlk_hr_trr","rlk_hr_trb","rlk_hr_tr_trib3"],billboard:"fixed",item_display:"none",brightness:{sky:15,block:15},view_range:2f,shadow_radius:0f,teleport_duration:1,interpolation_duration:1,transformation:{translation:[0.3189f,0.9033f,-0.0305f],left_rotation:[-0.0609f,0.0783f,0.0048f,0.9951f],scale:[0f,0f,0f],right_rotation:[0f,0f,0f,1f]},item:{id:"minecraft:paper",count:1,components:{"minecraft:item_model":"rlk:mboss/hr_kit/sw_band","minecraft:custom_model_data":{colors:[16771496]}}}}
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/tri/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/tri/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/tri/k/5
execute if score #pt hr matches 6 as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3251f,0.8692f,-0.1009f],left_rotation:[-0.1207f,0.1381f,0.017f,0.9829f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/tri/k/7
execute if score #pt hr matches 8 as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3206f,0.8578f,-0.1229f],left_rotation:[-0.1207f,0.1381f,0.017f,0.9829f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/tri/k/9
execute if score #pt hr matches 10 as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.316f,0.8463f,-0.1449f],left_rotation:[-0.1207f,0.1381f,0.017f,0.9829f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/tri/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/tri/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/tri/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/tri/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/tri/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/tri/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/tri/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/tri/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/tri/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/tri/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/tri/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/tri/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/tri/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/tri/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/tri/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/tri/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/tri/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/tri/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/tri/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/tri/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/tri/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/tri/k/32
execute if score #pt hr matches 33 as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.097f,1.442f,0.575f],left_rotation:[-0.7497f,-0.4156f,0.2497f,0.4505f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 34 as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0597f,1.3563f,0.5432f],left_rotation:[-0.7497f,-0.4156f,0.2497f,0.4505f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 35 as @e[type=minecraft:item_display,tag=rlk_hr_tr_trib3] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.1411f,1.337f,0.5826f],left_rotation:[-0.7497f,-0.4156f,0.2497f,0.4505f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/tri/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/tri/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/tri/k/38
execute if score #pt hr matches 39 run function rlk:boss/scarlet/p/tri/k/39
execute if score #pt hr matches 40 run function rlk:boss/scarlet/p/tri/k/40
execute if score #pt hr matches 41 run function rlk:boss/scarlet/p/tri/k/41
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/tri/k/42
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/tri/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/tri/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/tri/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/tri/k/46
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/tri/k/47
execute if score #pt hr matches 48 run function rlk:boss/scarlet/p/tri/k/48
execute if score #pt hr matches 49 run function rlk:boss/scarlet/p/tri/k/49
execute if score #pt hr matches 50 run function rlk:boss/scarlet/p/tri/k/50
execute if score #pt hr matches 51 run function rlk:boss/scarlet/p/tri/k/51
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/tri/k/52
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/tri/k/53
execute if score #pt hr matches 54 run function rlk:boss/scarlet/p/tri/k/54
execute if score #pt hr matches 55 run function rlk:boss/scarlet/p/tri/k/55
execute if score #pt hr matches 56 run function rlk:boss/scarlet/p/tri/k/56
execute if score #pt hr matches 57 run function rlk:boss/scarlet/p/tri/k/57
execute if score #pt hr matches 58 run function rlk:boss/scarlet/p/tri/k/58
execute if score #pt hr matches 59 run function rlk:boss/scarlet/p/tri/k/59
execute if score #pt hr matches 60 run function rlk:boss/scarlet/p/tri/k/60
execute if score #pt hr matches 61 run function rlk:boss/scarlet/p/tri/k/61
execute if score #pt hr matches 62 run function rlk:boss/scarlet/p/tri/k/62
execute if score #pt hr matches 63 run function rlk:boss/scarlet/p/tri/k/63
execute if score #pt hr matches 64 run function rlk:boss/scarlet/p/tri/k/64
execute if score #pt hr matches 65 run function rlk:boss/scarlet/p/tri/k/65
execute if score #pt hr matches 66 run function rlk:boss/scarlet/p/tri/k/66
execute if score #pt hr matches 67 run function rlk:boss/scarlet/p/tri/k/67
execute if score #pt hr matches 68 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_60]
execute if score #pt hr matches 69 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_tri_61]
execute if score #pt hr matches 70 run scoreboard players set #done hr 1
