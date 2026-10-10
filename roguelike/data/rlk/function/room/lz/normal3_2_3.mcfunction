# 구역 건설 (normal3_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:stone
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 6 200 28 9 200 30 minecraft:gravel
fill 10 200 31 12 200 34 minecraft:moss_block
fill 10 200 30 14 200 33 minecraft:coarse_dirt
fill 0 202 23 0 203 25 minecraft:andesite
fill 0 207 35 0 208 36 minecraft:granite
fill 0 208 26 0 210 29 minecraft:cobblestone
fill 0 209 23 0 210 26 minecraft:cobblestone
fill 0 209 30 0 210 30 minecraft:oak_leaves[persistent=true]
fill 19 209 21 19 210 25 minecraft:oak_leaves[persistent=true]
fill 19 204 29 19 206 33 minecraft:moss_block
fill 19 202 26 19 205 31 minecraft:mossy_cobblestone
fill 6 201 20 7 203 20 minecraft:moss_block
fill 10 201 20 11 204 20 minecraft:cobblestone
fill 8 210 20 8 210 20 minecraft:mossy_cobblestone
fill 14 209 20 19 210 20 minecraft:oak_leaves[persistent=true]
fill 7 207 39 12 210 39 minecraft:andesite
fill 3 209 39 6 210 39 minecraft:oak_leaves[persistent=true]
fill 0 201 39 1 203 39 minecraft:moss_block
fill 13 209 39 16 210 39 minecraft:oak_leaves[persistent=true]
fill 11 204 39 12 205 39 minecraft:moss_block
fill 13 204 39 18 204 39 minecraft:moss_block
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 3 201 21 3 201 25 minecraft:podzol
fill 4 201 26 5 201 26 minecraft:podzol
fill 3 201 27 4 201 27 minecraft:podzol
fill 1 201 28 2 201 28 minecraft:podzol
fill 2 201 21 2 201 27 minecraft:dirt
fill 2 202 21 2 202 27 minecraft:podzol
fill 1 201 26 1 201 27 minecraft:dirt
fill 1 202 26 1 202 27 minecraft:podzol
fill 3 201 26 3 201 26 minecraft:dirt
fill 3 202 26 3 202 26 minecraft:podzol
fill 1 201 21 1 202 25 minecraft:dirt
fill 1 203 21 1 203 25 minecraft:podzol
fill 5 201 37 7 205 37 minecraft:andesite
fill 5 206 37 7 206 37 minecraft:podzol
fill 6 201 38 7 205 38 minecraft:andesite
fill 6 206 38 7 206 38 minecraft:podzol
fill 5 201 38 5 205 38 minecraft:stone
fill 5 206 38 5 206 38 minecraft:podzol
execute positioned 5 201 31 run function rlk:room/prop/p_birch
execute positioned 10 201 35 run function rlk:room/prop/p_boulder
execute positioned 15 201 37 run function rlk:room/prop/p_dandelion
execute positioned 16 201 25 run function rlk:room/prop/p_grass
execute positioned 17 201 25 run function rlk:room/prop/p_wildflower
execute positioned 7 201 32 run function rlk:room/prop/p_wildflower
execute positioned 16 201 34 run function rlk:room/prop/p_grass
execute positioned 18 201 30 run function rlk:room/prop/p_dandelion
execute positioned 11 201 21 run function rlk:room/prop/p_grass
execute positioned 8 201 38 run function rlk:room/prop/p_grass
setblock 5 207 38 minecraft:azalea_leaves[persistent=true] keep
setblock 6 207 37 minecraft:azalea_leaves[persistent=true] keep
setblock 6 207 38 minecraft:azalea_leaves[persistent=true] keep
setblock 7 207 37 minecraft:azalea_leaves[persistent=true] keep
setblock 7 207 38 minecraft:azalea_leaves[persistent=true] keep
