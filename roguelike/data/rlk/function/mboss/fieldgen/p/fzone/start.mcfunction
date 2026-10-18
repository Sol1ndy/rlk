# F1 감소 영역 (clip field_erupt; @s = body at the centre): decals [22, 72, 102, 120, 141, 170, 181, 220, 231] (strike +15), end 260.
scoreboard players set #fq11P mb 0
execute rotated as @s rotated ~ 0 positioned ^3.85 ^4.1 ^0 run function rlk:mboss/fieldgen/fx/p/spark
execute rotated as @s rotated ~ 0 positioned ^-3.85 ^4.1 ^0 run function rlk:mboss/fieldgen/fx/p/spark
playsound minecraft:block.beacon.activate hostile @a[tag=player] ~ ~ ~ 0.7 1.3 0.23
playsound minecraft:block.conduit.activate hostile @a[tag=player] ~ ~ ~ 0.6 1.2 0.2
playsound minecraft:block.crafter.craft hostile @a[tag=player] ~ ~ ~ 0.6 0.7 0.2
