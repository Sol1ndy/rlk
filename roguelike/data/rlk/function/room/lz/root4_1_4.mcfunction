# 구역 건설 (root4_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill 5 200 -9 9 200 -8 minecraft:moss_block
fill 6 200 -8 10 200 -7 minecraft:coarse_dirt
fill -8 200 -9 -5 200 -6 minecraft:moss_block
fill -6 200 -17 -3 200 -14 minecraft:packed_mud
fill 8 200 -4 12 200 -2 minecraft:moss_block
fill -19 200 -18 -17 200 -17 minecraft:gravel
fill -20 202 -18 -20 203 -17 minecraft:moss_block
fill -20 205 -14 -20 208 -9 minecraft:andesite
fill -20 210 -18 -20 210 -16 minecraft:cherry_leaves[persistent=true]
fill -20 201 -10 -20 210 -10 minecraft:stripped_dark_oak_log
fill -20 209 -18 -20 210 -14 minecraft:cherry_leaves[persistent=true]
fill -20 201 -20 -15 201 -20 minecraft:andesite
fill -7 210 -20 -6 210 -20 minecraft:cherry_leaves[persistent=true]
fill -12 205 -20 -8 206 -20 minecraft:moss_block
fill -5 201 -20 -5 210 -20 minecraft:stripped_dark_oak_log
fill -7 209 -20 -2 210 -20 minecraft:cherry_leaves[persistent=true]
fill -20 210 -20 -17 210 -20 minecraft:cherry_leaves[persistent=true]
fill -20 209 -1 -19 210 -1 minecraft:cherry_leaves[persistent=true]
fill -8 209 -1 -7 210 -1 minecraft:cherry_leaves[persistent=true]
fill -10 204 -1 -5 204 -1 minecraft:moss_block
fill 19 209 -4 19 210 -3 minecraft:cherry_leaves[persistent=true]
fill 19 209 -15 19 210 -10 minecraft:cherry_leaves[persistent=true]
fill 19 205 -1 19 207 -1 minecraft:calcite
fill 19 205 -6 19 205 -1 minecraft:andesite
fill 2 209 -20 2 210 -20 minecraft:calcite
fill 11 207 -20 15 207 -20 minecraft:calcite
fill 16 201 -20 16 210 -20 minecraft:stripped_dark_oak_log
fill 3 201 -20 3 210 -20 minecraft:stripped_dark_oak_log
fill 1 210 -1 3 210 -1 minecraft:cherry_leaves[persistent=true]
fill 6 204 -1 7 204 -1 minecraft:andesite
fill 2 210 -1 3 210 -1 minecraft:calcite
fill 13 205 -1 15 207 -1 minecraft:cobblestone
fill 10 203 -1 11 204 -1 minecraft:andesite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill 10 201 -19 10 201 -15 minecraft:podzol
fill 9 201 -18 9 201 -15 minecraft:podzol
fill -2 201 -16 -1 201 -15 minecraft:podzol
fill -17 201 -15 -13 201 -15 minecraft:podzol
fill 0 201 -15 4 201 -15 minecraft:podzol
fill 6 201 -15 8 201 -15 minecraft:podzol
fill -18 201 -14 -15 201 -9 minecraft:podzol
fill 5 201 -14 5 201 -11 minecraft:podzol
fill -19 201 -13 -19 201 -10 minecraft:podzol
fill -16 201 -8 -15 201 -7 minecraft:podzol
fill -15 201 -6 -15 201 -4 minecraft:podzol
fill -16 201 -5 -16 201 -3 minecraft:podzol
fill -18 201 -3 -17 201 -2 minecraft:podzol
fill -19 201 -2 -19 201 -2 minecraft:podzol
fill 2 201 -19 3 201 -16 minecraft:dirt
fill 2 202 -19 3 202 -16 minecraft:podzol
fill 4 201 -18 8 201 -16 minecraft:dirt
fill 4 202 -18 8 202 -16 minecraft:podzol
fill 0 201 -16 1 201 -16 minecraft:dirt
fill 0 202 -16 1 202 -16 minecraft:podzol
fill 5 201 -15 5 201 -15 minecraft:dirt
fill 5 202 -15 5 202 -15 minecraft:podzol
fill -19 201 -9 -19 201 -3 minecraft:dirt
fill -19 202 -9 -19 202 -3 minecraft:podzol
fill -18 201 -8 -17 201 -4 minecraft:dirt
fill -18 202 -8 -17 202 -4 minecraft:podzol
fill -16 201 -6 -16 201 -6 minecraft:dirt
fill -16 202 -6 -16 202 -6 minecraft:podzol
fill 4 201 -19 5 207 -19 minecraft:mossy_stone_bricks
fill 4 208 -19 5 208 -19 minecraft:podzol
fill -2 201 -19 1 207 -17 minecraft:stone_bricks
fill -2 208 -19 1 208 -17 minecraft:podzol
fill 6 201 -19 9 207 -19 minecraft:stone_bricks
fill 6 208 -19 9 208 -19 minecraft:podzol
execute positioned -2 201 -5 run function rlk:room/prop/i_shop
execute positioned -5 201 -11 run function rlk:room/prop/i_fence_z
execute positioned -16 201 -17 run function rlk:room/prop/i_bamboo
execute positioned -6 201 -6 run function rlk:room/prop/i_bamboo
execute positioned -17 202 -9 run function rlk:room/prop/i_bamboo
execute positioned -14 201 -5 run function rlk:room/prop/i_fence_x
execute positioned -2 201 -9 run function rlk:room/prop/i_petal
execute positioned 14 201 -13 run function rlk:room/prop/i_petal
execute positioned -9 201 -17 run function rlk:room/prop/i_grass
execute positioned -9 201 -17 run function rlk:room/prop/i_grass
execute positioned 3 201 -13 run function rlk:room/prop/i_grass
execute positioned 14 201 -12 run function rlk:room/prop/i_grass
execute positioned -18 203 -4 run function rlk:room/prop/i_petal
execute positioned 4 201 -11 run function rlk:room/prop/i_flower
execute positioned 10 201 -13 run function rlk:room/prop/i_grass
execute positioned 12 201 -17 run function rlk:room/prop/i_flower
execute positioned 5 201 -5 run function rlk:room/prop/i_petal
execute positioned 2 201 -8 run function rlk:room/prop/i_flower
execute positioned 1 201 -2 run function rlk:room/prop/i_grass
execute positioned 14 201 -18 run function rlk:room/prop/i_grass
execute positioned -9 201 -7 run function rlk:room/prop/i_grass
execute positioned 5 201 -4 run function rlk:room/prop/i_flower
execute positioned -5 201 -2 run function rlk:room/prop/i_petal
execute positioned 14 201 -16 run function rlk:room/prop/i_petal
setblock -2 209 -18 minecraft:cherry_leaves[persistent=true] keep
setblock -2 209 -17 minecraft:cherry_leaves[persistent=true] keep
setblock -1 209 -19 minecraft:short_grass keep
setblock -1 209 -17 minecraft:short_grass keep
setblock 0 209 -18 minecraft:short_grass keep
setblock 0 209 -17 minecraft:short_grass keep
setblock 1 209 -17 minecraft:cherry_leaves[persistent=true] keep
setblock 4 209 -19 minecraft:cherry_leaves[persistent=true] keep
setblock 5 209 -19 minecraft:short_grass keep
setblock 6 209 -19 minecraft:short_grass keep
setblock 7 209 -19 minecraft:cherry_leaves[persistent=true] keep
setblock 9 209 -19 minecraft:cherry_leaves[persistent=true] keep
