# 구역 건설 (normal20_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -35 200 -6 -32 200 -4 minecraft:calcite
fill -26 200 -11 -23 200 -9 minecraft:gravel
fill -40 209 -18 -40 210 -15 minecraft:oak_leaves[persistent=true]
fill -40 205 -7 -40 205 -7 minecraft:diorite
fill -21 204 -8 -21 204 -7 minecraft:diorite
fill -21 209 -17 -21 210 -12 minecraft:calcite
fill -21 201 -5 -21 202 -4 minecraft:diorite
fill -34 210 -20 -33 210 -20 minecraft:oak_leaves[persistent=true]
fill -27 210 -20 -22 210 -20 minecraft:moss_block
fill -39 210 -20 -36 210 -20 minecraft:birch_leaves[persistent=true]
fill -32 210 -20 -27 210 -20 minecraft:birch_leaves[persistent=true]
fill -31 210 -20 -27 210 -20 minecraft:moss_block
fill -39 209 -20 -37 209 -20 minecraft:calcite
fill -25 210 -1 -24 210 -1 minecraft:birch_leaves[persistent=true]
fill -35 209 -1 -34 210 -1 minecraft:calcite
fill -33 209 -1 -33 210 -1 minecraft:calcite
fill -29 208 -1 -24 210 -1 minecraft:diorite
fill -30 207 -1 -27 208 -1 minecraft:prismarine
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -31 201 -19 -30 201 -19 minecraft:podzol
fill -22 201 -19 -22 201 -19 minecraft:podzol
fill -31 201 -18 -31 201 -17 minecraft:podzol
fill -30 201 -17 -30 201 -15 minecraft:podzol
fill -26 201 -17 -22 201 -17 minecraft:podzol
fill -27 201 -16 -27 201 -15 minecraft:podzol
fill -29 201 -15 -28 201 -15 minecraft:podzol
fill -29 201 -19 -29 201 -16 minecraft:dirt
fill -29 202 -19 -29 202 -16 minecraft:podzol
fill -23 201 -19 -23 201 -18 minecraft:dirt
fill -23 202 -19 -23 202 -18 minecraft:podzol
fill -30 201 -18 -30 201 -18 minecraft:dirt
fill -30 202 -18 -30 202 -18 minecraft:podzol
fill -26 201 -18 -24 201 -18 minecraft:dirt
fill -26 202 -18 -24 202 -18 minecraft:podzol
fill -22 201 -18 -22 201 -18 minecraft:dirt
fill -22 202 -18 -22 202 -18 minecraft:podzol
fill -27 201 -17 -27 201 -17 minecraft:dirt
fill -27 202 -17 -27 202 -17 minecraft:podzol
fill -28 201 -16 -28 201 -16 minecraft:dirt
fill -28 202 -16 -28 202 -16 minecraft:podzol
fill -28 201 -19 -24 202 -19 minecraft:dirt
fill -28 203 -19 -24 203 -19 minecraft:podzol
fill -28 201 -18 -27 202 -18 minecraft:dirt
fill -28 203 -18 -27 203 -18 minecraft:podzol
fill -28 201 -17 -28 202 -17 minecraft:dirt
fill -28 203 -17 -28 203 -17 minecraft:podzol
fill -35 199 -19 -32 199 -15 minecraft:clay
fill -35 200 -19 -32 200 -15 minecraft:water
fill -36 199 -16 -36 199 -9 minecraft:clay
fill -36 200 -16 -36 200 -9 minecraft:water
fill -31 199 -16 -31 199 -15 minecraft:clay
fill -31 200 -16 -31 200 -15 minecraft:water
fill -35 199 -14 -35 199 -9 minecraft:clay
fill -35 200 -14 -35 200 -9 minecraft:water
fill -36 200 -19 -36 200 -17 minecraft:sand
setblock -36 200 -15 minecraft:seagrass
setblock -36 200 -11 minecraft:seagrass
setblock -35 200 -9 minecraft:seagrass
setblock -34 200 -18 minecraft:seagrass
setblock -33 200 -18 minecraft:seagrass
setblock -32 200 -19 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -32 200 -18 minecraft:seagrass
setblock -32 200 -16 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -31 200 -15 minecraft:seagrass
execute positioned -37 201 -5 run function rlk:room/prop/fo_tree_b
execute positioned -39 201 -2 run function rlk:room/prop/fo_col_a
execute positioned -23 201 -15 run function rlk:room/prop/p_grass
execute positioned -39 201 -15 run function rlk:room/prop/fo_flower
execute positioned -28 201 -8 run function rlk:room/prop/p_grass
execute positioned -29 203 -19 run function rlk:room/prop/fo_flower
execute positioned -36 201 -8 run function rlk:room/prop/fo_flower
execute positioned -27 204 -18 run function rlk:room/prop/p_grass
execute positioned -27 201 -2 run function rlk:room/prop/fo_flower
execute positioned -32 201 -9 run function rlk:room/prop/fo_white
