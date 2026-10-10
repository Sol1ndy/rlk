# 구역 건설 (normal5_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -5 200 -33 -4 200 -32 minecraft:moss_block
fill -3 200 -34 -2 200 -31 minecraft:calcite
fill -7 200 -35 -3 200 -33 minecraft:coarse_dirt
fill -20 210 -25 -20 210 -22 minecraft:birch_leaves[persistent=true]
fill -20 209 -34 -20 210 -32 minecraft:calcite
fill -20 201 -25 -20 204 -24 minecraft:calcite
fill -20 209 -40 -20 209 -40 minecraft:diorite
fill -20 209 -29 -20 210 -24 minecraft:calcite
fill -1 202 -38 -1 204 -33 minecraft:dark_prismarine
fill -1 209 -35 -1 210 -33 minecraft:oak_leaves[persistent=true]
fill -1 206 -39 -1 209 -36 minecraft:diorite
fill -1 208 -36 -1 209 -34 minecraft:calcite
fill -5 203 -40 -1 205 -40 minecraft:diorite
fill -7 203 -40 -5 204 -40 minecraft:moss_block
fill -16 209 -40 -15 210 -40 minecraft:birch_leaves[persistent=true]
fill -18 210 -40 -18 210 -40 minecraft:oak_leaves[persistent=true]
fill -12 209 -40 -9 210 -40 minecraft:diorite
fill -13 210 -40 -9 210 -40 minecraft:oak_leaves[persistent=true]
fill -3 202 -21 -3 204 -21 minecraft:prismarine
fill -16 201 -21 -12 203 -21 minecraft:calcite
fill -5 208 -21 -2 210 -21 minecraft:diorite
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -19 201 -39 -19 201 -35 minecraft:podzol
fill -9 201 -39 -8 201 -35 minecraft:podzol
fill -14 201 -35 -10 201 -35 minecraft:podzol
fill -15 201 -34 -15 201 -30 minecraft:podzol
fill -19 201 -31 -19 201 -30 minecraft:podzol
fill -18 201 -30 -16 201 -30 minecraft:podzol
fill -18 201 -39 -10 201 -37 minecraft:dirt
fill -18 202 -39 -10 202 -37 minecraft:podzol
fill -18 201 -36 -18 201 -31 minecraft:dirt
fill -18 202 -36 -18 202 -31 minecraft:podzol
fill -15 201 -36 -10 201 -36 minecraft:dirt
fill -15 202 -36 -10 202 -36 minecraft:podzol
fill -15 201 -35 -15 201 -35 minecraft:dirt
fill -15 202 -35 -15 202 -35 minecraft:podzol
fill -19 201 -34 -19 201 -32 minecraft:dirt
fill -19 202 -34 -19 202 -32 minecraft:podzol
fill -17 201 -34 -16 201 -31 minecraft:dirt
fill -17 202 -34 -16 202 -31 minecraft:podzol
fill -17 201 -36 -16 207 -35 minecraft:calcite
fill -17 208 -36 -16 208 -35 minecraft:podzol
fill -19 201 -25 -19 207 -25 minecraft:calcite
fill -19 208 -25 -19 208 -25 minecraft:podzol
fill -19 201 -24 -19 207 -22 minecraft:diorite
fill -19 208 -24 -19 208 -22 minecraft:podzol
fill -17 199 -28 -15 199 -27 minecraft:clay
fill -17 200 -28 -15 200 -27 minecraft:water
fill -17 200 -29 -17 200 -29 minecraft:sand
fill -15 200 -29 -15 200 -29 minecraft:sand
fill -18 200 -27 -18 200 -27 minecraft:sand
fill -17 200 -26 -17 200 -26 minecraft:sand
setblock -17 200 -28 minecraft:seagrass
setblock -16 200 -27 minecraft:seagrass
execute positioned -13 203 -36 run function rlk:room/prop/fo_lamp
execute positioned -11 203 -39 run function rlk:room/prop/fo_rock_s
execute positioned -14 203 -39 run function rlk:room/prop/fo_col_a
execute positioned -9 201 -22 run function rlk:room/prop/p_grass
execute positioned -4 201 -39 run function rlk:room/prop/fo_white
execute positioned -18 201 -27 run function rlk:room/prop/fo_flower
execute positioned -14 201 -24 run function rlk:room/prop/fo_white
execute positioned -12 201 -32 run function rlk:room/prop/fo_white
execute positioned -8 202 -37 run function rlk:room/prop/fo_white
execute positioned -5 201 -23 run function rlk:room/prop/fo_white
execute positioned -4 201 -23 run function rlk:room/prop/fo_white
execute positioned -15 201 -26 run function rlk:room/prop/p_grass
execute positioned -9 201 -29 run function rlk:room/prop/p_grass
setblock -19 209 -23 minecraft:birch_leaves[persistent=true] keep
setblock -17 209 -36 minecraft:birch_leaves[persistent=true] keep
setblock -17 209 -35 minecraft:birch_leaves[persistent=true] keep
setblock -16 209 -36 minecraft:short_grass keep
