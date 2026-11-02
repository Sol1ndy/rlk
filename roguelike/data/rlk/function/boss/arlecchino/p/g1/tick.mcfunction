# G1 죽음의 칼날: one pattern tick (#pt kn = 1..140); events in k/<t>.
execute if score #pt kn matches 1..5 run function rlk:mboss/mv/turn {max:12}
execute if score #pt kn matches 6 run function rlk:boss/arlecchino/p/g1/k/6
execute if score #pt kn matches 33 run function rlk:boss/arlecchino/p/g1/k/33
execute if score #pt kn matches 34 run function rlk:boss/arlecchino/p/g1/k/34
execute if score #pt kn matches 40 run function rlk:boss/arlecchino/p/g1/k/40
execute if score #pt kn matches 61 run function rlk:boss/arlecchino/p/g1/k/61
execute if score #pt kn matches 62 run function rlk:boss/arlecchino/p/g1/k/62
execute if score #pt kn matches 66 run kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1]
execute if score #pt kn matches 70 run function rlk:boss/arlecchino/p/g1/rim
execute if score #pt kn matches 103 run function rlk:boss/arlecchino/p/g1/k/103
execute if score #pt kn matches 104 run function rlk:boss/arlecchino/p/g1/k/104
execute if score #pt kn matches 112 run kill @e[type=minecraft:item_display,tag=rlk_kn_blade,tag=rlk_kn_p_g1]
execute if score #pt kn matches 140 run scoreboard players set #done kn 1
