# C2 연속기 · 블링크 Ⅱ: one pattern tick (#pt tk = 1..74); events in k/<t>.
execute if score #pt tk matches 1..4 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 13..16 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 25..30 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 26..30 at @s unless entity @e[tag=rlk_body,distance=..3,limit=1] run function rlk:mboss/mv/step {d:0.15}
execute if score #pt tk matches 11 run function rlk:boss/tachy/p/c2/k/11
execute if score #pt tk matches 12 run function rlk:boss/tachy/p/c2/k/12
execute if score #pt tk matches 23 run function rlk:boss/tachy/p/c2/k/23
execute if score #pt tk matches 24 run function rlk:boss/tachy/p/c2/k/24
execute if score #pt tk matches 37 run function rlk:boss/tachy/p/c2/k/37
execute if score #pt tk matches 38 run function rlk:boss/tachy/p/c2/k/38
execute if score #pt tk matches 50 run function rlk:boss/tachy/p/c2/k/50
execute if score #pt tk matches 67 run function rlk:boss/tachy/p/c2/k/67
execute if score #pt tk matches 68 run function rlk:boss/tachy/p/c2/k/68
execute if score #pt tk matches 69 run function rlk:boss/tachy/p/c2/k/69
execute if score #pt tk matches 70 run function rlk:boss/tachy/p/c2/k/70
execute if score #pt tk matches 71 run function rlk:boss/tachy/p/c2/k/71
execute if score #pt tk matches 74 run scoreboard players set #done tk 1
