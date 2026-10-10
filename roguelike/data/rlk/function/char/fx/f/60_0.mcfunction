# 모션 60 의 0틱째 조각 (@s = 플레이어, at 몸)
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.62,0.25],scale:0.60} ^-1.06 ^0.35 ^0.28 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.94,0.68],scale:0.60} ^-0.99 ^0.24 ^0.48 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:firework ^-0.99 ^0.24 ^0.48 0.04 0.04 0.04 0.02 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.62,0.25],scale:0.60} ^-0.88 ^0.13 ^0.66 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.62,0.25],scale:0.60} ^1.06 ^0.35 ^0.28 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.94,0.68],scale:0.60} ^0.99 ^0.24 ^0.48 0 0 0 0 1
execute positioned ~ ~1.62 ~ run particle minecraft:firework ^0.99 ^0.24 ^0.48 0.04 0.04 0.04 0.02 1
execute positioned ~ ~1.62 ~ run particle minecraft:dust{color:[1.00,0.62,0.25],scale:0.60} ^0.88 ^0.13 ^0.66 0 0 0 0 1
execute unless score #k291 snd matches 1 run function rlk:snd/f326
