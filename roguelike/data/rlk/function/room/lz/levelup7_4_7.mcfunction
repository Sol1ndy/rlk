# 구역 건설 (levelup7_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 40 39 200 59 minecraft:podzol
fill 20 201 40 39 215 59 minecraft:stone
fill 21 201 41 38 215 58 minecraft:air
fill 21 214 41 38 214 58 minecraft:light[level=15]
fill 31 205 44 34 205 47 minecraft:gravel
fill 28 205 45 29 205 47 minecraft:calcite
fill 20 207 44 20 207 49 minecraft:calcite
fill 20 215 45 20 215 45 minecraft:birch_leaves[persistent=true]
fill 20 214 58 20 215 59 minecraft:birch_leaves[persistent=true]
fill 20 202 52 20 205 57 minecraft:moss_block
fill 20 212 42 20 214 42 minecraft:diorite
fill 20 209 46 20 212 46 minecraft:calcite
fill 39 201 54 39 201 57 minecraft:moss_block
fill 39 215 57 39 215 58 minecraft:prismarine
fill 39 213 49 39 215 54 minecraft:diorite
fill 29 215 40 33 215 40 minecraft:birch_leaves[persistent=true]
fill 22 215 40 27 215 40 minecraft:oak_leaves[persistent=true]
fill 26 214 40 27 215 40 minecraft:oak_leaves[persistent=true]
fill 33 202 59 38 203 59 minecraft:calcite
fill 25 210 59 27 213 59 minecraft:diorite
fill 31 214 59 34 215 59 minecraft:birch_leaves[persistent=true]
fill 20 215 40 39 215 59 minecraft:polished_deepslate
fill 21 215 41 38 215 58 minecraft:air
fill 21 201 41 38 204 41 minecraft:dirt
fill 21 205 41 38 205 41 minecraft:podzol
fill 21 201 42 22 204 42 minecraft:dirt
fill 21 205 42 22 205 42 minecraft:podzol
fill 24 201 42 38 204 45 minecraft:dirt
fill 24 205 42 38 205 45 minecraft:podzol
fill 26 201 46 38 204 58 minecraft:dirt
fill 26 205 46 38 205 58 minecraft:podzol
fill 21 201 50 25 204 58 minecraft:dirt
fill 21 205 50 25 205 58 minecraft:podzol
fill 23 201 42 23 205 49 minecraft:dirt
fill 23 206 42 23 206 49 minecraft:podzol
fill 22 201 43 22 205 49 minecraft:dirt
fill 22 206 43 22 206 49 minecraft:podzol
fill 24 201 46 25 205 49 minecraft:dirt
fill 24 206 46 25 206 49 minecraft:podzol
fill 21 201 47 21 205 49 minecraft:dirt
fill 21 206 47 21 206 49 minecraft:podzol
fill 21 201 43 21 211 43 minecraft:calcite
fill 21 212 43 21 212 43 minecraft:podzol
fill 21 201 44 21 211 46 minecraft:diorite
fill 21 212 44 21 212 46 minecraft:podzol
fill 20 186 51 25 199 57 minecraft:stone
fill 21 186 52 24 186 56 minecraft:clay
fill 21 187 52 24 188 56 minecraft:water
fill 21 189 52 24 206 56 minecraft:air
fill 27 204 55 33 204 58 minecraft:clay
fill 27 205 55 33 205 58 minecraft:water
fill 34 204 56 36 204 58 minecraft:clay
fill 34 205 56 36 205 58 minecraft:water
fill 37 205 56 37 205 58 minecraft:sand
setblock 28 205 58 minecraft:seagrass
setblock 31 205 56 minecraft:seagrass
setblock 32 205 56 minecraft:seagrass
setblock 33 205 55 minecraft:seagrass
setblock 34 205 58 minecraft:seagrass
setblock 36 205 58 minecraft:sea_pickle[pickles=2,waterlogged=true]
execute positioned 24 207 46 run function rlk:room/prop/fo_crates
execute positioned 33 206 46 run function rlk:room/prop/fo_white
execute positioned 24 206 43 run function rlk:room/prop/fo_flower
execute positioned 21 206 50 run function rlk:room/prop/fo_white
execute positioned 28 206 43 run function rlk:room/prop/fo_flower
execute positioned 22 206 55 run function rlk:room/prop/p_grass
execute positioned 38 206 45 run function rlk:room/prop/p_grass
execute positioned 34 206 45 run function rlk:room/prop/fo_flower
setblock 21 213 43 minecraft:birch_leaves[persistent=true] keep
setblock 21 213 45 minecraft:short_grass keep
setblock 21 213 46 minecraft:birch_leaves[persistent=true] keep
