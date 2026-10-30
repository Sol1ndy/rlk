# 구역 건설 (root0_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -30 200 -14 -26 200 -11 minecraft:coarse_dirt
fill -29 200 -15 -27 200 -13 minecraft:moss_block
fill -40 209 -16 -40 210 -13 minecraft:birch_leaves[persistent=true]
fill -40 206 -8 -40 208 -8 minecraft:prismarine
fill -40 201 -19 -40 202 -19 minecraft:calcite
fill -40 207 -6 -40 210 -4 minecraft:moss_block
fill -40 210 -12 -40 210 -10 minecraft:oak_leaves[persistent=true]
fill -21 203 -4 -21 203 -3 minecraft:diorite
fill -21 201 -12 -21 203 -9 minecraft:prismarine
fill -21 209 -16 -21 210 -13 minecraft:birch_leaves[persistent=true]
fill -40 201 -20 -36 203 -20 minecraft:calcite
fill -32 209 -20 -29 209 -20 minecraft:diorite
fill -25 210 -20 -21 210 -20 minecraft:birch_leaves[persistent=true]
fill -27 204 -1 -25 206 -1 minecraft:prismarine
fill -24 201 -1 -23 201 -1 minecraft:calcite
fill -37 202 -1 -33 203 -1 minecraft:moss_block
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -36 201 -19 -34 201 -19 minecraft:podzol
fill -35 201 -18 -34 201 -15 minecraft:podzol
fill -33 201 -17 -33 201 -15 minecraft:podzol
fill -37 201 -14 -35 201 -14 minecraft:podzol
fill -38 201 -13 -38 201 -7 minecraft:podzol
fill -37 201 -6 -35 201 -6 minecraft:podzol
fill -35 201 -5 -33 201 -5 minecraft:podzol
fill -39 201 -4 -35 201 -4 minecraft:podzol
fill -39 201 -3 -37 201 -3 minecraft:podzol
fill -39 201 -19 -37 201 -15 minecraft:dirt
fill -39 202 -19 -37 202 -15 minecraft:podzol
fill -36 201 -18 -36 201 -15 minecraft:dirt
fill -36 202 -18 -36 202 -15 minecraft:podzol
fill -39 201 -14 -38 201 -14 minecraft:dirt
fill -39 202 -14 -38 202 -14 minecraft:podzol
fill -39 201 -13 -39 201 -5 minecraft:dirt
fill -39 202 -13 -39 202 -5 minecraft:podzol
fill -38 201 -6 -38 201 -5 minecraft:dirt
fill -38 202 -6 -38 202 -5 minecraft:podzol
fill -37 201 -5 -36 201 -5 minecraft:dirt
fill -37 202 -5 -36 202 -5 minecraft:podzol
fill -28 201 -19 -28 206 -19 minecraft:calcite
fill -28 207 -19 -28 207 -19 minecraft:podzol
fill -27 201 -19 -25 206 -19 minecraft:diorite
fill -27 207 -19 -25 207 -19 minecraft:podzol
fill -32 199 -5 -27 199 -2 minecraft:clay
fill -32 200 -5 -27 200 -2 minecraft:water
fill -33 199 -4 -33 199 -2 minecraft:clay
fill -33 200 -4 -33 200 -2 minecraft:water
fill -26 199 -4 -22 199 -2 minecraft:clay
fill -26 200 -4 -22 200 -2 minecraft:water
fill -34 200 -4 -34 200 -2 minecraft:sand
setblock -31 200 -2 minecraft:seagrass
setblock -28 200 -4 minecraft:seagrass
setblock -28 200 -2 minecraft:seagrass
setblock -26 200 -3 minecraft:seagrass
execute positioned -37 203 -15 run function rlk:room/prop/fo_lamp
execute positioned -28 201 -9 run function rlk:room/prop/fo_white
execute positioned -22 201 -9 run function rlk:room/prop/p_grass
execute positioned -32 201 -15 run function rlk:room/prop/p_grass
execute positioned -23 201 -7 run function rlk:room/prop/fo_flower
execute positioned -31 201 -9 run function rlk:room/prop/fo_flower
execute positioned -36 202 -4 run function rlk:room/prop/p_grass
execute positioned -26 201 -12 run function rlk:room/prop/p_grass
setblock -28 208 -19 minecraft:birch_leaves[persistent=true] keep
setblock -25 208 -19 minecraft:birch_leaves[persistent=true] keep
