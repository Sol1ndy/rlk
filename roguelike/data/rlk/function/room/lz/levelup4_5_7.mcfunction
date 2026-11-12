# 구역 건설 (levelup4_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 40 19 200 59 minecraft:podzol
fill 0 201 40 19 210 59 minecraft:stone
fill 1 201 41 18 210 58 minecraft:air
fill 1 209 41 18 209 58 minecraft:light[level=15]
fill 9 200 53 10 200 55 minecraft:calcite
fill 1 200 45 4 200 46 minecraft:gravel
fill 2 200 42 5 200 43 minecraft:calcite
fill 0 209 54 0 210 58 minecraft:prismarine
fill 0 210 50 0 210 55 minecraft:birch_leaves[persistent=true]
fill 0 209 46 0 210 47 minecraft:oak_leaves[persistent=true]
fill 0 207 49 0 210 51 minecraft:calcite
fill 19 209 54 19 210 56 minecraft:oak_leaves[persistent=true]
fill 19 210 42 19 210 47 minecraft:calcite
fill 19 210 53 19 210 56 minecraft:diorite
fill 3 210 40 3 210 40 minecraft:birch_leaves[persistent=true]
fill 10 209 40 14 210 40 minecraft:oak_leaves[persistent=true]
fill 6 206 40 11 208 40 minecraft:prismarine
fill 10 201 59 13 203 59 minecraft:moss_block
fill 12 210 59 12 210 59 minecraft:birch_leaves[persistent=true]
fill 11 202 59 11 203 59 minecraft:moss_block
fill 11 202 59 11 202 59 minecraft:moss_block
fill 0 210 40 19 210 59 minecraft:polished_deepslate
fill 1 210 41 18 210 58 minecraft:air
fill 15 201 54 17 201 54 minecraft:podzol
fill 12 201 55 14 201 55 minecraft:podzol
fill 16 201 55 18 201 55 minecraft:podzol
fill 11 201 56 12 201 57 minecraft:podzol
fill 18 201 56 18 201 57 minecraft:podzol
fill 11 201 58 11 201 58 minecraft:podzol
fill 15 201 55 15 201 58 minecraft:dirt
fill 15 202 55 15 202 58 minecraft:podzol
fill 13 201 56 14 201 58 minecraft:dirt
fill 13 202 56 14 202 58 minecraft:podzol
fill 16 201 56 17 201 58 minecraft:dirt
fill 16 202 56 17 202 58 minecraft:podzol
fill 12 201 58 12 201 58 minecraft:dirt
fill 12 202 58 12 202 58 minecraft:podzol
fill 18 201 58 18 201 58 minecraft:dirt
fill 18 202 58 18 202 58 minecraft:podzol
fill 3 201 49 4 206 49 minecraft:calcite
fill 3 207 49 4 207 49 minecraft:podzol
fill 3 201 50 4 206 50 minecraft:diorite
fill 3 207 50 4 207 50 minecraft:podzol
fill 4 199 53 5 199 55 minecraft:clay
fill 4 200 53 5 200 55 minecraft:water
fill 6 199 55 10 199 58 minecraft:clay
fill 6 200 55 10 200 58 minecraft:water
fill 5 199 56 5 199 58 minecraft:clay
fill 5 200 56 5 200 58 minecraft:water
fill 3 200 52 3 200 56 minecraft:sand
fill 11 200 55 11 200 55 minecraft:sand
fill 4 200 56 4 200 58 minecraft:sand
setblock 4 200 53 minecraft:seagrass
setblock 5 200 55 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 6 200 56 minecraft:seagrass
setblock 7 200 56 minecraft:seagrass
setblock 8 200 57 minecraft:seagrass
execute positioned 16 201 43 run function rlk:room/prop/fo_pipe_z
execute positioned 15 203 58 run function rlk:room/prop/fo_crates
execute positioned 12 201 45 run function rlk:room/prop/fo_white
execute positioned 12 202 56 run function rlk:room/prop/p_grass
execute positioned 14 201 41 run function rlk:room/prop/p_grass
execute positioned 3 201 51 run function rlk:room/prop/fo_white
execute positioned 2 201 55 run function rlk:room/prop/fo_flower
execute positioned 11 201 45 run function rlk:room/prop/p_grass
execute positioned 7 201 44 run function rlk:room/prop/fo_flower
execute positioned 11 201 43 run function rlk:room/prop/p_grass
execute positioned 10 201 50 run function rlk:room/prop/p_grass
setblock 3 208 49 minecraft:short_grass keep
setblock 4 208 50 minecraft:birch_leaves[persistent=true] keep
