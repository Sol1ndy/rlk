# 구역 건설 (boss6_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 5 200 2 8 200 3 minecraft:moss_block
fill 2 200 15 6 200 16 minecraft:moss_block
fill 3 200 1 7 200 3 minecraft:calcite
fill 0 210 5 0 210 10 minecraft:oak_leaves[persistent=true]
fill 0 209 2 0 210 4 minecraft:birch_leaves[persistent=true]
fill 0 208 3 0 208 7 minecraft:calcite
fill 0 210 6 0 210 11 minecraft:oak_leaves[persistent=true]
fill 19 204 2 19 204 6 minecraft:dark_prismarine
fill 19 201 12 19 202 16 minecraft:prismarine
fill 19 210 13 19 210 16 minecraft:moss_block
fill 19 210 5 19 210 9 minecraft:oak_leaves[persistent=true]
fill 19 205 8 19 206 11 minecraft:moss_block
fill 19 209 1 19 210 6 minecraft:birch_leaves[persistent=true]
fill 0 209 0 5 210 0 minecraft:birch_leaves[persistent=true]
fill 9 204 0 12 205 0 minecraft:calcite
fill 0 203 0 2 204 0 minecraft:calcite
fill 0 207 19 5 207 19 minecraft:calcite
fill 10 209 19 14 209 19 minecraft:moss_block
fill 10 210 19 14 210 19 minecraft:birch_leaves[persistent=true]
fill 16 210 19 19 210 19 minecraft:birch_leaves[persistent=true]
fill 0 204 19 5 207 19 minecraft:dark_prismarine
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 16 201 1 18 201 10 minecraft:podzol
fill 15 201 6 15 201 12 minecraft:podzol
fill 16 201 11 16 201 13 minecraft:podzol
fill 17 201 11 17 206 11 minecraft:calcite
fill 17 207 11 17 207 11 minecraft:podzol
fill 18 201 11 18 206 13 minecraft:diorite
fill 18 207 11 18 207 13 minecraft:podzol
fill 17 201 12 17 206 13 minecraft:diorite
fill 17 207 12 17 207 13 minecraft:podzol
fill 3 201 13 4 207 14 minecraft:calcite
fill 3 208 13 4 208 14 minecraft:podzol
execute positioned 3 201 9 run function rlk:room/prop/fo_rock
execute positioned 11 201 15 run function rlk:room/prop/fo_lamp2
execute positioned 13 201 14 run function rlk:room/prop/p_grass
execute positioned 14 201 8 run function rlk:room/prop/fo_flower
execute positioned 2 201 15 run function rlk:room/prop/fo_flower
execute positioned 11 201 5 run function rlk:room/prop/p_grass
execute positioned 8 201 5 run function rlk:room/prop/p_grass
execute positioned 10 201 12 run function rlk:room/prop/fo_white
execute positioned 6 201 17 run function rlk:room/prop/p_grass
execute positioned 18 202 2 run function rlk:room/prop/fo_white
execute positioned 10 201 16 run function rlk:room/prop/fo_flower
setblock 3 209 14 minecraft:birch_leaves[persistent=true] keep
setblock 4 209 13 minecraft:birch_leaves[persistent=true] keep
setblock 17 208 11 minecraft:birch_leaves[persistent=true] keep
setblock 18 208 11 minecraft:birch_leaves[persistent=true] keep
setblock 18 208 12 minecraft:short_grass keep
setblock 18 208 13 minecraft:short_grass keep
