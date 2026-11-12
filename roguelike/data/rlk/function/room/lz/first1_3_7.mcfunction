# 구역 건설 (first1_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -13 200 -54 -9 200 -53 minecraft:coarse_dirt
fill -20 205 -58 -20 205 -54 minecraft:diorite
fill -20 201 -49 -20 203 -45 minecraft:moss_block
fill -20 210 -58 -20 210 -54 minecraft:birch_leaves[persistent=true]
fill -20 203 -55 -20 205 -55 minecraft:dark_prismarine
fill -1 210 -52 -1 210 -52 minecraft:birch_leaves[persistent=true]
fill -1 202 -49 -1 204 -49 minecraft:prismarine
fill -1 204 -54 -1 204 -54 minecraft:prismarine
fill -1 210 -49 -1 210 -48 minecraft:birch_leaves[persistent=true]
fill -1 204 -58 -1 206 -58 minecraft:diorite
fill -18 203 -60 -14 204 -60 minecraft:prismarine
fill -5 209 -60 -2 210 -60 minecraft:birch_leaves[persistent=true]
fill -20 202 -60 -19 205 -60 minecraft:diorite
fill -6 201 -60 -1 202 -60 minecraft:moss_block
fill -4 205 -60 -1 205 -60 minecraft:moss_block
fill -8 202 -41 -5 205 -41 minecraft:moss_block
fill -11 203 -41 -9 203 -41 minecraft:calcite
fill -11 205 -41 -7 205 -41 minecraft:calcite
fill -4 206 -41 -4 207 -41 minecraft:calcite
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -9 201 -59 -9 201 -56 minecraft:podzol
fill -8 201 -56 -8 201 -55 minecraft:podzol
fill -7 201 -55 -6 201 -55 minecraft:podzol
fill -5 201 -54 -2 201 -54 minecraft:podzol
fill -18 201 -45 -17 201 -42 minecraft:podzol
fill -19 201 -44 -19 201 -42 minecraft:podzol
fill -8 201 -59 -8 201 -57 minecraft:dirt
fill -8 202 -59 -8 202 -57 minecraft:podzol
fill -7 201 -58 -7 201 -56 minecraft:dirt
fill -7 202 -58 -7 202 -56 minecraft:podzol
fill -3 201 -56 -2 201 -55 minecraft:dirt
fill -3 202 -56 -2 202 -55 minecraft:podzol
fill -5 201 -55 -4 201 -55 minecraft:dirt
fill -5 202 -55 -4 202 -55 minecraft:podzol
fill -7 201 -59 -2 202 -59 minecraft:dirt
fill -7 203 -59 -2 203 -59 minecraft:podzol
fill -6 201 -58 -2 202 -58 minecraft:dirt
fill -6 203 -58 -2 203 -58 minecraft:podzol
fill -4 201 -57 -2 202 -57 minecraft:dirt
fill -4 203 -57 -2 203 -57 minecraft:podzol
fill -4 201 -56 -4 202 -56 minecraft:dirt
fill -4 203 -56 -4 203 -56 minecraft:podzol
fill -6 201 -57 -5 207 -57 minecraft:calcite
fill -6 208 -57 -5 208 -57 minecraft:podzol
fill -6 201 -56 -5 207 -56 minecraft:diorite
fill -6 208 -56 -5 208 -56 minecraft:podzol
fill -19 199 -57 -13 199 -55 minecraft:clay
fill -19 200 -57 -13 200 -55 minecraft:water
fill -2 199 -52 -2 199 -45 minecraft:clay
fill -2 200 -52 -2 200 -45 minecraft:water
fill -4 199 -46 -3 199 -45 minecraft:clay
fill -4 200 -46 -3 200 -45 minecraft:water
fill -2 200 -53 -2 200 -53 minecraft:sand
fill -4 200 -44 -2 200 -44 minecraft:sand
setblock -16 200 -55 minecraft:seagrass
setblock -15 200 -56 minecraft:seagrass
setblock -13 200 -56 minecraft:seagrass
setblock -2 200 -51 minecraft:seagrass
setblock -2 200 -50 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -2 200 -48 minecraft:seagrass
setblock -2 200 -47 minecraft:seagrass
execute positioned -4 201 -42 run function rlk:room/prop/fo_lamp2
execute positioned -9 202 -59 run function rlk:room/prop/fo_flower
execute positioned -13 201 -46 run function rlk:room/prop/fo_flower
execute positioned -6 201 -46 run function rlk:room/prop/fo_flower
execute positioned -3 201 -43 run function rlk:room/prop/fo_flower
execute positioned -8 202 -56 run function rlk:room/prop/fo_flower
execute positioned -19 201 -51 run function rlk:room/prop/p_grass
execute positioned -10 201 -42 run function rlk:room/prop/fo_flower
execute positioned -9 201 -46 run function rlk:room/prop/fo_flower
execute positioned -14 201 -49 run function rlk:room/prop/p_grass
execute positioned -4 201 -53 run function rlk:room/prop/p_grass
setblock -6 209 -57 minecraft:birch_leaves[persistent=true] keep
setblock -5 209 -57 minecraft:birch_leaves[persistent=true] keep
setblock -5 209 -56 minecraft:short_grass keep
