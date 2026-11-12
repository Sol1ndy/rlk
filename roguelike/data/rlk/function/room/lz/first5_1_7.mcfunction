# 구역 건설 (first5_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 13 200 13 17 200 14 minecraft:gravel
fill 5 200 8 6 200 11 minecraft:coarse_dirt
fill 0 210 17 0 210 19 minecraft:dark_prismarine
fill 0 210 5 0 210 5 minecraft:diorite
fill 0 202 15 0 202 17 minecraft:diorite
fill 0 209 16 0 210 17 minecraft:oak_leaves[persistent=true]
fill 0 207 13 0 207 13 minecraft:calcite
fill 19 202 12 19 205 17 minecraft:calcite
fill 19 210 1 19 210 5 minecraft:birch_leaves[persistent=true]
fill 19 202 17 19 205 19 minecraft:diorite
fill 19 207 4 19 208 9 minecraft:prismarine
fill 19 209 13 19 210 14 minecraft:birch_leaves[persistent=true]
fill 5 204 0 7 207 0 minecraft:moss_block
fill 18 209 0 18 210 0 minecraft:oak_leaves[persistent=true]
fill 11 208 0 16 209 0 minecraft:moss_block
fill 12 209 0 13 210 0 minecraft:birch_leaves[persistent=true]
fill 14 210 19 19 210 19 minecraft:birch_leaves[persistent=true]
fill 11 209 19 16 210 19 minecraft:oak_leaves[persistent=true]
fill 14 207 19 19 210 19 minecraft:calcite
fill 11 210 19 13 210 19 minecraft:calcite
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 7 201 15 13 201 15 minecraft:podzol
fill 7 201 16 8 201 16 minecraft:podzol
fill 14 201 16 18 201 16 minecraft:podzol
fill 7 201 17 7 201 18 minecraft:podzol
fill 8 201 18 8 201 18 minecraft:podzol
fill 9 201 16 13 201 18 minecraft:dirt
fill 9 202 16 13 202 18 minecraft:podzol
fill 8 201 17 8 201 17 minecraft:dirt
fill 8 202 17 8 202 17 minecraft:podzol
fill 14 201 17 18 201 18 minecraft:dirt
fill 14 202 17 18 202 18 minecraft:podzol
fill 1 199 1 4 199 2 minecraft:clay
fill 1 200 1 4 200 2 minecraft:water
fill 1 199 3 2 199 16 minecraft:clay
fill 1 200 3 2 200 16 minecraft:water
fill 3 199 5 3 199 16 minecraft:clay
fill 3 200 5 3 200 16 minecraft:water
fill 4 199 6 5 199 16 minecraft:clay
fill 4 200 6 5 200 16 minecraft:water
fill 6 199 15 6 199 16 minecraft:clay
fill 6 200 15 6 200 16 minecraft:water
fill 3 200 3 4 200 4 minecraft:spruce_planks
fill 4 200 5 5 200 5 minecraft:spruce_planks
fill 6 200 5 6 200 5 minecraft:sand
fill 1 200 17 6 200 17 minecraft:sand
setblock 1 200 1 minecraft:seagrass
setblock 1 200 2 minecraft:seagrass
setblock 1 200 3 minecraft:seagrass
setblock 2 200 9 minecraft:seagrass
setblock 2 200 11 minecraft:seagrass
setblock 2 200 12 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 3 200 6 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 3 200 8 minecraft:seagrass
setblock 6 200 16 minecraft:seagrass
execute positioned 12 203 17 run function rlk:room/prop/fo_rock
execute positioned 13 201 9 run function rlk:room/prop/fo_flower
execute positioned 14 201 7 run function rlk:room/prop/fo_flower
execute positioned 10 201 4 run function rlk:room/prop/fo_flower
execute positioned 8 201 2 run function rlk:room/prop/fo_flower
execute positioned 15 201 12 run function rlk:room/prop/fo_flower
execute positioned 11 201 8 run function rlk:room/prop/fo_flower
execute positioned 18 201 3 run function rlk:room/prop/fo_white
execute positioned 17 201 10 run function rlk:room/prop/fo_white
