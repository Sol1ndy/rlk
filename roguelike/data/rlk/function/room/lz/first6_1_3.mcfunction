# 구역 건설 (first6_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 14 200 -17 15 200 -14 minecraft:rooted_dirt
fill 11 200 -18 14 200 -16 minecraft:gravel
fill 0 205 -4 0 208 -1 minecraft:mossy_cobblestone
fill 0 208 -14 0 209 -12 minecraft:moss_block
fill 0 206 -5 0 206 -1 minecraft:tuff
fill 0 201 -11 0 204 -11 minecraft:granite
fill 19 207 -19 19 207 -18 minecraft:andesite
fill 19 207 -16 19 207 -11 minecraft:cobblestone
fill 19 209 -3 19 210 -3 minecraft:andesite
fill 12 206 -20 12 207 -20 minecraft:granite
fill 10 209 -20 12 210 -20 minecraft:moss_block
fill 7 202 -20 9 203 -20 minecraft:tuff
fill 1 207 -20 1 209 -20 minecraft:moss_block
fill 1 210 -20 6 210 -20 minecraft:oak_leaves[persistent=true]
fill 19 208 -1 19 210 -1 minecraft:tuff
fill 0 207 -1 0 210 -1 minecraft:moss_block
fill 4 210 -1 4 210 -1 minecraft:oak_leaves[persistent=true]
fill 12 208 -1 16 208 -1 minecraft:mossy_cobblestone
fill 15 209 -1 16 210 -1 minecraft:oak_leaves[persistent=true]
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -19 4 201 -19 minecraft:podzol
fill 4 201 -18 4 201 -18 minecraft:podzol
fill 3 201 -15 4 201 -15 minecraft:podzol
fill 1 201 -14 3 201 -14 minecraft:podzol
fill 1 201 -13 1 201 -13 minecraft:podzol
fill 1 201 -19 2 201 -15 minecraft:dirt
fill 1 202 -19 2 202 -15 minecraft:podzol
fill 3 201 -18 3 201 -16 minecraft:dirt
fill 3 202 -18 3 202 -16 minecraft:podzol
fill 8 201 -2 12 205 -2 minecraft:stone
fill 8 206 -2 12 206 -2 minecraft:podzol
fill 9 201 -17 10 207 -16 minecraft:andesite
fill 9 208 -17 10 208 -16 minecraft:podzol
fill 4 201 -17 5 207 -16 minecraft:stone
fill 4 208 -17 5 208 -16 minecraft:podzol
execute positioned 17 201 -17 run function rlk:room/prop/p_crates
execute positioned 17 201 -4 run function rlk:room/prop/p_boulder_s
execute positioned 6 201 -5 run function rlk:room/prop/p_grass
execute positioned 2 201 -8 run function rlk:room/prop/p_litter
execute positioned 4 201 -14 run function rlk:room/prop/p_dandelion
execute positioned 13 201 -19 run function rlk:room/prop/p_grass
execute positioned 5 201 -10 run function rlk:room/prop/p_wildflower
execute positioned 14 201 -15 run function rlk:room/prop/p_litter
execute positioned 18 201 -14 run function rlk:room/prop/p_dandelion
setblock 5 209 -17 minecraft:short_grass keep
setblock 5 209 -16 minecraft:azalea_leaves[persistent=true] keep
setblock 8 207 -2 minecraft:azalea_leaves[persistent=true] keep
setblock 9 207 -2 minecraft:short_grass keep
setblock 10 209 -16 minecraft:azalea_leaves[persistent=true] keep
setblock 11 207 -2 minecraft:azalea_leaves[persistent=true] keep
setblock 12 207 -2 minecraft:azalea_leaves[persistent=true] keep
