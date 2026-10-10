# 구역 건설 (first6_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 11 200 -13 12 200 -10 minecraft:gravel
fill 11 200 -19 15 200 -16 minecraft:moss_block
fill 0 201 -16 0 203 -15 minecraft:calcite
fill 0 201 -4 0 201 -2 minecraft:prismarine
fill 0 210 -8 0 210 -5 minecraft:birch_leaves[persistent=true]
fill 0 204 -12 0 206 -11 minecraft:calcite
fill 0 204 -6 0 207 -1 minecraft:moss_block
fill 0 209 -12 0 210 -11 minecraft:oak_leaves[persistent=true]
fill 19 202 -11 19 205 -9 minecraft:calcite
fill 19 210 -5 19 210 -4 minecraft:birch_leaves[persistent=true]
fill 19 210 -20 19 210 -17 minecraft:oak_leaves[persistent=true]
fill 16 203 -20 19 203 -20 minecraft:calcite
fill 8 204 -20 10 206 -20 minecraft:calcite
fill 2 210 -20 4 210 -20 minecraft:birch_leaves[persistent=true]
fill 6 204 -20 8 207 -20 minecraft:diorite
fill 15 206 -1 17 208 -1 minecraft:diorite
fill 14 204 -1 19 205 -1 minecraft:diorite
fill 0 210 -1 0 210 -1 minecraft:prismarine
fill 6 209 -1 6 210 -1 minecraft:calcite
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -19 4 201 -19 minecraft:podzol
fill 4 201 -18 4 201 -18 minecraft:podzol
fill 3 201 -15 4 201 -15 minecraft:podzol
fill 1 201 -14 3 201 -14 minecraft:podzol
fill 1 201 -13 1 201 -13 minecraft:podzol
fill 1 201 -19 2 201 -15 minecraft:dirt
fill 1 202 -19 2 202 -15 minecraft:podzol
fill 3 201 -18 3 201 -16 minecraft:dirt
fill 3 202 -18 3 202 -16 minecraft:podzol
fill 8 201 -2 12 205 -2 minecraft:calcite
fill 8 206 -2 12 206 -2 minecraft:podzol
fill 4 201 -17 5 207 -16 minecraft:calcite
fill 4 208 -17 5 208 -16 minecraft:podzol
fill 9 201 -17 10 207 -16 minecraft:diorite
fill 9 208 -17 10 208 -16 minecraft:podzol
execute positioned 1 201 -9 run function rlk:room/prop/fo_ruin_x
execute positioned 11 201 -9 run function rlk:room/prop/fo_flower
execute positioned 17 201 -11 run function rlk:room/prop/p_grass
execute positioned 6 201 -5 run function rlk:room/prop/p_grass
execute positioned 8 201 -10 run function rlk:room/prop/fo_flower
execute positioned 11 201 -10 run function rlk:room/prop/p_grass
execute positioned 9 201 -9 run function rlk:room/prop/fo_flower
execute positioned 16 201 -12 run function rlk:room/prop/p_grass
execute positioned 11 201 -16 run function rlk:room/prop/fo_flower
execute positioned 7 201 -3 run function rlk:room/prop/fo_flower
setblock 4 209 -16 minecraft:short_grass keep
setblock 9 209 -17 minecraft:birch_leaves[persistent=true] keep
setblock 10 209 -17 minecraft:short_grass keep
setblock 10 209 -16 minecraft:birch_leaves[persistent=true] keep
setblock 11 207 -2 minecraft:short_grass keep
setblock 12 207 -2 minecraft:short_grass keep
