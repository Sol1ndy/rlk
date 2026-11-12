# 구역 건설 (normal13_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -11 200 -54 -9 200 -52 minecraft:gravel
fill -10 200 -52 -8 200 -50 minecraft:coarse_dirt
fill -6 200 -58 -2 200 -55 minecraft:gravel
fill -16 200 -54 -14 200 -53 minecraft:moss_block
fill -20 209 -43 -20 210 -41 minecraft:birch_leaves[persistent=true]
fill -20 208 -54 -20 210 -49 minecraft:prismarine
fill -20 209 -49 -20 210 -45 minecraft:oak_leaves[persistent=true]
fill -20 210 -55 -20 210 -51 minecraft:birch_leaves[persistent=true]
fill -20 206 -43 -20 208 -41 minecraft:calcite
fill -20 207 -58 -20 207 -57 minecraft:moss_block
fill -1 209 -50 -1 210 -48 minecraft:birch_leaves[persistent=true]
fill -1 210 -54 -1 210 -53 minecraft:moss_block
fill -1 206 -53 -1 206 -51 minecraft:moss_block
fill -1 206 -50 -1 208 -48 minecraft:moss_block
fill -1 201 -48 -1 201 -43 minecraft:moss_block
fill -1 209 -54 -1 210 -51 minecraft:birch_leaves[persistent=true]
fill -14 210 -60 -13 210 -60 minecraft:birch_leaves[persistent=true]
fill -2 204 -60 -2 204 -60 minecraft:moss_block
fill -17 209 -60 -16 210 -60 minecraft:birch_leaves[persistent=true]
fill -5 201 -60 -1 204 -60 minecraft:calcite
fill -17 210 -60 -12 210 -60 minecraft:birch_leaves[persistent=true]
fill -13 210 -60 -13 210 -60 minecraft:birch_leaves[persistent=true]
fill -16 210 -41 -12 210 -41 minecraft:birch_leaves[persistent=true]
fill -14 209 -41 -9 210 -41 minecraft:dark_prismarine
fill -17 205 -41 -13 208 -41 minecraft:diorite
fill -16 201 -41 -12 201 -41 minecraft:moss_block
fill -3 203 -41 -1 205 -41 minecraft:calcite
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -54 -18 201 -42 minecraft:podzol
fill -17 201 -46 -17 201 -43 minecraft:podzol
fill -14 201 -59 -13 205 -59 minecraft:calcite
fill -14 206 -59 -13 206 -59 minecraft:podzol
fill -12 201 -58 -9 205 -58 minecraft:calcite
fill -12 206 -58 -9 206 -58 minecraft:podzol
fill -12 201 -59 -9 205 -59 minecraft:diorite
fill -12 206 -59 -9 206 -59 minecraft:podzol
fill -14 201 -58 -13 205 -58 minecraft:diorite
fill -14 206 -58 -13 206 -58 minecraft:podzol
fill -5 199 -59 -4 199 -54 minecraft:clay
fill -5 200 -59 -4 200 -54 minecraft:water
fill -4 199 -46 -2 199 -42 minecraft:clay
fill -4 200 -46 -2 200 -42 minecraft:water
fill -2 200 -47 -2 200 -47 minecraft:sand
setblock -4 200 -58 minecraft:seagrass
setblock -4 200 -44 minecraft:seagrass
execute positioned -19 202 -44 run function rlk:room/prop/fo_col_a
execute positioned -15 201 -55 run function rlk:room/prop/fo_ruin_x
execute positioned -10 201 -48 run function rlk:room/prop/fo_white
execute positioned -15 201 -53 run function rlk:room/prop/p_grass
execute positioned -10 201 -53 run function rlk:room/prop/fo_flower
execute positioned -11 201 -48 run function rlk:room/prop/p_grass
execute positioned -14 201 -53 run function rlk:room/prop/p_grass
execute positioned -7 201 -46 run function rlk:room/prop/p_grass
execute positioned -5 201 -45 run function rlk:room/prop/fo_flower
execute positioned -17 201 -54 run function rlk:room/prop/fo_flower
setblock -14 207 -59 minecraft:short_grass keep
setblock -14 207 -58 minecraft:birch_leaves[persistent=true] keep
setblock -13 207 -59 minecraft:birch_leaves[persistent=true] keep
setblock -13 207 -58 minecraft:birch_leaves[persistent=true] keep
setblock -12 207 -59 minecraft:short_grass keep
setblock -11 207 -59 minecraft:birch_leaves[persistent=true] keep
setblock -9 207 -59 minecraft:short_grass keep
setblock -9 207 -58 minecraft:birch_leaves[persistent=true] keep
