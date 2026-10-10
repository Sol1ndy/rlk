# 구역 건설 (normal9_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 9 200 -19 13 200 -18 minecraft:moss_block
fill 6 200 -12 9 200 -11 minecraft:coarse_dirt
fill 12 200 -9 15 200 -7 minecraft:packed_mud
fill 0 210 -12 0 210 -7 minecraft:cherry_leaves[persistent=true]
fill 0 207 -11 0 208 -7 minecraft:moss_block
fill 0 209 -14 0 210 -13 minecraft:cherry_leaves[persistent=true]
fill 0 209 -17 0 209 -15 minecraft:cobblestone
fill 19 202 -5 19 204 -4 minecraft:moss_block
fill 19 206 -15 19 209 -12 minecraft:tuff
fill 19 201 -3 19 210 -3 minecraft:stripped_dark_oak_log
fill 1 210 -20 5 210 -20 minecraft:andesite
fill 14 203 -20 16 204 -20 minecraft:moss_block
fill 0 201 -20 3 202 -20 minecraft:calcite
fill 9 208 -20 10 208 -20 minecraft:moss_block
fill 6 205 -20 11 206 -20 minecraft:tuff
fill 4 207 -1 9 209 -1 minecraft:cobblestone
fill 7 205 -1 9 206 -1 minecraft:tuff
fill 10 201 -1 10 210 -1 minecraft:stripped_dark_oak_log
fill 4 210 -1 4 210 -1 minecraft:tuff
fill 1 201 -1 1 210 -1 minecraft:stripped_dark_oak_log
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 5 201 -6 5 201 -5 minecraft:podzol
fill 4 201 -5 4 201 -2 minecraft:podzol
fill 6 201 -5 13 201 -5 minecraft:podzol
fill 3 201 -4 3 201 -2 minecraft:podzol
fill 10 201 -4 16 201 -2 minecraft:podzol
fill 17 201 -3 17 201 -2 minecraft:podzol
fill 5 201 -4 9 201 -2 minecraft:dirt
fill 5 202 -4 9 202 -2 minecraft:podzol
fill 1 201 -6 2 205 -5 minecraft:mossy_stone_bricks
fill 1 206 -6 2 206 -5 minecraft:podzol
fill 1 201 -7 2 205 -7 minecraft:stone_bricks
fill 1 206 -7 2 206 -7 minecraft:podzol
fill 1 201 -4 2 205 -2 minecraft:stone_bricks
fill 1 206 -4 2 206 -2 minecraft:podzol
execute positioned 5 201 -10 run function rlk:room/prop/i_sakura
execute positioned 14 201 -13 run function rlk:room/prop/i_petal
execute positioned 14 201 -12 run function rlk:room/prop/i_petal
execute positioned 13 201 -13 run function rlk:room/prop/i_grass
execute positioned 13 201 -9 run function rlk:room/prop/i_petal
execute positioned 5 203 -3 run function rlk:room/prop/i_petal
execute positioned 17 201 -8 run function rlk:room/prop/i_grass
execute positioned 9 201 -7 run function rlk:room/prop/i_flower
execute positioned 9 201 -18 run function rlk:room/prop/i_petal
execute positioned 4 201 -16 run function rlk:room/prop/i_petal
setblock 1 207 -7 minecraft:short_grass keep
setblock 1 207 -6 minecraft:cherry_leaves[persistent=true] keep
setblock 1 207 -4 minecraft:cherry_leaves[persistent=true] keep
setblock 1 207 -3 minecraft:cherry_leaves[persistent=true] keep
setblock 1 207 -2 minecraft:cherry_leaves[persistent=true] keep
setblock 2 207 -3 minecraft:cherry_leaves[persistent=true] keep
setblock 2 207 -2 minecraft:cherry_leaves[persistent=true] keep
