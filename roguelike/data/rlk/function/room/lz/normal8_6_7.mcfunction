# 구역 건설 (normal8_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 210 39 minecraft:stone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -28 200 29 -25 200 32 minecraft:calcite
fill -29 200 30 -28 200 32 minecraft:calcite
fill -26 200 28 -22 200 29 minecraft:calcite
fill -37 200 27 -34 200 29 minecraft:moss_block
fill -40 207 28 -40 210 28 minecraft:calcite
fill -40 201 31 -40 202 31 minecraft:moss_block
fill -40 209 29 -40 210 31 minecraft:birch_leaves[persistent=true]
fill -40 209 38 -40 210 39 minecraft:calcite
fill -21 210 32 -21 210 35 minecraft:oak_leaves[persistent=true]
fill -21 209 20 -21 210 21 minecraft:oak_leaves[persistent=true]
fill -21 209 26 -21 210 26 minecraft:birch_leaves[persistent=true]
fill -25 205 20 -25 205 20 minecraft:diorite
fill -37 205 20 -32 207 20 minecraft:calcite
fill -33 209 20 -29 210 20 minecraft:calcite
fill -36 210 39 -34 210 39 minecraft:birch_leaves[persistent=true]
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -39 201 21 -36 201 21 minecraft:podzol
fill -30 201 21 -29 201 21 minecraft:podzol
fill -39 201 22 -37 201 22 minecraft:podzol
fill -29 201 22 -28 201 25 minecraft:podzol
fill -39 201 23 -38 201 30 minecraft:podzol
fill -37 201 25 -37 201 26 minecraft:podzol
fill -34 201 25 -30 201 25 minecraft:podzol
fill -36 201 26 -35 201 26 minecraft:podzol
fill -35 201 21 -31 201 24 minecraft:dirt
fill -35 202 21 -31 202 24 minecraft:podzol
fill -36 201 22 -36 201 22 minecraft:dirt
fill -36 202 22 -36 202 22 minecraft:podzol
fill -30 201 22 -30 201 24 minecraft:dirt
fill -30 202 22 -30 202 24 minecraft:podzol
fill -36 201 25 -35 201 25 minecraft:dirt
fill -36 202 25 -35 202 25 minecraft:podzol
fill -36 201 38 -31 205 38 minecraft:calcite
fill -36 206 38 -31 206 38 minecraft:podzol
fill -37 201 23 -37 207 24 minecraft:calcite
fill -37 208 23 -37 208 24 minecraft:podzol
fill -36 201 24 -36 207 24 minecraft:calcite
fill -36 208 24 -36 208 24 minecraft:podzol
fill -36 201 23 -36 207 23 minecraft:diorite
fill -36 208 23 -36 208 23 minecraft:podzol
fill -39 199 31 -38 199 34 minecraft:clay
fill -39 200 31 -38 200 34 minecraft:water
fill -37 199 34 -36 199 34 minecraft:clay
fill -37 200 34 -36 200 34 minecraft:water
fill -35 200 34 -35 200 35 minecraft:sand
fill -39 200 35 -36 200 35 minecraft:sand
setblock -39 200 33 minecraft:seagrass
setblock -38 200 31 minecraft:seagrass
execute positioned -30 203 23 run function rlk:room/prop/fo_lamp
execute positioned -24 201 25 run function rlk:room/prop/fo_white
execute positioned -26 201 28 run function rlk:room/prop/p_grass
execute positioned -32 201 32 run function rlk:room/prop/p_grass
execute positioned -27 201 32 run function rlk:room/prop/fo_flower
execute positioned -37 201 28 run function rlk:room/prop/fo_flower
execute positioned -26 201 37 run function rlk:room/prop/p_grass
execute positioned -27 201 24 run function rlk:room/prop/fo_white
setblock -37 209 23 minecraft:birch_leaves[persistent=true] keep
setblock -36 209 24 minecraft:short_grass keep
setblock -36 207 38 minecraft:short_grass keep
setblock -34 207 38 minecraft:birch_leaves[persistent=true] keep
setblock -33 207 38 minecraft:birch_leaves[persistent=true] keep
setblock -32 207 38 minecraft:birch_leaves[persistent=true] keep
