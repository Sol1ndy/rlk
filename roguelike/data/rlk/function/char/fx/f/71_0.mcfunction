# 모션 71 의 0틱째 조각 (@s = 플레이어, at 몸)
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.30,0.10],scale:0.70} ^1.04 ^-0.05 ^0.60 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.78,0.30],scale:0.70} ^0.92 ^-0.06 ^0.77 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:small_flame ^0.92 ^-0.06 ^0.77 0.04 0.04 0.04 0.02 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.30,0.10],scale:0.70} ^0.77 ^-0.07 ^0.92 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.78,0.30],scale:0.70} ^0.60 ^-0.07 ^1.04 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.30,0.10],scale:0.70} ^0.41 ^-0.08 ^1.13 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:small_flame ^0.41 ^-0.08 ^1.13 0.04 0.04 0.04 0.02 1
execute unless score #k45 snd matches 1 run function rlk:snd/f346
