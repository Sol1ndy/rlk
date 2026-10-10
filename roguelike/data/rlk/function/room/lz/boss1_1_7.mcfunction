# 구역 건설 (boss1_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -15 200 5 -11 200 8 minecraft:coarse_dirt
fill -4 200 12 -3 200 14 minecraft:gravel
fill -12 200 2 -11 200 5 minecraft:moss_block
fill -20 206 16 -20 207 16 minecraft:diorite
fill -20 204 5 -20 206 8 minecraft:calcite
fill -20 210 3 -20 210 5 minecraft:oak_leaves[persistent=true]
fill -1 208 9 -1 210 11 minecraft:moss_block
fill -1 209 9 -1 210 14 minecraft:prismarine
fill -1 209 0 -1 210 5 minecraft:birch_leaves[persistent=true]
fill -1 202 12 -1 203 14 minecraft:dark_prismarine
fill -1 210 11 -1 210 12 minecraft:oak_leaves[persistent=true]
fill -19 204 0 -18 205 0 minecraft:calcite
fill -3 209 0 -3 210 0 minecraft:birch_leaves[persistent=true]
fill -7 209 0 -6 210 0 minecraft:diorite
fill -6 209 0 -3 210 0 minecraft:birch_leaves[persistent=true]
fill -18 202 0 -14 205 0 minecraft:calcite
fill -18 208 0 -15 210 0 minecraft:prismarine
fill -4 209 19 -4 210 19 minecraft:oak_leaves[persistent=true]
fill -9 205 19 -8 207 19 minecraft:calcite
fill -2 210 19 -2 210 19 minecraft:oak_leaves[persistent=true]
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -4 201 1 -2 201 4 minecraft:podzol
fill -19 201 6 -18 201 14 minecraft:podzol
fill -17 201 7 -16 201 12 minecraft:podzol
fill -15 201 9 -15 201 11 minecraft:podzol
fill -17 201 13 -16 207 13 minecraft:calcite
fill -17 208 13 -16 208 13 minecraft:podzol
fill -17 201 14 -16 207 14 minecraft:diorite
fill -17 208 14 -16 208 14 minecraft:podzol
fill -19 199 3 -17 199 5 minecraft:clay
fill -19 200 3 -17 200 5 minecraft:water
fill -17 199 6 -17 199 6 minecraft:clay
fill -17 200 6 -17 200 6 minecraft:water
fill -19 200 2 -17 200 2 minecraft:sand
fill -16 200 6 -16 200 6 minecraft:sand
setblock -19 200 4 minecraft:seagrass
setblock -18 200 4 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock -17 200 3 minecraft:seagrass
setblock -17 200 6 minecraft:seagrass
execute positioned -5 201 13 run function rlk:room/prop/fo_col_b
execute positioned -19 202 10 run function rlk:room/prop/fo_lamp
execute positioned -12 201 15 run function rlk:room/prop/p_grass
execute positioned -2 201 10 run function rlk:room/prop/fo_white
execute positioned -2 202 4 run function rlk:room/prop/fo_flower
execute positioned -5 201 18 run function rlk:room/prop/fo_flower
execute positioned -8 201 5 run function rlk:room/prop/fo_flower
execute positioned -9 201 8 run function rlk:room/prop/fo_white
execute positioned -10 201 2 run function rlk:room/prop/fo_flower
