# 구역 건설 (levelup7_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 40 39 200 59 minecraft:podzol
fill 20 201 40 39 210 59 minecraft:stone
fill 21 201 41 38 210 58 minecraft:air
fill 21 209 41 38 209 58 minecraft:light[level=15]
fill 31 200 44 34 200 47 minecraft:gravel
fill 28 200 45 29 200 47 minecraft:calcite
fill 20 202 44 20 202 49 minecraft:calcite
fill 20 210 45 20 210 45 minecraft:birch_leaves[persistent=true]
fill 20 209 58 20 210 59 minecraft:birch_leaves[persistent=true]
fill 20 207 42 20 209 42 minecraft:diorite
fill 20 204 46 20 207 46 minecraft:calcite
fill 39 210 57 39 210 58 minecraft:prismarine
fill 39 208 49 39 210 54 minecraft:diorite
fill 29 210 40 33 210 40 minecraft:birch_leaves[persistent=true]
fill 22 210 40 27 210 40 minecraft:oak_leaves[persistent=true]
fill 26 209 40 27 210 40 minecraft:oak_leaves[persistent=true]
fill 25 205 59 27 208 59 minecraft:diorite
fill 31 209 59 34 210 59 minecraft:birch_leaves[persistent=true]
fill 20 210 40 39 210 59 minecraft:polished_deepslate
fill 21 210 41 38 210 58 minecraft:air
fill 23 201 42 23 201 49 minecraft:podzol
fill 22 201 43 22 201 49 minecraft:podzol
fill 24 201 46 25 201 49 minecraft:podzol
fill 21 201 47 21 201 49 minecraft:podzol
fill 21 201 43 21 206 43 minecraft:calcite
fill 21 207 43 21 207 43 minecraft:podzol
fill 21 201 44 21 206 46 minecraft:diorite
fill 21 207 44 21 207 46 minecraft:podzol
fill 20 186 51 25 199 57 minecraft:stone
fill 21 186 52 24 186 56 minecraft:clay
fill 21 187 52 24 188 56 minecraft:water
fill 21 189 52 24 201 56 minecraft:air
fill 27 199 55 33 199 58 minecraft:clay
fill 27 200 55 33 200 58 minecraft:water
fill 34 199 56 36 199 58 minecraft:clay
fill 34 200 56 36 200 58 minecraft:water
fill 37 200 56 37 200 58 minecraft:sand
setblock 28 200 58 minecraft:seagrass
setblock 31 200 56 minecraft:seagrass
setblock 32 200 56 minecraft:seagrass
setblock 33 200 55 minecraft:seagrass
setblock 34 200 58 minecraft:seagrass
setblock 36 200 58 minecraft:sea_pickle[pickles=2,waterlogged=true]
execute positioned 24 202 46 run function rlk:room/prop/fo_crates
execute positioned 33 201 46 run function rlk:room/prop/fo_white
execute positioned 24 201 43 run function rlk:room/prop/fo_flower
execute positioned 21 201 50 run function rlk:room/prop/fo_white
execute positioned 28 201 43 run function rlk:room/prop/fo_flower
execute positioned 22 201 55 run function rlk:room/prop/p_grass
execute positioned 38 201 45 run function rlk:room/prop/p_grass
execute positioned 34 201 45 run function rlk:room/prop/fo_flower
setblock 21 208 43 minecraft:birch_leaves[persistent=true] keep
setblock 21 208 45 minecraft:short_grass keep
setblock 21 208 46 minecraft:birch_leaves[persistent=true] keep
