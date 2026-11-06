# 구역 건설 (levelup0_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:podzol
fill 20 201 20 39 210 39 minecraft:stone
fill 21 201 21 39 210 38 minecraft:air
fill 21 209 21 39 209 38 minecraft:light[level=15]
fill 40 200 20 59 200 39 minecraft:podzol
fill 40 201 20 59 210 39 minecraft:stone
fill 40 201 21 58 210 38 minecraft:air
fill 40 209 21 58 209 38 minecraft:light[level=15]
fill 21 200 29 22 200 30 minecraft:coarse_dirt
fill 28 200 23 32 200 25 minecraft:coarse_dirt
fill 22 200 25 23 200 26 minecraft:coarse_dirt
fill 20 210 21 20 210 26 minecraft:birch_leaves[persistent=true]
fill 20 206 35 20 209 35 minecraft:moss_block
fill 20 209 21 20 210 26 minecraft:oak_leaves[persistent=true]
fill 22 207 20 26 208 20 minecraft:calcite
fill 34 207 20 35 207 20 minecraft:calcite
fill 22 202 20 23 205 20 minecraft:calcite
fill 29 208 20 34 210 20 minecraft:diorite
fill 34 202 20 38 204 20 minecraft:moss_block
fill 20 209 39 24 210 39 minecraft:birch_leaves[persistent=true]
fill 30 208 39 33 208 39 minecraft:calcite
fill 37 201 39 37 201 39 minecraft:calcite
fill 26 209 39 31 210 39 minecraft:birch_leaves[persistent=true]
fill 21 210 39 23 210 39 minecraft:oak_leaves[persistent=true]
fill 59 209 31 59 210 34 minecraft:calcite
fill 59 209 31 59 210 36 minecraft:oak_leaves[persistent=true]
fill 59 210 34 59 210 37 minecraft:birch_leaves[persistent=true]
fill 46 205 20 51 206 20 minecraft:calcite
fill 40 209 20 44 210 20 minecraft:diorite
fill 55 209 20 59 210 20 minecraft:birch_leaves[persistent=true]
fill 42 209 20 42 210 20 minecraft:birch_leaves[persistent=true]
fill 41 210 39 46 210 39 minecraft:birch_leaves[persistent=true]
fill 51 208 39 56 210 39 minecraft:dark_prismarine
fill 54 201 39 54 201 39 minecraft:calcite
fill 49 208 39 54 210 39 minecraft:prismarine
fill 20 210 20 39 210 39 minecraft:polished_deepslate
fill 21 210 21 39 210 38 minecraft:air
fill 40 210 20 59 210 39 minecraft:polished_deepslate
fill 40 210 21 58 210 38 minecraft:air
fill 34 201 25 34 201 27 minecraft:podzol
fill 35 201 26 35 201 32 minecraft:podzol
fill 57 201 27 58 201 37 minecraft:podzol
fill 26 201 28 33 201 28 minecraft:podzol
fill 26 201 29 26 201 30 minecraft:podzol
fill 27 201 30 34 201 30 minecraft:podzol
fill 56 201 33 56 201 37 minecraft:podzol
fill 34 201 28 34 201 29 minecraft:dirt
fill 34 202 28 34 202 29 minecraft:podzol
fill 27 201 29 33 201 29 minecraft:dirt
fill 27 202 29 33 202 29 minecraft:podzol
fill 38 201 38 42 207 38 minecraft:calcite
fill 38 208 38 42 208 38 minecraft:podzol
fill 47 186 26 55 199 31 minecraft:stone
fill 26 186 32 33 199 39 minecraft:stone
fill 48 186 27 54 186 30 minecraft:clay
fill 48 187 27 54 188 30 minecraft:water
fill 48 189 27 54 201 30 minecraft:air
fill 27 186 33 32 186 38 minecraft:clay
fill 27 187 33 32 188 38 minecraft:water
fill 27 189 33 32 201 38 minecraft:air
fill 27 199 21 35 199 24 minecraft:clay
fill 27 200 21 35 200 24 minecraft:water
fill 26 199 23 26 199 24 minecraft:clay
fill 26 200 23 26 200 24 minecraft:water
fill 27 199 25 33 199 26 minecraft:clay
fill 27 200 25 33 200 26 minecraft:water
fill 28 199 27 33 199 27 minecraft:clay
fill 28 200 27 33 200 27 minecraft:water
fill 47 199 33 52 199 34 minecraft:clay
fill 47 200 33 52 200 34 minecraft:water
fill 47 199 35 48 199 35 minecraft:clay
fill 47 200 35 48 200 35 minecraft:water
fill 48 199 38 49 199 38 minecraft:clay
fill 48 200 38 49 200 38 minecraft:water
fill 47 200 36 48 200 37 minecraft:spruce_planks
fill 26 200 21 26 200 22 minecraft:sand
fill 36 200 21 36 200 25 minecraft:sand
fill 26 200 25 26 200 27 minecraft:sand
fill 35 200 25 35 200 25 minecraft:sand
fill 27 200 27 27 200 27 minecraft:sand
fill 49 200 35 50 200 35 minecraft:sand
setblock 27 200 26 minecraft:seagrass
setblock 28 200 25 minecraft:seagrass
setblock 29 200 21 minecraft:seagrass
setblock 31 200 26 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 32 200 22 minecraft:seagrass
setblock 33 200 26 minecraft:seagrass
setblock 34 200 22 minecraft:seagrass
setblock 47 200 34 minecraft:seagrass
setblock 50 200 34 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 51 200 34 minecraft:seagrass
setblock 52 200 33 minecraft:seagrass
execute positioned 56 201 32 run function rlk:room/prop/fo_col_b
execute positioned 43 201 21 run function rlk:room/prop/fo_ruin_z
execute positioned 47 201 28 run function rlk:room/prop/fo_col_b
execute positioned 29 202 30 run function rlk:room/prop/fo_crates
execute positioned 52 201 26 run function rlk:room/prop/fo_lamp
execute positioned 58 201 26 run function rlk:room/prop/fo_lamp
execute positioned 33 201 34 run function rlk:room/prop/fo_lamp
execute positioned 21 201 38 run function rlk:room/prop/fo_lamp
execute positioned 53 201 35 run function rlk:room/prop/p_grass
execute positioned 55 201 26 run function rlk:room/prop/p_grass
execute positioned 53 201 38 run function rlk:room/prop/p_grass
execute positioned 41 201 32 run function rlk:room/prop/fo_flower
execute positioned 26 201 38 run function rlk:room/prop/p_grass
execute positioned 34 201 38 run function rlk:room/prop/fo_flower
execute positioned 23 201 23 run function rlk:room/prop/fo_flower
execute positioned 45 201 28 run function rlk:room/prop/fo_flower
execute positioned 49 201 36 run function rlk:room/prop/fo_flower
execute positioned 50 201 38 run function rlk:room/prop/p_grass
execute positioned 56 201 27 run function rlk:room/prop/fo_flower
execute positioned 49 201 26 run function rlk:room/prop/p_grass
execute positioned 40 201 33 run function rlk:room/prop/p_grass
execute positioned 23 201 29 run function rlk:room/prop/fo_white
setblock 38 209 38 minecraft:birch_leaves[persistent=true] keep
setblock 39 209 38 minecraft:birch_leaves[persistent=true] keep
setblock 40 209 38 minecraft:short_grass keep
