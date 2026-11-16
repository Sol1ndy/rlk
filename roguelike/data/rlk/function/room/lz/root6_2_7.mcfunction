# 구역 건설 (root6_2, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -17 200 -33 -16 200 -31 minecraft:moss_block
fill -12 200 -24 -9 200 -23 minecraft:calcite
fill -20 201 -30 -20 203 -25 minecraft:diorite
fill -20 209 -28 -20 210 -23 minecraft:oak_leaves[persistent=true]
fill -20 209 -31 -20 210 -30 minecraft:birch_leaves[persistent=true]
fill -20 204 -27 -20 204 -25 minecraft:calcite
fill -20 202 -37 -20 202 -37 minecraft:calcite
fill -20 210 -36 -20 210 -33 minecraft:oak_leaves[persistent=true]
fill -1 201 -37 -1 201 -34 minecraft:calcite
fill -1 209 -35 -1 210 -31 minecraft:oak_leaves[persistent=true]
fill -1 209 -32 -1 210 -28 minecraft:birch_leaves[persistent=true]
fill -13 203 -40 -8 205 -40 minecraft:calcite
fill -13 203 -40 -11 204 -40 minecraft:prismarine
fill -12 208 -21 -7 210 -21 minecraft:calcite
fill -4 209 -21 -4 209 -21 minecraft:dark_prismarine
fill -2 208 -21 -1 210 -21 minecraft:moss_block
fill -18 209 -21 -16 210 -21 minecraft:oak_leaves[persistent=true]
fill -4 201 -21 -3 201 -21 minecraft:diorite
fill -12 201 -21 -12 201 -21 minecraft:calcite
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -10 201 -39 -9 201 -39 minecraft:podzol
fill -5 201 -39 -4 201 -39 minecraft:podzol
fill -10 201 -38 -10 201 -38 minecraft:podzol
fill -4 201 -38 -3 201 -38 minecraft:podzol
fill -11 201 -37 -11 201 -35 minecraft:podzol
fill -3 201 -37 -3 201 -34 minecraft:podzol
fill -18 201 -36 -18 201 -35 minecraft:podzol
fill -19 201 -35 -19 201 -35 minecraft:podzol
fill -17 201 -35 -15 201 -34 minecraft:podzol
fill -10 201 -35 -6 201 -35 minecraft:podzol
fill -5 201 -34 -4 201 -34 minecraft:podzol
fill -18 201 -33 -18 201 -26 minecraft:podzol
fill -19 201 -27 -19 201 -27 minecraft:podzol
fill -8 201 -39 -6 201 -36 minecraft:dirt
fill -8 202 -39 -6 202 -36 minecraft:podzol
fill -9 201 -38 -9 201 -36 minecraft:dirt
fill -9 202 -38 -9 202 -36 minecraft:podzol
fill -5 201 -38 -5 201 -35 minecraft:dirt
fill -5 202 -38 -5 202 -35 minecraft:podzol
fill -10 201 -37 -10 201 -36 minecraft:dirt
fill -10 202 -37 -10 202 -36 minecraft:podzol
fill -4 201 -37 -4 201 -35 minecraft:dirt
fill -4 202 -37 -4 202 -35 minecraft:podzol
fill -19 201 -34 -18 201 -34 minecraft:dirt
fill -19 202 -34 -18 202 -34 minecraft:podzol
fill -19 201 -33 -19 201 -28 minecraft:dirt
fill -19 202 -33 -19 202 -28 minecraft:podzol
fill -13 201 -39 -11 206 -39 minecraft:calcite
fill -13 207 -39 -11 207 -39 minecraft:podzol
fill -13 201 -38 -13 206 -38 minecraft:calcite
fill -13 207 -38 -13 207 -38 minecraft:podzol
fill -12 201 -38 -11 206 -38 minecraft:diorite
fill -12 207 -38 -11 207 -38 minecraft:podzol
fill -19 199 -25 -17 199 -22 minecraft:clay
fill -19 200 -25 -17 200 -22 minecraft:water
fill -19 200 -26 -19 200 -26 minecraft:sand
fill -17 200 -26 -17 200 -26 minecraft:sand
setblock -19 200 -25 minecraft:seagrass
setblock -17 200 -24 minecraft:seagrass
execute positioned -4 201 -22 run function rlk:room/prop/fo_lamp2
execute positioned -13 201 -37 run function rlk:room/prop/fo_flower
execute positioned -2 201 -27 run function rlk:room/prop/p_grass
execute positioned -12 201 -25 run function rlk:room/prop/fo_flower
execute positioned -5 202 -34 run function rlk:room/prop/p_grass
execute positioned -17 201 -31 run function rlk:room/prop/p_grass
execute positioned -9 202 -35 run function rlk:room/prop/fo_white
execute positioned -11 202 -36 run function rlk:room/prop/fo_flower
execute positioned -3 201 -30 run function rlk:room/prop/fo_flower
execute positioned -4 201 -24 run function rlk:room/prop/fo_white
execute positioned -6 201 -25 run function rlk:room/prop/fo_white
setblock -13 208 -39 minecraft:birch_leaves[persistent=true] keep
setblock -13 208 -38 minecraft:birch_leaves[persistent=true] keep
setblock -12 208 -39 minecraft:short_grass keep
setblock -12 208 -38 minecraft:short_grass keep
setblock -11 208 -39 minecraft:birch_leaves[persistent=true] keep
setblock -11 208 -38 minecraft:short_grass keep
