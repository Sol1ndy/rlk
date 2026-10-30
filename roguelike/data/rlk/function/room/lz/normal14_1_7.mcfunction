# 구역 건설 (normal14_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 17 200 -11 18 200 -8 minecraft:moss_block
fill 12 200 -8 15 200 -7 minecraft:coarse_dirt
fill 6 200 -15 9 200 -14 minecraft:calcite
fill 0 208 -19 0 208 -16 minecraft:moss_block
fill 0 210 -9 0 210 -4 minecraft:birch_leaves[persistent=true]
fill 0 204 -6 0 207 -1 minecraft:prismarine
fill 0 201 -19 0 201 -18 minecraft:moss_block
fill 0 203 -11 0 203 -8 minecraft:calcite
fill 0 208 -12 0 210 -8 minecraft:calcite
fill 19 210 -4 19 210 -4 minecraft:prismarine
fill 19 208 -5 19 210 -4 minecraft:moss_block
fill 19 207 -15 19 208 -11 minecraft:prismarine
fill 5 202 -20 7 204 -20 minecraft:calcite
fill 0 206 -20 4 206 -20 minecraft:diorite
fill 0 206 -20 4 208 -20 minecraft:diorite
fill 0 208 -1 3 210 -1 minecraft:moss_block
fill 4 207 -1 7 207 -1 minecraft:moss_block
fill 12 205 -1 17 207 -1 minecraft:prismarine
fill 9 203 -1 13 204 -1 minecraft:prismarine
fill 13 204 -1 15 207 -1 minecraft:moss_block
fill 2 210 -1 6 210 -1 minecraft:birch_leaves[persistent=true]
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 1 201 -4 3 201 -4 minecraft:podzol
fill 3 201 -3 3 201 -2 minecraft:podzol
fill 1 201 -3 2 201 -2 minecraft:dirt
fill 1 202 -3 2 202 -2 minecraft:podzol
fill 18 201 -7 18 205 -5 minecraft:calcite
fill 18 206 -7 18 206 -5 minecraft:podzol
fill 18 201 -4 18 205 -2 minecraft:diorite
fill 18 206 -4 18 206 -2 minecraft:podzol
execute positioned 15 201 -9 run function rlk:room/prop/fo_lamp
execute positioned 15 201 -19 run function rlk:room/prop/fo_flower
execute positioned 13 201 -12 run function rlk:room/prop/fo_white
execute positioned 7 201 -16 run function rlk:room/prop/fo_flower
execute positioned 18 201 -18 run function rlk:room/prop/fo_flower
execute positioned 14 201 -7 run function rlk:room/prop/fo_flower
execute positioned 1 201 -18 run function rlk:room/prop/fo_flower
execute positioned 11 201 -16 run function rlk:room/prop/fo_flower
execute positioned 10 201 -10 run function rlk:room/prop/fo_white
execute positioned 7 201 -4 run function rlk:room/prop/fo_white
execute positioned 14 201 -17 run function rlk:room/prop/p_grass
setblock 18 207 -7 minecraft:short_grass keep
setblock 18 207 -4 minecraft:short_grass keep
setblock 18 207 -3 minecraft:short_grass keep
setblock 18 207 -2 minecraft:birch_leaves[persistent=true] keep
