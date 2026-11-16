# 구역 건설 (normal3_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 40 19 200 59 minecraft:podzol
fill 0 201 40 19 210 59 minecraft:stone
fill 1 201 41 18 210 58 minecraft:air
fill 1 209 41 18 209 58 minecraft:light[level=15]
fill 10 200 47 13 200 48 minecraft:coarse_dirt
fill 16 200 43 17 200 45 minecraft:calcite
fill 0 207 40 0 209 43 minecraft:calcite
fill 0 210 43 0 210 46 minecraft:birch_leaves[persistent=true]
fill 0 204 50 0 205 50 minecraft:prismarine
fill 0 209 54 0 210 56 minecraft:oak_leaves[persistent=true]
fill 19 209 44 19 210 44 minecraft:birch_leaves[persistent=true]
fill 19 210 50 19 210 55 minecraft:diorite
fill 19 208 54 19 210 56 minecraft:calcite
fill 3 202 40 7 203 40 minecraft:prismarine
fill 5 209 40 7 210 40 minecraft:birch_leaves[persistent=true]
fill 6 201 40 11 201 40 minecraft:prismarine
fill 4 209 40 5 210 40 minecraft:oak_leaves[persistent=true]
fill 6 210 40 10 210 40 minecraft:birch_leaves[persistent=true]
fill 2 205 40 4 208 40 minecraft:diorite
fill 17 209 59 17 210 59 minecraft:oak_leaves[persistent=true]
fill 12 209 59 14 210 59 minecraft:calcite
fill 12 209 59 16 210 59 minecraft:birch_leaves[persistent=true]
fill 0 210 40 19 210 59 minecraft:polished_deepslate
fill 1 210 41 18 210 58 minecraft:air
fill 4 201 54 5 201 54 minecraft:podzol
fill 3 201 55 4 201 55 minecraft:podzol
fill 6 201 55 11 201 55 minecraft:podzol
fill 3 201 56 3 201 56 minecraft:podzol
fill 11 201 56 11 201 56 minecraft:podzol
fill 2 201 57 2 201 58 minecraft:podzol
fill 12 201 57 12 201 58 minecraft:podzol
fill 5 201 55 5 201 56 minecraft:dirt
fill 5 202 55 5 202 56 minecraft:podzol
fill 4 201 56 4 201 58 minecraft:dirt
fill 4 202 56 4 202 58 minecraft:podzol
fill 6 201 56 10 201 56 minecraft:dirt
fill 6 202 56 10 202 56 minecraft:podzol
fill 3 201 57 3 201 58 minecraft:dirt
fill 3 202 57 3 202 58 minecraft:podzol
fill 10 201 57 11 201 58 minecraft:dirt
fill 10 202 57 11 202 58 minecraft:podzol
fill 5 201 57 9 202 58 minecraft:dirt
fill 5 203 57 9 203 58 minecraft:podzol
fill 3 201 44 4 206 45 minecraft:diorite
fill 3 207 44 4 207 45 minecraft:podzol
fill 12 199 55 13 199 56 minecraft:clay
fill 12 200 55 13 200 56 minecraft:water
fill 14 199 56 18 199 58 minecraft:clay
fill 14 200 56 18 200 58 minecraft:water
fill 13 199 57 13 199 58 minecraft:clay
fill 13 200 57 13 200 58 minecraft:water
setblock 16 200 58 minecraft:seagrass
setblock 18 200 57 minecraft:seagrass
execute positioned 13 201 44 run function rlk:room/prop/fo_tree_c
execute positioned 3 201 48 run function rlk:room/prop/fo_white
execute positioned 18 201 48 run function rlk:room/prop/fo_flower
execute positioned 18 201 51 run function rlk:room/prop/p_grass
execute positioned 1 201 50 run function rlk:room/prop/fo_flower
execute positioned 13 201 51 run function rlk:room/prop/p_grass
execute positioned 1 201 46 run function rlk:room/prop/p_grass
execute positioned 6 201 50 run function rlk:room/prop/fo_white
execute positioned 14 201 43 run function rlk:room/prop/fo_flower
execute positioned 8 203 56 run function rlk:room/prop/fo_flower
setblock 3 208 45 minecraft:birch_leaves[persistent=true] keep
setblock 4 208 44 minecraft:short_grass keep
setblock 4 208 45 minecraft:birch_leaves[persistent=true] keep
