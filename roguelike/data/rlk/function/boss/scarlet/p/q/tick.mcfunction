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
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/q/k/4
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/q/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/q/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/q/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/q/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/q/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/q/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/q/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/q/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/q/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/q/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/q/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/q/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/q/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/q/k/21
execute if score #pt hr matches 22 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_m20]
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/q/k/23
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/q/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/q/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/q/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/q/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/q/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/q/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/q/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/q/k/38
execute if score #pt hr matches 39 run function rlk:boss/scarlet/p/q/k/39
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
execute if score #pt hr matches 50 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air22_44]
execute if score #pt hr matches 51 run function rlk:boss/scarlet/p/q/k/51
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/q/k/52
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/q/k/53
execute if score #pt hr matches 54 run function rlk:boss/scarlet/p/q/k/54
execute if score #pt hr matches 55 run function rlk:boss/scarlet/p/q/k/55
execute if score #pt hr matches 56 run function rlk:boss/scarlet/p/q/k/56
execute if score #pt hr matches 57 run function rlk:boss/scarlet/p/q/k/57
execute if score #pt hr matches 58 run function rlk:boss/scarlet/p/q/k/58
execute if score #pt hr matches 59 run function rlk:boss/scarlet/p/q/k/59
execute if score #pt hr matches 61 run function rlk:boss/scarlet/p/q/k/61
execute if score #pt hr matches 62 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_swl]
execute if score #pt hr matches 63 run function rlk:boss/scarlet/p/q/k/63
execute if score #pt hr matches 64 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air38_58]
execute if score #pt hr matches 65 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air38_59]
execute if score #pt hr matches 67 run function rlk:boss/scarlet/p/q/k/67
execute if score #pt hr matches 83 run function rlk:boss/scarlet/p/q/k/83
execute if score #pt hr matches 84 run function rlk:boss/scarlet/p/q/k/84
execute if score #pt hr matches 85 run function rlk:boss/scarlet/p/q/k/85
execute if score #pt hr matches 86 run function rlk:boss/scarlet/p/q/k/86
execute if score #pt hr matches 87 run function rlk:boss/scarlet/p/q/k/87
execute if score #pt hr matches 88 run function rlk:boss/scarlet/p/q/k/88
execute if score #pt hr matches 89 run function rlk:boss/scarlet/p/q/k/89
execute if score #pt hr matches 90 run function rlk:boss/scarlet/p/q/k/90
execute if score #pt hr matches 91 run function rlk:boss/scarlet/p/q/k/91
execute if score #pt hr matches 92 run function rlk:boss/scarlet/p/q/k/92
execute if score #pt hr matches 93 run function rlk:boss/scarlet/p/q/k/93
execute if score #pt hr matches 94 run function rlk:boss/scarlet/p/q/k/94
execute if score #pt hr matches 95 run function rlk:boss/scarlet/p/q/k/95
execute if score #pt hr matches 96 if score #q_hit hr matches 1 as @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air74_94] run data modify entity @s item.components."minecraft:item_model" set value "rlk:mboss/hr_kit/sw_arc_1"
execute if score #pt hr matches 97 run function rlk:boss/scarlet/p/q/k/97
execute if score #pt hr matches 98 run function rlk:boss/scarlet/p/q/k/98
execute if score #pt hr matches 99 run function rlk:boss/scarlet/p/q/k/99
execute if score #pt hr matches 100 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air74_94]
execute if score #pt hr matches 101 if score #q_hit hr matches 1 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_q_air74_95]
execute if score #pt hr matches 105 if score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 111 run scoreboard players set #done hr 1
