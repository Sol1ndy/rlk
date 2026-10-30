# 구역 건설 (normal11_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 210 39 minecraft:stone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -29 200 22 -25 200 24 minecraft:gravel
fill -32 200 28 -29 200 31 minecraft:moss_block
fill -40 209 25 -40 210 26 minecraft:moss_block
fill -40 210 28 -40 210 33 minecraft:birch_leaves[persistent=true]
fill -40 209 22 -40 210 26 minecraft:oak_leaves[persistent=true]
fill -40 209 23 -40 210 26 minecraft:oak_leaves[persistent=true]
fill -21 201 22 -21 201 27 minecraft:prismarine
fill -21 209 35 -21 210 38 minecraft:moss_block
fill -21 201 20 -21 202 21 minecraft:diorite
fill -21 202 32 -21 203 37 minecraft:moss_block
fill -39 204 20 -37 207 20 minecraft:diorite
fill -34 203 20 -32 204 20 minecraft:prismarine
fill -25 204 20 -21 207 20 minecraft:diorite
fill -34 210 20 -32 210 20 minecraft:birch_leaves[persistent=true]
fill -29 209 20 -27 210 20 minecraft:birch_leaves[persistent=true]
fill -24 210 39 -22 210 39 minecraft:birch_leaves[persistent=true]
fill -31 209 39 -27 210 39 minecraft:birch_leaves[persistent=true]
fill -31 205 39 -30 206 39 minecraft:calcite
fill -33 204 39 -28 206 39 minecraft:moss_block
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -29 201 35 -27 201 38 minecraft:podzol
fill -26 201 36 -22 201 38 minecraft:podzol
fill -34 201 38 -30 206 38 minecraft:calcite
fill -34 207 38 -30 207 38 minecraft:podzol
fill -39 199 21 -37 199 31 minecraft:clay
fill -39 200 21 -37 200 31 minecraft:water
fill -36 199 26 -35 199 31 minecraft:clay
fill -36 200 26 -35 200 31 minecraft:water
fill -37 199 32 -36 199 35 minecraft:clay
fill -37 200 32 -36 200 35 minecraft:water
fill -36 199 36 -35 199 36 minecraft:clay
fill -36 200 36 -35 200 36 minecraft:water
fill -39 200 32 -38 200 32 minecraft:sand
fill -35 200 32 -35 200 32 minecraft:sand
setblock -39 200 28 minecraft:seagrass
setblock -38 200 23 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock -37 200 32 minecraft:seagrass
setblock -37 200 33 minecraft:seagrass
setblock -37 200 34 minecraft:seagrass
setblock -36 200 27 minecraft:seagrass
setblock -36 200 28 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -35 200 28 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned -29 202 36 run function rlk:room/prop/fo_pipe_x
execute positioned -27 202 38 run function rlk:room/prop/fo_lamp
execute positioned -38 201 38 run function rlk:room/prop/fo_flower
execute positioned -26 201 35 run function rlk:room/prop/fo_flower
execute positioned -23 201 30 run function rlk:room/prop/p_grass
execute positioned -25 202 36 run function rlk:room/prop/p_grass
execute positioned -29 201 34 run function rlk:room/prop/p_grass
execute positioned -30 201 33 run function rlk:room/prop/fo_white
execute positioned -37 201 38 run function rlk:room/prop/fo_flower
execute positioned -33 201 29 run function rlk:room/prop/p_grass
execute positioned -29 201 28 run function rlk:room/prop/fo_white
setblock -33 208 38 minecraft:short_grass keep
setblock -31 208 38 minecraft:short_grass keep
