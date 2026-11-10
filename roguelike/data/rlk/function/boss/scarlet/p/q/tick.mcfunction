# Q 자영 포박 · 천공 낙월: one pattern tick (#pt hr = 1..111); events in k/<t>.
execute if score #pt hr matches 1..12 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 22..33 unless score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 32..33 unless score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 31..35 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 44..51 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 60..66 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 73..87 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:20}
execute if score #pt hr matches 96..110 if score #q_hit hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 106..110 if score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/q/k/4
execute if score #pt hr matches 8 run function rlk:boss/scarlet/p/q/k/8
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/q/k/13
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/q/k/16
execute if score #pt hr matches 19 run function rlk:boss/scarlet/p/q/k/19
execute if score #pt hr matches 20 run function rlk:boss/scarlet/p/q/k/20
execute if score #pt hr matches 21 run function rlk:boss/scarlet/p/q/k/21
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/q/k/23
execute if score #pt hr matches 31 unless score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 34 unless score #q_hit hr matches 1 run scoreboard players set #done hr 1
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/q/k/36
execute if score #pt hr matches 42 run function rlk:boss/scarlet/p/q/k/42
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/q/k/43
execute if score #pt hr matches 52 run function rlk:boss/scarlet/p/q/k/52
execute if score #pt hr matches 55 run function rlk:boss/scarlet/p/q/k/55
execute if score #pt hr matches 58 run function rlk:boss/scarlet/p/q/k/58
execute if score #pt hr matches 59 run function rlk:boss/scarlet/p/q/k/59
execute if score #pt hr matches 67 run function rlk:boss/scarlet/p/q/k/67
execute if score #pt hr matches 83 run function rlk:boss/scarlet/p/q/k/83
execute if score #pt hr matches 88 run function rlk:boss/scarlet/p/q/k/88
execute if score #pt hr matches 94 run function rlk:boss/scarlet/p/q/k/94
execute if score #pt hr matches 95 run function rlk:boss/scarlet/p/q/k/95
execute if score #pt hr matches 99 if score #q_hit hr matches 1 at @s positioned ~ 201 ~ run function rlk:mboss/mv/glide {t:6}
execute if score #pt hr matches 105 if score #q_hit hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 111 run scoreboard players set #done hr 1
