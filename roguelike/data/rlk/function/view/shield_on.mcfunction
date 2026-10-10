# 위치 = 아바타. 종류에 맞는 색으로 울타리를 세우고 반짝임
# bg = 막의 색(ARGB 정수: 앞 두 자리가 불투명도). 불투명도를 바꾸려면 build/p50 의 ALPHA
execute if score #shK view matches 1 run function rlk:view/shield_build {bg:1224726635,rim:"minecraft:gold_block",col:"#FFD86B",orb:"minecraft:gold_nugget"}
# 결정 방어막: 흡수한 원소의 색 (#shK = 10 + 원소)
execute if score #shK view matches 11 run function rlk:view/shield_build {bg:1224706621,rim:"minecraft:orange_concrete",col:"#FF8A3D",orb:"minecraft:blaze_powder"}
execute if score #shK view matches 12 run function rlk:view/shield_build {bg:1213184255,rim:"minecraft:light_blue_concrete",col:"#4FB8FF",orb:"minecraft:heart_of_the_sea"}
execute if score #shK view matches 13 run function rlk:view/shield_build {bg:1220905983,rim:"minecraft:purple_concrete",col:"#C58BFF",orb:"minecraft:amethyst_shard"}
execute if score #shK view matches 14 run function rlk:view/shield_build {bg:1218439413,rim:"minecraft:packed_ice",col:"#9FE8F5",orb:"minecraft:snowball"}
execute if score #shK view matches 18 run function rlk:view/shield_build {bg:1222653535,rim:"minecraft:crying_obsidian",col:"#E0365F",orb:"minecraft:redstone"}
execute if score #shK view matches 2 run function rlk:view/shield_build {bg:1217385471,rim:"minecraft:diamond_block",col:"#8FD3FF",orb:"minecraft:prismarine_crystals"}
particle minecraft:end_rod ~ ~0.4 ~ 0.6 0.3 0.6 0.02 8
particle minecraft:wax_on ~ ~0.4 ~ 0.7 0.3 0.7 0 6
