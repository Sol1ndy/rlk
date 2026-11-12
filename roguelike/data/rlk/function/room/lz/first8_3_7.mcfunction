# 구역 건설 (first8_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 210 -41 minecraft:stone
fill 21 201 -59 38 210 -42 minecraft:air
fill 21 209 -59 38 209 -42 minecraft:light[level=15]
fill 21 200 -53 23 200 -51 minecraft:coarse_dirt
fill 20 205 -58 20 206 -56 minecraft:calcite
fill 20 209 -52 20 210 -48 minecraft:oak_leaves[persistent=true]
fill 20 202 -55 20 202 -51 minecraft:moss_block
fill 20 206 -52 20 209 -48 minecraft:dark_prismarine
fill 39 209 -54 39 210 -54 minecraft:oak_leaves[persistent=true]
fill 39 210 -44 39 210 -41 minecraft:oak_leaves[persistent=true]
fill 39 209 -57 39 210 -52 minecraft:oak_leaves[persistent=true]
fill 39 209 -53 39 210 -53 minecraft:oak_leaves[persistent=true]
fill 23 210 -60 26 210 -60 minecraft:oak_leaves[persistent=true]
fill 35 202 -60 37 202 -60 minecraft:prismarine
fill 28 209 -60 31 210 -60 minecraft:calcite
fill 29 201 -60 30 202 -60 minecraft:diorite
fill 22 210 -41 23 210 -41 minecraft:birch_leaves[persistent=true]
fill 28 209 -41 31 210 -41 minecraft:birch_leaves[persistent=true]
fill 22 207 -41 24 207 -41 minecraft:prismarine
fill 20 205 -41 21 207 -41 minecraft:moss_block
fill 20 210 -60 39 210 -41 minecraft:polished_deepslate
fill 21 210 -59 38 210 -42 minecraft:air
fill 26 201 -59 27 201 -57 minecraft:podzol
fill 27 201 -56 27 201 -55 minecraft:podzol
fill 28 201 -55 34 201 -55 minecraft:podzol
fill 38 201 -55 38 201 -52 minecraft:podzol
fill 35 201 -54 37 201 -54 minecraft:podzol
fill 28 201 -59 28 201 -56 minecraft:dirt
fill 28 202 -59 28 202 -56 minecraft:podzol
fill 37 201 -59 38 201 -56 minecraft:dirt
fill 37 202 -59 38 202 -56 minecraft:podzol
fill 29 201 -56 34 201 -56 minecraft:dirt
fill 29 202 -56 34 202 -56 minecraft:podzol
fill 35 201 -55 37 201 -55 minecraft:dirt
fill 35 202 -55 37 202 -55 minecraft:podzol
fill 35 201 -59 36 202 -56 minecraft:dirt
fill 35 203 -59 36 203 -56 minecraft:podzol
fill 29 201 -59 29 207 -57 minecraft:calcite
fill 29 208 -59 29 208 -57 minecraft:podzol
fill 33 201 -59 34 207 -57 minecraft:calcite
fill 33 208 -59 34 208 -57 minecraft:podzol
fill 30 201 -59 32 207 -57 minecraft:diorite
fill 30 208 -59 32 208 -57 minecraft:podzol
fill 28 199 -45 32 199 -45 minecraft:clay
fill 28 200 -45 32 200 -45 minecraft:water
fill 29 199 -44 31 199 -44 minecraft:clay
fill 29 200 -44 31 200 -44 minecraft:water
fill 27 200 -45 27 200 -44 minecraft:sand
fill 33 200 -45 33 200 -44 minecraft:sand
fill 32 200 -44 32 200 -44 minecraft:sand
setblock 29 200 -44 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 30 200 -44 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned 23 201 -44 run function rlk:room/prop/fo_tree_b
execute positioned 23 201 -57 run function rlk:room/prop/fo_col_a
execute positioned 34 201 -49 run function rlk:room/prop/p_grass
execute positioned 25 201 -49 run function rlk:room/prop/fo_flower
execute positioned 38 203 -57 run function rlk:room/prop/p_grass
execute positioned 36 201 -47 run function rlk:room/prop/p_grass
execute positioned 21 201 -54 run function rlk:room/prop/fo_flower
execute positioned 28 203 -56 run function rlk:room/prop/p_grass
execute positioned 24 201 -51 run function rlk:room/prop/p_grass
setblock 29 209 -59 minecraft:short_grass keep
setblock 29 209 -58 minecraft:birch_leaves[persistent=true] keep
setblock 29 209 -57 minecraft:birch_leaves[persistent=true] keep
setblock 30 209 -59 minecraft:birch_leaves[persistent=true] keep
setblock 30 209 -58 minecraft:short_grass keep
setblock 31 209 -58 minecraft:birch_leaves[persistent=true] keep
setblock 31 209 -57 minecraft:birch_leaves[persistent=true] keep
setblock 32 209 -59 minecraft:short_grass keep
setblock 32 209 -58 minecraft:birch_leaves[persistent=true] keep
setblock 32 209 -57 minecraft:birch_leaves[persistent=true] keep
setblock 33 209 -59 minecraft:short_grass keep
setblock 33 209 -58 minecraft:birch_leaves[persistent=true] keep
setblock 33 209 -57 minecraft:birch_leaves[persistent=true] keep
setblock 34 209 -58 minecraft:birch_leaves[persistent=true] keep
