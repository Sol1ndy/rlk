# 구역 건설 (root7_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 31 200 -9 35 200 -6 minecraft:coarse_dirt
fill 34 200 -8 38 200 -6 minecraft:calcite
fill 27 200 -13 29 200 -11 minecraft:calcite
fill 20 210 -19 20 210 -14 minecraft:oak_leaves[persistent=true]
fill 20 209 -17 20 210 -16 minecraft:oak_leaves[persistent=true]
fill 20 205 -4 20 208 -3 minecraft:calcite
fill 20 209 -5 20 210 -5 minecraft:birch_leaves[persistent=true]
fill 39 206 -16 39 206 -16 minecraft:calcite
fill 39 210 -17 39 210 -17 minecraft:oak_leaves[persistent=true]
fill 39 206 -18 39 209 -18 minecraft:calcite
fill 39 201 -17 39 204 -13 minecraft:moss_block
fill 39 210 -11 39 210 -10 minecraft:calcite
fill 39 209 -11 39 210 -10 minecraft:prismarine
fill 22 207 -20 25 207 -20 minecraft:diorite
fill 23 201 -20 25 201 -20 minecraft:moss_block
fill 34 202 -20 34 204 -20 minecraft:calcite
fill 24 210 -20 25 210 -20 minecraft:oak_leaves[persistent=true]
fill 22 208 -20 26 210 -20 minecraft:diorite
fill 30 206 -20 33 209 -20 minecraft:moss_block
fill 35 205 -1 38 207 -1 minecraft:calcite
fill 32 205 -1 33 207 -1 minecraft:prismarine
fill 29 208 -1 31 210 -1 minecraft:calcite
fill 35 208 -1 35 210 -1 minecraft:calcite
fill 33 210 -1 38 210 -1 minecraft:prismarine
fill 25 209 -1 28 210 -1 minecraft:prismarine
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 28 201 -19 28 201 -17 minecraft:podzol
fill 21 201 -17 25 201 -17 minecraft:podzol
fill 26 201 -16 27 201 -15 minecraft:podzol
fill 27 201 -19 27 201 -17 minecraft:dirt
fill 27 202 -19 27 202 -17 minecraft:podzol
fill 21 201 -18 26 201 -18 minecraft:dirt
fill 21 202 -18 26 202 -18 minecraft:podzol
fill 26 201 -17 26 201 -17 minecraft:dirt
fill 26 202 -17 26 202 -17 minecraft:podzol
fill 21 201 -19 26 202 -19 minecraft:dirt
fill 21 203 -19 26 203 -19 minecraft:podzol
fill 29 201 -3 29 205 -2 minecraft:calcite
fill 29 206 -3 29 206 -2 minecraft:podzol
fill 30 201 -3 32 205 -2 minecraft:diorite
fill 30 206 -3 32 206 -2 minecraft:podzol
fill 30 201 -17 31 206 -16 minecraft:calcite
fill 30 207 -17 31 207 -16 minecraft:podzol
fill 36 199 -14 38 199 -14 minecraft:clay
fill 36 200 -14 38 200 -14 minecraft:water
fill 38 199 -13 38 199 -5 minecraft:clay
fill 38 200 -13 38 200 -5 minecraft:water
fill 35 199 -6 37 199 -5 minecraft:clay
fill 35 200 -6 37 200 -5 minecraft:water
fill 35 200 -15 38 200 -15 minecraft:sand
fill 35 200 -14 35 200 -14 minecraft:sand
fill 34 200 -5 34 200 -4 minecraft:sand
fill 35 200 -4 38 200 -4 minecraft:sand
setblock 38 200 -8 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 38 200 -6 minecraft:seagrass
setblock 38 200 -5 minecraft:seagrass
execute positioned 25 201 -4 run function rlk:room/prop/fo_tree_b
execute positioned 32 201 -4 run function rlk:room/prop/p_grass
execute positioned 22 201 -4 run function rlk:room/prop/fo_white
execute positioned 26 203 -17 run function rlk:room/prop/p_grass
execute positioned 25 201 -7 run function rlk:room/prop/fo_flower
execute positioned 28 201 -10 run function rlk:room/prop/p_grass
execute positioned 30 201 -5 run function rlk:room/prop/p_grass
execute positioned 37 201 -4 run function rlk:room/prop/p_grass
execute positioned 24 201 -9 run function rlk:room/prop/fo_flower
execute positioned 38 201 -15 run function rlk:room/prop/fo_flower
execute positioned 29 201 -13 run function rlk:room/prop/fo_white
setblock 29 207 -3 minecraft:birch_leaves[persistent=true] keep
setblock 30 208 -17 minecraft:short_grass keep
setblock 30 207 -3 minecraft:short_grass keep
setblock 30 207 -2 minecraft:short_grass keep
setblock 32 207 -3 minecraft:short_grass keep
setblock 32 207 -2 minecraft:birch_leaves[persistent=true] keep
