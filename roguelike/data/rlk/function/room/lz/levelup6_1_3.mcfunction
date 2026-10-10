# 구역 건설 (levelup6_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -1 minecraft:air
fill 1 209 -19 18 209 -1 minecraft:light[level=15]
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 0 18 210 18 minecraft:air
fill 1 209 0 18 209 18 minecraft:light[level=15]
fill 7 200 -5 10 200 -4 minecraft:rooted_dirt
fill 7 200 13 8 200 15 minecraft:gravel
fill 12 200 8 15 200 9 minecraft:moss_block
fill 9 200 -15 10 200 -14 minecraft:gravel
fill 0 205 -3 0 205 -2 minecraft:moss_block
fill 0 204 -12 0 204 -7 minecraft:mossy_cobblestone
fill 0 209 -7 0 210 -2 minecraft:tuff
fill 0 206 -7 0 209 -7 minecraft:cobblestone
fill 19 207 -13 19 209 -9 minecraft:tuff
fill 19 210 -13 19 210 -10 minecraft:oak_leaves[persistent=true]
fill 19 203 -9 19 203 -6 minecraft:mossy_cobblestone
fill 4 201 -20 7 204 -20 minecraft:tuff
fill 1 205 -20 2 206 -20 minecraft:moss_block
fill 14 205 -20 18 205 -20 minecraft:mossy_cobblestone
fill 0 207 6 0 210 8 minecraft:andesite
fill 0 202 3 0 202 7 minecraft:cobblestone
fill 0 210 4 0 210 6 minecraft:granite
fill 19 207 9 19 208 10 minecraft:andesite
fill 19 208 12 19 210 16 minecraft:tuff
fill 19 204 2 19 204 5 minecraft:tuff
fill 19 209 4 19 210 5 minecraft:oak_leaves[persistent=true]
fill 1 210 19 1 210 19 minecraft:moss_block
fill 12 203 19 13 204 19 minecraft:mossy_cobblestone
fill 12 203 19 15 205 19 minecraft:moss_block
fill 15 201 19 17 202 19 minecraft:tuff
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -1 minecraft:air
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 0 18 210 18 minecraft:air
fill 14 201 -10 18 201 -10 minecraft:podzol
fill 14 201 -9 15 201 -9 minecraft:podzol
fill 17 201 -9 18 201 -9 minecraft:podzol
fill 14 201 -8 14 201 -7 minecraft:podzol
fill 12 201 -6 13 201 -5 minecraft:podzol
fill 14 201 -5 14 201 -5 minecraft:podzol
fill 15 201 -4 15 201 0 minecraft:podzol
fill 18 201 -1 18 201 0 minecraft:podzol
fill 16 201 0 17 201 0 minecraft:podzol
fill 3 201 6 3 201 7 minecraft:podzol
fill 1 201 7 2 201 7 minecraft:podzol
fill 4 201 7 5 201 7 minecraft:podzol
fill 1 201 8 1 201 8 minecraft:podzol
fill 5 201 8 5 201 13 minecraft:podzol
fill 1 201 12 1 201 13 minecraft:podzol
fill 2 201 13 4 201 13 minecraft:podzol
fill 3 201 14 3 201 14 minecraft:podzol
fill 16 201 -9 16 201 -1 minecraft:dirt
fill 16 202 -9 16 202 -1 minecraft:podzol
fill 15 201 -8 15 201 -5 minecraft:dirt
fill 15 202 -8 15 202 -5 minecraft:podzol
fill 17 201 -8 18 201 -2 minecraft:dirt
fill 17 202 -8 18 202 -2 minecraft:podzol
fill 14 201 -6 14 201 -6 minecraft:dirt
fill 14 202 -6 14 202 -6 minecraft:podzol
fill 17 201 -1 17 201 -1 minecraft:dirt
fill 17 202 -1 17 202 -1 minecraft:podzol
fill 2 201 8 4 201 8 minecraft:dirt
fill 2 202 8 4 202 8 minecraft:podzol
fill 1 201 9 2 201 11 minecraft:dirt
fill 1 202 9 2 202 11 minecraft:podzol
fill 3 201 11 4 201 12 minecraft:dirt
fill 3 202 11 4 202 12 minecraft:podzol
fill 2 201 12 2 201 12 minecraft:dirt
fill 2 202 12 2 202 12 minecraft:podzol
fill 1 201 -1 1 205 1 minecraft:stone
fill 1 206 -1 1 206 1 minecraft:podzol
fill 4 201 14 4 206 16 minecraft:stone
fill 4 207 14 4 207 16 minecraft:podzol
fill 3 201 15 3 206 15 minecraft:stone
fill 3 207 15 3 207 15 minecraft:podzol
fill 5 201 15 5 206 15 minecraft:stone
fill 5 207 15 5 207 15 minecraft:podzol
fill 3 201 9 4 207 10 minecraft:stone
fill 3 208 9 4 208 10 minecraft:podzol
execute positioned 18 201 -19 run function rlk:room/prop/p_fence_z
execute positioned 4 201 -6 run function rlk:room/prop/p_shrub_tree
execute positioned 9 201 -6 run function rlk:room/prop/p_hay
execute positioned 13 201 1 run function rlk:room/prop/p_dandelion
execute positioned 5 201 -5 run function rlk:room/prop/p_grass
execute positioned 5 201 -5 run function rlk:room/prop/p_dandelion
execute positioned 18 201 5 run function rlk:room/prop/p_wildflower
execute positioned 17 201 16 run function rlk:room/prop/p_grass
execute positioned 9 201 18 run function rlk:room/prop/p_dandelion
execute positioned 9 201 14 run function rlk:room/prop/p_grass
execute positioned 13 201 -17 run function rlk:room/prop/p_grass
execute positioned 15 201 13 run function rlk:room/prop/p_wildflower
execute positioned 12 201 13 run function rlk:room/prop/p_dandelion
execute positioned 4 201 -18 run function rlk:room/prop/p_grass
execute positioned 6 201 -9 run function rlk:room/prop/p_grass
execute positioned 5 201 -19 run function rlk:room/prop/p_wildflower
execute positioned 12 201 -3 run function rlk:room/prop/p_grass
execute positioned 4 202 13 run function rlk:room/prop/p_grass
execute positioned 1 203 9 run function rlk:room/prop/p_grass
setblock 1 207 -1 minecraft:short_grass keep
setblock 1 207 0 minecraft:short_grass keep
setblock 1 207 1 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 9 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 10 minecraft:azalea_leaves[persistent=true] keep
setblock 3 208 15 minecraft:azalea_leaves[persistent=true] keep
setblock 4 209 9 minecraft:azalea_leaves[persistent=true] keep
setblock 4 209 10 minecraft:azalea_leaves[persistent=true] keep
setblock 4 208 14 minecraft:azalea_leaves[persistent=true] keep
setblock 4 208 16 minecraft:azalea_leaves[persistent=true] keep
