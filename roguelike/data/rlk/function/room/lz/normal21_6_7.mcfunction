# 구역 건설 (normal21_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -10 200 -52 -6 200 -50 minecraft:moss_block
fill -4 200 -44 -2 200 -43 minecraft:calcite
fill -20 210 -46 -20 210 -41 minecraft:birch_leaves[persistent=true]
fill -20 209 -45 -20 210 -43 minecraft:birch_leaves[persistent=true]
fill -20 210 -52 -20 210 -52 minecraft:birch_leaves[persistent=true]
fill -20 209 -54 -20 210 -49 minecraft:oak_leaves[persistent=true]
fill -1 202 -42 -1 203 -42 minecraft:calcite
fill -1 201 -42 -1 201 -42 minecraft:calcite
fill -1 201 -57 -1 203 -52 minecraft:prismarine
fill -9 209 -60 -5 210 -60 minecraft:birch_leaves[persistent=true]
fill -14 210 -60 -9 210 -60 minecraft:birch_leaves[persistent=true]
fill -7 210 -60 -3 210 -60 minecraft:oak_leaves[persistent=true]
fill -12 201 -41 -10 201 -41 minecraft:moss_block
fill -5 206 -41 -3 207 -41 minecraft:diorite
fill -11 209 -41 -11 209 -41 minecraft:moss_block
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -44 -17 201 -44 minecraft:podzol
fill -17 201 -43 -17 201 -42 minecraft:podzol
fill -19 201 -43 -18 201 -42 minecraft:dirt
fill -19 202 -43 -18 202 -42 minecraft:podzol
fill -13 201 -59 -13 205 -59 minecraft:calcite
fill -13 206 -59 -13 206 -59 minecraft:podzol
fill -12 201 -59 -8 205 -59 minecraft:diorite
fill -12 206 -59 -8 206 -59 minecraft:podzol
fill -14 199 -56 -9 199 -55 minecraft:clay
fill -14 200 -56 -9 200 -55 minecraft:water
setblock -11 200 -55 minecraft:seagrass
execute positioned -5 201 -56 run function rlk:room/prop/fo_col_b
execute positioned -5 201 -48 run function rlk:room/prop/fo_col_a
execute positioned -2 201 -53 run function rlk:room/prop/fo_lamp
execute positioned -17 201 -47 run function rlk:room/prop/fo_white
execute positioned -19 201 -58 run function rlk:room/prop/fo_flower
execute positioned -7 201 -44 run function rlk:room/prop/fo_flower
execute positioned -13 201 -43 run function rlk:room/prop/p_grass
execute positioned -4 201 -56 run function rlk:room/prop/fo_flower
execute positioned -16 201 -49 run function rlk:room/prop/fo_flower
execute positioned -18 201 -46 run function rlk:room/prop/fo_flower
execute positioned -3 201 -57 run function rlk:room/prop/fo_flower
execute positioned -13 201 -44 run function rlk:room/prop/fo_white
setblock -12 207 -59 minecraft:birch_leaves[persistent=true] keep
setblock -11 207 -59 minecraft:birch_leaves[persistent=true] keep
setblock -8 207 -59 minecraft:short_grass keep
