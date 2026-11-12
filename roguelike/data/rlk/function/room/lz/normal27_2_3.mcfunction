# 구역 건설 (normal27_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 1 201 -39 18 210 -22 minecraft:air
fill 1 209 -39 18 209 -22 minecraft:light[level=15]
fill 9 200 -23 13 200 -22 minecraft:rooted_dirt
fill 17 200 -34 18 200 -31 minecraft:rooted_dirt
fill 6 200 -30 7 200 -27 minecraft:rooted_dirt
fill 0 210 -39 0 210 -38 minecraft:oak_leaves[persistent=true]
fill 0 210 -28 0 210 -28 minecraft:oak_leaves[persistent=true]
fill 0 203 -35 0 204 -34 minecraft:granite
fill 0 210 -36 0 210 -36 minecraft:andesite
fill 19 204 -39 19 206 -36 minecraft:tuff
fill 19 201 -32 19 201 -28 minecraft:cobblestone
fill 19 207 -33 19 209 -29 minecraft:tuff
fill 19 206 -34 19 207 -33 minecraft:mossy_cobblestone
fill 3 210 -40 3 210 -40 minecraft:moss_block
fill 1 202 -40 6 205 -40 minecraft:andesite
fill 15 209 -40 16 210 -40 minecraft:oak_leaves[persistent=true]
fill 19 202 -40 19 202 -40 minecraft:andesite
fill 2 207 -21 6 208 -21 minecraft:mossy_cobblestone
fill 10 205 -21 11 207 -21 minecraft:tuff
fill 5 205 -21 7 206 -21 minecraft:tuff
fill 15 210 -21 15 210 -21 minecraft:andesite
fill 6 204 -21 10 205 -21 minecraft:mossy_cobblestone
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 1 210 -39 18 210 -22 minecraft:air
fill 2 201 -30 2 201 -29 minecraft:podzol
fill 1 201 -29 1 201 -29 minecraft:podzol
fill 3 201 -29 4 201 -29 minecraft:podzol
fill 4 201 -28 5 201 -27 minecraft:podzol
fill 3 201 -26 3 201 -23 minecraft:podzol
fill 2 201 -23 2 201 -22 minecraft:podzol
fill 1 201 -28 3 201 -28 minecraft:dirt
fill 1 202 -28 3 202 -28 minecraft:podzol
fill 2 201 -27 3 201 -27 minecraft:dirt
fill 2 202 -27 3 202 -27 minecraft:podzol
fill 2 201 -26 2 201 -24 minecraft:dirt
fill 2 202 -26 2 202 -24 minecraft:podzol
fill 3 201 -31 4 206 -30 minecraft:stone
fill 3 207 -31 4 207 -30 minecraft:podzol
fill 1 201 -22 1 207 -22 minecraft:andesite
fill 1 208 -22 1 208 -22 minecraft:podzol
fill 1 201 -27 1 207 -23 minecraft:stone
fill 1 208 -27 1 208 -23 minecraft:podzol
execute positioned 3 201 -37 run function rlk:room/prop/p_lantern
execute positioned 18 201 -22 run function rlk:room/prop/p_grass
execute positioned 11 201 -32 run function rlk:room/prop/p_wildflower
execute positioned 2 201 -38 run function rlk:room/prop/p_dandelion
execute positioned 13 201 -33 run function rlk:room/prop/p_grass
execute positioned 13 201 -27 run function rlk:room/prop/p_wildflower
execute positioned 11 201 -27 run function rlk:room/prop/p_wildflower
execute positioned 8 201 -31 run function rlk:room/prop/p_wildflower
setblock 1 209 -27 minecraft:short_grass keep
setblock 1 209 -24 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 -23 minecraft:short_grass keep
setblock 1 209 -22 minecraft:short_grass keep
setblock 4 208 -31 minecraft:azalea_leaves[persistent=true] keep
