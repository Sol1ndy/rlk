# 구역 건설 (normal21_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -6 200 -17 -3 200 -15 minecraft:coarse_dirt
fill -13 200 -8 -9 200 -6 minecraft:calcite
fill -7 200 -18 -3 200 -17 minecraft:calcite
fill -20 210 -10 -20 210 -5 minecraft:oak_leaves[persistent=true]
fill -20 206 -18 -20 207 -15 minecraft:calcite
fill -20 206 -20 -20 207 -19 minecraft:diorite
fill -20 201 -16 -20 204 -15 minecraft:moss_block
fill -1 209 -20 -1 210 -15 minecraft:oak_leaves[persistent=true]
fill -1 205 -17 -1 206 -17 minecraft:diorite
fill -1 205 -17 -1 205 -14 minecraft:prismarine
fill -16 206 -20 -14 209 -20 minecraft:diorite
fill -11 202 -20 -10 204 -20 minecraft:moss_block
fill -13 208 -20 -9 209 -20 minecraft:prismarine
fill -8 207 -1 -3 210 -1 minecraft:moss_block
fill -2 206 -1 -1 207 -1 minecraft:dark_prismarine
fill -7 203 -1 -2 203 -1 minecraft:dark_prismarine
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -19 201 -15 -17 201 -15 minecraft:podzol
fill -17 201 -14 -17 201 -6 minecraft:podzol
fill -4 201 -7 -2 201 -7 minecraft:podzol
fill -19 201 -6 -18 201 -5 minecraft:podzol
fill -5 201 -6 -5 201 -6 minecraft:podzol
fill -6 201 -5 -6 201 -5 minecraft:podzol
fill -7 201 -4 -7 201 -2 minecraft:podzol
fill -19 201 -14 -18 201 -7 minecraft:dirt
fill -19 202 -14 -18 202 -7 minecraft:podzol
fill -4 201 -6 -2 201 -6 minecraft:dirt
fill -4 202 -6 -2 202 -6 minecraft:podzol
fill -5 201 -5 -5 201 -5 minecraft:dirt
fill -5 202 -5 -5 202 -5 minecraft:podzol
fill -6 201 -4 -6 201 -2 minecraft:dirt
fill -6 202 -4 -6 202 -2 minecraft:podzol
fill -4 201 -5 -2 202 -2 minecraft:dirt
fill -4 203 -5 -2 203 -2 minecraft:podzol
fill -5 201 -4 -5 202 -2 minecraft:dirt
fill -5 203 -4 -5 203 -2 minecraft:podzol
fill -10 201 -17 -9 205 -16 minecraft:calcite
fill -10 206 -17 -9 206 -16 minecraft:podzol
fill -11 201 -19 -10 206 -18 minecraft:calcite
fill -11 207 -19 -10 207 -18 minecraft:podzol
fill -9 201 -18 -8 206 -18 minecraft:calcite
fill -9 207 -18 -8 207 -18 minecraft:podzol
fill -9 201 -19 -8 206 -19 minecraft:diorite
fill -9 207 -19 -8 207 -19 minecraft:podzol
fill -15 199 -16 -14 199 -15 minecraft:clay
fill -15 200 -16 -14 200 -15 minecraft:water
fill -13 199 -15 -13 199 -15 minecraft:clay
fill -13 200 -15 -13 200 -15 minecraft:water
fill -15 199 -14 -15 199 -13 minecraft:clay
fill -15 200 -14 -15 200 -13 minecraft:water
fill -15 200 -17 -15 200 -17 minecraft:sand
fill -12 200 -16 -12 200 -16 minecraft:sand
fill -15 200 -12 -15 200 -12 minecraft:sand
setblock -15 200 -13 minecraft:seagrass
execute positioned -16 201 -4 run function rlk:room/prop/fo_lamp2
execute positioned -3 201 -10 run function rlk:room/prop/fo_rock_s
execute positioned -19 201 -16 run function rlk:room/prop/fo_flower
execute positioned -6 201 -11 run function rlk:room/prop/fo_flower
execute positioned -17 202 -14 run function rlk:room/prop/p_grass
execute positioned -2 203 -6 run function rlk:room/prop/p_grass
execute positioned -8 201 -8 run function rlk:room/prop/fo_flower
execute positioned -13 201 -13 run function rlk:room/prop/fo_flower
execute positioned -16 201 -4 run function rlk:room/prop/fo_flower
execute positioned -4 204 -2 run function rlk:room/prop/p_grass
setblock -11 208 -19 minecraft:birch_leaves[persistent=true] keep
setblock -11 208 -18 minecraft:short_grass keep
setblock -10 208 -19 minecraft:birch_leaves[persistent=true] keep
setblock -10 208 -18 minecraft:short_grass keep
setblock -10 207 -16 minecraft:short_grass keep
setblock -9 208 -18 minecraft:birch_leaves[persistent=true] keep
setblock -8 208 -18 minecraft:short_grass keep
