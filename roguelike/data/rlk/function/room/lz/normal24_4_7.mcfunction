# 구역 건설 (normal24_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -11 200 -34 -9 200 -32 minecraft:coarse_dirt
fill -19 200 -38 -15 200 -37 minecraft:moss_block
fill -20 210 -32 -20 210 -29 minecraft:birch_leaves[persistent=true]
fill -20 209 -22 -20 210 -21 minecraft:birch_leaves[persistent=true]
fill -20 206 -29 -20 206 -26 minecraft:calcite
fill -20 209 -25 -20 210 -24 minecraft:birch_leaves[persistent=true]
fill -1 210 -26 -1 210 -23 minecraft:diorite
fill -1 209 -40 -1 210 -35 minecraft:calcite
fill -1 207 -40 -1 208 -35 minecraft:prismarine
fill -14 209 -40 -13 209 -40 minecraft:calcite
fill -18 205 -40 -16 206 -40 minecraft:dark_prismarine
fill -19 210 -40 -18 210 -40 minecraft:oak_leaves[persistent=true]
fill -5 209 -21 -2 210 -21 minecraft:birch_leaves[persistent=true]
fill -16 205 -21 -15 205 -21 minecraft:calcite
fill -10 209 -21 -9 210 -21 minecraft:diorite
fill -16 204 -21 -16 205 -21 minecraft:prismarine
fill -6 210 -21 -5 210 -21 minecraft:birch_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -7 201 -39 -7 201 -35 minecraft:podzol
fill -19 201 -35 -17 201 -35 minecraft:podzol
fill -6 201 -35 -6 201 -35 minecraft:podzol
fill -17 201 -34 -16 201 -27 minecraft:podzol
fill -5 201 -34 -5 201 -33 minecraft:podzol
fill -4 201 -33 -2 201 -33 minecraft:podzol
fill -19 201 -26 -17 201 -26 minecraft:podzol
fill -19 201 -25 -18 201 -25 minecraft:podzol
fill -6 201 -39 -5 201 -39 minecraft:dirt
fill -6 202 -39 -5 202 -39 minecraft:podzol
fill -6 201 -38 -6 201 -36 minecraft:dirt
fill -6 202 -38 -6 202 -36 minecraft:podzol
fill -5 201 -35 -5 201 -35 minecraft:dirt
fill -5 202 -35 -5 202 -35 minecraft:podzol
fill -19 201 -34 -18 201 -27 minecraft:dirt
fill -19 202 -34 -18 202 -27 minecraft:podzol
fill -4 201 -34 -2 201 -34 minecraft:dirt
fill -4 202 -34 -2 202 -34 minecraft:podzol
fill -4 201 -39 -2 202 -35 minecraft:dirt
fill -4 203 -39 -2 203 -35 minecraft:podzol
fill -5 201 -38 -5 202 -36 minecraft:dirt
fill -5 203 -38 -5 203 -36 minecraft:podzol
fill -11 201 -36 -10 207 -36 minecraft:calcite
fill -11 208 -36 -10 208 -36 minecraft:podzol
fill -7 201 -23 -2 207 -23 minecraft:calcite
fill -7 208 -23 -2 208 -23 minecraft:podzol
fill -6 201 -22 -2 207 -22 minecraft:calcite
fill -6 208 -22 -2 208 -22 minecraft:podzol
fill -11 201 -37 -10 207 -37 minecraft:diorite
fill -11 208 -37 -10 208 -37 minecraft:podzol
fill -7 201 -22 -7 207 -22 minecraft:diorite
fill -7 208 -22 -7 208 -22 minecraft:podzol
fill -5 199 -32 -2 199 -29 minecraft:clay
fill -5 200 -32 -2 200 -29 minecraft:water
fill -5 199 -28 -4 199 -27 minecraft:clay
fill -5 200 -28 -4 200 -27 minecraft:water
fill -3 200 -28 -2 200 -28 minecraft:sand
fill -3 200 -27 -3 200 -26 minecraft:sand
fill -5 200 -26 -5 200 -26 minecraft:sand
setblock -5 200 -31 minecraft:seagrass
setblock -4 200 -30 minecraft:seagrass
setblock -4 200 -28 minecraft:seagrass
setblock -3 200 -30 minecraft:seagrass
setblock -2 200 -32 minecraft:seagrass
execute positioned -15 201 -37 run function rlk:room/prop/fo_tree_b
execute positioned -11 201 -25 run function rlk:room/prop/fo_lamp
execute positioned -12 201 -22 run function rlk:room/prop/fo_lamp2
execute positioned -19 201 -24 run function rlk:room/prop/fo_flower
execute positioned -17 201 -39 run function rlk:room/prop/fo_flower
execute positioned -5 201 -25 run function rlk:room/prop/fo_flower
execute positioned -14 201 -23 run function rlk:room/prop/fo_flower
execute positioned -8 201 -22 run function rlk:room/prop/fo_flower
execute positioned -15 201 -25 run function rlk:room/prop/p_grass
execute positioned -17 202 -30 run function rlk:room/prop/fo_flower
setblock -11 209 -37 minecraft:short_grass keep
setblock -10 209 -36 minecraft:birch_leaves[persistent=true] keep
setblock -7 209 -23 minecraft:birch_leaves[persistent=true] keep
setblock -6 209 -22 minecraft:birch_leaves[persistent=true] keep
setblock -5 209 -22 minecraft:birch_leaves[persistent=true] keep
setblock -4 209 -23 minecraft:birch_leaves[persistent=true] keep
setblock -4 209 -22 minecraft:short_grass keep
setblock -3 209 -23 minecraft:short_grass keep
setblock -3 209 -22 minecraft:birch_leaves[persistent=true] keep
setblock -2 209 -23 minecraft:birch_leaves[persistent=true] keep
