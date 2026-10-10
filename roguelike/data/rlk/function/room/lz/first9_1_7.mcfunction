# 구역 건설 (first9_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -11 200 11 -10 200 14 minecraft:coarse_dirt
fill -5 200 14 -3 200 17 minecraft:calcite
fill -20 209 4 -20 210 7 minecraft:diorite
fill -20 202 16 -20 205 18 minecraft:diorite
fill -20 202 2 -20 203 3 minecraft:moss_block
fill -20 209 14 -20 210 14 minecraft:oak_leaves[persistent=true]
fill -20 209 0 -20 210 0 minecraft:dark_prismarine
fill -1 201 17 -1 201 17 minecraft:prismarine
fill -1 201 11 -1 201 16 minecraft:moss_block
fill -1 202 2 -1 202 2 minecraft:moss_block
fill -1 209 14 -1 210 19 minecraft:oak_leaves[persistent=true]
fill -13 210 0 -12 210 0 minecraft:calcite
fill -10 209 0 -9 209 0 minecraft:moss_block
fill -9 208 0 -6 209 0 minecraft:calcite
fill -12 210 0 -11 210 0 minecraft:oak_leaves[persistent=true]
fill -17 209 0 -12 210 0 minecraft:birch_leaves[persistent=true]
fill -14 209 19 -11 210 19 minecraft:birch_leaves[persistent=true]
fill -13 209 19 -12 210 19 minecraft:birch_leaves[persistent=true]
fill -9 210 19 -4 210 19 minecraft:oak_leaves[persistent=true]
fill -16 210 19 -13 210 19 minecraft:moss_block
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -7 201 1 -7 201 2 minecraft:podzol
fill -19 201 2 -18 201 3 minecraft:podzol
fill -8 201 2 -8 201 5 minecraft:podzol
fill -17 201 3 -17 201 4 minecraft:podzol
fill -16 201 4 -16 201 15 minecraft:podzol
fill -7 201 5 -6 201 5 minecraft:podzol
fill -15 201 6 -15 201 13 minecraft:podzol
fill -5 201 6 -5 201 9 minecraft:podzol
fill -4 201 9 -2 201 9 minecraft:podzol
fill -19 201 15 -17 201 15 minecraft:podzol
fill -19 201 16 -18 201 16 minecraft:podzol
fill -6 201 1 -2 201 1 minecraft:dirt
fill -6 202 1 -2 202 1 minecraft:podzol
fill -6 201 2 -6 201 2 minecraft:dirt
fill -6 202 2 -6 202 2 minecraft:podzol
fill -19 201 4 -18 201 5 minecraft:dirt
fill -19 202 4 -18 202 5 minecraft:podzol
fill -17 201 5 -17 201 14 minecraft:dirt
fill -17 202 5 -17 202 14 minecraft:podzol
fill -5 201 5 -5 201 5 minecraft:dirt
fill -5 202 5 -5 202 5 minecraft:podzol
fill -4 201 6 -4 201 8 minecraft:dirt
fill -4 202 6 -4 202 8 minecraft:podzol
fill -3 201 7 -2 201 8 minecraft:dirt
fill -3 202 7 -2 202 8 minecraft:podzol
fill -19 201 14 -18 201 14 minecraft:dirt
fill -19 202 14 -18 202 14 minecraft:podzol
fill -5 201 2 -2 202 2 minecraft:dirt
fill -5 203 2 -2 203 2 minecraft:podzol
fill -5 201 3 -3 202 4 minecraft:dirt
fill -5 203 3 -3 203 4 minecraft:podzol
fill -4 201 5 -3 202 5 minecraft:dirt
fill -4 203 5 -3 203 5 minecraft:podzol
fill -19 201 6 -18 202 13 minecraft:dirt
fill -19 203 6 -18 203 13 minecraft:podzol
fill -3 201 6 -2 202 6 minecraft:dirt
fill -3 203 6 -2 203 6 minecraft:podzol
fill -7 201 3 -6 207 4 minecraft:calcite
fill -7 208 3 -6 208 4 minecraft:podzol
fill -2 201 3 -2 207 5 minecraft:calcite
fill -2 208 3 -2 208 5 minecraft:podzol
fill -13 199 3 -11 199 5 minecraft:clay
fill -13 200 3 -11 200 5 minecraft:water
fill -10 199 4 -10 199 5 minecraft:clay
fill -10 200 4 -10 200 5 minecraft:water
fill -12 199 15 -2 199 16 minecraft:clay
fill -12 200 15 -2 200 16 minecraft:water
fill -12 200 2 -10 200 2 minecraft:sand
fill -14 200 3 -14 200 3 minecraft:sand
fill -9 200 4 -9 200 4 minecraft:sand
setblock -11 200 3 minecraft:seagrass
setblock -11 200 16 minecraft:seagrass
setblock -10 200 4 minecraft:seagrass
setblock -9 200 16 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -7 200 15 minecraft:seagrass
execute positioned -4 203 6 run function rlk:room/prop/fo_flower
execute positioned -2 204 2 run function rlk:room/prop/fo_flower
execute positioned -17 203 10 run function rlk:room/prop/p_grass
execute positioned -3 203 7 run function rlk:room/prop/p_grass
execute positioned -14 201 14 run function rlk:room/prop/fo_flower
execute positioned -3 202 9 run function rlk:room/prop/fo_flower
execute positioned -12 201 6 run function rlk:room/prop/fo_flower
execute positioned -10 201 12 run function rlk:room/prop/p_grass
execute positioned -7 201 7 run function rlk:room/prop/p_grass
setblock -7 209 4 minecraft:birch_leaves[persistent=true] keep
setblock -6 209 3 minecraft:birch_leaves[persistent=true] keep
setblock -2 209 4 minecraft:birch_leaves[persistent=true] keep
