# B2 옆걸음 4연격: one pattern tick (#pt tk = 1..78); events in k/<t>.
execute if score #pt tk matches 18..21 at @s unless entity @e[tag=rlk_body,distance=..2.2,limit=1] run function rlk:mboss/mv/step {d:0.375}
execute if score #pt tk matches 23..36 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 45..46 run function rlk:mboss/mv/turn {max:8}
execute if score #pt tk matches 55..56 run function rlk:mboss/mv/turn {max:8}
execute if score #pt tk matches 12 run function rlk:mboss/mv/face
execute if score #pt tk matches 21 run function rlk:boss/tachy/p/b2/k/21
execute if score #pt tk matches 22 run function rlk:boss/tachy/p/b2/k/22
execute if score #pt tk matches 30 run function rlk:boss/tachy/p/b2/k/30
execute if score #pt tk matches 43 run function rlk:boss/tachy/p/b2/k/43
execute if score #pt tk matches 44 run function rlk:boss/tachy/p/b2/k/44
execute if score #pt tk matches 53 run function rlk:boss/tachy/p/b2/k/53
execute if score #pt tk matches 54 run function rlk:boss/tachy/p/b2/k/54
execute if score #pt tk matches 63 run function rlk:boss/tachy/p/b2/k/63
execute if score #pt tk matches 64 run function rlk:boss/tachy/p/b2/k/64
execute if score #pt tk matches 78 run scoreboard players set #done tk 1
