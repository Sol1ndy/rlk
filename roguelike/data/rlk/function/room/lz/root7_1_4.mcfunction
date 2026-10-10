# 구역 건설 (root7_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill -6 200 -15 -2 200 -14 minecraft:coarse_dirt
fill -5 200 -8 -4 200 -6 minecraft:coarse_dirt
fill -18 200 -10 -14 200 -9 minecraft:gravel
fill -20 209 -19 -20 210 -19 minecraft:cherry_leaves[persistent=true]
fill -20 201 -10 -20 210 -10 minecraft:stripped_dark_oak_log
fill -20 210 -12 -20 210 -8 minecraft:andesite
fill -20 209 -15 -20 210 -10 minecraft:calcite
fill -20 208 -8 -20 208 -8 minecraft:tuff
fill -16 201 -20 -13 203 -20 minecraft:moss_block
fill -14 210 -20 -14 210 -20 minecraft:cherry_leaves[persistent=true]
fill -17 208 -20 -15 210 -20 minecraft:moss_block
fill -17 208 -1 -17 209 -1 minecraft:calcite
fill -11 207 -1 -8 208 -1 minecraft:andesite
fill -10 201 -1 -10 210 -1 minecraft:stripped_dark_oak_log
fill 19 207 -6 19 207 -5 minecraft:andesite
fill 19 203 -10 19 206 -5 minecraft:calcite
fill 19 203 -17 19 204 -12 minecraft:cobblestone
fill 19 209 -7 19 210 -7 minecraft:cherry_leaves[persistent=true]
fill 19 203 -5 19 206 -4 minecraft:calcite
fill 19 208 -2 19 208 -1 minecraft:andesite
fill 16 209 -20 19 210 -20 minecraft:andesite
fill 2 210 -20 5 210 -20 minecraft:cherry_leaves[persistent=true]
fill 14 201 -20 14 210 -20 minecraft:stripped_dark_oak_log
fill 17 201 -20 17 210 -20 minecraft:stripped_dark_oak_log
fill 17 206 -1 19 207 -1 minecraft:calcite
fill 14 208 -1 16 210 -1 minecraft:calcite
fill 8 207 -1 9 207 -1 minecraft:calcite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill 9 201 -19 15 201 -17 minecraft:podzol
fill 8 201 -18 8 201 -15 minecraft:podzol
fill 16 201 -18 16 201 -17 minecraft:podzol
fill 7 201 -17 7 201 -15 minecraft:podzol
fill 17 201 -17 17 201 -17 minecraft:podzol
fill 9 201 -16 13 201 -15 minecraft:podzol
fill -18 201 -8 -15 201 -7 minecraft:podzol
fill -19 201 -7 -19 201 -2 minecraft:podzol
fill -18 201 -6 -18 201 -6 minecraft:podzol
fill -14 201 -6 -10 201 -6 minecraft:podzol
fill -11 201 -5 -10 201 -2 minecraft:podzol
fill -17 201 -6 -15 201 -2 minecraft:dirt
fill -17 202 -6 -15 202 -2 minecraft:podzol
fill -18 201 -5 -18 201 -2 minecraft:dirt
fill -18 202 -5 -18 202 -2 minecraft:podzol
fill -14 201 -5 -12 201 -2 minecraft:dirt
fill -14 202 -5 -12 202 -2 minecraft:podzol
fill 3 201 -19 5 205 -19 minecraft:mossy_stone_bricks
fill 3 206 -19 5 206 -19 minecraft:podzol
fill 2 201 -19 2 205 -18 minecraft:stone_bricks
fill 2 206 -19 2 206 -18 minecraft:podzol
fill 3 201 -18 5 205 -18 minecraft:stone_bricks
fill 3 206 -18 5 206 -18 minecraft:podzol
fill -9 201 -19 -7 206 -19 minecraft:mossy_stone_bricks
fill -9 207 -19 -7 207 -19 minecraft:podzol
fill -11 201 -19 -10 206 -18 minecraft:stone_bricks
fill -11 207 -19 -10 207 -18 minecraft:podzol
fill -9 201 -18 -7 206 -18 minecraft:stone_bricks
fill -9 207 -18 -7 207 -18 minecraft:podzol
execute positioned -16 201 -14 run function rlk:room/prop/i_shop_r1
execute positioned 7 201 -5 run function rlk:room/prop/i_shop
execute positioned 1 201 -4 run function rlk:room/prop/i_lantern2
execute positioned 11 202 -17 run function rlk:room/prop/i_lantern
execute positioned -4 201 -17 run function rlk:room/prop/i_fence_x
execute positioned 18 201 -2 run function rlk:room/prop/i_lantern
execute positioned 18 201 -15 run function rlk:room/prop/i_flower
execute positioned -4 201 -15 run function rlk:room/prop/i_grass
execute positioned -14 201 -8 run function rlk:room/prop/i_petal
execute positioned 8 201 -11 run function rlk:room/prop/i_grass
execute positioned -8 201 -15 run function rlk:room/prop/i_petal
execute positioned -8 201 -11 run function rlk:room/prop/i_petal
execute positioned -4 201 -2 run function rlk:room/prop/i_flower
execute positioned -18 201 -10 run function rlk:room/prop/i_petal
execute positioned 8 201 -9 run function rlk:room/prop/i_flower
execute positioned -7 201 -17 run function rlk:room/prop/i_grass
execute positioned 15 201 -15 run function rlk:room/prop/i_flower
execute positioned 0 201 -5 run function rlk:room/prop/i_grass
execute positioned -12 203 -4 run function rlk:room/prop/i_grass
execute positioned -17 203 -5 run function rlk:room/prop/i_grass
execute positioned 15 201 -4 run function rlk:room/prop/i_grass
setblock -10 208 -19 minecraft:cherry_leaves[persistent=true] keep
setblock -10 208 -18 minecraft:cherry_leaves[persistent=true] keep
setblock -9 208 -19 minecraft:short_grass keep
setblock -9 208 -18 minecraft:short_grass keep
setblock -7 208 -19 minecraft:short_grass keep
setblock -7 208 -18 minecraft:cherry_leaves[persistent=true] keep
setblock 2 207 -19 minecraft:cherry_leaves[persistent=true] keep
setblock 2 207 -18 minecraft:cherry_leaves[persistent=true] keep
setblock 3 207 -18 minecraft:short_grass keep
setblock 4 207 -19 minecraft:short_grass keep
setblock 4 207 -18 minecraft:short_grass keep
setblock 5 207 -19 minecraft:cherry_leaves[persistent=true] keep
setblock 5 207 -18 minecraft:cherry_leaves[persistent=true] keep
