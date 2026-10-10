# 구역 건설 (normal0_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 10 200 4 13 200 7 minecraft:calcite
fill 0 209 10 0 209 15 minecraft:calcite
fill 0 210 8 0 210 11 minecraft:birch_leaves[persistent=true]
fill 0 204 7 0 205 7 minecraft:diorite
fill 0 208 2 0 210 3 minecraft:diorite
fill 0 209 13 0 210 17 minecraft:birch_leaves[persistent=true]
fill 19 209 15 19 209 15 minecraft:dark_prismarine
fill 19 209 17 19 210 18 minecraft:birch_leaves[persistent=true]
fill 19 204 15 19 206 15 minecraft:calcite
fill 1 203 0 4 205 0 minecraft:prismarine
fill 7 210 0 8 210 0 minecraft:birch_leaves[persistent=true]
fill 7 209 0 10 210 0 minecraft:oak_leaves[persistent=true]
fill 8 210 0 9 210 0 minecraft:moss_block
fill 15 208 0 19 210 0 minecraft:calcite
fill 2 209 0 6 210 0 minecraft:birch_leaves[persistent=true]
fill 3 210 19 8 210 19 minecraft:prismarine
fill 14 201 19 18 201 19 minecraft:dark_prismarine
fill 6 208 19 8 209 19 minecraft:prismarine
fill 9 210 19 13 210 19 minecraft:calcite
fill 13 204 19 16 207 19 minecraft:calcite
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 16 201 1 16 201 6 minecraft:podzol
fill 17 201 5 17 201 6 minecraft:podzol
fill 18 201 6 18 201 6 minecraft:podzol
fill 17 201 1 18 201 4 minecraft:dirt
fill 17 202 1 18 202 4 minecraft:podzol
fill 18 201 5 18 201 5 minecraft:dirt
fill 18 202 5 18 202 5 minecraft:podzol
fill 15 199 8 16 199 18 minecraft:clay
fill 15 200 8 16 200 18 minecraft:water
fill 4 199 10 5 199 14 minecraft:clay
fill 4 200 10 5 200 14 minecraft:water
fill 3 199 11 3 199 13 minecraft:clay
fill 3 200 11 3 200 13 minecraft:water
fill 2 200 10 2 200 10 minecraft:sand
fill 2 200 12 2 200 12 minecraft:sand
fill 2 200 14 2 200 14 minecraft:sand
fill 4 200 15 6 200 15 minecraft:sand
setblock 3 200 12 minecraft:seagrass
setblock 15 200 13 minecraft:seagrass
setblock 16 200 8 minecraft:seagrass
setblock 16 200 15 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned 5 201 8 run function rlk:room/prop/p_grass
execute positioned 5 201 17 run function rlk:room/prop/p_grass
execute positioned 10 201 13 run function rlk:room/prop/p_grass
execute positioned 17 201 9 run function rlk:room/prop/fo_white
execute positioned 9 201 9 run function rlk:room/prop/fo_white
execute positioned 12 201 1 run function rlk:room/prop/fo_white
execute positioned 5 201 4 run function rlk:room/prop/fo_white
execute positioned 1 201 18 run function rlk:room/prop/fo_flower
execute positioned 8 201 17 run function rlk:room/prop/p_grass
