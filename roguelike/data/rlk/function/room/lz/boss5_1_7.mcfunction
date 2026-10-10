# 구역 건설 (boss5_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -12 200 7 -11 200 8 minecraft:coarse_dirt
fill -17 200 2 -16 200 3 minecraft:coarse_dirt
fill -12 200 8 -10 200 11 minecraft:gravel
fill -12 200 3 -10 200 6 minecraft:calcite
fill -20 201 14 -20 204 16 minecraft:calcite
fill -20 204 16 -20 206 18 minecraft:diorite
fill -20 203 11 -20 203 15 minecraft:dark_prismarine
fill -20 201 3 -20 203 4 minecraft:moss_block
fill -20 206 19 -20 207 19 minecraft:diorite
fill -20 207 8 -20 209 9 minecraft:calcite
fill -1 204 4 -1 205 4 minecraft:moss_block
fill -1 210 11 -1 210 13 minecraft:birch_leaves[persistent=true]
fill -1 208 7 -1 208 7 minecraft:diorite
fill -1 209 8 -1 210 8 minecraft:moss_block
fill -1 208 15 -1 209 18 minecraft:dark_prismarine
fill -1 204 19 -1 206 19 minecraft:diorite
fill -10 210 0 -5 210 0 minecraft:oak_leaves[persistent=true]
fill -20 210 0 -16 210 0 minecraft:oak_leaves[persistent=true]
fill -5 209 0 -2 210 0 minecraft:oak_leaves[persistent=true]
fill -15 207 0 -13 207 0 minecraft:diorite
fill -13 201 0 -8 203 0 minecraft:diorite
fill -4 209 0 -1 210 0 minecraft:oak_leaves[persistent=true]
fill -17 209 19 -14 210 19 minecraft:oak_leaves[persistent=true]
fill -13 209 19 -10 210 19 minecraft:oak_leaves[persistent=true]
fill -19 204 19 -16 205 19 minecraft:moss_block
fill -7 210 19 -2 210 19 minecraft:birch_leaves[persistent=true]
fill -7 210 19 -2 210 19 minecraft:oak_leaves[persistent=true]
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -4 201 11 -2 201 12 minecraft:podzol
fill -5 201 12 -5 201 14 minecraft:podzol
fill -7 201 15 -6 201 16 minecraft:podzol
fill -6 201 17 -5 201 18 minecraft:podzol
fill -4 201 18 -2 201 18 minecraft:podzol
fill -4 201 13 -2 201 17 minecraft:dirt
fill -4 202 13 -2 202 17 minecraft:podzol
fill -5 201 15 -5 201 16 minecraft:dirt
fill -5 202 15 -5 202 16 minecraft:podzol
fill -3 201 3 -2 205 5 minecraft:calcite
fill -3 206 3 -2 206 5 minecraft:podzol
fill -3 201 6 -2 205 7 minecraft:diorite
fill -3 206 6 -2 206 7 minecraft:podzol
fill -19 199 1 -11 199 3 minecraft:clay
fill -19 200 1 -11 200 3 minecraft:water
fill -10 199 3 -7 199 5 minecraft:clay
fill -10 200 3 -7 200 5 minecraft:water
fill -14 199 4 -11 199 4 minecraft:clay
fill -14 200 4 -11 200 4 minecraft:water
fill -11 199 5 -11 199 5 minecraft:clay
fill -11 200 5 -11 200 5 minecraft:water
fill -10 200 1 -10 200 2 minecraft:sand
fill -9 200 2 -8 200 2 minecraft:sand
fill -6 200 4 -6 200 5 minecraft:sand
fill -14 200 5 -12 200 5 minecraft:sand
setblock -19 200 1 minecraft:seagrass
setblock -15 200 3 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -13 200 4 minecraft:seagrass
setblock -12 200 1 minecraft:seagrass
setblock -11 200 2 minecraft:seagrass
setblock -10 200 3 minecraft:seagrass
setblock -9 200 3 minecraft:seagrass
setblock -8 200 5 minecraft:sea_pickle[pickles=1,waterlogged=true]
execute positioned -6 201 1 run function rlk:room/prop/fo_col_b
execute positioned -7 201 18 run function rlk:room/prop/fo_col_b
execute positioned -3 202 18 run function rlk:room/prop/fo_flower
execute positioned -17 201 7 run function rlk:room/prop/p_grass
execute positioned -5 201 1 run function rlk:room/prop/fo_flower
execute positioned -9 201 7 run function rlk:room/prop/p_grass
execute positioned -6 201 3 run function rlk:room/prop/p_grass
execute positioned -10 201 18 run function rlk:room/prop/fo_white
execute positioned -2 201 1 run function rlk:room/prop/fo_white
execute positioned -19 201 9 run function rlk:room/prop/fo_flower
setblock -3 207 3 minecraft:birch_leaves[persistent=true] keep
setblock -3 207 5 minecraft:birch_leaves[persistent=true] keep
setblock -3 207 6 minecraft:birch_leaves[persistent=true] keep
setblock -3 207 7 minecraft:short_grass keep
setblock -2 207 3 minecraft:birch_leaves[persistent=true] keep
setblock -2 207 5 minecraft:birch_leaves[persistent=true] keep
setblock -2 207 6 minecraft:birch_leaves[persistent=true] keep
