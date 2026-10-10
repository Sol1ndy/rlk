# 구역 건설 (normal8_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -12 200 -14 -11 200 -13 minecraft:gravel
fill -20 209 -12 -20 210 -9 minecraft:birch_leaves[persistent=true]
fill -20 209 -4 -20 210 -1 minecraft:birch_leaves[persistent=true]
fill -20 210 -16 -20 210 -15 minecraft:birch_leaves[persistent=true]
fill -20 201 -4 -20 202 -2 minecraft:moss_block
fill -1 203 -1 -1 204 -1 minecraft:prismarine
fill -1 201 -9 -1 203 -6 minecraft:calcite
fill -1 209 -10 -1 210 -8 minecraft:oak_leaves[persistent=true]
fill -1 204 -18 -1 207 -18 minecraft:calcite
fill -1 210 -4 -1 210 -3 minecraft:birch_leaves[persistent=true]
fill -1 201 -10 -1 202 -7 minecraft:prismarine
fill -13 203 -20 -13 206 -20 minecraft:moss_block
fill -16 210 -20 -11 210 -20 minecraft:oak_leaves[persistent=true]
fill -9 207 -20 -4 208 -20 minecraft:moss_block
fill -16 210 -20 -15 210 -20 minecraft:oak_leaves[persistent=true]
fill -12 202 -1 -7 202 -1 minecraft:prismarine
fill -17 210 -1 -12 210 -1 minecraft:oak_leaves[persistent=true]
fill -17 208 -1 -14 209 -1 minecraft:diorite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -19 201 -19 -18 201 -18 minecraft:podzol
fill -13 201 -19 -13 201 -16 minecraft:podzol
fill -17 201 -18 -17 201 -17 minecraft:podzol
fill -16 201 -17 -16 201 -13 minecraft:podzol
fill -12 201 -17 -2 201 -15 minecraft:podzol
fill -5 201 -14 -5 201 -6 minecraft:podzol
fill -17 201 -13 -17 201 -12 minecraft:podzol
fill -19 201 -12 -18 201 -11 minecraft:podzol
fill -4 201 -6 -2 201 -6 minecraft:podzol
fill -12 201 -19 -2 201 -18 minecraft:dirt
fill -12 202 -19 -2 202 -18 minecraft:podzol
fill -19 201 -17 -18 201 -13 minecraft:dirt
fill -19 202 -17 -18 202 -13 minecraft:podzol
fill -17 201 -16 -17 201 -14 minecraft:dirt
fill -17 202 -16 -17 202 -14 minecraft:podzol
fill -4 201 -14 -2 201 -7 minecraft:dirt
fill -4 202 -14 -2 202 -7 minecraft:podzol
fill -15 201 -3 -13 207 -2 minecraft:calcite
fill -15 208 -3 -13 208 -2 minecraft:podzol
fill -17 201 -7 -16 207 -6 minecraft:diorite
fill -17 208 -7 -16 208 -6 minecraft:podzol
execute positioned -17 201 -19 run function rlk:room/prop/fo_crates
execute positioned -6 201 -5 run function rlk:room/prop/fo_flower
execute positioned -6 201 -2 run function rlk:room/prop/fo_white
execute positioned -7 202 -17 run function rlk:room/prop/p_grass
execute positioned -12 201 -3 run function rlk:room/prop/fo_flower
execute positioned -19 203 -13 run function rlk:room/prop/fo_flower
execute positioned -12 201 -7 run function rlk:room/prop/fo_white
execute positioned -9 203 -18 run function rlk:room/prop/fo_flower
execute positioned -7 202 -16 run function rlk:room/prop/p_grass
setblock -17 209 -7 minecraft:short_grass keep
setblock -17 209 -6 minecraft:short_grass keep
setblock -16 209 -6 minecraft:birch_leaves[persistent=true] keep
setblock -14 209 -2 minecraft:birch_leaves[persistent=true] keep
setblock -13 209 -3 minecraft:birch_leaves[persistent=true] keep
setblock -13 209 -2 minecraft:short_grass keep
