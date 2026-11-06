# C3 붉은 핵 연속기: one pattern tick (#pt tk = 1..104); events in k/<t>.
execute if score #pt tk matches 1..14 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 2..20 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt tk matches 23..24 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 24..30 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.22}
execute if score #pt tk matches 33..36 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 34..42 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.22}
execute if score #pt tk matches 45..52 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 46..58 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt tk matches 61..62 run function rlk:mboss/mv/turn {max:10}
execute if score #pt tk matches 62..68 at @s unless entity @e[tag=rlk_body,distance=..2.4,limit=1] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt tk matches 21 run function rlk:boss/tachy/p/c3/k/21
execute if score #pt tk matches 22 run function rlk:boss/tachy/p/c3/k/22
execute if score #pt tk matches 31 run function rlk:boss/tachy/p/c3/k/31
execute if score #pt tk matches 32 run function rlk:boss/tachy/p/c3/k/32
execute if score #pt tk matches 43 run function rlk:boss/tachy/p/c3/k/43
execute if score #pt tk matches 44 run function rlk:boss/tachy/p/c3/k/44
execute if score #pt tk matches 59 run function rlk:boss/tachy/p/c3/k/59
execute if score #pt tk matches 60 run function rlk:boss/tachy/p/c3/k/60
execute if score #pt tk matches 69 run function rlk:boss/tachy/p/c3/k/69
execute if score #pt tk matches 70 run function rlk:boss/tachy/p/c3/k/70
execute if score #pt tk matches 80 run function rlk:boss/tachy/p/c3/k/80
execute if score #pt tk matches 97 run function rlk:boss/tachy/p/c3/k/97
execute if score #pt tk matches 98 run function rlk:boss/tachy/p/c3/k/98
execute if score #pt tk matches 99 run function rlk:boss/tachy/p/c3/k/99
execute if score #pt tk matches 100 run function rlk:boss/tachy/p/c3/k/100
execute if score #pt tk matches 101 run function rlk:boss/tachy/p/c3/k/101
execute if score #pt tk matches 104 run scoreboard players set #done tk 1
