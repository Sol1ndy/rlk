# C1 연속기 · 블링크: one pattern tick (#pt tk = 1..92); events in k/<t>.
execute if score #pt tk matches 1..6 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 2..12 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt tk matches 15..24 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 16..30 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt tk matches 33..38 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 34..44 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.22}
execute if score #pt tk matches 47..50 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 48..56 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt tk matches 13 run function rlk:boss/tachy/p/c1/k/13
execute if score #pt tk matches 14 run function rlk:boss/tachy/p/c1/k/14
execute if score #pt tk matches 31 run function rlk:boss/tachy/p/c1/k/31
execute if score #pt tk matches 32 run function rlk:boss/tachy/p/c1/k/32
execute if score #pt tk matches 45 run function rlk:boss/tachy/p/c1/k/45
execute if score #pt tk matches 46 run function rlk:boss/tachy/p/c1/k/46
execute if score #pt tk matches 57 run function rlk:boss/tachy/p/c1/k/57
execute if score #pt tk matches 58 run function rlk:boss/tachy/p/c1/k/58
execute if score #pt tk matches 68 run function rlk:boss/tachy/p/c1/k/68
execute if score #pt tk matches 85 run function rlk:boss/tachy/p/c1/k/85
execute if score #pt tk matches 86 run function rlk:boss/tachy/p/c1/k/86
execute if score #pt tk matches 87 run function rlk:boss/tachy/p/c1/k/87
execute if score #pt tk matches 88 run function rlk:boss/tachy/p/c1/k/88
execute if score #pt tk matches 89 run function rlk:boss/tachy/p/c1/k/89
execute if score #pt tk matches 92 run scoreboard players set #done tk 1
