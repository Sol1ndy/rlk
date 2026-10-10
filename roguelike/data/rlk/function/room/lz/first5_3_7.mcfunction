# 구역 건설 (first5_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 212 -1 minecraft:stone
fill 1 201 -19 18 212 -2 minecraft:air
fill 1 211 -19 18 211 -2 minecraft:light[level=15]
fill 0 201 -17 0 204 -16 minecraft:moss_block
fill 0 210 -6 0 212 -1 minecraft:calcite
fill 0 211 -6 0 212 -6 minecraft:birch_leaves[persistent=true]
fill 19 212 -3 19 212 -3 minecraft:calcite
fill 19 211 -13 19 212 -10 minecraft:diorite
fill 19 204 -2 19 205 -1 minecraft:prismarine
fill 1 204 -20 4 207 -20 minecraft:prismarine
fill 14 205 -20 16 206 -20 minecraft:prismarine
fill 11 212 -20 11 212 -20 minecraft:birch_leaves[persistent=true]
fill 2 212 -20 6 212 -20 minecraft:oak_leaves[persistent=true]
fill 3 205 -20 8 208 -20 minecraft:dark_prismarine
fill 10 202 -20 12 203 -20 minecraft:moss_block
fill 2 205 -1 3 205 -1 minecraft:calcite
fill 4 202 -1 4 202 -1 minecraft:moss_block
fill 15 212 -1 19 212 -1 minecraft:birch_leaves[persistent=true]
fill 13 206 -1 17 208 -1 minecraft:dark_prismarine
fill 0 212 -20 19 212 -1 minecraft:polished_deepslate
fill 1 212 -19 18 212 -2 minecraft:air
fill 1 201 -19 5 201 -2 minecraft:dirt
fill 1 202 -19 5 202 -2 minecraft:podzol
fill 11 201 -19 18 201 -16 minecraft:dirt
fill 11 202 -19 18 202 -16 minecraft:podzol
fill 11 201 -15 16 201 -10 minecraft:dirt
fill 11 202 -15 16 202 -10 minecraft:podzol
fill 6 201 -14 10 201 -2 minecraft:dirt
fill 6 202 -14 10 202 -2 minecraft:podzol
fill 17 201 -10 18 201 -10 minecraft:dirt
fill 17 202 -10 18 202 -10 minecraft:podzol
fill 11 201 -9 14 201 -2 minecraft:dirt
fill 11 202 -9 14 202 -2 minecraft:podzol
fill 18 201 -9 18 201 -9 minecraft:dirt
fill 18 202 -9 18 202 -9 minecraft:podzol
fill 15 201 -6 15 201 -2 minecraft:dirt
fill 15 202 -6 15 202 -2 minecraft:podzol
fill 6 201 -19 6 202 -15 minecraft:dirt
fill 6 203 -19 6 203 -15 minecraft:podzol
fill 9 201 -19 10 202 -19 minecraft:dirt
fill 9 203 -19 10 203 -19 minecraft:podzol
fill 10 201 -18 10 202 -15 minecraft:dirt
fill 10 203 -18 10 203 -15 minecraft:podzol
fill 7 201 -15 9 202 -15 minecraft:dirt
fill 7 203 -15 9 203 -15 minecraft:podzol
fill 15 201 -9 17 202 -8 minecraft:dirt
fill 15 203 -9 17 203 -8 minecraft:podzol
fill 18 201 -8 18 202 -8 minecraft:dirt
fill 18 203 -8 18 203 -8 minecraft:podzol
fill 15 201 -7 15 202 -7 minecraft:dirt
fill 15 203 -7 15 203 -7 minecraft:podzol
fill 16 201 -6 16 202 -2 minecraft:dirt
fill 16 203 -6 16 203 -2 minecraft:podzol
fill 17 201 -2 18 202 -2 minecraft:dirt
fill 17 203 -2 18 203 -2 minecraft:podzol
fill 7 201 -19 8 203 -18 minecraft:dirt
fill 7 204 -19 8 204 -18 minecraft:podzol
fill 9 201 -18 9 203 -18 minecraft:dirt
fill 9 204 -18 9 204 -18 minecraft:podzol
fill 7 201 -17 7 203 -16 minecraft:dirt
fill 7 204 -17 7 204 -16 minecraft:podzol
fill 16 201 -7 18 203 -7 minecraft:dirt
fill 16 204 -7 18 204 -7 minecraft:podzol
fill 17 201 -6 18 203 -3 minecraft:dirt
fill 17 204 -6 18 204 -3 minecraft:podzol
fill 8 201 -17 8 209 -16 minecraft:calcite
fill 8 210 -17 8 210 -16 minecraft:podzol
fill 17 201 -15 18 209 -13 minecraft:calcite
fill 17 210 -15 18 210 -13 minecraft:podzol
fill 9 201 -17 9 209 -16 minecraft:diorite
fill 9 210 -17 9 210 -16 minecraft:podzol
fill 17 201 -12 18 209 -11 minecraft:diorite
fill 17 210 -12 18 210 -11 minecraft:podzol
fill 0 186 -20 4 199 -13 minecraft:stone
fill 1 186 -19 3 186 -14 minecraft:clay
fill 1 187 -19 3 188 -14 minecraft:water
fill 1 189 -19 3 203 -14 minecraft:air
execute positioned 13 203 -16 run function rlk:room/prop/fo_col_b
execute positioned 1 203 -4 run function rlk:room/prop/fo_rock_s
execute positioned 3 203 -6 run function rlk:room/prop/fo_col_a
execute positioned 7 203 -4 run function rlk:room/prop/p_grass
execute positioned 10 203 -5 run function rlk:room/prop/fo_flower
execute positioned 13 203 -17 run function rlk:room/prop/p_grass
execute positioned 18 205 -3 run function rlk:room/prop/fo_white
execute positioned 14 203 -3 run function rlk:room/prop/fo_flower
execute positioned 6 204 -17 run function rlk:room/prop/fo_flower
execute positioned 13 203 -13 run function rlk:room/prop/fo_white
execute positioned 11 203 -9 run function rlk:room/prop/fo_flower
execute positioned 12 203 -19 run function rlk:room/prop/p_grass
setblock 8 211 -17 minecraft:birch_leaves[persistent=true] keep
setblock 8 211 -16 minecraft:birch_leaves[persistent=true] keep
setblock 9 211 -17 minecraft:short_grass keep
setblock 17 211 -14 minecraft:birch_leaves[persistent=true] keep
setblock 17 211 -13 minecraft:birch_leaves[persistent=true] keep
setblock 17 211 -12 minecraft:short_grass keep
setblock 18 211 -15 minecraft:birch_leaves[persistent=true] keep
setblock 18 211 -13 minecraft:birch_leaves[persistent=true] keep
setblock 18 211 -12 minecraft:birch_leaves[persistent=true] keep
setblock 18 211 -11 minecraft:short_grass keep
