# 구역 건설 (normal27_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 1 201 -39 18 210 -22 minecraft:air
fill 1 209 -39 18 209 -22 minecraft:light[level=15]
fill 10 200 -26 13 200 -25 minecraft:moss_block
fill 11 200 -25 13 200 -22 minecraft:coarse_dirt
fill 0 210 -35 0 210 -34 minecraft:cherry_leaves[persistent=true]
fill 0 206 -25 0 209 -25 minecraft:cobblestone
fill 0 210 -31 0 210 -28 minecraft:cherry_leaves[persistent=true]
fill 0 203 -29 0 203 -24 minecraft:moss_block
fill 0 210 -23 0 210 -21 minecraft:cherry_leaves[persistent=true]
fill 19 207 -33 19 207 -32 minecraft:calcite
fill 19 201 -40 19 210 -40 minecraft:stripped_dark_oak_log
fill 19 202 -27 19 204 -24 minecraft:andesite
fill 19 206 -37 19 207 -37 minecraft:calcite
fill 19 201 -34 19 210 -34 minecraft:stripped_dark_oak_log
fill 4 203 -40 7 204 -40 minecraft:tuff
fill 0 210 -40 4 210 -40 minecraft:cherry_leaves[persistent=true]
fill 10 201 -40 15 201 -40 minecraft:moss_block
fill 3 209 -40 6 210 -40 minecraft:andesite
fill 3 210 -40 8 210 -40 minecraft:cherry_leaves[persistent=true]
fill 7 209 -40 9 210 -40 minecraft:calcite
fill 11 204 -21 14 207 -21 minecraft:tuff
fill 15 210 -21 15 210 -21 minecraft:cherry_leaves[persistent=true]
fill 9 205 -21 10 205 -21 minecraft:andesite
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
fill 3 201 -31 4 206 -30 minecraft:stone_bricks
fill 3 207 -31 4 207 -30 minecraft:podzol
fill 1 201 -22 1 207 -22 minecraft:mossy_stone_bricks
fill 1 208 -22 1 208 -22 minecraft:podzol
fill 1 201 -27 1 207 -23 minecraft:stone_bricks
fill 1 208 -27 1 208 -23 minecraft:podzol
execute positioned 11 201 -25 run function rlk:room/prop/i_petal
execute positioned 2 202 -30 run function rlk:room/prop/i_grass
execute positioned 11 201 -38 run function rlk:room/prop/i_flower
execute positioned 7 201 -27 run function rlk:room/prop/i_flower
execute positioned 7 201 -27 run function rlk:room/prop/i_grass
execute positioned 7 201 -25 run function rlk:room/prop/i_petal
execute positioned 15 201 -23 run function rlk:room/prop/i_flower
execute positioned 15 201 -39 run function rlk:room/prop/i_grass
execute positioned 3 202 -26 run function rlk:room/prop/i_grass
setblock 1 209 -27 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 -25 minecraft:short_grass keep
setblock 1 209 -24 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 -23 minecraft:short_grass keep
setblock 3 208 -30 minecraft:cherry_leaves[persistent=true] keep
setblock 4 208 -31 minecraft:short_grass keep
