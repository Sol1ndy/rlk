# E1 와리가리 베기: one pattern tick (#pt kn = 1..112); events in k/<t>.
execute if score #pt kn matches 1..64 run function rlk:mboss/mv/turn {max:20}
execute if score #pt kn matches 78..90 at @s unless entity @e[tag=rlk_body,limit=1,distance=..2.6] run function rlk:mboss/mv/step {d:0.3}
execute if score #pt kn matches 77..86 run function rlk:mboss/mv/turn {max:14}
execute if score #pt kn matches 16 run function rlk:boss/arlecchino/p/e1/k/16
execute if score #pt kn matches 26 run function rlk:boss/arlecchino/p/e1/k/26
execute if score #pt kn matches 36 run function rlk:boss/arlecchino/p/e1/k/36
execute if score #pt kn matches 46 run function rlk:boss/arlecchino/p/e1/k/46
execute if score #pt kn matches 56 run function rlk:boss/arlecchino/p/e1/k/56
execute if score #pt kn matches 64 run function rlk:boss/arlecchino/p/e1/k/64
execute if score #pt kn matches 70 run function rlk:boss/arlecchino/p/e1/k/70
execute if score #pt kn matches 75 run function rlk:boss/arlecchino/p/e1/k/75
execute if score #pt kn matches 76 run function rlk:boss/arlecchino/p/e1/k/76
execute if score #pt kn matches 91 run function rlk:boss/arlecchino/p/e1/k/91
execute if score #pt kn matches 92 run function rlk:boss/arlecchino/p/e1/k/92
execute if score #pt kn matches 112 run scoreboard players set #done kn 1
