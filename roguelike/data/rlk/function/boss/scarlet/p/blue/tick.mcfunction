# BLUE 청광 돌파: one pattern tick (#pt hr = 1..32); events in k/<t>.
execute if score #pt hr matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 23..31 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..31 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/blue/k/15
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/blue/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/blue/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/blue/k/22
execute if score #pt hr matches 23 run kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
execute if score #pt hr matches 26 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 32 run scoreboard players set #done hr 1
