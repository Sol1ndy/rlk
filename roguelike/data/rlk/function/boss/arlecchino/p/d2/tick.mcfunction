# D2 블러드 돌진: one pattern tick (#pt kn = 1..76); events in k/<t>.
execute if score #pt kn matches 1..20 run function rlk:mboss/mv/turn {max:8}
execute if score #pt kn matches 27..31 if score #hitev kn matches 1.. run scoreboard players set #d2_l kn 1
execute if score #pt kn matches 32..44 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 31..40 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 25 run function rlk:boss/arlecchino/p/d2/k/25
execute if score #pt kn matches 26 run function rlk:boss/arlecchino/p/d2/k/26
execute if score #pt kn matches 27 run function rlk:boss/arlecchino/p/d2/k/27
execute if score #pt kn matches 28 run function rlk:boss/arlecchino/p/d2/k/28
execute if score #pt kn matches 29 run function rlk:boss/arlecchino/p/d2/k/29
execute if score #pt kn matches 30 run function rlk:boss/arlecchino/p/d2/k/30
execute if score #pt kn matches 34 run function rlk:boss/arlecchino/p/d2/k/34
execute if score #pt kn matches 45 run function rlk:boss/arlecchino/p/d2/k/45
execute if score #pt kn matches 46 run function rlk:boss/arlecchino/p/d2/k/46
execute if score #pt kn matches 76 run scoreboard players set #done kn 1
