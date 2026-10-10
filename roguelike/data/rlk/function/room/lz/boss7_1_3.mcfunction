# 구역 건설 (boss7_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 13 200 8 14 200 10 minecraft:rooted_dirt
fill 8 200 12 12 200 14 minecraft:moss_block
fill 0 209 3 0 210 6 minecraft:oak_leaves[persistent=true]
fill 0 210 9 0 210 9 minecraft:oak_leaves[persistent=true]
fill 0 202 12 0 203 17 minecraft:moss_block
fill 0 210 5 0 210 6 minecraft:cobblestone
fill 19 206 15 19 207 18 minecraft:moss_block
fill 19 208 6 19 210 8 minecraft:cobblestone
fill 19 210 11 19 210 13 minecraft:oak_leaves[persistent=true]
fill 9 206 0 9 208 0 minecraft:moss_block
fill 14 201 0 15 203 0 minecraft:granite
fill 8 206 0 12 208 0 minecraft:andesite
fill 1 205 0 1 208 0 minecraft:mossy_cobblestone
fill 14 210 19 17 210 19 minecraft:oak_leaves[persistent=true]
fill 18 209 19 18 210 19 minecraft:andesite
fill 12 202 19 17 205 19 minecraft:moss_block
fill 1 209 19 1 210 19 minecraft:oak_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 5 201 11 5 201 14 minecraft:podzol
fill 4 201 12 4 201 13 minecraft:podzol
fill 3 201 13 3 201 17 minecraft:podzol
fill 6 201 15 13 201 15 minecraft:podzol
fill 14 201 16 15 201 17 minecraft:podzol
fill 4 201 17 4 201 18 minecraft:podzol
fill 14 201 18 14 201 18 minecraft:podzol
fill 4 201 14 4 201 16 minecraft:dirt
fill 4 202 14 4 202 16 minecraft:podzol
fill 5 201 15 5 201 18 minecraft:dirt
fill 5 202 15 5 202 18 minecraft:podzol
fill 6 201 16 13 201 16 minecraft:dirt
fill 6 202 16 13 202 16 minecraft:podzol
fill 6 201 17 6 201 18 minecraft:dirt
fill 6 202 17 6 202 18 minecraft:podzol
fill 12 201 17 13 201 18 minecraft:dirt
fill 12 202 17 13 202 18 minecraft:podzol
fill 7 201 18 7 201 18 minecraft:dirt
fill 7 202 18 7 202 18 minecraft:podzol
fill 11 201 18 11 201 18 minecraft:dirt
fill 11 202 18 11 202 18 minecraft:podzol
fill 7 201 17 11 202 17 minecraft:dirt
fill 7 203 17 11 203 17 minecraft:podzol
fill 8 201 18 10 202 18 minecraft:dirt
fill 8 203 18 10 203 18 minecraft:podzol
fill 1 201 2 2 206 3 minecraft:andesite
fill 1 207 2 2 207 3 minecraft:podzol
fill 1 201 1 2 206 1 minecraft:stone
fill 1 207 1 2 207 1 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:andesite
fill 12 208 3 12 208 3 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:stone
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:stone
fill 12 208 4 12 208 4 minecraft:podzol
execute positioned 5 201 3 run function rlk:room/prop/p_fence_z
execute positioned 5 202 13 run function rlk:room/prop/p_pillar_ruin
execute positioned 8 201 1 run function rlk:room/prop/p_litter
execute positioned 10 201 8 run function rlk:room/prop/p_dandelion
execute positioned 7 201 4 run function rlk:room/prop/p_grass
execute positioned 12 201 10 run function rlk:room/prop/p_grass
execute positioned 7 202 15 run function rlk:room/prop/p_litter
execute positioned 9 201 5 run function rlk:room/prop/p_wildflower
execute positioned 5 203 16 run function rlk:room/prop/p_grass
setblock 1 208 3 minecraft:short_grass keep
setblock 2 208 1 minecraft:azalea_leaves[persistent=true] keep
setblock 2 208 2 minecraft:azalea_leaves[persistent=true] keep
setblock 2 208 3 minecraft:azalea_leaves[persistent=true] keep
setblock 11 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock 12 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock 12 209 4 minecraft:short_grass keep
