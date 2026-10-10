# 구역 건설 (normal13_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 212 -41 minecraft:stone
fill -19 201 -59 -2 212 -42 minecraft:air
fill -19 211 -59 -2 211 -42 minecraft:light[level=15]
fill -11 202 -54 -9 202 -52 minecraft:gravel
fill -10 202 -52 -8 202 -50 minecraft:coarse_dirt
fill -6 202 -58 -2 202 -55 minecraft:gravel
fill -16 202 -54 -14 202 -53 minecraft:moss_block
fill -20 211 -43 -20 212 -41 minecraft:birch_leaves[persistent=true]
fill -20 210 -54 -20 212 -49 minecraft:prismarine
fill -20 211 -49 -20 212 -45 minecraft:oak_leaves[persistent=true]
fill -20 212 -55 -20 212 -51 minecraft:birch_leaves[persistent=true]
fill -20 208 -43 -20 210 -41 minecraft:calcite
fill -20 209 -58 -20 209 -57 minecraft:moss_block
fill -1 211 -50 -1 212 -48 minecraft:birch_leaves[persistent=true]
fill -1 212 -54 -1 212 -53 minecraft:moss_block
fill -1 208 -53 -1 208 -51 minecraft:moss_block
fill -1 208 -50 -1 210 -48 minecraft:moss_block
fill -1 203 -48 -1 203 -43 minecraft:moss_block
fill -1 211 -54 -1 212 -51 minecraft:birch_leaves[persistent=true]
fill -14 212 -60 -13 212 -60 minecraft:birch_leaves[persistent=true]
fill -2 206 -60 -2 206 -60 minecraft:moss_block
fill -17 211 -60 -16 212 -60 minecraft:birch_leaves[persistent=true]
fill -5 203 -60 -1 206 -60 minecraft:calcite
fill -17 212 -60 -12 212 -60 minecraft:birch_leaves[persistent=true]
fill -13 212 -60 -13 212 -60 minecraft:birch_leaves[persistent=true]
fill -16 212 -41 -12 212 -41 minecraft:birch_leaves[persistent=true]
fill -14 211 -41 -9 212 -41 minecraft:dark_prismarine
fill -17 207 -41 -13 210 -41 minecraft:diorite
fill -16 203 -41 -12 203 -41 minecraft:moss_block
fill -3 205 -41 -1 207 -41 minecraft:calcite
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
fill -14 201 -59 -13 207 -59 minecraft:calcite
fill -14 208 -59 -13 208 -59 minecraft:podzol
fill -12 201 -58 -9 207 -58 minecraft:calcite
fill -12 208 -58 -9 208 -58 minecraft:podzol
fill -12 201 -59 -9 207 -59 minecraft:diorite
fill -12 208 -59 -9 208 -59 minecraft:podzol
fill -14 201 -58 -13 207 -58 minecraft:diorite
fill -14 208 -58 -13 208 -58 minecraft:podzol
fill -5 201 -59 -4 201 -54 minecraft:clay
fill -5 202 -59 -4 202 -54 minecraft:water
fill -4 201 -46 -2 201 -42 minecraft:clay
fill -4 202 -46 -2 202 -42 minecraft:water
fill -2 202 -47 -2 202 -47 minecraft:sand
setblock -4 202 -58 minecraft:seagrass
setblock -4 202 -44 minecraft:seagrass
execute positioned -19 204 -44 run function rlk:room/prop/fo_col_a
execute positioned -15 203 -55 run function rlk:room/prop/fo_ruin_x
execute positioned -10 203 -48 run function rlk:room/prop/fo_white
execute positioned -15 203 -53 run function rlk:room/prop/p_grass
execute positioned -10 203 -53 run function rlk:room/prop/fo_flower
execute positioned -11 203 -48 run function rlk:room/prop/p_grass
execute positioned -14 203 -53 run function rlk:room/prop/p_grass
execute positioned -7 203 -46 run function rlk:room/prop/p_grass
execute positioned -5 203 -45 run function rlk:room/prop/fo_flower
execute positioned -17 203 -54 run function rlk:room/prop/fo_flower
setblock -14 209 -59 minecraft:short_grass keep
setblock -14 209 -58 minecraft:birch_leaves[persistent=true] keep
setblock -13 209 -59 minecraft:birch_leaves[persistent=true] keep
setblock -13 209 -58 minecraft:birch_leaves[persistent=true] keep
setblock -12 209 -59 minecraft:short_grass keep
setblock -11 209 -59 minecraft:birch_leaves[persistent=true] keep
setblock -9 209 -59 minecraft:short_grass keep
setblock -9 209 -58 minecraft:birch_leaves[persistent=true] keep
