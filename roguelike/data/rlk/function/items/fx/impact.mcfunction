# 명중 (위치 = 궤적의 끝, 대상의 눈 근처)
execute if score #aqE eng matches 1 run particle minecraft:dust{color:[1.00f,0.54f,0.24f],scale:1.6f} ~ ~ ~ 0.3 0.3 0.3 0 14
execute if score #aqE eng matches 1 run particle minecraft:flame ~ ~ ~ 0.3 0.3 0.3 0.12 14
execute if score #aqE eng matches 2 run particle minecraft:dust{color:[0.31f,0.72f,1.00f],scale:1.6f} ~ ~ ~ 0.3 0.3 0.3 0 14
execute if score #aqE eng matches 2 run particle minecraft:bubble_pop ~ ~ ~ 0.3 0.3 0.3 0.12 14
execute if score #aqE eng matches 3 run particle minecraft:dust{color:[0.77f,0.55f,1.00f],scale:1.6f} ~ ~ ~ 0.3 0.3 0.3 0 14
execute if score #aqE eng matches 3 run particle minecraft:electric_spark ~ ~ ~ 0.3 0.3 0.3 0.12 14
execute if score #aqE eng matches 4 run particle minecraft:dust{color:[0.62f,0.91f,0.96f],scale:1.6f} ~ ~ ~ 0.3 0.3 0.3 0 14
execute if score #aqE eng matches 4 run particle minecraft:snowflake ~ ~ ~ 0.3 0.3 0.3 0.12 14
execute if score #aqE eng matches 5 run particle minecraft:dust{color:[0.95f,0.76f,0.31f],scale:1.6f} ~ ~ ~ 0.3 0.3 0.3 0 14
execute if score #aqE eng matches 5 run particle minecraft:wax_on ~ ~ ~ 0.3 0.3 0.3 0.12 14
execute if score #aqE eng matches 6 run particle minecraft:dust{color:[0.44f,0.89f,0.76f],scale:1.6f} ~ ~ ~ 0.3 0.3 0.3 0 14
execute if score #aqE eng matches 6 run particle minecraft:cloud ~ ~ ~ 0.3 0.3 0.3 0.12 14
execute if score #aqE eng matches 7 run particle minecraft:dust{color:[0.65f,0.85f,0.29f],scale:1.6f} ~ ~ ~ 0.3 0.3 0.3 0 14
execute if score #aqE eng matches 7 run particle minecraft:happy_villager ~ ~ ~ 0.3 0.3 0.3 0.12 14
particle minecraft:crit ~ ~ ~ 0.3 0.3 0.3 0.3 8
# 번개: 대상 머리 위에서 내리꽂는 줄기
execute if score #aqE eng matches 3 run particle minecraft:dust{color:[0.77f,0.55f,1.00f],scale:1.5f} ~ ~1.6 ~ 0.06 1.3 0.06 0 24
# 불: 치솟는 불꽃 / 물: 물보라 / 얼음: 얼음 파편 / 바위: 돌 파편 / 풀: 잎
execute if score #aqE eng matches 1 run particle minecraft:lava ~ ~ ~ 0.2 0.2 0.2 0 3
execute if score #aqE eng matches 2 run particle minecraft:splash ~ ~ ~ 0.3 0.3 0.3 0.2 16
execute if score #aqE eng matches 4 run particle minecraft:block{block_state:"minecraft:ice"} ~ ~ ~ 0.3 0.3 0.3 0.1 10
execute if score #aqE eng matches 5 run particle minecraft:block{block_state:"minecraft:yellow_terracotta"} ~ ~ ~ 0.3 0.3 0.3 0.1 10
execute if score #aqE eng matches 7 run particle minecraft:cherry_leaves ~ ~ ~ 0.3 0.3 0.3 0 6
