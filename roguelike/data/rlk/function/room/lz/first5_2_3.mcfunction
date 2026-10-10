# 구역 건설 (first5_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:podzol
fill 20 201 0 39 210 19 minecraft:stone
fill 21 201 1 38 210 18 minecraft:air
fill 21 209 1 38 209 18 minecraft:light[level=15]
fill 22 200 15 26 200 18 minecraft:rooted_dirt
fill 20 210 14 20 210 14 minecraft:oak_leaves[persistent=true]
fill 20 205 9 20 206 12 minecraft:moss_block
fill 20 207 4 20 209 6 minecraft:mossy_cobblestone
fill 20 209 6 20 210 11 minecraft:oak_leaves[persistent=true]
fill 20 202 8 20 203 12 minecraft:cobblestone
fill 39 210 6 39 210 9 minecraft:oak_leaves[persistent=true]
fill 39 208 0 39 210 0 minecraft:moss_block
fill 39 201 1 39 201 2 minecraft:mossy_cobblestone
fill 39 206 17 39 207 17 minecraft:moss_block
fill 39 206 11 39 208 12 minecraft:mossy_cobblestone
fill 27 202 0 28 204 0 minecraft:andesite
fill 21 207 0 24 209 0 minecraft:moss_block
fill 23 210 0 26 210 0 minecraft:oak_leaves[persistent=true]
fill 26 201 19 31 203 19 minecraft:mossy_cobblestone
fill 33 201 19 37 202 19 minecraft:mossy_cobblestone
fill 27 206 19 31 206 19 minecraft:cobblestone
fill 27 203 19 29 206 19 minecraft:andesite
fill 31 204 19 35 205 19 minecraft:moss_block
fill 30 206 19 30 209 19 minecraft:mossy_cobblestone
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 38 210 18 minecraft:air
fill 25 201 1 34 201 1 minecraft:podzol
fill 26 201 2 34 201 2 minecraft:podzol
fill 21 201 3 32 201 3 minecraft:podzol
fill 26 201 4 32 201 5 minecraft:podzol
fill 35 201 4 37 201 4 minecraft:podzol
fill 33 201 5 36 201 5 minecraft:podzol
fill 35 201 6 35 201 6 minecraft:podzol
fill 21 201 1 24 201 2 minecraft:dirt
fill 21 202 1 24 202 2 minecraft:podzol
fill 25 201 2 25 201 2 minecraft:dirt
fill 25 202 2 25 202 2 minecraft:podzol
fill 33 201 4 34 207 4 minecraft:andesite
fill 33 208 4 34 208 4 minecraft:podzol
fill 35 201 1 38 207 3 minecraft:stone
fill 35 208 1 38 208 3 minecraft:podzol
fill 33 201 3 34 207 3 minecraft:stone
fill 33 208 3 34 208 3 minecraft:podzol
execute positioned 36 201 12 run function rlk:room/prop/p_oak
execute positioned 35 201 7 run function rlk:room/prop/p_fence_z
execute positioned 29 202 4 run function rlk:room/prop/p_boulder
execute positioned 21 201 16 run function rlk:room/prop/p_boulder_s
execute positioned 38 201 13 run function rlk:room/prop/p_wildflower
execute positioned 32 201 12 run function rlk:room/prop/p_wildflower
execute positioned 26 201 13 run function rlk:room/prop/p_grass
execute positioned 37 201 10 run function rlk:room/prop/p_grass
execute positioned 26 201 13 run function rlk:room/prop/p_wildflower
execute positioned 21 202 3 run function rlk:room/prop/p_dandelion
execute positioned 31 202 3 run function rlk:room/prop/p_grass
execute positioned 28 202 1 run function rlk:room/prop/p_wildflower
setblock 33 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock 34 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock 36 209 2 minecraft:short_grass keep
setblock 36 209 3 minecraft:short_grass keep
setblock 37 209 2 minecraft:azalea_leaves[persistent=true] keep
setblock 37 209 3 minecraft:short_grass keep
setblock 38 209 1 minecraft:azalea_leaves[persistent=true] keep
setblock 38 209 2 minecraft:azalea_leaves[persistent=true] keep
setblock 38 209 3 minecraft:azalea_leaves[persistent=true] keep
