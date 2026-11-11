# BLUE 청광 돌파: one pattern tick (#pt hr = 1..32); events in k/<t>.
execute if score #pt hr matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 23..31 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..31 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/blue/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/blue/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/blue/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/blue/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/blue/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/blue/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/blue/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/blue/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/blue/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/blue/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/blue/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/blue/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/blue/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/blue/k/23
execute if score #pt hr matches 24 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_m22]
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/blue/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/blue/k/26
execute if score #pt hr matches 27 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_blue22_21]
execute if score #pt hr matches 28 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_blue22_22]
execute if score #pt hr matches 32 run scoreboard players set #done hr 1
