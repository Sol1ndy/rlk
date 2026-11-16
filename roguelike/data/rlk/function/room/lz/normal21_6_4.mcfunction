# 구역 건설 (normal21_6, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -13 200 -49 -9 200 -47 minecraft:moss_block
fill -5 200 -48 -3 200 -46 minecraft:moss_block
fill -16 200 -53 -12 200 -51 minecraft:packed_mud
fill -20 201 -48 -20 210 -48 minecraft:stripped_dark_oak_log
fill -20 208 -47 -20 210 -43 minecraft:andesite
fill -20 208 -54 -20 210 -49 minecraft:cobblestone
fill -20 208 -45 -20 210 -42 minecraft:moss_block
fill -1 201 -49 -1 210 -49 minecraft:stripped_dark_oak_log
fill -1 210 -52 -1 210 -50 minecraft:cherry_leaves[persistent=true]
fill -1 201 -44 -1 210 -44 minecraft:stripped_dark_oak_log
fill -9 201 -60 -4 202 -60 minecraft:andesite
fill -8 209 -60 -4 210 -60 minecraft:cherry_leaves[persistent=true]
fill -9 209 -41 -5 210 -41 minecraft:cherry_leaves[persistent=true]
fill -10 210 -41 -7 210 -41 minecraft:cherry_leaves[persistent=true]
fill -10 210 -41 -6 210 -41 minecraft:cherry_leaves[persistent=true]
fill -4 208 -41 -3 208 -41 minecraft:cobblestone
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -44 -17 201 -44 minecraft:podzol
fill -17 201 -43 -17 201 -42 minecraft:podzol
fill -19 201 -43 -18 201 -42 minecraft:dirt
fill -19 202 -43 -18 202 -42 minecraft:podzol
fill -12 201 -59 -8 205 -59 minecraft:mossy_stone_bricks
fill -12 206 -59 -8 206 -59 minecraft:podzol
fill -13 201 -59 -13 205 -59 minecraft:stone_bricks
fill -13 206 -59 -13 206 -59 minecraft:podzol
execute positioned -6 201 -57 run function rlk:room/prop/i_rock
execute positioned -12 201 -56 run function rlk:room/prop/i_lantern
execute positioned -5 201 -54 run function rlk:room/prop/i_rock
execute positioned -2 201 -53 run function rlk:room/prop/i_fence_z
execute positioned -14 201 -55 run function rlk:room/prop/i_lantern
execute positioned -9 201 -56 run function rlk:room/prop/i_sakura
execute positioned -2 201 -59 run function rlk:room/prop/i_petal
execute positioned -8 201 -56 run function rlk:room/prop/i_grass
execute positioned -4 201 -51 run function rlk:room/prop/i_petal
execute positioned -14 201 -58 run function rlk:room/prop/i_flower
execute positioned -18 201 -52 run function rlk:room/prop/i_petal
execute positioned -13 201 -45 run function rlk:room/prop/i_petal
execute positioned -11 201 -52 run function rlk:room/prop/i_grass
execute positioned -10 201 -45 run function rlk:room/prop/i_petal
execute positioned -17 201 -50 run function rlk:room/prop/i_grass
setblock -13 207 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -12 207 -59 minecraft:short_grass keep
setblock -9 207 -59 minecraft:cherry_leaves[persistent=true] keep
setblock -8 207 -59 minecraft:short_grass keep
