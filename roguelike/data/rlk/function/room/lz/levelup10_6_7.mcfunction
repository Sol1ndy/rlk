# 구역 건설 (levelup10_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 20 59 200 39 minecraft:podzol
fill 40 201 20 59 210 39 minecraft:stone
fill 41 201 21 58 210 38 minecraft:air
fill 41 209 21 58 209 38 minecraft:light[level=15]
fill 48 200 23 49 200 26 minecraft:moss_block
fill 49 200 32 50 200 33 minecraft:coarse_dirt
fill 40 209 27 40 210 28 minecraft:birch_leaves[persistent=true]
fill 40 209 24 40 210 27 minecraft:oak_leaves[persistent=true]
fill 40 203 28 40 206 31 minecraft:moss_block
fill 40 207 37 40 210 39 minecraft:calcite
fill 59 210 24 59 210 24 minecraft:oak_leaves[persistent=true]
fill 59 207 28 59 209 32 minecraft:calcite
fill 59 210 31 59 210 34 minecraft:oak_leaves[persistent=true]
fill 59 208 28 59 209 29 minecraft:diorite
fill 48 209 20 53 210 20 minecraft:birch_leaves[persistent=true]
fill 47 204 20 48 204 20 minecraft:prismarine
fill 53 205 20 54 206 20 minecraft:diorite
fill 47 202 39 48 204 39 minecraft:moss_block
fill 57 201 39 57 201 39 minecraft:calcite
fill 44 210 39 44 210 39 minecraft:oak_leaves[persistent=true]
fill 55 202 39 57 202 39 minecraft:diorite
fill 52 209 39 53 210 39 minecraft:oak_leaves[persistent=true]
fill 49 209 39 50 210 39 minecraft:oak_leaves[persistent=true]
fill 40 210 20 59 210 39 minecraft:polished_deepslate
fill 41 210 21 58 210 38 minecraft:air
fill 51 201 35 55 201 37 minecraft:podzol
fill 50 201 36 50 201 38 minecraft:podzol
fill 56 201 36 56 201 38 minecraft:podzol
fill 49 201 38 49 201 38 minecraft:podzol
fill 54 201 38 55 201 38 minecraft:podzol
fill 57 201 38 57 201 38 minecraft:podzol
fill 51 201 38 53 206 38 minecraft:calcite
fill 51 207 38 53 207 38 minecraft:podzol
fill 56 199 21 58 199 35 minecraft:clay
fill 56 200 21 58 200 35 minecraft:water
fill 55 199 26 55 199 34 minecraft:clay
fill 55 200 26 55 200 34 minecraft:water
fill 57 199 36 58 199 36 minecraft:clay
fill 57 200 36 58 200 36 minecraft:water
fill 57 200 37 58 200 37 minecraft:sand
setblock 55 200 29 minecraft:seagrass
setblock 56 200 21 minecraft:seagrass
setblock 56 200 32 minecraft:seagrass
setblock 58 200 23 minecraft:seagrass
setblock 58 200 27 minecraft:seagrass
setblock 58 200 34 minecraft:seagrass
execute positioned 47 201 36 run function rlk:room/prop/fo_col_b
execute positioned 54 201 32 run function rlk:room/prop/fo_flower
execute positioned 53 201 29 run function rlk:room/prop/fo_white
execute positioned 47 201 24 run function rlk:room/prop/fo_flower
execute positioned 54 201 32 run function rlk:room/prop/fo_flower
execute positioned 42 201 37 run function rlk:room/prop/fo_flower
execute positioned 47 201 32 run function rlk:room/prop/fo_flower
execute positioned 42 201 33 run function rlk:room/prop/fo_flower
execute positioned 49 201 31 run function rlk:room/prop/fo_flower
setblock 51 208 38 minecraft:short_grass keep
setblock 52 208 38 minecraft:short_grass keep
setblock 53 208 38 minecraft:short_grass keep
