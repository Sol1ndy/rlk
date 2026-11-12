# A1 돌진 베기: one pattern tick (#pt tk = 1..34); events in k/<t>.
execute if score #pt tk matches 1..8 run function rlk:mboss/mv/turn {max:8}
execute if score #pt tk matches 13 run function rlk:boss/tachy/p/a1/k/13
execute if score #pt tk matches 14 run function rlk:boss/tachy/p/a1/k/14
execute if score #pt tk matches 15 run function rlk:boss/tachy/p/a1/k/15
execute if score #pt tk matches 16 run function rlk:boss/tachy/p/a1/k/16
execute if score #pt tk matches 17 run function rlk:boss/tachy/p/a1/k/17
execute if score #pt tk matches 18 run function rlk:boss/tachy/p/a1/k/18
execute if score #pt tk matches 19 run function rlk:boss/tachy/p/a1/k/19
execute if score #pt tk matches 20 run function rlk:boss/tachy/p/a1/k/20
execute if score #pt tk matches 34 run scoreboard players set #done tk 1
