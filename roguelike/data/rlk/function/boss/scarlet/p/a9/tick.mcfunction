# A9 황광 원참: one pattern tick (#pt hr = 1..40); events in k/<t>.
execute if score #pt hr matches 1..20 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 29..39 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 33..39 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/a9/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a9/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/a9/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a9/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a9/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a9/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a9/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a9/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a9/k/12
execute if score #pt hr matches 13 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a9f3_7]
execute if score #pt hr matches 14 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a9f3_8]
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a9/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a9/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/a9/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a9/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a9/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a9/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a9/k/22
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/a9/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a9/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/a9/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/a9/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/a9/k/27
execute if score #pt hr matches 28 run function rlk:boss/scarlet/p/a9/k/28
execute if score #pt hr matches 29 run function rlk:boss/scarlet/p/a9/k/29
execute if score #pt hr matches 30 run function rlk:boss/scarlet/p/a9/k/30
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/a9/k/31
execute if score #pt hr matches 32 run function rlk:boss/scarlet/p/a9/k/32
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/a9/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/a9/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/a9/k/35
execute if score #pt hr matches 36 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a928_30]
execute if score #pt hr matches 37 run kill @e[type=minecraft:item_display,tag=rlk_hr_sw_a928_31]
execute if score #pt hr matches 40 run scoreboard players set #done hr 1
