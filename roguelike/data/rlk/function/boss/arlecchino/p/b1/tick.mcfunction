# B1 붉은 달의 낫: one pattern tick (#pt kn = 1..60); events in k/<t>.
execute if score #pt kn matches 1..20 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 10 run function rlk:boss/arlecchino/p/b1/k/10
execute if score #pt kn matches 28 run function rlk:boss/arlecchino/p/b1/k/28
execute if score #pt kn matches 51 run function rlk:boss/arlecchino/rig/look/weapon_r/hand
execute if score #pt kn matches 52 run function rlk:boss/arlecchino/rig/look/weapon_r/hand
execute if score #pt kn matches 60 run scoreboard players set #done kn 1
