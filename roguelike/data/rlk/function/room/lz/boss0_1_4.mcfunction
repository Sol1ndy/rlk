# 구역 건설 (boss0_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -8 200 8 -4 200 9 minecraft:moss_block
fill -5 200 3 -4 200 4 minecraft:moss_block
fill -10 200 8 -9 200 10 minecraft:coarse_dirt
fill -20 207 8 -20 210 11 minecraft:moss_block
fill -20 206 3 -20 208 7 minecraft:tuff
fill -20 210 13 -20 210 13 minecraft:tuff
fill -20 201 2 -20 210 2 minecraft:stripped_dark_oak_log
fill -20 207 12 -20 210 14 minecraft:tuff
fill -1 207 6 -1 208 10 minecraft:andesite
fill -1 209 9 -1 210 13 minecraft:cherry_leaves[persistent=true]
fill -1 209 11 -1 210 15 minecraft:cherry_leaves[persistent=true]
fill -9 206 0 -4 208 0 minecraft:cobblestone
fill -14 210 0 -12 210 0 minecraft:tuff
fill -20 209 0 -16 210 0 minecraft:cherry_leaves[persistent=true]
fill -7 204 0 -4 204 0 minecraft:calcite
fill -15 203 0 -12 204 0 minecraft:andesite
fill -4 205 0 -4 208 0 minecraft:calcite
fill -5 210 19 -1 210 19 minecraft:cherry_leaves[persistent=true]
fill -11 203 19 -10 203 19 minecraft:moss_block
fill -20 205 19 -17 205 19 minecraft:moss_block
fill -17 210 19 -13 210 19 minecraft:cherry_leaves[persistent=true]
fill -6 207 19 -5 210 19 minecraft:tuff
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -15 201 11 -15 201 14 minecraft:podzol
fill -17 201 12 -16 201 13 minecraft:podzol
fill -17 201 14 -17 201 15 minecraft:podzol
fill -14 201 15 -7 201 15 minecraft:podzol
fill -8 201 16 -7 201 18 minecraft:podzol
fill -16 201 14 -16 201 18 minecraft:dirt
fill -16 202 14 -16 202 18 minecraft:podzol
fill -15 201 15 -15 201 18 minecraft:dirt
fill -15 202 15 -15 202 18 minecraft:podzol
fill -17 201 16 -17 201 18 minecraft:dirt
fill -17 202 16 -17 202 18 minecraft:podzol
fill -14 201 16 -9 201 18 minecraft:dirt
fill -14 202 16 -9 202 18 minecraft:podzol
fill -17 201 7 -16 205 8 minecraft:mossy_stone_bricks
fill -17 206 7 -16 206 8 minecraft:podzol
fill -18 201 14 -18 206 17 minecraft:mossy_stone_bricks
fill -18 207 14 -18 207 17 minecraft:podzol
fill -19 201 13 -18 206 13 minecraft:stone_bricks
fill -19 207 13 -18 207 13 minecraft:podzol
fill -19 201 14 -19 206 18 minecraft:stone_bricks
fill -19 207 14 -19 207 18 minecraft:podzol
fill -18 201 18 -18 206 18 minecraft:stone_bricks
fill -18 207 18 -18 207 18 minecraft:podzol
execute positioned -4 201 8 run function rlk:room/prop/i_lantern2
execute positioned -4 201 13 run function rlk:room/prop/i_sakura
execute positioned -9 201 14 run function rlk:room/prop/i_petal
execute positioned -19 201 4 run function rlk:room/prop/i_petal
execute positioned -14 201 4 run function rlk:room/prop/i_grass
execute positioned -10 203 18 run function rlk:room/prop/i_flower
execute positioned -9 201 8 run function rlk:room/prop/i_petal
execute positioned -17 201 6 run function rlk:room/prop/i_flower
execute positioned -16 203 18 run function rlk:room/prop/i_petal
execute positioned -12 201 10 run function rlk:room/prop/i_grass
execute positioned -15 202 13 run function rlk:room/prop/i_grass
setblock -19 208 14 minecraft:cherry_leaves[persistent=true] keep
setblock -19 208 16 minecraft:short_grass keep
setblock -19 208 18 minecraft:cherry_leaves[persistent=true] keep
setblock -18 208 13 minecraft:cherry_leaves[persistent=true] keep
setblock -18 208 14 minecraft:short_grass keep
setblock -18 208 17 minecraft:cherry_leaves[persistent=true] keep
setblock -18 208 18 minecraft:short_grass keep
setblock -17 207 7 minecraft:cherry_leaves[persistent=true] keep
setblock -16 207 7 minecraft:cherry_leaves[persistent=true] keep
