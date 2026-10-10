# 구역 건설 (normal3_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:stone
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 9 200 24 11 200 27 minecraft:moss_block
fill 6 200 26 9 200 29 minecraft:gravel
fill 0 203 26 0 203 29 minecraft:diorite
fill 0 210 20 0 210 25 minecraft:oak_leaves[persistent=true]
fill 0 210 35 0 210 35 minecraft:oak_leaves[persistent=true]
fill 0 210 32 0 210 36 minecraft:birch_leaves[persistent=true]
fill 0 209 33 0 210 36 minecraft:oak_leaves[persistent=true]
fill 0 206 28 0 209 29 minecraft:calcite
fill 19 201 32 19 202 37 minecraft:calcite
fill 19 201 30 19 203 34 minecraft:calcite
fill 19 209 30 19 210 32 minecraft:birch_leaves[persistent=true]
fill 19 210 20 19 210 20 minecraft:oak_leaves[persistent=true]
fill 19 208 28 19 208 33 minecraft:moss_block
fill 0 210 20 2 210 20 minecraft:moss_block
fill 6 205 20 9 207 20 minecraft:moss_block
fill 7 209 20 7 210 20 minecraft:moss_block
fill 2 202 20 2 202 20 minecraft:calcite
fill 2 209 39 4 210 39 minecraft:diorite
fill 2 210 39 4 210 39 minecraft:birch_leaves[persistent=true]
fill 17 207 39 17 210 39 minecraft:calcite
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 3 201 21 3 201 25 minecraft:podzol
fill 4 201 26 5 201 26 minecraft:podzol
fill 3 201 27 4 201 27 minecraft:podzol
fill 1 201 28 2 201 28 minecraft:podzol
fill 2 201 21 2 201 27 minecraft:dirt
fill 2 202 21 2 202 27 minecraft:podzol
fill 1 201 26 1 201 27 minecraft:dirt
fill 1 202 26 1 202 27 minecraft:podzol
fill 3 201 26 3 201 26 minecraft:dirt
fill 3 202 26 3 202 26 minecraft:podzol
fill 1 201 21 1 202 25 minecraft:dirt
fill 1 203 21 1 203 25 minecraft:podzol
fill 5 201 38 5 205 38 minecraft:calcite
fill 5 206 38 5 206 38 minecraft:podzol
fill 5 201 37 7 205 37 minecraft:diorite
fill 5 206 37 7 206 37 minecraft:podzol
fill 6 201 38 7 205 38 minecraft:diorite
fill 6 206 38 7 206 38 minecraft:podzol
fill 3 199 28 5 199 33 minecraft:clay
fill 3 200 28 5 200 33 minecraft:water
setblock 4 200 33 minecraft:seagrass
execute positioned 1 204 21 run function rlk:room/prop/fo_lamp
execute positioned 9 201 24 run function rlk:room/prop/fo_white
execute positioned 18 201 33 run function rlk:room/prop/fo_flower
execute positioned 14 201 24 run function rlk:room/prop/fo_flower
execute positioned 1 202 28 run function rlk:room/prop/fo_white
execute positioned 14 201 35 run function rlk:room/prop/p_grass
execute positioned 2 201 35 run function rlk:room/prop/p_grass
execute positioned 2 201 29 run function rlk:room/prop/fo_white
setblock 5 207 37 minecraft:short_grass keep
setblock 5 207 38 minecraft:short_grass keep
setblock 6 207 37 minecraft:short_grass keep
setblock 7 207 37 minecraft:short_grass keep
setblock 7 207 38 minecraft:short_grass keep
