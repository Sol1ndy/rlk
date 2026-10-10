# 구역 건설 (normal19_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 212 -41 minecraft:stone
fill -19 201 -59 -2 212 -42 minecraft:air
fill -19 211 -59 -2 211 -42 minecraft:light[level=15]
fill -5 202 -59 -4 202 -56 minecraft:moss_block
fill -16 202 -53 -13 202 -51 minecraft:coarse_dirt
fill -20 212 -46 -20 212 -41 minecraft:calcite
fill -20 204 -55 -20 206 -51 minecraft:calcite
fill -20 212 -48 -20 212 -43 minecraft:oak_leaves[persistent=true]
fill -20 207 -49 -20 210 -49 minecraft:diorite
fill -1 211 -58 -1 212 -55 minecraft:birch_leaves[persistent=true]
fill -1 212 -49 -1 212 -45 minecraft:birch_leaves[persistent=true]
fill -1 212 -59 -1 212 -59 minecraft:birch_leaves[persistent=true]
fill -1 211 -46 -1 212 -42 minecraft:oak_leaves[persistent=true]
fill -1 201 -58 -1 201 -58 minecraft:prismarine
fill -1 205 -58 -1 205 -57 minecraft:calcite
fill -10 211 -60 -6 212 -60 minecraft:oak_leaves[persistent=true]
fill -6 209 -60 -4 212 -60 minecraft:diorite
fill -1 212 -60 -1 212 -60 minecraft:oak_leaves[persistent=true]
fill -6 211 -41 -4 212 -41 minecraft:prismarine
fill -5 210 -41 -5 210 -41 minecraft:diorite
fill -15 211 -41 -15 212 -41 minecraft:birch_leaves[persistent=true]
fill -4 204 -41 -2 206 -41 minecraft:calcite
fill -20 212 -60 -1 212 -41 minecraft:polished_deepslate
fill -19 212 -59 -2 212 -42 minecraft:air
fill -19 201 -59 -2 201 -46 minecraft:dirt
fill -19 202 -59 -2 202 -46 minecraft:podzol
fill -19 201 -45 -15 201 -45 minecraft:dirt
fill -19 202 -45 -15 202 -45 minecraft:podzol
fill -5 201 -45 -2 201 -44 minecraft:dirt
fill -5 202 -45 -2 202 -44 minecraft:podzol
fill -19 201 -44 -17 201 -44 minecraft:dirt
fill -19 202 -44 -17 202 -44 minecraft:podzol
fill -19 201 -43 -18 201 -42 minecraft:dirt
fill -19 202 -43 -18 202 -42 minecraft:podzol
fill -4 201 -43 -2 201 -42 minecraft:dirt
fill -4 202 -43 -2 202 -42 minecraft:podzol
fill -17 201 -42 -17 201 -42 minecraft:dirt
fill -17 202 -42 -17 202 -42 minecraft:podzol
fill -5 201 -42 -5 201 -42 minecraft:dirt
fill -5 202 -42 -5 202 -42 minecraft:podzol
fill -14 201 -45 -6 202 -45 minecraft:dirt
fill -14 203 -45 -6 203 -45 minecraft:podzol
fill -16 201 -44 -15 202 -42 minecraft:dirt
fill -16 203 -44 -15 203 -42 minecraft:podzol
fill -6 201 -44 -6 202 -42 minecraft:dirt
fill -6 203 -44 -6 203 -42 minecraft:podzol
fill -17 201 -43 -17 202 -43 minecraft:dirt
fill -17 203 -43 -17 203 -43 minecraft:podzol
fill -5 201 -43 -5 202 -43 minecraft:dirt
fill -5 203 -43 -5 203 -43 minecraft:podzol
fill -14 201 -44 -7 203 -44 minecraft:dirt
fill -14 204 -44 -7 204 -44 minecraft:podzol
fill -14 201 -43 -10 203 -42 minecraft:dirt
fill -14 204 -43 -10 204 -42 minecraft:podzol
fill -9 201 -42 -7 209 -42 minecraft:calcite
fill -9 210 -42 -7 210 -42 minecraft:podzol
fill -9 201 -43 -7 209 -43 minecraft:diorite
fill -9 210 -43 -7 210 -43 minecraft:podzol
fill -6 201 -56 -2 201 -55 minecraft:clay
fill -6 202 -56 -2 202 -55 minecraft:water
fill -5 201 -54 -2 201 -54 minecraft:clay
fill -5 202 -54 -2 202 -54 minecraft:water
fill -2 201 -53 -2 201 -48 minecraft:clay
fill -2 202 -53 -2 202 -48 minecraft:water
fill -7 202 -57 -2 202 -57 minecraft:sand
fill -7 202 -56 -7 202 -55 minecraft:sand
fill -2 202 -47 -2 202 -47 minecraft:sand
setblock -5 202 -54 minecraft:seagrass
setblock -4 202 -56 minecraft:seagrass
setblock -4 202 -54 minecraft:seagrass
setblock -2 202 -52 minecraft:seagrass
execute positioned -14 203 -55 run function rlk:room/prop/fo_tree_c
execute positioned -3 203 -42 run function rlk:room/prop/fo_flower
execute positioned -8 203 -46 run function rlk:room/prop/p_grass
execute positioned -11 203 -52 run function rlk:room/prop/p_grass
execute positioned -19 203 -52 run function rlk:room/prop/p_grass
execute positioned -6 203 -59 run function rlk:room/prop/p_grass
execute positioned -11 205 -43 run function rlk:room/prop/p_grass
execute positioned -13 203 -52 run function rlk:room/prop/fo_flower
execute positioned -7 203 -48 run function rlk:room/prop/fo_flower
execute positioned -14 204 -45 run function rlk:room/prop/p_grass
execute positioned -13 203 -53 run function rlk:room/prop/p_grass
setblock -9 211 -43 minecraft:short_grass keep
setblock -9 211 -42 minecraft:birch_leaves[persistent=true] keep
setblock -8 211 -43 minecraft:birch_leaves[persistent=true] keep
setblock -7 211 -43 minecraft:birch_leaves[persistent=true] keep
setblock -7 211 -42 minecraft:birch_leaves[persistent=true] keep
