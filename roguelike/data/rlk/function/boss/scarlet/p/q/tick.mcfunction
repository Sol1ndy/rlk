# Q 자영 포박 · 천공 낙월: one pattern tick (#pt hr = 1..111); events in k/<t>.
execute if score #pt hr matches 1..12 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 22..33 unless score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 32..33 unless score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 31..35 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 44..51 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 60..66 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 73..87 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 96..110 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 106..110 if score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/q/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/q/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/q/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/q/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/q/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/q/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/q/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/q/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/q/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/q/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/q/k/11
execute if score #pt hr matches 12 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3931f,0.6882f,0.0271f],left_rotation:[-0.5214f,0.6578f,-0.4778f,0.2591f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/q/k/13
execute if score #pt hr matches 14 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q0b1] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.482f,0.6614f,-0.0209f],left_rotation:[-0.527f,0.6546f,-0.472f,0.2665f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/q/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/q/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/q/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/q/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/q/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/q/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/q/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/q/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/q/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/q/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/q/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/q/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/q/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/q/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/q/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/q/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/q/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/q/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/q/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/q/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/q/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/q/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/q/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/q/k/38
execute if score #pt hr matches 39 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3299f,2.0072f,0.727f],left_rotation:[-0.7553f,-0.2899f,0.2106f,0.5488f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 40 run function rlk:boss/scarlet/p/q/k/40
execute if score #pt hr matches 41 run function rlk:boss/scarlet/p/q/k/41
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/q/k/42
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/q/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/q/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/q/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/q/k/46
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/q/k/47
execute if score #pt hr matches 48 run function rlk:boss/scarlet/p/q/k/48
execute if score #pt hr matches 49 run function rlk:boss/scarlet/p/q/k/49
execute if score #pt hr matches 50 run function rlk:boss/scarlet/p/q/k/50
execute if score #pt hr matches 51 run function rlk:boss/scarlet/p/q/k/51
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/q/k/52
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/q/k/53
execute if score #pt hr matches 54 run function rlk:boss/scarlet/p/q/k/54
execute if score #pt hr matches 55 run function rlk:boss/scarlet/p/q/k/55
execute if score #pt hr matches 56 run function rlk:boss/scarlet/p/q/k/56
execute if score #pt hr matches 57 run function rlk:boss/scarlet/p/q/k/57
execute if score #pt hr matches 58 run function rlk:boss/scarlet/p/q/k/58
execute if score #pt hr matches 59 run function rlk:boss/scarlet/p/q/k/59
execute if score #pt hr matches 60 run function rlk:boss/scarlet/p/q/k/60
execute if score #pt hr matches 61 run function rlk:boss/scarlet/p/q/k/61
execute if score #pt hr matches 62 run function rlk:boss/scarlet/p/q/k/62
execute if score #pt hr matches 63 run function rlk:boss/scarlet/p/q/k/63
execute if score #pt hr matches 64 run function rlk:boss/scarlet/p/q/k/64
execute if score #pt hr matches 65 run function rlk:boss/scarlet/p/q/k/65
execute if score #pt hr matches 66 run function rlk:boss/scarlet/p/q/k/66
execute if score #pt hr matches 67 run function rlk:boss/scarlet/p/q/k/67
execute if score #pt hr matches 68 run function rlk:boss/scarlet/p/q/k/68
execute if score #pt hr matches 69 run function rlk:boss/scarlet/p/q/k/69
execute if score #pt hr matches 70 run function rlk:boss/scarlet/p/q/k/70
execute if score #pt hr matches 71 run function rlk:boss/scarlet/p/q/k/71
execute if score #pt hr matches 72 run function rlk:boss/scarlet/p/q/k/72
execute if score #pt hr matches 73 run function rlk:boss/scarlet/p/q/k/73
execute if score #pt hr matches 74 run function rlk:boss/scarlet/p/q/k/74
execute if score #pt hr matches 75 run function rlk:boss/scarlet/p/q/k/75
execute if score #pt hr matches 76 run function rlk:boss/scarlet/p/q/k/76
execute if score #pt hr matches 77 run function rlk:boss/scarlet/p/q/k/77
execute if score #pt hr matches 78 run function rlk:boss/scarlet/p/q/k/78
execute if score #pt hr matches 79 run function rlk:boss/scarlet/p/q/k/79
execute if score #pt hr matches 80 run function rlk:boss/scarlet/p/q/k/80
execute if score #pt hr matches 81 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4018f,2.2448f,-0.0592f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 82 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4015f,2.2468f,-0.0608f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 83 run function rlk:boss/scarlet/p/q/k/83
execute if score #pt hr matches 84 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4008f,2.2507f,-0.0641f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 85 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4005f,2.2527f,-0.0658f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 86 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4001f,2.2546f,-0.0675f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 87 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.3998f,2.2566f,-0.0692f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 88 run function rlk:boss/scarlet/p/q/k/88
execute if score #pt hr matches 89 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4005f,2.2615f,-0.0658f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 90 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4009f,2.264f,-0.0641f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 91 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1b21] run data merge entity @s {start_interpolation:0,interpolation_duration:1,transformation:{translation:[0.4013f,2.2664f,-0.0625f],left_rotation:[-0.5087f,-0.5087f,-0.4912f,0.4912f],scale:[0.26f,0.26f,1.6f],right_rotation:[0f,0f,0f,1f]}}
execute if score #pt hr matches 92 run function rlk:boss/scarlet/p/q/k/92
execute if score #pt hr matches 93 run function rlk:boss/scarlet/p/q/k/93
execute if score #pt hr matches 94 run function rlk:boss/scarlet/p/q/k/94
execute if score #pt hr matches 95 run function rlk:boss/scarlet/p/q/k/95
execute if score #pt hr matches 96 run function rlk:boss/scarlet/p/q/k/96
execute if score #pt hr matches 97 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_93] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_fan_1"
execute if score #pt hr matches 98 run function rlk:boss/scarlet/p/q/k/98
execute if score #pt hr matches 99 run function rlk:boss/scarlet/p/q/k/99
execute if score #pt hr matches 100 run function rlk:boss/scarlet/p/q/k/100
execute if score #pt hr matches 101 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_93]
execute if score #pt hr matches 102 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_q1_94]
execute if score #pt hr matches 105 if score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 111 run scoreboard players set #done hr 1
