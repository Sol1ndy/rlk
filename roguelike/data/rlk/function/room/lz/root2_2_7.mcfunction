# 구역 건설 (root2_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -16 200 -33 -12 200 -32 minecraft:coarse_dirt
fill -10 200 -37 -9 200 -34 minecraft:moss_block
fill -20 201 -26 -20 203 -24 minecraft:moss_block
fill -20 209 -26 -20 210 -21 minecraft:birch_leaves[persistent=true]
fill -20 208 -39 -20 210 -35 minecraft:calcite
fill -20 209 -22 -20 210 -22 minecraft:oak_leaves[persistent=true]
fill -20 207 -36 -20 209 -36 minecraft:prismarine
fill -1 209 -39 -1 210 -35 minecraft:birch_leaves[persistent=true]
fill -1 209 -27 -1 210 -26 minecraft:calcite
fill -1 209 -27 -1 210 -24 minecraft:birch_leaves[persistent=true]
fill -1 210 -26 -1 210 -22 minecraft:oak_leaves[persistent=true]
fill -1 208 -38 -1 208 -38 minecraft:calcite
fill -7 201 -40 -5 201 -40 minecraft:calcite
fill -20 209 -40 -17 210 -40 minecraft:birch_leaves[persistent=true]
fill -14 204 -40 -10 207 -40 minecraft:calcite
fill -17 202 -40 -12 203 -40 minecraft:dark_prismarine
fill -18 206 -40 -17 207 -40 minecraft:moss_block
fill -2 210 -40 -1 210 -40 minecraft:oak_leaves[persistent=true]
fill -10 208 -21 -9 210 -21 minecraft:diorite
fill -12 209 -21 -10 210 -21 minecraft:oak_leaves[persistent=true]
fill -20 210 -21 -19 210 -21 minecraft:oak_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -15 201 -38 -14 201 -38 minecraft:podzol
fill -16 201 -37 -15 201 -37 minecraft:podzol
fill -19 201 -36 -16 201 -36 minecraft:podzol
fill -19 201 -35 -17 201 -35 minecraft:podzol
fill -19 201 -27 -18 201 -26 minecraft:podzol
fill -17 201 -26 -17 201 -22 minecraft:podzol
fill -19 201 -39 -17 201 -37 minecraft:dirt
fill -19 202 -39 -17 202 -37 minecraft:podzol
fill -16 201 -38 -16 201 -38 minecraft:dirt
fill -16 202 -38 -16 202 -38 minecraft:podzol
fill -19 201 -25 -18 201 -22 minecraft:dirt
fill -19 202 -25 -18 202 -22 minecraft:podzol
fill -16 201 -39 -11 207 -39 minecraft:calcite
fill -16 208 -39 -11 208 -39 minecraft:podzol
fill -7 199 -39 -6 199 -38 minecraft:clay
fill -7 200 -39 -6 200 -38 minecraft:water
fill -6 199 -37 -5 199 -37 minecraft:clay
fill -6 200 -37 -5 200 -37 minecraft:water
fill -15 199 -36 -14 199 -35 minecraft:clay
fill -15 200 -36 -14 200 -35 minecraft:water
fill -5 199 -36 -4 199 -34 minecraft:clay
fill -5 200 -36 -4 200 -34 minecraft:water
fill -16 199 -35 -16 199 -34 minecraft:clay
fill -16 200 -35 -16 200 -34 minecraft:water
fill -17 199 -34 -17 199 -34 minecraft:clay
fill -17 200 -34 -17 200 -34 minecraft:water
fill -15 199 -34 -15 199 -34 minecraft:clay
fill -15 200 -34 -15 200 -34 minecraft:water
fill -13 200 -37 -13 200 -36 minecraft:sand
fill -18 200 -34 -18 200 -33 minecraft:sand
setblock -15 200 -36 minecraft:seagrass
setblock -5 200 -37 minecraft:seagrass
setblock -5 200 -35 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -4 200 -35 minecraft:seagrass
execute positioned -8 201 -25 run function rlk:room/prop/fo_flower
execute positioned -11 201 -33 run function rlk:room/prop/p_grass
execute positioned -2 201 -24 run function rlk:room/prop/fo_flower
execute positioned -4 201 -39 run function rlk:room/prop/p_grass
execute positioned -19 201 -31 run function rlk:room/prop/fo_white
execute positioned -16 202 -36 run function rlk:room/prop/fo_flower
execute positioned -4 201 -27 run function rlk:room/prop/p_grass
setblock -16 209 -39 minecraft:birch_leaves[persistent=true] keep
setblock -15 209 -39 minecraft:short_grass keep
setblock -14 209 -39 minecraft:birch_leaves[persistent=true] keep
setblock -13 209 -39 minecraft:birch_leaves[persistent=true] keep
setblock -12 209 -39 minecraft:short_grass keep
setblock -11 209 -39 minecraft:birch_leaves[persistent=true] keep
