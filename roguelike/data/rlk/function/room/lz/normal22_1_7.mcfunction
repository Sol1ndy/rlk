# 구역 건설 (normal22_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -19 200 -19 -15 200 -17 minecraft:calcite
fill -11 200 -13 -7 200 -10 minecraft:calcite
fill -19 200 -4 -17 200 -2 minecraft:coarse_dirt
fill -20 204 -13 -20 207 -9 minecraft:calcite
fill -20 209 -11 -20 209 -9 minecraft:prismarine
fill -20 203 -17 -20 204 -13 minecraft:prismarine
fill -20 210 -17 -20 210 -17 minecraft:oak_leaves[persistent=true]
fill -20 206 -11 -20 209 -7 minecraft:calcite
fill -20 210 -5 -20 210 -1 minecraft:birch_leaves[persistent=true]
fill -1 204 -10 -1 205 -6 minecraft:calcite
fill -1 209 -18 -1 210 -18 minecraft:birch_leaves[persistent=true]
fill -1 201 -20 -1 202 -15 minecraft:moss_block
fill -1 203 -13 -1 205 -9 minecraft:prismarine
fill -1 208 -20 -1 210 -19 minecraft:diorite
fill -20 209 -20 -16 210 -20 minecraft:moss_block
fill -15 210 -20 -13 210 -20 minecraft:oak_leaves[persistent=true]
fill -20 208 -20 -16 209 -20 minecraft:diorite
fill -12 205 -20 -8 207 -20 minecraft:moss_block
fill -9 206 -1 -4 208 -1 minecraft:diorite
fill -11 206 -1 -9 208 -1 minecraft:calcite
fill -8 209 -1 -3 210 -1 minecraft:oak_leaves[persistent=true]
fill -18 209 -1 -16 210 -1 minecraft:birch_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -5 201 -12 -3 201 -11 minecraft:podzol
fill -2 201 -11 -2 201 -10 minecraft:podzol
fill -5 201 -10 -5 201 -7 minecraft:podzol
fill -4 201 -6 -4 201 -2 minecraft:podzol
fill -3 201 -3 -2 201 -3 minecraft:podzol
fill -3 201 -2 -3 201 -2 minecraft:podzol
fill -4 201 -10 -3 201 -7 minecraft:dirt
fill -4 202 -10 -3 202 -7 minecraft:podzol
fill -2 201 -9 -2 201 -7 minecraft:dirt
fill -2 202 -9 -2 202 -7 minecraft:podzol
fill -3 201 -6 -3 201 -4 minecraft:dirt
fill -3 202 -6 -3 202 -4 minecraft:podzol
fill -2 201 -4 -2 207 -4 minecraft:calcite
fill -2 208 -4 -2 208 -4 minecraft:podzol
fill -2 201 -6 -2 207 -5 minecraft:diorite
fill -2 208 -6 -2 208 -5 minecraft:podzol
fill -4 199 -16 -2 199 -13 minecraft:clay
fill -4 200 -16 -2 200 -13 minecraft:water
fill -5 199 -14 -5 199 -13 minecraft:clay
fill -5 200 -14 -5 200 -13 minecraft:water
fill -4 200 -17 -2 200 -17 minecraft:sand
fill -2 200 -12 -2 200 -12 minecraft:sand
setblock -3 200 -13 minecraft:seagrass
setblock -2 200 -15 minecraft:seagrass
execute positioned -19 201 -3 run function rlk:room/prop/fo_rock
execute positioned -12 201 -11 run function rlk:room/prop/p_grass
execute positioned -10 201 -15 run function rlk:room/prop/p_grass
execute positioned -10 201 -17 run function rlk:room/prop/p_grass
execute positioned -14 201 -14 run function rlk:room/prop/p_grass
execute positioned -10 201 -16 run function rlk:room/prop/p_grass
execute positioned -10 201 -17 run function rlk:room/prop/p_grass
execute positioned -8 201 -7 run function rlk:room/prop/fo_white
execute positioned -6 201 -3 run function rlk:room/prop/fo_flower
execute positioned -16 201 -4 run function rlk:room/prop/fo_flower
setblock -2 209 -6 minecraft:birch_leaves[persistent=true] keep
setblock -2 209 -5 minecraft:short_grass keep
setblock -2 209 -4 minecraft:birch_leaves[persistent=true] keep
