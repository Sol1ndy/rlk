# 모션 13 의 0틱째 조각 (@s = 플레이어, at 몸)
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.96,0.98,1.00],scale:1.00} ^-0.15 ^-1.50 ^1.02 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.70,0.82,1.00],scale:1.10} ^-0.13 ^-1.50 ^0.89 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.96,0.98,1.00],scale:1.00} ^-0.15 ^-1.50 ^1.19 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.70,0.82,1.00],scale:1.10} ^-0.13 ^-1.50 ^1.03 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.96,0.98,1.00],scale:1.00} ^-0.15 ^-1.49 ^1.33 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.70,0.82,1.00],scale:1.10} ^-0.13 ^-1.49 ^1.16 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:crit ^-0.15 ^-1.49 ^1.33 0.06 0.06 0.06 0.02 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.96,0.98,1.00],scale:1.00} ^-0.15 ^-1.32 ^1.46 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.70,0.82,1.00],scale:1.10} ^-0.13 ^-1.32 ^1.27 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.96,0.98,1.00],scale:1.00} ^-0.15 ^-1.15 ^1.57 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.70,0.82,1.00],scale:1.10} ^-0.13 ^-1.15 ^1.37 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.96,0.98,1.00],scale:1.00} ^-0.15 ^-0.96 ^1.66 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.70,0.82,1.00],scale:1.10} ^-0.13 ^-0.96 ^1.44 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.96,0.98,1.00],scale:1.00} ^-0.15 ^-0.76 ^1.72 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.70,0.82,1.00],scale:1.10} ^-0.13 ^-0.76 ^1.50 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:crit ^-0.15 ^-0.76 ^1.72 0.06 0.06 0.06 0.02 1
execute unless score #k300 snd matches 1 run function rlk:snd/f340
execute unless score #k250 snd matches 1 run function rlk:snd/f341
