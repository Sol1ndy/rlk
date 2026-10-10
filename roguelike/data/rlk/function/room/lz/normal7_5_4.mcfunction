# 구역 건설 (normal7_5, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:stone
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 9 200 33 12 200 36 minecraft:moss_block
fill 1 200 24 5 200 25 minecraft:coarse_dirt
fill 0 210 32 0 210 35 minecraft:cherry_leaves[persistent=true]
fill 0 209 22 0 210 27 minecraft:cherry_leaves[persistent=true]
fill 0 204 36 0 207 38 minecraft:calcite
fill 0 201 29 0 210 29 minecraft:stripped_dark_oak_log
fill 0 209 35 0 210 35 minecraft:cherry_leaves[persistent=true]
fill 0 210 22 0 210 27 minecraft:cherry_leaves[persistent=true]
fill 19 210 22 19 210 24 minecraft:calcite
fill 19 210 29 19 210 30 minecraft:cherry_leaves[persistent=true]
fill 19 205 22 19 205 25 minecraft:andesite
fill 19 209 23 19 210 25 minecraft:cherry_leaves[persistent=true]
fill 19 206 26 19 208 28 minecraft:andesite
fill 19 206 27 19 207 32 minecraft:calcite
fill 12 210 20 15 210 20 minecraft:cherry_leaves[persistent=true]
fill 14 210 20 14 210 20 minecraft:calcite
fill 12 205 20 16 206 20 minecraft:calcite
fill 17 201 20 17 210 20 minecraft:stripped_dark_oak_log
fill 7 201 20 8 203 20 minecraft:andesite
fill 9 205 39 10 208 39 minecraft:andesite
fill 13 210 39 15 210 39 minecraft:cherry_leaves[persistent=true]
fill 3 208 39 4 210 39 minecraft:moss_block
fill 3 209 39 8 210 39 minecraft:cherry_leaves[persistent=true]
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
fill 3 201 29 4 207 29 minecraft:mossy_stone_bricks
fill 3 208 29 4 208 29 minecraft:podzol
fill 1 201 33 2 207 33 minecraft:mossy_stone_bricks
fill 1 208 33 2 208 33 minecraft:podzol
fill 3 201 34 3 207 37 minecraft:mossy_stone_bricks
fill 3 208 34 3 208 37 minecraft:podzol
fill 1 201 38 2 207 38 minecraft:mossy_stone_bricks
fill 1 208 38 2 208 38 minecraft:podzol
fill 3 201 30 4 207 30 minecraft:stone_bricks
fill 3 208 30 4 208 30 minecraft:podzol
fill 3 201 33 3 207 33 minecraft:stone_bricks
fill 3 208 33 3 208 33 minecraft:podzol
fill 1 201 34 2 207 37 minecraft:stone_bricks
fill 1 208 34 2 208 37 minecraft:podzol
fill 3 201 38 3 207 38 minecraft:stone_bricks
fill 3 208 38 3 208 38 minecraft:podzol
execute positioned 8 201 36 run function rlk:room/prop/i_wall_x
execute positioned 15 201 32 run function rlk:room/prop/i_grass
execute positioned 10 201 33 run function rlk:room/prop/i_petal
execute positioned 3 203 31 run function rlk:room/prop/i_petal
execute positioned 6 201 33 run function rlk:room/prop/i_grass
execute positioned 10 201 35 run function rlk:room/prop/i_grass
execute positioned 5 201 21 run function rlk:room/prop/i_grass
execute positioned 15 201 31 run function rlk:room/prop/i_petal
setblock 1 209 33 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 35 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 37 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 38 minecraft:short_grass keep
setblock 2 209 34 minecraft:short_grass keep
setblock 2 209 35 minecraft:short_grass keep
setblock 2 209 36 minecraft:cherry_leaves[persistent=true] keep
setblock 2 209 38 minecraft:short_grass keep
setblock 3 209 30 minecraft:cherry_leaves[persistent=true] keep
setblock 3 209 34 minecraft:cherry_leaves[persistent=true] keep
setblock 3 209 36 minecraft:short_grass keep
setblock 3 209 37 minecraft:short_grass keep
