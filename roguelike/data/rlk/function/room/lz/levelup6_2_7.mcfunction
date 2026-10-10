# 구역 건설 (levelup6_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 1 201 -39 18 210 -22 minecraft:air
fill 1 209 -39 18 209 -22 minecraft:light[level=15]
fill 7 200 -28 11 200 -25 minecraft:coarse_dirt
fill 15 200 -32 18 200 -29 minecraft:moss_block
fill 13 200 -29 16 200 -26 minecraft:calcite
fill 0 207 -37 0 210 -37 minecraft:calcite
fill 0 207 -31 0 207 -29 minecraft:diorite
fill 0 201 -34 0 202 -29 minecraft:diorite
fill 19 207 -34 19 209 -31 minecraft:diorite
fill 19 206 -30 19 206 -28 minecraft:calcite
fill 19 209 -37 19 210 -34 minecraft:birch_leaves[persistent=true]
fill 19 201 -33 19 201 -30 minecraft:moss_block
fill 19 203 -38 19 204 -37 minecraft:calcite
fill 19 209 -32 19 210 -32 minecraft:birch_leaves[persistent=true]
fill 15 210 -40 19 210 -40 minecraft:oak_leaves[persistent=true]
fill 6 204 -40 8 205 -40 minecraft:prismarine
fill 10 207 -40 15 209 -40 minecraft:calcite
fill 10 205 -21 13 207 -21 minecraft:moss_block
fill 9 207 -21 10 207 -21 minecraft:calcite
fill 5 209 -21 8 210 -21 minecraft:oak_leaves[persistent=true]
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 1 210 -39 18 210 -22 minecraft:air
fill 2 201 -39 2 201 -37 minecraft:podzol
fill 9 201 -39 9 201 -35 minecraft:podzol
fill 3 201 -37 5 201 -37 minecraft:podzol
fill 6 201 -36 6 201 -35 minecraft:podzol
fill 7 201 -35 8 201 -35 minecraft:podzol
fill 3 201 -39 4 201 -38 minecraft:dirt
fill 3 202 -39 4 202 -38 minecraft:podzol
fill 8 201 -39 8 201 -36 minecraft:dirt
fill 8 202 -39 8 202 -36 minecraft:podzol
fill 5 201 -38 5 201 -38 minecraft:dirt
fill 5 202 -38 5 202 -38 minecraft:podzol
fill 6 201 -37 6 201 -37 minecraft:dirt
fill 6 202 -37 6 202 -37 minecraft:podzol
fill 7 201 -36 7 201 -36 minecraft:dirt
fill 7 202 -36 7 202 -36 minecraft:podzol
fill 5 201 -39 7 202 -39 minecraft:dirt
fill 5 203 -39 7 203 -39 minecraft:podzol
fill 6 201 -38 7 202 -38 minecraft:dirt
fill 6 203 -38 7 203 -38 minecraft:podzol
fill 7 201 -37 7 202 -37 minecraft:dirt
fill 7 203 -37 7 203 -37 minecraft:podzol
fill 11 186 -40 16 199 -35 minecraft:stone
fill 12 186 -39 15 186 -36 minecraft:clay
fill 12 187 -39 15 188 -36 minecraft:water
fill 12 189 -39 15 201 -36 minecraft:air
fill 18 199 -37 18 199 -27 minecraft:clay
fill 18 200 -37 18 200 -27 minecraft:water
fill 15 199 -33 17 199 -27 minecraft:clay
fill 15 200 -33 17 200 -27 minecraft:water
fill 18 200 -38 18 200 -38 minecraft:sand
fill 16 200 -26 18 200 -26 minecraft:sand
setblock 15 200 -33 minecraft:seagrass
setblock 15 200 -32 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 15 200 -30 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 16 200 -29 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 16 200 -28 minecraft:seagrass
setblock 16 200 -27 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 18 200 -33 minecraft:seagrass
execute positioned 1 201 -22 run function rlk:room/prop/fo_crates
execute positioned 12 201 -24 run function rlk:room/prop/fo_flower
execute positioned 14 201 -22 run function rlk:room/prop/p_grass
execute positioned 5 202 -37 run function rlk:room/prop/fo_flower
execute positioned 14 201 -36 run function rlk:room/prop/fo_flower
execute positioned 13 201 -29 run function rlk:room/prop/fo_flower
execute positioned 14 201 -24 run function rlk:room/prop/fo_flower
execute positioned 15 201 -36 run function rlk:room/prop/fo_white
execute positioned 17 201 -25 run function rlk:room/prop/fo_flower
execute positioned 6 201 -33 run function rlk:room/prop/fo_white
execute positioned 9 202 -38 run function rlk:room/prop/fo_flower
