# 구역 건설 (levelup3_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 211 -21 minecraft:stone
fill -19 201 -39 -2 211 -22 minecraft:air
fill -19 210 -39 -2 210 -22 minecraft:light[level=15]
fill -18 201 -30 -16 201 -29 minecraft:gravel
fill -13 201 -28 -9 201 -27 minecraft:calcite
fill -11 201 -31 -7 201 -30 minecraft:coarse_dirt
fill -8 201 -36 -4 201 -35 minecraft:moss_block
fill -20 211 -24 -20 211 -21 minecraft:birch_leaves[persistent=true]
fill -20 211 -36 -20 211 -32 minecraft:diorite
fill -20 208 -27 -20 211 -23 minecraft:calcite
fill -1 209 -31 -1 210 -30 minecraft:calcite
fill -1 211 -33 -1 211 -28 minecraft:moss_block
fill -1 211 -26 -1 211 -26 minecraft:birch_leaves[persistent=true]
fill -1 211 -31 -1 211 -26 minecraft:oak_leaves[persistent=true]
fill -1 211 -39 -1 211 -38 minecraft:oak_leaves[persistent=true]
fill -1 204 -34 -1 204 -29 minecraft:calcite
fill -7 210 -40 -7 211 -40 minecraft:oak_leaves[persistent=true]
fill -10 203 -40 -8 206 -40 minecraft:diorite
fill -18 203 -40 -18 203 -40 minecraft:calcite
fill -12 211 -40 -7 211 -40 minecraft:oak_leaves[persistent=true]
fill -10 210 -40 -10 211 -40 minecraft:oak_leaves[persistent=true]
fill -12 210 -40 -7 211 -40 minecraft:oak_leaves[persistent=true]
fill -18 210 -21 -16 211 -21 minecraft:birch_leaves[persistent=true]
fill -9 206 -21 -5 208 -21 minecraft:moss_block
fill -14 210 -21 -11 211 -21 minecraft:oak_leaves[persistent=true]
fill -20 211 -40 -1 211 -21 minecraft:polished_deepslate
fill -19 211 -39 -2 211 -22 minecraft:air
fill -19 201 -39 -2 201 -27 minecraft:podzol
fill -19 201 -26 -6 201 -26 minecraft:podzol
fill -3 201 -26 -2 201 -22 minecraft:podzol
fill -19 201 -25 -15 201 -25 minecraft:podzol
fill -19 201 -24 -17 201 -22 minecraft:podzol
fill -5 201 -26 -4 201 -26 minecraft:dirt
fill -5 202 -26 -4 202 -26 minecraft:podzol
fill -14 201 -25 -6 201 -25 minecraft:dirt
fill -14 202 -25 -6 202 -25 minecraft:podzol
fill -4 201 -25 -4 201 -22 minecraft:dirt
fill -4 202 -25 -4 202 -22 minecraft:podzol
fill -16 201 -24 -15 201 -24 minecraft:dirt
fill -16 202 -24 -15 202 -24 minecraft:podzol
fill -16 201 -23 -16 201 -22 minecraft:dirt
fill -16 202 -23 -16 202 -22 minecraft:podzol
fill -5 201 -25 -5 202 -22 minecraft:dirt
fill -5 203 -25 -5 203 -22 minecraft:podzol
fill -14 201 -24 -6 202 -24 minecraft:dirt
fill -14 203 -24 -6 203 -24 minecraft:podzol
fill -15 201 -23 -14 202 -22 minecraft:dirt
fill -15 203 -23 -14 203 -22 minecraft:podzol
fill -6 201 -23 -6 202 -22 minecraft:dirt
fill -6 203 -23 -6 203 -22 minecraft:podzol
fill -13 201 -23 -7 203 -23 minecraft:dirt
fill -13 204 -23 -7 204 -23 minecraft:podzol
fill -7 201 -22 -7 203 -22 minecraft:dirt
fill -7 204 -22 -7 204 -22 minecraft:podzol
fill -13 201 -22 -8 208 -22 minecraft:diorite
fill -13 209 -22 -8 209 -22 minecraft:podzol
fill -12 200 -37 -9 200 -36 minecraft:clay
fill -12 201 -37 -9 201 -36 minecraft:water
fill -5 200 -37 -2 200 -34 minecraft:clay
fill -5 201 -37 -2 201 -34 minecraft:water
fill -14 200 -36 -13 200 -35 minecraft:clay
fill -14 201 -36 -13 201 -35 minecraft:water
fill -8 200 -36 -6 200 -35 minecraft:clay
fill -8 201 -36 -6 201 -35 minecraft:water
fill -2 200 -33 -2 200 -28 minecraft:clay
fill -2 201 -33 -2 201 -28 minecraft:water
fill -6 201 -38 -2 201 -38 minecraft:sand
fill -7 201 -37 -6 201 -37 minecraft:sand
fill -2 201 -27 -2 201 -27 minecraft:sand
setblock -13 201 -35 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -12 201 -37 minecraft:seagrass
setblock -11 201 -37 minecraft:seagrass
setblock -11 201 -36 minecraft:seagrass
setblock -10 201 -37 minecraft:seagrass
setblock -10 201 -36 minecraft:seagrass
setblock -9 201 -37 minecraft:seagrass
setblock -9 201 -36 minecraft:seagrass
setblock -6 201 -35 minecraft:seagrass
setblock -5 201 -34 minecraft:seagrass
setblock -3 201 -37 minecraft:seagrass
setblock -3 201 -36 minecraft:seagrass
setblock -2 201 -32 minecraft:seagrass
setblock -2 201 -30 minecraft:seagrass
execute positioned -14 204 -24 run function rlk:room/prop/fo_col_a
execute positioned -4 202 -32 run function rlk:room/prop/p_grass
execute positioned -14 204 -22 run function rlk:room/prop/fo_flower
execute positioned -5 202 -27 run function rlk:room/prop/fo_flower
execute positioned -9 202 -39 run function rlk:room/prop/p_grass
execute positioned -15 202 -35 run function rlk:room/prop/fo_flower
execute positioned -2 202 -39 run function rlk:room/prop/p_grass
execute positioned -5 202 -39 run function rlk:room/prop/p_grass
setblock -13 210 -22 minecraft:short_grass keep
setblock -12 210 -22 minecraft:short_grass keep
setblock -10 210 -22 minecraft:birch_leaves[persistent=true] keep
setblock -8 210 -22 minecraft:birch_leaves[persistent=true] keep
