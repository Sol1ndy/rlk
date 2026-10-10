# 구역 건설 (root5_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 20 -1 200 39 minecraft:podzol
fill -20 201 20 -1 210 39 minecraft:stone
fill -19 201 21 -2 210 38 minecraft:air
fill -19 209 21 -2 209 38 minecraft:light[level=15]
fill -7 200 35 -4 200 37 minecraft:gravel
fill -8 200 28 -7 200 30 minecraft:coarse_dirt
fill -17 200 32 -15 200 33 minecraft:calcite
fill -11 200 26 -8 200 29 minecraft:moss_block
fill -20 201 26 -20 204 26 minecraft:calcite
fill -20 204 25 -20 206 30 minecraft:calcite
fill -20 209 37 -20 210 39 minecraft:oak_leaves[persistent=true]
fill -20 202 21 -20 205 21 minecraft:moss_block
fill -1 204 28 -1 205 31 minecraft:diorite
fill -1 206 22 -1 207 23 minecraft:moss_block
fill -1 203 30 -1 203 30 minecraft:dark_prismarine
fill -1 206 31 -1 208 31 minecraft:calcite
fill -1 209 25 -1 210 29 minecraft:oak_leaves[persistent=true]
fill -1 203 29 -1 203 29 minecraft:prismarine
fill -8 201 20 -3 202 20 minecraft:prismarine
fill -4 205 20 -1 206 20 minecraft:moss_block
fill -10 201 20 -5 203 20 minecraft:calcite
fill -15 210 20 -12 210 20 minecraft:oak_leaves[persistent=true]
fill -15 203 20 -10 205 20 minecraft:moss_block
fill -8 210 20 -7 210 20 minecraft:oak_leaves[persistent=true]
fill -11 209 39 -11 210 39 minecraft:birch_leaves[persistent=true]
fill -9 207 39 -5 210 39 minecraft:calcite
fill -5 202 39 -3 203 39 minecraft:calcite
fill -20 210 20 -1 210 39 minecraft:polished_deepslate
fill -19 210 21 -2 210 38 minecraft:air
fill -4 201 21 -3 201 22 minecraft:podzol
fill -2 201 22 -2 201 22 minecraft:podzol
fill -4 201 23 -4 201 26 minecraft:podzol
fill -5 201 26 -5 201 26 minecraft:podzol
fill -3 201 26 -3 201 26 minecraft:podzol
fill -2 201 27 -2 201 30 minecraft:podzol
fill -3 201 23 -2 201 25 minecraft:dirt
fill -3 202 23 -2 202 25 minecraft:podzol
fill -2 201 26 -2 201 26 minecraft:dirt
fill -2 202 26 -2 202 26 minecraft:podzol
fill -15 201 37 -12 206 37 minecraft:calcite
fill -15 207 37 -12 207 37 minecraft:podzol
fill -15 201 38 -13 206 38 minecraft:calcite
fill -15 207 38 -13 207 38 minecraft:podzol
fill -12 201 38 -12 206 38 minecraft:diorite
fill -12 207 38 -12 207 38 minecraft:podzol
fill -19 199 23 -17 199 26 minecraft:clay
fill -19 200 23 -17 200 26 minecraft:water
fill -19 199 27 -18 199 34 minecraft:clay
fill -19 200 27 -18 200 34 minecraft:water
fill -19 200 22 -17 200 22 minecraft:sand
fill -16 200 26 -16 200 26 minecraft:sand
fill -17 200 34 -17 200 35 minecraft:sand
fill -19 200 35 -18 200 35 minecraft:sand
setblock -19 200 23 minecraft:seagrass
setblock -19 200 34 minecraft:seagrass
setblock -18 200 25 minecraft:seagrass
setblock -18 200 28 minecraft:seagrass
setblock -18 200 29 minecraft:seagrass
execute positioned -9 201 21 run function rlk:room/prop/fo_flower
execute positioned -16 201 27 run function rlk:room/prop/fo_flower
execute positioned -18 201 36 run function rlk:room/prop/p_grass
execute positioned -8 201 34 run function rlk:room/prop/fo_flower
execute positioned -4 202 22 run function rlk:room/prop/fo_flower
execute positioned -16 201 21 run function rlk:room/prop/fo_flower
execute positioned -14 201 29 run function rlk:room/prop/fo_flower
execute positioned -8 201 25 run function rlk:room/prop/fo_white
setblock -15 208 37 minecraft:short_grass keep
setblock -15 208 38 minecraft:birch_leaves[persistent=true] keep
setblock -12 208 37 minecraft:short_grass keep
setblock -12 208 38 minecraft:birch_leaves[persistent=true] keep
