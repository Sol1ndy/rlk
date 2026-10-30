# 구역 건설 (normal21_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -39 200 -13 -37 200 -12 minecraft:coarse_dirt
fill -40 210 -5 -40 210 -4 minecraft:oak_leaves[persistent=true]
fill -40 203 -11 -40 203 -9 minecraft:moss_block
fill -40 202 -18 -40 205 -14 minecraft:dark_prismarine
fill -40 209 -14 -40 210 -12 minecraft:oak_leaves[persistent=true]
fill -40 207 -6 -40 209 -2 minecraft:calcite
fill -40 209 -11 -40 210 -11 minecraft:oak_leaves[persistent=true]
fill -21 204 -15 -21 207 -11 minecraft:moss_block
fill -21 201 -2 -21 201 -1 minecraft:diorite
fill -21 204 -14 -21 207 -10 minecraft:calcite
fill -21 201 -6 -21 203 -5 minecraft:calcite
fill -21 204 -2 -21 205 -1 minecraft:diorite
fill -23 202 -20 -21 205 -20 minecraft:calcite
fill -29 209 -20 -27 210 -20 minecraft:calcite
fill -30 209 -20 -25 210 -20 minecraft:oak_leaves[persistent=true]
fill -38 207 -20 -38 208 -20 minecraft:calcite
fill -35 209 -1 -33 210 -1 minecraft:birch_leaves[persistent=true]
fill -29 210 -1 -29 210 -1 minecraft:moss_block
fill -28 201 -1 -23 202 -1 minecraft:moss_block
fill -30 207 -1 -29 209 -1 minecraft:calcite
fill -27 210 -1 -24 210 -1 minecraft:oak_leaves[persistent=true]
fill -30 210 -1 -28 210 -1 minecraft:oak_leaves[persistent=true]
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -39 201 -10 -37 201 -7 minecraft:podzol
fill -36 201 -9 -36 201 -7 minecraft:podzol
fill -38 201 -6 -37 201 -4 minecraft:podzol
fill -39 201 -4 -39 207 -4 minecraft:calcite
fill -39 208 -4 -39 208 -4 minecraft:podzol
fill -39 201 -6 -39 207 -5 minecraft:diorite
fill -39 208 -6 -39 208 -5 minecraft:podzol
fill -40 186 -20 -31 199 -16 minecraft:stone
fill -39 186 -19 -32 186 -17 minecraft:clay
fill -39 187 -19 -32 188 -17 minecraft:water
fill -39 189 -19 -32 201 -17 minecraft:air
fill -39 199 -14 -36 199 -11 minecraft:clay
fill -39 200 -14 -36 200 -11 minecraft:water
fill -35 199 -13 -35 199 -6 minecraft:clay
fill -35 200 -13 -35 200 -6 minecraft:water
fill -36 199 -10 -36 199 -10 minecraft:clay
fill -36 200 -10 -36 200 -10 minecraft:water
fill -36 199 -6 -36 199 -5 minecraft:clay
fill -36 200 -6 -36 200 -5 minecraft:water
fill -35 200 -14 -35 200 -14 minecraft:sand
fill -36 200 -4 -36 200 -4 minecraft:sand
setblock -39 200 -12 minecraft:seagrass
setblock -37 200 -13 minecraft:seagrass
setblock -35 200 -12 minecraft:seagrass
execute positioned -30 201 -5 run function rlk:room/prop/fo_col_b
execute positioned -26 201 -19 run function rlk:room/prop/fo_rock
execute positioned -29 201 -19 run function rlk:room/prop/fo_lamp2
execute positioned -22 201 -15 run function rlk:room/prop/fo_flower
execute positioned -26 201 -16 run function rlk:room/prop/fo_white
execute positioned -35 201 -15 run function rlk:room/prop/fo_flower
execute positioned -27 201 -12 run function rlk:room/prop/p_grass
execute positioned -34 201 -15 run function rlk:room/prop/fo_flower
execute positioned -26 201 -3 run function rlk:room/prop/fo_white
execute positioned -33 201 -3 run function rlk:room/prop/fo_white
execute positioned -23 201 -8 run function rlk:room/prop/fo_flower
execute positioned -32 201 -19 run function rlk:room/prop/p_grass
setblock -39 209 -6 minecraft:birch_leaves[persistent=true] keep
setblock -39 209 -5 minecraft:short_grass keep
setblock -39 209 -4 minecraft:short_grass keep
