# KCUT 황광 난참: one pattern tick (#pt hr = 1..34); events in k/<t>.
execute if score #pt hr matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 23..33 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 27..33 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/kcut/k/3
execute if score #pt hr matches 9 run function rlk:boss/scarlet/p/kcut/k/9
execute if score #pt hr matches 12 run function rlk:boss/scarlet/rig/look/blade/lilac
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/kcut/k/15
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/kcut/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/kcut/k/21
execute if score #pt hr matches 22 run function rlk:boss/scarlet/p/kcut/k/22
execute if score #pt hr matches 23 run kill @e[type=minecraft:marker,tag=rlk_hr_a9s]
execute if score #pt hr matches 26 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 34 run scoreboard players set #done hr 1
