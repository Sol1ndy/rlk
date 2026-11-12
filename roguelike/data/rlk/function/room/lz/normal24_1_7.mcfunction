# 구역 건설 (normal24_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -16 200 -16 -13 200 -15 minecraft:moss_block
fill -14 200 -19 -11 200 -16 minecraft:calcite
fill -20 209 -11 -20 210 -7 minecraft:prismarine
fill -20 202 -5 -20 204 -3 minecraft:diorite
fill -20 210 -10 -20 210 -7 minecraft:oak_leaves[persistent=true]
fill -20 210 -4 -20 210 -3 minecraft:calcite
fill -20 201 -8 -20 204 -4 minecraft:moss_block
fill -20 210 -20 -20 210 -17 minecraft:birch_leaves[persistent=true]
fill -1 209 -16 -1 210 -14 minecraft:oak_leaves[persistent=true]
fill -1 210 -19 -1 210 -14 minecraft:oak_leaves[persistent=true]
fill -1 204 -8 -1 206 -6 minecraft:dark_prismarine
fill -1 209 -7 -1 210 -6 minecraft:oak_leaves[persistent=true]
fill -3 202 -20 -2 203 -20 minecraft:prismarine
fill -5 204 -20 -5 204 -20 minecraft:calcite
fill -6 210 -20 -3 210 -20 minecraft:prismarine
fill -12 209 -20 -7 210 -20 minecraft:oak_leaves[persistent=true]
fill -13 210 -20 -12 210 -20 minecraft:birch_leaves[persistent=true]
fill -20 210 -1 -18 210 -1 minecraft:oak_leaves[persistent=true]
fill -7 209 -1 -6 210 -1 minecraft:oak_leaves[persistent=true]
fill -10 209 -1 -7 210 -1 minecraft:prismarine
fill -20 204 -1 -18 205 -1 minecraft:diorite
fill -5 210 -1 -5 210 -1 minecraft:birch_leaves[persistent=true]
fill -15 209 -1 -15 210 -1 minecraft:oak_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -7 201 -18 -3 201 -18 minecraft:podzol
fill -9 201 -17 -7 201 -15 minecraft:podzol
fill -4 201 -17 -2 201 -8 minecraft:podzol
fill -10 201 -16 -10 201 -15 minecraft:podzol
fill -6 201 -15 -5 201 -15 minecraft:podzol
fill -5 201 -14 -5 201 -8 minecraft:podzol
fill -17 201 -19 -16 206 -19 minecraft:calcite
fill -17 207 -19 -16 207 -19 minecraft:podzol
fill -15 201 -19 -15 206 -19 minecraft:diorite
fill -15 207 -19 -15 207 -19 minecraft:podzol
fill -6 201 -17 -5 207 -16 minecraft:calcite
fill -6 208 -17 -5 208 -16 minecraft:podzol
execute positioned -2 201 -6 run function rlk:room/prop/fo_lamp
execute positioned -8 201 -8 run function rlk:room/prop/fo_flower
execute positioned -18 201 -8 run function rlk:room/prop/fo_white
execute positioned -6 201 -6 run function rlk:room/prop/fo_flower
execute positioned -15 201 -18 run function rlk:room/prop/p_grass
execute positioned -7 201 -12 run function rlk:room/prop/fo_white
execute positioned -15 201 -16 run function rlk:room/prop/fo_flower
execute positioned -12 201 -4 run function rlk:room/prop/fo_white
execute positioned -14 201 -14 run function rlk:room/prop/p_grass
setblock -17 208 -19 minecraft:birch_leaves[persistent=true] keep
setblock -16 208 -19 minecraft:birch_leaves[persistent=true] keep
setblock -5 209 -17 minecraft:birch_leaves[persistent=true] keep
setblock -5 209 -16 minecraft:short_grass keep
