# A2 사형장으로의 초대: one pattern tick (#pt kn = 1..46); events in k/<t>.
execute if score #pt kn matches 1..12 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.2}
execute if score #pt kn matches 1..6 run function rlk:mboss/mv/turn {max:12}
execute if score #pt kn matches 16..22 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 15..18 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 13 run function rlk:boss/arlecchino/p/a2/k/13
execute if score #pt kn matches 14 run function rlk:boss/arlecchino/p/a2/k/14
execute if score #pt kn matches 23 run function rlk:boss/arlecchino/p/a2/k/23
execute if score #pt kn matches 24 run function rlk:boss/arlecchino/p/a2/k/24
execute if score #pt kn matches 46 run scoreboard players set #done kn 1
