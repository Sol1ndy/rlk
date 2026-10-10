# 구역 건설 (levelup7_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:podzol
fill 20 201 20 39 215 39 minecraft:stone
fill 21 201 21 38 215 38 minecraft:air
fill 21 214 21 38 214 38 minecraft:light[level=15]
fill 26 205 34 29 205 37 minecraft:moss_block
fill 27 205 32 29 205 34 minecraft:calcite
fill 20 209 32 20 212 34 minecraft:moss_block
fill 20 202 30 20 203 35 minecraft:moss_block
fill 20 214 30 20 215 30 minecraft:oak_leaves[persistent=true]
fill 20 209 29 20 209 33 minecraft:diorite
fill 20 214 31 20 215 36 minecraft:birch_leaves[persistent=true]
fill 20 211 29 20 213 33 minecraft:calcite
fill 39 204 27 39 206 27 minecraft:calcite
fill 39 214 30 39 215 31 minecraft:calcite
fill 39 214 34 39 215 35 minecraft:prismarine
fill 39 203 30 39 205 31 minecraft:prismarine
fill 26 212 20 26 214 20 minecraft:diorite
fill 31 214 20 31 215 20 minecraft:oak_leaves[persistent=true]
fill 35 214 20 39 215 20 minecraft:oak_leaves[persistent=true]
fill 26 202 20 30 204 20 minecraft:calcite
fill 35 214 39 35 215 39 minecraft:birch_leaves[persistent=true]
fill 21 207 39 26 207 39 minecraft:calcite
fill 25 204 39 26 204 39 minecraft:calcite
fill 23 211 39 25 213 39 minecraft:dark_prismarine
fill 34 214 39 38 215 39 minecraft:birch_leaves[persistent=true]
fill 36 214 39 39 214 39 minecraft:calcite
fill 20 215 20 39 215 39 minecraft:polished_deepslate
fill 21 215 21 38 215 38 minecraft:air
fill 21 201 21 27 204 38 minecraft:dirt
fill 21 205 21 27 205 38 minecraft:podzol
fill 31 201 21 33 204 22 minecraft:dirt
fill 31 205 21 33 205 22 minecraft:podzol
fill 31 201 23 32 204 38 minecraft:dirt
fill 31 205 23 32 205 38 minecraft:podzol
fill 28 201 24 30 204 38 minecraft:dirt
fill 28 205 24 30 205 38 minecraft:podzol
fill 33 201 25 35 204 38 minecraft:dirt
fill 33 205 25 35 205 38 minecraft:podzol
fill 36 201 26 38 204 38 minecraft:dirt
fill 36 205 26 38 205 38 minecraft:podzol
fill 34 201 21 34 205 22 minecraft:dirt
fill 34 206 21 34 206 22 minecraft:podzol
fill 35 201 22 35 205 24 minecraft:dirt
fill 35 206 22 35 206 24 minecraft:podzol
fill 36 201 24 37 205 25 minecraft:dirt
fill 36 206 24 37 206 25 minecraft:podzol
fill 38 201 25 38 205 25 minecraft:dirt
fill 38 206 25 38 206 25 minecraft:podzol
fill 35 201 21 38 206 21 minecraft:dirt
fill 35 207 21 38 207 21 minecraft:podzol
fill 36 201 22 38 206 23 minecraft:dirt
fill 36 207 22 38 207 23 minecraft:podzol
fill 38 201 24 38 206 24 minecraft:dirt
fill 38 207 24 38 207 24 minecraft:podzol
fill 28 201 21 30 211 23 minecraft:calcite
fill 28 212 21 30 212 23 minecraft:podzol
fill 33 201 23 34 212 24 minecraft:calcite
fill 33 213 23 34 213 24 minecraft:podzol
fill 35 204 26 38 204 32 minecraft:clay
fill 35 205 26 38 205 32 minecraft:water
fill 35 205 33 38 205 33 minecraft:sand
setblock 35 205 29 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 35 205 32 minecraft:seagrass
setblock 36 205 27 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 36 205 31 minecraft:seagrass
setblock 38 205 27 minecraft:seagrass
execute positioned 24 206 23 run function rlk:room/prop/fo_crates
execute positioned 28 206 37 run function rlk:room/prop/p_grass
execute positioned 37 207 24 run function rlk:room/prop/fo_flower
execute positioned 27 206 24 run function rlk:room/prop/p_grass
execute positioned 22 206 25 run function rlk:room/prop/p_grass
execute positioned 31 206 31 run function rlk:room/prop/p_grass
execute positioned 32 206 21 run function rlk:room/prop/p_grass
execute positioned 29 206 34 run function rlk:room/prop/fo_white
setblock 28 213 21 minecraft:short_grass keep
setblock 28 213 22 minecraft:birch_leaves[persistent=true] keep
setblock 28 213 23 minecraft:birch_leaves[persistent=true] keep
setblock 29 213 23 minecraft:short_grass keep
setblock 30 213 21 minecraft:birch_leaves[persistent=true] keep
setblock 30 213 22 minecraft:birch_leaves[persistent=true] keep
setblock 33 214 24 minecraft:birch_leaves[persistent=true] keep
