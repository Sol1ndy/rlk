# 구역 건설 (normal16_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 11 200 7 14 200 10 minecraft:moss_block
fill 9 200 9 10 200 10 minecraft:calcite
fill 0 203 6 0 205 9 minecraft:diorite
fill 0 209 0 0 210 1 minecraft:birch_leaves[persistent=true]
fill 0 210 0 0 210 0 minecraft:calcite
fill 19 209 11 19 210 12 minecraft:diorite
fill 19 209 9 19 210 9 minecraft:oak_leaves[persistent=true]
fill 19 209 7 19 210 9 minecraft:oak_leaves[persistent=true]
fill 19 210 0 19 210 1 minecraft:birch_leaves[persistent=true]
fill 19 210 6 19 210 10 minecraft:oak_leaves[persistent=true]
fill 19 210 15 19 210 15 minecraft:oak_leaves[persistent=true]
fill 2 207 0 4 209 0 minecraft:prismarine
fill 0 205 0 3 205 0 minecraft:diorite
fill 17 210 0 19 210 0 minecraft:diorite
fill 7 203 0 9 203 0 minecraft:diorite
fill 11 206 0 16 209 0 minecraft:diorite
fill 12 205 0 12 207 0 minecraft:prismarine
fill 12 205 19 17 205 19 minecraft:dark_prismarine
fill 15 209 19 18 210 19 minecraft:birch_leaves[persistent=true]
fill 11 209 19 13 210 19 minecraft:oak_leaves[persistent=true]
fill 7 210 19 11 210 19 minecraft:oak_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 13 201 1 14 201 5 minecraft:podzol
fill 15 201 6 18 201 6 minecraft:podzol
fill 15 201 7 16 201 7 minecraft:podzol
fill 15 201 1 18 201 5 minecraft:dirt
fill 15 202 1 18 202 5 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:calcite
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:calcite
fill 12 208 4 12 208 4 minecraft:podzol
fill 17 201 7 18 207 9 minecraft:calcite
fill 17 208 7 18 208 9 minecraft:podzol
fill 17 201 10 17 207 10 minecraft:calcite
fill 17 208 10 17 208 10 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:diorite
fill 12 208 3 12 208 3 minecraft:podzol
fill 18 201 10 18 207 10 minecraft:diorite
fill 18 208 10 18 208 10 minecraft:podzol
execute positioned 15 201 14 run function rlk:room/prop/fo_crates
execute positioned 1 201 18 run function rlk:room/prop/fo_ruin_x
execute positioned 14 201 11 run function rlk:room/prop/fo_flower
execute positioned 2 201 6 run function rlk:room/prop/fo_flower
execute positioned 17 201 17 run function rlk:room/prop/p_grass
execute positioned 4 201 6 run function rlk:room/prop/p_grass
execute positioned 14 201 18 run function rlk:room/prop/p_grass
execute positioned 4 201 3 run function rlk:room/prop/p_grass
execute positioned 11 201 9 run function rlk:room/prop/fo_flower
execute positioned 16 202 6 run function rlk:room/prop/fo_flower
execute positioned 3 201 17 run function rlk:room/prop/fo_white
setblock 11 209 4 minecraft:birch_leaves[persistent=true] keep
setblock 12 209 3 minecraft:birch_leaves[persistent=true] keep
setblock 12 209 4 minecraft:birch_leaves[persistent=true] keep
setblock 17 209 7 minecraft:short_grass keep
setblock 17 209 9 minecraft:short_grass keep
setblock 17 209 10 minecraft:birch_leaves[persistent=true] keep
setblock 18 209 7 minecraft:short_grass keep
setblock 18 209 8 minecraft:birch_leaves[persistent=true] keep
