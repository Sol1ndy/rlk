# 궤적 (0.5칸씩, 최대 20칸). 대상의 몸통 근처에 닿으면 명중 효과
execute if score #aqE eng matches 1 run particle minecraft:dust{color:[1.00f,0.54f,0.24f],scale:1.3f} ~ ~ ~ 0.04 0.04 0.04 0 3
execute if score #aqE eng matches 1 run particle minecraft:flame ~ ~ ~ 0.03 0.03 0.03 0.005 1
execute if score #aqE eng matches 2 run particle minecraft:dust{color:[0.31f,0.72f,1.00f],scale:1.3f} ~ ~ ~ 0.04 0.04 0.04 0 3
execute if score #aqE eng matches 2 run particle minecraft:bubble_pop ~ ~ ~ 0.03 0.03 0.03 0.005 1
execute if score #aqE eng matches 3 run particle minecraft:dust{color:[0.77f,0.55f,1.00f],scale:1.3f} ~ ~ ~ 0.04 0.04 0.04 0 3
execute if score #aqE eng matches 3 run particle minecraft:electric_spark ~ ~ ~ 0.03 0.03 0.03 0.005 1
execute if score #aqE eng matches 4 run particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:1.3f} ~ ~ ~ 0.04 0.04 0.04 0 3
execute if score #aqE eng matches 4 run particle minecraft:snowflake ~ ~ ~ 0.03 0.03 0.03 0.005 1
execute if score #aqE eng matches 5 run particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.3f} ~ ~ ~ 0.04 0.04 0.04 0 3
execute if score #aqE eng matches 5 run particle minecraft:wax_on ~ ~ ~ 0.03 0.03 0.03 0.005 1
execute if score #aqE eng matches 6 run particle minecraft:dust{color:[0.44f,0.89f,0.76f],scale:1.3f} ~ ~ ~ 0.04 0.04 0.04 0 3
execute if score #aqE eng matches 6 run particle minecraft:cloud ~ ~ ~ 0.03 0.03 0.03 0.005 1
execute if score #aqE eng matches 7 run particle minecraft:dust{color:[0.65f,0.85f,0.29f],scale:1.3f} ~ ~ ~ 0.04 0.04 0.04 0 3
execute if score #aqE eng matches 7 run particle minecraft:happy_villager ~ ~ ~ 0.03 0.03 0.03 0.005 1
execute positioned ~ ~-0.9 ~ if entity @e[tag=rlk_abt,distance=..1.1,limit=1] run return run function rlk:items/fx/impact
scoreboard players add #bi eng 1
execute if score #bi eng matches 40.. run return 0
execute positioned ^ ^ ^0.5 run function rlk:items/fx/trail
