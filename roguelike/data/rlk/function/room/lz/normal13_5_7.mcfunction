# 구역 건설 (normal13_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -5 200 -8 -3 200 -6 minecraft:moss_block
fill -20 204 -13 -20 206 -10 minecraft:diorite
fill -20 201 -20 -20 204 -19 minecraft:calcite
fill -20 205 -19 -20 205 -19 minecraft:dark_prismarine
fill -20 204 -8 -20 207 -5 minecraft:moss_block
fill -20 205 -3 -20 206 -2 minecraft:prismarine
fill -1 206 -9 -1 207 -7 minecraft:moss_block
fill -1 202 -18 -1 204 -14 minecraft:calcite
fill -1 202 -14 -1 203 -14 minecraft:moss_block
fill -1 210 -1 -1 210 -1 minecraft:oak_leaves[persistent=true]
fill -1 209 -5 -1 210 -4 minecraft:birch_leaves[persistent=true]
fill -1 210 -6 -1 210 -6 minecraft:oak_leaves[persistent=true]
fill -7 204 -20 -2 206 -20 minecraft:moss_block
fill -10 204 -20 -7 204 -20 minecraft:moss_block
fill -12 205 -20 -7 206 -20 minecraft:calcite
fill -5 205 -20 -3 205 -20 minecraft:diorite
fill -11 202 -20 -6 203 -20 minecraft:moss_block
fill -8 208 -20 -5 210 -20 minecraft:diorite
fill -12 205 -1 -11 206 -1 minecraft:calcite
fill -13 210 -1 -10 210 -1 minecraft:birch_leaves[persistent=true]
fill -5 206 -1 -5 208 -1 minecraft:moss_block
fill -11 202 -1 -11 203 -1 minecraft:calcite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -19 201 -10 -16 201 -10 minecraft:podzol
fill -19 201 -9 -18 201 -9 minecraft:podzol
fill -15 201 -9 -15 201 -6 minecraft:podzol
fill -19 201 -8 -19 201 -8 minecraft:podzol
fill -14 201 -5 -13 201 -5 minecraft:podzol
fill -19 201 -4 -19 201 -2 minecraft:podzol
fill -15 201 -4 -14 201 -4 minecraft:podzol
fill -18 201 -3 -15 201 -3 minecraft:podzol
fill -18 201 -2 -16 201 -2 minecraft:podzol
fill -18 201 -8 -18 201 -4 minecraft:dirt
fill -18 202 -8 -18 202 -4 minecraft:podzol
fill -19 201 -7 -19 201 -5 minecraft:dirt
fill -19 202 -7 -19 202 -5 minecraft:podzol
fill -17 201 -7 -16 201 -4 minecraft:dirt
fill -17 202 -7 -16 202 -4 minecraft:podzol
fill -15 201 -5 -15 201 -5 minecraft:dirt
fill -15 202 -5 -15 202 -5 minecraft:podzol
fill -11 201 -2 -8 206 -2 minecraft:calcite
fill -11 207 -2 -8 207 -2 minecraft:podzol
fill -17 201 -9 -16 207 -9 minecraft:calcite
fill -17 208 -9 -16 208 -9 minecraft:podzol
fill -17 201 -8 -16 207 -8 minecraft:diorite
fill -17 208 -8 -16 208 -8 minecraft:podzol
fill -4 199 -17 -2 199 -8 minecraft:clay
fill -4 200 -17 -2 200 -8 minecraft:water
fill -5 199 -14 -5 199 -9 minecraft:clay
fill -5 200 -14 -5 200 -9 minecraft:water
fill -4 200 -18 -2 200 -18 minecraft:sand
fill -5 200 -8 -5 200 -7 minecraft:sand
fill -4 200 -7 -2 200 -7 minecraft:sand
setblock -4 200 -17 minecraft:seagrass
setblock -4 200 -14 minecraft:seagrass
setblock -4 200 -10 minecraft:seagrass
setblock -3 200 -11 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -2 200 -16 minecraft:seagrass
setblock -2 200 -14 minecraft:seagrass
setblock -2 200 -9 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned -17 201 -19 run function rlk:room/prop/fo_lamp
execute positioned -17 202 -2 run function rlk:room/prop/fo_lamp2
execute positioned -6 201 -14 run function rlk:room/prop/p_grass
execute positioned -7 201 -9 run function rlk:room/prop/p_grass
execute positioned -7 201 -8 run function rlk:room/prop/fo_flower
execute positioned -6 201 -4 run function rlk:room/prop/p_grass
execute positioned -12 201 -17 run function rlk:room/prop/fo_flower
execute positioned -3 201 -7 run function rlk:room/prop/fo_white
execute positioned -3 201 -4 run function rlk:room/prop/fo_white
execute positioned -18 202 -2 run function rlk:room/prop/fo_white
execute positioned -16 201 -11 run function rlk:room/prop/p_grass
execute positioned -11 201 -19 run function rlk:room/prop/fo_flower
setblock -17 209 -9 minecraft:short_grass keep
setblock -17 209 -8 minecraft:short_grass keep
setblock -16 209 -9 minecraft:short_grass keep
setblock -10 208 -2 minecraft:short_grass keep
setblock -9 208 -2 minecraft:birch_leaves[persistent=true] keep
setblock -8 208 -2 minecraft:short_grass keep
