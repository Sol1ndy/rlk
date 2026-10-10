# 구역 건설 (root3_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 32 200 -16 33 200 -14 minecraft:calcite
fill 30 200 -18 32 200 -16 minecraft:gravel
fill 25 200 -17 27 200 -16 minecraft:gravel
fill 20 210 -16 20 210 -16 minecraft:birch_leaves[persistent=true]
fill 20 210 -5 20 210 -1 minecraft:birch_leaves[persistent=true]
fill 20 202 -5 20 204 -5 minecraft:calcite
fill 20 208 -17 20 210 -16 minecraft:dark_prismarine
fill 20 204 -14 20 204 -13 minecraft:moss_block
fill 20 210 -13 20 210 -9 minecraft:birch_leaves[persistent=true]
fill 39 209 -5 39 210 -3 minecraft:oak_leaves[persistent=true]
fill 39 205 -16 39 207 -14 minecraft:moss_block
fill 39 209 -16 39 210 -15 minecraft:birch_leaves[persistent=true]
fill 25 207 -20 29 207 -20 minecraft:moss_block
fill 32 207 -20 37 210 -20 minecraft:dark_prismarine
fill 36 210 -20 38 210 -20 minecraft:oak_leaves[persistent=true]
fill 37 204 -20 38 207 -20 minecraft:calcite
fill 24 206 -1 29 207 -1 minecraft:prismarine
fill 33 202 -1 38 203 -1 minecraft:moss_block
fill 30 209 -1 35 210 -1 minecraft:oak_leaves[persistent=true]
fill 21 209 -1 26 210 -1 minecraft:birch_leaves[persistent=true]
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 38 201 -8 38 201 -3 minecraft:podzol
fill 35 201 -6 37 201 -6 minecraft:podzol
fill 31 201 -5 34 201 -5 minecraft:podzol
fill 37 201 -5 37 201 -3 minecraft:podzol
fill 30 201 -4 31 201 -4 minecraft:podzol
fill 31 201 -3 31 201 -2 minecraft:podzol
fill 32 201 -2 32 201 -2 minecraft:podzol
fill 35 201 -5 36 201 -3 minecraft:dirt
fill 35 202 -5 36 202 -3 minecraft:podzol
fill 32 201 -4 34 201 -3 minecraft:dirt
fill 32 202 -4 34 202 -3 minecraft:podzol
fill 33 201 -2 35 201 -2 minecraft:dirt
fill 33 202 -2 35 202 -2 minecraft:podzol
fill 36 201 -2 38 206 -2 minecraft:diorite
fill 36 207 -2 38 207 -2 minecraft:podzol
fill 28 201 -17 29 207 -16 minecraft:diorite
fill 28 208 -17 29 208 -16 minecraft:podzol
fill 35 199 -19 36 199 -14 minecraft:clay
fill 35 200 -19 36 200 -14 minecraft:water
fill 27 199 -5 29 199 -2 minecraft:clay
fill 27 200 -5 29 200 -2 minecraft:water
fill 30 199 -3 30 199 -2 minecraft:clay
fill 30 200 -3 30 200 -2 minecraft:water
fill 26 200 -5 26 200 -2 minecraft:sand
fill 30 200 -5 30 200 -5 minecraft:sand
setblock 27 200 -4 minecraft:seagrass
setblock 28 200 -3 minecraft:seagrass
setblock 29 200 -4 minecraft:seagrass
setblock 29 200 -3 minecraft:seagrass
setblock 29 200 -2 minecraft:seagrass
setblock 35 200 -16 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 36 200 -16 minecraft:seagrass
setblock 36 200 -14 minecraft:seagrass
execute positioned 24 201 -12 run function rlk:room/prop/p_grass
execute positioned 29 201 -9 run function rlk:room/prop/fo_flower
execute positioned 28 201 -12 run function rlk:room/prop/p_grass
execute positioned 32 203 -4 run function rlk:room/prop/fo_white
execute positioned 32 201 -14 run function rlk:room/prop/p_grass
execute positioned 31 201 -7 run function rlk:room/prop/p_grass
execute positioned 23 201 -2 run function rlk:room/prop/fo_flower
setblock 28 209 -17 minecraft:short_grass keep
setblock 28 209 -16 minecraft:short_grass keep
setblock 36 208 -2 minecraft:birch_leaves[persistent=true] keep
setblock 37 208 -2 minecraft:birch_leaves[persistent=true] keep
setblock 38 208 -2 minecraft:short_grass keep
