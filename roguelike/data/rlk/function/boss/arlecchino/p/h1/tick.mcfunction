# H1 연옥 그림자 분신: one pattern tick (#pt kn = 1..124); events in k/<t>.
execute if score #pt kn matches 1..20 run function rlk:mboss/mv/turn {max:20}
execute if score #pt kn matches 35..64 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 65..70 run function rlk:mboss/mv/turn {max:20}
execute if score #pt kn matches 73..81 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 73..82 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 10 run function rlk:boss/arlecchino/p/h1/k/10
execute if score #pt kn matches 20 run function rlk:boss/arlecchino/p/h1/k/20
execute if score #pt kn matches 33 run function rlk:boss/arlecchino/p/h1/k/33
execute if score #pt kn matches 34 run function rlk:boss/arlecchino/p/h1/k/34
execute if score #pt kn matches 36 run kill @e[type=minecraft:item_display,tag=rlk_kn_clone,tag=rlk_kn_p_h1]
execute if score #pt kn matches 58 run function rlk:boss/arlecchino/p/h1/k/58
execute if score #pt kn matches 64 run function rlk:boss/arlecchino/p/h1/k/64
execute if score #pt kn matches 71 run function rlk:boss/arlecchino/p/h1/k/71
execute if score #pt kn matches 72 run function rlk:boss/arlecchino/p/h1/k/72
execute if score #pt kn matches 83 run function rlk:boss/arlecchino/p/h1/k/83
execute if score #pt kn matches 84 run function rlk:boss/arlecchino/p/h1/k/84
execute if score #pt kn matches 124 run scoreboard players set #done kn 1
execute if score #pt kn matches 140 run function rlk:boss/arlecchino/rig/look/wings/off
