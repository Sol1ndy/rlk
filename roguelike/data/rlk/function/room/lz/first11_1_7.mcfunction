# 구역 건설 (first11_1, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 5 200 1 6 200 2 minecraft:moss_block
fill 3 200 16 4 200 18 minecraft:calcite
fill 0 205 14 0 208 19 minecraft:calcite
fill 0 205 10 0 206 15 minecraft:prismarine
fill 0 210 1 0 210 1 minecraft:oak_leaves[persistent=true]
fill 19 207 7 19 208 11 minecraft:moss_block
fill 19 210 16 19 210 18 minecraft:oak_leaves[persistent=true]
fill 19 203 3 19 205 8 minecraft:diorite
fill 19 205 13 19 206 15 minecraft:moss_block
fill 3 208 0 6 210 0 minecraft:calcite
fill 12 205 0 14 208 0 minecraft:moss_block
fill 3 203 0 4 206 0 minecraft:calcite
fill 6 209 19 8 210 19 minecraft:oak_leaves[persistent=true]
fill 7 208 19 10 210 19 minecraft:calcite
fill 0 202 19 0 203 19 minecraft:prismarine
fill 3 209 19 4 210 19 minecraft:birch_leaves[persistent=true]
fill 12 210 19 13 210 19 minecraft:birch_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 4 201 3 6 201 3 minecraft:podzol
fill 2 201 4 2 201 10 minecraft:podzol
fill 5 201 4 8 201 4 minecraft:podzol
fill 6 201 5 8 201 5 minecraft:podzol
fill 1 201 6 1 201 8 minecraft:podzol
fill 5 201 6 5 201 11 minecraft:podzol
fill 3 201 9 3 201 10 minecraft:podzol
fill 4 201 10 4 201 11 minecraft:podzol
fill 5 201 5 5 201 5 minecraft:dirt
fill 5 202 5 5 202 5 minecraft:podzol
fill 3 201 6 4 201 8 minecraft:dirt
fill 3 202 6 4 202 8 minecraft:podzol
fill 4 201 9 4 201 9 minecraft:dirt
fill 4 202 9 4 202 9 minecraft:podzol
fill 3 201 4 4 207 5 minecraft:calcite
fill 3 208 4 4 208 5 minecraft:podzol
fill 15 199 7 16 199 13 minecraft:clay
fill 15 200 7 16 200 13 minecraft:water
fill 1 199 10 1 199 16 minecraft:clay
fill 1 200 10 1 200 16 minecraft:water
fill 2 199 11 3 199 16 minecraft:clay
fill 2 200 11 3 200 16 minecraft:water
fill 4 199 12 5 199 14 minecraft:clay
fill 4 200 12 5 200 14 minecraft:water
fill 4 199 15 4 199 15 minecraft:clay
fill 4 200 15 4 200 15 minecraft:water
fill 1 200 9 1 200 9 minecraft:sand
fill 1 200 17 3 200 17 minecraft:sand
setblock 1 200 10 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock 2 200 13 minecraft:seagrass
setblock 2 200 14 minecraft:sea_pickle[pickles=3,waterlogged=true]
setblock 2 200 16 minecraft:seagrass
setblock 3 200 14 minecraft:seagrass
setblock 15 200 13 minecraft:sea_pickle[pickles=1,waterlogged=true]
execute positioned 12 201 5 run function rlk:room/prop/fo_tree
execute positioned 8 202 5 run function rlk:room/prop/fo_lamp
execute positioned 6 201 18 run function rlk:room/prop/fo_flower
execute positioned 13 201 13 run function rlk:room/prop/fo_white
execute positioned 17 201 12 run function rlk:room/prop/fo_flower
execute positioned 12 201 10 run function rlk:room/prop/fo_white
execute positioned 18 201 7 run function rlk:room/prop/fo_flower
execute positioned 13 201 7 run function rlk:room/prop/fo_flower
execute positioned 18 201 15 run function rlk:room/prop/fo_flower
execute positioned 11 201 3 run function rlk:room/prop/fo_white
execute positioned 18 201 8 run function rlk:room/prop/fo_flower
setblock 3 209 5 minecraft:birch_leaves[persistent=true] keep
setblock 4 209 5 minecraft:birch_leaves[persistent=true] keep
