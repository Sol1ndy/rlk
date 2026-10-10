# 모션 30 의 0틱째 조각 (@s = 플레이어, at 몸)
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.30 ^-0.30 ^0.70 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.27 ^-0.29 ^0.94 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.76,0.68,1.00],scale:0.63} ^0.27 ^-0.36 ^0.94 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.25 ^-0.28 ^1.17 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:electric_spark ^0.25 ^-0.28 ^1.17 0.06 0.06 0.06 0.02 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.22 ^-0.27 ^1.41 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.76,0.68,1.00],scale:0.63} ^0.22 ^-0.34 ^1.41 0 0 0 0 1
execute unless score #k297 snd matches 1 run function rlk:snd/f336
