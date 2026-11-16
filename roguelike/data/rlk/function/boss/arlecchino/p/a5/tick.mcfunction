# A5 사형장으로의 초대: one pattern tick (#pt kn = 1..124); events in k/<t>.
execute if score #pt kn matches 1..12 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.2}
execute if score #pt kn matches 1..6 run function rlk:mboss/mv/turn {max:12}
execute if score #pt kn matches 16..22 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 15..18 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 26..42 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 25..38 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 46..62 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 45..58 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 66..82 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 65..78 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 13 run function rlk:boss/arlecchino/p/a5/k/13
execute if score #pt kn matches 14 run function rlk:boss/arlecchino/p/a5/k/14
execute if score #pt kn matches 23 run function rlk:boss/arlecchino/p/a5/k/23
execute if score #pt kn matches 24 run function rlk:boss/arlecchino/p/a5/k/24
execute if score #pt kn matches 43 run function rlk:boss/arlecchino/p/a5/k/43
execute if score #pt kn matches 44 run function rlk:boss/arlecchino/p/a5/k/44
execute if score #pt kn matches 63 run function rlk:boss/arlecchino/p/a5/k/63
execute if score #pt kn matches 64 run function rlk:boss/arlecchino/p/a5/k/64
execute if score #pt kn matches 83 run function rlk:boss/arlecchino/p/a5/k/83
execute if score #pt kn matches 84 run function rlk:boss/arlecchino/p/a5/k/84
execute if score #pt kn matches 124 run scoreboard players set #done kn 1
