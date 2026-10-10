# 구역 건설 (root4_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 213 -1 minecraft:stone
fill 21 201 -19 38 213 -2 minecraft:air
fill 21 212 -19 38 212 -2 minecraft:light[level=15]
fill 26 203 -13 28 203 -11 minecraft:calcite
fill 20 210 -20 20 210 -20 minecraft:moss_block
fill 20 213 -18 20 213 -18 minecraft:birch_leaves[persistent=true]
fill 20 212 -16 20 213 -16 minecraft:birch_leaves[persistent=true]
fill 20 213 -13 20 213 -11 minecraft:prismarine
fill 20 207 -16 20 208 -11 minecraft:calcite
fill 39 206 -8 39 206 -3 minecraft:calcite
fill 39 213 -7 39 213 -4 minecraft:birch_leaves[persistent=true]
fill 39 212 -13 39 213 -12 minecraft:diorite
fill 24 213 -20 28 213 -20 minecraft:birch_leaves[persistent=true]
fill 31 212 -20 32 213 -20 minecraft:birch_leaves[persistent=true]
fill 34 204 -20 38 205 -20 minecraft:diorite
fill 28 207 -20 33 209 -20 minecraft:calcite
fill 35 212 -20 35 213 -20 minecraft:diorite
fill 21 207 -20 24 210 -20 minecraft:dark_prismarine
fill 27 212 -1 28 213 -1 minecraft:birch_leaves[persistent=true]
fill 35 213 -1 38 213 -1 minecraft:birch_leaves[persistent=true]
fill 29 213 -1 32 213 -1 minecraft:birch_leaves[persistent=true]
fill 20 213 -20 39 213 -1 minecraft:polished_deepslate
fill 21 213 -19 38 213 -2 minecraft:air
fill 21 201 -19 38 202 -18 minecraft:dirt
fill 21 203 -19 38 203 -18 minecraft:podzol
fill 21 201 -17 28 202 -6 minecraft:dirt
fill 21 203 -17 28 203 -6 minecraft:podzol
fill 31 201 -17 38 202 -6 minecraft:dirt
fill 31 203 -17 38 203 -6 minecraft:podzol
fill 29 201 -15 30 202 -6 minecraft:dirt
fill 29 203 -15 30 203 -6 minecraft:podzol
fill 21 201 -5 25 202 -5 minecraft:dirt
fill 21 203 -5 25 203 -5 minecraft:podzol
fill 35 201 -5 38 202 -5 minecraft:dirt
fill 35 203 -5 38 203 -5 minecraft:podzol
fill 21 201 -4 24 202 -2 minecraft:dirt
fill 21 203 -4 24 203 -2 minecraft:podzol
fill 36 201 -4 38 202 -2 minecraft:dirt
fill 36 203 -4 38 203 -2 minecraft:podzol
fill 26 201 -5 34 203 -5 minecraft:dirt
fill 26 204 -5 34 204 -5 minecraft:podzol
fill 25 201 -4 26 203 -2 minecraft:dirt
fill 25 204 -4 26 204 -2 minecraft:podzol
fill 34 201 -4 35 203 -2 minecraft:dirt
fill 34 204 -4 35 204 -2 minecraft:podzol
fill 27 201 -4 33 204 -2 minecraft:dirt
fill 27 205 -4 33 205 -2 minecraft:podzol
fill 30 201 -17 30 208 -16 minecraft:calcite
fill 30 209 -17 30 209 -16 minecraft:podzol
fill 29 201 -17 29 208 -16 minecraft:diorite
fill 29 209 -17 29 209 -16 minecraft:podzol
fill 21 202 -4 24 202 -2 minecraft:clay
fill 21 203 -4 24 203 -2 minecraft:water
setblock 22 203 -4 minecraft:seagrass
setblock 22 203 -2 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 23 203 -2 minecraft:seagrass
execute positioned 31 204 -19 run function rlk:room/prop/fo_lamp2
execute positioned 24 204 -15 run function rlk:room/prop/fo_white
execute positioned 28 204 -9 run function rlk:room/prop/fo_flower
execute positioned 36 204 -18 run function rlk:room/prop/fo_flower
execute positioned 34 205 -3 run function rlk:room/prop/fo_flower
execute positioned 29 204 -13 run function rlk:room/prop/fo_flower
execute positioned 34 205 -4 run function rlk:room/prop/fo_flower
execute positioned 26 205 -2 run function rlk:room/prop/fo_flower
execute positioned 28 204 -7 run function rlk:room/prop/p_grass
execute positioned 36 204 -18 run function rlk:room/prop/fo_flower
execute positioned 23 204 -12 run function rlk:room/prop/p_grass
setblock 29 210 -17 minecraft:birch_leaves[persistent=true] keep
setblock 29 210 -16 minecraft:short_grass keep
setblock 30 210 -17 minecraft:short_grass keep
