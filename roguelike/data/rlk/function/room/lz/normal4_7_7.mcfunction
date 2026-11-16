# 구역 건설 (normal4_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 8 200 -14 12 200 -11 minecraft:coarse_dirt
fill 4 200 -8 8 200 -6 minecraft:coarse_dirt
fill 0 204 -9 0 204 -6 minecraft:moss_block
fill 0 201 -2 0 203 -1 minecraft:prismarine
fill 0 210 -16 0 210 -15 minecraft:oak_leaves[persistent=true]
fill 0 210 -15 0 210 -13 minecraft:birch_leaves[persistent=true]
fill 0 206 -20 0 207 -15 minecraft:calcite
fill 19 209 -8 19 210 -6 minecraft:oak_leaves[persistent=true]
fill 19 201 -10 19 203 -10 minecraft:calcite
fill 19 202 -19 19 202 -19 minecraft:diorite
fill 19 210 -15 19 210 -11 minecraft:oak_leaves[persistent=true]
fill 13 201 -20 17 202 -20 minecraft:diorite
fill 8 210 -20 11 210 -20 minecraft:birch_leaves[persistent=true]
fill 9 201 -20 10 201 -20 minecraft:diorite
fill 7 209 -1 9 210 -1 minecraft:oak_leaves[persistent=true]
fill 13 203 -1 18 205 -1 minecraft:prismarine
fill 8 209 -1 12 210 -1 minecraft:moss_block
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 15 201 -6 16 201 -2 minecraft:podzol
fill 6 201 -5 14 201 -5 minecraft:podzol
fill 3 201 -4 5 201 -4 minecraft:podzol
fill 17 201 -4 17 201 -2 minecraft:podzol
fill 3 201 -3 3 201 -2 minecraft:podzol
fill 4 201 -2 4 201 -2 minecraft:podzol
fill 14 201 -2 14 201 -2 minecraft:podzol
fill 6 201 -4 14 201 -4 minecraft:dirt
fill 6 202 -4 14 202 -4 minecraft:podzol
fill 4 201 -3 5 201 -3 minecraft:dirt
fill 4 202 -3 5 202 -3 minecraft:podzol
fill 13 201 -3 14 201 -3 minecraft:dirt
fill 13 202 -3 14 202 -3 minecraft:podzol
fill 5 201 -2 5 201 -2 minecraft:dirt
fill 5 202 -2 5 202 -2 minecraft:podzol
fill 12 201 -2 13 201 -2 minecraft:dirt
fill 12 202 -2 13 202 -2 minecraft:podzol
fill 6 201 -3 12 202 -3 minecraft:dirt
fill 6 203 -3 12 203 -3 minecraft:podzol
fill 13 201 -17 14 207 -16 minecraft:calcite
fill 13 208 -17 14 208 -16 minecraft:podzol
fill 6 201 -2 11 207 -2 minecraft:calcite
fill 6 208 -2 11 208 -2 minecraft:podzol
execute positioned 10 201 -19 run function rlk:room/prop/fo_lamp2
execute positioned 1 201 -17 run function rlk:room/prop/fo_lamp
execute positioned 5 201 -11 run function rlk:room/prop/fo_flower
execute positioned 8 201 -10 run function rlk:room/prop/p_grass
execute positioned 16 201 -17 run function rlk:room/prop/fo_white
execute positioned 16 201 -7 run function rlk:room/prop/fo_flower
execute positioned 17 201 -11 run function rlk:room/prop/fo_flower
execute positioned 10 201 -15 run function rlk:room/prop/fo_flower
execute positioned 2 201 -15 run function rlk:room/prop/fo_flower
execute positioned 13 201 -8 run function rlk:room/prop/fo_flower
setblock 7 209 -2 minecraft:birch_leaves[persistent=true] keep
setblock 9 209 -2 minecraft:birch_leaves[persistent=true] keep
setblock 10 209 -2 minecraft:short_grass keep
setblock 13 209 -17 minecraft:birch_leaves[persistent=true] keep
setblock 13 209 -16 minecraft:birch_leaves[persistent=true] keep
