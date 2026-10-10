# 구역 건설 (boss0_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -12 200 1 -10 200 3 minecraft:moss_block
fill -5 200 1 -3 200 4 minecraft:moss_block
fill -9 200 8 -6 200 11 minecraft:coarse_dirt
fill -20 207 3 -20 207 5 minecraft:dark_prismarine
fill -20 209 0 -20 210 0 minecraft:birch_leaves[persistent=true]
fill -20 205 2 -20 208 6 minecraft:calcite
fill -1 210 2 -1 210 7 minecraft:birch_leaves[persistent=true]
fill -1 210 9 -1 210 9 minecraft:calcite
fill -1 203 8 -1 206 10 minecraft:moss_block
fill -10 210 0 -10 210 0 minecraft:birch_leaves[persistent=true]
fill -15 210 0 -14 210 0 minecraft:moss_block
fill -12 209 0 -8 210 0 minecraft:birch_leaves[persistent=true]
fill -19 209 0 -15 210 0 minecraft:birch_leaves[persistent=true]
fill -4 210 0 -1 210 0 minecraft:oak_leaves[persistent=true]
fill -18 209 19 -13 210 19 minecraft:birch_leaves[persistent=true]
fill -12 202 19 -10 202 19 minecraft:diorite
fill -10 209 19 -10 210 19 minecraft:oak_leaves[persistent=true]
fill -11 208 19 -8 209 19 minecraft:moss_block
fill -10 202 19 -9 203 19 minecraft:moss_block
fill -10 210 19 -7 210 19 minecraft:birch_leaves[persistent=true]
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -15 201 11 -15 201 14 minecraft:podzol
fill -17 201 12 -16 201 13 minecraft:podzol
fill -17 201 14 -17 201 15 minecraft:podzol
fill -14 201 15 -7 201 15 minecraft:podzol
fill -8 201 16 -7 201 18 minecraft:podzol
fill -16 201 14 -16 201 18 minecraft:dirt
fill -16 202 14 -16 202 18 minecraft:podzol
fill -15 201 15 -15 201 18 minecraft:dirt
fill -15 202 15 -15 202 18 minecraft:podzol
fill -17 201 16 -17 201 18 minecraft:dirt
fill -17 202 16 -17 202 18 minecraft:podzol
fill -14 201 16 -9 201 18 minecraft:dirt
fill -14 202 16 -9 202 18 minecraft:podzol
fill -17 201 7 -16 205 8 minecraft:diorite
fill -17 206 7 -16 206 8 minecraft:podzol
fill -19 201 13 -18 206 13 minecraft:calcite
fill -19 207 13 -18 207 13 minecraft:podzol
fill -19 201 14 -19 206 18 minecraft:calcite
fill -19 207 14 -19 207 18 minecraft:podzol
fill -18 201 18 -18 206 18 minecraft:calcite
fill -18 207 18 -18 207 18 minecraft:podzol
fill -18 201 14 -18 206 17 minecraft:diorite
fill -18 207 14 -18 207 17 minecraft:podzol
fill -4 199 4 -2 199 15 minecraft:clay
fill -4 200 4 -2 200 15 minecraft:water
fill -5 199 6 -5 199 14 minecraft:clay
fill -5 200 6 -5 200 14 minecraft:water
fill -4 200 3 -2 200 3 minecraft:sand
fill -6 200 15 -5 200 15 minecraft:sand
fill -5 200 16 -2 200 16 minecraft:sand
setblock -5 200 8 minecraft:seagrass
setblock -5 200 13 minecraft:seagrass
setblock -4 200 8 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -3 200 10 minecraft:seagrass
setblock -2 200 11 minecraft:seagrass
setblock -2 200 13 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned -3 201 18 run function rlk:room/prop/fo_rock_s
execute positioned -9 201 1 run function rlk:room/prop/p_grass
execute positioned -14 201 14 run function rlk:room/prop/p_grass
execute positioned -16 203 18 run function rlk:room/prop/fo_flower
execute positioned -8 201 3 run function rlk:room/prop/fo_white
execute positioned -19 201 12 run function rlk:room/prop/fo_white
execute positioned -6 201 11 run function rlk:room/prop/p_grass
execute positioned -11 201 12 run function rlk:room/prop/fo_white
execute positioned -6 201 9 run function rlk:room/prop/fo_flower
execute positioned -10 201 4 run function rlk:room/prop/p_grass
execute positioned -13 201 8 run function rlk:room/prop/fo_white
setblock -19 208 15 minecraft:birch_leaves[persistent=true] keep
setblock -18 208 13 minecraft:short_grass keep
setblock -18 208 14 minecraft:birch_leaves[persistent=true] keep
setblock -18 208 16 minecraft:birch_leaves[persistent=true] keep
setblock -18 208 17 minecraft:short_grass keep
setblock -18 208 18 minecraft:birch_leaves[persistent=true] keep
setblock -17 207 7 minecraft:short_grass keep
setblock -16 207 7 minecraft:short_grass keep
