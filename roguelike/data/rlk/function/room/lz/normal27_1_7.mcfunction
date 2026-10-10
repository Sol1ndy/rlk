# 구역 건설 (normal27_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 8 200 -12 9 200 -10 minecraft:calcite
fill 15 200 -14 18 200 -13 minecraft:moss_block
fill 0 204 -16 0 207 -11 minecraft:moss_block
fill 0 206 -16 0 209 -12 minecraft:calcite
fill 0 210 -17 0 210 -15 minecraft:birch_leaves[persistent=true]
fill 19 209 -7 19 210 -5 minecraft:birch_leaves[persistent=true]
fill 19 209 -16 19 210 -13 minecraft:diorite
fill 19 204 -16 19 204 -11 minecraft:calcite
fill 19 208 -20 19 208 -20 minecraft:dark_prismarine
fill 8 209 -20 13 210 -20 minecraft:oak_leaves[persistent=true]
fill 7 203 -20 8 205 -20 minecraft:calcite
fill 5 204 -1 8 206 -1 minecraft:moss_block
fill 2 205 -1 2 205 -1 minecraft:calcite
fill 1 208 -1 3 208 -1 minecraft:moss_block
fill 5 204 -1 8 204 -1 minecraft:calcite
fill 5 208 -1 6 210 -1 minecraft:moss_block
fill 6 210 -1 7 210 -1 minecraft:birch_leaves[persistent=true]
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 4 201 -19 5 201 -18 minecraft:podzol
fill 5 201 -17 18 201 -17 minecraft:podzol
fill 1 201 -10 5 201 -10 minecraft:podzol
fill 1 201 -9 1 201 -9 minecraft:podzol
fill 5 201 -9 5 201 -6 minecraft:podzol
fill 6 201 -5 9 201 -5 minecraft:podzol
fill 9 201 -4 9 201 -2 minecraft:podzol
fill 8 201 -2 8 201 -2 minecraft:podzol
fill 6 201 -19 18 201 -18 minecraft:dirt
fill 6 202 -19 18 202 -18 minecraft:podzol
fill 2 201 -9 4 201 -8 minecraft:dirt
fill 2 202 -9 4 202 -8 minecraft:podzol
fill 1 201 -8 1 201 -6 minecraft:dirt
fill 1 202 -8 1 202 -6 minecraft:podzol
fill 4 201 -7 4 201 -6 minecraft:dirt
fill 4 202 -7 4 202 -6 minecraft:podzol
fill 5 201 -5 5 201 -5 minecraft:dirt
fill 5 202 -5 5 202 -5 minecraft:podzol
fill 1 201 -4 1 201 -2 minecraft:dirt
fill 1 202 -4 1 202 -2 minecraft:podzol
fill 6 201 -4 8 201 -4 minecraft:dirt
fill 6 202 -4 8 202 -4 minecraft:podzol
fill 7 201 -3 8 201 -3 minecraft:dirt
fill 7 202 -3 8 202 -3 minecraft:podzol
fill 2 201 -2 3 201 -2 minecraft:dirt
fill 2 202 -2 3 202 -2 minecraft:podzol
fill 5 201 -2 7 201 -2 minecraft:dirt
fill 5 202 -2 7 202 -2 minecraft:podzol
fill 2 201 -7 3 202 -3 minecraft:dirt
fill 2 203 -7 3 203 -3 minecraft:podzol
fill 1 201 -5 1 202 -5 minecraft:dirt
fill 1 203 -5 1 203 -5 minecraft:podzol
fill 4 201 -5 4 202 -2 minecraft:dirt
fill 4 203 -5 4 203 -2 minecraft:podzol
fill 5 201 -4 5 202 -3 minecraft:dirt
fill 5 203 -4 5 203 -3 minecraft:podzol
fill 6 201 -3 6 202 -3 minecraft:dirt
fill 6 203 -3 6 203 -3 minecraft:podzol
fill 14 199 -15 18 199 -15 minecraft:clay
fill 14 200 -15 18 200 -15 minecraft:water
fill 15 199 -14 18 199 -6 minecraft:clay
fill 15 200 -14 18 200 -6 minecraft:water
fill 13 200 -15 13 200 -15 minecraft:sand
fill 14 200 -5 18 200 -5 minecraft:sand
setblock 14 200 -15 minecraft:seagrass
setblock 15 200 -14 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 15 200 -9 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 15 200 -8 minecraft:seagrass
setblock 16 200 -12 minecraft:seagrass
setblock 17 200 -12 minecraft:seagrass
setblock 17 200 -10 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 17 200 -6 minecraft:seagrass
execute positioned 5 202 -10 run function rlk:room/prop/fo_pipe_z
execute positioned 6 201 -15 run function rlk:room/prop/fo_crates
execute positioned 8 202 -2 run function rlk:room/prop/fo_white
execute positioned 6 201 -10 run function rlk:room/prop/p_grass
execute positioned 18 201 -3 run function rlk:room/prop/fo_white
execute positioned 9 202 -17 run function rlk:room/prop/fo_white
execute positioned 10 202 -17 run function rlk:room/prop/fo_flower
execute positioned 5 202 -19 run function rlk:room/prop/p_grass
execute positioned 5 202 -10 run function rlk:room/prop/fo_flower
