# 구역 건설 (root4_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 26 200 -13 28 200 -11 minecraft:calcite
fill 20 207 -20 20 207 -20 minecraft:moss_block
fill 20 210 -18 20 210 -18 minecraft:birch_leaves[persistent=true]
fill 20 209 -16 20 210 -16 minecraft:birch_leaves[persistent=true]
fill 20 210 -13 20 210 -11 minecraft:prismarine
fill 20 204 -16 20 205 -11 minecraft:calcite
fill 39 203 -8 39 203 -3 minecraft:calcite
fill 39 210 -7 39 210 -4 minecraft:birch_leaves[persistent=true]
fill 39 209 -13 39 210 -12 minecraft:diorite
fill 24 210 -20 28 210 -20 minecraft:birch_leaves[persistent=true]
fill 31 209 -20 32 210 -20 minecraft:birch_leaves[persistent=true]
fill 34 201 -20 38 202 -20 minecraft:diorite
fill 28 204 -20 33 206 -20 minecraft:calcite
fill 35 209 -20 35 210 -20 minecraft:diorite
fill 21 204 -20 24 207 -20 minecraft:dark_prismarine
fill 27 209 -1 28 210 -1 minecraft:birch_leaves[persistent=true]
fill 35 210 -1 38 210 -1 minecraft:birch_leaves[persistent=true]
fill 29 210 -1 32 210 -1 minecraft:birch_leaves[persistent=true]
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 26 201 -5 34 201 -5 minecraft:podzol
fill 25 201 -4 26 201 -2 minecraft:podzol
fill 34 201 -4 35 201 -2 minecraft:podzol
fill 27 201 -4 33 201 -2 minecraft:dirt
fill 27 202 -4 33 202 -2 minecraft:podzol
fill 30 201 -17 30 205 -16 minecraft:calcite
fill 30 206 -17 30 206 -16 minecraft:podzol
fill 29 201 -17 29 205 -16 minecraft:diorite
fill 29 206 -17 29 206 -16 minecraft:podzol
fill 21 199 -4 24 199 -2 minecraft:clay
fill 21 200 -4 24 200 -2 minecraft:water
setblock 22 200 -4 minecraft:seagrass
setblock 22 200 -2 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 23 200 -2 minecraft:seagrass
execute positioned 31 201 -19 run function rlk:room/prop/fo_lamp2
execute positioned 24 201 -15 run function rlk:room/prop/fo_white
execute positioned 28 201 -9 run function rlk:room/prop/fo_flower
execute positioned 36 201 -18 run function rlk:room/prop/fo_flower
execute positioned 34 202 -3 run function rlk:room/prop/fo_flower
execute positioned 29 201 -13 run function rlk:room/prop/fo_flower
execute positioned 34 202 -4 run function rlk:room/prop/fo_flower
execute positioned 26 202 -2 run function rlk:room/prop/fo_flower
execute positioned 28 201 -7 run function rlk:room/prop/p_grass
execute positioned 36 201 -18 run function rlk:room/prop/fo_flower
execute positioned 23 201 -12 run function rlk:room/prop/p_grass
setblock 29 207 -17 minecraft:birch_leaves[persistent=true] keep
setblock 29 207 -16 minecraft:short_grass keep
setblock 30 207 -17 minecraft:short_grass keep
