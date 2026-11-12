# A1 회전 반월참: one pattern tick (#pt hr = 1..24); events in k/<t>.
execute if score #pt hr matches 1..3 run function rlk:mboss/mv/turn {max:60}
execute if score #pt hr matches 4..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 15..16 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 15..23 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 19..23 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/a1/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/a1/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/a1/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/a1/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/a1/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/a1/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a1/k/7
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/a1/k/8
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/a1/k/9
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a1/k/10
execute if score #pt hr matches 11 run function rlk:boss/scarlet/p/a1/k/11
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/a1/k/12
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a1/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a1/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/a1/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/a1/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/a1/k/17
execute if score #pt hr matches 18 run function rlk:boss/scarlet/p/a1/k/18
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/a1/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/a1/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/a1/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/a1/k/22
execute if score #pt hr matches 23 run kill @e[type=minecraft:item_display,tag=rlk_hr_tr_a1_15]
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/a1/k/24
