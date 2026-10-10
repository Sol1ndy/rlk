# 모션 62 의 0틱째 조각 (@s = 플레이어, at 몸)
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.62,0.25],scale:0.60} ^0.00 ^-1.12 ^0.92 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.94,0.68],scale:0.60} ^0.00 ^-0.96 ^1.05 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:firework ^0.00 ^-0.96 ^1.05 0.04 0.04 0.04 0.02 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.62,0.25],scale:0.60} ^0.00 ^-0.78 ^1.16 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.94,0.68],scale:0.60} ^0.00 ^-0.59 ^1.24 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.62,0.25],scale:0.60} ^0.00 ^-0.38 ^1.29 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:firework ^0.00 ^-0.38 ^1.29 0.04 0.04 0.04 0.02 1
execute unless score #k302 snd matches 1 run function rlk:snd/f345
