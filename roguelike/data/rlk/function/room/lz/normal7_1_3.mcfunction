# 구역 건설 (normal7_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 2 200 15 6 200 17 minecraft:moss_block
fill 2 200 6 6 200 9 minecraft:moss_block
fill 3 200 12 6 200 14 minecraft:moss_block
fill 3 200 8 6 200 9 minecraft:rooted_dirt
fill 0 207 16 0 208 17 minecraft:moss_block
fill 0 204 2 0 207 7 minecraft:andesite
fill 0 209 6 0 210 8 minecraft:oak_leaves[persistent=true]
fill 19 204 8 19 206 8 minecraft:tuff
fill 19 206 5 19 209 10 minecraft:mossy_cobblestone
fill 19 206 14 19 207 14 minecraft:moss_block
fill 5 206 0 5 209 0 minecraft:andesite
fill 14 203 0 15 205 0 minecraft:mossy_cobblestone
fill 15 209 0 16 210 0 minecraft:moss_block
fill 2 204 0 7 204 0 minecraft:mossy_cobblestone
fill 17 204 0 18 204 0 minecraft:moss_block
fill 2 207 19 3 209 19 minecraft:cobblestone
fill 14 206 19 19 207 19 minecraft:granite
fill 9 204 19 11 206 19 minecraft:cobblestone
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 3 201 1 3 201 3 minecraft:podzol
fill 1 201 3 2 201 3 minecraft:podzol
fill 2 201 1 2 201 2 minecraft:dirt
fill 2 202 1 2 202 2 minecraft:podzol
fill 1 201 2 1 201 2 minecraft:dirt
fill 1 202 2 1 202 2 minecraft:podzol
fill 1 201 1 1 202 1 minecraft:dirt
fill 1 203 1 1 203 1 minecraft:podzol
fill 18 201 10 18 207 11 minecraft:andesite
fill 18 208 10 18 208 11 minecraft:podzol
fill 17 201 8 18 207 9 minecraft:stone
fill 17 208 8 18 208 9 minecraft:podzol
fill 17 201 10 17 207 11 minecraft:stone
fill 17 208 10 17 208 11 minecraft:podzol
execute positioned 17 201 14 run function rlk:room/prop/p_hay
execute positioned 9 201 4 run function rlk:room/prop/p_crates
execute positioned 18 201 1 run function rlk:room/prop/p_wildflower
execute positioned 18 201 13 run function rlk:room/prop/p_wildflower
execute positioned 3 201 4 run function rlk:room/prop/p_dandelion
execute positioned 10 201 15 run function rlk:room/prop/p_grass
execute positioned 1 204 1 run function rlk:room/prop/p_dandelion
execute positioned 1 202 3 run function rlk:room/prop/p_wildflower
setblock 17 209 10 minecraft:azalea_leaves[persistent=true] keep
setblock 17 209 11 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 8 minecraft:short_grass keep
setblock 18 209 9 minecraft:short_grass keep
setblock 18 209 10 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 11 minecraft:short_grass keep
