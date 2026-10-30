# 구역 건설 (normal28_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 7 200 15 11 200 16 minecraft:rooted_dirt
fill 6 200 6 7 200 8 minecraft:rooted_dirt
fill 0 209 1 0 210 3 minecraft:oak_leaves[persistent=true]
fill 0 202 4 0 203 8 minecraft:mossy_cobblestone
fill 0 202 2 0 202 6 minecraft:moss_block
fill 0 204 9 0 206 14 minecraft:andesite
fill 0 204 7 0 204 12 minecraft:andesite
fill 0 210 11 0 210 15 minecraft:oak_leaves[persistent=true]
fill 19 204 2 19 207 5 minecraft:mossy_cobblestone
fill 19 204 5 19 205 10 minecraft:mossy_cobblestone
fill 19 204 3 19 207 7 minecraft:cobblestone
fill 19 209 10 19 210 11 minecraft:oak_leaves[persistent=true]
fill 19 204 6 19 206 8 minecraft:andesite
fill 19 209 6 19 210 10 minecraft:oak_leaves[persistent=true]
fill 7 208 0 10 208 0 minecraft:moss_block
fill 3 201 0 6 203 0 minecraft:moss_block
fill 12 204 0 14 204 0 minecraft:andesite
fill 12 202 0 14 205 0 minecraft:andesite
fill 10 204 0 11 207 0 minecraft:mossy_cobblestone
fill 13 206 0 16 206 0 minecraft:moss_block
fill 17 207 19 17 207 19 minecraft:mossy_cobblestone
fill 17 207 19 18 207 19 minecraft:moss_block
fill 15 209 19 19 210 19 minecraft:oak_leaves[persistent=true]
fill 9 206 19 10 209 19 minecraft:andesite
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 2 201 1 3 201 1 minecraft:podzol
fill 3 201 2 3 201 5 minecraft:podzol
fill 4 201 6 4 201 6 minecraft:podzol
fill 5 201 7 5 201 9 minecraft:podzol
fill 16 201 7 18 201 7 minecraft:podzol
fill 4 201 8 4 201 10 minecraft:podzol
fill 15 201 8 16 201 8 minecraft:podzol
fill 2 201 9 3 201 10 minecraft:podzol
fill 15 201 9 15 201 14 minecraft:podzol
fill 1 201 10 1 201 11 minecraft:podzol
fill 2 201 11 2 201 11 minecraft:podzol
fill 12 201 15 14 201 15 minecraft:podzol
fill 13 201 16 13 201 17 minecraft:podzol
fill 14 201 17 14 201 18 minecraft:podzol
fill 15 201 18 16 201 18 minecraft:podzol
fill 1 201 1 1 201 9 minecraft:dirt
fill 1 202 1 1 202 9 minecraft:podzol
fill 2 201 2 2 201 8 minecraft:dirt
fill 2 202 2 2 202 8 minecraft:podzol
fill 3 201 6 3 201 8 minecraft:dirt
fill 3 202 6 3 202 8 minecraft:podzol
fill 4 201 7 4 201 7 minecraft:dirt
fill 4 202 7 4 202 7 minecraft:podzol
fill 17 201 8 18 201 9 minecraft:dirt
fill 17 202 8 18 202 9 minecraft:podzol
fill 16 201 9 16 201 14 minecraft:dirt
fill 16 202 9 16 202 14 minecraft:podzol
fill 15 201 15 15 201 17 minecraft:dirt
fill 15 202 15 15 202 17 minecraft:podzol
fill 14 201 16 14 201 16 minecraft:dirt
fill 14 202 16 14 202 16 minecraft:podzol
fill 16 201 16 16 201 17 minecraft:dirt
fill 16 202 16 16 202 17 minecraft:podzol
fill 17 201 17 18 201 18 minecraft:dirt
fill 17 202 17 18 202 18 minecraft:podzol
fill 17 201 10 18 202 16 minecraft:dirt
fill 17 203 10 18 203 16 minecraft:podzol
fill 16 201 15 16 202 15 minecraft:dirt
fill 16 203 15 16 203 15 minecraft:podzol
fill 1 201 12 2 205 15 minecraft:stone
fill 1 206 12 2 206 15 minecraft:podzol
fill 3 201 12 4 206 13 minecraft:stone
fill 3 207 12 4 207 13 minecraft:podzol
execute positioned 1 203 4 run function rlk:room/prop/p_pillar_ruin
execute positioned 11 201 1 run function rlk:room/prop/p_grass
execute positioned 7 201 12 run function rlk:room/prop/p_grass
execute positioned 7 201 12 run function rlk:room/prop/p_grass
execute positioned 15 202 12 run function rlk:room/prop/p_wildflower
execute positioned 18 201 2 run function rlk:room/prop/p_wildflower
execute positioned 13 201 6 run function rlk:room/prop/p_litter
setblock 1 207 12 minecraft:azalea_leaves[persistent=true] keep
setblock 1 207 13 minecraft:azalea_leaves[persistent=true] keep
setblock 1 207 14 minecraft:azalea_leaves[persistent=true] keep
setblock 1 207 15 minecraft:azalea_leaves[persistent=true] keep
setblock 2 207 13 minecraft:short_grass keep
setblock 2 207 14 minecraft:azalea_leaves[persistent=true] keep
setblock 3 208 13 minecraft:short_grass keep
setblock 4 208 12 minecraft:short_grass keep
setblock 4 208 13 minecraft:short_grass keep
