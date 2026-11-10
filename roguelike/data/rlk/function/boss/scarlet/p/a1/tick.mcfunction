# A1 회전 반월참: one pattern tick (#pt hr = 1..24); events in k/<t>.
execute if score #pt hr matches 1..3 run function rlk:mboss/mv/turn {max:60}
execute if score #pt hr matches 4..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 15..16 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 15..23 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 19..23 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/a1/k/7
execute if score #pt hr matches 10 run function rlk:boss/scarlet/p/a1/k/10
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/a1/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/a1/k/14
execute if score #pt hr matches 18 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 24 run scoreboard players set #done hr 1
