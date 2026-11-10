# ULT 공간 참: one pattern tick (#pt hr = 1..58); events in k/<t>.
execute if score #pt hr matches 1..17 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 47..57 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 51..57 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/ult/k/12
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/ult/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/ult/k/24
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/ult/k/26
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/ult/k/34
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/ult/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/ult/k/46
execute if score #pt hr matches 50 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 58 run scoreboard players set #done hr 1
