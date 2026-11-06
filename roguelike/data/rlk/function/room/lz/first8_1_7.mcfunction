# 구역 건설 (first8_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -13 200 -8 -12 200 -5 minecraft:moss_block
fill -15 200 -9 -13 200 -8 minecraft:coarse_dirt
fill -20 205 -11 -20 205 -6 minecraft:diorite
fill -20 202 -12 -20 205 -8 minecraft:prismarine
fill -20 210 -14 -20 210 -12 minecraft:oak_leaves[persistent=true]
fill -20 206 -16 -20 208 -14 minecraft:calcite
fill -1 204 -11 -1 204 -10 minecraft:moss_block
fill -1 203 -2 -1 205 -2 minecraft:calcite
fill -1 209 -8 -1 210 -5 minecraft:birch_leaves[persistent=true]
fill -1 205 -18 -1 207 -14 minecraft:prismarine
fill -1 210 -2 -1 210 -1 minecraft:moss_block
fill -6 210 -20 -2 210 -20 minecraft:birch_leaves[persistent=true]
fill -12 210 -20 -12 210 -20 minecraft:oak_leaves[persistent=true]
fill -8 210 -20 -6 210 -20 minecraft:birch_leaves[persistent=true]
fill -1 210 -20 -1 210 -20 minecraft:oak_leaves[persistent=true]
fill -10 210 -20 -10 210 -20 minecraft:prismarine
fill -5 209 -1 -3 210 -1 minecraft:birch_leaves[persistent=true]
fill -11 201 -1 -8 203 -1 minecraft:moss_block
fill -12 204 -1 -7 206 -1 minecraft:moss_block
fill -15 205 -1 -14 205 -1 minecraft:prismarine
fill -15 209 -1 -12 210 -1 minecraft:oak_leaves[persistent=true]
fill -5 206 -1 -5 206 -1 minecraft:prismarine
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -18 201 -19 -18 201 -16 minecraft:podzol
fill -17 201 -15 -17 201 -14 minecraft:podzol
fill -16 201 -13 -15 201 -13 minecraft:podzol
fill -15 201 -12 -15 201 -10 minecraft:podzol
fill -16 201 -10 -16 201 -9 minecraft:podzol
fill -19 201 -9 -17 201 -9 minecraft:podzol
fill -19 201 -19 -19 201 -16 minecraft:dirt
fill -19 202 -19 -19 202 -16 minecraft:podzol
fill -18 201 -15 -18 201 -14 minecraft:dirt
fill -18 202 -15 -18 202 -14 minecraft:podzol
fill -17 201 -13 -17 201 -13 minecraft:dirt
fill -17 202 -13 -17 202 -13 minecraft:podzol
fill -16 201 -12 -16 201 -11 minecraft:dirt
fill -16 202 -12 -16 202 -11 minecraft:podzol
fill -19 201 -11 -17 201 -10 minecraft:dirt
fill -19 202 -11 -17 202 -10 minecraft:podzol
fill -19 201 -15 -19 202 -12 minecraft:dirt
fill -19 203 -15 -19 203 -12 minecraft:podzol
fill -18 201 -13 -18 202 -12 minecraft:dirt
fill -18 203 -13 -18 203 -12 minecraft:podzol
fill -17 201 -12 -17 202 -12 minecraft:dirt
fill -17 203 -12 -17 203 -12 minecraft:podzol
fill -8 201 -3 -5 206 -2 minecraft:calcite
fill -8 207 -3 -5 207 -2 minecraft:podzol
fill -17 201 -7 -16 206 -6 minecraft:diorite
fill -17 207 -7 -16 207 -6 minecraft:podzol
execute positioned -11 201 -4 run function rlk:room/prop/fo_col_b
execute positioned -13 201 -5 run function rlk:room/prop/fo_pipe_x
execute positioned -4 201 -10 run function rlk:room/prop/fo_flower
execute positioned -14 201 -18 run function rlk:room/prop/fo_white
execute positioned -9 201 -5 run function rlk:room/prop/fo_flower
execute positioned -2 201 -14 run function rlk:room/prop/p_grass
execute positioned -11 201 -11 run function rlk:room/prop/fo_white
execute positioned -7 201 -15 run function rlk:room/prop/p_grass
execute positioned -12 201 -2 run function rlk:room/prop/p_grass
execute positioned -5 201 -4 run function rlk:room/prop/fo_flower
execute positioned -2 201 -14 run function rlk:room/prop/fo_white
execute positioned -15 201 -16 run function rlk:room/prop/fo_flower
setblock -16 208 -7 minecraft:birch_leaves[persistent=true] keep
setblock -16 208 -6 minecraft:birch_leaves[persistent=true] keep
setblock -8 208 -3 minecraft:birch_leaves[persistent=true] keep
setblock -7 208 -2 minecraft:birch_leaves[persistent=true] keep
setblock -6 208 -3 minecraft:birch_leaves[persistent=true] keep
setblock -6 208 -2 minecraft:birch_leaves[persistent=true] keep
setblock -5 208 -3 minecraft:birch_leaves[persistent=true] keep
setblock -5 208 -2 minecraft:short_grass keep
