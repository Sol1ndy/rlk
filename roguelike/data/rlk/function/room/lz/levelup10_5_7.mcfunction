# 구역 건설 (levelup10_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 0 59 200 19 minecraft:podzol
fill 40 201 0 59 210 19 minecraft:stone
fill 41 201 1 58 210 18 minecraft:air
fill 41 209 1 58 209 18 minecraft:light[level=15]
fill 57 200 9 58 200 10 minecraft:moss_block
fill 54 200 7 58 200 8 minecraft:coarse_dirt
fill 40 209 5 40 210 9 minecraft:birch_leaves[persistent=true]
fill 40 209 6 40 210 11 minecraft:moss_block
fill 40 210 9 40 210 13 minecraft:diorite
fill 40 210 2 40 210 4 minecraft:calcite
fill 59 210 3 59 210 8 minecraft:dark_prismarine
fill 59 204 14 59 205 19 minecraft:moss_block
fill 59 209 12 59 210 17 minecraft:calcite
fill 59 209 7 59 210 11 minecraft:birch_leaves[persistent=true]
fill 59 201 2 59 201 6 minecraft:calcite
fill 49 205 0 50 208 0 minecraft:prismarine
fill 45 209 0 49 210 0 minecraft:moss_block
fill 43 210 0 43 210 0 minecraft:birch_leaves[persistent=true]
fill 56 209 0 57 210 0 minecraft:birch_leaves[persistent=true]
fill 52 205 19 57 205 19 minecraft:dark_prismarine
fill 52 209 19 55 210 19 minecraft:oak_leaves[persistent=true]
fill 40 207 19 45 209 19 minecraft:diorite
fill 43 202 19 46 203 19 minecraft:diorite
fill 40 210 0 59 210 19 minecraft:polished_deepslate
fill 41 210 1 58 210 18 minecraft:air
fill 43 201 11 43 201 18 minecraft:podzol
fill 44 201 12 45 201 13 minecraft:podzol
fill 44 201 14 44 201 18 minecraft:podzol
fill 41 201 15 42 201 18 minecraft:podzol
fill 41 201 9 42 207 9 minecraft:calcite
fill 41 208 9 42 208 9 minecraft:podzol
fill 41 201 10 41 207 14 minecraft:calcite
fill 41 208 10 41 208 14 minecraft:podzol
fill 42 201 14 42 207 14 minecraft:calcite
fill 42 208 14 42 208 14 minecraft:podzol
fill 42 201 10 42 207 13 minecraft:diorite
fill 42 208 10 42 208 13 minecraft:podzol
fill 44 199 6 45 199 8 minecraft:clay
fill 44 200 6 45 200 8 minecraft:water
fill 55 199 6 58 199 13 minecraft:clay
fill 55 200 6 58 200 13 minecraft:water
fill 43 200 5 43 200 7 minecraft:sand
fill 44 200 9 45 200 9 minecraft:sand
setblock 55 200 7 minecraft:seagrass
setblock 56 200 6 minecraft:seagrass
setblock 56 200 12 minecraft:seagrass
setblock 57 200 11 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 58 200 7 minecraft:seagrass
setblock 58 200 11 minecraft:seagrass
execute positioned 47 201 5 run function rlk:room/prop/fo_col_a
execute positioned 45 201 18 run function rlk:room/prop/fo_rock_s
execute positioned 45 201 11 run function rlk:room/prop/fo_col_a
execute positioned 48 201 16 run function rlk:room/prop/fo_flower
execute positioned 50 201 15 run function rlk:room/prop/fo_flower
execute positioned 46 201 10 run function rlk:room/prop/fo_flower
execute positioned 43 201 10 run function rlk:room/prop/fo_flower
execute positioned 44 201 3 run function rlk:room/prop/p_grass
execute positioned 46 201 12 run function rlk:room/prop/fo_flower
execute positioned 58 201 5 run function rlk:room/prop/fo_white
setblock 41 209 10 minecraft:short_grass keep
setblock 41 209 14 minecraft:short_grass keep
setblock 42 209 10 minecraft:short_grass keep
setblock 42 209 11 minecraft:short_grass keep
setblock 42 209 12 minecraft:short_grass keep
setblock 42 209 13 minecraft:birch_leaves[persistent=true] keep
setblock 42 209 14 minecraft:birch_leaves[persistent=true] keep
