# B2 붉은 달의 낫: one pattern tick (#pt kn = 1..130); events in k/<t>.
execute if score #pt kn matches 1..20 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 29..51 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 59..80 run function rlk:mboss/mv/turn {max:10}
execute if score #pt kn matches 10 run function rlk:boss/arlecchino/p/b2/k/10
execute if score #pt kn matches 28 run function rlk:boss/arlecchino/p/b2/k/28
execute if score #pt kn matches 40 at @s run function rlk:boss/arlecchino/fx/snd/wheel_spin
execute if score #pt kn matches 51 run function rlk:boss/arlecchino/rig/look/weapon_r/hand
execute if score #pt kn matches 52 run function rlk:boss/arlecchino/p/b2/k/52
execute if score #pt kn matches 58 run function rlk:boss/arlecchino/p/b2/k/58
execute if score #pt kn matches 76 run function rlk:boss/arlecchino/p/b2/k/76
execute if score #pt kn matches 80 run function rlk:boss/arlecchino/core/lockp
execute if score #pt kn matches 81 run function rlk:boss/arlecchino/rig/look/weapon_r/hand
execute if score #pt kn matches 92 at @e[type=minecraft:marker,tag=rlk_kn_lock,limit=1] positioned ~ ~1 ~ run function rlk:boss/arlecchino/fx/p/claw {r:22}
execute if score #pt kn matches 95 run function rlk:boss/arlecchino/p/b2/k/95
execute if score #pt kn matches 96 run function rlk:boss/arlecchino/p/b2/k/96
execute if score #pt kn matches 130 run scoreboard players set #done kn 1
