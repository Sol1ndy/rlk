# 구역 건설 (levelup7_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:podzol
fill 20 201 20 39 210 39 minecraft:stone
fill 21 201 21 38 210 38 minecraft:air
fill 21 209 21 38 209 38 minecraft:light[level=15]
fill 24 200 24 26 200 25 minecraft:coarse_dirt
fill 20 209 24 20 210 26 minecraft:oak_leaves[persistent=true]
fill 20 206 20 20 209 25 minecraft:granite
fill 20 210 24 20 210 26 minecraft:oak_leaves[persistent=true]
fill 20 204 30 20 206 31 minecraft:mossy_cobblestone
fill 39 210 23 39 210 28 minecraft:andesite
fill 39 201 31 39 201 35 minecraft:cobblestone
fill 39 202 29 39 205 31 minecraft:moss_block
fill 38 209 20 38 210 20 minecraft:moss_block
fill 22 208 20 23 209 20 minecraft:moss_block
fill 35 201 39 39 201 39 minecraft:tuff
fill 25 202 39 27 204 39 minecraft:cobblestone
fill 35 206 39 39 208 39 minecraft:mossy_cobblestone
fill 20 210 20 39 210 39 minecraft:polished_deepslate
fill 21 210 21 38 210 38 minecraft:air
fill 34 201 21 34 201 22 minecraft:podzol
fill 35 201 22 35 201 24 minecraft:podzol
fill 36 201 24 37 201 25 minecraft:podzol
fill 38 201 25 38 201 25 minecraft:podzol
fill 35 201 21 38 201 21 minecraft:dirt
fill 35 202 21 38 202 21 minecraft:podzol
fill 36 201 22 38 201 23 minecraft:dirt
fill 36 202 22 38 202 23 minecraft:podzol
fill 38 201 24 38 201 24 minecraft:dirt
fill 38 202 24 38 202 24 minecraft:podzol
fill 28 201 21 30 206 23 minecraft:stone
fill 28 207 21 30 207 23 minecraft:podzol
fill 33 201 23 34 207 24 minecraft:stone
fill 33 208 23 34 208 24 minecraft:podzol
execute positioned 37 201 34 run function rlk:room/prop/p_boulder
execute positioned 23 201 36 run function rlk:room/prop/p_grass
execute positioned 26 201 34 run function rlk:room/prop/p_litter
execute positioned 22 201 24 run function rlk:room/prop/p_dandelion
execute positioned 35 201 35 run function rlk:room/prop/p_grass
execute positioned 25 201 25 run function rlk:room/prop/p_grass
execute positioned 35 201 37 run function rlk:room/prop/p_grass
setblock 28 208 21 minecraft:azalea_leaves[persistent=true] keep
setblock 28 208 22 minecraft:short_grass keep
setblock 29 208 22 minecraft:short_grass keep
setblock 30 208 21 minecraft:azalea_leaves[persistent=true] keep
setblock 30 208 22 minecraft:azalea_leaves[persistent=true] keep
setblock 30 208 23 minecraft:azalea_leaves[persistent=true] keep
setblock 33 209 24 minecraft:short_grass keep
setblock 34 209 23 minecraft:azalea_leaves[persistent=true] keep
