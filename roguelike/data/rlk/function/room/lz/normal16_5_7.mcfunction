# 구역 건설 (normal16_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 0 -21 200 19 minecraft:podzol
fill -40 201 0 -21 210 19 minecraft:stone
fill -39 201 1 -22 210 18 minecraft:air
fill -39 209 1 -22 209 18 minecraft:light[level=15]
fill -33 200 7 -31 200 8 minecraft:calcite
fill -40 210 14 -40 210 18 minecraft:prismarine
fill -40 205 6 -40 206 11 minecraft:diorite
fill -40 209 18 -40 210 18 minecraft:birch_leaves[persistent=true]
fill -21 206 3 -21 209 8 minecraft:moss_block
fill -21 205 13 -21 207 13 minecraft:diorite
fill -21 209 6 -21 210 11 minecraft:birch_leaves[persistent=true]
fill -21 210 5 -21 210 10 minecraft:birch_leaves[persistent=true]
fill -21 203 4 -21 203 5 minecraft:prismarine
fill -38 202 0 -38 205 0 minecraft:calcite
fill -30 209 0 -30 210 0 minecraft:moss_block
fill -22 209 0 -21 209 0 minecraft:diorite
fill -29 205 0 -27 206 0 minecraft:moss_block
fill -24 206 0 -21 209 0 minecraft:dark_prismarine
fill -35 206 0 -30 208 0 minecraft:diorite
fill -35 210 19 -31 210 19 minecraft:calcite
fill -30 210 19 -29 210 19 minecraft:birch_leaves[persistent=true]
fill -37 209 19 -35 210 19 minecraft:birch_leaves[persistent=true]
fill -21 205 19 -21 207 19 minecraft:moss_block
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -39 210 1 -22 210 18 minecraft:air
fill -33 201 1 -33 201 5 minecraft:podzol
fill -27 201 1 -26 201 1 minecraft:podzol
fill -26 201 2 -26 201 3 minecraft:podzol
fill -27 201 3 -27 201 5 minecraft:podzol
fill -32 201 5 -28 201 5 minecraft:podzol
fill -35 201 11 -35 201 14 minecraft:podzol
fill -36 201 12 -36 201 15 minecraft:podzol
fill -37 201 13 -37 201 18 minecraft:podzol
fill -38 201 14 -38 201 18 minecraft:podzol
fill -34 201 15 -27 201 15 minecraft:podzol
fill -27 201 16 -26 201 18 minecraft:podzol
fill -32 201 1 -28 201 4 minecraft:dirt
fill -32 202 1 -28 202 4 minecraft:podzol
fill -27 201 2 -27 201 2 minecraft:dirt
fill -27 202 2 -27 202 2 minecraft:podzol
fill -35 201 15 -35 201 17 minecraft:dirt
fill -35 202 15 -35 202 17 minecraft:podzol
fill -36 201 16 -36 201 18 minecraft:dirt
fill -36 202 16 -36 202 18 minecraft:podzol
fill -34 201 16 -28 201 17 minecraft:dirt
fill -34 202 16 -28 202 17 minecraft:podzol
fill -29 201 18 -28 201 18 minecraft:dirt
fill -29 202 18 -28 202 18 minecraft:podzol
fill -35 201 18 -30 207 18 minecraft:calcite
fill -35 208 18 -30 208 18 minecraft:podzol
fill -40 186 0 -35 199 7 minecraft:stone
fill -39 186 1 -36 186 6 minecraft:clay
fill -39 187 1 -36 188 6 minecraft:water
fill -39 189 1 -36 201 6 minecraft:air
fill -39 199 9 -35 199 10 minecraft:clay
fill -39 200 9 -35 200 10 minecraft:water
fill -39 199 11 -36 199 11 minecraft:clay
fill -39 200 11 -36 200 11 minecraft:water
fill -39 199 12 -37 199 12 minecraft:clay
fill -39 200 12 -37 200 12 minecraft:water
fill -39 199 13 -38 199 13 minecraft:clay
fill -39 200 13 -38 200 13 minecraft:water
fill -39 199 14 -39 199 14 minecraft:clay
fill -39 200 14 -39 200 14 minecraft:water
fill -39 200 15 -39 200 15 minecraft:sand
setblock -39 200 10 minecraft:seagrass
setblock -39 200 14 minecraft:seagrass
setblock -38 200 9 minecraft:seagrass
setblock -38 200 11 minecraft:seagrass
setblock -37 200 10 minecraft:seagrass
execute positioned -24 201 16 run function rlk:room/prop/fo_col_b
execute positioned -27 202 18 run function rlk:room/prop/fo_lamp
execute positioned -26 202 1 run function rlk:room/prop/fo_col_b
execute positioned -30 203 17 run function rlk:room/prop/fo_flower
execute positioned -34 201 14 run function rlk:room/prop/fo_flower
execute positioned -34 201 1 run function rlk:room/prop/p_grass
execute positioned -26 202 2 run function rlk:room/prop/fo_white
execute positioned -25 201 1 run function rlk:room/prop/p_grass
execute positioned -36 202 12 run function rlk:room/prop/fo_white
execute positioned -29 201 8 run function rlk:room/prop/fo_flower
execute positioned -25 201 10 run function rlk:room/prop/p_grass
setblock -35 209 18 minecraft:short_grass keep
setblock -32 209 18 minecraft:birch_leaves[persistent=true] keep
setblock -30 209 18 minecraft:birch_leaves[persistent=true] keep
