# 구역 건설 (levelup5_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 40 -21 200 59 minecraft:podzol
fill -40 201 40 -21 210 59 minecraft:stone
fill -39 201 41 -22 210 58 minecraft:air
fill -39 209 41 -22 209 58 minecraft:light[level=15]
fill -38 200 50 -34 200 52 minecraft:coarse_dirt
fill -38 200 53 -37 200 54 minecraft:calcite
fill -29 200 48 -27 200 49 minecraft:gravel
fill -40 207 43 -40 210 45 minecraft:calcite
fill -40 208 52 -40 209 57 minecraft:diorite
fill -40 209 50 -40 210 52 minecraft:oak_leaves[persistent=true]
fill -40 210 50 -40 210 55 minecraft:oak_leaves[persistent=true]
fill -21 209 49 -21 210 52 minecraft:oak_leaves[persistent=true]
fill -21 203 42 -21 204 47 minecraft:diorite
fill -21 203 43 -21 204 44 minecraft:calcite
fill -21 203 46 -21 203 47 minecraft:diorite
fill -29 205 40 -27 206 40 minecraft:prismarine
fill -37 210 40 -36 210 40 minecraft:oak_leaves[persistent=true]
fill -28 209 40 -25 210 40 minecraft:oak_leaves[persistent=true]
fill -33 209 40 -33 210 40 minecraft:birch_leaves[persistent=true]
fill -40 201 59 -36 202 59 minecraft:diorite
fill -39 203 59 -38 204 59 minecraft:moss_block
fill -34 203 59 -33 206 59 minecraft:diorite
fill -26 201 59 -23 204 59 minecraft:diorite
fill -40 210 40 -21 210 59 minecraft:polished_deepslate
fill -39 210 41 -22 210 58 minecraft:air
fill -39 201 41 -37 201 41 minecraft:podzol
fill -37 201 42 -37 201 45 minecraft:podzol
fill -36 201 46 -35 201 46 minecraft:podzol
fill -35 201 47 -35 201 48 minecraft:podzol
fill -36 201 48 -36 201 48 minecraft:podzol
fill -39 201 49 -37 201 49 minecraft:podzol
fill -39 201 42 -38 201 42 minecraft:dirt
fill -39 202 42 -38 202 42 minecraft:podzol
fill -38 201 43 -38 201 45 minecraft:dirt
fill -38 202 43 -38 202 45 minecraft:podzol
fill -37 201 46 -37 201 46 minecraft:dirt
fill -37 202 46 -37 202 46 minecraft:podzol
fill -36 201 47 -36 201 47 minecraft:dirt
fill -36 202 47 -36 202 47 minecraft:podzol
fill -39 201 48 -37 201 48 minecraft:dirt
fill -39 202 48 -37 202 48 minecraft:podzol
fill -39 201 43 -39 202 47 minecraft:dirt
fill -39 203 43 -39 203 47 minecraft:podzol
fill -38 201 46 -38 202 47 minecraft:dirt
fill -38 203 46 -38 203 47 minecraft:podzol
fill -37 201 47 -37 202 47 minecraft:dirt
fill -37 203 47 -37 203 47 minecraft:podzol
fill -34 201 57 -34 206 57 minecraft:calcite
fill -34 207 57 -34 207 57 minecraft:podzol
fill -30 201 57 -30 206 58 minecraft:calcite
fill -30 207 57 -30 207 58 minecraft:podzol
fill -33 201 58 -31 206 58 minecraft:calcite
fill -33 207 58 -31 207 58 minecraft:podzol
fill -33 201 57 -31 206 57 minecraft:diorite
fill -33 207 57 -31 207 57 minecraft:podzol
fill -34 201 58 -34 206 58 minecraft:diorite
fill -34 207 58 -34 207 58 minecraft:podzol
fill -25 186 47 -21 199 59 minecraft:stone
fill -24 186 48 -22 186 58 minecraft:clay
fill -24 187 48 -22 188 58 minecraft:water
fill -24 189 48 -22 201 58 minecraft:air
execute positioned -38 201 53 run function rlk:room/prop/fo_bench
execute positioned -37 203 48 run function rlk:room/prop/fo_lamp
execute positioned -39 201 50 run function rlk:room/prop/fo_flower
execute positioned -26 201 54 run function rlk:room/prop/fo_flower
execute positioned -38 203 45 run function rlk:room/prop/fo_flower
execute positioned -38 201 56 run function rlk:room/prop/fo_flower
execute positioned -36 201 52 run function rlk:room/prop/p_grass
execute positioned -39 203 48 run function rlk:room/prop/p_grass
execute positioned -34 201 46 run function rlk:room/prop/p_grass
execute positioned -25 201 41 run function rlk:room/prop/p_grass
setblock -34 208 57 minecraft:short_grass keep
setblock -33 208 58 minecraft:birch_leaves[persistent=true] keep
setblock -32 208 57 minecraft:short_grass keep
setblock -32 208 58 minecraft:birch_leaves[persistent=true] keep
setblock -31 208 57 minecraft:short_grass keep
setblock -31 208 58 minecraft:short_grass keep
setblock -30 208 57 minecraft:birch_leaves[persistent=true] keep
setblock -30 208 58 minecraft:short_grass keep
