# 위치 = 아바타. 종류에 맞는 색으로 울타리를 세우고 반짝임
# bg = 막의 색(ARGB 정수: 앞 두 자리가 불투명도). 불투명도를 바꾸려면 build/p50 의 ALPHA
execute if score #shK view matches 1 run function rlk:view/shield_build {bg:1224726635,rim:"minecraft:gold_block",col:"#FFD86B",orb:"minecraft:gold_nugget"}
execute if score #shK view matches 2 run function rlk:view/shield_build {bg:1217385471,rim:"minecraft:diamond_block",col:"#8FD3FF",orb:"minecraft:prismarine_crystals"}
particle minecraft:end_rod ~ ~0.4 ~ 0.6 0.3 0.6 0.02 8
particle minecraft:wax_on ~ ~0.4 ~ 0.7 0.3 0.7 0 6
