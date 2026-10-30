# 구역 건설 (normal13_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 6 200 -13 8 200 -11 minecraft:coarse_dirt
fill 9 200 -15 12 200 -14 minecraft:gravel
fill 4 200 -18 6 200 -15 minecraft:packed_mud
fill 0 204 -12 0 206 -8 minecraft:moss_block
fill 0 209 -8 0 210 -5 minecraft:cherry_leaves[persistent=true]
fill 0 210 -14 0 210 -13 minecraft:cherry_leaves[persistent=true]
fill 0 201 -12 0 210 -12 minecraft:stripped_dark_oak_log
fill 0 203 -5 0 206 -3 minecraft:moss_block
fill 0 201 -19 0 210 -19 minecraft:stripped_dark_oak_log
fill 19 201 -4 19 202 -1 minecraft:moss_block
fill 19 202 -20 19 203 -18 minecraft:andesite
fill 19 206 -18 19 206 -13 minecraft:moss_block
fill 19 201 -1 19 203 -1 minecraft:moss_block
fill 19 202 -6 19 203 -6 minecraft:moss_block
fill 19 210 -19 19 210 -14 minecraft:cherry_leaves[persistent=true]
fill 5 202 -20 6 204 -20 minecraft:cobblestone
fill 3 210 -20 6 210 -20 minecraft:cherry_leaves[persistent=true]
fill 3 202 -20 6 205 -20 minecraft:cobblestone
fill 11 205 -1 15 207 -1 minecraft:calcite
fill 14 208 -1 19 209 -1 minecraft:moss_block
fill 13 205 -1 13 206 -1 minecraft:andesite
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 1 201 -19 3 201 -12 minecraft:podzol
fill 4 201 -14 5 201 -12 minecraft:podzol
fill 1 201 -11 2 201 -3 minecraft:podzol
fill 5 201 -11 5 201 -3 minecraft:podzol
fill 3 201 -9 4 201 -2 minecraft:podzol
fill 6 201 -5 7 201 -4 minecraft:podzol
fill 6 201 -3 6 201 -3 minecraft:podzol
fill 2 201 -2 2 201 -2 minecraft:podzol
fill 3 201 -11 4 207 -11 minecraft:mossy_stone_bricks
fill 3 208 -11 4 208 -11 minecraft:podzol
fill 3 201 -10 4 207 -10 minecraft:stone_bricks
fill 3 208 -10 4 208 -10 minecraft:podzol
execute positioned 4 202 -6 run function rlk:room/prop/i_lantern
execute positioned 14 201 -5 run function rlk:room/prop/i_rock
execute positioned 1 202 -5 run function rlk:room/prop/i_rock
execute positioned 2 202 -7 run function rlk:room/prop/i_petal
execute positioned 10 201 -7 run function rlk:room/prop/i_petal
execute positioned 3 202 -6 run function rlk:room/prop/i_petal
execute positioned 1 202 -5 run function rlk:room/prop/i_flower
execute positioned 9 201 -8 run function rlk:room/prop/i_petal
execute positioned 16 201 -17 run function rlk:room/prop/i_grass
execute positioned 10 201 -11 run function rlk:room/prop/i_flower
execute positioned 8 201 -9 run function rlk:room/prop/i_grass
setblock 3 209 -11 minecraft:cherry_leaves[persistent=true] keep
setblock 3 209 -10 minecraft:short_grass keep
setblock 4 209 -11 minecraft:short_grass keep
setblock 4 209 -10 minecraft:cherry_leaves[persistent=true] keep
