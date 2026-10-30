# 구역 건설 (normal8_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -60 19 200 -41 minecraft:podzol
fill 0 201 -60 19 210 -41 minecraft:stone
fill 1 201 -59 18 210 -42 minecraft:air
fill 1 209 -59 18 209 -42 minecraft:light[level=15]
fill 8 200 -49 9 200 -46 minecraft:gravel
fill 0 209 -45 0 210 -43 minecraft:birch_leaves[persistent=true]
fill 0 209 -58 0 210 -53 minecraft:oak_leaves[persistent=true]
fill 0 204 -57 0 207 -53 minecraft:diorite
fill 0 210 -49 0 210 -46 minecraft:birch_leaves[persistent=true]
fill 0 210 -53 0 210 -52 minecraft:calcite
fill 19 210 -50 19 210 -46 minecraft:birch_leaves[persistent=true]
fill 19 206 -44 19 208 -41 minecraft:diorite
fill 19 209 -56 19 210 -51 minecraft:oak_leaves[persistent=true]
fill 19 209 -49 19 210 -47 minecraft:birch_leaves[persistent=true]
fill 19 206 -58 19 208 -54 minecraft:moss_block
fill 7 210 -60 12 210 -60 minecraft:oak_leaves[persistent=true]
fill 14 209 -60 17 210 -60 minecraft:oak_leaves[persistent=true]
fill 11 201 -60 13 202 -60 minecraft:moss_block
fill 2 209 -60 2 210 -60 minecraft:birch_leaves[persistent=true]
fill 14 210 -60 17 210 -60 minecraft:oak_leaves[persistent=true]
fill 12 209 -41 12 210 -41 minecraft:birch_leaves[persistent=true]
fill 3 207 -41 6 208 -41 minecraft:diorite
fill 12 204 -41 16 205 -41 minecraft:diorite
fill 12 209 -41 16 210 -41 minecraft:birch_leaves[persistent=true]
fill 0 210 -60 19 210 -41 minecraft:polished_deepslate
fill 1 210 -59 18 210 -42 minecraft:air
fill 1 201 -59 5 201 -57 minecraft:podzol
fill 6 201 -57 6 201 -57 minecraft:podzol
fill 15 201 -52 18 201 -51 minecraft:podzol
fill 15 201 -50 15 201 -47 minecraft:podzol
fill 16 201 -47 18 201 -47 minecraft:podzol
fill 16 201 -50 18 201 -48 minecraft:dirt
fill 16 202 -50 18 202 -48 minecraft:podzol
fill 8 201 -57 9 206 -57 minecraft:calcite
fill 8 207 -57 9 207 -57 minecraft:podzol
fill 8 201 -56 9 206 -56 minecraft:diorite
fill 8 207 -56 9 207 -56 minecraft:podzol
fill 7 186 -45 19 199 -41 minecraft:stone
fill 8 186 -44 18 186 -42 minecraft:clay
fill 8 187 -44 18 188 -42 minecraft:water
fill 8 189 -44 18 201 -42 minecraft:air
fill 14 199 -57 16 199 -55 minecraft:clay
fill 14 200 -57 16 200 -55 minecraft:water
fill 13 199 -56 13 199 -55 minecraft:clay
fill 13 200 -56 13 200 -55 minecraft:water
fill 17 199 -56 18 199 -53 minecraft:clay
fill 17 200 -56 18 200 -53 minecraft:water
fill 15 199 -54 16 199 -53 minecraft:clay
fill 15 200 -54 16 200 -53 minecraft:water
fill 14 200 -58 15 200 -58 minecraft:sand
fill 13 200 -57 13 200 -57 minecraft:sand
fill 17 200 -57 18 200 -57 minecraft:sand
setblock 16 200 -54 minecraft:seagrass
setblock 17 200 -53 minecraft:seagrass
setblock 18 200 -55 minecraft:seagrass
execute positioned 1 202 -57 run function rlk:room/prop/fo_lamp
execute positioned 1 201 -43 run function rlk:room/prop/fo_rock
execute positioned 6 201 -59 run function rlk:room/prop/fo_rock_s
execute positioned 17 203 -48 run function rlk:room/prop/fo_flower
execute positioned 4 201 -44 run function rlk:room/prop/p_grass
execute positioned 12 201 -46 run function rlk:room/prop/p_grass
execute positioned 16 201 -58 run function rlk:room/prop/fo_flower
execute positioned 17 203 -50 run function rlk:room/prop/fo_flower
execute positioned 12 201 -48 run function rlk:room/prop/p_grass
execute positioned 9 201 -47 run function rlk:room/prop/fo_flower
setblock 8 208 -57 minecraft:short_grass keep
setblock 8 208 -56 minecraft:short_grass keep
setblock 9 208 -56 minecraft:birch_leaves[persistent=true] keep
