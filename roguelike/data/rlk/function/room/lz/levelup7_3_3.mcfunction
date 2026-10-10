# 구역 건설 (levelup7_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:podzol
fill 20 201 20 39 215 39 minecraft:stone
fill 21 201 21 38 215 38 minecraft:air
fill 21 214 21 38 214 38 minecraft:light[level=15]
fill 24 205 24 26 205 25 minecraft:coarse_dirt
fill 20 214 24 20 215 26 minecraft:oak_leaves[persistent=true]
fill 20 211 20 20 214 25 minecraft:granite
fill 20 215 24 20 215 26 minecraft:oak_leaves[persistent=true]
fill 20 204 20 20 205 24 minecraft:moss_block
fill 20 209 30 20 211 31 minecraft:mossy_cobblestone
fill 20 202 23 20 202 28 minecraft:mossy_cobblestone
fill 39 215 23 39 215 28 minecraft:andesite
fill 39 204 31 39 206 35 minecraft:cobblestone
fill 39 207 29 39 210 31 minecraft:moss_block
fill 38 214 20 38 215 20 minecraft:moss_block
fill 34 201 20 39 202 20 minecraft:cobblestone
fill 22 213 20 23 214 20 minecraft:moss_block
fill 35 206 39 39 206 39 minecraft:tuff
fill 25 207 39 27 209 39 minecraft:cobblestone
fill 35 211 39 39 213 39 minecraft:mossy_cobblestone
fill 20 215 20 39 215 39 minecraft:polished_deepslate
fill 21 215 21 38 215 38 minecraft:air
fill 21 201 21 27 204 38 minecraft:dirt
fill 21 205 21 27 205 38 minecraft:podzol
fill 31 201 21 33 204 22 minecraft:dirt
fill 31 205 21 33 205 22 minecraft:podzol
fill 31 201 23 32 204 38 minecraft:dirt
fill 31 205 23 32 205 38 minecraft:podzol
fill 28 201 24 30 204 38 minecraft:dirt
fill 28 205 24 30 205 38 minecraft:podzol
fill 33 201 25 35 204 38 minecraft:dirt
fill 33 205 25 35 205 38 minecraft:podzol
fill 36 201 26 38 204 38 minecraft:dirt
fill 36 205 26 38 205 38 minecraft:podzol
fill 34 201 21 34 205 22 minecraft:dirt
fill 34 206 21 34 206 22 minecraft:podzol
fill 35 201 22 35 205 24 minecraft:dirt
fill 35 206 22 35 206 24 minecraft:podzol
fill 36 201 24 37 205 25 minecraft:dirt
fill 36 206 24 37 206 25 minecraft:podzol
fill 38 201 25 38 205 25 minecraft:dirt
fill 38 206 25 38 206 25 minecraft:podzol
fill 35 201 21 38 206 21 minecraft:dirt
fill 35 207 21 38 207 21 minecraft:podzol
fill 36 201 22 38 206 23 minecraft:dirt
fill 36 207 22 38 207 23 minecraft:podzol
fill 38 201 24 38 206 24 minecraft:dirt
fill 38 207 24 38 207 24 minecraft:podzol
fill 28 201 21 30 211 23 minecraft:stone
fill 28 212 21 30 212 23 minecraft:podzol
fill 33 201 23 34 212 24 minecraft:stone
fill 33 213 23 34 213 24 minecraft:podzol
execute positioned 37 206 34 run function rlk:room/prop/p_boulder
execute positioned 23 206 36 run function rlk:room/prop/p_grass
execute positioned 26 206 34 run function rlk:room/prop/p_litter
execute positioned 22 206 24 run function rlk:room/prop/p_dandelion
execute positioned 35 206 35 run function rlk:room/prop/p_grass
execute positioned 25 206 25 run function rlk:room/prop/p_grass
execute positioned 35 206 37 run function rlk:room/prop/p_grass
setblock 28 213 21 minecraft:azalea_leaves[persistent=true] keep
setblock 28 213 22 minecraft:short_grass keep
setblock 29 213 22 minecraft:short_grass keep
setblock 30 213 21 minecraft:azalea_leaves[persistent=true] keep
setblock 30 213 22 minecraft:azalea_leaves[persistent=true] keep
setblock 30 213 23 minecraft:azalea_leaves[persistent=true] keep
setblock 33 214 24 minecraft:short_grass keep
setblock 34 214 23 minecraft:azalea_leaves[persistent=true] keep
