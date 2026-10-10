# 구역 건설 (normal7_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:stone
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 0 209 22 0 210 24 minecraft:calcite
fill 0 206 25 0 208 30 minecraft:diorite
fill 0 206 27 0 207 30 minecraft:diorite
fill 0 209 32 0 210 33 minecraft:oak_leaves[persistent=true]
fill 0 204 36 0 207 37 minecraft:moss_block
fill 19 208 30 19 209 32 minecraft:diorite
fill 19 203 39 19 205 39 minecraft:calcite
fill 19 206 21 19 209 25 minecraft:diorite
fill 19 209 22 19 210 26 minecraft:birch_leaves[persistent=true]
fill 16 203 20 17 206 20 minecraft:calcite
fill 9 210 20 14 210 20 minecraft:birch_leaves[persistent=true]
fill 16 201 20 19 201 20 minecraft:calcite
fill 12 210 20 13 210 20 minecraft:prismarine
fill 4 209 20 9 210 20 minecraft:oak_leaves[persistent=true]
fill 9 207 39 13 207 39 minecraft:diorite
fill 13 210 39 16 210 39 minecraft:moss_block
fill 15 210 39 19 210 39 minecraft:birch_leaves[persistent=true]
fill 9 202 39 10 205 39 minecraft:diorite
fill 0 205 39 5 207 39 minecraft:moss_block
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 3 201 27 5 201 28 minecraft:podzol
fill 1 201 28 2 201 29 minecraft:podzol
fill 5 201 29 5 201 34 minecraft:podzol
fill 1 201 30 1 201 30 minecraft:podzol
fill 6 201 35 8 201 35 minecraft:podzol
fill 4 201 36 7 201 36 minecraft:podzol
fill 13 201 36 18 201 36 minecraft:podzol
fill 4 201 37 5 201 37 minecraft:podzol
fill 13 201 37 14 201 38 minecraft:podzol
fill 2 201 30 2 201 32 minecraft:dirt
fill 2 202 30 2 202 32 minecraft:podzol
fill 1 201 31 1 201 32 minecraft:dirt
fill 1 202 31 1 202 32 minecraft:podzol
fill 3 201 31 4 201 32 minecraft:dirt
fill 3 202 31 4 202 32 minecraft:podzol
fill 4 201 33 4 201 35 minecraft:dirt
fill 4 202 33 4 202 35 minecraft:podzol
fill 5 201 35 5 201 35 minecraft:dirt
fill 5 202 35 5 202 35 minecraft:podzol
fill 15 201 37 18 201 38 minecraft:dirt
fill 15 202 37 18 202 38 minecraft:podzol
fill 3 201 30 4 207 30 minecraft:calcite
fill 3 208 30 4 208 30 minecraft:podzol
fill 3 201 33 3 207 33 minecraft:calcite
fill 3 208 33 3 208 33 minecraft:podzol
fill 1 201 34 2 207 37 minecraft:calcite
fill 1 208 34 2 208 37 minecraft:podzol
fill 3 201 38 3 207 38 minecraft:calcite
fill 3 208 38 3 208 38 minecraft:podzol
fill 3 201 29 4 207 29 minecraft:diorite
fill 3 208 29 4 208 29 minecraft:podzol
fill 1 201 33 2 207 33 minecraft:diorite
fill 1 208 33 2 208 33 minecraft:podzol
fill 3 201 34 3 207 37 minecraft:diorite
fill 3 208 34 3 208 37 minecraft:podzol
fill 1 201 38 2 207 38 minecraft:diorite
fill 1 208 38 2 208 38 minecraft:podzol
execute positioned 1 201 27 run function rlk:room/prop/fo_lamp
execute positioned 3 201 26 run function rlk:room/prop/fo_lamp
execute positioned 7 202 36 run function rlk:room/prop/fo_lamp
execute positioned 1 201 24 run function rlk:room/prop/fo_col_a
execute positioned 13 201 35 run function rlk:room/prop/p_grass
execute positioned 13 201 34 run function rlk:room/prop/fo_flower
execute positioned 17 201 22 run function rlk:room/prop/fo_flower
execute positioned 2 201 27 run function rlk:room/prop/p_grass
execute positioned 16 201 21 run function rlk:room/prop/p_grass
execute positioned 13 201 33 run function rlk:room/prop/p_grass
execute positioned 10 201 33 run function rlk:room/prop/fo_flower
execute positioned 12 201 21 run function rlk:room/prop/fo_flower
setblock 1 209 33 minecraft:birch_leaves[persistent=true] keep
setblock 1 209 34 minecraft:short_grass keep
setblock 1 209 35 minecraft:short_grass keep
setblock 1 209 36 minecraft:birch_leaves[persistent=true] keep
setblock 1 209 38 minecraft:short_grass keep
setblock 2 209 33 minecraft:birch_leaves[persistent=true] keep
setblock 2 209 34 minecraft:short_grass keep
setblock 2 209 36 minecraft:birch_leaves[persistent=true] keep
setblock 2 209 38 minecraft:short_grass keep
setblock 3 209 30 minecraft:birch_leaves[persistent=true] keep
setblock 3 209 35 minecraft:birch_leaves[persistent=true] keep
setblock 3 209 36 minecraft:short_grass keep
setblock 4 209 29 minecraft:short_grass keep
setblock 4 209 30 minecraft:birch_leaves[persistent=true] keep
