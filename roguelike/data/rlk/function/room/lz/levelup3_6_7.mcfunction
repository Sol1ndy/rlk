# 구역 건설 (levelup3_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -20 -41 200 -1 minecraft:podzol
fill -60 201 -20 -41 210 -1 minecraft:stone
fill -59 201 -19 -42 210 -2 minecraft:air
fill -59 209 -19 -42 209 -2 minecraft:light[level=15]
fill -60 207 -16 -60 209 -12 minecraft:diorite
fill -60 210 -2 -60 210 -2 minecraft:calcite
fill -60 209 -6 -60 210 -6 minecraft:moss_block
fill -41 210 -9 -41 210 -7 minecraft:diorite
fill -41 205 -8 -41 205 -3 minecraft:diorite
fill -41 209 -16 -41 210 -13 minecraft:oak_leaves[persistent=true]
fill -41 206 -5 -41 207 -5 minecraft:diorite
fill -41 201 -19 -41 204 -15 minecraft:dark_prismarine
fill -52 205 -20 -47 208 -20 minecraft:moss_block
fill -52 209 -20 -47 210 -20 minecraft:diorite
fill -45 207 -20 -45 210 -20 minecraft:calcite
fill -48 201 -20 -43 204 -20 minecraft:moss_block
fill -57 206 -20 -56 208 -20 minecraft:moss_block
fill -60 209 -20 -59 210 -20 minecraft:oak_leaves[persistent=true]
fill -48 204 -1 -48 205 -1 minecraft:diorite
fill -52 210 -1 -48 210 -1 minecraft:oak_leaves[persistent=true]
fill -48 207 -1 -43 208 -1 minecraft:diorite
fill -47 205 -1 -45 205 -1 minecraft:moss_block
fill -60 210 -20 -41 210 -1 minecraft:polished_deepslate
fill -59 210 -19 -42 210 -2 minecraft:air
fill -44 201 -19 -42 201 -18 minecraft:podzol
fill -44 201 -17 -44 201 -15 minecraft:podzol
fill -45 201 -14 -45 201 -9 minecraft:podzol
fill -44 201 -10 -42 201 -9 minecraft:podzol
fill -43 201 -17 -42 201 -11 minecraft:dirt
fill -43 202 -17 -42 202 -11 minecraft:podzol
fill -44 201 -14 -44 201 -11 minecraft:dirt
fill -44 202 -14 -44 202 -11 minecraft:podzol
fill -57 201 -11 -56 206 -11 minecraft:calcite
fill -57 207 -11 -56 207 -11 minecraft:podzol
fill -57 201 -10 -56 206 -10 minecraft:diorite
fill -57 207 -10 -56 207 -10 minecraft:podzol
fill -45 199 -8 -42 199 -5 minecraft:clay
fill -45 200 -8 -42 200 -5 minecraft:water
setblock -45 200 -8 minecraft:seagrass
setblock -45 200 -6 minecraft:seagrass
setblock -45 200 -5 minecraft:seagrass
execute positioned -56 201 -5 run function rlk:room/prop/fo_tree_b
execute positioned -59 201 -6 run function rlk:room/prop/fo_rock_s
execute positioned -53 201 -4 run function rlk:room/prop/fo_rock_s
execute positioned -49 201 -4 run function rlk:room/prop/fo_flower
execute positioned -43 203 -12 run function rlk:room/prop/fo_flower
execute positioned -55 201 -2 run function rlk:room/prop/p_grass
execute positioned -54 201 -10 run function rlk:room/prop/p_grass
execute positioned -59 201 -13 run function rlk:room/prop/fo_flower
execute positioned -57 201 -14 run function rlk:room/prop/fo_white
execute positioned -55 201 -9 run function rlk:room/prop/p_grass
execute positioned -46 201 -15 run function rlk:room/prop/p_grass
setblock -56 208 -11 minecraft:short_grass keep
setblock -56 208 -10 minecraft:short_grass keep
