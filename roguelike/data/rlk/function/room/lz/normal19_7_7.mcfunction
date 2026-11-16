# 구역 건설 (normal19_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -5 200 -59 -4 200 -56 minecraft:moss_block
fill -16 200 -53 -13 200 -51 minecraft:coarse_dirt
fill -20 210 -46 -20 210 -41 minecraft:calcite
fill -20 202 -55 -20 204 -51 minecraft:calcite
fill -20 210 -48 -20 210 -43 minecraft:oak_leaves[persistent=true]
fill -20 205 -49 -20 208 -49 minecraft:diorite
fill -1 209 -58 -1 210 -55 minecraft:birch_leaves[persistent=true]
fill -1 210 -49 -1 210 -45 minecraft:birch_leaves[persistent=true]
fill -1 210 -59 -1 210 -59 minecraft:birch_leaves[persistent=true]
fill -1 209 -46 -1 210 -42 minecraft:oak_leaves[persistent=true]
fill -1 203 -58 -1 203 -57 minecraft:calcite
fill -10 209 -60 -6 210 -60 minecraft:oak_leaves[persistent=true]
fill -6 207 -60 -4 210 -60 minecraft:diorite
fill -1 210 -60 -1 210 -60 minecraft:oak_leaves[persistent=true]
fill -6 209 -41 -4 210 -41 minecraft:prismarine
fill -5 208 -41 -5 208 -41 minecraft:diorite
fill -15 209 -41 -15 210 -41 minecraft:birch_leaves[persistent=true]
fill -4 202 -41 -2 204 -41 minecraft:calcite
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -14 201 -45 -6 201 -45 minecraft:podzol
fill -16 201 -44 -15 201 -42 minecraft:podzol
fill -6 201 -44 -6 201 -42 minecraft:podzol
fill -17 201 -43 -17 201 -43 minecraft:podzol
fill -5 201 -43 -5 201 -43 minecraft:podzol
fill -14 201 -44 -7 201 -44 minecraft:dirt
fill -14 202 -44 -7 202 -44 minecraft:podzol
fill -14 201 -43 -10 201 -42 minecraft:dirt
fill -14 202 -43 -10 202 -42 minecraft:podzol
fill -9 201 -42 -7 207 -42 minecraft:calcite
fill -9 208 -42 -7 208 -42 minecraft:podzol
fill -9 201 -43 -7 207 -43 minecraft:diorite
fill -9 208 -43 -7 208 -43 minecraft:podzol
fill -6 199 -56 -2 199 -55 minecraft:clay
fill -6 200 -56 -2 200 -55 minecraft:water
fill -5 199 -54 -2 199 -54 minecraft:clay
fill -5 200 -54 -2 200 -54 minecraft:water
fill -2 199 -53 -2 199 -48 minecraft:clay
fill -2 200 -53 -2 200 -48 minecraft:water
fill -7 200 -57 -2 200 -57 minecraft:sand
fill -7 200 -56 -7 200 -55 minecraft:sand
fill -2 200 -47 -2 200 -47 minecraft:sand
setblock -5 200 -54 minecraft:seagrass
setblock -4 200 -56 minecraft:seagrass
setblock -4 200 -54 minecraft:seagrass
setblock -2 200 -52 minecraft:seagrass
execute positioned -14 201 -55 run function rlk:room/prop/fo_tree_c
execute positioned -3 201 -42 run function rlk:room/prop/fo_flower
execute positioned -8 201 -46 run function rlk:room/prop/p_grass
execute positioned -11 201 -52 run function rlk:room/prop/p_grass
execute positioned -19 201 -52 run function rlk:room/prop/p_grass
execute positioned -6 201 -59 run function rlk:room/prop/p_grass
execute positioned -11 203 -43 run function rlk:room/prop/p_grass
execute positioned -13 201 -52 run function rlk:room/prop/fo_flower
execute positioned -7 201 -48 run function rlk:room/prop/fo_flower
execute positioned -14 202 -45 run function rlk:room/prop/p_grass
execute positioned -13 201 -53 run function rlk:room/prop/p_grass
setblock -9 209 -43 minecraft:short_grass keep
setblock -9 209 -42 minecraft:birch_leaves[persistent=true] keep
setblock -8 209 -43 minecraft:birch_leaves[persistent=true] keep
setblock -7 209 -43 minecraft:birch_leaves[persistent=true] keep
setblock -7 209 -42 minecraft:birch_leaves[persistent=true] keep
