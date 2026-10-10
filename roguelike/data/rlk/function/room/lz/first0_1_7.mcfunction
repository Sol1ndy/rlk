# 구역 건설 (first0_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -6 200 11 -2 200 12 minecraft:calcite
fill -9 200 11 -6 200 14 minecraft:coarse_dirt
fill -20 203 16 -20 206 17 minecraft:moss_block
fill -20 204 16 -20 207 17 minecraft:calcite
fill -20 207 8 -20 208 13 minecraft:calcite
fill -1 210 0 -1 210 3 minecraft:birch_leaves[persistent=true]
fill -1 210 3 -1 210 6 minecraft:calcite
fill -1 206 7 -1 207 12 minecraft:moss_block
fill -12 210 0 -9 210 0 minecraft:oak_leaves[persistent=true]
fill -8 201 0 -3 202 0 minecraft:prismarine
fill -18 204 0 -15 204 0 minecraft:diorite
fill -5 209 0 -1 210 0 minecraft:birch_leaves[persistent=true]
fill -12 201 19 -12 201 19 minecraft:prismarine
fill -19 206 19 -14 209 19 minecraft:dark_prismarine
fill -4 209 19 -4 210 19 minecraft:oak_leaves[persistent=true]
fill -4 210 19 -3 210 19 minecraft:prismarine
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -16 201 4 -14 201 5 minecraft:podzol
fill -18 201 5 -17 201 13 minecraft:podzol
fill -13 201 5 -12 201 5 minecraft:podzol
fill -19 201 6 -19 201 14 minecraft:podzol
fill -16 201 6 -15 201 13 minecraft:podzol
fill -18 201 14 -18 201 14 minecraft:podzol
fill -15 201 14 -15 201 18 minecraft:podzol
fill -14 201 16 -14 201 18 minecraft:podzol
fill -19 201 15 -18 201 18 minecraft:dirt
fill -19 202 15 -18 202 18 minecraft:podzol
fill -17 201 16 -16 201 18 minecraft:dirt
fill -17 202 16 -16 202 18 minecraft:podzol
fill -17 201 14 -16 207 15 minecraft:diorite
fill -17 208 14 -16 208 15 minecraft:podzol
fill -13 199 3 -7 199 4 minecraft:clay
fill -13 200 3 -7 200 4 minecraft:water
fill -13 199 15 -10 199 18 minecraft:clay
fill -13 200 15 -10 200 18 minecraft:water
fill -14 200 15 -14 200 15 minecraft:sand
fill -9 200 15 -9 200 18 minecraft:sand
setblock -13 200 15 minecraft:seagrass
setblock -11 200 17 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -8 200 4 minecraft:seagrass
execute positioned -16 202 10 run function rlk:room/prop/fo_lamp
execute positioned -17 201 3 run function rlk:room/prop/fo_flower
execute positioned -19 202 14 run function rlk:room/prop/p_grass
execute positioned -10 201 8 run function rlk:room/prop/fo_flower
execute positioned -13 201 9 run function rlk:room/prop/fo_flower
execute positioned -14 201 6 run function rlk:room/prop/fo_flower
execute positioned -2 201 17 run function rlk:room/prop/p_grass
execute positioned -3 201 3 run function rlk:room/prop/fo_flower
execute positioned -16 202 6 run function rlk:room/prop/p_grass
execute positioned -19 201 1 run function rlk:room/prop/p_grass
execute positioned -6 201 18 run function rlk:room/prop/p_grass
setblock -17 209 14 minecraft:short_grass keep
setblock -17 209 15 minecraft:short_grass keep
setblock -16 209 14 minecraft:birch_leaves[persistent=true] keep
setblock -16 209 15 minecraft:short_grass keep
