# 구역 건설 (levelup7_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -1 minecraft:air
fill 1 209 -19 18 209 -1 minecraft:light[level=15]
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 0 18 210 18 minecraft:air
fill 1 209 0 18 209 18 minecraft:light[level=15]
fill 12 200 -12 14 200 -9 minecraft:gravel
fill 4 200 11 5 200 12 minecraft:rooted_dirt
fill 7 200 8 9 200 10 minecraft:coarse_dirt
fill 1 200 -9 2 200 -7 minecraft:gravel
fill 11 200 -15 12 200 -13 minecraft:moss_block
fill 6 200 -7 9 200 -5 minecraft:rooted_dirt
fill 5 200 10 9 200 13 minecraft:moss_block
fill 13 200 -7 15 200 -4 minecraft:gravel
fill 0 210 -20 0 210 -20 minecraft:oak_leaves[persistent=true]
fill 0 210 -6 0 210 -6 minecraft:tuff
fill 0 209 -20 0 210 -20 minecraft:mossy_cobblestone
fill 19 205 -4 19 208 -1 minecraft:andesite
fill 19 208 -9 19 209 -4 minecraft:andesite
fill 19 210 -12 19 210 -7 minecraft:oak_leaves[persistent=true]
fill 11 206 -20 13 206 -20 minecraft:andesite
fill 10 206 -20 11 209 -20 minecraft:andesite
fill 10 205 -20 14 206 -20 minecraft:cobblestone
fill 3 210 -20 6 210 -20 minecraft:oak_leaves[persistent=true]
fill 9 210 -20 12 210 -20 minecraft:oak_leaves[persistent=true]
fill 0 210 11 0 210 14 minecraft:oak_leaves[persistent=true]
fill 0 205 2 0 206 3 minecraft:moss_block
fill 0 201 1 0 204 6 minecraft:andesite
fill 0 207 7 0 210 11 minecraft:andesite
fill 0 204 3 0 207 6 minecraft:cobblestone
fill 0 210 12 0 210 15 minecraft:oak_leaves[persistent=true]
fill 19 201 7 19 204 9 minecraft:andesite
fill 19 208 13 19 209 16 minecraft:tuff
fill 19 209 1 19 210 6 minecraft:cobblestone
fill 19 207 9 19 208 11 minecraft:mossy_cobblestone
fill 19 210 2 19 210 3 minecraft:oak_leaves[persistent=true]
fill 19 205 1 19 206 6 minecraft:cobblestone
fill 4 209 19 9 210 19 minecraft:andesite
fill 4 202 19 6 202 19 minecraft:moss_block
fill 13 201 19 17 201 19 minecraft:mossy_cobblestone
fill 13 201 19 16 204 19 minecraft:tuff
fill 7 208 19 12 210 19 minecraft:andesite
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -1 minecraft:air
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 0 18 210 18 minecraft:air
fill 5 201 -19 6 201 -19 minecraft:podzol
fill 6 201 -18 7 201 -16 minecraft:podzol
fill 5 201 -15 6 201 -15 minecraft:podzol
fill 4 201 -14 5 201 -13 minecraft:podzol
fill 3 201 -13 3 201 -12 minecraft:podzol
fill 1 201 -12 2 201 -11 minecraft:podzol
fill 4 201 -12 4 201 -12 minecraft:podzol
fill 15 201 3 17 201 11 minecraft:podzol
fill 18 201 4 18 201 11 minecraft:podzol
fill 11 201 5 14 201 5 minecraft:podzol
fill 14 201 6 14 201 11 minecraft:podzol
fill 1 201 -19 4 201 -15 minecraft:dirt
fill 1 202 -19 4 202 -15 minecraft:podzol
fill 5 201 -18 5 201 -16 minecraft:dirt
fill 5 202 -18 5 202 -16 minecraft:podzol
fill 1 201 -14 3 201 -14 minecraft:dirt
fill 1 202 -14 3 202 -14 minecraft:podzol
fill 1 201 -13 2 201 -13 minecraft:dirt
fill 1 202 -13 2 202 -13 minecraft:podzol
fill 3 201 -8 4 206 -7 minecraft:stone
fill 3 207 -8 4 207 -7 minecraft:podzol
fill 1 201 8 2 207 9 minecraft:andesite
fill 1 208 8 2 208 9 minecraft:podzol
fill 1 201 -3 2 207 1 minecraft:stone
fill 1 208 -3 2 208 1 minecraft:podzol
fill 1 201 4 3 207 7 minecraft:stone
fill 1 208 4 3 208 7 minecraft:podzol
fill 3 201 8 3 207 9 minecraft:stone
fill 3 208 8 3 208 9 minecraft:podzol
execute positioned 17 201 -16 run function rlk:room/prop/p_hay
execute positioned 15 201 -2 run function rlk:room/prop/p_boulder_s
execute positioned 13 201 -5 run function rlk:room/prop/p_birch
execute positioned 11 201 6 run function rlk:room/prop/p_wildflower
execute positioned 13 201 17 run function rlk:room/prop/p_dandelion
execute positioned 3 201 15 run function rlk:room/prop/p_grass
execute positioned 8 201 -12 run function rlk:room/prop/p_wildflower
execute positioned 10 201 -15 run function rlk:room/prop/p_litter
execute positioned 15 201 -2 run function rlk:room/prop/p_grass
execute positioned 12 201 -7 run function rlk:room/prop/p_litter
execute positioned 18 202 6 run function rlk:room/prop/p_grass
execute positioned 18 201 3 run function rlk:room/prop/p_dandelion
execute positioned 16 202 10 run function rlk:room/prop/p_grass
execute positioned 7 201 -6 run function rlk:room/prop/p_grass
execute positioned 15 201 -10 run function rlk:room/prop/p_grass
execute positioned 18 201 3 run function rlk:room/prop/p_wildflower
execute positioned 3 201 -3 run function rlk:room/prop/p_wildflower
setblock 1 209 -3 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 -1 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 0 minecraft:short_grass keep
setblock 1 209 1 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 6 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 8 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 9 minecraft:short_grass keep
setblock 2 209 -3 minecraft:azalea_leaves[persistent=true] keep
setblock 2 209 -2 minecraft:short_grass keep
setblock 2 209 -1 minecraft:short_grass keep
setblock 2 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock 2 209 6 minecraft:short_grass keep
setblock 2 209 7 minecraft:azalea_leaves[persistent=true] keep
setblock 2 209 8 minecraft:short_grass keep
setblock 2 209 9 minecraft:azalea_leaves[persistent=true] keep
setblock 3 208 -7 minecraft:short_grass keep
setblock 3 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 5 minecraft:azalea_leaves[persistent=true] keep
setblock 4 208 -8 minecraft:azalea_leaves[persistent=true] keep
setblock 4 208 -7 minecraft:short_grass keep
