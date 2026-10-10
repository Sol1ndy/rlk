# 구역 건설 (normal23_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -12 200 14 -9 200 15 minecraft:moss_block
fill -11 200 4 -9 200 7 minecraft:packed_mud
fill -20 206 6 -20 206 6 minecraft:cobblestone
fill -20 205 14 -20 205 16 minecraft:moss_block
fill -20 210 9 -20 210 12 minecraft:cherry_leaves[persistent=true]
fill -20 205 7 -20 207 12 minecraft:cobblestone
fill -1 210 10 -1 210 15 minecraft:cherry_leaves[persistent=true]
fill -1 204 5 -1 204 9 minecraft:calcite
fill -1 210 10 -1 210 12 minecraft:andesite
fill -1 208 18 -1 210 19 minecraft:cobblestone
fill -1 206 2 -1 206 7 minecraft:cobblestone
fill -3 201 0 -3 210 0 minecraft:stripped_dark_oak_log
fill -14 210 0 -9 210 0 minecraft:cobblestone
fill -14 201 0 -12 204 0 minecraft:moss_block
fill -18 202 0 -15 203 0 minecraft:tuff
fill -12 210 0 -7 210 0 minecraft:cherry_leaves[persistent=true]
fill -19 210 19 -16 210 19 minecraft:cherry_leaves[persistent=true]
fill -13 201 19 -13 210 19 minecraft:stripped_dark_oak_log
fill -11 208 19 -7 208 19 minecraft:cobblestone
fill -15 201 19 -15 210 19 minecraft:stripped_dark_oak_log
fill -20 202 19 -20 205 19 minecraft:moss_block
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -4 201 1 -2 201 3 minecraft:podzol
fill -18 201 8 -17 205 9 minecraft:mossy_stone_bricks
fill -18 206 8 -17 206 9 minecraft:podzol
fill -19 201 8 -19 205 10 minecraft:stone_bricks
fill -19 206 8 -19 206 10 minecraft:podzol
fill -18 201 10 -17 205 10 minecraft:stone_bricks
fill -18 206 10 -17 206 10 minecraft:podzol
execute positioned -11 201 15 run function rlk:room/prop/i_shop
execute positioned -2 201 16 run function rlk:room/prop/i_pillar
execute positioned -14 201 15 run function rlk:room/prop/i_lantern
execute positioned -2 201 16 run function rlk:room/prop/i_petal
execute positioned -15 201 12 run function rlk:room/prop/i_grass
execute positioned -3 202 2 run function rlk:room/prop/i_petal
execute positioned -12 201 6 run function rlk:room/prop/i_grass
execute positioned -18 201 5 run function rlk:room/prop/i_flower
execute positioned -16 201 18 run function rlk:room/prop/i_petal
execute positioned -7 201 17 run function rlk:room/prop/i_petal
setblock -19 207 8 minecraft:cherry_leaves[persistent=true] keep
setblock -19 207 9 minecraft:cherry_leaves[persistent=true] keep
setblock -18 207 8 minecraft:cherry_leaves[persistent=true] keep
setblock -18 207 9 minecraft:short_grass keep
setblock -18 207 10 minecraft:short_grass keep
setblock -17 207 8 minecraft:short_grass keep
