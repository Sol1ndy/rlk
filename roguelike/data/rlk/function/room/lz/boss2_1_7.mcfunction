# 구역 건설 (boss2_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 12 200 6 13 200 7 minecraft:moss_block
fill 12 200 10 13 200 11 minecraft:moss_block
fill 0 207 6 0 207 7 minecraft:moss_block
fill 0 210 3 0 210 8 minecraft:birch_leaves[persistent=true]
fill 0 209 4 0 210 7 minecraft:oak_leaves[persistent=true]
fill 19 208 7 19 209 10 minecraft:prismarine
fill 19 204 5 19 207 7 minecraft:calcite
fill 19 210 1 19 210 5 minecraft:birch_leaves[persistent=true]
fill 19 210 14 19 210 17 minecraft:birch_leaves[persistent=true]
fill 10 201 0 12 203 0 minecraft:prismarine
fill 0 205 0 2 205 0 minecraft:moss_block
fill 0 209 0 0 209 0 minecraft:calcite
fill 5 206 0 10 206 0 minecraft:calcite
fill 12 205 19 14 208 19 minecraft:diorite
fill 8 203 19 12 204 19 minecraft:moss_block
fill 16 207 19 16 210 19 minecraft:calcite
fill 2 207 19 7 208 19 minecraft:moss_block
fill 13 210 19 16 210 19 minecraft:birch_leaves[persistent=true]
fill 15 208 19 19 209 19 minecraft:prismarine
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 1 201 5 2 201 15 minecraft:podzol
fill 3 201 6 4 201 14 minecraft:podzol
fill 5 201 7 5 201 13 minecraft:podzol
fill 3 201 4 4 207 5 minecraft:calcite
fill 3 208 4 4 208 5 minecraft:podzol
fill 7 199 1 15 199 3 minecraft:clay
fill 7 200 1 15 200 3 minecraft:water
fill 7 199 4 13 199 5 minecraft:clay
fill 7 200 4 13 200 5 minecraft:water
fill 6 200 1 6 200 5 minecraft:sand
fill 16 200 1 16 200 3 minecraft:sand
setblock 7 200 2 minecraft:seagrass
setblock 8 200 1 minecraft:seagrass
setblock 12 200 1 minecraft:seagrass
execute positioned 9 201 13 run function rlk:room/prop/fo_flower
execute positioned 8 201 17 run function rlk:room/prop/fo_flower
execute positioned 11 201 14 run function rlk:room/prop/p_grass
execute positioned 2 202 10 run function rlk:room/prop/p_grass
execute positioned 1 202 6 run function rlk:room/prop/fo_flower
execute positioned 7 201 18 run function rlk:room/prop/fo_flower
execute positioned 17 201 4 run function rlk:room/prop/fo_flower
execute positioned 1 202 8 run function rlk:room/prop/fo_white
execute positioned 17 201 4 run function rlk:room/prop/p_grass
execute positioned 17 201 1 run function rlk:room/prop/fo_white
setblock 3 209 4 minecraft:birch_leaves[persistent=true] keep
setblock 4 209 5 minecraft:short_grass keep
