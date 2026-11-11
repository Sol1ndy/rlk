# KCUT 황광 난참: one pattern tick (#pt hr = 1..34); events in k/<t>.
execute if score #pt hr matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 23..33 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..33 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/kcut/k/3
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/kcut/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/kcut/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/kcut/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/kcut/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/kcut/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/kcut/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/kcut/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/kcut/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/kcut/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/kcut/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/kcut/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/kcut/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/kcut/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/kcut/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/kcut/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/kcut/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/kcut/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/kcut/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/kcut/k/27
execute if score #pt hr matches 28 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_kcut22_22]
execute if score #pt hr matches 29 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_kcut22_23]
execute if score #pt hr matches 34 run scoreboard players set #done hr 1
