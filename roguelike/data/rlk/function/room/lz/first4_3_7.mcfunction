# 구역 건설 (first4_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 11 200 14 12 200 15 minecraft:coarse_dirt
fill 0 204 18 0 204 19 minecraft:moss_block
fill 0 205 13 0 206 18 minecraft:calcite
fill 0 209 11 0 210 13 minecraft:birch_leaves[persistent=true]
fill 19 208 14 19 210 17 minecraft:moss_block
fill 19 201 10 19 201 12 minecraft:calcite
fill 19 207 14 19 208 17 minecraft:calcite
fill 1 208 0 5 209 0 minecraft:prismarine
fill 12 206 0 14 207 0 minecraft:prismarine
fill 2 209 0 3 210 0 minecraft:birch_leaves[persistent=true]
fill 1 202 0 2 204 0 minecraft:prismarine
fill 5 210 0 10 210 0 minecraft:oak_leaves[persistent=true]
fill 13 210 0 18 210 0 minecraft:birch_leaves[persistent=true]
fill 15 201 19 19 203 19 minecraft:moss_block
fill 15 208 19 16 210 19 minecraft:moss_block
fill 7 209 19 11 210 19 minecraft:oak_leaves[persistent=true]
fill 1 204 19 6 204 19 minecraft:dark_prismarine
fill 2 210 19 6 210 19 minecraft:birch_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 1 201 1 2 201 3 minecraft:podzol
fill 12 201 1 13 201 2 minecraft:podzol
fill 3 201 3 5 201 3 minecraft:podzol
fill 13 201 3 13 201 4 minecraft:podzol
fill 6 201 4 6 201 5 minecraft:podzol
fill 7 201 5 12 201 5 minecraft:podzol
fill 3 201 1 11 201 2 minecraft:dirt
fill 3 202 1 11 202 2 minecraft:podzol
fill 6 201 3 10 201 3 minecraft:dirt
fill 6 202 3 10 202 3 minecraft:podzol
fill 7 201 4 10 201 4 minecraft:dirt
fill 7 202 4 10 202 4 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:calcite
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:calcite
fill 12 208 4 12 208 4 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:diorite
fill 12 208 3 12 208 3 minecraft:podzol
fill 15 186 0 19 199 12 minecraft:stone
fill 16 186 1 18 186 11 minecraft:clay
fill 16 187 1 18 188 11 minecraft:water
fill 16 189 1 18 201 11 minecraft:air
fill 16 199 14 18 199 18 minecraft:clay
fill 16 200 14 18 200 18 minecraft:water
fill 6 199 15 15 199 18 minecraft:clay
fill 6 200 15 15 200 18 minecraft:water
fill 5 199 16 5 199 18 minecraft:clay
fill 5 200 16 5 200 18 minecraft:water
fill 15 200 14 15 200 14 minecraft:sand
fill 4 200 16 4 200 18 minecraft:sand
setblock 6 200 18 minecraft:seagrass
setblock 7 200 16 minecraft:seagrass
setblock 8 200 16 minecraft:seagrass
setblock 9 200 17 minecraft:seagrass
setblock 9 200 18 minecraft:seagrass
setblock 11 200 18 minecraft:seagrass
setblock 14 200 15 minecraft:seagrass
setblock 15 200 16 minecraft:seagrass
setblock 15 200 18 minecraft:seagrass
setblock 17 200 16 minecraft:sea_pickle[pickles=1,waterlogged=true]
setblock 17 200 17 minecraft:seagrass
setblock 18 200 15 minecraft:seagrass
setblock 18 200 18 minecraft:seagrass
execute positioned 8 203 4 run function rlk:room/prop/fo_lamp
execute positioned 7 203 1 run function rlk:room/prop/fo_rock_s
execute positioned 7 203 1 run function rlk:room/prop/p_grass
execute positioned 16 201 7 run function rlk:room/prop/p_grass
execute positioned 7 201 8 run function rlk:room/prop/fo_flower
execute positioned 13 201 8 run function rlk:room/prop/fo_flower
execute positioned 2 202 1 run function rlk:room/prop/fo_flower
execute positioned 18 201 4 run function rlk:room/prop/p_grass
execute positioned 4 201 5 run function rlk:room/prop/fo_white
execute positioned 6 201 13 run function rlk:room/prop/fo_white
setblock 11 209 3 minecraft:birch_leaves[persistent=true] keep
setblock 11 209 4 minecraft:short_grass keep
