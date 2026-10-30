# 구역 건설 (normal13_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 1 201 -39 18 210 -22 minecraft:air
fill 1 209 -39 18 209 -22 minecraft:light[level=15]
fill 5 200 -31 9 200 -28 minecraft:coarse_dirt
fill 0 208 -27 0 210 -26 minecraft:cobblestone
fill 0 202 -33 0 202 -29 minecraft:granite
fill 0 207 -34 0 208 -29 minecraft:andesite
fill 0 209 -37 0 210 -32 minecraft:oak_leaves[persistent=true]
fill 0 206 -39 0 207 -37 minecraft:tuff
fill 0 202 -27 0 202 -24 minecraft:mossy_cobblestone
fill 19 201 -32 19 204 -31 minecraft:mossy_cobblestone
fill 19 205 -23 19 205 -22 minecraft:andesite
fill 19 203 -25 19 206 -23 minecraft:moss_block
fill 19 206 -32 19 208 -30 minecraft:cobblestone
fill 19 207 -25 19 208 -21 minecraft:moss_block
fill 5 210 -40 8 210 -40 minecraft:oak_leaves[persistent=true]
fill 9 208 -40 12 210 -40 minecraft:tuff
fill 3 210 -40 3 210 -40 minecraft:oak_leaves[persistent=true]
fill 6 210 -21 7 210 -21 minecraft:oak_leaves[persistent=true]
fill 2 208 -21 3 208 -21 minecraft:andesite
fill 9 210 -21 9 210 -21 minecraft:oak_leaves[persistent=true]
fill 12 206 -21 17 209 -21 minecraft:granite
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 1 210 -39 18 210 -22 minecraft:air
fill 15 201 -33 18 201 -32 minecraft:podzol
fill 15 201 -31 17 201 -31 minecraft:podzol
fill 15 201 -30 16 201 -30 minecraft:podzol
fill 15 201 -29 15 201 -27 minecraft:podzol
fill 16 201 -26 16 201 -22 minecraft:podzol
fill 18 201 -22 18 201 -22 minecraft:podzol
fill 17 201 -30 17 201 -22 minecraft:dirt
fill 17 202 -30 17 202 -22 minecraft:podzol
fill 16 201 -29 16 201 -27 minecraft:dirt
fill 16 202 -29 16 202 -27 minecraft:podzol
fill 18 201 -25 18 201 -23 minecraft:dirt
fill 18 202 -25 18 202 -23 minecraft:podzol
fill 18 201 -28 18 207 -27 minecraft:andesite
fill 18 208 -28 18 208 -27 minecraft:podzol
fill 18 201 -31 18 207 -29 minecraft:stone
fill 18 208 -31 18 208 -29 minecraft:podzol
fill 18 201 -26 18 207 -26 minecraft:stone
fill 18 208 -26 18 208 -26 minecraft:podzol
execute positioned 15 201 -35 run function rlk:room/prop/p_boulder
execute positioned 4 201 -24 run function rlk:room/prop/p_grass
execute positioned 16 202 -32 run function rlk:room/prop/p_wildflower
execute positioned 13 201 -28 run function rlk:room/prop/p_wildflower
execute positioned 13 201 -29 run function rlk:room/prop/p_wildflower
execute positioned 4 201 -27 run function rlk:room/prop/p_dandelion
execute positioned 3 201 -37 run function rlk:room/prop/p_grass
setblock 18 209 -31 minecraft:short_grass keep
setblock 18 209 -30 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 -29 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 -28 minecraft:azalea_leaves[persistent=true] keep
setblock 18 209 -26 minecraft:short_grass keep
