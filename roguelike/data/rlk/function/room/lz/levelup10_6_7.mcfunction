# 구역 건설 (levelup10_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 20 59 200 39 minecraft:podzol
fill 40 201 20 59 215 39 minecraft:stone
fill 41 201 21 58 215 38 minecraft:air
fill 41 214 21 58 214 38 minecraft:light[level=15]
fill 48 205 23 49 205 26 minecraft:moss_block
fill 49 205 32 50 205 33 minecraft:coarse_dirt
fill 40 214 27 40 215 28 minecraft:birch_leaves[persistent=true]
fill 40 214 24 40 215 27 minecraft:oak_leaves[persistent=true]
fill 40 208 28 40 211 31 minecraft:moss_block
fill 40 212 37 40 215 39 minecraft:calcite
fill 59 215 24 59 215 24 minecraft:oak_leaves[persistent=true]
fill 59 212 28 59 214 32 minecraft:calcite
fill 59 215 31 59 215 34 minecraft:oak_leaves[persistent=true]
fill 59 213 28 59 214 29 minecraft:diorite
fill 59 202 36 59 204 37 minecraft:calcite
fill 48 214 20 53 215 20 minecraft:birch_leaves[persistent=true]
fill 47 209 20 48 209 20 minecraft:prismarine
fill 53 210 20 54 211 20 minecraft:diorite
fill 47 207 39 48 209 39 minecraft:moss_block
fill 57 203 39 57 206 39 minecraft:calcite
fill 44 215 39 44 215 39 minecraft:oak_leaves[persistent=true]
fill 55 207 39 57 207 39 minecraft:diorite
fill 52 214 39 53 215 39 minecraft:oak_leaves[persistent=true]
fill 49 214 39 50 215 39 minecraft:oak_leaves[persistent=true]
fill 40 215 20 59 215 39 minecraft:polished_deepslate
fill 41 215 21 58 215 38 minecraft:air
fill 41 201 21 58 204 34 minecraft:dirt
fill 41 205 21 58 205 34 minecraft:podzol
fill 41 201 35 50 204 35 minecraft:dirt
fill 41 205 35 50 205 35 minecraft:podzol
fill 56 201 35 58 204 35 minecraft:dirt
fill 56 205 35 58 205 35 minecraft:podzol
fill 41 201 36 49 204 37 minecraft:dirt
fill 41 205 36 49 205 37 minecraft:podzol
fill 57 201 36 58 204 37 minecraft:dirt
fill 57 205 36 58 205 37 minecraft:podzol
fill 41 201 38 48 204 38 minecraft:dirt
fill 41 205 38 48 205 38 minecraft:podzol
fill 58 201 38 58 204 38 minecraft:dirt
fill 58 205 38 58 205 38 minecraft:podzol
fill 51 201 35 55 205 37 minecraft:dirt
fill 51 206 35 55 206 37 minecraft:podzol
fill 50 201 36 50 205 38 minecraft:dirt
fill 50 206 36 50 206 38 minecraft:podzol
fill 56 201 36 56 205 38 minecraft:dirt
fill 56 206 36 56 206 38 minecraft:podzol
fill 49 201 38 49 205 38 minecraft:dirt
fill 49 206 38 49 206 38 minecraft:podzol
fill 54 201 38 55 205 38 minecraft:dirt
fill 54 206 38 55 206 38 minecraft:podzol
fill 57 201 38 57 205 38 minecraft:dirt
fill 57 206 38 57 206 38 minecraft:podzol
fill 51 201 38 53 211 38 minecraft:calcite
fill 51 212 38 53 212 38 minecraft:podzol
fill 56 204 21 58 204 35 minecraft:clay
fill 56 205 21 58 205 35 minecraft:water
fill 55 204 26 55 204 34 minecraft:clay
fill 55 205 26 55 205 34 minecraft:water
fill 57 204 36 58 204 36 minecraft:clay
fill 57 205 36 58 205 36 minecraft:water
fill 57 205 37 58 205 37 minecraft:sand
setblock 55 205 29 minecraft:seagrass
setblock 56 205 21 minecraft:seagrass
setblock 56 205 32 minecraft:seagrass
setblock 58 205 23 minecraft:seagrass
setblock 58 205 27 minecraft:seagrass
setblock 58 205 34 minecraft:seagrass
execute positioned 47 206 36 run function rlk:room/prop/fo_col_b
execute positioned 54 206 32 run function rlk:room/prop/fo_flower
execute positioned 53 206 29 run function rlk:room/prop/fo_white
execute positioned 47 206 24 run function rlk:room/prop/fo_flower
execute positioned 54 206 32 run function rlk:room/prop/fo_flower
execute positioned 42 206 37 run function rlk:room/prop/fo_flower
execute positioned 47 206 32 run function rlk:room/prop/fo_flower
execute positioned 42 206 33 run function rlk:room/prop/fo_flower
execute positioned 49 206 31 run function rlk:room/prop/fo_flower
setblock 51 213 38 minecraft:short_grass keep
setblock 52 213 38 minecraft:short_grass keep
setblock 53 213 38 minecraft:short_grass keep
