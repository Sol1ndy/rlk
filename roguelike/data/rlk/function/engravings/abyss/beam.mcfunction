# 탄환 궤적 (위치·방향 = 몸의 눈에서 대상 쪽으로). 0.6칸씩 대상 근처까지, 원소 색
execute if score #aqE eng matches 1 run particle minecraft:dust{color:[1.00f,0.54f,0.24f],scale:1.0f} ~ ~ ~ 0.03 0.03 0.03 0 2
execute if score #aqE eng matches 2 run particle minecraft:dust{color:[0.31f,0.72f,1.00f],scale:1.0f} ~ ~ ~ 0.03 0.03 0.03 0 2
execute if score #aqE eng matches 3 run particle minecraft:dust{color:[0.77f,0.55f,1.00f],scale:1.0f} ~ ~ ~ 0.03 0.03 0.03 0 2
execute if score #aqE eng matches 4 run particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:1.0f} ~ ~ ~ 0.03 0.03 0.03 0 2
execute if score #aqE eng matches 5 run particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.0f} ~ ~ ~ 0.03 0.03 0.03 0 2
execute if score #aqE eng matches 6 run particle minecraft:dust{color:[0.44f,0.89f,0.76f],scale:1.0f} ~ ~ ~ 0.03 0.03 0.03 0 2
execute if score #aqE eng matches 7 run particle minecraft:dust{color:[0.65f,0.85f,0.29f],scale:1.0f} ~ ~ ~ 0.03 0.03 0.03 0 2
execute if entity @e[tag=rlk_abt,distance=..1.2,limit=1] run return 0
scoreboard players add #bi eng 1
execute if score #bi eng matches 30.. run return 0
execute positioned ^ ^ ^0.6 run function rlk:engravings/abyss/beam
