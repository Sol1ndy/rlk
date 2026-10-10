# 구역 건설 (normal8_6, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 215 39 minecraft:stone
fill -39 201 21 -22 215 38 minecraft:air
fill -39 214 21 -22 214 38 minecraft:light[level=15]
fill -28 205 29 -25 205 32 minecraft:calcite
fill -29 205 30 -28 205 32 minecraft:calcite
fill -26 205 28 -22 205 29 minecraft:calcite
fill -37 205 27 -34 205 29 minecraft:moss_block
fill -40 212 28 -40 215 28 minecraft:calcite
fill -40 204 31 -40 207 31 minecraft:moss_block
fill -40 214 29 -40 215 31 minecraft:birch_leaves[persistent=true]
fill -40 202 30 -40 203 33 minecraft:moss_block
fill -40 214 38 -40 215 39 minecraft:calcite
fill -21 215 32 -21 215 35 minecraft:oak_leaves[persistent=true]
fill -21 214 20 -21 215 21 minecraft:oak_leaves[persistent=true]
fill -21 214 26 -21 215 26 minecraft:birch_leaves[persistent=true]
fill -21 203 33 -21 204 36 minecraft:moss_block
fill -25 210 20 -25 210 20 minecraft:diorite
fill -37 210 20 -32 212 20 minecraft:calcite
fill -25 205 20 -21 205 20 minecraft:moss_block
fill -33 214 20 -29 215 20 minecraft:calcite
fill -29 201 39 -27 201 39 minecraft:calcite
fill -28 202 39 -26 205 39 minecraft:calcite
fill -36 215 39 -34 215 39 minecraft:birch_leaves[persistent=true]
fill -40 215 20 -21 215 39 minecraft:polished_deepslate
fill -39 215 21 -22 215 38 minecraft:air
fill -28 201 21 -22 204 21 minecraft:dirt
fill -28 205 21 -22 205 21 minecraft:podzol
fill -27 201 22 -22 204 38 minecraft:dirt
fill -27 205 22 -22 205 38 minecraft:podzol
fill -34 201 26 -28 204 37 minecraft:dirt
fill -34 205 26 -28 205 37 minecraft:podzol
fill -37 201 27 -35 204 37 minecraft:dirt
fill -37 205 27 -35 205 37 minecraft:podzol
fill -39 201 31 -38 204 38 minecraft:dirt
fill -39 205 31 -38 205 38 minecraft:podzol
fill -37 201 38 -37 204 38 minecraft:dirt
fill -37 205 38 -37 205 38 minecraft:podzol
fill -30 201 38 -28 204 38 minecraft:dirt
fill -30 205 38 -28 205 38 minecraft:podzol
fill -39 201 21 -36 205 21 minecraft:dirt
fill -39 206 21 -36 206 21 minecraft:podzol
fill -30 201 21 -29 205 21 minecraft:dirt
fill -30 206 21 -29 206 21 minecraft:podzol
fill -39 201 22 -37 205 22 minecraft:dirt
fill -39 206 22 -37 206 22 minecraft:podzol
fill -29 201 22 -28 205 25 minecraft:dirt
fill -29 206 22 -28 206 25 minecraft:podzol
fill -39 201 23 -38 205 30 minecraft:dirt
fill -39 206 23 -38 206 30 minecraft:podzol
fill -37 201 25 -37 205 26 minecraft:dirt
fill -37 206 25 -37 206 26 minecraft:podzol
fill -34 201 25 -30 205 25 minecraft:dirt
fill -34 206 25 -30 206 25 minecraft:podzol
fill -36 201 26 -35 205 26 minecraft:dirt
fill -36 206 26 -35 206 26 minecraft:podzol
fill -35 201 21 -31 206 24 minecraft:dirt
fill -35 207 21 -31 207 24 minecraft:podzol
fill -36 201 22 -36 206 22 minecraft:dirt
fill -36 207 22 -36 207 22 minecraft:podzol
fill -30 201 22 -30 206 24 minecraft:dirt
fill -30 207 22 -30 207 24 minecraft:podzol
fill -36 201 25 -35 206 25 minecraft:dirt
fill -36 207 25 -35 207 25 minecraft:podzol
fill -36 201 38 -31 210 38 minecraft:calcite
fill -36 211 38 -31 211 38 minecraft:podzol
fill -37 201 23 -37 212 24 minecraft:calcite
fill -37 213 23 -37 213 24 minecraft:podzol
fill -36 201 24 -36 212 24 minecraft:calcite
fill -36 213 24 -36 213 24 minecraft:podzol
fill -36 201 23 -36 212 23 minecraft:diorite
fill -36 213 23 -36 213 23 minecraft:podzol
fill -39 204 31 -38 204 34 minecraft:clay
fill -39 205 31 -38 205 34 minecraft:water
fill -37 204 34 -36 204 34 minecraft:clay
fill -37 205 34 -36 205 34 minecraft:water
fill -35 205 34 -35 205 35 minecraft:sand
fill -39 205 35 -36 205 35 minecraft:sand
setblock -39 205 33 minecraft:seagrass
setblock -38 205 31 minecraft:seagrass
execute positioned -30 208 23 run function rlk:room/prop/fo_lamp
execute positioned -24 206 25 run function rlk:room/prop/fo_white
execute positioned -26 206 28 run function rlk:room/prop/p_grass
execute positioned -32 206 32 run function rlk:room/prop/p_grass
execute positioned -27 206 32 run function rlk:room/prop/fo_flower
execute positioned -37 206 28 run function rlk:room/prop/fo_flower
execute positioned -26 206 37 run function rlk:room/prop/p_grass
execute positioned -27 206 24 run function rlk:room/prop/fo_white
setblock -37 214 23 minecraft:birch_leaves[persistent=true] keep
setblock -36 214 24 minecraft:short_grass keep
setblock -36 212 38 minecraft:short_grass keep
setblock -34 212 38 minecraft:birch_leaves[persistent=true] keep
setblock -33 212 38 minecraft:birch_leaves[persistent=true] keep
setblock -32 212 38 minecraft:birch_leaves[persistent=true] keep
