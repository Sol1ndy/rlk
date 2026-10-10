# 구역 건설 (first0_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 8 200 17 11 200 18 minecraft:rooted_dirt
fill 0 202 5 0 204 9 minecraft:mossy_cobblestone
fill 0 210 5 0 210 5 minecraft:oak_leaves[persistent=true]
fill 0 204 16 0 205 19 minecraft:andesite
fill 0 207 7 0 209 10 minecraft:moss_block
fill 19 209 13 19 210 18 minecraft:andesite
fill 19 210 17 19 210 17 minecraft:oak_leaves[persistent=true]
fill 19 210 7 19 210 12 minecraft:andesite
fill 19 201 8 19 202 9 minecraft:mossy_cobblestone
fill 5 203 0 5 205 0 minecraft:moss_block
fill 5 205 0 9 205 0 minecraft:cobblestone
fill 0 210 0 2 210 0 minecraft:oak_leaves[persistent=true]
fill 5 209 0 7 210 0 minecraft:oak_leaves[persistent=true]
fill 1 204 0 6 205 0 minecraft:andesite
fill 10 209 0 10 210 0 minecraft:oak_leaves[persistent=true]
fill 13 207 19 16 208 19 minecraft:andesite
fill 10 209 19 11 210 19 minecraft:andesite
fill 11 208 19 16 208 19 minecraft:moss_block
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 1 201 16 3 201 16 minecraft:podzol
fill 3 201 17 3 201 18 minecraft:podzol
fill 1 201 17 2 201 18 minecraft:dirt
fill 1 202 17 2 202 18 minecraft:podzol
fill 18 201 2 18 206 3 minecraft:andesite
fill 18 207 2 18 207 3 minecraft:podzol
fill 16 201 1 18 206 1 minecraft:stone
fill 16 207 1 18 207 1 minecraft:podzol
fill 16 201 2 17 206 3 minecraft:stone
fill 16 207 2 17 207 3 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:andesite
fill 12 208 3 12 208 3 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:stone
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:stone
fill 12 208 4 12 208 4 minecraft:podzol
execute positioned 17 201 9 run function rlk:room/prop/p_boulder
execute positioned 15 201 13 run function rlk:room/prop/p_oak_big
execute positioned 4 201 3 run function rlk:room/prop/p_crates
execute positioned 9 201 5 run function rlk:room/prop/p_lantern
execute positioned 8 201 3 run function rlk:room/prop/p_lantern
execute positioned 9 201 8 run function rlk:room/prop/p_litter
execute positioned 17 201 17 run function rlk:room/prop/p_litter
execute positioned 12 201 1 run function rlk:room/prop/p_wildflower
execute positioned 8 201 3 run function rlk:room/prop/p_dandelion
execute positioned 9 201 17 run function rlk:room/prop/p_wildflower
execute positioned 6 201 7 run function rlk:room/prop/p_grass
execute positioned 13 201 3 run function rlk:room/prop/p_grass
execute positioned 12 201 11 run function rlk:room/prop/p_litter
execute positioned 4 201 12 run function rlk:room/prop/p_grass
setblock 11 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock 11 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock 12 209 4 minecraft:short_grass keep
setblock 16 208 2 minecraft:short_grass keep
setblock 17 208 1 minecraft:azalea_leaves[persistent=true] keep
setblock 17 208 2 minecraft:azalea_leaves[persistent=true] keep
setblock 18 208 1 minecraft:short_grass keep
setblock 18 208 3 minecraft:short_grass keep
