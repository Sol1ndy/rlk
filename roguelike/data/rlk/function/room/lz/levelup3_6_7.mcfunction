# 구역 건설 (levelup3_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -20 -41 200 -1 minecraft:podzol
fill -60 201 -20 -41 211 -1 minecraft:stone
fill -59 201 -19 -42 211 -2 minecraft:air
fill -59 210 -19 -42 210 -2 minecraft:light[level=15]
fill -60 208 -16 -60 210 -12 minecraft:diorite
fill -60 211 -2 -60 211 -2 minecraft:calcite
fill -60 210 -6 -60 211 -6 minecraft:moss_block
fill -41 211 -9 -41 211 -7 minecraft:diorite
fill -41 206 -8 -41 206 -3 minecraft:diorite
fill -41 210 -16 -41 211 -13 minecraft:oak_leaves[persistent=true]
fill -41 207 -5 -41 208 -5 minecraft:diorite
fill -41 202 -19 -41 205 -15 minecraft:dark_prismarine
fill -52 206 -20 -47 209 -20 minecraft:moss_block
fill -52 210 -20 -47 211 -20 minecraft:diorite
fill -45 208 -20 -45 211 -20 minecraft:calcite
fill -48 202 -20 -43 205 -20 minecraft:moss_block
fill -57 207 -20 -56 209 -20 minecraft:moss_block
fill -60 210 -20 -59 211 -20 minecraft:oak_leaves[persistent=true]
fill -48 205 -1 -48 206 -1 minecraft:diorite
fill -52 211 -1 -48 211 -1 minecraft:oak_leaves[persistent=true]
fill -48 208 -1 -43 209 -1 minecraft:diorite
fill -47 206 -1 -45 206 -1 minecraft:moss_block
fill -60 211 -20 -41 211 -1 minecraft:polished_deepslate
fill -59 211 -19 -42 211 -2 minecraft:air
fill -59 201 -19 -45 201 -15 minecraft:podzol
fill -59 201 -14 -46 201 -12 minecraft:podzol
fill -59 201 -11 -58 201 -2 minecraft:podzol
fill -55 201 -11 -46 201 -4 minecraft:podzol
fill -57 201 -9 -56 201 -2 minecraft:podzol
fill -45 201 -8 -42 201 -4 minecraft:podzol
fill -55 201 -3 -53 201 -2 minecraft:podzol
fill -44 201 -19 -42 201 -18 minecraft:dirt
fill -44 202 -19 -42 202 -18 minecraft:podzol
fill -44 201 -17 -44 201 -15 minecraft:dirt
fill -44 202 -17 -44 202 -15 minecraft:podzol
fill -45 201 -14 -45 201 -9 minecraft:dirt
fill -45 202 -14 -45 202 -9 minecraft:podzol
fill -44 201 -10 -42 201 -9 minecraft:dirt
fill -44 202 -10 -42 202 -9 minecraft:podzol
fill -52 201 -3 -42 201 -2 minecraft:dirt
fill -52 202 -3 -42 202 -2 minecraft:podzol
fill -43 201 -17 -42 202 -11 minecraft:dirt
fill -43 203 -17 -42 203 -11 minecraft:podzol
fill -44 201 -14 -44 202 -11 minecraft:dirt
fill -44 203 -14 -44 203 -11 minecraft:podzol
fill -57 201 -11 -56 207 -11 minecraft:calcite
fill -57 208 -11 -56 208 -11 minecraft:podzol
fill -57 201 -10 -56 207 -10 minecraft:diorite
fill -57 208 -10 -56 208 -10 minecraft:podzol
fill -45 200 -8 -42 200 -5 minecraft:clay
fill -45 201 -8 -42 201 -5 minecraft:water
setblock -45 201 -8 minecraft:seagrass
setblock -45 201 -6 minecraft:seagrass
setblock -45 201 -5 minecraft:seagrass
execute positioned -56 202 -5 run function rlk:room/prop/fo_tree_b
execute positioned -59 202 -6 run function rlk:room/prop/fo_rock_s
execute positioned -53 202 -4 run function rlk:room/prop/fo_rock_s
execute positioned -49 202 -4 run function rlk:room/prop/fo_flower
execute positioned -43 204 -12 run function rlk:room/prop/fo_flower
execute positioned -55 202 -2 run function rlk:room/prop/p_grass
execute positioned -54 202 -10 run function rlk:room/prop/p_grass
execute positioned -59 202 -13 run function rlk:room/prop/fo_flower
execute positioned -57 202 -14 run function rlk:room/prop/fo_white
execute positioned -55 202 -9 run function rlk:room/prop/p_grass
execute positioned -46 202 -15 run function rlk:room/prop/p_grass
setblock -56 209 -11 minecraft:short_grass keep
setblock -56 209 -10 minecraft:short_grass keep
