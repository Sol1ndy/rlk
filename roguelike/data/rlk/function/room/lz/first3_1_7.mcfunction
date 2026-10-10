# 구역 건설 (first3_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -18 200 3 -16 200 4 minecraft:coarse_dirt
fill -20 209 2 -20 210 7 minecraft:prismarine
fill -20 210 11 -20 210 13 minecraft:birch_leaves[persistent=true]
fill -20 209 0 -20 209 1 minecraft:diorite
fill -20 201 0 -20 202 4 minecraft:calcite
fill -20 201 10 -20 202 14 minecraft:calcite
fill -1 209 5 -1 210 7 minecraft:oak_leaves[persistent=true]
fill -1 209 3 -1 210 3 minecraft:oak_leaves[persistent=true]
fill -1 209 13 -1 210 15 minecraft:oak_leaves[persistent=true]
fill -20 201 0 -18 202 0 minecraft:moss_block
fill -16 209 0 -13 210 0 minecraft:birch_leaves[persistent=true]
fill -19 208 0 -19 210 0 minecraft:calcite
fill -7 210 0 -5 210 0 minecraft:oak_leaves[persistent=true]
fill -13 209 0 -8 210 0 minecraft:birch_leaves[persistent=true]
fill -13 210 0 -10 210 0 minecraft:diorite
fill -12 203 19 -10 205 19 minecraft:dark_prismarine
fill -17 204 19 -15 204 19 minecraft:dark_prismarine
fill -6 207 19 -5 207 19 minecraft:calcite
fill -14 202 19 -10 204 19 minecraft:moss_block
fill -5 201 19 -2 203 19 minecraft:diorite
fill -17 210 19 -12 210 19 minecraft:calcite
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -17 201 7 -15 201 13 minecraft:podzol
fill -18 201 8 -18 201 12 minecraft:podzol
fill -5 201 18 -2 206 18 minecraft:calcite
fill -5 207 18 -2 207 18 minecraft:podzol
fill -19 199 1 -17 199 6 minecraft:clay
fill -19 200 1 -17 200 6 minecraft:water
fill -16 199 6 -16 199 6 minecraft:clay
fill -16 200 6 -16 200 6 minecraft:water
fill -19 199 7 -18 199 7 minecraft:clay
fill -19 200 7 -18 200 7 minecraft:water
fill -19 199 8 -19 199 16 minecraft:clay
fill -19 200 8 -19 200 16 minecraft:water
fill -18 199 13 -18 199 16 minecraft:clay
fill -18 200 13 -18 200 16 minecraft:water
fill -17 199 14 -15 199 16 minecraft:clay
fill -17 200 14 -15 200 16 minecraft:water
fill -14 199 15 -9 199 16 minecraft:clay
fill -14 200 15 -9 200 16 minecraft:water
fill -15 200 6 -15 200 6 minecraft:sand
setblock -18 200 14 minecraft:seagrass
setblock -17 200 1 minecraft:seagrass
setblock -16 200 6 minecraft:seagrass
setblock -16 200 16 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -13 200 16 minecraft:seagrass
setblock -10 200 16 minecraft:seagrass
execute positioned -10 201 8 run function rlk:room/prop/p_grass
execute positioned -5 201 12 run function rlk:room/prop/fo_flower
execute positioned -18 202 9 run function rlk:room/prop/fo_flower
execute positioned -8 201 16 run function rlk:room/prop/p_grass
execute positioned -10 201 14 run function rlk:room/prop/fo_flower
execute positioned -10 201 7 run function rlk:room/prop/p_grass
execute positioned -5 201 16 run function rlk:room/prop/fo_white
execute positioned -16 201 18 run function rlk:room/prop/fo_white
execute positioned -15 202 8 run function rlk:room/prop/p_grass
setblock -5 208 18 minecraft:birch_leaves[persistent=true] keep
setblock -3 208 18 minecraft:short_grass keep
