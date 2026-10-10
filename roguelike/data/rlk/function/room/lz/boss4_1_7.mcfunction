# 구역 건설 (boss4_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 11 200 -17 14 200 -16 minecraft:gravel
fill 7 200 -14 9 200 -13 minecraft:moss_block
fill 0 208 -6 0 210 -6 minecraft:prismarine
fill 0 209 -5 0 210 -3 minecraft:birch_leaves[persistent=true]
fill 0 210 -17 0 210 -14 minecraft:moss_block
fill 19 210 -10 19 210 -10 minecraft:dark_prismarine
fill 19 209 -10 19 210 -5 minecraft:oak_leaves[persistent=true]
fill 19 209 -20 19 210 -15 minecraft:birch_leaves[persistent=true]
fill 15 209 -20 19 210 -20 minecraft:oak_leaves[persistent=true]
fill 15 210 -20 19 210 -20 minecraft:moss_block
fill 10 210 -20 10 210 -20 minecraft:dark_prismarine
fill 14 209 -1 14 210 -1 minecraft:oak_leaves[persistent=true]
fill 11 210 -1 14 210 -1 minecraft:birch_leaves[persistent=true]
fill 16 201 -1 19 202 -1 minecraft:diorite
fill 8 209 -1 12 210 -1 minecraft:oak_leaves[persistent=true]
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -11 5 201 -9 minecraft:podzol
fill 2 201 -10 2 201 -7 minecraft:podzol
fill 1 201 -9 1 201 -2 minecraft:podzol
fill 5 201 -8 5 201 -6 minecraft:podzol
fill 6 201 -5 12 201 -5 minecraft:podzol
fill 11 201 -4 12 201 -2 minecraft:podzol
fill 2 201 -3 2 201 -2 minecraft:podzol
fill 10 201 -3 10 201 -2 minecraft:podzol
fill 3 201 -8 4 201 -2 minecraft:dirt
fill 3 202 -8 4 202 -2 minecraft:podzol
fill 2 201 -6 2 201 -4 minecraft:dirt
fill 2 202 -6 2 202 -4 minecraft:podzol
fill 5 201 -5 5 201 -2 minecraft:dirt
fill 5 202 -5 5 202 -2 minecraft:podzol
fill 6 201 -4 10 201 -4 minecraft:dirt
fill 6 202 -4 10 202 -4 minecraft:podzol
fill 6 201 -3 9 201 -2 minecraft:dirt
fill 6 202 -3 9 202 -2 minecraft:podzol
fill 8 201 -19 13 205 -19 minecraft:calcite
fill 8 206 -19 13 206 -19 minecraft:podzol
fill 5 201 -17 6 207 -16 minecraft:calcite
fill 5 208 -17 6 208 -16 minecraft:podzol
fill 13 199 -4 18 199 -2 minecraft:clay
fill 13 200 -4 18 200 -2 minecraft:water
fill 13 200 -5 13 200 -5 minecraft:sand
setblock 16 200 -2 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned 4 201 -19 run function rlk:room/prop/fo_lamp
execute positioned 1 202 -8 run function rlk:room/prop/fo_rock
execute positioned 4 201 -12 run function rlk:room/prop/p_grass
execute positioned 13 201 -14 run function rlk:room/prop/p_grass
execute positioned 11 201 -8 run function rlk:room/prop/p_grass
execute positioned 5 201 -12 run function rlk:room/prop/fo_flower
execute positioned 5 203 -4 run function rlk:room/prop/p_grass
execute positioned 3 203 -7 run function rlk:room/prop/p_grass
execute positioned 15 201 -9 run function rlk:room/prop/fo_white
execute positioned 1 201 -11 run function rlk:room/prop/fo_white
execute positioned 5 203 -5 run function rlk:room/prop/p_grass
execute positioned 11 202 -5 run function rlk:room/prop/fo_flower
setblock 5 209 -17 minecraft:birch_leaves[persistent=true] keep
setblock 5 209 -16 minecraft:birch_leaves[persistent=true] keep
setblock 6 209 -17 minecraft:birch_leaves[persistent=true] keep
setblock 8 207 -19 minecraft:birch_leaves[persistent=true] keep
setblock 9 207 -19 minecraft:short_grass keep
setblock 10 207 -19 minecraft:birch_leaves[persistent=true] keep
setblock 11 207 -19 minecraft:short_grass keep
setblock 12 207 -19 minecraft:short_grass keep
