# 구역 건설 (root7_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 33 200 -12 37 200 -11 minecraft:rooted_dirt
fill 20 204 -18 20 206 -14 minecraft:moss_block
fill 20 201 -20 20 202 -20 minecraft:andesite
fill 20 207 -8 20 207 -4 minecraft:moss_block
fill 20 210 -16 20 210 -11 minecraft:oak_leaves[persistent=true]
fill 20 205 -4 20 205 -1 minecraft:tuff
fill 39 203 -12 39 206 -12 minecraft:andesite
fill 39 201 -12 39 204 -10 minecraft:tuff
fill 39 203 -3 39 203 -3 minecraft:andesite
fill 23 208 -20 25 209 -20 minecraft:andesite
fill 21 205 -20 21 208 -20 minecraft:mossy_cobblestone
fill 32 209 -20 37 210 -20 minecraft:andesite
fill 24 203 -20 24 205 -20 minecraft:moss_block
fill 26 209 -20 28 210 -20 minecraft:moss_block
fill 23 208 -1 28 209 -1 minecraft:andesite
fill 29 210 -1 33 210 -1 minecraft:mossy_cobblestone
fill 23 205 -1 28 206 -1 minecraft:moss_block
fill 33 210 -1 38 210 -1 minecraft:mossy_cobblestone
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 28 201 -19 28 201 -17 minecraft:podzol
fill 21 201 -17 25 201 -17 minecraft:podzol
fill 26 201 -16 27 201 -15 minecraft:podzol
fill 27 201 -19 27 201 -17 minecraft:dirt
fill 27 202 -19 27 202 -17 minecraft:podzol
fill 21 201 -18 26 201 -18 minecraft:dirt
fill 21 202 -18 26 202 -18 minecraft:podzol
fill 26 201 -17 26 201 -17 minecraft:dirt
fill 26 202 -17 26 202 -17 minecraft:podzol
fill 21 201 -19 26 202 -19 minecraft:dirt
fill 21 203 -19 26 203 -19 minecraft:podzol
fill 30 201 -3 32 205 -2 minecraft:andesite
fill 30 206 -3 32 206 -2 minecraft:podzol
fill 29 201 -3 29 205 -2 minecraft:stone
fill 29 206 -3 29 206 -2 minecraft:podzol
fill 30 201 -17 31 206 -16 minecraft:stone
fill 30 207 -17 31 207 -16 minecraft:podzol
execute positioned 32 201 -19 run function rlk:room/prop/p_fence_x
execute positioned 36 201 -6 run function rlk:room/prop/p_birch
execute positioned 38 201 -9 run function rlk:room/prop/p_wildflower
execute positioned 25 201 -14 run function rlk:room/prop/p_litter
execute positioned 26 201 -7 run function rlk:room/prop/p_grass
execute positioned 22 201 -5 run function rlk:room/prop/p_grass
execute positioned 37 201 -10 run function rlk:room/prop/p_wildflower
execute positioned 31 201 -12 run function rlk:room/prop/p_dandelion
execute positioned 33 201 -11 run function rlk:room/prop/p_wildflower
execute positioned 26 202 -15 run function rlk:room/prop/p_dandelion
setblock 29 207 -3 minecraft:short_grass keep
setblock 29 207 -2 minecraft:azalea_leaves[persistent=true] keep
setblock 30 208 -17 minecraft:azalea_leaves[persistent=true] keep
setblock 30 207 -2 minecraft:azalea_leaves[persistent=true] keep
setblock 31 208 -17 minecraft:azalea_leaves[persistent=true] keep
setblock 31 207 -3 minecraft:azalea_leaves[persistent=true] keep
setblock 31 207 -2 minecraft:short_grass keep
setblock 32 207 -3 minecraft:azalea_leaves[persistent=true] keep
