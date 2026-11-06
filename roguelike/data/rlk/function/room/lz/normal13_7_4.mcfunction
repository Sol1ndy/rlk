# 구역 건설 (normal13_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -14 200 -46 -13 200 -43 minecraft:gravel
fill -15 200 -56 -12 200 -55 minecraft:coarse_dirt
fill -20 210 -59 -20 210 -58 minecraft:cherry_leaves[persistent=true]
fill -20 201 -57 -20 210 -57 minecraft:stripped_dark_oak_log
fill -20 201 -50 -20 210 -50 minecraft:stripped_dark_oak_log
fill -20 204 -59 -20 205 -56 minecraft:andesite
fill -20 201 -56 -20 210 -56 minecraft:stripped_dark_oak_log
fill -1 208 -59 -1 210 -54 minecraft:moss_block
fill -1 207 -56 -1 207 -56 minecraft:moss_block
fill -1 202 -58 -1 205 -54 minecraft:andesite
fill -8 209 -60 -6 210 -60 minecraft:cherry_leaves[persistent=true]
fill -14 201 -60 -14 210 -60 minecraft:stripped_dark_oak_log
fill -18 210 -60 -15 210 -60 minecraft:cherry_leaves[persistent=true]
fill -13 209 -60 -8 210 -60 minecraft:moss_block
fill -6 202 -60 -1 205 -60 minecraft:tuff
fill -10 207 -41 -5 207 -41 minecraft:tuff
fill -9 210 -41 -6 210 -41 minecraft:cherry_leaves[persistent=true]
fill -4 201 -41 -3 203 -41 minecraft:tuff
fill -14 209 -41 -11 210 -41 minecraft:cherry_leaves[persistent=true]
fill -14 203 -41 -11 204 -41 minecraft:cobblestone
fill -17 203 -41 -12 204 -41 minecraft:moss_block
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -54 -18 201 -42 minecraft:podzol
fill -17 201 -46 -17 201 -43 minecraft:podzol
fill -12 201 -59 -9 205 -59 minecraft:mossy_stone_bricks
fill -12 206 -59 -9 206 -59 minecraft:podzol
fill -14 201 -58 -13 205 -58 minecraft:mossy_stone_bricks
fill -14 206 -58 -13 206 -58 minecraft:podzol
fill -14 201 -59 -13 205 -59 minecraft:stone_bricks
fill -14 206 -59 -13 206 -59 minecraft:podzol
fill -12 201 -58 -9 205 -58 minecraft:stone_bricks
fill -12 206 -58 -9 206 -58 minecraft:podzol
execute positioned -4 201 -59 run function rlk:room/prop/i_lantern
execute positioned -2 201 -56 run function rlk:room/prop/i_lantern
execute positioned -19 202 -49 run function rlk:room/prop/i_lantern
execute positioned -12 201 -57 run function rlk:room/prop/i_grass
execute positioned -4 201 -44 run function rlk:room/prop/i_flower
execute positioned -11 201 -53 run function rlk:room/prop/i_petal
execute positioned -2 201 -52 run function rlk:room/prop/i_petal
execute positioned -2 201 -56 run function rlk:room/prop/i_flower
execute positioned -15 201 -48 run function rlk:room/prop/i_petal
execute positioned -5 201 -53 run function rlk:room/prop/i_petal
setblock -14 207 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -13 207 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -12 207 -58 minecraft:short_grass keep
setblock -11 207 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -9 207 -59 minecraft:short_grass keep
