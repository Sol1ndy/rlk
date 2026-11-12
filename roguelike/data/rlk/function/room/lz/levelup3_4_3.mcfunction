# 구역 건설 (levelup3_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 210 39 minecraft:stone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -31 200 21 -27 200 22 minecraft:rooted_dirt
fill -33 200 32 -31 200 34 minecraft:rooted_dirt
fill -40 209 32 -40 210 32 minecraft:moss_block
fill -40 210 34 -40 210 35 minecraft:mossy_cobblestone
fill -40 210 26 -40 210 31 minecraft:andesite
fill -40 205 24 -40 207 25 minecraft:mossy_cobblestone
fill -40 209 28 -40 210 30 minecraft:oak_leaves[persistent=true]
fill -40 209 34 -40 210 34 minecraft:oak_leaves[persistent=true]
fill -21 204 30 -21 206 33 minecraft:moss_block
fill -21 205 31 -21 205 33 minecraft:tuff
fill -21 201 32 -21 203 35 minecraft:andesite
fill -21 210 31 -21 210 34 minecraft:oak_leaves[persistent=true]
fill -21 207 21 -21 209 25 minecraft:mossy_cobblestone
fill -32 207 20 -32 207 20 minecraft:andesite
fill -33 202 20 -29 205 20 minecraft:andesite
fill -29 207 20 -25 208 20 minecraft:granite
fill -31 210 20 -27 210 20 minecraft:cobblestone
fill -25 201 20 -21 203 20 minecraft:moss_block
fill -35 206 39 -32 207 39 minecraft:andesite
fill -36 201 39 -32 203 39 minecraft:andesite
fill -27 201 39 -27 204 39 minecraft:cobblestone
fill -29 209 39 -29 210 39 minecraft:oak_leaves[persistent=true]
fill -32 204 39 -30 206 39 minecraft:cobblestone
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -25 201 30 -24 201 31 minecraft:podzol
fill -23 201 31 -22 201 32 minecraft:podzol
fill -25 201 32 -25 201 34 minecraft:podzol
fill -22 201 33 -22 201 33 minecraft:podzol
fill -31 201 35 -26 201 35 minecraft:podzol
fill -31 201 36 -30 201 36 minecraft:podzol
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
fill -31 201 37 -27 207 38 minecraft:stone
fill -31 208 37 -27 208 38 minecraft:podzol
execute positioned -23 201 24 run function rlk:room/prop/p_boulder
execute positioned -25 202 31 run function rlk:room/prop/p_ruin_z
execute positioned -34 201 35 run function rlk:room/prop/p_boulder
execute positioned -39 201 23 run function rlk:room/prop/p_hay
execute positioned -34 201 29 run function rlk:room/prop/p_litter
execute positioned -39 201 30 run function rlk:room/prop/p_grass
execute positioned -33 201 25 run function rlk:room/prop/p_grass
execute positioned -26 201 28 run function rlk:room/prop/p_wildflower
execute positioned -32 201 31 run function rlk:room/prop/p_wildflower
execute positioned -27 201 33 run function rlk:room/prop/p_wildflower
execute positioned -28 201 28 run function rlk:room/prop/p_grass
execute positioned -29 201 27 run function rlk:room/prop/p_wildflower
setblock -29 209 37 minecraft:azalea_leaves[persistent=true] keep
setblock -29 209 38 minecraft:azalea_leaves[persistent=true] keep
setblock -28 209 37 minecraft:azalea_leaves[persistent=true] keep
setblock -28 209 38 minecraft:azalea_leaves[persistent=true] keep
setblock -27 209 38 minecraft:azalea_leaves[persistent=true] keep
