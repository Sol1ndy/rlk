# 구역 건설 (first10_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 20 59 200 39 minecraft:podzol
fill 40 201 20 59 210 39 minecraft:stone
fill 41 201 21 58 210 39 minecraft:air
fill 41 209 21 58 209 39 minecraft:light[level=15]
fill 40 200 40 59 200 59 minecraft:podzol
fill 40 201 40 59 210 59 minecraft:stone
fill 41 201 40 58 210 58 minecraft:air
fill 41 209 40 58 209 58 minecraft:light[level=15]
fill 56 200 53 57 200 55 minecraft:moss_block
fill 52 200 41 53 200 43 minecraft:gravel
fill 46 200 38 48 200 41 minecraft:coarse_dirt
fill 40 204 20 40 204 20 minecraft:cobblestone
fill 40 203 31 40 203 35 minecraft:andesite
fill 40 201 25 40 203 26 minecraft:granite
fill 59 206 31 59 208 34 minecraft:andesite
fill 59 210 21 59 210 22 minecraft:tuff
fill 44 209 20 49 210 20 minecraft:oak_leaves[persistent=true]
fill 52 201 20 57 202 20 minecraft:tuff
fill 50 209 20 52 210 20 minecraft:oak_leaves[persistent=true]
fill 40 206 20 41 206 20 minecraft:moss_block
fill 40 203 42 40 206 44 minecraft:moss_block
fill 40 202 41 40 202 41 minecraft:moss_block
fill 40 201 40 40 203 42 minecraft:andesite
fill 40 202 50 40 204 54 minecraft:tuff
fill 59 209 49 59 210 53 minecraft:oak_leaves[persistent=true]
fill 59 210 49 59 210 49 minecraft:mossy_cobblestone
fill 59 210 46 59 210 51 minecraft:oak_leaves[persistent=true]
fill 48 210 59 52 210 59 minecraft:oak_leaves[persistent=true]
fill 53 207 59 54 210 59 minecraft:cobblestone
fill 52 206 59 52 207 59 minecraft:mossy_cobblestone
fill 42 204 59 46 207 59 minecraft:andesite
fill 40 210 20 59 210 39 minecraft:polished_deepslate
fill 41 210 21 58 210 39 minecraft:air
fill 40 210 40 59 210 59 minecraft:polished_deepslate
fill 41 210 40 58 210 58 minecraft:air
fill 55 201 31 58 201 36 minecraft:podzol
fill 54 201 32 54 201 35 minecraft:podzol
fill 53 201 33 53 201 35 minecraft:podzol
fill 58 201 37 58 201 39 minecraft:podzol
fill 46 201 48 48 201 51 minecraft:podzol
fill 49 201 49 49 201 51 minecraft:podzol
fill 50 201 51 51 201 52 minecraft:podzol
fill 46 201 52 46 201 57 minecraft:podzol
fill 51 201 53 51 201 57 minecraft:podzol
fill 45 201 56 45 201 57 minecraft:podzol
fill 50 201 56 50 201 57 minecraft:podzol
fill 47 201 57 49 201 58 minecraft:podzol
fill 47 201 52 49 201 56 minecraft:dirt
fill 47 202 52 49 202 56 minecraft:podzol
fill 50 201 53 50 201 55 minecraft:dirt
fill 50 202 53 50 202 55 minecraft:podzol
fill 52 201 48 54 205 48 minecraft:andesite
fill 52 206 48 54 206 48 minecraft:podzol
fill 52 201 49 53 205 49 minecraft:andesite
fill 52 206 49 53 206 49 minecraft:podzol
fill 51 201 30 51 205 32 minecraft:stone
fill 51 206 30 51 206 32 minecraft:podzol
fill 50 201 31 50 205 31 minecraft:stone
fill 50 206 31 50 206 31 minecraft:podzol
fill 52 201 31 52 205 31 minecraft:stone
fill 52 206 31 52 206 31 minecraft:podzol
fill 53 201 47 54 205 47 minecraft:stone
fill 53 206 47 54 206 47 minecraft:podzol
fill 42 201 24 42 206 27 minecraft:andesite
fill 42 207 24 42 207 27 minecraft:podzol
fill 41 201 26 41 206 27 minecraft:andesite
fill 41 207 26 41 207 27 minecraft:podzol
fill 41 201 24 41 206 25 minecraft:stone
fill 41 207 24 41 207 25 minecraft:podzol
execute positioned 51 201 24 run function rlk:room/prop/p_lantern
execute positioned 45 201 32 run function rlk:room/prop/p_oak
execute positioned 49 202 49 run function rlk:room/prop/p_pillar_ruin
execute positioned 44 201 35 run function rlk:room/prop/p_shrub_tree
execute positioned 55 201 52 run function rlk:room/prop/p_fence_x
execute positioned 41 201 44 run function rlk:room/prop/p_litter
execute positioned 55 202 34 run function rlk:room/prop/p_dandelion
execute positioned 48 201 30 run function rlk:room/prop/p_dandelion
execute positioned 43 201 44 run function rlk:room/prop/p_grass
execute positioned 51 201 44 run function rlk:room/prop/p_wildflower
execute positioned 42 201 28 run function rlk:room/prop/p_grass
execute positioned 49 203 56 run function rlk:room/prop/p_wildflower
execute positioned 49 201 44 run function rlk:room/prop/p_litter
execute positioned 49 201 38 run function rlk:room/prop/p_grass
execute positioned 48 201 25 run function rlk:room/prop/p_grass
execute positioned 55 201 39 run function rlk:room/prop/p_grass
execute positioned 44 201 24 run function rlk:room/prop/p_wildflower
execute positioned 53 201 31 run function rlk:room/prop/p_grass
execute positioned 44 201 31 run function rlk:room/prop/p_grass
execute positioned 44 201 27 run function rlk:room/prop/p_grass
execute positioned 43 201 49 run function rlk:room/prop/p_grass
setblock 41 208 27 minecraft:azalea_leaves[persistent=true] keep
setblock 42 208 24 minecraft:short_grass keep
setblock 42 208 26 minecraft:short_grass keep
setblock 42 208 27 minecraft:short_grass keep
setblock 51 207 30 minecraft:azalea_leaves[persistent=true] keep
setblock 51 207 31 minecraft:azalea_leaves[persistent=true] keep
setblock 52 207 31 minecraft:azalea_leaves[persistent=true] keep
setblock 52 207 49 minecraft:azalea_leaves[persistent=true] keep
setblock 54 207 47 minecraft:short_grass keep
setblock 54 207 48 minecraft:azalea_leaves[persistent=true] keep
