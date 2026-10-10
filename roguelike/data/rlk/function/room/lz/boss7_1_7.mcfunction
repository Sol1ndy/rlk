# 구역 건설 (boss7_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 6 200 7 7 200 10 minecraft:coarse_dirt
fill 12 200 11 13 200 14 minecraft:calcite
fill 5 200 8 6 200 9 minecraft:calcite
fill 0 209 15 0 210 17 minecraft:oak_leaves[persistent=true]
fill 0 209 2 0 210 7 minecraft:calcite
fill 0 203 6 0 204 7 minecraft:calcite
fill 0 210 2 0 210 6 minecraft:oak_leaves[persistent=true]
fill 19 205 7 19 205 10 minecraft:moss_block
fill 19 210 17 19 210 17 minecraft:oak_leaves[persistent=true]
fill 19 210 8 19 210 13 minecraft:oak_leaves[persistent=true]
fill 19 210 10 19 210 12 minecraft:prismarine
fill 19 210 8 19 210 9 minecraft:oak_leaves[persistent=true]
fill 11 209 0 13 209 0 minecraft:moss_block
fill 0 210 0 3 210 0 minecraft:diorite
fill 13 203 0 14 205 0 minecraft:calcite
fill 12 209 0 16 210 0 minecraft:birch_leaves[persistent=true]
fill 4 210 19 8 210 19 minecraft:birch_leaves[persistent=true]
fill 7 203 19 11 203 19 minecraft:diorite
fill 2 209 19 4 210 19 minecraft:oak_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 5 201 11 5 201 14 minecraft:podzol
fill 4 201 12 4 201 13 minecraft:podzol
fill 3 201 13 3 201 17 minecraft:podzol
fill 6 201 15 13 201 15 minecraft:podzol
fill 14 201 16 15 201 17 minecraft:podzol
fill 4 201 17 4 201 18 minecraft:podzol
fill 14 201 18 14 201 18 minecraft:podzol
fill 4 201 14 4 201 16 minecraft:dirt
fill 4 202 14 4 202 16 minecraft:podzol
fill 5 201 15 5 201 18 minecraft:dirt
fill 5 202 15 5 202 18 minecraft:podzol
fill 6 201 16 13 201 16 minecraft:dirt
fill 6 202 16 13 202 16 minecraft:podzol
fill 6 201 17 6 201 18 minecraft:dirt
fill 6 202 17 6 202 18 minecraft:podzol
fill 12 201 17 13 201 18 minecraft:dirt
fill 12 202 17 13 202 18 minecraft:podzol
fill 7 201 18 7 201 18 minecraft:dirt
fill 7 202 18 7 202 18 minecraft:podzol
fill 11 201 18 11 201 18 minecraft:dirt
fill 11 202 18 11 202 18 minecraft:podzol
fill 7 201 17 11 202 17 minecraft:dirt
fill 7 203 17 11 203 17 minecraft:podzol
fill 8 201 18 10 202 18 minecraft:dirt
fill 8 203 18 10 203 18 minecraft:podzol
fill 1 201 1 2 206 1 minecraft:calcite
fill 1 207 1 2 207 1 minecraft:podzol
fill 1 201 2 2 206 3 minecraft:diorite
fill 1 207 2 2 207 3 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:calcite
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:calcite
fill 12 208 4 12 208 4 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:diorite
fill 12 208 3 12 208 3 minecraft:podzol
execute positioned 6 201 4 run function rlk:room/prop/fo_tree_c
execute positioned 18 201 16 run function rlk:room/prop/fo_lamp
execute positioned 12 201 9 run function rlk:room/prop/fo_white
execute positioned 11 201 6 run function rlk:room/prop/p_grass
execute positioned 11 203 16 run function rlk:room/prop/fo_flower
execute positioned 11 201 7 run function rlk:room/prop/p_grass
execute positioned 7 201 8 run function rlk:room/prop/p_grass
execute positioned 8 201 4 run function rlk:room/prop/p_grass
execute positioned 1 201 11 run function rlk:room/prop/fo_flower
execute positioned 4 201 5 run function rlk:room/prop/p_grass
setblock 1 208 1 minecraft:short_grass keep
setblock 1 208 2 minecraft:short_grass keep
setblock 1 208 3 minecraft:birch_leaves[persistent=true] keep
setblock 2 208 2 minecraft:short_grass keep
setblock 2 208 3 minecraft:birch_leaves[persistent=true] keep
setblock 11 209 3 minecraft:short_grass keep
setblock 12 209 4 minecraft:birch_leaves[persistent=true] keep
