# 구역 건설 (normal6_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -20 59 200 -1 minecraft:podzol
fill 40 201 -20 59 210 -1 minecraft:stone
fill 41 201 -19 58 210 -2 minecraft:air
fill 41 209 -19 58 209 -2 minecraft:light[level=15]
fill 50 200 -17 53 200 -15 minecraft:gravel
fill 48 200 -11 51 200 -9 minecraft:calcite
fill 40 209 -19 40 210 -19 minecraft:birch_leaves[persistent=true]
fill 40 209 -3 40 210 -2 minecraft:birch_leaves[persistent=true]
fill 40 201 -12 40 201 -11 minecraft:calcite
fill 40 207 -7 40 207 -2 minecraft:prismarine
fill 59 209 -16 59 210 -12 minecraft:oak_leaves[persistent=true]
fill 40 209 -20 43 209 -20 minecraft:dark_prismarine
fill 47 201 -20 47 201 -20 minecraft:diorite
fill 57 210 -20 57 210 -20 minecraft:birch_leaves[persistent=true]
fill 54 202 -20 57 205 -20 minecraft:calcite
fill 48 210 -1 48 210 -1 minecraft:birch_leaves[persistent=true]
fill 43 203 -1 48 203 -1 minecraft:calcite
fill 51 201 -1 52 201 -1 minecraft:moss_block
fill 40 210 -20 59 210 -1 minecraft:polished_deepslate
fill 41 210 -19 58 210 -2 minecraft:air
fill 57 201 -12 58 201 -12 minecraft:podzol
fill 55 201 -11 56 201 -10 minecraft:podzol
fill 55 201 -9 55 201 -3 minecraft:podzol
fill 54 201 -5 54 201 -4 minecraft:podzol
fill 56 201 -4 56 201 -3 minecraft:podzol
fill 57 201 -3 58 201 -2 minecraft:podzol
fill 56 201 -9 56 201 -5 minecraft:dirt
fill 56 202 -9 56 202 -5 minecraft:podzol
fill 57 201 -8 58 201 -4 minecraft:dirt
fill 57 202 -8 58 202 -4 minecraft:podzol
fill 57 201 -11 58 207 -9 minecraft:calcite
fill 57 208 -11 58 208 -9 minecraft:podzol
fill 50 199 -5 52 199 -4 minecraft:clay
fill 50 200 -5 52 200 -4 minecraft:water
fill 53 200 -5 53 200 -5 minecraft:sand
fill 49 200 -3 49 200 -3 minecraft:sand
fill 51 200 -3 52 200 -3 minecraft:sand
execute positioned 45 201 -12 run function rlk:room/prop/fo_col_b
execute positioned 45 201 -5 run function rlk:room/prop/fo_col_b
execute positioned 45 201 -2 run function rlk:room/prop/fo_col_a
execute positioned 43 201 -7 run function rlk:room/prop/fo_lamp
execute positioned 50 201 -12 run function rlk:room/prop/p_grass
execute positioned 50 201 -7 run function rlk:room/prop/fo_flower
execute positioned 55 202 -3 run function rlk:room/prop/p_grass
execute positioned 48 201 -10 run function rlk:room/prop/p_grass
execute positioned 43 201 -17 run function rlk:room/prop/fo_flower
execute positioned 51 201 -19 run function rlk:room/prop/fo_flower
execute positioned 57 201 -19 run function rlk:room/prop/p_grass
execute positioned 51 201 -15 run function rlk:room/prop/fo_flower
execute positioned 54 201 -10 run function rlk:room/prop/p_grass
setblock 57 209 -11 minecraft:birch_leaves[persistent=true] keep
setblock 57 209 -9 minecraft:birch_leaves[persistent=true] keep
setblock 58 209 -11 minecraft:birch_leaves[persistent=true] keep
setblock 58 209 -9 minecraft:short_grass keep
