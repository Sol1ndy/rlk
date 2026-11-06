# 구역 건설 (levelup3_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -18 200 -30 -16 200 -29 minecraft:gravel
fill -13 200 -28 -9 200 -27 minecraft:calcite
fill -11 200 -31 -7 200 -30 minecraft:coarse_dirt
fill -8 200 -36 -4 200 -35 minecraft:moss_block
fill -20 210 -24 -20 210 -21 minecraft:birch_leaves[persistent=true]
fill -20 210 -36 -20 210 -32 minecraft:diorite
fill -20 207 -27 -20 210 -23 minecraft:calcite
fill -1 208 -31 -1 209 -30 minecraft:calcite
fill -1 210 -33 -1 210 -28 minecraft:moss_block
fill -1 210 -26 -1 210 -26 minecraft:birch_leaves[persistent=true]
fill -1 210 -31 -1 210 -26 minecraft:oak_leaves[persistent=true]
fill -1 210 -39 -1 210 -38 minecraft:oak_leaves[persistent=true]
fill -1 203 -34 -1 203 -29 minecraft:calcite
fill -7 209 -40 -7 210 -40 minecraft:oak_leaves[persistent=true]
fill -10 202 -40 -8 205 -40 minecraft:diorite
fill -18 202 -40 -18 202 -40 minecraft:calcite
fill -12 210 -40 -7 210 -40 minecraft:oak_leaves[persistent=true]
fill -10 209 -40 -10 210 -40 minecraft:oak_leaves[persistent=true]
fill -12 209 -40 -7 210 -40 minecraft:oak_leaves[persistent=true]
fill -18 209 -21 -16 210 -21 minecraft:birch_leaves[persistent=true]
fill -9 205 -21 -5 207 -21 minecraft:moss_block
fill -14 209 -21 -11 210 -21 minecraft:oak_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -5 201 -26 -4 201 -26 minecraft:podzol
fill -14 201 -25 -6 201 -25 minecraft:podzol
fill -4 201 -25 -4 201 -22 minecraft:podzol
fill -16 201 -24 -15 201 -24 minecraft:podzol
fill -16 201 -23 -16 201 -22 minecraft:podzol
fill -5 201 -25 -5 201 -22 minecraft:dirt
fill -5 202 -25 -5 202 -22 minecraft:podzol
fill -14 201 -24 -6 201 -24 minecraft:dirt
fill -14 202 -24 -6 202 -24 minecraft:podzol
fill -15 201 -23 -14 201 -22 minecraft:dirt
fill -15 202 -23 -14 202 -22 minecraft:podzol
fill -6 201 -23 -6 201 -22 minecraft:dirt
fill -6 202 -23 -6 202 -22 minecraft:podzol
fill -13 201 -23 -7 202 -23 minecraft:dirt
fill -13 203 -23 -7 203 -23 minecraft:podzol
fill -7 201 -22 -7 202 -22 minecraft:dirt
fill -7 203 -22 -7 203 -22 minecraft:podzol
fill -13 201 -22 -8 207 -22 minecraft:diorite
fill -13 208 -22 -8 208 -22 minecraft:podzol
fill -12 199 -37 -9 199 -36 minecraft:clay
fill -12 200 -37 -9 200 -36 minecraft:water
fill -5 199 -37 -2 199 -34 minecraft:clay
fill -5 200 -37 -2 200 -34 minecraft:water
fill -14 199 -36 -13 199 -35 minecraft:clay
fill -14 200 -36 -13 200 -35 minecraft:water
fill -8 199 -36 -6 199 -35 minecraft:clay
fill -8 200 -36 -6 200 -35 minecraft:water
fill -2 199 -33 -2 199 -28 minecraft:clay
fill -2 200 -33 -2 200 -28 minecraft:water
fill -6 200 -38 -2 200 -38 minecraft:sand
fill -7 200 -37 -6 200 -37 minecraft:sand
fill -2 200 -27 -2 200 -27 minecraft:sand
setblock -13 200 -35 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -12 200 -37 minecraft:seagrass
setblock -11 200 -37 minecraft:seagrass
setblock -11 200 -36 minecraft:seagrass
setblock -10 200 -37 minecraft:seagrass
setblock -10 200 -36 minecraft:seagrass
setblock -9 200 -37 minecraft:seagrass
setblock -9 200 -36 minecraft:seagrass
setblock -6 200 -35 minecraft:seagrass
setblock -5 200 -34 minecraft:seagrass
setblock -3 200 -37 minecraft:seagrass
setblock -3 200 -36 minecraft:seagrass
setblock -2 200 -32 minecraft:seagrass
setblock -2 200 -30 minecraft:seagrass
execute positioned -14 203 -24 run function rlk:room/prop/fo_col_a
execute positioned -4 201 -32 run function rlk:room/prop/p_grass
execute positioned -14 203 -22 run function rlk:room/prop/fo_flower
execute positioned -5 201 -27 run function rlk:room/prop/fo_flower
execute positioned -9 201 -39 run function rlk:room/prop/p_grass
execute positioned -15 201 -35 run function rlk:room/prop/fo_flower
execute positioned -2 201 -39 run function rlk:room/prop/p_grass
execute positioned -5 201 -39 run function rlk:room/prop/p_grass
setblock -13 209 -22 minecraft:short_grass keep
setblock -12 209 -22 minecraft:short_grass keep
setblock -10 209 -22 minecraft:birch_leaves[persistent=true] keep
setblock -8 209 -22 minecraft:birch_leaves[persistent=true] keep
