# 구역 건설 (root1_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 0 -21 200 19 minecraft:podzol
fill -40 201 0 -21 213 19 minecraft:stone
fill -39 201 1 -22 213 18 minecraft:air
fill -39 212 1 -22 212 18 minecraft:light[level=15]
fill -23 203 2 -22 203 3 minecraft:calcite
fill -30 203 14 -28 203 17 minecraft:coarse_dirt
fill -40 205 0 -40 207 3 minecraft:calcite
fill -40 204 8 -40 206 12 minecraft:prismarine
fill -40 206 0 -40 207 0 minecraft:calcite
fill -40 206 15 -40 207 16 minecraft:prismarine
fill -40 207 0 -40 208 2 minecraft:prismarine
fill -40 209 17 -40 211 18 minecraft:calcite
fill -21 213 2 -21 213 2 minecraft:oak_leaves[persistent=true]
fill -21 212 9 -21 213 12 minecraft:birch_leaves[persistent=true]
fill -21 212 9 -21 213 10 minecraft:birch_leaves[persistent=true]
fill -34 207 0 -34 207 0 minecraft:diorite
fill -27 202 0 -24 202 0 minecraft:moss_block
fill -28 213 0 -25 213 0 minecraft:birch_leaves[persistent=true]
fill -39 213 0 -35 213 0 minecraft:oak_leaves[persistent=true]
fill -31 202 0 -30 204 0 minecraft:moss_block
fill -30 213 19 -29 213 19 minecraft:moss_block
fill -37 213 19 -34 213 19 minecraft:oak_leaves[persistent=true]
fill -30 202 19 -28 205 19 minecraft:diorite
fill -29 204 19 -24 207 19 minecraft:diorite
fill -26 205 19 -26 205 19 minecraft:calcite
fill -32 210 19 -30 212 19 minecraft:diorite
fill -40 213 0 -21 213 19 minecraft:polished_deepslate
fill -39 213 1 -22 213 18 minecraft:air
fill -26 201 1 -22 202 18 minecraft:dirt
fill -26 203 1 -22 203 18 minecraft:podzol
fill -28 201 2 -27 202 18 minecraft:dirt
fill -28 203 2 -27 203 18 minecraft:podzol
fill -34 201 6 -29 202 18 minecraft:dirt
fill -34 203 6 -29 203 18 minecraft:podzol
fill -37 201 7 -35 202 18 minecraft:dirt
fill -37 203 7 -35 203 18 minecraft:podzol
fill -39 201 8 -39 202 18 minecraft:dirt
fill -39 203 8 -39 203 18 minecraft:podzol
fill -38 201 9 -38 202 18 minecraft:dirt
fill -38 203 9 -38 203 18 minecraft:podzol
fill -29 201 2 -29 203 5 minecraft:dirt
fill -29 204 2 -29 204 5 minecraft:podzol
fill -34 201 5 -30 203 5 minecraft:dirt
fill -34 204 5 -30 204 5 minecraft:podzol
fill -39 201 6 -39 203 7 minecraft:dirt
fill -39 204 6 -39 204 7 minecraft:podzol
fill -37 201 6 -35 203 6 minecraft:dirt
fill -37 204 6 -35 204 6 minecraft:podzol
fill -38 201 7 -38 203 8 minecraft:dirt
fill -38 204 7 -38 204 8 minecraft:podzol
fill -39 201 1 -39 204 5 minecraft:dirt
fill -39 205 1 -39 205 5 minecraft:podzol
fill -31 201 1 -30 204 4 minecraft:dirt
fill -31 205 1 -30 205 4 minecraft:podzol
fill -38 201 4 -38 204 6 minecraft:dirt
fill -38 205 4 -38 205 6 minecraft:podzol
fill -32 201 4 -32 204 4 minecraft:dirt
fill -32 205 4 -32 205 4 minecraft:podzol
fill -37 201 5 -35 204 5 minecraft:dirt
fill -37 205 5 -35 205 5 minecraft:podzol
fill -38 201 1 -32 205 2 minecraft:dirt
fill -38 206 1 -32 206 2 minecraft:podzol
fill -38 201 3 -35 205 3 minecraft:dirt
fill -38 206 3 -35 206 3 minecraft:podzol
fill -32 201 3 -32 205 3 minecraft:dirt
fill -32 206 3 -32 206 3 minecraft:podzol
fill -37 201 4 -35 205 4 minecraft:dirt
fill -37 206 4 -35 206 4 minecraft:podzol
fill -29 201 1 -27 210 1 minecraft:calcite
fill -29 211 1 -27 211 1 minecraft:podzol
fill -34 201 3 -33 210 4 minecraft:calcite
fill -34 211 3 -33 211 4 minecraft:podzol
fill -36 202 14 -35 202 15 minecraft:clay
fill -36 203 14 -35 203 15 minecraft:water
fill -34 202 15 -27 202 18 minecraft:clay
fill -34 203 15 -27 203 18 minecraft:water
fill -26 202 16 -26 202 18 minecraft:clay
fill -26 203 16 -26 203 18 minecraft:water
fill -35 203 16 -35 203 18 minecraft:sand
fill -25 203 16 -25 203 18 minecraft:sand
setblock -36 203 14 minecraft:seagrass
setblock -36 203 15 minecraft:seagrass
setblock -32 203 16 minecraft:seagrass
setblock -30 203 16 minecraft:seagrass
setblock -29 203 18 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -28 203 18 minecraft:seagrass
execute positioned -26 204 15 run function rlk:room/prop/fo_flower
execute positioned -30 206 1 run function rlk:room/prop/p_grass
execute positioned -33 204 10 run function rlk:room/prop/fo_white
execute positioned -24 204 3 run function rlk:room/prop/fo_flower
execute positioned -28 204 6 run function rlk:room/prop/fo_white
execute positioned -33 207 2 run function rlk:room/prop/fo_flower
execute positioned -26 204 6 run function rlk:room/prop/fo_flower
execute positioned -22 204 15 run function rlk:room/prop/fo_flower
execute positioned -39 205 6 run function rlk:room/prop/fo_white
setblock -34 212 3 minecraft:birch_leaves[persistent=true] keep
setblock -34 212 4 minecraft:birch_leaves[persistent=true] keep
setblock -33 212 3 minecraft:birch_leaves[persistent=true] keep
setblock -29 212 1 minecraft:short_grass keep
