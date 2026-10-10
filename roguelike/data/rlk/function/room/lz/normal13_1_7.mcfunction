# 구역 건설 (normal13_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 9 200 -5 11 200 -3 minecraft:coarse_dirt
fill 12 200 -18 16 200 -16 minecraft:moss_block
fill 0 202 -19 0 202 -17 minecraft:moss_block
fill 0 209 -6 0 210 -6 minecraft:oak_leaves[persistent=true]
fill 0 203 -15 0 204 -11 minecraft:moss_block
fill 19 209 -17 19 210 -14 minecraft:oak_leaves[persistent=true]
fill 19 203 -6 19 204 -2 minecraft:calcite
fill 19 209 -5 19 210 -5 minecraft:calcite
fill 19 210 -12 19 210 -9 minecraft:calcite
fill 4 203 -20 9 203 -20 minecraft:diorite
fill 12 209 -20 15 210 -20 minecraft:oak_leaves[persistent=true]
fill 7 209 -20 10 210 -20 minecraft:oak_leaves[persistent=true]
fill 15 208 -1 17 209 -1 minecraft:calcite
fill 4 209 -1 7 210 -1 minecraft:oak_leaves[persistent=true]
fill 8 210 -1 12 210 -1 minecraft:oak_leaves[persistent=true]
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 1 201 -19 3 201 -12 minecraft:podzol
fill 16 201 -15 18 201 -15 minecraft:podzol
fill 4 201 -14 5 201 -12 minecraft:podzol
fill 15 201 -14 16 201 -7 minecraft:podzol
fill 1 201 -11 2 201 -3 minecraft:podzol
fill 5 201 -11 5 201 -3 minecraft:podzol
fill 3 201 -9 4 201 -2 minecraft:podzol
fill 16 201 -6 18 201 -5 minecraft:podzol
fill 6 201 -5 7 201 -4 minecraft:podzol
fill 17 201 -4 18 201 -4 minecraft:podzol
fill 6 201 -3 6 201 -3 minecraft:podzol
fill 2 201 -2 2 201 -2 minecraft:podzol
fill 17 201 -14 18 201 -7 minecraft:dirt
fill 17 202 -14 18 202 -7 minecraft:podzol
fill 3 201 -10 4 207 -10 minecraft:calcite
fill 3 208 -10 4 208 -10 minecraft:podzol
fill 3 201 -11 4 207 -11 minecraft:diorite
fill 3 208 -11 4 208 -11 minecraft:podzol
fill 8 199 -5 14 199 -2 minecraft:clay
fill 8 200 -5 14 200 -2 minecraft:water
fill 7 199 -3 7 199 -2 minecraft:clay
fill 7 200 -3 7 200 -2 minecraft:water
fill 15 199 -3 15 199 -2 minecraft:clay
fill 15 200 -3 15 200 -2 minecraft:water
fill 6 199 -2 6 199 -2 minecraft:clay
fill 6 200 -2 6 200 -2 minecraft:water
fill 5 200 -2 5 200 -2 minecraft:sand
fill 16 200 -2 16 200 -2 minecraft:sand
setblock 10 200 -5 minecraft:seagrass
setblock 11 200 -5 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 13 200 -5 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 15 200 -2 minecraft:sea_pickle[pickles=1,waterlogged=true]
execute positioned 16 201 -19 run function rlk:room/prop/fo_lamp
execute positioned 4 202 -6 run function rlk:room/prop/fo_lamp
execute positioned 5 202 -10 run function rlk:room/prop/p_grass
execute positioned 12 201 -10 run function rlk:room/prop/fo_white
execute positioned 7 202 -5 run function rlk:room/prop/p_grass
execute positioned 10 201 -15 run function rlk:room/prop/fo_flower
execute positioned 12 201 -14 run function rlk:room/prop/fo_flower
execute positioned 1 202 -13 run function rlk:room/prop/fo_flower
execute positioned 1 202 -4 run function rlk:room/prop/fo_flower
execute positioned 9 201 -15 run function rlk:room/prop/p_grass
execute positioned 1 202 -3 run function rlk:room/prop/fo_white
execute positioned 16 201 -19 run function rlk:room/prop/p_grass
setblock 3 209 -11 minecraft:short_grass keep
setblock 4 209 -11 minecraft:birch_leaves[persistent=true] keep
setblock 4 209 -10 minecraft:short_grass keep
