# 구역 건설 (first5_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:podzol
fill 20 201 0 39 210 19 minecraft:stone
fill 21 201 1 38 210 18 minecraft:air
fill 21 209 1 38 209 18 minecraft:light[level=15]
fill 23 200 7 24 200 8 minecraft:calcite
fill 26 200 11 27 200 13 minecraft:calcite
fill 27 200 12 29 200 14 minecraft:calcite
fill 20 210 1 20 210 1 minecraft:oak_leaves[persistent=true]
fill 20 204 6 20 205 11 minecraft:prismarine
fill 20 210 13 20 210 18 minecraft:birch_leaves[persistent=true]
fill 20 209 10 20 210 15 minecraft:birch_leaves[persistent=true]
fill 20 210 12 20 210 12 minecraft:oak_leaves[persistent=true]
fill 39 209 9 39 210 9 minecraft:oak_leaves[persistent=true]
fill 39 206 5 39 206 6 minecraft:calcite
fill 39 209 14 39 210 19 minecraft:calcite
fill 39 210 17 39 210 19 minecraft:calcite
fill 39 206 16 39 208 18 minecraft:moss_block
fill 28 209 0 28 210 0 minecraft:moss_block
fill 31 206 0 32 206 0 minecraft:diorite
fill 30 210 0 32 210 0 minecraft:diorite
fill 24 209 0 26 209 0 minecraft:diorite
fill 28 210 19 31 210 19 minecraft:birch_leaves[persistent=true]
fill 31 207 19 34 210 19 minecraft:calcite
fill 24 202 19 27 203 19 minecraft:diorite
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 38 210 18 minecraft:air
fill 25 201 1 34 201 1 minecraft:podzol
fill 26 201 2 34 201 2 minecraft:podzol
fill 21 201 3 32 201 3 minecraft:podzol
fill 26 201 4 32 201 5 minecraft:podzol
fill 35 201 4 37 201 4 minecraft:podzol
fill 33 201 5 36 201 5 minecraft:podzol
fill 35 201 6 35 201 6 minecraft:podzol
fill 21 201 1 24 201 2 minecraft:dirt
fill 21 202 1 24 202 2 minecraft:podzol
fill 25 201 2 25 201 2 minecraft:dirt
fill 25 202 2 25 202 2 minecraft:podzol
fill 35 201 1 38 207 3 minecraft:calcite
fill 35 208 1 38 208 3 minecraft:podzol
fill 33 201 3 34 207 3 minecraft:calcite
fill 33 208 3 34 208 3 minecraft:podzol
fill 33 201 4 34 207 4 minecraft:diorite
fill 33 208 4 34 208 4 minecraft:podzol
fill 35 199 8 36 199 12 minecraft:clay
fill 35 200 8 36 200 12 minecraft:water
fill 36 200 7 37 200 7 minecraft:sand
fill 37 200 8 37 200 8 minecraft:sand
fill 37 200 10 37 200 13 minecraft:sand
setblock 36 200 9 minecraft:seagrass
execute positioned 28 202 1 run function rlk:room/prop/fo_col_a
execute positioned 26 202 5 run function rlk:room/prop/fo_lamp
execute positioned 21 202 3 run function rlk:room/prop/fo_rock_s
execute positioned 23 201 12 run function rlk:room/prop/fo_flower
execute positioned 25 201 6 run function rlk:room/prop/p_grass
execute positioned 38 201 12 run function rlk:room/prop/p_grass
execute positioned 24 201 13 run function rlk:room/prop/p_grass
execute positioned 35 202 4 run function rlk:room/prop/p_grass
execute positioned 22 201 5 run function rlk:room/prop/fo_flower
execute positioned 28 201 13 run function rlk:room/prop/fo_white
execute positioned 33 201 15 run function rlk:room/prop/p_grass
execute positioned 21 201 16 run function rlk:room/prop/p_grass
setblock 33 209 4 minecraft:birch_leaves[persistent=true] keep
setblock 34 209 3 minecraft:birch_leaves[persistent=true] keep
setblock 35 209 1 minecraft:short_grass keep
setblock 35 209 2 minecraft:birch_leaves[persistent=true] keep
setblock 35 209 3 minecraft:birch_leaves[persistent=true] keep
setblock 36 209 1 minecraft:birch_leaves[persistent=true] keep
setblock 36 209 3 minecraft:birch_leaves[persistent=true] keep
setblock 37 209 1 minecraft:short_grass keep
setblock 37 209 2 minecraft:birch_leaves[persistent=true] keep
setblock 38 209 2 minecraft:birch_leaves[persistent=true] keep
setblock 38 209 3 minecraft:birch_leaves[persistent=true] keep
