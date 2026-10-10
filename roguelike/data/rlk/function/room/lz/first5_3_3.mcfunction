# 구역 건설 (first5_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 212 -1 minecraft:stone
fill 1 201 -19 18 212 -2 minecraft:air
fill 1 211 -19 18 211 -2 minecraft:light[level=15]
fill 13 202 -4 14 202 -3 minecraft:rooted_dirt
fill 15 202 -19 17 202 -17 minecraft:rooted_dirt
fill 0 202 -8 0 203 -3 minecraft:granite
fill 0 201 -16 0 202 -13 minecraft:tuff
fill 0 211 -20 0 212 -16 minecraft:oak_leaves[persistent=true]
fill 0 205 -8 0 205 -3 minecraft:tuff
fill 0 212 -20 0 212 -18 minecraft:oak_leaves[persistent=true]
fill 19 207 -19 19 207 -16 minecraft:moss_block
fill 19 211 -6 19 211 -2 minecraft:moss_block
fill 19 210 -6 19 212 -3 minecraft:andesite
fill 19 208 -9 19 211 -7 minecraft:moss_block
fill 19 208 -19 19 210 -18 minecraft:moss_block
fill 19 211 -6 19 212 -4 minecraft:oak_leaves[persistent=true]
fill 0 211 -20 4 212 -20 minecraft:oak_leaves[persistent=true]
fill 9 212 -20 14 212 -20 minecraft:oak_leaves[persistent=true]
fill 10 204 -20 12 205 -20 minecraft:andesite
fill 13 205 -20 17 207 -20 minecraft:tuff
fill 12 211 -20 13 212 -20 minecraft:moss_block
fill 2 212 -1 7 212 -1 minecraft:oak_leaves[persistent=true]
fill 8 202 -1 8 205 -1 minecraft:cobblestone
fill 8 206 -1 9 209 -1 minecraft:mossy_cobblestone
fill 16 211 -1 18 212 -1 minecraft:oak_leaves[persistent=true]
fill 8 207 -1 13 210 -1 minecraft:cobblestone
fill 0 212 -20 19 212 -1 minecraft:polished_deepslate
fill 1 212 -19 18 212 -2 minecraft:air
fill 1 201 -19 5 201 -2 minecraft:dirt
fill 1 202 -19 5 202 -2 minecraft:podzol
fill 11 201 -19 18 201 -16 minecraft:dirt
fill 11 202 -19 18 202 -16 minecraft:podzol
fill 11 201 -15 16 201 -10 minecraft:dirt
fill 11 202 -15 16 202 -10 minecraft:podzol
fill 6 201 -14 10 201 -2 minecraft:dirt
fill 6 202 -14 10 202 -2 minecraft:podzol
fill 17 201 -10 18 201 -10 minecraft:dirt
fill 17 202 -10 18 202 -10 minecraft:podzol
fill 11 201 -9 14 201 -2 minecraft:dirt
fill 11 202 -9 14 202 -2 minecraft:podzol
fill 18 201 -9 18 201 -9 minecraft:dirt
fill 18 202 -9 18 202 -9 minecraft:podzol
fill 15 201 -6 15 201 -2 minecraft:dirt
fill 15 202 -6 15 202 -2 minecraft:podzol
fill 6 201 -19 6 202 -15 minecraft:dirt
fill 6 203 -19 6 203 -15 minecraft:podzol
fill 9 201 -19 10 202 -19 minecraft:dirt
fill 9 203 -19 10 203 -19 minecraft:podzol
fill 10 201 -18 10 202 -15 minecraft:dirt
fill 10 203 -18 10 203 -15 minecraft:podzol
fill 7 201 -15 9 202 -15 minecraft:dirt
fill 7 203 -15 9 203 -15 minecraft:podzol
fill 15 201 -9 17 202 -8 minecraft:dirt
fill 15 203 -9 17 203 -8 minecraft:podzol
fill 18 201 -8 18 202 -8 minecraft:dirt
fill 18 203 -8 18 203 -8 minecraft:podzol
fill 15 201 -7 15 202 -7 minecraft:dirt
fill 15 203 -7 15 203 -7 minecraft:podzol
fill 16 201 -6 16 202 -2 minecraft:dirt
fill 16 203 -6 16 203 -2 minecraft:podzol
fill 17 201 -2 18 202 -2 minecraft:dirt
fill 17 203 -2 18 203 -2 minecraft:podzol
fill 7 201 -19 8 203 -18 minecraft:dirt
fill 7 204 -19 8 204 -18 minecraft:podzol
fill 9 201 -18 9 203 -18 minecraft:dirt
fill 9 204 -18 9 204 -18 minecraft:podzol
fill 7 201 -17 7 203 -16 minecraft:dirt
fill 7 204 -17 7 204 -16 minecraft:podzol
fill 16 201 -7 18 203 -7 minecraft:dirt
fill 16 204 -7 18 204 -7 minecraft:podzol
fill 17 201 -6 18 203 -3 minecraft:dirt
fill 17 204 -6 18 204 -3 minecraft:podzol
fill 9 201 -17 9 209 -16 minecraft:andesite
fill 9 210 -17 9 210 -16 minecraft:podzol
fill 17 201 -12 18 209 -11 minecraft:andesite
fill 17 210 -12 18 210 -11 minecraft:podzol
fill 8 201 -17 8 209 -16 minecraft:stone
fill 8 210 -17 8 210 -16 minecraft:podzol
fill 17 201 -15 18 209 -13 minecraft:stone
fill 17 210 -15 18 210 -13 minecraft:podzol
fill 0 186 -20 4 199 -13 minecraft:stone
fill 1 186 -19 3 186 -14 minecraft:dirt
fill 1 187 -19 3 188 -14 minecraft:azalea_leaves[persistent=true]
fill 1 189 -19 3 203 -14 minecraft:air
execute positioned 1 203 -8 run function rlk:room/prop/p_fence_x
execute positioned 1 203 -5 run function rlk:room/prop/p_ruin_x
execute positioned 15 203 -17 run function rlk:room/prop/p_birch
execute positioned 18 203 -19 run function rlk:room/prop/p_dandelion
execute positioned 3 203 -17 run function rlk:room/prop/p_wildflower
execute positioned 10 203 -11 run function rlk:room/prop/p_litter
execute positioned 4 203 -8 run function rlk:room/prop/p_dandelion
execute positioned 1 203 -2 run function rlk:room/prop/p_wildflower
execute positioned 3 203 -7 run function rlk:room/prop/p_grass
execute positioned 15 203 -4 run function rlk:room/prop/p_grass
execute positioned 1 203 -19 run function rlk:room/prop/p_wildflower
execute positioned 2 203 -6 run function rlk:room/prop/p_wildflower
setblock 8 211 -17 minecraft:short_grass keep
setblock 8 211 -16 minecraft:azalea_leaves[persistent=true] keep
setblock 9 211 -17 minecraft:azalea_leaves[persistent=true] keep
setblock 9 211 -16 minecraft:short_grass keep
setblock 17 211 -15 minecraft:short_grass keep
setblock 17 211 -13 minecraft:short_grass keep
setblock 17 211 -12 minecraft:azalea_leaves[persistent=true] keep
setblock 17 211 -11 minecraft:azalea_leaves[persistent=true] keep
setblock 18 211 -15 minecraft:azalea_leaves[persistent=true] keep
setblock 18 211 -13 minecraft:short_grass keep
setblock 18 211 -12 minecraft:azalea_leaves[persistent=true] keep
setblock 18 211 -11 minecraft:azalea_leaves[persistent=true] keep
