# 구역 건설 (levelup10_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -20 59 200 -1 minecraft:podzol
fill 40 201 -20 59 215 -1 minecraft:stone
fill 41 201 -19 58 215 -2 minecraft:air
fill 41 214 -19 58 214 -2 minecraft:light[level=15]
fill 46 205 -18 47 205 -17 minecraft:calcite
fill 55 205 -17 56 205 -15 minecraft:coarse_dirt
fill 40 211 -9 40 212 -5 minecraft:calcite
fill 40 215 -12 40 215 -9 minecraft:oak_leaves[persistent=true]
fill 40 208 -10 40 209 -8 minecraft:diorite
fill 40 215 -12 40 215 -10 minecraft:birch_leaves[persistent=true]
fill 59 209 -15 59 211 -14 minecraft:diorite
fill 59 209 -17 59 209 -16 minecraft:moss_block
fill 59 210 -7 59 210 -4 minecraft:calcite
fill 59 215 -7 59 215 -2 minecraft:birch_leaves[persistent=true]
fill 59 204 -19 59 205 -15 minecraft:diorite
fill 49 204 -20 51 205 -20 minecraft:dark_prismarine
fill 54 211 -20 55 214 -20 minecraft:calcite
fill 47 211 -20 51 211 -20 minecraft:moss_block
fill 51 214 -20 53 215 -20 minecraft:moss_block
fill 53 215 -1 55 215 -1 minecraft:birch_leaves[persistent=true]
fill 45 203 -1 49 205 -1 minecraft:prismarine
fill 55 215 -1 55 215 -1 minecraft:birch_leaves[persistent=true]
fill 40 215 -1 41 215 -1 minecraft:prismarine
fill 44 214 -1 47 215 -1 minecraft:birch_leaves[persistent=true]
fill 55 212 -1 59 212 -1 minecraft:calcite
fill 40 215 -20 59 215 -1 minecraft:polished_deepslate
fill 41 215 -19 58 215 -2 minecraft:air
fill 41 201 -19 58 204 -16 minecraft:dirt
fill 41 205 -19 58 205 -16 minecraft:podzol
fill 41 201 -15 42 204 -15 minecraft:dirt
fill 41 205 -15 42 205 -15 minecraft:podzol
fill 44 201 -15 58 204 -15 minecraft:dirt
fill 44 205 -15 58 205 -15 minecraft:podzol
fill 41 201 -14 41 204 -2 minecraft:dirt
fill 41 205 -14 41 205 -2 minecraft:podzol
fill 46 201 -14 58 204 -2 minecraft:dirt
fill 46 205 -14 58 205 -2 minecraft:podzol
fill 42 201 -9 42 204 -2 minecraft:dirt
fill 42 205 -9 42 205 -2 minecraft:podzol
fill 43 201 -8 45 204 -2 minecraft:dirt
fill 43 205 -8 45 205 -2 minecraft:podzol
fill 43 201 -15 43 205 -14 minecraft:dirt
fill 43 206 -15 43 206 -14 minecraft:podzol
fill 42 201 -14 42 205 -10 minecraft:dirt
fill 42 206 -14 42 206 -10 minecraft:podzol
fill 44 201 -14 45 205 -14 minecraft:dirt
fill 44 206 -14 45 206 -14 minecraft:podzol
fill 45 201 -13 45 205 -9 minecraft:dirt
fill 45 206 -13 45 206 -9 minecraft:podzol
fill 43 201 -11 44 205 -9 minecraft:dirt
fill 43 206 -11 44 206 -9 minecraft:podzol
fill 43 201 -13 44 211 -13 minecraft:calcite
fill 43 212 -13 44 212 -13 minecraft:podzol
fill 43 201 -12 44 211 -12 minecraft:diorite
fill 43 212 -12 44 212 -12 minecraft:podzol
fill 56 204 -19 58 204 -11 minecraft:clay
fill 56 205 -19 58 205 -11 minecraft:water
fill 55 204 -14 55 204 -7 minecraft:clay
fill 55 205 -14 55 205 -7 minecraft:water
fill 56 204 -10 56 204 -7 minecraft:clay
fill 56 205 -10 56 205 -7 minecraft:water
fill 57 205 -10 58 205 -10 minecraft:sand
setblock 55 205 -10 minecraft:seagrass
setblock 55 205 -7 minecraft:seagrass
setblock 56 205 -16 minecraft:seagrass
setblock 56 205 -12 minecraft:seagrass
setblock 56 205 -7 minecraft:seagrass
setblock 57 205 -12 minecraft:seagrass
execute positioned 42 206 -7 run function rlk:room/prop/fo_bench
execute positioned 41 206 -14 run function rlk:room/prop/fo_col_b
execute positioned 42 206 -3 run function rlk:room/prop/p_grass
execute positioned 50 206 -5 run function rlk:room/prop/fo_flower
execute positioned 50 206 -18 run function rlk:room/prop/fo_flower
execute positioned 50 206 -2 run function rlk:room/prop/p_grass
execute positioned 41 206 -12 run function rlk:room/prop/fo_white
execute positioned 53 206 -2 run function rlk:room/prop/fo_flower
execute positioned 53 206 -8 run function rlk:room/prop/fo_white
setblock 43 213 -13 minecraft:short_grass keep
setblock 44 213 -12 minecraft:short_grass keep
