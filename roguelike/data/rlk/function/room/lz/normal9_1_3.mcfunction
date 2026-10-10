# 구역 건설 (normal9_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 4 200 -14 7 200 -11 minecraft:rooted_dirt
fill 5 200 -9 8 200 -7 minecraft:gravel
fill 0 209 -4 0 210 -4 minecraft:moss_block
fill 0 208 -3 0 209 -1 minecraft:mossy_cobblestone
fill 0 202 -4 0 202 -2 minecraft:cobblestone
fill 0 208 -13 0 209 -12 minecraft:tuff
fill 0 209 -10 0 210 -8 minecraft:oak_leaves[persistent=true]
fill 0 209 -7 0 210 -4 minecraft:oak_leaves[persistent=true]
fill 19 201 -13 19 203 -8 minecraft:cobblestone
fill 19 209 -18 19 210 -14 minecraft:mossy_cobblestone
fill 19 209 -11 19 210 -6 minecraft:oak_leaves[persistent=true]
fill 19 209 -18 19 209 -15 minecraft:cobblestone
fill 19 207 -18 19 208 -15 minecraft:mossy_cobblestone
fill 8 210 -20 9 210 -20 minecraft:oak_leaves[persistent=true]
fill 4 205 -20 8 205 -20 minecraft:mossy_cobblestone
fill 12 209 -20 13 210 -20 minecraft:mossy_cobblestone
fill 13 203 -20 18 203 -20 minecraft:cobblestone
fill 4 202 -20 9 205 -20 minecraft:andesite
fill 7 208 -20 9 209 -20 minecraft:andesite
fill 4 209 -1 7 210 -1 minecraft:oak_leaves[persistent=true]
fill 5 210 -1 5 210 -1 minecraft:oak_leaves[persistent=true]
fill 13 202 -1 14 205 -1 minecraft:moss_block
fill 10 206 -1 15 206 -1 minecraft:andesite
fill 8 209 -1 11 210 -1 minecraft:granite
fill 8 202 -1 13 203 -1 minecraft:moss_block
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 5 201 -6 5 201 -5 minecraft:podzol
fill 4 201 -5 4 201 -2 minecraft:podzol
fill 6 201 -5 13 201 -5 minecraft:podzol
fill 3 201 -4 3 201 -2 minecraft:podzol
fill 10 201 -4 16 201 -2 minecraft:podzol
fill 17 201 -3 17 201 -2 minecraft:podzol
fill 5 201 -4 9 201 -2 minecraft:dirt
fill 5 202 -4 9 202 -2 minecraft:podzol
fill 1 201 -6 2 205 -5 minecraft:andesite
fill 1 206 -6 2 206 -5 minecraft:podzol
fill 1 201 -7 2 205 -7 minecraft:stone
fill 1 206 -7 2 206 -7 minecraft:podzol
fill 1 201 -4 2 205 -2 minecraft:stone
fill 1 206 -4 2 206 -2 minecraft:podzol
execute positioned 4 201 -8 run function rlk:room/prop/p_crates
execute positioned 5 201 -11 run function rlk:room/prop/p_lantern
execute positioned 8 202 -5 run function rlk:room/prop/p_wildflower
execute positioned 11 202 -5 run function rlk:room/prop/p_wildflower
execute positioned 6 201 -12 run function rlk:room/prop/p_grass
execute positioned 13 201 -10 run function rlk:room/prop/p_wildflower
execute positioned 17 202 -2 run function rlk:room/prop/p_litter
execute positioned 3 201 -14 run function rlk:room/prop/p_wildflower
execute positioned 17 201 -7 run function rlk:room/prop/p_grass
execute positioned 11 201 -7 run function rlk:room/prop/p_grass
setblock 1 207 -7 minecraft:short_grass keep
setblock 1 207 -6 minecraft:short_grass keep
setblock 1 207 -5 minecraft:short_grass keep
setblock 1 207 -2 minecraft:short_grass keep
setblock 2 207 -6 minecraft:short_grass keep
setblock 2 207 -4 minecraft:short_grass keep
setblock 2 207 -3 minecraft:short_grass keep
setblock 2 207 -2 minecraft:azalea_leaves[persistent=true] keep
