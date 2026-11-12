# 구역 건설 (first5_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 13 200 -4 14 200 -3 minecraft:rooted_dirt
fill 15 200 -19 17 200 -17 minecraft:rooted_dirt
fill 0 201 -8 0 201 -3 minecraft:granite
fill 0 209 -20 0 210 -16 minecraft:oak_leaves[persistent=true]
fill 0 203 -8 0 203 -3 minecraft:tuff
fill 0 210 -20 0 210 -18 minecraft:oak_leaves[persistent=true]
fill 19 205 -19 19 205 -16 minecraft:moss_block
fill 19 209 -6 19 209 -2 minecraft:moss_block
fill 19 208 -6 19 210 -3 minecraft:andesite
fill 19 206 -9 19 209 -7 minecraft:moss_block
fill 19 206 -19 19 208 -18 minecraft:moss_block
fill 19 209 -6 19 210 -4 minecraft:oak_leaves[persistent=true]
fill 0 209 -20 4 210 -20 minecraft:oak_leaves[persistent=true]
fill 9 210 -20 14 210 -20 minecraft:oak_leaves[persistent=true]
fill 10 202 -20 12 203 -20 minecraft:andesite
fill 13 203 -20 17 205 -20 minecraft:tuff
fill 12 209 -20 13 210 -20 minecraft:moss_block
fill 2 210 -1 7 210 -1 minecraft:oak_leaves[persistent=true]
fill 8 201 -1 8 203 -1 minecraft:cobblestone
fill 8 204 -1 9 207 -1 minecraft:mossy_cobblestone
fill 16 209 -1 18 210 -1 minecraft:oak_leaves[persistent=true]
fill 8 205 -1 13 208 -1 minecraft:cobblestone
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 6 201 -19 6 201 -15 minecraft:podzol
fill 9 201 -19 10 201 -19 minecraft:podzol
fill 10 201 -18 10 201 -15 minecraft:podzol
fill 7 201 -15 9 201 -15 minecraft:podzol
fill 15 201 -9 17 201 -8 minecraft:podzol
fill 18 201 -8 18 201 -8 minecraft:podzol
fill 15 201 -7 15 201 -7 minecraft:podzol
fill 16 201 -6 16 201 -2 minecraft:podzol
fill 17 201 -2 18 201 -2 minecraft:podzol
fill 7 201 -19 8 201 -18 minecraft:dirt
fill 7 202 -19 8 202 -18 minecraft:podzol
fill 9 201 -18 9 201 -18 minecraft:dirt
fill 9 202 -18 9 202 -18 minecraft:podzol
fill 7 201 -17 7 201 -16 minecraft:dirt
fill 7 202 -17 7 202 -16 minecraft:podzol
fill 16 201 -7 18 201 -7 minecraft:dirt
fill 16 202 -7 18 202 -7 minecraft:podzol
fill 17 201 -6 18 201 -3 minecraft:dirt
fill 17 202 -6 18 202 -3 minecraft:podzol
fill 9 201 -17 9 207 -16 minecraft:andesite
fill 9 208 -17 9 208 -16 minecraft:podzol
fill 17 201 -12 18 207 -11 minecraft:andesite
fill 17 208 -12 18 208 -11 minecraft:podzol
fill 8 201 -17 8 207 -16 minecraft:stone
fill 8 208 -17 8 208 -16 minecraft:podzol
fill 17 201 -15 18 207 -13 minecraft:stone
fill 17 208 -15 18 208 -13 minecraft:podzol
fill 0 186 -20 4 199 -13 minecraft:stone
fill 1 186 -19 3 186 -14 minecraft:dirt
fill 1 187 -19 3 188 -14 minecraft:azalea_leaves[persistent=true]
fill 1 189 -19 3 201 -14 minecraft:air
execute positioned 1 201 -8 run function rlk:room/prop/p_fence_x
execute positioned 1 201 -5 run function rlk:room/prop/p_ruin_x
execute positioned 15 201 -17 run function rlk:room/prop/p_birch
execute positioned 18 201 -19 run function rlk:room/prop/p_dandelion
execute positioned 3 201 -17 run function rlk:room/prop/p_wildflower
execute positioned 10 201 -11 run function rlk:room/prop/p_litter
execute positioned 4 201 -8 run function rlk:room/prop/p_dandelion
execute positioned 1 201 -2 run function rlk:room/prop/p_wildflower
execute positioned 3 201 -7 run function rlk:room/prop/p_grass
execute positioned 15 201 -4 run function rlk:room/prop/p_grass
execute positioned 1 201 -19 run function rlk:room/prop/p_wildflower
execute positioned 2 201 -6 run function rlk:room/prop/p_wildflower
setblock 8 209 -17 minecraft:short_grass keep
setblock 8 209 -16 minecraft:azalea_leaves[persistent=true] keep
setblock 9 209 -17 minecraft:azalea_leaves[persistent=true] keep
setblock 9 209 -16 minecraft:short_grass keep
setblock 17 209 -15 minecraft:short_grass keep
setblock 17 209 -13 minecraft:short_grass keep
setblock 17 209 -12 minecraft:azalea_leaves[persistent=true] keep
setblock 17 209 -11 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 -15 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 -13 minecraft:short_grass keep
setblock 18 209 -12 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 -11 minecraft:azalea_leaves[persistent=true] keep
