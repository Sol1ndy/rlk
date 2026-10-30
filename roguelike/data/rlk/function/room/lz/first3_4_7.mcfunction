# 구역 건설 (first3_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -30 200 -12 -28 200 -11 minecraft:coarse_dirt
fill -39 200 -16 -37 200 -15 minecraft:calcite
fill -40 204 -2 -40 204 -1 minecraft:prismarine
fill -40 206 -15 -40 207 -13 minecraft:dark_prismarine
fill -40 206 -11 -40 208 -7 minecraft:prismarine
fill -40 210 -19 -40 210 -16 minecraft:birch_leaves[persistent=true]
fill -40 209 -13 -40 210 -9 minecraft:birch_leaves[persistent=true]
fill -21 205 -18 -21 206 -14 minecraft:calcite
fill -21 209 -6 -21 210 -2 minecraft:prismarine
fill -21 203 -8 -21 204 -7 minecraft:diorite
fill -21 201 -8 -21 201 -3 minecraft:moss_block
fill -26 210 -20 -25 210 -20 minecraft:calcite
fill -24 201 -20 -22 201 -20 minecraft:calcite
fill -40 205 -20 -35 208 -20 minecraft:moss_block
fill -30 201 -20 -29 203 -20 minecraft:dark_prismarine
fill -29 209 -20 -24 210 -20 minecraft:birch_leaves[persistent=true]
fill -36 209 -20 -36 210 -20 minecraft:oak_leaves[persistent=true]
fill -35 201 -1 -33 202 -1 minecraft:prismarine
fill -33 202 -1 -33 203 -1 minecraft:moss_block
fill -31 201 -1 -30 202 -1 minecraft:moss_block
fill -34 202 -1 -33 202 -1 minecraft:prismarine
fill -40 210 -1 -36 210 -1 minecraft:birch_leaves[persistent=true]
fill -26 210 -1 -23 210 -1 minecraft:moss_block
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -28 201 -18 -27 201 -16 minecraft:podzol
fill -26 201 -17 -22 201 -17 minecraft:podzol
fill -27 201 -15 -27 201 -15 minecraft:podzol
fill -26 201 -18 -22 201 -18 minecraft:dirt
fill -26 202 -18 -22 202 -18 minecraft:podzol
fill -30 201 -17 -29 206 -16 minecraft:calcite
fill -30 207 -17 -29 207 -16 minecraft:podzol
fill -24 201 -19 -22 207 -19 minecraft:calcite
fill -24 208 -19 -22 208 -19 minecraft:podzol
fill -27 201 -19 -25 207 -19 minecraft:diorite
fill -27 208 -19 -25 208 -19 minecraft:podzol
fill -39 199 -5 -33 199 -4 minecraft:clay
fill -39 200 -5 -33 200 -4 minecraft:water
setblock -39 200 -4 minecraft:seagrass
setblock -38 200 -5 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -37 200 -5 minecraft:seagrass
execute positioned -36 201 -15 run function rlk:room/prop/fo_pipe_x
execute positioned -33 201 -19 run function rlk:room/prop/p_grass
execute positioned -33 201 -14 run function rlk:room/prop/fo_white
execute positioned -24 201 -11 run function rlk:room/prop/fo_flower
execute positioned -35 201 -12 run function rlk:room/prop/fo_flower
execute positioned -36 201 -19 run function rlk:room/prop/p_grass
execute positioned -34 201 -8 run function rlk:room/prop/p_grass
execute positioned -23 201 -15 run function rlk:room/prop/fo_flower
execute positioned -29 201 -10 run function rlk:room/prop/fo_white
execute positioned -34 201 -9 run function rlk:room/prop/p_grass
setblock -30 208 -17 minecraft:birch_leaves[persistent=true] keep
setblock -30 208 -16 minecraft:short_grass keep
setblock -27 209 -19 minecraft:short_grass keep
setblock -25 209 -19 minecraft:short_grass keep
setblock -24 209 -19 minecraft:birch_leaves[persistent=true] keep
setblock -23 209 -19 minecraft:birch_leaves[persistent=true] keep
