# D4 원월 사연: one pattern tick (#pt hr = 1..64); events in k/<t>.
execute if score #pt hr matches 1..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 1..7 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 15..27 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 16..32 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 35..37 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 36..42 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 45..47 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 46..52 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 55..56 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 55..63 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 59..63 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/d4/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/d4/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/d4/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/d4/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/d4/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/d4/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/d4/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/d4/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/d4/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/d4/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/d4/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/d4/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/d4/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/d4/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/d4/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/d4/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/d4/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/d4/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/d4/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/d4/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/d4/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/d4/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/d4/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/d4/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/d4/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/d4/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/d4/k/27
execute if score #pt hr matches 28 as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0565f,0.9718f,0.5754f],left_rotation:[-0.2491f,-0.2603f,0.9302f,-0.0701f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 29 as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.053f,0.968f,0.5789f],left_rotation:[-0.2492f,-0.259f,0.9306f,-0.0697f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 30 as @e[type=minecraft:item_display,tag=rlk_hr_tr_d4b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.0494f,0.9642f,0.5824f],left_rotation:[-0.2493f,-0.2577f,0.9309f,-0.0694f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/d4/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/d4/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/d4/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/d4/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/d4/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/d4/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/d4/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/d4/k/38
execute if score #pt hr matches 39 run function rlk:boss/scarlet/p/d4/k/39
execute if score #pt hr matches 40 run function rlk:boss/scarlet/p/d4/k/40
execute if score #pt hr matches 41 run function rlk:boss/scarlet/p/d4/k/41
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/d4/k/42
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/d4/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/d4/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/d4/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/d4/k/46
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/d4/k/47
execute if score #pt hr matches 48 run function rlk:boss/scarlet/p/d4/k/48
execute if score #pt hr matches 49 run function rlk:boss/scarlet/p/d4/k/49
execute if score #pt hr matches 50 run function rlk:boss/scarlet/p/d4/k/50
execute if score #pt hr matches 51 run function rlk:boss/scarlet/p/d4/k/51
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/d4/k/52
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/d4/k/53
execute if score #pt hr matches 54 run function rlk:boss/scarlet/p/d4/k/54
execute if score #pt hr matches 55 run function rlk:boss/scarlet/p/d4/k/55
execute if score #pt hr matches 56 run function rlk:boss/scarlet/p/d4/k/56
execute if score #pt hr matches 57 run function rlk:boss/scarlet/p/d4/k/57
execute if score #pt hr matches 58 run function rlk:boss/scarlet/p/d4/k/58
execute if score #pt hr matches 59 run function rlk:boss/scarlet/p/d4/k/59
execute if score #pt hr matches 60 run function rlk:boss/scarlet/p/d4/k/60
execute if score #pt hr matches 61 run function rlk:boss/scarlet/p/d4/k/61
execute if score #pt hr matches 62 run function rlk:boss/scarlet/p/d4/k/62
execute if score #pt hr matches 63 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_d4_55]
execute if score #pt hr matches 64 run function rlk:boss/scarlet/p/d4/k/64
