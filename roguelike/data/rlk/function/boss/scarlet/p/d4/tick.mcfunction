# D4 원월 사연: one pattern tick (#pt hr = 1..64); events in k/<t>.
execute if score #pt hr matches 1..7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 1..7 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 15..27 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 16..32 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 35..37 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 36..42 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 45..47 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 46..52 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.4] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt hr matches 55..56 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 55..63 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 59..63 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/d4/k/7
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/d4/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/d4/k/14
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/d4/k/27
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/d4/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/d4/k/34
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/d4/k/37
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/d4/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/d4/k/44
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/d4/k/47
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/d4/k/53
execute if score #pt hr matches 54 run function rlk:boss/scarlet/p/d4/k/54
execute if score #pt hr matches 58 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 64 run scoreboard players set #done hr 1
