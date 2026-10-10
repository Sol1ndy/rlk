# 구역 건설 (levelup8_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -20 -41 200 -1 minecraft:podzol
fill -60 201 -20 -41 210 -1 minecraft:stone
fill -59 201 -19 -42 210 -2 minecraft:air
fill -59 209 -19 -42 209 -2 minecraft:light[level=15]
fill -55 200 -16 -54 200 -13 minecraft:moss_block
fill -45 200 -16 -43 200 -15 minecraft:moss_block
fill -45 200 -10 -42 200 -7 minecraft:gravel
fill -54 200 -15 -53 200 -13 minecraft:moss_block
fill -60 209 -4 -60 210 -2 minecraft:oak_leaves[persistent=true]
fill -60 210 -13 -60 210 -9 minecraft:oak_leaves[persistent=true]
fill -60 210 -2 -60 210 -1 minecraft:diorite
fill -60 206 -18 -60 208 -13 minecraft:dark_prismarine
fill -60 209 -6 -60 210 -5 minecraft:birch_leaves[persistent=true]
fill -41 205 -19 -41 205 -19 minecraft:diorite
fill -41 210 -14 -41 210 -13 minecraft:birch_leaves[persistent=true]
fill -41 201 -6 -41 204 -6 minecraft:prismarine
fill -41 210 -6 -41 210 -2 minecraft:birch_leaves[persistent=true]
fill -41 210 -12 -41 210 -10 minecraft:prismarine
fill -47 206 -20 -42 207 -20 minecraft:diorite
fill -47 205 -20 -42 206 -20 minecraft:calcite
fill -41 206 -20 -41 209 -20 minecraft:moss_block
fill -58 210 -1 -56 210 -1 minecraft:birch_leaves[persistent=true]
fill -54 207 -1 -54 209 -1 minecraft:diorite
fill -45 204 -1 -45 207 -1 minecraft:moss_block
fill -55 207 -1 -51 209 -1 minecraft:diorite
fill -52 209 -1 -50 210 -1 minecraft:prismarine
fill -59 204 -1 -56 205 -1 minecraft:calcite
fill -60 210 -20 -41 210 -1 minecraft:polished_deepslate
fill -59 210 -19 -42 210 -2 minecraft:air
fill -44 201 -6 -43 201 -2 minecraft:podzol
fill -42 201 -5 -42 201 -2 minecraft:podzol
fill -45 199 -11 -44 199 -9 minecraft:clay
fill -45 200 -11 -44 200 -9 minecraft:water
fill -45 200 -12 -44 200 -12 minecraft:sand
fill -43 200 -10 -43 200 -9 minecraft:sand
fill -44 200 -8 -44 200 -8 minecraft:sand
setblock -45 200 -11 minecraft:seagrass
setblock -45 200 -10 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock -45 200 -9 minecraft:seagrass
setblock -44 200 -11 minecraft:seagrass
execute positioned -55 201 -12 run function rlk:room/prop/fo_tree
execute positioned -57 201 -9 run function rlk:room/prop/fo_rock
execute positioned -59 201 -7 run function rlk:room/prop/fo_col_a
execute positioned -47 201 -3 run function rlk:room/prop/p_grass
execute positioned -49 201 -8 run function rlk:room/prop/fo_flower
execute positioned -47 201 -9 run function rlk:room/prop/fo_white
execute positioned -54 201 -2 run function rlk:room/prop/fo_flower
execute positioned -42 202 -2 run function rlk:room/prop/fo_white
execute positioned -51 201 -19 run function rlk:room/prop/p_grass
execute positioned -58 201 -5 run function rlk:room/prop/fo_flower
execute positioned -54 201 -16 run function rlk:room/prop/p_grass
