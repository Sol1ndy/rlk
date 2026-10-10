# 구역 건설 (first0_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 10 200 16 14 200 17 minecraft:calcite
fill 11 200 16 15 200 18 minecraft:calcite
fill 11 200 6 12 200 7 minecraft:coarse_dirt
fill 0 209 0 0 210 5 minecraft:oak_leaves[persistent=true]
fill 0 202 12 0 204 16 minecraft:calcite
fill 0 209 12 0 210 13 minecraft:birch_leaves[persistent=true]
fill 0 204 9 0 204 14 minecraft:prismarine
fill 0 207 2 0 207 5 minecraft:prismarine
fill 0 203 9 0 205 14 minecraft:diorite
fill 19 208 18 19 209 18 minecraft:dark_prismarine
fill 19 210 0 19 210 1 minecraft:oak_leaves[persistent=true]
fill 19 204 14 19 204 18 minecraft:moss_block
fill 19 204 1 19 207 1 minecraft:diorite
fill 19 208 1 19 208 1 minecraft:diorite
fill 3 203 0 8 206 0 minecraft:calcite
fill 14 203 0 18 204 0 minecraft:calcite
fill 8 203 0 8 206 0 minecraft:moss_block
fill 14 209 0 15 210 0 minecraft:birch_leaves[persistent=true]
fill 8 208 0 13 210 0 minecraft:calcite
fill 3 206 0 7 209 0 minecraft:moss_block
fill 13 201 19 16 203 19 minecraft:calcite
fill 13 210 19 18 210 19 minecraft:moss_block
fill 7 209 19 7 210 19 minecraft:birch_leaves[persistent=true]
fill 15 205 19 15 207 19 minecraft:prismarine
fill 13 202 19 13 204 19 minecraft:moss_block
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 1 201 16 3 201 16 minecraft:podzol
fill 3 201 17 3 201 18 minecraft:podzol
fill 1 201 17 2 201 18 minecraft:dirt
fill 1 202 17 2 202 18 minecraft:podzol
fill 16 201 1 18 206 1 minecraft:calcite
fill 16 207 1 18 207 1 minecraft:podzol
fill 16 201 2 17 206 3 minecraft:calcite
fill 16 207 2 17 207 3 minecraft:podzol
fill 18 201 2 18 206 3 minecraft:diorite
fill 18 207 2 18 207 3 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:calcite
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:calcite
fill 12 208 4 12 208 4 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:diorite
fill 12 208 3 12 208 3 minecraft:podzol
execute positioned 1 203 18 run function rlk:room/prop/fo_lamp
execute positioned 15 201 7 run function rlk:room/prop/fo_lamp
execute positioned 15 201 11 run function rlk:room/prop/fo_tree_b
execute positioned 9 201 5 run function rlk:room/prop/p_grass
execute positioned 5 201 13 run function rlk:room/prop/p_grass
execute positioned 14 201 18 run function rlk:room/prop/fo_flower
execute positioned 15 201 9 run function rlk:room/prop/fo_flower
execute positioned 1 201 10 run function rlk:room/prop/fo_flower
execute positioned 5 201 15 run function rlk:room/prop/fo_flower
execute positioned 6 201 8 run function rlk:room/prop/fo_flower
execute positioned 11 201 17 run function rlk:room/prop/p_grass
setblock 11 209 4 minecraft:birch_leaves[persistent=true] keep
setblock 12 209 4 minecraft:short_grass keep
setblock 16 208 1 minecraft:birch_leaves[persistent=true] keep
setblock 16 208 2 minecraft:birch_leaves[persistent=true] keep
setblock 16 208 3 minecraft:birch_leaves[persistent=true] keep
setblock 17 208 1 minecraft:birch_leaves[persistent=true] keep
setblock 17 208 3 minecraft:birch_leaves[persistent=true] keep
setblock 18 208 1 minecraft:short_grass keep
setblock 18 208 2 minecraft:birch_leaves[persistent=true] keep
setblock 18 208 3 minecraft:short_grass keep
