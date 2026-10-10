# 구역 건설 (root5_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 20 -1 200 39 minecraft:podzol
fill -20 201 20 -1 210 39 minecraft:stone
fill -19 201 21 -2 210 38 minecraft:air
fill -19 209 21 -2 209 38 minecraft:light[level=15]
fill -10 200 26 -9 200 29 minecraft:coarse_dirt
fill -9 200 28 -7 200 31 minecraft:moss_block
fill -20 210 31 -20 210 36 minecraft:oak_leaves[persistent=true]
fill -20 210 20 -20 210 25 minecraft:moss_block
fill -20 210 34 -20 210 36 minecraft:moss_block
fill -20 205 33 -20 205 34 minecraft:granite
fill -20 206 33 -20 207 37 minecraft:cobblestone
fill -1 207 34 -1 208 39 minecraft:mossy_cobblestone
fill -1 207 22 -1 210 24 minecraft:cobblestone
fill -1 202 24 -1 204 26 minecraft:granite
fill -1 204 24 -1 207 27 minecraft:tuff
fill -1 204 34 -1 205 35 minecraft:granite
fill -20 209 20 -20 210 20 minecraft:oak_leaves[persistent=true]
fill -20 209 20 -15 210 20 minecraft:oak_leaves[persistent=true]
fill -15 206 20 -14 209 20 minecraft:andesite
fill -8 207 20 -7 208 20 minecraft:andesite
fill -14 209 39 -11 210 39 minecraft:oak_leaves[persistent=true]
fill -15 204 39 -11 204 39 minecraft:mossy_cobblestone
fill -3 202 39 -2 205 39 minecraft:moss_block
fill -20 210 20 -1 210 39 minecraft:polished_deepslate
fill -19 210 21 -2 210 38 minecraft:air
fill -4 201 21 -3 201 22 minecraft:podzol
fill -2 201 22 -2 201 22 minecraft:podzol
fill -4 201 23 -4 201 26 minecraft:podzol
fill -5 201 26 -5 201 26 minecraft:podzol
fill -3 201 26 -3 201 26 minecraft:podzol
fill -2 201 27 -2 201 30 minecraft:podzol
fill -3 201 23 -2 201 25 minecraft:dirt
fill -3 202 23 -2 202 25 minecraft:podzol
fill -2 201 26 -2 201 26 minecraft:dirt
fill -2 202 26 -2 202 26 minecraft:podzol
fill -12 201 38 -12 206 38 minecraft:andesite
fill -12 207 38 -12 207 38 minecraft:podzol
fill -15 201 37 -12 206 37 minecraft:stone
fill -15 207 37 -12 207 37 minecraft:podzol
fill -15 201 38 -13 206 38 minecraft:stone
fill -15 207 38 -13 207 38 minecraft:podzol
execute positioned -19 201 26 run function rlk:room/prop/p_fence_x
execute positioned -13 201 21 run function rlk:room/prop/p_litter
execute positioned -19 201 23 run function rlk:room/prop/p_grass
execute positioned -7 201 35 run function rlk:room/prop/p_dandelion
execute positioned -18 201 30 run function rlk:room/prop/p_grass
execute positioned -5 201 35 run function rlk:room/prop/p_grass
execute positioned -4 201 27 run function rlk:room/prop/p_wildflower
execute positioned -14 201 24 run function rlk:room/prop/p_wildflower
execute positioned -4 202 25 run function rlk:room/prop/p_wildflower
setblock -15 208 38 minecraft:azalea_leaves[persistent=true] keep
setblock -14 208 37 minecraft:short_grass keep
setblock -13 208 38 minecraft:azalea_leaves[persistent=true] keep
setblock -12 208 37 minecraft:azalea_leaves[persistent=true] keep
setblock -12 208 38 minecraft:short_grass keep
