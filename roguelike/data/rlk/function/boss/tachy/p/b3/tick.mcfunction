# B3 충전 6연격: one pattern tick (#pt tk = 1..112); events in k/<t>.
execute if score #pt tk matches 1..26 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 41..42 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 51..52 run function rlk:mboss/mv/turn {max:6}
execute if score #pt tk matches 29 run function rlk:boss/tachy/p/b3/k/29
execute if score #pt tk matches 30 run function rlk:boss/tachy/p/b3/k/30
execute if score #pt tk matches 39 run function rlk:boss/tachy/p/b3/k/39
execute if score #pt tk matches 40 run function rlk:boss/tachy/p/b3/k/40
execute if score #pt tk matches 49 run function rlk:boss/tachy/p/b3/k/49
execute if score #pt tk matches 50 run function rlk:boss/tachy/p/b3/k/50
execute if score #pt tk matches 59 run function rlk:boss/tachy/p/b3/k/59
execute if score #pt tk matches 60 run function rlk:boss/tachy/p/b3/k/60
execute if score #pt tk matches 64 run function rlk:boss/tachy/rig/look/edge/glint
execute if score #pt tk matches 66 run function rlk:mboss/mv/turn {max:30}
execute if score #pt tk matches 75 run function rlk:boss/tachy/p/b3/k/75
execute if score #pt tk matches 76 run function rlk:boss/tachy/p/b3/k/76
execute if score #pt tk matches 78 run function rlk:mboss/mv/turn {max:30}
execute if score #pt tk matches 87 run function rlk:boss/tachy/p/b3/k/87
execute if score #pt tk matches 88 run function rlk:boss/tachy/p/b3/k/88
execute if score #pt tk matches 90 run function rlk:mboss/mv/turn {max:30}
execute if score #pt tk matches 99 run function rlk:boss/tachy/p/b3/k/99
execute if score #pt tk matches 100 run function rlk:boss/tachy/p/b3/k/100
execute if score #pt tk matches 112 run scoreboard players set #done tk 1
