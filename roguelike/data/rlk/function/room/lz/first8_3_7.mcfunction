# 구역 건설 (first8_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 215 -41 minecraft:stone
fill 21 201 -59 38 215 -42 minecraft:air
fill 21 214 -59 38 214 -42 minecraft:light[level=15]
fill 21 205 -53 23 205 -51 minecraft:coarse_dirt
fill 20 210 -58 20 211 -56 minecraft:calcite
fill 20 214 -52 20 215 -48 minecraft:oak_leaves[persistent=true]
fill 20 207 -55 20 207 -51 minecraft:moss_block
fill 20 211 -52 20 214 -48 minecraft:dark_prismarine
fill 20 202 -44 20 203 -42 minecraft:calcite
fill 39 214 -54 39 215 -54 minecraft:oak_leaves[persistent=true]
fill 39 203 -46 39 204 -43 minecraft:moss_block
fill 39 215 -44 39 215 -41 minecraft:oak_leaves[persistent=true]
fill 39 214 -57 39 215 -52 minecraft:oak_leaves[persistent=true]
fill 39 214 -53 39 215 -53 minecraft:oak_leaves[persistent=true]
fill 23 215 -60 26 215 -60 minecraft:oak_leaves[persistent=true]
fill 35 207 -60 37 207 -60 minecraft:prismarine
fill 28 214 -60 31 215 -60 minecraft:calcite
fill 29 205 -60 30 207 -60 minecraft:diorite
fill 22 215 -41 23 215 -41 minecraft:birch_leaves[persistent=true]
fill 28 214 -41 31 215 -41 minecraft:birch_leaves[persistent=true]
fill 22 212 -41 24 212 -41 minecraft:prismarine
fill 20 210 -41 21 212 -41 minecraft:moss_block
fill 20 215 -60 39 215 -41 minecraft:polished_deepslate
fill 21 215 -59 38 215 -42 minecraft:air
fill 21 201 -59 25 204 -42 minecraft:dirt
fill 21 205 -59 25 205 -42 minecraft:podzol
fill 26 201 -56 26 204 -42 minecraft:dirt
fill 26 205 -56 26 205 -42 minecraft:podzol
fill 27 201 -54 34 204 -42 minecraft:dirt
fill 27 205 -54 34 205 -42 minecraft:podzol
fill 35 201 -53 37 204 -42 minecraft:dirt
fill 35 205 -53 37 205 -42 minecraft:podzol
fill 38 201 -51 38 204 -42 minecraft:dirt
fill 38 205 -51 38 205 -42 minecraft:podzol
fill 26 201 -59 27 205 -57 minecraft:dirt
fill 26 206 -59 27 206 -57 minecraft:podzol
fill 27 201 -56 27 205 -55 minecraft:dirt
fill 27 206 -56 27 206 -55 minecraft:podzol
fill 28 201 -55 34 205 -55 minecraft:dirt
fill 28 206 -55 34 206 -55 minecraft:podzol
fill 38 201 -55 38 205 -52 minecraft:dirt
fill 38 206 -55 38 206 -52 minecraft:podzol
fill 35 201 -54 37 205 -54 minecraft:dirt
fill 35 206 -54 37 206 -54 minecraft:podzol
fill 28 201 -59 28 206 -56 minecraft:dirt
fill 28 207 -59 28 207 -56 minecraft:podzol
fill 37 201 -59 38 206 -56 minecraft:dirt
fill 37 207 -59 38 207 -56 minecraft:podzol
fill 29 201 -56 34 206 -56 minecraft:dirt
fill 29 207 -56 34 207 -56 minecraft:podzol
fill 35 201 -55 37 206 -55 minecraft:dirt
fill 35 207 -55 37 207 -55 minecraft:podzol
fill 35 201 -59 36 207 -56 minecraft:dirt
fill 35 208 -59 36 208 -56 minecraft:podzol
fill 29 201 -59 29 212 -57 minecraft:calcite
fill 29 213 -59 29 213 -57 minecraft:podzol
fill 33 201 -59 34 212 -57 minecraft:calcite
fill 33 213 -59 34 213 -57 minecraft:podzol
fill 30 201 -59 32 212 -57 minecraft:diorite
fill 30 213 -59 32 213 -57 minecraft:podzol
fill 28 204 -45 32 204 -45 minecraft:clay
fill 28 205 -45 32 205 -45 minecraft:water
fill 29 204 -44 31 204 -44 minecraft:clay
fill 29 205 -44 31 205 -44 minecraft:water
fill 27 205 -45 27 205 -44 minecraft:sand
fill 33 205 -45 33 205 -44 minecraft:sand
fill 32 205 -44 32 205 -44 minecraft:sand
setblock 29 205 -44 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 30 205 -44 minecraft:sea_pickle[pickles=3,waterlogged=true]
execute positioned 23 206 -44 run function rlk:room/prop/fo_tree_b
execute positioned 23 206 -57 run function rlk:room/prop/fo_col_a
execute positioned 34 206 -49 run function rlk:room/prop/p_grass
execute positioned 25 206 -49 run function rlk:room/prop/fo_flower
execute positioned 38 208 -57 run function rlk:room/prop/p_grass
execute positioned 36 206 -47 run function rlk:room/prop/p_grass
execute positioned 21 206 -54 run function rlk:room/prop/fo_flower
execute positioned 28 208 -56 run function rlk:room/prop/p_grass
execute positioned 24 206 -51 run function rlk:room/prop/p_grass
setblock 29 214 -59 minecraft:short_grass keep
setblock 29 214 -58 minecraft:birch_leaves[persistent=true] keep
setblock 29 214 -57 minecraft:birch_leaves[persistent=true] keep
setblock 30 214 -59 minecraft:birch_leaves[persistent=true] keep
setblock 30 214 -58 minecraft:short_grass keep
setblock 31 214 -58 minecraft:birch_leaves[persistent=true] keep
setblock 31 214 -57 minecraft:birch_leaves[persistent=true] keep
setblock 32 214 -59 minecraft:short_grass keep
setblock 32 214 -58 minecraft:birch_leaves[persistent=true] keep
setblock 32 214 -57 minecraft:birch_leaves[persistent=true] keep
setblock 33 214 -59 minecraft:short_grass keep
setblock 33 214 -58 minecraft:birch_leaves[persistent=true] keep
setblock 33 214 -57 minecraft:birch_leaves[persistent=true] keep
setblock 34 214 -58 minecraft:birch_leaves[persistent=true] keep
