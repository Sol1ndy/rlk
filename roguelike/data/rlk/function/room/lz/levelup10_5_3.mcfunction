# 구역 건설 (levelup10_5, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 0 59 200 19 minecraft:podzol
fill 40 201 0 59 210 19 minecraft:stone
fill 41 201 1 58 210 18 minecraft:air
fill 41 209 1 58 209 18 minecraft:light[level=15]
fill 47 200 7 49 200 8 minecraft:moss_block
fill 54 200 10 57 200 11 minecraft:coarse_dirt
fill 40 203 12 40 204 16 minecraft:andesite
fill 40 201 14 40 202 16 minecraft:tuff
fill 40 210 4 40 210 5 minecraft:oak_leaves[persistent=true]
fill 40 204 5 40 206 5 minecraft:cobblestone
fill 40 210 7 40 210 9 minecraft:andesite
fill 40 210 12 40 210 12 minecraft:oak_leaves[persistent=true]
fill 59 205 8 59 208 8 minecraft:moss_block
fill 59 204 1 59 205 2 minecraft:tuff
fill 59 210 17 59 210 17 minecraft:moss_block
fill 59 203 2 59 203 6 minecraft:moss_block
fill 59 204 5 59 205 6 minecraft:andesite
fill 59 205 14 59 208 18 minecraft:andesite
fill 49 205 0 54 207 0 minecraft:andesite
fill 52 201 0 56 203 0 minecraft:granite
fill 50 209 0 51 209 0 minecraft:moss_block
fill 55 209 19 58 210 19 minecraft:oak_leaves[persistent=true]
fill 58 202 19 59 202 19 minecraft:cobblestone
fill 52 210 19 52 210 19 minecraft:oak_leaves[persistent=true]
fill 51 205 19 52 206 19 minecraft:cobblestone
fill 41 203 19 46 204 19 minecraft:moss_block
fill 43 210 19 46 210 19 minecraft:oak_leaves[persistent=true]
fill 40 210 0 59 210 19 minecraft:polished_deepslate
fill 41 210 1 58 210 18 minecraft:air
fill 43 201 11 43 201 18 minecraft:podzol
fill 44 201 12 45 201 13 minecraft:podzol
fill 44 201 14 44 201 18 minecraft:podzol
fill 41 201 15 42 201 18 minecraft:podzol
fill 42 201 10 42 207 13 minecraft:andesite
fill 42 208 10 42 208 13 minecraft:podzol
fill 41 201 9 42 207 9 minecraft:stone
fill 41 208 9 42 208 9 minecraft:podzol
fill 41 201 10 41 207 14 minecraft:stone
fill 41 208 10 41 208 14 minecraft:podzol
fill 42 201 14 42 207 14 minecraft:stone
fill 42 208 14 42 208 14 minecraft:podzol
execute positioned 46 201 15 run function rlk:room/prop/p_fence_z
execute positioned 55 201 9 run function rlk:room/prop/p_oak
execute positioned 44 201 1 run function rlk:room/prop/p_pillar_ruin
execute positioned 50 201 7 run function rlk:room/prop/p_grass
execute positioned 55 201 11 run function rlk:room/prop/p_grass
execute positioned 54 201 14 run function rlk:room/prop/p_litter
execute positioned 46 201 18 run function rlk:room/prop/p_wildflower
execute positioned 57 201 3 run function rlk:room/prop/p_wildflower
execute positioned 52 201 16 run function rlk:room/prop/p_wildflower
execute positioned 55 201 3 run function rlk:room/prop/p_grass
setblock 41 209 10 minecraft:short_grass keep
setblock 41 209 13 minecraft:azalea_leaves[persistent=true] keep
setblock 42 209 9 minecraft:short_grass keep
setblock 42 209 10 minecraft:azalea_leaves[persistent=true] keep
setblock 42 209 11 minecraft:short_grass keep
setblock 42 209 12 minecraft:azalea_leaves[persistent=true] keep
setblock 42 209 13 minecraft:short_grass keep
setblock 42 209 14 minecraft:short_grass keep
