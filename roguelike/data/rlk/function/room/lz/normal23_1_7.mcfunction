# 구역 건설 (normal23_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -11 200 9 -7 200 12 minecraft:coarse_dirt
fill -14 200 15 -11 200 17 minecraft:coarse_dirt
fill -17 200 15 -15 200 18 minecraft:coarse_dirt
fill -20 207 1 -20 208 1 minecraft:prismarine
fill -20 202 8 -20 202 10 minecraft:calcite
fill -20 209 15 -20 210 17 minecraft:diorite
fill -1 210 3 -1 210 4 minecraft:birch_leaves[persistent=true]
fill -1 208 3 -1 210 5 minecraft:prismarine
fill -1 210 4 -1 210 6 minecraft:oak_leaves[persistent=true]
fill -1 209 13 -1 210 14 minecraft:dark_prismarine
fill -1 209 1 -1 210 3 minecraft:calcite
fill -1 209 11 -1 210 15 minecraft:birch_leaves[persistent=true]
fill -5 210 0 -5 210 0 minecraft:birch_leaves[persistent=true]
fill -9 207 0 -8 209 0 minecraft:diorite
fill -11 207 0 -11 210 0 minecraft:calcite
fill -20 204 0 -17 206 0 minecraft:calcite
fill -12 209 0 -11 210 0 minecraft:moss_block
fill -18 209 0 -15 210 0 minecraft:moss_block
fill -7 202 19 -6 202 19 minecraft:calcite
fill -20 204 19 -19 206 19 minecraft:moss_block
fill -10 207 19 -8 207 19 minecraft:moss_block
fill -10 206 19 -9 206 19 minecraft:moss_block
fill -10 201 19 -10 204 19 minecraft:diorite
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -4 201 1 -2 201 3 minecraft:podzol
fill -19 201 8 -19 205 10 minecraft:calcite
fill -19 206 8 -19 206 10 minecraft:podzol
fill -18 201 10 -17 205 10 minecraft:calcite
fill -18 206 10 -17 206 10 minecraft:podzol
fill -18 201 8 -17 205 9 minecraft:diorite
fill -18 206 8 -17 206 9 minecraft:podzol
fill -16 199 13 -15 199 18 minecraft:clay
fill -16 200 13 -15 200 18 minecraft:water
fill -17 199 14 -17 199 18 minecraft:clay
fill -17 200 14 -17 200 18 minecraft:water
fill -14 199 15 -7 199 18 minecraft:clay
fill -14 200 15 -7 200 18 minecraft:water
fill -6 199 16 -2 199 18 minecraft:clay
fill -6 200 16 -2 200 18 minecraft:water
fill -17 200 12 -15 200 12 minecraft:sand
fill -18 200 13 -17 200 13 minecraft:sand
fill -18 200 14 -18 200 18 minecraft:sand
setblock -16 200 15 minecraft:seagrass
setblock -15 200 14 minecraft:seagrass
setblock -13 200 18 minecraft:seagrass
setblock -12 200 16 minecraft:seagrass
setblock -10 200 15 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -10 200 17 minecraft:seagrass
setblock -9 200 18 minecraft:seagrass
setblock -8 200 17 minecraft:seagrass
setblock -7 200 17 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -5 200 17 minecraft:seagrass
setblock -4 200 17 minecraft:seagrass
execute positioned -19 201 3 run function rlk:room/prop/fo_col_a
execute positioned -16 201 9 run function rlk:room/prop/fo_white
execute positioned -9 201 14 run function rlk:room/prop/p_grass
execute positioned -19 201 15 run function rlk:room/prop/p_grass
execute positioned -8 201 4 run function rlk:room/prop/fo_flower
execute positioned -14 201 10 run function rlk:room/prop/p_grass
execute positioned -12 201 6 run function rlk:room/prop/fo_white
execute positioned -4 202 3 run function rlk:room/prop/fo_flower
setblock -19 207 10 minecraft:birch_leaves[persistent=true] keep
setblock -18 207 8 minecraft:short_grass keep
setblock -17 207 8 minecraft:birch_leaves[persistent=true] keep
setblock -17 207 9 minecraft:birch_leaves[persistent=true] keep
