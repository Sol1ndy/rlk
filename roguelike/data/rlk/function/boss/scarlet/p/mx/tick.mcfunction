# MX 자광 십자참: one pattern tick (#pt hr = 1..40); events in k/<t>.
execute if score #mx_pre hr matches 1.. run return run function rlk:boss/scarlet/p/mx/pre
execute if score #pt hr matches 1..8 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 17..21 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 29..30 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 29..39 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 33..39 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/mx/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/mx/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/mx/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/mx/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/mx/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/mx/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/mx/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/mx/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/mx/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/mx/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/mx/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/mx/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/mx/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/mx/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/mx/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/mx/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/mx/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/mx/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/mx/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/mx/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/mx/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/mx/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/mx/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/mx/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/mx/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/mx/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/mx/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/mx/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/mx/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/mx/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/mx/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/mx/k/35
execute if score #pt hr matches 36 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_30]
execute if score #pt hr matches 37 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_mx28_31]
execute if score #pt hr matches 40 run scoreboard players set #done hr 1
