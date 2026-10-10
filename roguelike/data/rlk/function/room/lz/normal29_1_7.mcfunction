# 구역 건설 (normal29_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -9 200 -10 -5 200 -7 minecraft:gravel
fill -17 200 -14 -15 200 -12 minecraft:calcite
fill -4 200 -15 -2 200 -13 minecraft:calcite
fill -20 207 -17 -20 210 -13 minecraft:calcite
fill -20 207 -8 -20 207 -3 minecraft:diorite
fill -20 210 -20 -20 210 -16 minecraft:oak_leaves[persistent=true]
fill -20 206 -10 -20 208 -6 minecraft:calcite
fill -1 208 -3 -1 208 -1 minecraft:moss_block
fill -1 209 -11 -1 210 -11 minecraft:prismarine
fill -1 203 -13 -1 203 -12 minecraft:diorite
fill -1 209 -13 -1 210 -10 minecraft:birch_leaves[persistent=true]
fill -13 205 -20 -13 205 -20 minecraft:moss_block
fill -14 210 -20 -11 210 -20 minecraft:birch_leaves[persistent=true]
fill -9 207 -20 -9 209 -20 minecraft:prismarine
fill -16 207 -20 -14 210 -20 minecraft:prismarine
fill -12 210 -1 -8 210 -1 minecraft:diorite
fill -3 209 -1 -3 210 -1 minecraft:oak_leaves[persistent=true]
fill -12 210 -1 -8 210 -1 minecraft:oak_leaves[persistent=true]
fill -6 206 -1 -2 207 -1 minecraft:moss_block
fill -11 207 -1 -11 207 -1 minecraft:calcite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -14 201 -5 -9 201 -5 minecraft:podzol
fill -19 201 -4 -15 201 -4 minecraft:podzol
fill -9 201 -4 -9 201 -3 minecraft:podzol
fill -19 201 -3 -19 201 -3 minecraft:podzol
fill -8 201 -3 -8 201 -2 minecraft:podzol
fill -14 201 -4 -10 201 -4 minecraft:dirt
fill -14 202 -4 -10 202 -4 minecraft:podzol
fill -18 201 -3 -15 201 -3 minecraft:dirt
fill -18 202 -3 -15 202 -3 minecraft:podzol
fill -10 201 -3 -10 201 -2 minecraft:dirt
fill -10 202 -3 -10 202 -2 minecraft:podzol
fill -19 201 -2 -18 201 -2 minecraft:dirt
fill -19 202 -2 -18 202 -2 minecraft:podzol
fill -9 201 -2 -9 201 -2 minecraft:dirt
fill -9 202 -2 -9 202 -2 minecraft:podzol
fill -14 201 -3 -11 202 -2 minecraft:dirt
fill -14 203 -3 -11 203 -2 minecraft:podzol
fill -17 201 -2 -15 202 -2 minecraft:dirt
fill -17 203 -2 -15 203 -2 minecraft:podzol
fill -3 201 -4 -2 206 -2 minecraft:calcite
fill -3 207 -4 -2 207 -2 minecraft:podzol
fill -19 199 -19 -4 199 -17 minecraft:clay
fill -19 200 -19 -4 200 -17 minecraft:water
fill -14 199 -16 -4 199 -15 minecraft:clay
fill -14 200 -16 -4 200 -15 minecraft:water
fill -5 199 -14 -4 199 -13 minecraft:clay
fill -5 200 -14 -4 200 -13 minecraft:water
setblock -15 200 -19 minecraft:seagrass
setblock -15 200 -18 minecraft:seagrass
setblock -14 200 -17 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -14 200 -15 minecraft:seagrass
setblock -11 200 -15 minecraft:seagrass
setblock -9 200 -15 minecraft:seagrass
setblock -4 200 -17 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock -4 200 -13 minecraft:sea_pickle[pickles=2,waterlogged=true]
execute positioned -4 201 -6 run function rlk:room/prop/fo_lamp
execute positioned -15 201 -11 run function rlk:room/prop/fo_white
execute positioned -16 201 -7 run function rlk:room/prop/fo_flower
execute positioned -11 201 -13 run function rlk:room/prop/p_grass
execute positioned -19 203 -2 run function rlk:room/prop/fo_flower
execute positioned -8 201 -13 run function rlk:room/prop/fo_flower
execute positioned -15 201 -16 run function rlk:room/prop/fo_flower
execute positioned -17 202 -4 run function rlk:room/prop/p_grass
execute positioned -3 201 -15 run function rlk:room/prop/fo_flower
execute positioned -16 201 -5 run function rlk:room/prop/fo_flower
execute positioned -14 201 -12 run function rlk:room/prop/p_grass
setblock -3 208 -4 minecraft:short_grass keep
setblock -2 208 -3 minecraft:birch_leaves[persistent=true] keep
setblock -2 208 -2 minecraft:birch_leaves[persistent=true] keep
