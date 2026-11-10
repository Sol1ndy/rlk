# HCUT 황광 섬월: one pattern tick (#pt hr = 1..38); events in k/<t>.
execute if score #pt hr matches 1..18 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..37 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 31..37 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/hcut/k/2
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/hcut/k/8
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/hcut/k/12
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/hcut/k/16
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/hcut/k/19
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/hcut/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/hcut/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/hcut/k/26
execute if score #pt hr matches 27 run kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
execute if score #pt hr matches 30 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 38 run scoreboard players set #done hr 1
