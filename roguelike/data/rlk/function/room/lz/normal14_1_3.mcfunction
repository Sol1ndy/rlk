# 구역 건설 (normal14_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 0 209 -6 0 210 -3 minecraft:oak_leaves[persistent=true]
fill 0 209 -15 0 210 -10 minecraft:oak_leaves[persistent=true]
fill 0 206 -10 0 208 -9 minecraft:cobblestone
fill 0 203 -10 0 203 -9 minecraft:tuff
fill 0 205 -5 0 208 -4 minecraft:andesite
fill 0 206 -6 0 206 -3 minecraft:andesite
fill 19 204 -9 19 207 -6 minecraft:mossy_cobblestone
fill 19 210 -15 19 210 -13 minecraft:oak_leaves[persistent=true]
fill 19 209 -19 19 210 -19 minecraft:oak_leaves[persistent=true]
fill 5 201 -20 8 203 -20 minecraft:moss_block
fill 0 207 -20 5 209 -20 minecraft:moss_block
fill 2 207 -20 6 209 -20 minecraft:andesite
fill 1 210 -20 5 210 -20 minecraft:andesite
fill 3 204 -20 4 206 -20 minecraft:moss_block
fill 12 208 -1 15 210 -1 minecraft:mossy_cobblestone
fill 2 206 -1 2 209 -1 minecraft:cobblestone
fill 9 209 -1 13 210 -1 minecraft:oak_leaves[persistent=true]
fill 19 207 -1 19 207 -1 minecraft:tuff
fill 0 204 -1 3 207 -1 minecraft:tuff
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 5 201 -19 6 201 -18 minecraft:podzol
fill 6 201 -17 18 201 -17 minecraft:podzol
fill 7 201 -16 18 201 -16 minecraft:podzol
fill 1 201 -4 3 201 -4 minecraft:podzol
fill 3 201 -3 3 201 -2 minecraft:podzol
fill 7 201 -19 18 201 -18 minecraft:dirt
fill 7 202 -19 18 202 -18 minecraft:podzol
fill 1 201 -3 2 201 -2 minecraft:dirt
fill 1 202 -3 2 202 -2 minecraft:podzol
fill 18 201 -4 18 205 -2 minecraft:andesite
fill 18 206 -4 18 206 -2 minecraft:podzol
fill 18 201 -7 18 205 -5 minecraft:stone
fill 18 206 -7 18 206 -5 minecraft:podzol
execute positioned 15 201 -12 run function rlk:room/prop/p_boulder_s
execute positioned 2 201 -14 run function rlk:room/prop/p_grass
execute positioned 10 201 -10 run function rlk:room/prop/p_grass
execute positioned 16 201 -12 run function rlk:room/prop/p_litter
execute positioned 13 201 -5 run function rlk:room/prop/p_litter
execute positioned 14 201 -4 run function rlk:room/prop/p_dandelion
execute positioned 10 201 -8 run function rlk:room/prop/p_wildflower
execute positioned 6 201 -10 run function rlk:room/prop/p_litter
execute positioned 11 201 -15 run function rlk:room/prop/p_litter
execute positioned 4 201 -9 run function rlk:room/prop/p_grass
setblock 18 207 -6 minecraft:short_grass keep
setblock 18 207 -4 minecraft:short_grass keep
setblock 18 207 -3 minecraft:azalea_leaves[persistent=true] keep
setblock 18 207 -2 minecraft:azalea_leaves[persistent=true] keep
