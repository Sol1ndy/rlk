# 구역 건설 (normal19_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 0 -41 200 19 minecraft:podzol
fill -60 201 0 -41 210 19 minecraft:stone
fill -59 201 1 -42 210 18 minecraft:air
fill -59 209 1 -42 209 18 minecraft:light[level=15]
fill -53 200 5 -50 200 8 minecraft:calcite
fill -53 200 16 -49 200 17 minecraft:calcite
fill -60 206 14 -60 209 14 minecraft:calcite
fill -60 205 9 -60 207 11 minecraft:prismarine
fill -60 207 4 -60 210 9 minecraft:moss_block
fill -41 207 5 -41 209 8 minecraft:diorite
fill -41 209 4 -41 210 8 minecraft:birch_leaves[persistent=true]
fill -41 210 11 -41 210 15 minecraft:birch_leaves[persistent=true]
fill -41 209 2 -41 210 5 minecraft:moss_block
fill -41 201 5 -41 201 8 minecraft:diorite
fill -58 210 0 -58 210 0 minecraft:calcite
fill -55 209 0 -51 210 0 minecraft:oak_leaves[persistent=true]
fill -47 203 0 -44 204 0 minecraft:diorite
fill -48 208 0 -46 209 0 minecraft:calcite
fill -50 209 19 -48 210 19 minecraft:oak_leaves[persistent=true]
fill -55 209 19 -55 209 19 minecraft:calcite
fill -48 210 19 -45 210 19 minecraft:oak_leaves[persistent=true]
fill -59 209 19 -54 210 19 minecraft:moss_block
fill -48 205 19 -43 207 19 minecraft:moss_block
fill -60 210 0 -41 210 19 minecraft:polished_deepslate
fill -59 210 1 -42 210 18 minecraft:air
fill -59 201 9 -57 201 9 minecraft:podzol
fill -57 201 10 -56 201 10 minecraft:podzol
fill -56 201 11 -56 201 14 minecraft:podzol
fill -57 201 14 -57 201 15 minecraft:podzol
fill -59 201 15 -58 201 15 minecraft:podzol
fill -59 201 10 -58 201 14 minecraft:dirt
fill -59 202 10 -58 202 14 minecraft:podzol
fill -57 201 11 -57 201 13 minecraft:dirt
fill -57 202 11 -57 202 13 minecraft:podzol
fill -51 201 3 -50 206 4 minecraft:calcite
fill -51 207 3 -50 207 4 minecraft:podzol
fill -51 201 18 -51 206 18 minecraft:calcite
fill -51 207 18 -51 207 18 minecraft:podzol
fill -54 201 18 -52 206 18 minecraft:diorite
fill -54 207 18 -52 207 18 minecraft:podzol
fill -56 201 3 -55 207 4 minecraft:calcite
fill -56 208 3 -55 208 4 minecraft:podzol
fill -57 201 4 -57 207 5 minecraft:calcite
fill -57 208 4 -57 208 5 minecraft:podzol
fill -56 201 5 -56 207 5 minecraft:calcite
fill -56 208 5 -56 208 5 minecraft:podzol
execute positioned -47 201 4 run function rlk:room/prop/fo_col_b
execute positioned -50 201 15 run function rlk:room/prop/fo_lamp2
execute positioned -52 201 1 run function rlk:room/prop/fo_lamp
execute positioned -59 201 16 run function rlk:room/prop/fo_ruin_x
execute positioned -48 201 13 run function rlk:room/prop/fo_flower
execute positioned -46 201 9 run function rlk:room/prop/fo_white
execute positioned -42 201 7 run function rlk:room/prop/p_grass
execute positioned -59 201 8 run function rlk:room/prop/fo_flower
execute positioned -59 203 12 run function rlk:room/prop/p_grass
execute positioned -57 202 10 run function rlk:room/prop/fo_flower
execute positioned -45 201 17 run function rlk:room/prop/fo_flower
execute positioned -49 201 11 run function rlk:room/prop/p_grass
setblock -57 209 4 minecraft:short_grass keep
setblock -57 209 5 minecraft:birch_leaves[persistent=true] keep
setblock -56 209 4 minecraft:short_grass keep
setblock -56 209 5 minecraft:birch_leaves[persistent=true] keep
setblock -55 209 3 minecraft:birch_leaves[persistent=true] keep
setblock -55 209 4 minecraft:birch_leaves[persistent=true] keep
setblock -54 208 18 minecraft:birch_leaves[persistent=true] keep
setblock -51 208 4 minecraft:short_grass keep
setblock -51 208 18 minecraft:short_grass keep
setblock -50 208 3 minecraft:birch_leaves[persistent=true] keep
