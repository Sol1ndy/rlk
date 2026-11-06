# 구역 건설 (normal19_6, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 0 -41 200 19 minecraft:podzol
fill -60 201 0 -41 210 19 minecraft:stone
fill -59 201 1 -42 210 18 minecraft:air
fill -59 209 1 -42 209 18 minecraft:light[level=15]
fill -46 200 1 -45 200 2 minecraft:packed_mud
fill -49 200 5 -48 200 8 minecraft:packed_mud
fill -60 210 10 -60 210 13 minecraft:tuff
fill -60 210 13 -60 210 17 minecraft:andesite
fill -60 201 9 -60 210 9 minecraft:stripped_dark_oak_log
fill -41 205 6 -41 206 9 minecraft:andesite
fill -41 209 2 -41 210 2 minecraft:cherry_leaves[persistent=true]
fill -41 208 10 -41 209 13 minecraft:andesite
fill -41 208 14 -41 210 16 minecraft:cobblestone
fill -41 209 4 -41 210 8 minecraft:cherry_leaves[persistent=true]
fill -49 208 0 -44 208 0 minecraft:cobblestone
fill -55 209 0 -50 210 0 minecraft:tuff
fill -47 209 0 -45 210 0 minecraft:calcite
fill -50 206 0 -47 208 0 minecraft:cobblestone
fill -55 209 0 -52 210 0 minecraft:moss_block
fill -52 210 19 -52 210 19 minecraft:cherry_leaves[persistent=true]
fill -60 210 19 -57 210 19 minecraft:cherry_leaves[persistent=true]
fill -57 204 19 -55 207 19 minecraft:cobblestone
fill -48 201 19 -48 210 19 minecraft:stripped_dark_oak_log
fill -60 210 0 -41 210 19 minecraft:polished_deepslate
fill -59 210 1 -42 210 18 minecraft:air
fill -59 201 9 -57 201 9 minecraft:podzol
fill -57 201 10 -56 201 10 minecraft:podzol
fill -56 201 11 -56 201 14 minecraft:podzol
fill -57 201 14 -57 201 15 minecraft:podzol
fill -59 201 15 -58 201 15 minecraft:podzol
fill -59 201 10 -58 201 14 minecraft:dirt
fill -59 202 10 -58 202 14 minecraft:podzol
fill -57 201 11 -57 201 13 minecraft:dirt
fill -57 202 11 -57 202 13 minecraft:podzol
fill -54 201 18 -52 206 18 minecraft:mossy_stone_bricks
fill -54 207 18 -52 207 18 minecraft:podzol
fill -51 201 3 -50 206 4 minecraft:stone_bricks
fill -51 207 3 -50 207 4 minecraft:podzol
fill -51 201 18 -51 206 18 minecraft:stone_bricks
fill -51 207 18 -51 207 18 minecraft:podzol
fill -56 201 3 -55 207 4 minecraft:stone_bricks
fill -56 208 3 -55 208 4 minecraft:podzol
fill -57 201 4 -57 207 5 minecraft:stone_bricks
fill -57 208 4 -57 208 5 minecraft:podzol
fill -56 201 5 -56 207 5 minecraft:stone_bricks
fill -56 208 5 -56 208 5 minecraft:podzol
execute positioned -45 201 16 run function rlk:room/prop/i_fence_x
execute positioned -55 201 15 run function rlk:room/prop/i_lantern
execute positioned -49 201 15 run function rlk:room/prop/i_sakura
execute positioned -47 201 18 run function rlk:room/prop/i_lantern
execute positioned -44 201 4 run function rlk:room/prop/i_petal
execute positioned -42 201 1 run function rlk:room/prop/i_petal
execute positioned -47 201 2 run function rlk:room/prop/i_petal
execute positioned -55 201 12 run function rlk:room/prop/i_petal
execute positioned -45 201 1 run function rlk:room/prop/i_petal
execute positioned -44 201 1 run function rlk:room/prop/i_petal
execute positioned -57 201 7 run function rlk:room/prop/i_flower
execute positioned -53 201 16 run function rlk:room/prop/i_petal
execute positioned -58 201 5 run function rlk:room/prop/i_grass
setblock -57 209 5 minecraft:cherry_leaves[persistent=true] keep
setblock -56 209 3 minecraft:short_grass keep
setblock -56 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock -56 209 5 minecraft:cherry_leaves[persistent=true] keep
setblock -54 208 18 minecraft:short_grass keep
setblock -53 208 18 minecraft:short_grass keep
setblock -52 208 18 minecraft:cherry_leaves[persistent=true] keep
setblock -51 208 3 minecraft:cherry_leaves[persistent=true] keep
setblock -51 208 18 minecraft:cherry_leaves[persistent=true] keep
setblock -50 208 4 minecraft:cherry_leaves[persistent=true] keep
