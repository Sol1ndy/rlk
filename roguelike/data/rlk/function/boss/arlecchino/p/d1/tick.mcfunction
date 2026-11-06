# D1 블러드 돌진: one pattern tick (#pt kn = 1..56); events in k/<t>.
execute if score #pt kn matches 1..20 run function rlk:mboss/mv/turn {max:8}
execute if score #pt kn matches 25 run function rlk:boss/arlecchino/p/d1/k/25
execute if score #pt kn matches 26 run function rlk:boss/arlecchino/p/d1/k/26
execute if score #pt kn matches 27 run function rlk:boss/arlecchino/p/d1/k/27
execute if score #pt kn matches 28 run function rlk:boss/arlecchino/p/d1/k/28
execute if score #pt kn matches 29 run function rlk:boss/arlecchino/p/d1/k/29
execute if score #pt kn matches 30 run function rlk:boss/arlecchino/p/d1/k/30
execute if score #pt kn matches 56 run scoreboard players set #done kn 1
