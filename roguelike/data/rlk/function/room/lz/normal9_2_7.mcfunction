# 구역 건설 (normal9_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 1 201 -39 18 210 -22 minecraft:air
fill 1 209 -39 18 209 -22 minecraft:light[level=15]
fill 6 200 -31 10 200 -30 minecraft:coarse_dirt
fill 14 200 -32 16 200 -30 minecraft:coarse_dirt
fill 2 200 -24 5 200 -22 minecraft:calcite
fill 7 200 -27 9 200 -25 minecraft:gravel
fill 0 206 -24 0 209 -23 minecraft:diorite
fill 0 205 -36 0 208 -34 minecraft:calcite
fill 0 201 -30 0 202 -27 minecraft:prismarine
fill 19 203 -32 19 204 -31 minecraft:prismarine
fill 19 207 -30 19 209 -28 minecraft:calcite
fill 19 209 -27 19 210 -26 minecraft:oak_leaves[persistent=true]
fill 19 203 -35 19 203 -34 minecraft:calcite
fill 19 206 -27 19 208 -27 minecraft:prismarine
fill 5 207 -40 10 209 -40 minecraft:calcite
fill 4 209 -40 8 210 -40 minecraft:oak_leaves[persistent=true]
fill 14 206 -40 17 208 -40 minecraft:moss_block
fill 15 206 -40 15 209 -40 minecraft:moss_block
fill 2 208 -40 5 210 -40 minecraft:diorite
fill 10 210 -21 15 210 -21 minecraft:calcite
fill 1 209 -21 3 210 -21 minecraft:birch_leaves[persistent=true]
fill 14 203 -21 14 206 -21 minecraft:moss_block
fill 5 209 -21 7 210 -21 minecraft:moss_block
fill 14 203 -21 19 204 -21 minecraft:prismarine
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 1 210 -39 18 210 -22 minecraft:air
fill 2 201 -35 8 201 -35 minecraft:podzol
fill 1 201 -34 5 201 -34 minecraft:podzol
fill 1 201 -33 2 201 -33 minecraft:podzol
fill 5 201 -33 5 201 -27 minecraft:podzol
fill 1 201 -32 1 201 -26 minecraft:podzol
fill 2 201 -27 2 201 -25 minecraft:podzol
fill 4 201 -27 4 201 -27 minecraft:podzol
fill 3 201 -26 3 201 -25 minecraft:podzol
fill 3 201 -33 4 201 -28 minecraft:dirt
fill 3 202 -33 4 202 -28 minecraft:podzol
fill 2 201 -32 2 201 -28 minecraft:dirt
fill 2 202 -32 2 202 -28 minecraft:podzol
fill 3 201 -27 3 201 -27 minecraft:dirt
fill 3 202 -27 3 202 -27 minecraft:podzol
fill 5 201 -37 6 207 -37 minecraft:calcite
fill 5 208 -37 6 208 -37 minecraft:podzol
fill 6 201 -36 6 207 -36 minecraft:calcite
fill 6 208 -36 6 208 -36 minecraft:podzol
fill 5 201 -36 5 207 -36 minecraft:diorite
fill 5 208 -36 5 208 -36 minecraft:podzol
fill 15 199 -39 16 199 -30 minecraft:clay
fill 15 200 -39 16 200 -30 minecraft:water
fill 17 200 -32 17 200 -29 minecraft:sand
fill 16 200 -29 16 200 -29 minecraft:sand
setblock 15 200 -38 minecraft:seagrass
setblock 15 200 -35 minecraft:seagrass
setblock 16 200 -39 minecraft:seagrass
setblock 16 200 -38 minecraft:seagrass
execute positioned 10 201 -39 run function rlk:room/prop/fo_lamp
execute positioned 3 201 -24 run function rlk:room/prop/fo_lamp
execute positioned 17 201 -28 run function rlk:room/prop/fo_rock_s
execute positioned 11 201 -36 run function rlk:room/prop/fo_col_b
execute positioned 1 201 -37 run function rlk:room/prop/fo_crates
execute positioned 3 201 -38 run function rlk:room/prop/fo_flower
execute positioned 6 201 -27 run function rlk:room/prop/p_grass
execute positioned 9 201 -33 run function rlk:room/prop/p_grass
execute positioned 12 201 -25 run function rlk:room/prop/p_grass
execute positioned 1 201 -24 run function rlk:room/prop/fo_flower
execute positioned 1 201 -22 run function rlk:room/prop/fo_flower
execute positioned 3 201 -37 run function rlk:room/prop/fo_white
execute positioned 17 201 -29 run function rlk:room/prop/fo_flower
execute positioned 18 201 -34 run function rlk:room/prop/fo_flower
execute positioned 18 201 -27 run function rlk:room/prop/fo_flower
setblock 5 209 -37 minecraft:short_grass keep
setblock 5 209 -36 minecraft:short_grass keep
setblock 6 209 -37 minecraft:short_grass keep
