# 구역 건설 (normal9_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 9 200 -11 10 200 -9 minecraft:calcite
fill 12 200 -15 13 200 -13 minecraft:gravel
fill 0 207 -19 0 209 -19 minecraft:moss_block
fill 0 202 -20 0 203 -19 minecraft:calcite
fill 0 204 -6 0 207 -2 minecraft:dark_prismarine
fill 0 210 -18 0 210 -17 minecraft:oak_leaves[persistent=true]
fill 0 202 -2 0 205 -2 minecraft:prismarine
fill 19 210 -2 19 210 -2 minecraft:birch_leaves[persistent=true]
fill 19 209 -20 19 210 -16 minecraft:oak_leaves[persistent=true]
fill 19 205 -8 19 205 -4 minecraft:dark_prismarine
fill 6 204 -20 8 206 -20 minecraft:diorite
fill 8 210 -20 13 210 -20 minecraft:birch_leaves[persistent=true]
fill 19 210 -20 19 210 -20 minecraft:oak_leaves[persistent=true]
fill 11 210 -1 13 210 -1 minecraft:birch_leaves[persistent=true]
fill 7 205 -1 9 205 -1 minecraft:moss_block
fill 6 210 -1 8 210 -1 minecraft:oak_leaves[persistent=true]
fill 16 210 -1 18 210 -1 minecraft:diorite
fill 12 204 -1 14 206 -1 minecraft:moss_block
fill 10 207 -1 11 207 -1 minecraft:moss_block
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 5 201 -6 5 201 -5 minecraft:podzol
fill 4 201 -5 4 201 -2 minecraft:podzol
fill 6 201 -5 13 201 -5 minecraft:podzol
fill 3 201 -4 3 201 -2 minecraft:podzol
fill 10 201 -4 16 201 -2 minecraft:podzol
fill 17 201 -3 17 201 -2 minecraft:podzol
fill 5 201 -4 9 201 -2 minecraft:dirt
fill 5 202 -4 9 202 -2 minecraft:podzol
fill 1 201 -7 2 205 -7 minecraft:calcite
fill 1 206 -7 2 206 -7 minecraft:podzol
fill 1 201 -4 2 205 -2 minecraft:calcite
fill 1 206 -4 2 206 -2 minecraft:podzol
fill 1 201 -6 2 205 -5 minecraft:diorite
fill 1 206 -6 2 206 -5 minecraft:podzol
fill 3 199 -14 4 199 -9 minecraft:clay
fill 3 200 -14 4 200 -9 minecraft:water
setblock 4 200 -13 minecraft:seagrass
setblock 4 200 -10 minecraft:seagrass
execute positioned 14 201 -12 run function rlk:room/prop/p_grass
execute positioned 18 201 -17 run function rlk:room/prop/fo_flower
execute positioned 16 201 -5 run function rlk:room/prop/p_grass
execute positioned 1 201 -15 run function rlk:room/prop/fo_white
execute positioned 8 201 -17 run function rlk:room/prop/fo_flower
execute positioned 8 201 -9 run function rlk:room/prop/fo_flower
execute positioned 9 201 -8 run function rlk:room/prop/p_grass
execute positioned 17 201 -10 run function rlk:room/prop/fo_white
setblock 1 207 -7 minecraft:short_grass keep
setblock 1 207 -5 minecraft:short_grass keep
setblock 1 207 -4 minecraft:short_grass keep
setblock 1 207 -3 minecraft:birch_leaves[persistent=true] keep
setblock 1 207 -2 minecraft:birch_leaves[persistent=true] keep
setblock 2 207 -6 minecraft:short_grass keep
setblock 2 207 -3 minecraft:short_grass keep
