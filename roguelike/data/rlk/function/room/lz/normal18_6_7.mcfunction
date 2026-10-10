# 구역 건설 (normal18_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 10 200 7 11 200 9 minecraft:coarse_dirt
fill 3 200 12 7 200 13 minecraft:moss_block
fill 0 207 3 0 208 3 minecraft:calcite
fill 0 210 15 0 210 15 minecraft:diorite
fill 0 208 5 0 209 8 minecraft:dark_prismarine
fill 0 208 5 0 210 8 minecraft:moss_block
fill 0 202 11 0 203 13 minecraft:calcite
fill 19 205 12 19 205 17 minecraft:moss_block
fill 19 202 16 19 204 19 minecraft:moss_block
fill 19 204 12 19 207 16 minecraft:calcite
fill 19 209 11 19 210 14 minecraft:oak_leaves[persistent=true]
fill 19 209 16 19 210 17 minecraft:birch_leaves[persistent=true]
fill 6 208 0 11 208 0 minecraft:diorite
fill 0 206 0 1 208 0 minecraft:prismarine
fill 0 206 0 4 208 0 minecraft:diorite
fill 0 207 19 4 208 19 minecraft:calcite
fill 8 201 19 8 203 19 minecraft:diorite
fill 10 204 19 11 206 19 minecraft:diorite
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 15 201 5 18 201 6 minecraft:podzol
fill 18 201 7 18 201 15 minecraft:podzol
fill 15 201 14 17 201 15 minecraft:podzol
fill 7 201 3 8 205 4 minecraft:calcite
fill 7 206 3 8 206 4 minecraft:podzol
fill 10 201 17 11 206 18 minecraft:calcite
fill 10 207 17 11 207 18 minecraft:podzol
fill 12 201 17 12 206 18 minecraft:diorite
fill 12 207 17 12 207 18 minecraft:podzol
fill 14 199 3 18 199 4 minecraft:clay
fill 14 200 3 18 200 4 minecraft:water
fill 13 199 4 13 199 5 minecraft:clay
fill 13 200 4 13 200 5 minecraft:water
fill 14 199 5 14 199 5 minecraft:clay
fill 14 200 5 14 200 5 minecraft:water
fill 13 200 2 18 200 2 minecraft:sand
fill 12 200 3 13 200 3 minecraft:sand
fill 12 200 4 12 200 5 minecraft:sand
setblock 17 200 3 minecraft:seagrass
execute positioned 18 202 11 run function rlk:room/prop/fo_col_a
execute positioned 16 202 6 run function rlk:room/prop/fo_flower
execute positioned 13 201 16 run function rlk:room/prop/fo_flower
execute positioned 17 201 16 run function rlk:room/prop/p_grass
execute positioned 6 201 3 run function rlk:room/prop/p_grass
execute positioned 17 201 16 run function rlk:room/prop/p_grass
execute positioned 3 201 16 run function rlk:room/prop/fo_flower
execute positioned 9 201 11 run function rlk:room/prop/fo_flower
execute positioned 7 201 1 run function rlk:room/prop/fo_flower
execute positioned 16 201 7 run function rlk:room/prop/fo_white
execute positioned 1 201 11 run function rlk:room/prop/p_grass
setblock 7 207 3 minecraft:birch_leaves[persistent=true] keep
setblock 8 207 3 minecraft:birch_leaves[persistent=true] keep
setblock 8 207 4 minecraft:short_grass keep
setblock 10 208 18 minecraft:short_grass keep
setblock 11 208 18 minecraft:birch_leaves[persistent=true] keep
setblock 12 208 17 minecraft:short_grass keep
