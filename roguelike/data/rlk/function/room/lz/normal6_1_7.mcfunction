# 구역 건설 (normal6_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -7 200 -4 -6 200 -3 minecraft:moss_block
fill -20 204 -7 -20 204 -3 minecraft:prismarine
fill -20 209 -3 -20 210 -2 minecraft:oak_leaves[persistent=true]
fill -20 210 -18 -20 210 -13 minecraft:oak_leaves[persistent=true]
fill -20 204 -6 -20 207 -4 minecraft:dark_prismarine
fill -20 205 -16 -20 208 -16 minecraft:moss_block
fill -1 209 -19 -1 210 -19 minecraft:birch_leaves[persistent=true]
fill -1 209 -6 -1 210 -1 minecraft:calcite
fill -1 209 -20 -1 210 -20 minecraft:birch_leaves[persistent=true]
fill -6 203 -20 -3 205 -20 minecraft:calcite
fill -19 205 -20 -18 206 -20 minecraft:dark_prismarine
fill -14 201 -20 -9 201 -20 minecraft:calcite
fill -11 204 -1 -10 204 -1 minecraft:diorite
fill -7 209 -1 -3 210 -1 minecraft:oak_leaves[persistent=true]
fill -5 204 -1 -3 205 -1 minecraft:moss_block
fill -5 205 -1 -2 208 -1 minecraft:diorite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -18 201 -19 -18 201 -16 minecraft:podzol
fill -10 201 -19 -10 201 -16 minecraft:podzol
fill -17 201 -15 -17 201 -15 minecraft:podzol
fill -14 201 -15 -11 201 -15 minecraft:podzol
fill -16 201 -14 -15 201 -14 minecraft:podzol
fill -17 201 -19 -17 201 -16 minecraft:dirt
fill -17 202 -19 -17 202 -16 minecraft:podzol
fill -11 201 -19 -11 201 -16 minecraft:dirt
fill -11 202 -19 -11 202 -16 minecraft:podzol
fill -16 201 -16 -16 201 -15 minecraft:dirt
fill -16 202 -16 -16 202 -15 minecraft:podzol
fill -12 201 -16 -12 201 -16 minecraft:dirt
fill -12 202 -16 -12 202 -16 minecraft:podzol
fill -15 201 -15 -15 201 -15 minecraft:dirt
fill -15 202 -15 -15 202 -15 minecraft:podzol
fill -16 201 -19 -12 202 -18 minecraft:dirt
fill -16 203 -19 -12 203 -18 minecraft:podzol
fill -16 201 -17 -15 202 -17 minecraft:dirt
fill -16 203 -17 -15 203 -17 minecraft:podzol
fill -12 201 -17 -12 202 -17 minecraft:dirt
fill -12 203 -17 -12 203 -17 minecraft:podzol
fill -15 201 -16 -15 202 -16 minecraft:dirt
fill -15 203 -16 -15 203 -16 minecraft:podzol
fill -19 201 -12 -18 206 -12 minecraft:calcite
fill -19 207 -12 -18 207 -12 minecraft:podzol
fill -19 201 -14 -18 206 -13 minecraft:diorite
fill -19 207 -14 -18 207 -13 minecraft:podzol
fill -14 201 -17 -13 207 -17 minecraft:calcite
fill -14 208 -17 -13 208 -17 minecraft:podzol
fill -14 201 -16 -13 207 -16 minecraft:diorite
fill -14 208 -16 -13 208 -16 minecraft:podzol
fill -9 199 -19 -4 199 -15 minecraft:clay
fill -9 200 -19 -4 200 -15 minecraft:water
fill -5 199 -14 -4 199 -13 minecraft:clay
fill -5 200 -14 -4 200 -13 minecraft:water
fill -3 200 -19 -3 200 -12 minecraft:sand
fill -10 200 -15 -10 200 -15 minecraft:sand
fill -4 200 -12 -4 200 -12 minecraft:sand
setblock -8 200 -19 minecraft:seagrass
setblock -8 200 -18 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock -6 200 -18 minecraft:seagrass
setblock -5 200 -18 minecraft:seagrass
setblock -4 200 -18 minecraft:seagrass
execute positioned -19 201 -7 run function rlk:room/prop/fo_col_b
execute positioned -4 201 -9 run function rlk:room/prop/fo_col_b
execute positioned -17 201 -4 run function rlk:room/prop/p_grass
execute positioned -2 201 -8 run function rlk:room/prop/fo_flower
execute positioned -16 201 -7 run function rlk:room/prop/fo_flower
execute positioned -11 202 -15 run function rlk:room/prop/p_grass
execute positioned -2 201 -14 run function rlk:room/prop/fo_flower
execute positioned -2 201 -12 run function rlk:room/prop/p_grass
execute positioned -17 201 -2 run function rlk:room/prop/p_grass
execute positioned -15 201 -2 run function rlk:room/prop/p_grass
execute positioned -8 201 -2 run function rlk:room/prop/p_grass
execute positioned -16 204 -19 run function rlk:room/prop/fo_flower
setblock -19 208 -14 minecraft:birch_leaves[persistent=true] keep
setblock -18 208 -12 minecraft:birch_leaves[persistent=true] keep
setblock -14 209 -16 minecraft:short_grass keep
setblock -13 209 -17 minecraft:birch_leaves[persistent=true] keep
setblock -13 209 -16 minecraft:birch_leaves[persistent=true] keep
