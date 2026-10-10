# 모션 32 의 0틱째 조각 (@s = 플레이어, at 몸)
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.35 ^-0.12 ^0.70 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.33 ^-0.12 ^0.94 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.76,0.68,1.00],scale:0.63} ^0.33 ^-0.19 ^0.94 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.30 ^-0.11 ^1.17 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:electric_spark ^0.30 ^-0.11 ^1.17 0.06 0.06 0.06 0.02 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,1.00,1.00],scale:0.70} ^0.28 ^-0.11 ^1.41 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[0.76,0.68,1.00],scale:0.63} ^0.28 ^-0.18 ^1.41 0 0 0 0 1
execute unless score #k297 snd matches 1 run function rlk:snd/f336
