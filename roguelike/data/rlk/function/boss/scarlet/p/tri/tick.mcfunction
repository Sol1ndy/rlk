# TRI 돌진 삼월참: one pattern tick (#pt hr = 1..70); events in k/<t>.
execute if score #pt hr matches 1..6 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 1..11 at @s unless entity @e[tag=rlk_body,limit=1,distance=..6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 15..31 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 16..36 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 39..41 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 40..46 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 49..53 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 50..58 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 61..62 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 61..69 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 65..69 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/tri/k/7
execute if score #pt hr matches 12 run function rlk:boss/scarlet/p/tri/k/12
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/tri/k/14
execute if score #pt hr matches 31 run function rlk:boss/scarlet/p/tri/k/31
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/tri/k/37
execute if score #pt hr matches 38 run function rlk:boss/scarlet/p/tri/k/38
execute if score #pt hr matches 41 run function rlk:boss/scarlet/p/tri/k/41
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/tri/k/47
execute if score #pt hr matches 48 run function rlk:boss/scarlet/p/tri/k/48
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/tri/k/53
execute if score #pt hr matches 59 run function rlk:boss/scarlet/p/tri/k/59
execute if score #pt hr matches 60 run function rlk:boss/scarlet/p/tri/k/60
execute if score #pt hr matches 64 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 70 run scoreboard players set #done hr 1
