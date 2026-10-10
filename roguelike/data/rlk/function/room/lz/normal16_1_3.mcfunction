# 구역 건설 (normal16_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 10 200 8 13 200 10 minecraft:gravel
fill 6 200 6 8 200 9 minecraft:moss_block
fill 0 201 13 0 202 16 minecraft:mossy_cobblestone
fill 0 209 8 0 210 8 minecraft:moss_block
fill 0 208 15 0 208 16 minecraft:moss_block
fill 19 205 16 19 207 17 minecraft:moss_block
fill 19 210 4 19 210 5 minecraft:andesite
fill 19 209 2 19 210 2 minecraft:moss_block
fill 19 210 6 19 210 11 minecraft:oak_leaves[persistent=true]
fill 19 208 1 19 210 6 minecraft:moss_block
fill 19 203 16 19 203 19 minecraft:andesite
fill 8 209 0 10 210 0 minecraft:oak_leaves[persistent=true]
fill 19 210 0 19 210 0 minecraft:andesite
fill 4 201 0 9 202 0 minecraft:andesite
fill 13 209 0 14 210 0 minecraft:oak_leaves[persistent=true]
fill 1 204 19 2 206 19 minecraft:granite
fill 9 202 19 11 202 19 minecraft:cobblestone
fill 2 201 19 5 204 19 minecraft:mossy_cobblestone
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 13 201 1 14 201 5 minecraft:podzol
fill 1 201 4 4 201 5 minecraft:podzol
fill 4 201 6 5 201 13 minecraft:podzol
fill 15 201 6 18 201 6 minecraft:podzol
fill 15 201 7 16 201 7 minecraft:podzol
fill 1 201 14 4 201 14 minecraft:podzol
fill 1 201 15 3 201 15 minecraft:podzol
fill 7 201 15 18 201 16 minecraft:podzol
fill 6 201 16 6 201 18 minecraft:podzol
fill 15 201 1 18 201 5 minecraft:dirt
fill 15 202 1 18 202 5 minecraft:podzol
fill 1 201 6 3 201 13 minecraft:dirt
fill 1 202 6 3 202 13 minecraft:podzol
fill 7 201 17 18 201 18 minecraft:dirt
fill 7 202 17 18 202 18 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:andesite
fill 12 208 3 12 208 3 minecraft:podzol
fill 18 201 10 18 207 10 minecraft:andesite
fill 18 208 10 18 208 10 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:stone
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:stone
fill 12 208 4 12 208 4 minecraft:podzol
fill 17 201 7 18 207 9 minecraft:stone
fill 17 208 7 18 208 9 minecraft:podzol
fill 17 201 10 17 207 10 minecraft:stone
fill 17 208 10 17 208 10 minecraft:podzol
execute positioned 6 201 3 run function rlk:room/prop/p_ruin_x
execute positioned 4 201 1 run function rlk:room/prop/p_wildflower
execute positioned 13 202 4 run function rlk:room/prop/p_grass
execute positioned 3 201 2 run function rlk:room/prop/p_grass
execute positioned 4 202 8 run function rlk:room/prop/p_dandelion
execute positioned 1 203 8 run function rlk:room/prop/p_wildflower
execute positioned 2 202 14 run function rlk:room/prop/p_grass
setblock 11 209 3 minecraft:short_grass keep
setblock 17 209 8 minecraft:short_grass keep
setblock 17 209 9 minecraft:azalea_leaves[persistent=true] keep
setblock 17 209 10 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 7 minecraft:short_grass keep
setblock 18 209 8 minecraft:short_grass keep
setblock 18 209 10 minecraft:azalea_leaves[persistent=true] keep
