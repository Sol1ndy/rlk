# 구역 건설 (normal13_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 212 -41 minecraft:stone
fill -19 201 -59 -2 212 -42 minecraft:air
fill -19 211 -59 -2 211 -42 minecraft:light[level=15]
fill -14 202 -46 -13 202 -43 minecraft:gravel
fill -15 202 -56 -12 202 -55 minecraft:coarse_dirt
fill -20 212 -59 -20 212 -58 minecraft:cherry_leaves[persistent=true]
fill -20 201 -57 -20 212 -57 minecraft:stripped_dark_oak_log
fill -20 201 -50 -20 212 -50 minecraft:stripped_dark_oak_log
fill -20 206 -59 -20 207 -56 minecraft:andesite
fill -20 201 -56 -20 212 -56 minecraft:stripped_dark_oak_log
fill -20 201 -42 -20 201 -42 minecraft:moss_block
fill -1 210 -59 -1 212 -54 minecraft:moss_block
fill -1 209 -56 -1 209 -56 minecraft:moss_block
fill -1 204 -58 -1 207 -54 minecraft:andesite
fill -8 211 -60 -6 212 -60 minecraft:cherry_leaves[persistent=true]
fill -14 201 -60 -14 212 -60 minecraft:stripped_dark_oak_log
fill -18 212 -60 -15 212 -60 minecraft:cherry_leaves[persistent=true]
fill -13 211 -60 -8 212 -60 minecraft:moss_block
fill -6 204 -60 -1 207 -60 minecraft:tuff
fill -10 209 -41 -5 209 -41 minecraft:tuff
fill -9 212 -41 -6 212 -41 minecraft:cherry_leaves[persistent=true]
fill -4 202 -41 -3 205 -41 minecraft:tuff
fill -14 211 -41 -11 212 -41 minecraft:cherry_leaves[persistent=true]
fill -14 205 -41 -11 206 -41 minecraft:cobblestone
fill -17 205 -41 -12 206 -41 minecraft:moss_block
fill -20 212 -60 -1 212 -41 minecraft:polished_deepslate
fill -19 212 -59 -2 212 -42 minecraft:air
fill -19 201 -59 -15 201 -55 minecraft:dirt
fill -19 202 -59 -15 202 -55 minecraft:podzol
fill -8 201 -59 -2 201 -42 minecraft:dirt
fill -8 202 -59 -2 202 -42 minecraft:podzol
fill -14 201 -57 -9 201 -42 minecraft:dirt
fill -14 202 -57 -9 202 -42 minecraft:podzol
fill -17 201 -54 -15 201 -47 minecraft:dirt
fill -17 202 -54 -15 202 -47 minecraft:podzol
fill -16 201 -46 -15 201 -42 minecraft:dirt
fill -16 202 -46 -15 202 -42 minecraft:podzol
fill -17 201 -42 -17 201 -42 minecraft:dirt
fill -17 202 -42 -17 202 -42 minecraft:podzol
fill -19 201 -54 -18 202 -42 minecraft:dirt
fill -19 203 -54 -18 203 -42 minecraft:podzol
fill -17 201 -46 -17 202 -43 minecraft:dirt
fill -17 203 -46 -17 203 -43 minecraft:podzol
fill -12 201 -59 -9 207 -59 minecraft:mossy_stone_bricks
fill -12 208 -59 -9 208 -59 minecraft:podzol
fill -14 201 -58 -13 207 -58 minecraft:mossy_stone_bricks
fill -14 208 -58 -13 208 -58 minecraft:podzol
fill -14 201 -59 -13 207 -59 minecraft:stone_bricks
fill -14 208 -59 -13 208 -59 minecraft:podzol
fill -12 201 -58 -9 207 -58 minecraft:stone_bricks
fill -12 208 -58 -9 208 -58 minecraft:podzol
execute positioned -4 203 -59 run function rlk:room/prop/i_lantern
execute positioned -2 203 -56 run function rlk:room/prop/i_lantern
execute positioned -19 204 -49 run function rlk:room/prop/i_lantern
execute positioned -12 203 -57 run function rlk:room/prop/i_grass
execute positioned -4 203 -44 run function rlk:room/prop/i_flower
execute positioned -11 203 -53 run function rlk:room/prop/i_petal
execute positioned -2 203 -52 run function rlk:room/prop/i_petal
execute positioned -2 203 -56 run function rlk:room/prop/i_flower
execute positioned -15 203 -48 run function rlk:room/prop/i_petal
execute positioned -5 203 -53 run function rlk:room/prop/i_petal
setblock -14 209 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -13 209 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -12 209 -58 minecraft:short_grass keep
setblock -11 209 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -9 209 -59 minecraft:short_grass keep
