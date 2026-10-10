# 구역 건설 (normal16_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 212 19 minecraft:stone
fill -19 201 1 -2 212 18 minecraft:air
fill -19 211 1 -2 211 18 minecraft:light[level=15]
fill -10 202 11 -6 202 12 minecraft:calcite
fill -20 212 12 -20 212 16 minecraft:birch_leaves[persistent=true]
fill -20 203 0 -20 205 3 minecraft:prismarine
fill -20 210 7 -20 210 12 minecraft:calcite
fill -20 212 10 -20 212 12 minecraft:birch_leaves[persistent=true]
fill -1 211 12 -1 212 13 minecraft:oak_leaves[persistent=true]
fill -1 211 6 -1 212 7 minecraft:birch_leaves[persistent=true]
fill -1 211 13 -1 212 13 minecraft:birch_leaves[persistent=true]
fill -1 211 2 -1 212 5 minecraft:diorite
fill -10 205 0 -6 207 0 minecraft:diorite
fill -11 208 0 -7 211 0 minecraft:dark_prismarine
fill -7 209 0 -4 209 0 minecraft:calcite
fill -5 207 0 -1 207 0 minecraft:diorite
fill -8 207 0 -5 209 0 minecraft:calcite
fill -14 210 0 -9 212 0 minecraft:diorite
fill -9 207 19 -5 208 19 minecraft:calcite
fill -11 212 19 -6 212 19 minecraft:diorite
fill -16 202 19 -12 202 19 minecraft:dark_prismarine
fill -7 207 19 -2 208 19 minecraft:moss_block
fill -18 204 19 -15 206 19 minecraft:diorite
fill -11 205 19 -6 205 19 minecraft:dark_prismarine
fill -20 212 0 -1 212 19 minecraft:polished_deepslate
fill -19 212 1 -2 212 18 minecraft:air
fill -2 201 1 -2 201 18 minecraft:dirt
fill -2 202 1 -2 202 18 minecraft:podzol
fill -19 201 4 -14 201 18 minecraft:dirt
fill -19 202 4 -14 202 18 minecraft:podzol
fill -6 201 4 -3 201 18 minecraft:dirt
fill -6 202 4 -3 202 18 minecraft:podzol
fill -13 201 6 -7 201 18 minecraft:dirt
fill -13 202 6 -7 202 18 minecraft:podzol
fill -10 201 1 -3 202 3 minecraft:dirt
fill -10 203 1 -3 203 3 minecraft:podzol
fill -14 201 2 -11 202 3 minecraft:dirt
fill -14 203 2 -11 203 3 minecraft:podzol
fill -19 201 3 -15 202 3 minecraft:dirt
fill -19 203 3 -15 203 3 minecraft:podzol
fill -13 201 4 -7 202 5 minecraft:dirt
fill -13 203 4 -7 203 5 minecraft:podzol
fill -16 201 1 -15 203 2 minecraft:dirt
fill -16 204 1 -15 204 2 minecraft:podzol
fill -19 201 2 -17 203 2 minecraft:dirt
fill -19 204 2 -17 204 2 minecraft:podzol
fill -19 201 1 -17 204 1 minecraft:dirt
fill -19 205 1 -17 205 1 minecraft:podzol
fill -14 201 1 -13 209 1 minecraft:calcite
fill -14 210 1 -13 210 1 minecraft:podzol
fill -12 201 1 -11 209 1 minecraft:diorite
fill -12 210 1 -11 210 1 minecraft:podzol
fill -14 201 15 -7 201 16 minecraft:clay
fill -14 202 15 -7 202 16 minecraft:water
setblock -14 202 16 minecraft:seagrass
setblock -13 202 15 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock -12 202 15 minecraft:seagrass
setblock -11 202 15 minecraft:seagrass
setblock -10 202 15 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -9 202 15 minecraft:seagrass
execute positioned -11 204 4 run function rlk:room/prop/fo_pipe_x
execute positioned -2 203 18 run function rlk:room/prop/fo_col_a
execute positioned -5 203 11 run function rlk:room/prop/p_grass
execute positioned -15 203 13 run function rlk:room/prop/p_grass
execute positioned -17 203 14 run function rlk:room/prop/fo_flower
execute positioned -12 203 18 run function rlk:room/prop/fo_flower
execute positioned -15 203 9 run function rlk:room/prop/fo_white
execute positioned -4 203 9 run function rlk:room/prop/p_grass
execute positioned -18 203 8 run function rlk:room/prop/fo_white
execute positioned -17 203 16 run function rlk:room/prop/p_grass
setblock -14 211 1 minecraft:birch_leaves[persistent=true] keep
