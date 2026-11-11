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
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/tri/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/tri/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/tri/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/tri/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/tri/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/tri/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/tri/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/tri/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/tri/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/tri/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/tri/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/tri/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/tri/k/14
execute if score #pt hr matches 16 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_m14]
execute if score #pt hr matches 17 run kill @e[type=minecraft:item_display,tag=rlk_hr_swl]
execute if score #pt hr matches 18 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri14_12]
execute if score #pt hr matches 19 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri14_13]
execute if score #pt hr matches 20 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri14_14]
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/tri/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/tri/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/tri/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/tri/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/tri/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/tri/k/35
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
execute if score #pt hr matches 67 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri60_61]
execute if score #pt hr matches 68 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_tri60_62]
execute if score #pt hr matches 70 run scoreboard players set #done hr 1
