# 구역 건설 (root3_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 34 200 -16 37 200 -15 minecraft:moss_block
fill 25 200 -7 26 200 -5 minecraft:coarse_dirt
fill 26 200 -16 27 200 -14 minecraft:rooted_dirt
fill 20 203 -13 20 204 -9 minecraft:moss_block
fill 20 207 -6 20 209 -3 minecraft:moss_block
fill 20 210 -17 20 210 -16 minecraft:oak_leaves[persistent=true]
fill 20 203 -15 20 205 -13 minecraft:moss_block
fill 39 208 -4 39 210 -4 minecraft:mossy_cobblestone
fill 39 201 -11 39 203 -10 minecraft:andesite
fill 39 205 -9 39 206 -4 minecraft:moss_block
fill 39 205 -10 39 207 -5 minecraft:andesite
fill 34 207 -20 37 209 -20 minecraft:andesite
fill 31 208 -20 32 210 -20 minecraft:moss_block
fill 20 206 -20 22 208 -20 minecraft:moss_block
fill 21 201 -20 23 201 -20 minecraft:andesite
fill 20 202 -20 22 205 -20 minecraft:cobblestone
fill 36 201 -1 38 201 -1 minecraft:mossy_cobblestone
fill 36 208 -1 37 208 -1 minecraft:cobblestone
fill 23 204 -1 27 207 -1 minecraft:moss_block
fill 33 202 -1 36 204 -1 minecraft:cobblestone
fill 25 206 -1 29 206 -1 minecraft:mossy_cobblestone
fill 28 206 -1 29 209 -1 minecraft:andesite
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 38 201 -8 38 201 -3 minecraft:podzol
fill 35 201 -6 37 201 -6 minecraft:podzol
fill 31 201 -5 34 201 -5 minecraft:podzol
fill 37 201 -5 37 201 -3 minecraft:podzol
fill 30 201 -4 31 201 -4 minecraft:podzol
fill 31 201 -3 31 201 -2 minecraft:podzol
fill 32 201 -2 32 201 -2 minecraft:podzol
fill 35 201 -5 36 201 -3 minecraft:dirt
fill 35 202 -5 36 202 -3 minecraft:podzol
fill 32 201 -4 34 201 -3 minecraft:dirt
fill 32 202 -4 34 202 -3 minecraft:podzol
fill 33 201 -2 35 201 -2 minecraft:dirt
fill 33 202 -2 35 202 -2 minecraft:podzol
fill 36 201 -2 38 206 -2 minecraft:andesite
fill 36 207 -2 38 207 -2 minecraft:podzol
fill 28 201 -17 29 207 -16 minecraft:andesite
fill 28 208 -17 29 208 -16 minecraft:podzol
execute positioned 32 201 -17 run function rlk:room/prop/p_pillar_ruin
execute positioned 34 201 -16 run function rlk:room/prop/p_hay
execute positioned 23 201 -4 run function rlk:room/prop/p_dandelion
execute positioned 33 201 -7 run function rlk:room/prop/p_wildflower
execute positioned 23 201 -17 run function rlk:room/prop/p_dandelion
execute positioned 33 201 -12 run function rlk:room/prop/p_litter
execute positioned 23 201 -18 run function rlk:room/prop/p_grass
execute positioned 22 201 -3 run function rlk:room/prop/p_grass
execute positioned 30 201 -17 run function rlk:room/prop/p_wildflower
execute positioned 36 201 -11 run function rlk:room/prop/p_grass
setblock 28 209 -17 minecraft:short_grass keep
setblock 28 209 -16 minecraft:azalea_leaves[persistent=true] keep
setblock 29 209 -16 minecraft:short_grass keep
setblock 37 208 -2 minecraft:short_grass keep
setblock 38 208 -2 minecraft:azalea_leaves[persistent=true] keep
