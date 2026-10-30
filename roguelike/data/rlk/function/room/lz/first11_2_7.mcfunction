# 구역 건설 (first11_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:stone
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 5 200 30 7 200 32 minecraft:coarse_dirt
fill 7 200 33 8 200 34 minecraft:moss_block
fill 0 202 33 0 204 35 minecraft:diorite
fill 0 209 29 0 210 31 minecraft:oak_leaves[persistent=true]
fill 0 202 31 0 203 36 minecraft:calcite
fill 19 209 21 19 210 23 minecraft:dark_prismarine
fill 19 201 29 19 201 33 minecraft:prismarine
fill 19 209 27 19 210 32 minecraft:calcite
fill 19 210 36 19 210 37 minecraft:birch_leaves[persistent=true]
fill 19 210 23 19 210 28 minecraft:oak_leaves[persistent=true]
fill 19 210 28 19 210 32 minecraft:oak_leaves[persistent=true]
fill 12 210 20 16 210 20 minecraft:birch_leaves[persistent=true]
fill 1 201 20 5 201 20 minecraft:prismarine
fill 7 210 20 12 210 20 minecraft:moss_block
fill 10 209 20 15 210 20 minecraft:birch_leaves[persistent=true]
fill 1 210 20 4 210 20 minecraft:prismarine
fill 16 206 39 17 207 39 minecraft:diorite
fill 10 206 39 14 209 39 minecraft:diorite
fill 14 201 39 18 201 39 minecraft:calcite
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 6 201 35 13 201 35 minecraft:podzol
fill 6 201 36 6 201 38 minecraft:podzol
fill 13 201 36 13 201 36 minecraft:podzol
fill 5 201 37 5 201 37 minecraft:podzol
fill 14 201 37 14 201 38 minecraft:podzol
fill 7 201 36 12 201 38 minecraft:dirt
fill 7 202 36 12 202 38 minecraft:podzol
fill 13 201 37 13 201 38 minecraft:dirt
fill 13 202 37 13 202 38 minecraft:podzol
fill 1 201 26 1 205 29 minecraft:calcite
fill 1 206 26 1 206 29 minecraft:podzol
fill 1 201 30 1 205 31 minecraft:diorite
fill 1 206 30 1 206 31 minecraft:podzol
execute positioned 4 201 34 run function rlk:room/prop/fo_rock
execute positioned 4 201 29 run function rlk:room/prop/fo_col_b
execute positioned 18 201 36 run function rlk:room/prop/fo_col_b
execute positioned 4 201 26 run function rlk:room/prop/fo_tree_b
execute positioned 4 201 25 run function rlk:room/prop/p_grass
execute positioned 6 201 30 run function rlk:room/prop/fo_flower
execute positioned 6 201 26 run function rlk:room/prop/fo_white
execute positioned 10 202 35 run function rlk:room/prop/p_grass
execute positioned 2 201 30 run function rlk:room/prop/fo_white
execute positioned 13 201 27 run function rlk:room/prop/fo_flower
execute positioned 9 201 34 run function rlk:room/prop/p_grass
execute positioned 6 201 26 run function rlk:room/prop/fo_flower
execute positioned 15 201 23 run function rlk:room/prop/fo_white
setblock 1 207 26 minecraft:short_grass keep
setblock 1 207 27 minecraft:birch_leaves[persistent=true] keep
setblock 1 207 29 minecraft:short_grass keep
setblock 1 207 30 minecraft:birch_leaves[persistent=true] keep
setblock 1 207 31 minecraft:birch_leaves[persistent=true] keep
