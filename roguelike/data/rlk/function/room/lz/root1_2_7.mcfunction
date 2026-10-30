# 구역 건설 (root1_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 0 -21 200 19 minecraft:podzol
fill -40 201 0 -21 210 19 minecraft:stone
fill -39 201 1 -22 210 18 minecraft:air
fill -39 209 1 -22 209 18 minecraft:light[level=15]
fill -23 200 2 -22 200 3 minecraft:calcite
fill -30 200 14 -28 200 17 minecraft:coarse_dirt
fill -40 202 0 -40 204 3 minecraft:calcite
fill -40 201 8 -40 203 12 minecraft:prismarine
fill -40 203 0 -40 204 0 minecraft:calcite
fill -40 203 15 -40 204 16 minecraft:prismarine
fill -40 204 0 -40 205 2 minecraft:prismarine
fill -40 206 17 -40 208 18 minecraft:calcite
fill -21 210 2 -21 210 2 minecraft:oak_leaves[persistent=true]
fill -21 209 9 -21 210 12 minecraft:birch_leaves[persistent=true]
fill -21 209 9 -21 210 10 minecraft:birch_leaves[persistent=true]
fill -34 204 0 -34 204 0 minecraft:diorite
fill -28 210 0 -25 210 0 minecraft:birch_leaves[persistent=true]
fill -39 210 0 -35 210 0 minecraft:oak_leaves[persistent=true]
fill -31 201 0 -30 201 0 minecraft:moss_block
fill -30 210 19 -29 210 19 minecraft:moss_block
fill -37 210 19 -34 210 19 minecraft:oak_leaves[persistent=true]
fill -30 201 19 -28 202 19 minecraft:diorite
fill -29 201 19 -24 204 19 minecraft:diorite
fill -26 202 19 -26 202 19 minecraft:calcite
fill -32 207 19 -30 209 19 minecraft:diorite
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -39 210 1 -22 210 18 minecraft:air
fill -29 201 2 -29 201 5 minecraft:podzol
fill -34 201 5 -30 201 5 minecraft:podzol
fill -39 201 6 -39 201 7 minecraft:podzol
fill -37 201 6 -35 201 6 minecraft:podzol
fill -38 201 7 -38 201 8 minecraft:podzol
fill -39 201 1 -39 201 5 minecraft:dirt
fill -39 202 1 -39 202 5 minecraft:podzol
fill -31 201 1 -30 201 4 minecraft:dirt
fill -31 202 1 -30 202 4 minecraft:podzol
fill -38 201 4 -38 201 6 minecraft:dirt
fill -38 202 4 -38 202 6 minecraft:podzol
fill -32 201 4 -32 201 4 minecraft:dirt
fill -32 202 4 -32 202 4 minecraft:podzol
fill -37 201 5 -35 201 5 minecraft:dirt
fill -37 202 5 -35 202 5 minecraft:podzol
fill -38 201 1 -32 202 2 minecraft:dirt
fill -38 203 1 -32 203 2 minecraft:podzol
fill -38 201 3 -35 202 3 minecraft:dirt
fill -38 203 3 -35 203 3 minecraft:podzol
fill -32 201 3 -32 202 3 minecraft:dirt
fill -32 203 3 -32 203 3 minecraft:podzol
fill -37 201 4 -35 202 4 minecraft:dirt
fill -37 203 4 -35 203 4 minecraft:podzol
fill -29 201 1 -27 207 1 minecraft:calcite
fill -29 208 1 -27 208 1 minecraft:podzol
fill -34 201 3 -33 207 4 minecraft:calcite
fill -34 208 3 -33 208 4 minecraft:podzol
fill -36 199 14 -35 199 15 minecraft:clay
fill -36 200 14 -35 200 15 minecraft:water
fill -34 199 15 -27 199 18 minecraft:clay
fill -34 200 15 -27 200 18 minecraft:water
fill -26 199 16 -26 199 18 minecraft:clay
fill -26 200 16 -26 200 18 minecraft:water
fill -35 200 16 -35 200 18 minecraft:sand
fill -25 200 16 -25 200 18 minecraft:sand
setblock -36 200 14 minecraft:seagrass
setblock -36 200 15 minecraft:seagrass
setblock -32 200 16 minecraft:seagrass
setblock -30 200 16 minecraft:seagrass
setblock -29 200 18 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -28 200 18 minecraft:seagrass
execute positioned -26 201 15 run function rlk:room/prop/fo_flower
execute positioned -30 203 1 run function rlk:room/prop/p_grass
execute positioned -33 201 10 run function rlk:room/prop/fo_white
execute positioned -24 201 3 run function rlk:room/prop/fo_flower
execute positioned -28 201 6 run function rlk:room/prop/fo_white
execute positioned -33 204 2 run function rlk:room/prop/fo_flower
execute positioned -26 201 6 run function rlk:room/prop/fo_flower
execute positioned -22 201 15 run function rlk:room/prop/fo_flower
execute positioned -39 202 6 run function rlk:room/prop/fo_white
setblock -34 209 3 minecraft:birch_leaves[persistent=true] keep
setblock -34 209 4 minecraft:birch_leaves[persistent=true] keep
setblock -33 209 3 minecraft:birch_leaves[persistent=true] keep
setblock -29 209 1 minecraft:short_grass keep
