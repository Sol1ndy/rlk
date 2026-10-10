# 구역 건설 (normal14_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -16 200 -16 -15 200 -15 minecraft:gravel
fill -16 200 -15 -14 200 -13 minecraft:coarse_dirt
fill -20 203 -14 -20 206 -13 minecraft:moss_block
fill -20 203 -16 -20 206 -11 minecraft:diorite
fill -20 209 -17 -20 210 -17 minecraft:birch_leaves[persistent=true]
fill -1 208 -12 -1 210 -12 minecraft:moss_block
fill -1 201 -14 -1 203 -9 minecraft:calcite
fill -1 209 -17 -1 210 -12 minecraft:birch_leaves[persistent=true]
fill -1 202 -12 -1 205 -10 minecraft:prismarine
fill -10 203 -20 -7 204 -20 minecraft:diorite
fill -14 210 -20 -11 210 -20 minecraft:birch_leaves[persistent=true]
fill -6 209 -20 -3 210 -20 minecraft:birch_leaves[persistent=true]
fill -2 202 -20 -1 202 -20 minecraft:moss_block
fill -1 205 -20 -1 208 -20 minecraft:calcite
fill -7 209 -20 -6 210 -20 minecraft:oak_leaves[persistent=true]
fill -18 210 -1 -18 210 -1 minecraft:birch_leaves[persistent=true]
fill -8 210 -1 -6 210 -1 minecraft:oak_leaves[persistent=true]
fill -16 206 -1 -15 208 -1 minecraft:prismarine
fill -1 203 -1 -1 203 -1 minecraft:calcite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -10 201 -5 -7 201 -5 minecraft:podzol
fill -11 201 -4 -9 201 -4 minecraft:podzol
fill -6 201 -4 -2 201 -4 minecraft:podzol
fill -10 201 -3 -10 201 -2 minecraft:podzol
fill -2 201 -3 -2 201 -2 minecraft:podzol
fill -9 201 -2 -9 201 -2 minecraft:podzol
fill -3 201 -2 -3 201 -2 minecraft:podzol
fill -8 201 -4 -7 201 -2 minecraft:dirt
fill -8 202 -4 -7 202 -2 minecraft:podzol
fill -9 201 -3 -9 201 -3 minecraft:dirt
fill -9 202 -3 -9 202 -3 minecraft:podzol
fill -6 201 -3 -3 201 -3 minecraft:dirt
fill -6 202 -3 -3 202 -3 minecraft:podzol
fill -6 201 -2 -4 201 -2 minecraft:dirt
fill -6 202 -2 -4 202 -2 minecraft:podzol
fill -17 201 -3 -14 206 -2 minecraft:calcite
fill -17 207 -3 -14 207 -2 minecraft:podzol
fill -20 186 -20 -16 199 -8 minecraft:stone
fill -19 186 -19 -17 186 -9 minecraft:clay
fill -19 187 -19 -17 188 -9 minecraft:water
fill -19 189 -19 -17 201 -9 minecraft:air
fill -14 199 -19 -4 199 -17 minecraft:clay
fill -14 200 -19 -4 200 -17 minecraft:water
fill -14 199 -16 -7 199 -15 minecraft:clay
fill -14 200 -16 -7 200 -15 minecraft:water
fill -3 200 -19 -3 200 -17 minecraft:sand
setblock -9 200 -18 minecraft:seagrass
setblock -8 200 -19 minecraft:seagrass
setblock -8 200 -17 minecraft:seagrass
setblock -5 200 -17 minecraft:seagrass
execute positioned -3 201 -6 run function rlk:room/prop/fo_flower
execute positioned -6 201 -5 run function rlk:room/prop/p_grass
execute positioned -4 201 -14 run function rlk:room/prop/fo_flower
execute positioned -14 201 -7 run function rlk:room/prop/fo_flower
execute positioned -4 201 -6 run function rlk:room/prop/p_grass
execute positioned -18 201 -2 run function rlk:room/prop/fo_flower
execute positioned -9 201 -6 run function rlk:room/prop/p_grass
execute positioned -3 202 -2 run function rlk:room/prop/p_grass
execute positioned -4 203 -2 run function rlk:room/prop/fo_flower
setblock -16 208 -3 minecraft:short_grass keep
setblock -15 208 -2 minecraft:birch_leaves[persistent=true] keep
