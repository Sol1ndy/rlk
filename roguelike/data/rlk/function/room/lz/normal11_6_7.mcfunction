# 구역 건설 (normal11_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 212 39 minecraft:stone
fill -39 201 21 -22 212 38 minecraft:air
fill -39 211 21 -22 211 38 minecraft:light[level=15]
fill -29 202 22 -25 202 24 minecraft:gravel
fill -32 202 28 -29 202 31 minecraft:moss_block
fill -40 211 25 -40 212 26 minecraft:moss_block
fill -40 212 28 -40 212 33 minecraft:birch_leaves[persistent=true]
fill -40 211 22 -40 212 26 minecraft:oak_leaves[persistent=true]
fill -40 211 23 -40 212 26 minecraft:oak_leaves[persistent=true]
fill -21 201 22 -21 203 27 minecraft:prismarine
fill -21 211 35 -21 212 38 minecraft:moss_block
fill -21 203 20 -21 204 21 minecraft:diorite
fill -21 204 32 -21 205 37 minecraft:moss_block
fill -39 206 20 -37 209 20 minecraft:diorite
fill -34 205 20 -32 206 20 minecraft:prismarine
fill -25 206 20 -21 209 20 minecraft:diorite
fill -34 212 20 -32 212 20 minecraft:birch_leaves[persistent=true]
fill -29 211 20 -27 212 20 minecraft:birch_leaves[persistent=true]
fill -24 212 39 -22 212 39 minecraft:birch_leaves[persistent=true]
fill -31 211 39 -27 212 39 minecraft:birch_leaves[persistent=true]
fill -31 207 39 -30 208 39 minecraft:calcite
fill -33 206 39 -28 208 39 minecraft:moss_block
fill -40 212 20 -21 212 39 minecraft:polished_deepslate
fill -39 212 21 -22 212 38 minecraft:air
fill -39 201 21 -22 201 34 minecraft:dirt
fill -39 202 21 -22 202 34 minecraft:podzol
fill -39 201 35 -30 201 37 minecraft:dirt
fill -39 202 35 -30 202 37 minecraft:podzol
fill -26 201 35 -22 201 35 minecraft:dirt
fill -26 202 35 -22 202 35 minecraft:podzol
fill -39 201 38 -35 201 38 minecraft:dirt
fill -39 202 38 -35 202 38 minecraft:podzol
fill -29 201 35 -27 202 38 minecraft:dirt
fill -29 203 35 -27 203 38 minecraft:podzol
fill -26 201 36 -22 202 38 minecraft:dirt
fill -26 203 36 -22 203 38 minecraft:podzol
fill -34 201 38 -30 208 38 minecraft:calcite
fill -34 209 38 -30 209 38 minecraft:podzol
fill -39 201 21 -37 201 31 minecraft:clay
fill -39 202 21 -37 202 31 minecraft:water
fill -36 201 26 -35 201 31 minecraft:clay
fill -36 202 26 -35 202 31 minecraft:water
fill -37 201 32 -36 201 35 minecraft:clay
fill -37 202 32 -36 202 35 minecraft:water
fill -36 201 36 -35 201 36 minecraft:clay
fill -36 202 36 -35 202 36 minecraft:water
fill -39 202 32 -38 202 32 minecraft:sand
fill -35 202 32 -35 202 32 minecraft:sand
setblock -39 202 28 minecraft:seagrass
setblock -38 202 23 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock -37 202 32 minecraft:seagrass
setblock -37 202 33 minecraft:seagrass
setblock -37 202 34 minecraft:seagrass
setblock -36 202 27 minecraft:seagrass
setblock -36 202 28 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -35 202 28 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned -29 204 36 run function rlk:room/prop/fo_pipe_x
execute positioned -27 204 38 run function rlk:room/prop/fo_lamp
execute positioned -38 203 38 run function rlk:room/prop/fo_flower
execute positioned -26 203 35 run function rlk:room/prop/fo_flower
execute positioned -23 203 30 run function rlk:room/prop/p_grass
execute positioned -25 204 36 run function rlk:room/prop/p_grass
execute positioned -29 203 34 run function rlk:room/prop/p_grass
execute positioned -30 203 33 run function rlk:room/prop/fo_white
execute positioned -37 203 38 run function rlk:room/prop/fo_flower
execute positioned -33 203 29 run function rlk:room/prop/p_grass
execute positioned -29 203 28 run function rlk:room/prop/fo_white
setblock -33 210 38 minecraft:short_grass keep
setblock -31 210 38 minecraft:short_grass keep
