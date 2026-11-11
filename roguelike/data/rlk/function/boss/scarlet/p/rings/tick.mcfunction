# RINGS 회전 월륜: one pattern tick (#pt hr = 1..64); events in k/<t>.
execute if score #pt hr matches 45..46 if score #ph hr matches 1 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 55..56 if score #ph hr matches 7 if score #pp hr matches 1 run function rlk:boss/scarlet/core/pp
execute if score #pt hr matches 45..53 if score #ph hr matches 1 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 49..53 if score #ph hr matches 1 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 55..63 if score #ph hr matches 7 run function rlk:mboss/mv/turn {max:10}
execute if score #pt hr matches 59..63 if score #ph hr matches 7 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail_step
execute if score #pt hr matches 1 run function rlk:boss/scarlet/p/rings/k/1
execute if score #pt hr matches 2 run function rlk:boss/scarlet/p/rings/k/2
execute if score #pt hr matches 3 run function rlk:boss/scarlet/p/rings/k/3
execute if score #pt hr matches 4 run function rlk:boss/scarlet/p/rings/k/4
execute if score #pt hr matches 5 run function rlk:boss/scarlet/p/rings/k/5
execute if score #pt hr matches 6 run function rlk:boss/scarlet/p/rings/k/6
execute if score #pt hr matches 7 run function rlk:boss/scarlet/p/rings/k/7
execute if score #pt hr matches 13 run function rlk:boss/scarlet/p/rings/k/13
execute if score #pt hr matches 14 run function rlk:boss/scarlet/p/rings/k/14
execute if score #pt hr matches 15 run function rlk:boss/scarlet/p/rings/k/15
execute if score #pt hr matches 16 run function rlk:boss/scarlet/p/rings/k/16
execute if score #pt hr matches 17 run function rlk:boss/scarlet/p/rings/k/17
execute if score #pt hr matches 23 run function rlk:boss/scarlet/p/rings/k/23
execute if score #pt hr matches 24 run function rlk:boss/scarlet/p/rings/k/24
execute if score #pt hr matches 25 run function rlk:boss/scarlet/p/rings/k/25
execute if score #pt hr matches 26 run function rlk:boss/scarlet/p/rings/k/26
execute if score #pt hr matches 27 run function rlk:boss/scarlet/p/rings/k/27
execute if score #pt hr matches 33 run function rlk:boss/scarlet/p/rings/k/33
execute if score #pt hr matches 34 run function rlk:boss/scarlet/p/rings/k/34
execute if score #pt hr matches 35 run function rlk:boss/scarlet/p/rings/k/35
execute if score #pt hr matches 36 run function rlk:boss/scarlet/p/rings/k/36
execute if score #pt hr matches 37 run function rlk:boss/scarlet/p/rings/k/37
execute if score #pt hr matches 43 run function rlk:boss/scarlet/p/rings/k/43
execute if score #pt hr matches 44 run function rlk:boss/scarlet/p/rings/k/44
execute if score #pt hr matches 45 run function rlk:boss/scarlet/p/rings/k/45
execute if score #pt hr matches 46 run function rlk:boss/scarlet/p/rings/k/46
execute if score #pt hr matches 47 run function rlk:boss/scarlet/p/rings/k/47
execute if score #pt hr matches 48 if score #ph hr matches 1 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 50 if score #ph hr matches 1 if score #ultq hr matches 1 run scoreboard players set #done hr 1
execute if score #pt hr matches 53 run function rlk:boss/scarlet/p/rings/k/53
execute if score #pt hr matches 54 run function rlk:boss/scarlet/p/rings/k/54
execute if score #pt hr matches 58 if score #ph hr matches 7 unless score #ultq hr matches 1 run function rlk:boss/scarlet/ai/tail
execute if score #pt hr matches 60 if score #ph hr matches 7 if score #ultq hr matches 1 run scoreboard players set #done hr 1
execute if score #pt hr matches 64 run scoreboard players set #done hr 1
