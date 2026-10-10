# 구역 건설 (normal7_5, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:stone
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 12 200 22 16 200 24 minecraft:gravel
fill 12 200 27 13 200 29 minecraft:coarse_dirt
fill 0 209 23 0 210 28 minecraft:mossy_cobblestone
fill 0 209 23 0 210 24 minecraft:moss_block
fill 0 203 28 0 203 32 minecraft:andesite
fill 0 204 26 0 204 31 minecraft:mossy_cobblestone
fill 19 201 36 19 203 37 minecraft:andesite
fill 19 204 29 19 205 34 minecraft:cobblestone
fill 19 205 26 19 206 26 minecraft:andesite
fill 19 207 37 19 207 37 minecraft:cobblestone
fill 19 204 34 19 207 35 minecraft:granite
fill 3 209 20 5 210 20 minecraft:oak_leaves[persistent=true]
fill 12 203 20 14 204 20 minecraft:mossy_cobblestone
fill 11 209 20 12 210 20 minecraft:oak_leaves[persistent=true]
fill 9 207 20 12 208 20 minecraft:moss_block
fill 12 209 39 13 210 39 minecraft:tuff
fill 14 209 39 19 210 39 minecraft:mossy_cobblestone
fill 15 201 39 17 204 39 minecraft:tuff
fill 9 209 39 12 210 39 minecraft:oak_leaves[persistent=true]
fill 2 209 39 3 210 39 minecraft:oak_leaves[persistent=true]
fill 2 202 39 4 203 39 minecraft:granite
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 3 201 27 5 201 28 minecraft:podzol
fill 1 201 28 2 201 29 minecraft:podzol
fill 5 201 29 5 201 34 minecraft:podzol
fill 1 201 30 1 201 30 minecraft:podzol
fill 6 201 35 8 201 35 minecraft:podzol
fill 4 201 36 7 201 36 minecraft:podzol
fill 13 201 36 18 201 36 minecraft:podzol
fill 4 201 37 5 201 37 minecraft:podzol
fill 13 201 37 14 201 38 minecraft:podzol
fill 2 201 30 2 201 32 minecraft:dirt
fill 2 202 30 2 202 32 minecraft:podzol
fill 1 201 31 1 201 32 minecraft:dirt
fill 1 202 31 1 202 32 minecraft:podzol
fill 3 201 31 4 201 32 minecraft:dirt
fill 3 202 31 4 202 32 minecraft:podzol
fill 4 201 33 4 201 35 minecraft:dirt
fill 4 202 33 4 202 35 minecraft:podzol
fill 5 201 35 5 201 35 minecraft:dirt
fill 5 202 35 5 202 35 minecraft:podzol
fill 15 201 37 18 201 38 minecraft:dirt
fill 15 202 37 18 202 38 minecraft:podzol
fill 3 201 29 4 207 29 minecraft:andesite
fill 3 208 29 4 208 29 minecraft:podzol
fill 1 201 33 2 207 33 minecraft:andesite
fill 1 208 33 2 208 33 minecraft:podzol
fill 3 201 34 3 207 37 minecraft:andesite
fill 3 208 34 3 208 37 minecraft:podzol
fill 1 201 38 2 207 38 minecraft:andesite
fill 1 208 38 2 208 38 minecraft:podzol
fill 3 201 30 4 207 30 minecraft:stone
fill 3 208 30 4 208 30 minecraft:podzol
fill 3 201 33 3 207 33 minecraft:stone
fill 3 208 33 3 208 33 minecraft:podzol
fill 1 201 34 2 207 37 minecraft:stone
fill 1 208 34 2 208 37 minecraft:podzol
fill 3 201 38 3 207 38 minecraft:stone
fill 3 208 38 3 208 38 minecraft:podzol
execute positioned 1 201 23 run function rlk:room/prop/p_hay
execute positioned 16 203 38 run function rlk:room/prop/p_ruin_x
execute positioned 4 201 26 run function rlk:room/prop/p_wildflower
execute positioned 11 201 34 run function rlk:room/prop/p_dandelion
execute positioned 11 201 25 run function rlk:room/prop/p_litter
execute positioned 5 202 29 run function rlk:room/prop/p_wildflower
execute positioned 13 201 27 run function rlk:room/prop/p_dandelion
execute positioned 10 201 22 run function rlk:room/prop/p_litter
setblock 1 209 33 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 34 minecraft:short_grass keep
setblock 1 209 35 minecraft:short_grass keep
setblock 1 209 37 minecraft:short_grass keep
setblock 1 209 38 minecraft:azalea_leaves[persistent=true] keep
setblock 2 209 35 minecraft:short_grass keep
setblock 2 209 36 minecraft:short_grass keep
setblock 2 209 38 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 29 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 30 minecraft:short_grass keep
setblock 3 209 33 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 34 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 35 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 36 minecraft:azalea_leaves[persistent=true] keep
setblock 3 209 37 minecraft:short_grass keep
setblock 4 209 29 minecraft:azalea_leaves[persistent=true] keep
setblock 4 209 30 minecraft:azalea_leaves[persistent=true] keep
