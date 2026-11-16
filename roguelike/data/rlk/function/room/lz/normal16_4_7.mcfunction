# 구역 건설 (normal16_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -10 200 11 -6 200 12 minecraft:calcite
fill -20 210 12 -20 210 16 minecraft:birch_leaves[persistent=true]
fill -20 201 0 -20 203 3 minecraft:prismarine
fill -20 208 7 -20 208 12 minecraft:calcite
fill -20 210 10 -20 210 12 minecraft:birch_leaves[persistent=true]
fill -1 209 12 -1 210 13 minecraft:oak_leaves[persistent=true]
fill -1 209 6 -1 210 7 minecraft:birch_leaves[persistent=true]
fill -1 209 13 -1 210 13 minecraft:birch_leaves[persistent=true]
fill -1 209 2 -1 210 5 minecraft:diorite
fill -10 203 0 -6 205 0 minecraft:diorite
fill -11 206 0 -7 209 0 minecraft:dark_prismarine
fill -7 207 0 -4 207 0 minecraft:calcite
fill -5 205 0 -1 205 0 minecraft:diorite
fill -8 205 0 -5 207 0 minecraft:calcite
fill -14 208 0 -9 210 0 minecraft:diorite
fill -9 205 19 -5 206 19 minecraft:calcite
fill -11 210 19 -6 210 19 minecraft:diorite
fill -7 205 19 -2 206 19 minecraft:moss_block
fill -18 202 19 -15 204 19 minecraft:diorite
fill -11 203 19 -6 203 19 minecraft:dark_prismarine
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -10 201 1 -3 201 3 minecraft:podzol
fill -14 201 2 -11 201 3 minecraft:podzol
fill -19 201 3 -15 201 3 minecraft:podzol
fill -13 201 4 -7 201 5 minecraft:podzol
fill -16 201 1 -15 201 2 minecraft:dirt
fill -16 202 1 -15 202 2 minecraft:podzol
fill -19 201 2 -17 201 2 minecraft:dirt
fill -19 202 2 -17 202 2 minecraft:podzol
fill -19 201 1 -17 202 1 minecraft:dirt
fill -19 203 1 -17 203 1 minecraft:podzol
fill -14 201 1 -13 207 1 minecraft:calcite
fill -14 208 1 -13 208 1 minecraft:podzol
fill -12 201 1 -11 207 1 minecraft:diorite
fill -12 208 1 -11 208 1 minecraft:podzol
fill -14 199 15 -7 199 16 minecraft:clay
fill -14 200 15 -7 200 16 minecraft:water
setblock -14 200 16 minecraft:seagrass
setblock -13 200 15 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock -12 200 15 minecraft:seagrass
setblock -11 200 15 minecraft:seagrass
setblock -10 200 15 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -9 200 15 minecraft:seagrass
execute positioned -11 202 4 run function rlk:room/prop/fo_pipe_x
execute positioned -2 201 18 run function rlk:room/prop/fo_col_a
execute positioned -5 201 11 run function rlk:room/prop/p_grass
execute positioned -15 201 13 run function rlk:room/prop/p_grass
execute positioned -17 201 14 run function rlk:room/prop/fo_flower
execute positioned -12 201 18 run function rlk:room/prop/fo_flower
execute positioned -15 201 9 run function rlk:room/prop/fo_white
execute positioned -4 201 9 run function rlk:room/prop/p_grass
execute positioned -18 201 8 run function rlk:room/prop/fo_white
execute positioned -17 201 16 run function rlk:room/prop/p_grass
setblock -14 209 1 minecraft:birch_leaves[persistent=true] keep
