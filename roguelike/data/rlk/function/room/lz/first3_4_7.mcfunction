# 구역 건설 (first3_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 212 -1 minecraft:stone
fill -39 201 -19 -22 212 -2 minecraft:air
fill -39 211 -19 -22 211 -2 minecraft:light[level=15]
fill -30 202 -12 -28 202 -11 minecraft:coarse_dirt
fill -39 202 -16 -37 202 -15 minecraft:calcite
fill -40 206 -2 -40 206 -1 minecraft:prismarine
fill -40 208 -15 -40 209 -13 minecraft:dark_prismarine
fill -40 208 -11 -40 210 -7 minecraft:prismarine
fill -40 212 -19 -40 212 -16 minecraft:birch_leaves[persistent=true]
fill -40 211 -13 -40 212 -9 minecraft:birch_leaves[persistent=true]
fill -21 207 -18 -21 208 -14 minecraft:calcite
fill -21 211 -6 -21 212 -2 minecraft:prismarine
fill -21 205 -8 -21 206 -7 minecraft:diorite
fill -21 202 -8 -21 203 -3 minecraft:moss_block
fill -26 212 -20 -25 212 -20 minecraft:calcite
fill -24 202 -20 -22 203 -20 minecraft:calcite
fill -40 207 -20 -35 210 -20 minecraft:moss_block
fill -30 202 -20 -29 205 -20 minecraft:dark_prismarine
fill -29 211 -20 -24 212 -20 minecraft:birch_leaves[persistent=true]
fill -36 211 -20 -36 212 -20 minecraft:oak_leaves[persistent=true]
fill -35 201 -1 -33 204 -1 minecraft:prismarine
fill -33 204 -1 -33 205 -1 minecraft:moss_block
fill -31 201 -1 -30 204 -1 minecraft:moss_block
fill -34 204 -1 -33 204 -1 minecraft:prismarine
fill -40 212 -1 -36 212 -1 minecraft:birch_leaves[persistent=true]
fill -26 212 -1 -23 212 -1 minecraft:moss_block
fill -40 212 -20 -21 212 -1 minecraft:polished_deepslate
fill -39 212 -19 -22 212 -2 minecraft:air
fill -39 201 -19 -28 201 -19 minecraft:dirt
fill -39 202 -19 -28 202 -19 minecraft:podzol
fill -39 201 -18 -29 201 -18 minecraft:dirt
fill -39 202 -18 -29 202 -18 minecraft:podzol
fill -39 201 -17 -31 201 -2 minecraft:dirt
fill -39 202 -17 -31 202 -2 minecraft:podzol
fill -26 201 -16 -22 201 -2 minecraft:dirt
fill -26 202 -16 -22 202 -2 minecraft:podzol
fill -30 201 -15 -28 201 -2 minecraft:dirt
fill -30 202 -15 -28 202 -2 minecraft:podzol
fill -27 201 -14 -27 201 -2 minecraft:dirt
fill -27 202 -14 -27 202 -2 minecraft:podzol
fill -28 201 -18 -27 202 -16 minecraft:dirt
fill -28 203 -18 -27 203 -16 minecraft:podzol
fill -26 201 -17 -22 202 -17 minecraft:dirt
fill -26 203 -17 -22 203 -17 minecraft:podzol
fill -27 201 -15 -27 202 -15 minecraft:dirt
fill -27 203 -15 -27 203 -15 minecraft:podzol
fill -26 201 -18 -22 203 -18 minecraft:dirt
fill -26 204 -18 -22 204 -18 minecraft:podzol
fill -30 201 -17 -29 208 -16 minecraft:calcite
fill -30 209 -17 -29 209 -16 minecraft:podzol
fill -24 201 -19 -22 209 -19 minecraft:calcite
fill -24 210 -19 -22 210 -19 minecraft:podzol
fill -27 201 -19 -25 209 -19 minecraft:diorite
fill -27 210 -19 -25 210 -19 minecraft:podzol
fill -39 201 -5 -33 201 -4 minecraft:clay
fill -39 202 -5 -33 202 -4 minecraft:water
setblock -39 202 -4 minecraft:seagrass
setblock -38 202 -5 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -37 202 -5 minecraft:seagrass
execute positioned -36 203 -15 run function rlk:room/prop/fo_pipe_x
execute positioned -33 203 -19 run function rlk:room/prop/p_grass
execute positioned -33 203 -14 run function rlk:room/prop/fo_white
execute positioned -24 203 -11 run function rlk:room/prop/fo_flower
execute positioned -35 203 -12 run function rlk:room/prop/fo_flower
execute positioned -36 203 -19 run function rlk:room/prop/p_grass
execute positioned -34 203 -8 run function rlk:room/prop/p_grass
execute positioned -23 203 -15 run function rlk:room/prop/fo_flower
execute positioned -29 203 -10 run function rlk:room/prop/fo_white
execute positioned -34 203 -9 run function rlk:room/prop/p_grass
setblock -30 210 -17 minecraft:birch_leaves[persistent=true] keep
setblock -30 210 -16 minecraft:short_grass keep
setblock -27 211 -19 minecraft:short_grass keep
setblock -25 211 -19 minecraft:short_grass keep
setblock -24 211 -19 minecraft:birch_leaves[persistent=true] keep
setblock -23 211 -19 minecraft:birch_leaves[persistent=true] keep
