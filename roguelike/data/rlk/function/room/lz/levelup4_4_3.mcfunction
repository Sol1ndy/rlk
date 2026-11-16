# 구역 건설 (levelup4_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 20 59 200 39 minecraft:podzol
fill 40 201 20 59 210 39 minecraft:stone
fill 41 201 21 58 210 38 minecraft:air
fill 41 209 21 58 209 38 minecraft:light[level=15]
fill 42 200 22 43 200 24 minecraft:rooted_dirt
fill 40 202 23 40 202 26 minecraft:moss_block
fill 40 205 32 40 205 32 minecraft:tuff
fill 40 203 24 40 205 27 minecraft:tuff
fill 59 209 34 59 209 38 minecraft:cobblestone
fill 59 201 34 59 202 34 minecraft:mossy_cobblestone
fill 59 210 20 59 210 23 minecraft:oak_leaves[persistent=true]
fill 46 207 20 51 210 20 minecraft:granite
fill 45 205 20 47 207 20 minecraft:moss_block
fill 47 202 20 49 204 20 minecraft:andesite
fill 44 209 20 47 210 20 minecraft:andesite
fill 53 205 20 55 206 20 minecraft:mossy_cobblestone
fill 55 204 20 58 206 20 minecraft:cobblestone
fill 44 202 39 48 204 39 minecraft:andesite
fill 41 210 39 46 210 39 minecraft:mossy_cobblestone
fill 54 204 39 59 204 39 minecraft:tuff
fill 50 201 39 52 202 39 minecraft:andesite
fill 40 210 20 59 210 39 minecraft:polished_deepslate
fill 41 210 21 58 210 38 minecraft:air
fill 50 201 21 58 201 22 minecraft:podzol
fill 49 201 22 49 201 24 minecraft:podzol
fill 50 201 23 50 201 25 minecraft:podzol
fill 53 201 23 58 201 25 minecraft:podzol
fill 51 201 25 52 201 25 minecraft:podzol
fill 55 201 26 58 201 26 minecraft:podzol
fill 55 201 27 57 201 27 minecraft:podzol
fill 55 201 28 55 201 28 minecraft:podzol
fill 51 201 23 52 206 24 minecraft:stone
fill 51 207 23 52 207 24 minecraft:podzol
execute positioned 45 201 21 run function rlk:room/prop/p_boulder
execute positioned 57 202 25 run function rlk:room/prop/p_hay
execute positioned 55 201 33 run function rlk:room/prop/p_oak
execute positioned 47 201 31 run function rlk:room/prop/p_dandelion
execute positioned 42 201 24 run function rlk:room/prop/p_wildflower
execute positioned 48 201 28 run function rlk:room/prop/p_dandelion
execute positioned 55 201 36 run function rlk:room/prop/p_wildflower
execute positioned 57 202 22 run function rlk:room/prop/p_grass
execute positioned 55 201 29 run function rlk:room/prop/p_grass
setblock 51 208 23 minecraft:azalea_leaves[persistent=true] keep
setblock 51 208 24 minecraft:azalea_leaves[persistent=true] keep
setblock 52 208 23 minecraft:azalea_leaves[persistent=true] keep
