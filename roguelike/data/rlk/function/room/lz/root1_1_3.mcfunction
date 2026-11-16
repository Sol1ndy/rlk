# 구역 건설 (root1_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -1 210 18 minecraft:air
fill -19 209 1 -1 209 18 minecraft:light[level=15]
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 0 201 1 18 210 18 minecraft:air
fill 0 209 1 18 209 18 minecraft:light[level=15]
fill 1 200 13 4 200 14 minecraft:moss_block
fill 13 200 2 17 200 3 minecraft:coarse_dirt
fill -20 209 15 -20 210 17 minecraft:andesite
fill -20 204 13 -20 207 16 minecraft:mossy_cobblestone
fill -20 204 6 -20 205 9 minecraft:tuff
fill -20 207 10 -20 207 14 minecraft:tuff
fill -4 210 0 -1 210 0 minecraft:moss_block
fill -12 205 0 -11 208 0 minecraft:andesite
fill -18 210 0 -16 210 0 minecraft:tuff
fill -11 208 0 -7 210 0 minecraft:moss_block
fill -20 205 19 -20 207 19 minecraft:mossy_cobblestone
fill -4 202 19 -2 204 19 minecraft:moss_block
fill -7 210 19 -7 210 19 minecraft:oak_leaves[persistent=true]
fill -9 207 19 -4 207 19 minecraft:granite
fill -15 210 19 -12 210 19 minecraft:oak_leaves[persistent=true]
fill 19 207 17 19 210 18 minecraft:moss_block
fill 19 209 10 19 210 10 minecraft:oak_leaves[persistent=true]
fill 19 201 9 19 203 9 minecraft:andesite
fill 19 207 9 19 209 10 minecraft:moss_block
fill 6 204 0 11 204 0 minecraft:mossy_cobblestone
fill 7 209 0 8 209 0 minecraft:mossy_cobblestone
fill 4 205 0 9 206 0 minecraft:andesite
fill 4 203 0 9 205 0 minecraft:moss_block
fill 13 206 0 15 208 0 minecraft:granite
fill 11 205 0 13 205 0 minecraft:mossy_cobblestone
fill 0 204 19 2 207 19 minecraft:tuff
fill 13 206 19 17 208 19 minecraft:tuff
fill 10 208 19 14 208 19 minecraft:mossy_cobblestone
fill 6 202 19 10 205 19 minecraft:cobblestone
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -1 210 18 minecraft:air
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 0 210 1 18 210 18 minecraft:air
fill -3 201 3 -2 201 3 minecraft:podzol
fill -10 201 4 -8 201 5 minecraft:podzol
fill -2 201 4 -1 201 5 minecraft:podzol
fill -7 201 5 -7 201 5 minecraft:podzol
fill -4 201 5 -3 201 5 minecraft:podzol
fill 0 201 5 0 201 5 minecraft:podzol
fill -6 201 6 -5 201 13 minecraft:podzol
fill 16 201 13 18 201 18 minecraft:podzol
fill -9 201 14 -7 201 14 minecraft:podzol
fill -5 201 14 -5 201 15 minecraft:podzol
fill 15 201 14 15 201 18 minecraft:podzol
fill -8 201 15 -6 201 15 minecraft:podzol
fill -4 201 15 -2 201 15 minecraft:podzol
fill 14 201 15 14 201 17 minecraft:podzol
fill -7 201 4 -3 201 4 minecraft:dirt
fill -7 202 4 -3 202 4 minecraft:podzol
fill -6 201 5 -5 201 5 minecraft:dirt
fill -6 202 5 -5 202 5 minecraft:podzol
fill -6 201 14 -6 201 14 minecraft:dirt
fill -6 202 14 -6 202 14 minecraft:podzol
fill 9 201 3 10 206 4 minecraft:stone
fill 9 207 3 10 207 4 minecraft:podzol
fill -9 201 1 -4 207 1 minecraft:andesite
fill -9 208 1 -4 208 1 minecraft:podzol
fill -9 201 2 -4 207 3 minecraft:stone
fill -9 208 2 -4 208 3 minecraft:podzol
fill 4 201 3 5 207 4 minecraft:stone
fill 4 208 3 5 208 4 minecraft:podzol
execute positioned -6 201 18 run function rlk:room/prop/p_pillar_ruin
execute positioned 0 201 15 run function rlk:room/prop/p_ruin_x
execute positioned 14 201 12 run function rlk:room/prop/p_lantern
execute positioned -13 201 5 run function rlk:room/prop/p_boulder_s
execute positioned 10 201 15 run function rlk:room/prop/p_birch
execute positioned -15 201 10 run function rlk:room/prop/p_litter
execute positioned 6 201 3 run function rlk:room/prop/p_dandelion
execute positioned -2 201 2 run function rlk:room/prop/p_litter
execute positioned 7 201 18 run function rlk:room/prop/p_litter
execute positioned -11 201 7 run function rlk:room/prop/p_wildflower
execute positioned -3 201 14 run function rlk:room/prop/p_wildflower
execute positioned -16 201 10 run function rlk:room/prop/p_grass
execute positioned 4 201 10 run function rlk:room/prop/p_litter
execute positioned 17 201 12 run function rlk:room/prop/p_grass
execute positioned 17 202 17 run function rlk:room/prop/p_litter
execute positioned 1 201 13 run function rlk:room/prop/p_litter
execute positioned -10 201 10 run function rlk:room/prop/p_grass
execute positioned -5 201 17 run function rlk:room/prop/p_dandelion
execute positioned 0 201 9 run function rlk:room/prop/p_litter
execute positioned 15 201 3 run function rlk:room/prop/p_grass
execute positioned 0 201 2 run function rlk:room/prop/p_grass
execute positioned -14 201 6 run function rlk:room/prop/p_dandelion
execute positioned -2 201 8 run function rlk:room/prop/p_wildflower
setblock -9 209 1 minecraft:short_grass keep
setblock -9 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock -8 209 1 minecraft:azalea_leaves[persistent=true] keep
setblock -8 209 2 minecraft:short_grass keep
setblock -8 209 3 minecraft:short_grass keep
setblock -7 209 2 minecraft:azalea_leaves[persistent=true] keep
setblock -7 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock -6 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock -5 209 1 minecraft:azalea_leaves[persistent=true] keep
setblock -5 209 2 minecraft:azalea_leaves[persistent=true] keep
setblock -5 209 3 minecraft:short_grass keep
setblock -4 209 1 minecraft:azalea_leaves[persistent=true] keep
setblock -4 209 2 minecraft:short_grass keep
setblock 4 209 3 minecraft:azalea_leaves[persistent=true] keep
setblock 4 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock 5 209 4 minecraft:short_grass keep
setblock 9 208 3 minecraft:azalea_leaves[persistent=true] keep
setblock 9 208 4 minecraft:short_grass keep
setblock 10 208 3 minecraft:short_grass keep
setblock 10 208 4 minecraft:azalea_leaves[persistent=true] keep
