# 구역 건설 (normal23_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -50 200 -31 -48 200 -29 minecraft:moss_block
fill -60 204 -39 -60 207 -35 minecraft:calcite
fill -60 210 -37 -60 210 -32 minecraft:birch_leaves[persistent=true]
fill -60 207 -39 -60 209 -35 minecraft:prismarine
fill -41 210 -38 -41 210 -34 minecraft:birch_leaves[persistent=true]
fill -41 209 -38 -41 210 -36 minecraft:birch_leaves[persistent=true]
fill -41 205 -26 -41 205 -21 minecraft:diorite
fill -41 207 -26 -41 210 -26 minecraft:moss_block
fill -47 210 -40 -42 210 -40 minecraft:moss_block
fill -55 206 -40 -53 209 -40 minecraft:moss_block
fill -46 209 -40 -44 210 -40 minecraft:birch_leaves[persistent=true]
fill -49 210 -40 -47 210 -40 minecraft:birch_leaves[persistent=true]
fill -49 206 -40 -44 208 -40 minecraft:calcite
fill -46 202 -21 -45 202 -21 minecraft:prismarine
fill -52 208 -21 -49 209 -21 minecraft:prismarine
fill -51 203 -21 -47 203 -21 minecraft:calcite
fill -57 205 -21 -54 206 -21 minecraft:calcite
fill -51 209 -21 -50 210 -21 minecraft:calcite
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -57 201 -39 -57 201 -35 minecraft:podzol
fill -56 201 -34 -55 201 -34 minecraft:podzol
fill -55 201 -33 -55 201 -31 minecraft:podzol
fill -57 201 -31 -56 201 -31 minecraft:podzol
fill -59 201 -30 -57 201 -30 minecraft:podzol
fill -56 201 -28 -55 201 -27 minecraft:podzol
fill -55 201 -26 -55 201 -26 minecraft:podzol
fill -54 201 -25 -50 201 -25 minecraft:podzol
fill -51 201 -24 -50 201 -22 minecraft:podzol
fill -58 201 -23 -57 201 -22 minecraft:podzol
fill -58 201 -39 -58 201 -35 minecraft:dirt
fill -58 202 -39 -58 202 -35 minecraft:podzol
fill -57 201 -34 -57 201 -32 minecraft:dirt
fill -57 202 -34 -57 202 -32 minecraft:podzol
fill -56 201 -33 -56 201 -32 minecraft:dirt
fill -56 202 -33 -56 202 -32 minecraft:podzol
fill -59 201 -32 -58 201 -31 minecraft:dirt
fill -59 202 -32 -58 202 -31 minecraft:podzol
fill -56 201 -26 -56 201 -22 minecraft:dirt
fill -56 202 -26 -56 202 -22 minecraft:podzol
fill -55 201 -25 -55 201 -22 minecraft:dirt
fill -55 202 -25 -55 202 -22 minecraft:podzol
fill -54 201 -24 -52 201 -22 minecraft:dirt
fill -54 202 -24 -52 202 -22 minecraft:podzol
fill -59 201 -39 -59 202 -33 minecraft:dirt
fill -59 203 -39 -59 203 -33 minecraft:podzol
fill -58 201 -34 -58 202 -33 minecraft:dirt
fill -58 203 -34 -58 203 -33 minecraft:podzol
fill -59 201 -29 -58 207 -24 minecraft:calcite
fill -59 208 -29 -58 208 -24 minecraft:podzol
fill -57 201 -28 -57 207 -27 minecraft:calcite
fill -57 208 -28 -57 208 -27 minecraft:podzol
fill -57 201 -29 -57 207 -29 minecraft:diorite
fill -57 208 -29 -57 208 -29 minecraft:podzol
fill -57 201 -26 -57 207 -24 minecraft:diorite
fill -57 208 -26 -57 208 -24 minecraft:podzol
execute positioned -59 204 -34 run function rlk:room/prop/fo_col_b
execute positioned -51 202 -25 run function rlk:room/prop/fo_crates
execute positioned -55 202 -33 run function rlk:room/prop/fo_col_a
execute positioned -54 202 -25 run function rlk:room/prop/fo_col_b
execute positioned -44 201 -38 run function rlk:room/prop/p_grass
execute positioned -46 201 -32 run function rlk:room/prop/p_grass
execute positioned -47 201 -30 run function rlk:room/prop/p_grass
execute positioned -51 202 -23 run function rlk:room/prop/p_grass
execute positioned -54 201 -37 run function rlk:room/prop/p_grass
execute positioned -57 202 -36 run function rlk:room/prop/fo_flower
execute positioned -42 201 -26 run function rlk:room/prop/fo_white
execute positioned -48 201 -37 run function rlk:room/prop/fo_white
setblock -59 209 -29 minecraft:short_grass keep
setblock -59 209 -28 minecraft:short_grass keep
setblock -59 209 -27 minecraft:short_grass keep
setblock -59 209 -24 minecraft:short_grass keep
setblock -58 209 -28 minecraft:birch_leaves[persistent=true] keep
setblock -57 209 -29 minecraft:short_grass keep
setblock -57 209 -28 minecraft:birch_leaves[persistent=true] keep
setblock -57 209 -27 minecraft:short_grass keep
setblock -57 209 -25 minecraft:birch_leaves[persistent=true] keep
setblock -57 209 -24 minecraft:birch_leaves[persistent=true] keep
