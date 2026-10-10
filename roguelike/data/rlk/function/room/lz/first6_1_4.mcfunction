# 구역 건설 (first6_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 6 200 -11 8 200 -9 minecraft:gravel
fill 15 200 -9 18 200 -6 minecraft:coarse_dirt
fill 15 200 -5 17 200 -4 minecraft:coarse_dirt
fill 0 201 -12 0 210 -12 minecraft:stripped_dark_oak_log
fill 0 202 -16 0 204 -12 minecraft:cobblestone
fill 0 204 -18 0 207 -14 minecraft:moss_block
fill 0 209 -19 0 210 -17 minecraft:cherry_leaves[persistent=true]
fill 0 203 -18 0 205 -16 minecraft:tuff
fill 0 209 -19 0 210 -15 minecraft:cherry_leaves[persistent=true]
fill 19 201 -18 19 201 -15 minecraft:moss_block
fill 19 204 -11 19 206 -10 minecraft:calcite
fill 19 201 -20 19 204 -18 minecraft:tuff
fill 2 201 -20 2 210 -20 minecraft:stripped_dark_oak_log
fill 14 205 -20 14 206 -20 minecraft:calcite
fill 0 201 -20 1 203 -20 minecraft:moss_block
fill 14 202 -1 19 205 -1 minecraft:cobblestone
fill 13 210 -1 15 210 -1 minecraft:cherry_leaves[persistent=true]
fill 3 210 -1 8 210 -1 minecraft:cherry_leaves[persistent=true]
fill 3 208 -1 6 209 -1 minecraft:moss_block
fill 6 204 -1 7 205 -1 minecraft:andesite
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -19 4 201 -19 minecraft:podzol
fill 4 201 -18 4 201 -18 minecraft:podzol
fill 3 201 -15 4 201 -15 minecraft:podzol
fill 1 201 -14 3 201 -14 minecraft:podzol
fill 1 201 -13 1 201 -13 minecraft:podzol
fill 1 201 -19 2 201 -15 minecraft:dirt
fill 1 202 -19 2 202 -15 minecraft:podzol
fill 3 201 -18 3 201 -16 minecraft:dirt
fill 3 202 -18 3 202 -16 minecraft:podzol
fill 8 201 -2 12 205 -2 minecraft:stone_bricks
fill 8 206 -2 12 206 -2 minecraft:podzol
fill 9 201 -17 10 207 -16 minecraft:mossy_stone_bricks
fill 9 208 -17 10 208 -16 minecraft:podzol
fill 4 201 -17 5 207 -16 minecraft:stone_bricks
fill 4 208 -17 5 208 -16 minecraft:podzol
execute positioned 3 201 -7 run function rlk:room/prop/i_bamboo
execute positioned 5 201 -4 run function rlk:room/prop/i_sakura
execute positioned 4 201 -10 run function rlk:room/prop/i_sakura
execute positioned 1 203 -17 run function rlk:room/prop/i_grass
execute positioned 9 201 -18 run function rlk:room/prop/i_grass
execute positioned 4 202 -19 run function rlk:room/prop/i_petal
execute positioned 12 201 -16 run function rlk:room/prop/i_petal
execute positioned 16 201 -6 run function rlk:room/prop/i_petal
execute positioned 11 201 -10 run function rlk:room/prop/i_grass
execute positioned 14 201 -13 run function rlk:room/prop/i_petal
execute positioned 17 201 -11 run function rlk:room/prop/i_petal
execute positioned 14 201 -8 run function rlk:room/prop/i_grass
execute positioned 3 201 -5 run function rlk:room/prop/i_grass
setblock 4 209 -16 minecraft:short_grass keep
setblock 5 209 -16 minecraft:cherry_leaves[persistent=true] keep
setblock 8 207 -2 minecraft:cherry_leaves[persistent=true] keep
setblock 9 209 -17 minecraft:short_grass keep
setblock 9 209 -16 minecraft:cherry_leaves[persistent=true] keep
setblock 9 207 -2 minecraft:cherry_leaves[persistent=true] keep
setblock 10 209 -17 minecraft:short_grass keep
setblock 10 209 -16 minecraft:short_grass keep
setblock 11 207 -2 minecraft:short_grass keep
