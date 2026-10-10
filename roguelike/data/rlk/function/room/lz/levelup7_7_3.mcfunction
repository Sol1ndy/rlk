# 구역 건설 (levelup7_7, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 20 59 200 39 minecraft:podzol
fill 40 201 20 59 210 39 minecraft:stone
fill 41 201 21 58 210 38 minecraft:air
fill 41 209 21 58 209 38 minecraft:light[level=15]
fill 46 200 23 49 200 25 minecraft:rooted_dirt
fill 48 200 26 50 200 27 minecraft:rooted_dirt
fill 40 210 34 40 210 39 minecraft:oak_leaves[persistent=true]
fill 40 201 29 40 203 32 minecraft:mossy_cobblestone
fill 40 209 22 40 210 25 minecraft:oak_leaves[persistent=true]
fill 40 204 23 40 206 25 minecraft:mossy_cobblestone
fill 40 204 37 40 206 38 minecraft:tuff
fill 40 209 23 40 210 23 minecraft:oak_leaves[persistent=true]
fill 59 208 31 59 209 33 minecraft:moss_block
fill 59 201 20 59 202 22 minecraft:mossy_cobblestone
fill 59 210 22 59 210 24 minecraft:andesite
fill 59 206 21 59 206 24 minecraft:andesite
fill 54 205 20 59 206 20 minecraft:cobblestone
fill 53 210 20 57 210 20 minecraft:moss_block
fill 51 210 20 51 210 20 minecraft:oak_leaves[persistent=true]
fill 40 209 20 44 210 20 minecraft:mossy_cobblestone
fill 50 205 20 53 207 20 minecraft:granite
fill 46 206 20 46 209 20 minecraft:tuff
fill 49 207 39 53 209 39 minecraft:cobblestone
fill 40 204 39 41 204 39 minecraft:moss_block
fill 41 204 39 42 205 39 minecraft:mossy_cobblestone
fill 44 210 39 49 210 39 minecraft:cobblestone
fill 47 206 39 52 207 39 minecraft:andesite
fill 47 203 39 47 204 39 minecraft:moss_block
fill 56 201 30 58 201 38 minecraft:podzol
fill 55 201 31 55 201 38 minecraft:podzol
fill 41 201 33 43 201 38 minecraft:podzol
fill 44 201 34 44 201 38 minecraft:podzol
fill 53 201 35 54 201 37 minecraft:podzol
fill 54 201 38 54 201 38 minecraft:podzol
fill 46 201 37 50 205 38 minecraft:stone
fill 46 206 37 50 206 38 minecraft:podzol
execute positioned 43 201 21 run function rlk:room/prop/p_litter
execute positioned 56 201 28 run function rlk:room/prop/p_wildflower
execute positioned 41 201 24 run function rlk:room/prop/p_dandelion
execute positioned 56 202 30 run function rlk:room/prop/p_grass
execute positioned 58 202 30 run function rlk:room/prop/p_litter
execute positioned 54 202 38 run function rlk:room/prop/p_grass
execute positioned 47 201 25 run function rlk:room/prop/p_grass
execute positioned 54 202 35 run function rlk:room/prop/p_wildflower
setblock 48 207 37 minecraft:azalea_leaves[persistent=true] keep
setblock 50 207 38 minecraft:azalea_leaves[persistent=true] keep
setblock 46 207 38 minecraft:azalea_leaves[persistent=true] keep
setblock 49 207 37 minecraft:azalea_leaves[persistent=true] keep
setblock 47 207 37 minecraft:azalea_leaves[persistent=true] keep
