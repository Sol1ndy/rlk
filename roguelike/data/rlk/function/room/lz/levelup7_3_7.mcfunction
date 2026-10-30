# 구역 건설 (levelup7_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:podzol
fill 20 201 20 39 210 39 minecraft:stone
fill 21 201 21 38 210 38 minecraft:air
fill 21 209 21 38 209 38 minecraft:light[level=15]
fill 26 200 34 29 200 37 minecraft:moss_block
fill 27 200 32 29 200 34 minecraft:calcite
fill 20 204 32 20 207 34 minecraft:moss_block
fill 20 209 30 20 210 30 minecraft:oak_leaves[persistent=true]
fill 20 204 29 20 204 33 minecraft:diorite
fill 20 209 31 20 210 36 minecraft:birch_leaves[persistent=true]
fill 20 206 29 20 208 33 minecraft:calcite
fill 39 201 27 39 201 27 minecraft:calcite
fill 39 209 30 39 210 31 minecraft:calcite
fill 39 209 34 39 210 35 minecraft:prismarine
fill 26 207 20 26 209 20 minecraft:diorite
fill 31 209 20 31 210 20 minecraft:oak_leaves[persistent=true]
fill 35 209 20 39 210 20 minecraft:oak_leaves[persistent=true]
fill 35 209 39 35 210 39 minecraft:birch_leaves[persistent=true]
fill 21 202 39 26 202 39 minecraft:calcite
fill 23 206 39 25 208 39 minecraft:dark_prismarine
fill 34 209 39 38 210 39 minecraft:birch_leaves[persistent=true]
fill 36 209 39 39 209 39 minecraft:calcite
fill 20 210 20 39 210 39 minecraft:polished_deepslate
fill 21 210 21 38 210 38 minecraft:air
fill 34 201 21 34 201 22 minecraft:podzol
fill 35 201 22 35 201 24 minecraft:podzol
fill 36 201 24 37 201 25 minecraft:podzol
fill 38 201 25 38 201 25 minecraft:podzol
fill 35 201 21 38 201 21 minecraft:dirt
fill 35 202 21 38 202 21 minecraft:podzol
fill 36 201 22 38 201 23 minecraft:dirt
fill 36 202 22 38 202 23 minecraft:podzol
fill 38 201 24 38 201 24 minecraft:dirt
fill 38 202 24 38 202 24 minecraft:podzol
fill 28 201 21 30 206 23 minecraft:calcite
fill 28 207 21 30 207 23 minecraft:podzol
fill 33 201 23 34 207 24 minecraft:calcite
fill 33 208 23 34 208 24 minecraft:podzol
fill 35 199 26 38 199 32 minecraft:clay
fill 35 200 26 38 200 32 minecraft:water
fill 35 200 33 38 200 33 minecraft:sand
setblock 35 200 29 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 35 200 32 minecraft:seagrass
setblock 36 200 27 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 36 200 31 minecraft:seagrass
setblock 38 200 27 minecraft:seagrass
execute positioned 24 201 23 run function rlk:room/prop/fo_crates
execute positioned 28 201 37 run function rlk:room/prop/p_grass
execute positioned 37 202 24 run function rlk:room/prop/fo_flower
execute positioned 27 201 24 run function rlk:room/prop/p_grass
execute positioned 22 201 25 run function rlk:room/prop/p_grass
execute positioned 31 201 31 run function rlk:room/prop/p_grass
execute positioned 32 201 21 run function rlk:room/prop/p_grass
execute positioned 29 201 34 run function rlk:room/prop/fo_white
setblock 28 208 21 minecraft:short_grass keep
setblock 28 208 22 minecraft:birch_leaves[persistent=true] keep
setblock 28 208 23 minecraft:birch_leaves[persistent=true] keep
setblock 29 208 23 minecraft:short_grass keep
setblock 30 208 21 minecraft:birch_leaves[persistent=true] keep
setblock 30 208 22 minecraft:birch_leaves[persistent=true] keep
setblock 33 209 24 minecraft:birch_leaves[persistent=true] keep
