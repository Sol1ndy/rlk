# 구역 건설 (levelup10_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -20 59 200 -1 minecraft:podzol
fill 40 201 -20 59 210 -1 minecraft:stone
fill 41 201 -19 58 210 -2 minecraft:air
fill 41 209 -19 58 209 -2 minecraft:light[level=15]
fill 46 200 -18 47 200 -17 minecraft:calcite
fill 55 200 -17 56 200 -15 minecraft:coarse_dirt
fill 40 206 -9 40 207 -5 minecraft:calcite
fill 40 210 -12 40 210 -9 minecraft:oak_leaves[persistent=true]
fill 40 203 -10 40 204 -8 minecraft:diorite
fill 40 210 -12 40 210 -10 minecraft:birch_leaves[persistent=true]
fill 59 204 -15 59 206 -14 minecraft:diorite
fill 59 204 -17 59 204 -16 minecraft:moss_block
fill 59 205 -7 59 205 -4 minecraft:calcite
fill 59 210 -7 59 210 -2 minecraft:birch_leaves[persistent=true]
fill 54 206 -20 55 209 -20 minecraft:calcite
fill 47 206 -20 51 206 -20 minecraft:moss_block
fill 51 209 -20 53 210 -20 minecraft:moss_block
fill 53 210 -1 55 210 -1 minecraft:birch_leaves[persistent=true]
fill 55 210 -1 55 210 -1 minecraft:birch_leaves[persistent=true]
fill 40 210 -1 41 210 -1 minecraft:prismarine
fill 44 209 -1 47 210 -1 minecraft:birch_leaves[persistent=true]
fill 55 207 -1 59 207 -1 minecraft:calcite
fill 40 210 -20 59 210 -1 minecraft:polished_deepslate
fill 41 210 -19 58 210 -2 minecraft:air
fill 43 201 -15 43 201 -14 minecraft:podzol
fill 42 201 -14 42 201 -10 minecraft:podzol
fill 44 201 -14 45 201 -14 minecraft:podzol
fill 45 201 -13 45 201 -9 minecraft:podzol
fill 43 201 -11 44 201 -9 minecraft:podzol
fill 43 201 -13 44 206 -13 minecraft:calcite
fill 43 207 -13 44 207 -13 minecraft:podzol
fill 43 201 -12 44 206 -12 minecraft:diorite
fill 43 207 -12 44 207 -12 minecraft:podzol
fill 56 199 -19 58 199 -11 minecraft:clay
fill 56 200 -19 58 200 -11 minecraft:water
fill 55 199 -14 55 199 -7 minecraft:clay
fill 55 200 -14 55 200 -7 minecraft:water
fill 56 199 -10 56 199 -7 minecraft:clay
fill 56 200 -10 56 200 -7 minecraft:water
fill 57 200 -10 58 200 -10 minecraft:sand
setblock 55 200 -10 minecraft:seagrass
setblock 55 200 -7 minecraft:seagrass
setblock 56 200 -16 minecraft:seagrass
setblock 56 200 -12 minecraft:seagrass
setblock 56 200 -7 minecraft:seagrass
setblock 57 200 -12 minecraft:seagrass
execute positioned 42 201 -7 run function rlk:room/prop/fo_bench
execute positioned 41 201 -14 run function rlk:room/prop/fo_col_b
execute positioned 42 201 -3 run function rlk:room/prop/p_grass
execute positioned 50 201 -5 run function rlk:room/prop/fo_flower
execute positioned 50 201 -18 run function rlk:room/prop/fo_flower
execute positioned 50 201 -2 run function rlk:room/prop/p_grass
execute positioned 41 201 -12 run function rlk:room/prop/fo_white
execute positioned 53 201 -2 run function rlk:room/prop/fo_flower
execute positioned 53 201 -8 run function rlk:room/prop/fo_white
setblock 43 208 -13 minecraft:short_grass keep
setblock 44 208 -12 minecraft:short_grass keep
