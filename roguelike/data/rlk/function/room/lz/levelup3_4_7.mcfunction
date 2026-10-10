# 구역 건설 (levelup3_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 210 39 minecraft:stone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -34 200 27 -30 200 28 minecraft:gravel
fill -36 200 21 -32 200 23 minecraft:coarse_dirt
fill -40 210 32 -40 210 35 minecraft:diorite
fill -40 207 23 -40 207 26 minecraft:calcite
fill -40 210 22 -40 210 22 minecraft:oak_leaves[persistent=true]
fill -40 209 20 -40 210 25 minecraft:oak_leaves[persistent=true]
fill -40 209 34 -40 209 37 minecraft:prismarine
fill -40 209 24 -40 210 24 minecraft:birch_leaves[persistent=true]
fill -21 202 36 -21 205 36 minecraft:calcite
fill -21 209 22 -21 209 24 minecraft:calcite
fill -21 209 32 -21 210 32 minecraft:birch_leaves[persistent=true]
fill -21 201 28 -21 202 30 minecraft:prismarine
fill -21 205 32 -21 207 35 minecraft:calcite
fill -21 210 32 -21 210 36 minecraft:oak_leaves[persistent=true]
fill -40 210 20 -36 210 20 minecraft:birch_leaves[persistent=true]
fill -29 210 20 -24 210 20 minecraft:moss_block
fill -28 204 20 -27 206 20 minecraft:moss_block
fill -31 201 39 -26 201 39 minecraft:diorite
fill -28 202 39 -24 204 39 minecraft:calcite
fill -34 204 39 -32 206 39 minecraft:calcite
fill -34 207 39 -32 210 39 minecraft:diorite
fill -40 210 39 -38 210 39 minecraft:birch_leaves[persistent=true]
fill -26 205 39 -23 208 39 minecraft:dark_prismarine
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -39 201 25 -37 201 25 minecraft:podzol
fill -37 201 26 -37 201 34 minecraft:podzol
fill -25 201 30 -24 201 31 minecraft:podzol
fill -23 201 31 -22 201 32 minecraft:podzol
fill -25 201 32 -25 201 34 minecraft:podzol
fill -22 201 33 -22 201 33 minecraft:podzol
fill -39 201 34 -38 201 35 minecraft:podzol
fill -31 201 35 -26 201 35 minecraft:podzol
fill -31 201 36 -30 201 36 minecraft:podzol
fill -39 201 26 -38 201 33 minecraft:dirt
fill -39 202 26 -38 202 33 minecraft:podzol
fill -24 201 32 -24 201 38 minecraft:dirt
fill -24 202 32 -24 202 38 minecraft:podzol
fill -23 201 33 -23 201 38 minecraft:dirt
fill -23 202 33 -23 202 38 minecraft:podzol
fill -22 201 34 -22 201 38 minecraft:dirt
fill -22 202 34 -22 202 38 minecraft:podzol
fill -25 201 35 -25 201 38 minecraft:dirt
fill -25 202 35 -25 202 38 minecraft:podzol
fill -29 201 36 -26 201 36 minecraft:dirt
fill -29 202 36 -26 202 36 minecraft:podzol
fill -26 201 37 -26 201 38 minecraft:dirt
fill -26 202 37 -26 202 38 minecraft:podzol
fill -31 201 37 -27 207 38 minecraft:calcite
fill -31 208 37 -27 208 38 minecraft:podzol
execute positioned -35 201 30 run function rlk:room/prop/fo_lamp2
execute positioned -24 203 38 run function rlk:room/prop/fo_col_a
execute positioned -22 202 33 run function rlk:room/prop/fo_col_b
execute positioned -23 201 30 run function rlk:room/prop/fo_crates
execute positioned -39 201 36 run function rlk:room/prop/fo_rock_s
execute positioned -31 201 32 run function rlk:room/prop/fo_flower
execute positioned -26 201 29 run function rlk:room/prop/fo_white
execute positioned -38 201 24 run function rlk:room/prop/fo_white
execute positioned -31 201 32 run function rlk:room/prop/p_grass
execute positioned -29 201 24 run function rlk:room/prop/fo_white
execute positioned -39 202 34 run function rlk:room/prop/p_grass
execute positioned -27 201 34 run function rlk:room/prop/fo_flower
execute positioned -27 201 27 run function rlk:room/prop/fo_white
execute positioned -22 202 33 run function rlk:room/prop/p_grass
execute positioned -35 201 37 run function rlk:room/prop/p_grass
setblock -31 209 38 minecraft:short_grass keep
setblock -30 209 37 minecraft:short_grass keep
setblock -30 209 38 minecraft:birch_leaves[persistent=true] keep
setblock -29 209 37 minecraft:short_grass keep
setblock -28 209 37 minecraft:birch_leaves[persistent=true] keep
setblock -27 209 37 minecraft:short_grass keep
setblock -27 209 38 minecraft:birch_leaves[persistent=true] keep
