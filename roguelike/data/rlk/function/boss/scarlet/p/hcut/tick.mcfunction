# HCUT 황광 섬월: one pattern tick (#pt hr = 1..38); events in k/<t>.
execute if score #pt hr matches 1..18 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..37 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 31..37 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/hcut/k/2
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/hcut/k/8
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/hcut/k/12
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/hcut/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/hcut/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/hcut/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/hcut/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/hcut/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/hcut/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/hcut/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/hcut/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/hcut/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/hcut/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/hcut/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/hcut/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/hcut/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/hcut/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/hcut/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/hcut/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/hcut/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/hcut/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/hcut/k/32
execute if score #pt hr matches 33 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_hcut26_27]
execute if score #pt hr matches 34 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_hcut26_28]
execute if score #pt hr matches 38 run scoreboard players set #done hr 1
