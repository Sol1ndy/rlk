# 구역 건설 (first1_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 212 -41 minecraft:stone
fill -19 201 -59 -2 212 -42 minecraft:air
fill -19 211 -59 -2 211 -42 minecraft:light[level=15]
fill -13 202 -54 -9 202 -53 minecraft:coarse_dirt
fill -20 207 -58 -20 207 -54 minecraft:diorite
fill -20 202 -49 -20 205 -45 minecraft:moss_block
fill -20 212 -58 -20 212 -54 minecraft:birch_leaves[persistent=true]
fill -20 205 -55 -20 207 -55 minecraft:dark_prismarine
fill -1 212 -52 -1 212 -52 minecraft:birch_leaves[persistent=true]
fill -1 204 -49 -1 206 -49 minecraft:prismarine
fill -1 206 -54 -1 206 -54 minecraft:prismarine
fill -1 212 -49 -1 212 -48 minecraft:birch_leaves[persistent=true]
fill -1 206 -58 -1 208 -58 minecraft:diorite
fill -18 205 -60 -14 206 -60 minecraft:prismarine
fill -5 211 -60 -2 212 -60 minecraft:birch_leaves[persistent=true]
fill -20 204 -60 -19 207 -60 minecraft:diorite
fill -6 201 -60 -1 204 -60 minecraft:moss_block
fill -4 207 -60 -1 207 -60 minecraft:moss_block
fill -8 204 -41 -5 207 -41 minecraft:moss_block
fill -11 205 -41 -9 205 -41 minecraft:calcite
fill -11 207 -41 -7 207 -41 minecraft:calcite
fill -4 208 -41 -4 209 -41 minecraft:calcite
fill -20 212 -60 -1 212 -41 minecraft:polished_deepslate
fill -19 212 -59 -2 212 -42 minecraft:air
fill -19 201 -59 -10 201 -46 minecraft:dirt
fill -19 202 -59 -10 202 -46 minecraft:podzol
fill -9 201 -55 -9 201 -42 minecraft:dirt
fill -9 202 -55 -9 202 -42 minecraft:podzol
fill -8 201 -54 -6 201 -42 minecraft:dirt
fill -8 202 -54 -6 202 -42 minecraft:podzol
fill -5 201 -53 -2 201 -42 minecraft:dirt
fill -5 202 -53 -2 202 -42 minecraft:podzol
fill -19 201 -45 -19 201 -45 minecraft:dirt
fill -19 202 -45 -19 202 -45 minecraft:podzol
fill -16 201 -45 -10 201 -42 minecraft:dirt
fill -16 202 -45 -10 202 -42 minecraft:podzol
fill -9 201 -59 -9 202 -56 minecraft:dirt
fill -9 203 -59 -9 203 -56 minecraft:podzol
fill -8 201 -56 -8 202 -55 minecraft:dirt
fill -8 203 -56 -8 203 -55 minecraft:podzol
fill -7 201 -55 -6 202 -55 minecraft:dirt
fill -7 203 -55 -6 203 -55 minecraft:podzol
fill -5 201 -54 -2 202 -54 minecraft:dirt
fill -5 203 -54 -2 203 -54 minecraft:podzol
fill -18 201 -45 -17 202 -42 minecraft:dirt
fill -18 203 -45 -17 203 -42 minecraft:podzol
fill -19 201 -44 -19 202 -42 minecraft:dirt
fill -19 203 -44 -19 203 -42 minecraft:podzol
fill -8 201 -59 -8 203 -57 minecraft:dirt
fill -8 204 -59 -8 204 -57 minecraft:podzol
fill -7 201 -58 -7 203 -56 minecraft:dirt
fill -7 204 -58 -7 204 -56 minecraft:podzol
fill -3 201 -56 -2 203 -55 minecraft:dirt
fill -3 204 -56 -2 204 -55 minecraft:podzol
fill -5 201 -55 -4 203 -55 minecraft:dirt
fill -5 204 -55 -4 204 -55 minecraft:podzol
fill -7 201 -59 -2 204 -59 minecraft:dirt
fill -7 205 -59 -2 205 -59 minecraft:podzol
fill -6 201 -58 -2 204 -58 minecraft:dirt
fill -6 205 -58 -2 205 -58 minecraft:podzol
fill -4 201 -57 -2 204 -57 minecraft:dirt
fill -4 205 -57 -2 205 -57 minecraft:podzol
fill -4 201 -56 -4 204 -56 minecraft:dirt
fill -4 205 -56 -4 205 -56 minecraft:podzol
fill -6 201 -57 -5 209 -57 minecraft:calcite
fill -6 210 -57 -5 210 -57 minecraft:podzol
fill -6 201 -56 -5 209 -56 minecraft:diorite
fill -6 210 -56 -5 210 -56 minecraft:podzol
fill -19 201 -57 -13 201 -55 minecraft:clay
fill -19 202 -57 -13 202 -55 minecraft:water
fill -2 201 -52 -2 201 -45 minecraft:clay
fill -2 202 -52 -2 202 -45 minecraft:water
fill -4 201 -46 -3 201 -45 minecraft:clay
fill -4 202 -46 -3 202 -45 minecraft:water
fill -2 202 -53 -2 202 -53 minecraft:sand
fill -4 202 -44 -2 202 -44 minecraft:sand
setblock -16 202 -55 minecraft:seagrass
setblock -15 202 -56 minecraft:seagrass
setblock -13 202 -56 minecraft:seagrass
setblock -2 202 -51 minecraft:seagrass
setblock -2 202 -50 minecraft:sea_pickle[pickles=2,waterlogged=true]
setblock -2 202 -48 minecraft:seagrass
setblock -2 202 -47 minecraft:seagrass
execute positioned -4 203 -42 run function rlk:room/prop/fo_lamp2
execute positioned -9 204 -59 run function rlk:room/prop/fo_flower
execute positioned -13 203 -46 run function rlk:room/prop/fo_flower
execute positioned -6 203 -46 run function rlk:room/prop/fo_flower
execute positioned -3 203 -43 run function rlk:room/prop/fo_flower
execute positioned -8 204 -56 run function rlk:room/prop/fo_flower
execute positioned -19 203 -51 run function rlk:room/prop/p_grass
execute positioned -10 203 -42 run function rlk:room/prop/fo_flower
execute positioned -9 203 -46 run function rlk:room/prop/fo_flower
execute positioned -14 203 -49 run function rlk:room/prop/p_grass
execute positioned -4 203 -53 run function rlk:room/prop/p_grass
setblock -6 211 -57 minecraft:birch_leaves[persistent=true] keep
setblock -5 211 -57 minecraft:birch_leaves[persistent=true] keep
setblock -5 211 -56 minecraft:short_grass keep
