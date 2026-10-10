# 구역 건설 (root7_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 31 200 -9 34 200 -6 minecraft:coarse_dirt
fill 23 200 -12 25 200 -9 minecraft:coarse_dirt
fill 35 200 -13 36 200 -10 minecraft:moss_block
fill 20 209 -19 20 210 -19 minecraft:cherry_leaves[persistent=true]
fill 20 205 -2 20 208 -1 minecraft:tuff
fill 20 207 -16 20 208 -12 minecraft:tuff
fill 20 210 -8 20 210 -6 minecraft:cherry_leaves[persistent=true]
fill 20 201 -10 20 210 -10 minecraft:stripped_dark_oak_log
fill 20 210 -18 20 210 -16 minecraft:cherry_leaves[persistent=true]
fill 39 206 -12 39 208 -9 minecraft:calcite
fill 39 202 -14 39 202 -10 minecraft:andesite
fill 39 207 -11 39 209 -6 minecraft:cobblestone
fill 34 205 -20 37 205 -20 minecraft:moss_block
fill 20 201 -20 20 210 -20 minecraft:stripped_dark_oak_log
fill 24 205 -20 26 206 -20 minecraft:andesite
fill 32 210 -1 37 210 -1 minecraft:andesite
fill 33 206 -1 37 208 -1 minecraft:calcite
fill 20 210 -1 21 210 -1 minecraft:cherry_leaves[persistent=true]
fill 36 209 -1 39 210 -1 minecraft:cherry_leaves[persistent=true]
fill 25 201 -1 25 210 -1 minecraft:stripped_dark_oak_log
fill 22 209 -1 23 210 -1 minecraft:cherry_leaves[persistent=true]
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 28 201 -19 28 201 -17 minecraft:podzol
fill 21 201 -17 25 201 -17 minecraft:podzol
fill 26 201 -16 27 201 -15 minecraft:podzol
fill 27 201 -19 27 201 -17 minecraft:dirt
fill 27 202 -19 27 202 -17 minecraft:podzol
fill 21 201 -18 26 201 -18 minecraft:dirt
fill 21 202 -18 26 202 -18 minecraft:podzol
fill 26 201 -17 26 201 -17 minecraft:dirt
fill 26 202 -17 26 202 -17 minecraft:podzol
fill 21 201 -19 26 202 -19 minecraft:dirt
fill 21 203 -19 26 203 -19 minecraft:podzol
fill 30 201 -3 32 205 -2 minecraft:mossy_stone_bricks
fill 30 206 -3 32 206 -2 minecraft:podzol
fill 29 201 -3 29 205 -2 minecraft:stone_bricks
fill 29 206 -3 29 206 -2 minecraft:podzol
fill 30 201 -17 31 206 -16 minecraft:stone_bricks
fill 30 207 -17 31 207 -16 minecraft:podzol
execute positioned 35 201 -6 run function rlk:room/prop/i_sakura
execute positioned 31 201 -6 run function rlk:room/prop/i_petal
execute positioned 36 201 -13 run function rlk:room/prop/i_petal
execute positioned 30 201 -8 run function rlk:room/prop/i_petal
execute positioned 38 201 -19 run function rlk:room/prop/i_grass
execute positioned 35 201 -5 run function rlk:room/prop/i_flower
execute positioned 22 201 -7 run function rlk:room/prop/i_petal
execute positioned 36 201 -7 run function rlk:room/prop/i_grass
setblock 29 207 -3 minecraft:cherry_leaves[persistent=true] keep
setblock 30 208 -17 minecraft:cherry_leaves[persistent=true] keep
setblock 30 208 -16 minecraft:cherry_leaves[persistent=true] keep
setblock 31 207 -3 minecraft:cherry_leaves[persistent=true] keep
setblock 32 207 -3 minecraft:cherry_leaves[persistent=true] keep
setblock 32 207 -2 minecraft:short_grass keep
