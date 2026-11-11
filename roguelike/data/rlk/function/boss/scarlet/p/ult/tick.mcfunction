# ULT 공간 참: one pattern tick (#pt hr = 1..58); events in k/<t>.
execute if score #pt hr matches 1..17 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 47..57 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 51..57 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/ult/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/ult/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/ult/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/ult/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/ult/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/ult/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/ult/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/ult/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/ult/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/ult/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/ult/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/ult/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/ult/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/ult/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/ult/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/ult/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/ult/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/ult/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/ult/k/30
execute if score #pt hr matches 31 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_ult24_25]
execute if score #pt hr matches 32 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_ult24_26]
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/ult/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/ult/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/ult/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/ult/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/ult/k/38
execute if score #pt hr matches 39 run function rlk:boss/scarlet/p/ult/k/39
execute if score #pt hr matches 40 run function rlk:boss/scarlet/p/ult/k/40
execute if score #pt hr matches 41 run function rlk:boss/scarlet/p/ult/k/41
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/ult/k/42
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/ult/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/ult/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/ult/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/ult/k/46
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/ult/k/47
execute if score #pt hr matches 48 run function rlk:boss/scarlet/p/ult/k/48
execute if score #pt hr matches 49 run function rlk:boss/scarlet/p/ult/k/49
execute if score #pt hr matches 50 run function rlk:boss/scarlet/p/ult/k/50
execute if score #pt hr matches 51 run function rlk:boss/scarlet/p/ult/k/51
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/ult/k/52
execute if score #pt hr matches 53 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_47]
execute if score #pt hr matches 54 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_ult46_48]
execute if score #pt hr matches 58 run scoreboard players set #done hr 1
