# 구역 건설 (normal24_7, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -48 200 -33 -44 200 -32 minecraft:moss_block
fill -48 200 -37 -46 200 -34 minecraft:moss_block
fill -60 209 -32 -60 210 -27 minecraft:oak_leaves[persistent=true]
fill -60 209 -29 -60 210 -28 minecraft:birch_leaves[persistent=true]
fill -60 210 -26 -60 210 -22 minecraft:diorite
fill -60 209 -35 -60 210 -31 minecraft:moss_block
fill -60 201 -27 -60 203 -25 minecraft:calcite
fill -41 209 -34 -41 210 -33 minecraft:birch_leaves[persistent=true]
fill -41 210 -36 -41 210 -35 minecraft:birch_leaves[persistent=true]
fill -41 204 -39 -41 206 -35 minecraft:diorite
fill -41 209 -40 -41 210 -38 minecraft:calcite
fill -41 201 -23 -41 203 -22 minecraft:moss_block
fill -41 210 -25 -41 210 -23 minecraft:birch_leaves[persistent=true]
fill -47 209 -40 -46 210 -40 minecraft:moss_block
fill -58 206 -40 -55 208 -40 minecraft:diorite
fill -56 207 -40 -52 209 -40 minecraft:diorite
fill -50 209 -21 -49 209 -21 minecraft:moss_block
fill -50 209 -21 -45 210 -21 minecraft:birch_leaves[persistent=true]
fill -46 206 -21 -43 206 -21 minecraft:diorite
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -58 201 -39 -57 201 -39 minecraft:podzol
fill -51 201 -39 -50 201 -39 minecraft:podzol
fill -57 201 -38 -57 201 -37 minecraft:podzol
fill -51 201 -38 -51 201 -37 minecraft:podzol
fill -56 201 -37 -56 201 -37 minecraft:podzol
fill -52 201 -37 -52 201 -36 minecraft:podzol
fill -55 201 -36 -53 201 -36 minecraft:podzol
fill -54 201 -35 -54 201 -35 minecraft:podzol
fill -51 201 -25 -47 201 -24 minecraft:podzol
fill -46 201 -24 -42 201 -22 minecraft:podzol
fill -48 201 -23 -47 201 -22 minecraft:podzol
fill -56 201 -39 -52 201 -38 minecraft:dirt
fill -56 202 -39 -52 202 -38 minecraft:podzol
fill -55 201 -37 -53 201 -37 minecraft:dirt
fill -55 202 -37 -53 202 -37 minecraft:podzol
fill -51 201 -23 -49 206 -22 minecraft:diorite
fill -51 207 -23 -49 207 -22 minecraft:podzol
fill -57 201 -36 -56 207 -35 minecraft:calcite
fill -57 208 -36 -56 208 -35 minecraft:podzol
execute positioned -59 201 -28 run function rlk:room/prop/fo_crates
execute positioned -45 201 -37 run function rlk:room/prop/fo_crates
execute positioned -56 201 -25 run function rlk:room/prop/fo_flower
execute positioned -56 201 -32 run function rlk:room/prop/fo_flower
execute positioned -47 202 -23 run function rlk:room/prop/p_grass
execute positioned -56 201 -26 run function rlk:room/prop/fo_white
execute positioned -42 201 -38 run function rlk:room/prop/p_grass
execute positioned -46 201 -36 run function rlk:room/prop/fo_white
execute positioned -47 202 -22 run function rlk:room/prop/p_grass
setblock -57 209 -36 minecraft:short_grass keep
setblock -56 209 -36 minecraft:birch_leaves[persistent=true] keep
setblock -56 209 -35 minecraft:birch_leaves[persistent=true] keep
setblock -51 208 -23 minecraft:short_grass keep
setblock -51 208 -22 minecraft:birch_leaves[persistent=true] keep
setblock -50 208 -23 minecraft:birch_leaves[persistent=true] keep
setblock -50 208 -22 minecraft:short_grass keep
setblock -49 208 -23 minecraft:birch_leaves[persistent=true] keep
setblock -49 208 -22 minecraft:birch_leaves[persistent=true] keep
