# 구역 건설 (normal20_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 212 -1 minecraft:stone
fill -39 201 -19 -22 212 -2 minecraft:air
fill -39 211 -19 -22 211 -2 minecraft:light[level=15]
fill -35 202 -6 -32 202 -4 minecraft:calcite
fill -26 202 -11 -23 202 -9 minecraft:gravel
fill -40 211 -18 -40 212 -15 minecraft:oak_leaves[persistent=true]
fill -40 207 -7 -40 207 -7 minecraft:diorite
fill -40 202 -17 -40 202 -16 minecraft:prismarine
fill -21 206 -8 -21 206 -7 minecraft:diorite
fill -21 211 -17 -21 212 -12 minecraft:calcite
fill -21 201 -5 -21 204 -4 minecraft:diorite
fill -34 212 -20 -33 212 -20 minecraft:oak_leaves[persistent=true]
fill -27 212 -20 -22 212 -20 minecraft:moss_block
fill -39 212 -20 -36 212 -20 minecraft:birch_leaves[persistent=true]
fill -32 212 -20 -27 212 -20 minecraft:birch_leaves[persistent=true]
fill -31 212 -20 -27 212 -20 minecraft:moss_block
fill -39 211 -20 -37 211 -20 minecraft:calcite
fill -25 212 -1 -24 212 -1 minecraft:birch_leaves[persistent=true]
fill -35 211 -1 -34 212 -1 minecraft:calcite
fill -33 211 -1 -33 212 -1 minecraft:calcite
fill -29 210 -1 -24 212 -1 minecraft:diorite
fill -30 209 -1 -27 210 -1 minecraft:prismarine
fill -40 212 -20 -21 212 -1 minecraft:polished_deepslate
fill -39 212 -19 -22 212 -2 minecraft:air
fill -39 201 -19 -32 201 -2 minecraft:dirt
fill -39 202 -19 -32 202 -2 minecraft:podzol
fill -31 201 -16 -31 201 -2 minecraft:dirt
fill -31 202 -16 -31 202 -2 minecraft:podzol
fill -26 201 -16 -22 201 -2 minecraft:dirt
fill -26 202 -16 -22 202 -2 minecraft:podzol
fill -30 201 -14 -27 201 -2 minecraft:dirt
fill -30 202 -14 -27 202 -2 minecraft:podzol
fill -31 201 -19 -30 202 -19 minecraft:dirt
fill -31 203 -19 -30 203 -19 minecraft:podzol
fill -22 201 -19 -22 202 -19 minecraft:dirt
fill -22 203 -19 -22 203 -19 minecraft:podzol
fill -31 201 -18 -31 202 -17 minecraft:dirt
fill -31 203 -18 -31 203 -17 minecraft:podzol
fill -30 201 -17 -30 202 -15 minecraft:dirt
fill -30 203 -17 -30 203 -15 minecraft:podzol
fill -26 201 -17 -22 202 -17 minecraft:dirt
fill -26 203 -17 -22 203 -17 minecraft:podzol
fill -27 201 -16 -27 202 -15 minecraft:dirt
fill -27 203 -16 -27 203 -15 minecraft:podzol
fill -29 201 -15 -28 202 -15 minecraft:dirt
fill -29 203 -15 -28 203 -15 minecraft:podzol
fill -29 201 -19 -29 203 -16 minecraft:dirt
fill -29 204 -19 -29 204 -16 minecraft:podzol
fill -23 201 -19 -23 203 -18 minecraft:dirt
fill -23 204 -19 -23 204 -18 minecraft:podzol
fill -30 201 -18 -30 203 -18 minecraft:dirt
fill -30 204 -18 -30 204 -18 minecraft:podzol
fill -26 201 -18 -24 203 -18 minecraft:dirt
fill -26 204 -18 -24 204 -18 minecraft:podzol
fill -22 201 -18 -22 203 -18 minecraft:dirt
fill -22 204 -18 -22 204 -18 minecraft:podzol
fill -27 201 -17 -27 203 -17 minecraft:dirt
fill -27 204 -17 -27 204 -17 minecraft:podzol
fill -28 201 -16 -28 203 -16 minecraft:dirt
fill -28 204 -16 -28 204 -16 minecraft:podzol
fill -28 201 -19 -24 204 -19 minecraft:dirt
fill -28 205 -19 -24 205 -19 minecraft:podzol
fill -28 201 -18 -27 204 -18 minecraft:dirt
fill -28 205 -18 -27 205 -18 minecraft:podzol
fill -28 201 -17 -28 204 -17 minecraft:dirt
fill -28 205 -17 -28 205 -17 minecraft:podzol
fill -35 201 -19 -32 201 -15 minecraft:clay
fill -35 202 -19 -32 202 -15 minecraft:water
fill -36 201 -16 -36 201 -9 minecraft:clay
fill -36 202 -16 -36 202 -9 minecraft:water
fill -31 201 -16 -31 201 -15 minecraft:clay
fill -31 202 -16 -31 202 -15 minecraft:water
fill -35 201 -14 -35 201 -9 minecraft:clay
fill -35 202 -14 -35 202 -9 minecraft:water
fill -36 202 -19 -36 202 -17 minecraft:sand
setblock -36 202 -15 minecraft:seagrass
setblock -36 202 -11 minecraft:seagrass
setblock -35 202 -9 minecraft:seagrass
setblock -34 202 -18 minecraft:seagrass
setblock -33 202 -18 minecraft:seagrass
setblock -32 202 -19 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -32 202 -18 minecraft:seagrass
setblock -32 202 -16 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -31 202 -15 minecraft:seagrass
execute positioned -37 203 -5 run function rlk:room/prop/fo_tree_b
execute positioned -39 203 -2 run function rlk:room/prop/fo_col_a
execute positioned -23 203 -15 run function rlk:room/prop/p_grass
execute positioned -39 203 -15 run function rlk:room/prop/fo_flower
execute positioned -28 203 -8 run function rlk:room/prop/p_grass
execute positioned -29 205 -19 run function rlk:room/prop/fo_flower
execute positioned -36 203 -8 run function rlk:room/prop/fo_flower
execute positioned -27 206 -18 run function rlk:room/prop/p_grass
execute positioned -27 203 -2 run function rlk:room/prop/fo_flower
execute positioned -32 203 -9 run function rlk:room/prop/fo_white
