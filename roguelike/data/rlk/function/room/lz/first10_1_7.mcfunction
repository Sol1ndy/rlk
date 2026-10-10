# 구역 건설 (first10_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 5 200 -19 8 200 -16 minecraft:moss_block
fill 9 200 -14 12 200 -12 minecraft:calcite
fill 0 210 -9 0 210 -9 minecraft:birch_leaves[persistent=true]
fill 0 201 -15 0 202 -13 minecraft:dark_prismarine
fill 0 203 -3 0 203 -2 minecraft:diorite
fill 0 207 -16 0 210 -12 minecraft:calcite
fill 0 205 -4 0 206 -4 minecraft:calcite
fill 19 209 -6 19 210 -5 minecraft:oak_leaves[persistent=true]
fill 19 209 -4 19 210 -3 minecraft:moss_block
fill 19 207 -5 19 209 -2 minecraft:dark_prismarine
fill 19 203 -5 19 206 -2 minecraft:calcite
fill 19 203 -9 19 203 -7 minecraft:diorite
fill 9 201 -20 14 204 -20 minecraft:calcite
fill 11 210 -20 11 210 -20 minecraft:oak_leaves[persistent=true]
fill 11 203 -20 13 205 -20 minecraft:calcite
fill 10 209 -20 11 210 -20 minecraft:oak_leaves[persistent=true]
fill 0 210 -20 4 210 -20 minecraft:birch_leaves[persistent=true]
fill 5 209 -1 6 210 -1 minecraft:birch_leaves[persistent=true]
fill 13 210 -1 18 210 -1 minecraft:oak_leaves[persistent=true]
fill 4 209 -1 8 210 -1 minecraft:birch_leaves[persistent=true]
fill 4 202 -1 6 205 -1 minecraft:moss_block
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 12 201 -5 13 201 -4 minecraft:podzol
fill 11 201 -4 11 201 -2 minecraft:podzol
fill 14 201 -4 18 201 -4 minecraft:podzol
fill 12 201 -3 12 201 -2 minecraft:podzol
fill 13 201 -3 18 201 -2 minecraft:dirt
fill 13 202 -3 18 202 -2 minecraft:podzol
fill 13 201 -19 14 205 -19 minecraft:calcite
fill 13 206 -19 14 206 -19 minecraft:podzol
fill 15 201 -19 16 205 -19 minecraft:diorite
fill 15 206 -19 16 206 -19 minecraft:podzol
fill 3 199 -19 5 199 -14 minecraft:clay
fill 3 200 -19 5 200 -14 minecraft:water
fill 3 199 -11 5 199 -2 minecraft:clay
fill 3 200 -11 5 200 -2 minecraft:water
fill 3 200 -13 5 200 -12 minecraft:spruce_planks
setblock 3 200 -18 minecraft:seagrass
setblock 3 200 -15 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 3 200 -10 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 3 200 -6 minecraft:seagrass
setblock 3 200 -2 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 5 200 -9 minecraft:seagrass
setblock 5 200 -5 minecraft:seagrass
execute positioned 14 201 -12 run function rlk:room/prop/fo_flower
execute positioned 18 203 -3 run function rlk:room/prop/fo_white
execute positioned 1 201 -12 run function rlk:room/prop/fo_flower
execute positioned 15 202 -4 run function rlk:room/prop/p_grass
execute positioned 9 201 -14 run function rlk:room/prop/p_grass
execute positioned 11 201 -17 run function rlk:room/prop/fo_flower
execute positioned 10 201 -14 run function rlk:room/prop/fo_flower
execute positioned 9 201 -2 run function rlk:room/prop/p_grass
execute positioned 17 201 -9 run function rlk:room/prop/p_grass
setblock 14 207 -19 minecraft:birch_leaves[persistent=true] keep
setblock 16 207 -19 minecraft:short_grass keep
