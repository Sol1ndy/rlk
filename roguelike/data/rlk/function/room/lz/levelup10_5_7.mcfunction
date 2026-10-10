# 구역 건설 (levelup10_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 0 59 200 19 minecraft:podzol
fill 40 201 0 59 213 19 minecraft:stone
fill 41 201 1 58 213 18 minecraft:air
fill 41 212 1 58 212 18 minecraft:light[level=15]
fill 57 203 9 58 203 10 minecraft:moss_block
fill 54 203 7 58 203 8 minecraft:coarse_dirt
fill 40 212 5 40 213 9 minecraft:birch_leaves[persistent=true]
fill 40 212 6 40 213 11 minecraft:moss_block
fill 40 213 9 40 213 13 minecraft:diorite
fill 40 213 2 40 213 4 minecraft:calcite
fill 59 213 3 59 213 8 minecraft:dark_prismarine
fill 59 207 14 59 208 19 minecraft:moss_block
fill 59 212 12 59 213 17 minecraft:calcite
fill 59 212 7 59 213 11 minecraft:birch_leaves[persistent=true]
fill 59 204 2 59 204 6 minecraft:calcite
fill 49 208 0 50 211 0 minecraft:prismarine
fill 45 212 0 49 213 0 minecraft:moss_block
fill 43 213 0 43 213 0 minecraft:birch_leaves[persistent=true]
fill 56 212 0 57 213 0 minecraft:birch_leaves[persistent=true]
fill 52 208 19 57 208 19 minecraft:dark_prismarine
fill 52 212 19 55 213 19 minecraft:oak_leaves[persistent=true]
fill 40 210 19 45 212 19 minecraft:diorite
fill 43 205 19 46 206 19 minecraft:diorite
fill 40 213 0 59 213 19 minecraft:polished_deepslate
fill 41 213 1 58 213 18 minecraft:air
fill 41 201 1 45 202 8 minecraft:dirt
fill 41 203 1 45 203 8 minecraft:podzol
fill 46 201 4 46 202 18 minecraft:dirt
fill 46 203 4 46 203 18 minecraft:podzol
fill 47 201 5 58 202 14 minecraft:dirt
fill 47 203 5 58 203 14 minecraft:podzol
fill 43 201 9 45 202 10 minecraft:dirt
fill 43 203 9 45 203 10 minecraft:podzol
fill 44 201 11 45 202 11 minecraft:dirt
fill 44 203 11 45 203 11 minecraft:podzol
fill 45 201 14 45 202 18 minecraft:dirt
fill 45 203 14 45 203 18 minecraft:podzol
fill 47 201 15 47 202 15 minecraft:dirt
fill 47 203 15 47 203 15 minecraft:podzol
fill 46 201 1 46 203 3 minecraft:dirt
fill 46 204 1 46 204 3 minecraft:podzol
fill 47 201 3 58 203 4 minecraft:dirt
fill 47 204 3 58 204 4 minecraft:podzol
fill 43 201 11 43 203 18 minecraft:dirt
fill 43 204 11 43 204 18 minecraft:podzol
fill 44 201 12 45 203 13 minecraft:dirt
fill 44 204 12 45 204 13 minecraft:podzol
fill 44 201 14 44 203 18 minecraft:dirt
fill 44 204 14 44 204 18 minecraft:podzol
fill 41 201 15 42 203 18 minecraft:dirt
fill 41 204 15 42 204 18 minecraft:podzol
fill 48 201 15 58 203 16 minecraft:dirt
fill 48 204 15 58 204 16 minecraft:podzol
fill 47 201 16 47 203 18 minecraft:dirt
fill 47 204 16 47 204 18 minecraft:podzol
fill 47 201 1 58 204 2 minecraft:dirt
fill 47 205 1 58 205 2 minecraft:podzol
fill 48 201 17 58 204 18 minecraft:dirt
fill 48 205 17 58 205 18 minecraft:podzol
fill 41 201 9 42 210 9 minecraft:calcite
fill 41 211 9 42 211 9 minecraft:podzol
fill 41 201 10 41 210 14 minecraft:calcite
fill 41 211 10 41 211 14 minecraft:podzol
fill 42 201 14 42 210 14 minecraft:calcite
fill 42 211 14 42 211 14 minecraft:podzol
fill 42 201 10 42 210 13 minecraft:diorite
fill 42 211 10 42 211 13 minecraft:podzol
fill 44 202 6 45 202 8 minecraft:clay
fill 44 203 6 45 203 8 minecraft:water
fill 55 202 6 58 202 13 minecraft:clay
fill 55 203 6 58 203 13 minecraft:water
fill 43 203 5 43 203 7 minecraft:sand
fill 44 203 9 45 203 9 minecraft:sand
setblock 55 203 7 minecraft:seagrass
setblock 56 203 6 minecraft:seagrass
setblock 56 203 12 minecraft:seagrass
setblock 57 203 11 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 58 203 7 minecraft:seagrass
setblock 58 203 11 minecraft:seagrass
execute positioned 47 204 5 run function rlk:room/prop/fo_col_a
execute positioned 45 204 18 run function rlk:room/prop/fo_rock_s
execute positioned 45 204 11 run function rlk:room/prop/fo_col_a
execute positioned 48 205 16 run function rlk:room/prop/fo_flower
execute positioned 50 205 15 run function rlk:room/prop/fo_flower
execute positioned 46 204 10 run function rlk:room/prop/fo_flower
execute positioned 43 204 10 run function rlk:room/prop/fo_flower
execute positioned 44 204 3 run function rlk:room/prop/p_grass
execute positioned 46 204 12 run function rlk:room/prop/fo_flower
execute positioned 58 204 5 run function rlk:room/prop/fo_white
setblock 41 212 10 minecraft:short_grass keep
setblock 41 212 14 minecraft:short_grass keep
setblock 42 212 10 minecraft:short_grass keep
setblock 42 212 11 minecraft:short_grass keep
setblock 42 212 12 minecraft:short_grass keep
setblock 42 212 13 minecraft:birch_leaves[persistent=true] keep
setblock 42 212 14 minecraft:birch_leaves[persistent=true] keep
