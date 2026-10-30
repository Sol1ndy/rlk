# 구역 건설 (levelup2_5, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -48 200 -36 -46 200 -34 minecraft:calcite
fill -49 200 -39 -47 200 -38 minecraft:calcite
fill -60 210 -30 -60 210 -25 minecraft:oak_leaves[persistent=true]
fill -60 204 -34 -60 207 -34 minecraft:moss_block
fill -60 209 -29 -60 210 -26 minecraft:birch_leaves[persistent=true]
fill -60 201 -35 -60 202 -33 minecraft:diorite
fill -41 210 -25 -41 210 -21 minecraft:birch_leaves[persistent=true]
fill -41 210 -28 -41 210 -24 minecraft:birch_leaves[persistent=true]
fill -41 207 -28 -41 210 -25 minecraft:moss_block
fill -41 201 -34 -41 201 -29 minecraft:calcite
fill -41 210 -38 -41 210 -37 minecraft:birch_leaves[persistent=true]
fill -53 209 -40 -50 209 -40 minecraft:prismarine
fill -46 210 -21 -42 210 -21 minecraft:birch_leaves[persistent=true]
fill -51 201 -21 -46 201 -21 minecraft:prismarine
fill -53 210 -21 -49 210 -21 minecraft:birch_leaves[persistent=true]
fill -52 201 -21 -50 202 -21 minecraft:dark_prismarine
fill -52 201 -21 -52 201 -21 minecraft:dark_prismarine
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -59 201 -35 -56 201 -35 minecraft:podzol
fill -56 201 -34 -55 201 -34 minecraft:podzol
fill -55 201 -33 -55 201 -27 minecraft:podzol
fill -56 201 -27 -56 201 -27 minecraft:podzol
fill -57 201 -26 -57 201 -23 minecraft:podzol
fill -59 201 -23 -58 201 -23 minecraft:podzol
fill -59 201 -34 -57 201 -33 minecraft:dirt
fill -59 202 -34 -57 202 -33 minecraft:podzol
fill -56 201 -33 -56 201 -28 minecraft:dirt
fill -56 202 -33 -56 202 -28 minecraft:podzol
fill -57 201 -27 -57 201 -27 minecraft:dirt
fill -57 202 -27 -57 202 -27 minecraft:podzol
fill -58 201 -26 -58 201 -24 minecraft:dirt
fill -58 202 -26 -58 202 -24 minecraft:podzol
fill -59 201 -25 -59 201 -24 minecraft:dirt
fill -59 202 -25 -59 202 -24 minecraft:podzol
fill -59 201 -32 -57 202 -28 minecraft:dirt
fill -59 203 -32 -57 203 -28 minecraft:podzol
fill -59 201 -27 -58 202 -27 minecraft:dirt
fill -59 203 -27 -58 203 -27 minecraft:podzol
fill -59 201 -26 -59 202 -26 minecraft:dirt
fill -59 203 -26 -59 203 -26 minecraft:podzol
fill -54 201 -39 -52 205 -38 minecraft:calcite
fill -54 206 -39 -52 206 -38 minecraft:podzol
fill -51 201 -39 -50 205 -38 minecraft:diorite
fill -51 206 -39 -50 206 -38 minecraft:podzol
fill -56 201 -36 -55 207 -36 minecraft:calcite
fill -56 208 -36 -55 208 -36 minecraft:podzol
fill -56 201 -37 -55 207 -37 minecraft:diorite
fill -56 208 -37 -55 208 -37 minecraft:podzol
execute positioned -56 203 -28 run function rlk:room/prop/fo_lamp
execute positioned -54 201 -37 run function rlk:room/prop/p_grass
execute positioned -49 201 -39 run function rlk:room/prop/p_grass
execute positioned -50 201 -34 run function rlk:room/prop/p_grass
execute positioned -42 201 -27 run function rlk:room/prop/p_grass
execute positioned -47 201 -25 run function rlk:room/prop/fo_flower
execute positioned -47 201 -33 run function rlk:room/prop/fo_flower
execute positioned -45 201 -31 run function rlk:room/prop/fo_flower
setblock -56 209 -37 minecraft:birch_leaves[persistent=true] keep
setblock -53 207 -39 minecraft:birch_leaves[persistent=true] keep
setblock -53 207 -38 minecraft:birch_leaves[persistent=true] keep
setblock -51 207 -39 minecraft:short_grass keep
setblock -50 207 -39 minecraft:short_grass keep
setblock -50 207 -38 minecraft:short_grass keep
