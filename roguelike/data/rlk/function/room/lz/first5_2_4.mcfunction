# 구역 건설 (first5_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:podzol
fill 20 201 0 39 210 19 minecraft:stone
fill 21 201 1 38 210 18 minecraft:air
fill 21 209 1 38 209 18 minecraft:light[level=15]
fill 24 200 11 25 200 14 minecraft:moss_block
fill 25 200 7 28 200 10 minecraft:packed_mud
fill 24 200 11 28 200 12 minecraft:packed_mud
fill 20 204 8 20 206 10 minecraft:cobblestone
fill 20 208 13 20 210 14 minecraft:tuff
fill 20 204 1 20 207 6 minecraft:moss_block
fill 20 201 6 20 201 8 minecraft:andesite
fill 39 201 0 39 202 4 minecraft:tuff
fill 39 206 10 39 207 11 minecraft:moss_block
fill 39 204 4 39 207 5 minecraft:andesite
fill 39 209 8 39 210 10 minecraft:cherry_leaves[persistent=true]
fill 25 210 0 25 210 0 minecraft:cobblestone
fill 33 209 0 33 210 0 minecraft:cherry_leaves[persistent=true]
fill 32 209 0 37 210 0 minecraft:cherry_leaves[persistent=true]
fill 26 206 0 27 206 0 minecraft:cobblestone
fill 34 207 0 35 209 0 minecraft:tuff
fill 29 204 0 33 207 0 minecraft:tuff
fill 22 209 19 23 210 19 minecraft:cherry_leaves[persistent=true]
fill 37 202 19 37 204 19 minecraft:cobblestone
fill 30 210 19 32 210 19 minecraft:cherry_leaves[persistent=true]
fill 23 205 19 28 206 19 minecraft:calcite
fill 23 210 19 23 210 19 minecraft:andesite
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 38 210 18 minecraft:air
fill 25 201 1 34 201 1 minecraft:podzol
fill 26 201 2 34 201 2 minecraft:podzol
fill 21 201 3 32 201 3 minecraft:podzol
fill 26 201 4 32 201 5 minecraft:podzol
fill 35 201 4 37 201 4 minecraft:podzol
fill 33 201 5 36 201 5 minecraft:podzol
fill 35 201 6 35 201 6 minecraft:podzol
fill 21 201 1 24 201 2 minecraft:dirt
fill 21 202 1 24 202 2 minecraft:podzol
fill 25 201 2 25 201 2 minecraft:dirt
fill 25 202 2 25 202 2 minecraft:podzol
fill 33 201 4 34 207 4 minecraft:mossy_stone_bricks
fill 33 208 4 34 208 4 minecraft:podzol
fill 35 201 1 38 207 3 minecraft:stone_bricks
fill 35 208 1 38 208 3 minecraft:podzol
fill 33 201 3 34 207 3 minecraft:stone_bricks
fill 33 208 3 34 208 3 minecraft:podzol
execute positioned 29 202 3 run function rlk:room/prop/i_pillar
execute positioned 35 201 8 run function rlk:room/prop/i_bamboo
execute positioned 25 202 3 run function rlk:room/prop/i_bamboo
execute positioned 24 201 13 run function rlk:room/prop/i_petal
execute positioned 28 202 1 run function rlk:room/prop/i_grass
execute positioned 24 201 8 run function rlk:room/prop/i_grass
execute positioned 26 201 16 run function rlk:room/prop/i_petal
execute positioned 21 201 18 run function rlk:room/prop/i_grass
execute positioned 26 201 6 run function rlk:room/prop/i_grass
execute positioned 32 201 6 run function rlk:room/prop/i_petal
execute positioned 24 201 8 run function rlk:room/prop/i_petal
execute positioned 25 201 4 run function rlk:room/prop/i_petal
setblock 33 209 3 minecraft:short_grass keep
setblock 33 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock 34 209 3 minecraft:short_grass keep
setblock 34 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock 36 209 1 minecraft:short_grass keep
setblock 36 209 3 minecraft:cherry_leaves[persistent=true] keep
setblock 37 209 1 minecraft:cherry_leaves[persistent=true] keep
setblock 38 209 1 minecraft:cherry_leaves[persistent=true] keep
setblock 38 209 2 minecraft:short_grass keep
setblock 38 209 3 minecraft:cherry_leaves[persistent=true] keep
