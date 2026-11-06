# 구역 건설 (first5_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 0 201 -17 0 202 -16 minecraft:moss_block
fill 0 208 -6 0 210 -1 minecraft:calcite
fill 0 209 -6 0 210 -6 minecraft:birch_leaves[persistent=true]
fill 19 210 -3 19 210 -3 minecraft:calcite
fill 19 209 -13 19 210 -10 minecraft:diorite
fill 19 202 -2 19 203 -1 minecraft:prismarine
fill 1 202 -20 4 205 -20 minecraft:prismarine
fill 14 203 -20 16 204 -20 minecraft:prismarine
fill 11 210 -20 11 210 -20 minecraft:birch_leaves[persistent=true]
fill 2 210 -20 6 210 -20 minecraft:oak_leaves[persistent=true]
fill 3 203 -20 8 206 -20 minecraft:dark_prismarine
fill 10 201 -20 12 201 -20 minecraft:moss_block
fill 2 203 -1 3 203 -1 minecraft:calcite
fill 15 210 -1 19 210 -1 minecraft:birch_leaves[persistent=true]
fill 13 204 -1 17 206 -1 minecraft:dark_prismarine
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 6 201 -19 6 201 -15 minecraft:podzol
fill 9 201 -19 10 201 -19 minecraft:podzol
fill 10 201 -18 10 201 -15 minecraft:podzol
fill 7 201 -15 9 201 -15 minecraft:podzol
fill 15 201 -9 17 201 -8 minecraft:podzol
fill 18 201 -8 18 201 -8 minecraft:podzol
fill 15 201 -7 15 201 -7 minecraft:podzol
fill 16 201 -6 16 201 -2 minecraft:podzol
fill 17 201 -2 18 201 -2 minecraft:podzol
fill 7 201 -19 8 201 -18 minecraft:dirt
fill 7 202 -19 8 202 -18 minecraft:podzol
fill 9 201 -18 9 201 -18 minecraft:dirt
fill 9 202 -18 9 202 -18 minecraft:podzol
fill 7 201 -17 7 201 -16 minecraft:dirt
fill 7 202 -17 7 202 -16 minecraft:podzol
fill 16 201 -7 18 201 -7 minecraft:dirt
fill 16 202 -7 18 202 -7 minecraft:podzol
fill 17 201 -6 18 201 -3 minecraft:dirt
fill 17 202 -6 18 202 -3 minecraft:podzol
fill 8 201 -17 8 207 -16 minecraft:calcite
fill 8 208 -17 8 208 -16 minecraft:podzol
fill 17 201 -15 18 207 -13 minecraft:calcite
fill 17 208 -15 18 208 -13 minecraft:podzol
fill 9 201 -17 9 207 -16 minecraft:diorite
fill 9 208 -17 9 208 -16 minecraft:podzol
fill 17 201 -12 18 207 -11 minecraft:diorite
fill 17 208 -12 18 208 -11 minecraft:podzol
fill 0 186 -20 4 199 -13 minecraft:stone
fill 1 186 -19 3 186 -14 minecraft:clay
fill 1 187 -19 3 188 -14 minecraft:water
fill 1 189 -19 3 201 -14 minecraft:air
execute positioned 13 201 -16 run function rlk:room/prop/fo_col_b
execute positioned 1 201 -4 run function rlk:room/prop/fo_rock_s
execute positioned 3 201 -6 run function rlk:room/prop/fo_col_a
execute positioned 7 201 -4 run function rlk:room/prop/p_grass
execute positioned 10 201 -5 run function rlk:room/prop/fo_flower
execute positioned 13 201 -17 run function rlk:room/prop/p_grass
execute positioned 18 203 -3 run function rlk:room/prop/fo_white
execute positioned 14 201 -3 run function rlk:room/prop/fo_flower
execute positioned 6 202 -17 run function rlk:room/prop/fo_flower
execute positioned 13 201 -13 run function rlk:room/prop/fo_white
execute positioned 11 201 -9 run function rlk:room/prop/fo_flower
execute positioned 12 201 -19 run function rlk:room/prop/p_grass
setblock 8 209 -17 minecraft:birch_leaves[persistent=true] keep
setblock 8 209 -16 minecraft:birch_leaves[persistent=true] keep
setblock 9 209 -17 minecraft:short_grass keep
setblock 17 209 -14 minecraft:birch_leaves[persistent=true] keep
setblock 17 209 -13 minecraft:birch_leaves[persistent=true] keep
setblock 17 209 -12 minecraft:short_grass keep
setblock 18 209 -15 minecraft:birch_leaves[persistent=true] keep
setblock 18 209 -13 minecraft:birch_leaves[persistent=true] keep
setblock 18 209 -12 minecraft:birch_leaves[persistent=true] keep
setblock 18 209 -11 minecraft:short_grass keep
