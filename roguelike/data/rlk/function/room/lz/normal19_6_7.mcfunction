# 구역 건설 (normal19_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 0 -41 200 19 minecraft:podzol
fill -60 201 0 -41 211 19 minecraft:stone
fill -59 201 1 -42 211 18 minecraft:air
fill -59 210 1 -42 210 18 minecraft:light[level=15]
fill -53 201 5 -50 201 8 minecraft:calcite
fill -53 201 16 -49 201 17 minecraft:calcite
fill -60 207 14 -60 210 14 minecraft:calcite
fill -60 206 9 -60 208 11 minecraft:prismarine
fill -60 208 4 -60 211 9 minecraft:moss_block
fill -41 208 5 -41 210 8 minecraft:diorite
fill -41 210 4 -41 211 8 minecraft:birch_leaves[persistent=true]
fill -41 211 11 -41 211 15 minecraft:birch_leaves[persistent=true]
fill -41 210 2 -41 211 5 minecraft:moss_block
fill -41 201 5 -41 202 8 minecraft:diorite
fill -58 211 0 -58 211 0 minecraft:calcite
fill -55 210 0 -51 211 0 minecraft:oak_leaves[persistent=true]
fill -47 204 0 -44 205 0 minecraft:diorite
fill -48 209 0 -46 210 0 minecraft:calcite
fill -50 210 19 -48 211 19 minecraft:oak_leaves[persistent=true]
fill -55 210 19 -55 210 19 minecraft:calcite
fill -48 211 19 -45 211 19 minecraft:oak_leaves[persistent=true]
fill -59 210 19 -54 211 19 minecraft:moss_block
fill -48 206 19 -43 208 19 minecraft:moss_block
fill -60 211 0 -41 211 19 minecraft:polished_deepslate
fill -59 211 1 -42 211 18 minecraft:air
fill -59 201 1 -42 201 2 minecraft:podzol
fill -59 201 3 -57 201 3 minecraft:podzol
fill -54 201 3 -52 201 17 minecraft:podzol
fill -49 201 3 -42 201 18 minecraft:podzol
fill -59 201 4 -58 201 8 minecraft:podzol
fill -55 201 5 -55 201 18 minecraft:podzol
fill -51 201 5 -50 201 17 minecraft:podzol
fill -57 201 6 -56 201 8 minecraft:podzol
fill -56 201 9 -56 201 9 minecraft:podzol
fill -56 201 15 -56 201 18 minecraft:podzol
fill -59 201 16 -57 201 18 minecraft:podzol
fill -50 201 18 -50 201 18 minecraft:podzol
fill -59 201 9 -57 201 9 minecraft:dirt
fill -59 202 9 -57 202 9 minecraft:podzol
fill -57 201 10 -56 201 10 minecraft:dirt
fill -57 202 10 -56 202 10 minecraft:podzol
fill -56 201 11 -56 201 14 minecraft:dirt
fill -56 202 11 -56 202 14 minecraft:podzol
fill -57 201 14 -57 201 15 minecraft:dirt
fill -57 202 14 -57 202 15 minecraft:podzol
fill -59 201 15 -58 201 15 minecraft:dirt
fill -59 202 15 -58 202 15 minecraft:podzol
fill -59 201 10 -58 202 14 minecraft:dirt
fill -59 203 10 -58 203 14 minecraft:podzol
fill -57 201 11 -57 202 13 minecraft:dirt
fill -57 203 11 -57 203 13 minecraft:podzol
fill -51 201 3 -50 207 4 minecraft:calcite
fill -51 208 3 -50 208 4 minecraft:podzol
fill -51 201 18 -51 207 18 minecraft:calcite
fill -51 208 18 -51 208 18 minecraft:podzol
fill -54 201 18 -52 207 18 minecraft:diorite
fill -54 208 18 -52 208 18 minecraft:podzol
fill -56 201 3 -55 208 4 minecraft:calcite
fill -56 209 3 -55 209 4 minecraft:podzol
fill -57 201 4 -57 208 5 minecraft:calcite
fill -57 209 4 -57 209 5 minecraft:podzol
fill -56 201 5 -56 208 5 minecraft:calcite
fill -56 209 5 -56 209 5 minecraft:podzol
execute positioned -47 202 4 run function rlk:room/prop/fo_col_b
execute positioned -50 202 15 run function rlk:room/prop/fo_lamp2
execute positioned -52 202 1 run function rlk:room/prop/fo_lamp
execute positioned -59 202 16 run function rlk:room/prop/fo_ruin_x
execute positioned -48 202 13 run function rlk:room/prop/fo_flower
execute positioned -46 202 9 run function rlk:room/prop/fo_white
execute positioned -42 202 7 run function rlk:room/prop/p_grass
execute positioned -59 202 8 run function rlk:room/prop/fo_flower
execute positioned -59 204 12 run function rlk:room/prop/p_grass
execute positioned -57 203 10 run function rlk:room/prop/fo_flower
execute positioned -45 202 17 run function rlk:room/prop/fo_flower
execute positioned -49 202 11 run function rlk:room/prop/p_grass
setblock -57 210 4 minecraft:short_grass keep
setblock -57 210 5 minecraft:birch_leaves[persistent=true] keep
setblock -56 210 4 minecraft:short_grass keep
setblock -56 210 5 minecraft:birch_leaves[persistent=true] keep
setblock -55 210 3 minecraft:birch_leaves[persistent=true] keep
setblock -55 210 4 minecraft:birch_leaves[persistent=true] keep
setblock -54 209 18 minecraft:birch_leaves[persistent=true] keep
setblock -51 209 4 minecraft:short_grass keep
setblock -51 209 18 minecraft:short_grass keep
setblock -50 209 3 minecraft:birch_leaves[persistent=true] keep
