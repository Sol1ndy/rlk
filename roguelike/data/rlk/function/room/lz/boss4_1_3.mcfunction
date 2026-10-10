# 구역 건설 (boss4_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 7 200 -18 8 200 -16 minecraft:gravel
fill 13 200 -11 17 200 -9 minecraft:rooted_dirt
fill 15 200 -11 17 200 -10 minecraft:moss_block
fill 0 201 -13 0 202 -13 minecraft:moss_block
fill 0 206 -3 0 208 -1 minecraft:cobblestone
fill 0 203 -15 0 206 -14 minecraft:mossy_cobblestone
fill 0 210 -13 0 210 -12 minecraft:oak_leaves[persistent=true]
fill 0 202 -8 0 204 -6 minecraft:mossy_cobblestone
fill 19 208 -7 19 210 -2 minecraft:moss_block
fill 19 204 -11 19 205 -7 minecraft:cobblestone
fill 19 207 -7 19 208 -5 minecraft:cobblestone
fill 19 207 -17 19 207 -17 minecraft:granite
fill 19 210 -11 19 210 -6 minecraft:moss_block
fill 19 209 -16 19 210 -12 minecraft:oak_leaves[persistent=true]
fill 4 206 -20 9 209 -20 minecraft:tuff
fill 16 208 -20 17 209 -20 minecraft:moss_block
fill 12 209 -20 17 209 -20 minecraft:cobblestone
fill 8 209 -20 11 210 -20 minecraft:oak_leaves[persistent=true]
fill 0 206 -20 4 208 -20 minecraft:cobblestone
fill 0 203 -20 1 206 -20 minecraft:cobblestone
fill 17 203 -1 18 206 -1 minecraft:tuff
fill 2 204 -1 6 204 -1 minecraft:cobblestone
fill 7 208 -1 10 208 -1 minecraft:andesite
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -11 5 201 -9 minecraft:podzol
fill 2 201 -10 2 201 -7 minecraft:podzol
fill 1 201 -9 1 201 -2 minecraft:podzol
fill 5 201 -8 5 201 -6 minecraft:podzol
fill 6 201 -5 12 201 -5 minecraft:podzol
fill 11 201 -4 12 201 -2 minecraft:podzol
fill 2 201 -3 2 201 -2 minecraft:podzol
fill 10 201 -3 10 201 -2 minecraft:podzol
fill 3 201 -8 4 201 -2 minecraft:dirt
fill 3 202 -8 4 202 -2 minecraft:podzol
fill 2 201 -6 2 201 -4 minecraft:dirt
fill 2 202 -6 2 202 -4 minecraft:podzol
fill 5 201 -5 5 201 -2 minecraft:dirt
fill 5 202 -5 5 202 -2 minecraft:podzol
fill 6 201 -4 10 201 -4 minecraft:dirt
fill 6 202 -4 10 202 -4 minecraft:podzol
fill 6 201 -3 9 201 -2 minecraft:dirt
fill 6 202 -3 9 202 -2 minecraft:podzol
fill 8 201 -19 13 205 -19 minecraft:stone
fill 8 206 -19 13 206 -19 minecraft:podzol
fill 5 201 -17 6 207 -16 minecraft:stone
fill 5 208 -17 6 208 -16 minecraft:podzol
execute positioned 10 201 -16 run function rlk:room/prop/p_pillar_ruin
execute positioned 4 203 -5 run function rlk:room/prop/p_crates
execute positioned 16 201 -13 run function rlk:room/prop/p_wildflower
execute positioned 3 201 -16 run function rlk:room/prop/p_wildflower
execute positioned 16 201 -19 run function rlk:room/prop/p_wildflower
execute positioned 2 201 -11 run function rlk:room/prop/p_wildflower
execute positioned 3 201 -15 run function rlk:room/prop/p_litter
execute positioned 8 201 -14 run function rlk:room/prop/p_grass
execute positioned 4 201 -17 run function rlk:room/prop/p_wildflower
execute positioned 11 201 -13 run function rlk:room/prop/p_grass
execute positioned 14 201 -6 run function rlk:room/prop/p_grass
setblock 5 209 -17 minecraft:azalea_leaves[persistent=true] keep
setblock 6 209 -17 minecraft:azalea_leaves[persistent=true] keep
setblock 6 209 -16 minecraft:short_grass keep
setblock 8 207 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 9 207 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 10 207 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 12 207 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 13 207 -19 minecraft:short_grass keep
