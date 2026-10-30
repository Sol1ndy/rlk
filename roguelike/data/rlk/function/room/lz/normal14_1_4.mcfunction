# 구역 건설 (normal14_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 10 200 -6 14 200 -4 minecraft:moss_block
fill 7 200 -10 11 200 -9 minecraft:moss_block
fill 12 200 -6 13 200 -4 minecraft:coarse_dirt
fill 0 206 -12 0 207 -9 minecraft:moss_block
fill 0 205 -6 0 206 -6 minecraft:andesite
fill 0 202 -3 0 202 -3 minecraft:tuff
fill 19 209 -13 19 210 -9 minecraft:cherry_leaves[persistent=true]
fill 19 202 -11 19 203 -8 minecraft:moss_block
fill 19 203 -17 19 205 -12 minecraft:calcite
fill 19 206 -13 19 209 -11 minecraft:calcite
fill 19 206 -4 19 208 -3 minecraft:calcite
fill 14 210 -20 18 210 -20 minecraft:cherry_leaves[persistent=true]
fill 10 202 -20 15 203 -20 minecraft:calcite
fill 13 210 -20 17 210 -20 minecraft:cobblestone
fill 3 201 -20 3 210 -20 minecraft:stripped_dark_oak_log
fill 10 203 -1 15 206 -1 minecraft:moss_block
fill 1 209 -1 5 210 -1 minecraft:cherry_leaves[persistent=true]
fill 0 201 -1 0 210 -1 minecraft:stripped_dark_oak_log
fill 5 201 -1 5 210 -1 minecraft:stripped_dark_oak_log
fill 12 209 -1 13 210 -1 minecraft:cherry_leaves[persistent=true]
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 1 201 -4 3 201 -4 minecraft:podzol
fill 3 201 -3 3 201 -2 minecraft:podzol
fill 1 201 -3 2 201 -2 minecraft:dirt
fill 1 202 -3 2 202 -2 minecraft:podzol
fill 18 201 -4 18 205 -2 minecraft:mossy_stone_bricks
fill 18 206 -4 18 206 -2 minecraft:podzol
fill 18 201 -7 18 205 -5 minecraft:stone_bricks
fill 18 206 -7 18 206 -5 minecraft:podzol
execute positioned 13 201 -17 run function rlk:room/prop/i_grass
execute positioned 5 201 -13 run function rlk:room/prop/i_petal
execute positioned 5 201 -10 run function rlk:room/prop/i_grass
execute positioned 3 201 -12 run function rlk:room/prop/i_grass
execute positioned 17 201 -13 run function rlk:room/prop/i_petal
execute positioned 2 201 -8 run function rlk:room/prop/i_grass
execute positioned 7 201 -5 run function rlk:room/prop/i_petal
setblock 18 207 -7 minecraft:cherry_leaves[persistent=true] keep
setblock 18 207 -6 minecraft:short_grass keep
setblock 18 207 -5 minecraft:short_grass keep
setblock 18 207 -4 minecraft:cherry_leaves[persistent=true] keep
setblock 18 207 -3 minecraft:cherry_leaves[persistent=true] keep
