# 구역 건설 (first8_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 215 -41 minecraft:stone
fill 21 201 -59 38 215 -42 minecraft:air
fill 21 214 -59 38 214 -42 minecraft:light[level=15]
fill 21 205 -55 24 205 -54 minecraft:gravel
fill 22 205 -56 26 205 -54 minecraft:coarse_dirt
fill 20 204 -51 20 206 -47 minecraft:mossy_cobblestone
fill 20 214 -59 20 215 -55 minecraft:oak_leaves[persistent=true]
fill 20 210 -58 20 212 -57 minecraft:granite
fill 39 215 -49 39 215 -47 minecraft:moss_block
fill 39 209 -55 39 211 -50 minecraft:cobblestone
fill 39 204 -51 39 206 -51 minecraft:andesite
fill 39 212 -60 39 212 -60 minecraft:mossy_cobblestone
fill 37 205 -60 38 206 -60 minecraft:andesite
fill 25 214 -60 30 215 -60 minecraft:oak_leaves[persistent=true]
fill 27 205 -60 30 205 -60 minecraft:cobblestone
fill 28 215 -60 33 215 -60 minecraft:oak_leaves[persistent=true]
fill 20 214 -60 21 215 -60 minecraft:oak_leaves[persistent=true]
fill 20 202 -60 23 202 -60 minecraft:moss_block
fill 22 206 -41 24 209 -41 minecraft:andesite
fill 34 202 -41 35 202 -41 minecraft:moss_block
fill 21 212 -41 21 212 -41 minecraft:moss_block
fill 22 211 -41 27 213 -41 minecraft:andesite
fill 20 215 -60 39 215 -41 minecraft:polished_deepslate
fill 21 215 -59 38 215 -42 minecraft:air
fill 21 201 -59 25 204 -42 minecraft:dirt
fill 21 205 -59 25 205 -42 minecraft:podzol
fill 26 201 -56 26 204 -42 minecraft:dirt
fill 26 205 -56 26 205 -42 minecraft:podzol
fill 27 201 -54 34 204 -42 minecraft:dirt
fill 27 205 -54 34 205 -42 minecraft:podzol
fill 35 201 -53 37 204 -42 minecraft:dirt
fill 35 205 -53 37 205 -42 minecraft:podzol
fill 38 201 -51 38 204 -42 minecraft:dirt
fill 38 205 -51 38 205 -42 minecraft:podzol
fill 26 201 -59 27 205 -57 minecraft:dirt
fill 26 206 -59 27 206 -57 minecraft:podzol
fill 27 201 -56 27 205 -55 minecraft:dirt
fill 27 206 -56 27 206 -55 minecraft:podzol
fill 28 201 -55 34 205 -55 minecraft:dirt
fill 28 206 -55 34 206 -55 minecraft:podzol
fill 38 201 -55 38 205 -52 minecraft:dirt
fill 38 206 -55 38 206 -52 minecraft:podzol
fill 35 201 -54 37 205 -54 minecraft:dirt
fill 35 206 -54 37 206 -54 minecraft:podzol
fill 28 201 -59 28 206 -56 minecraft:dirt
fill 28 207 -59 28 207 -56 minecraft:podzol
fill 37 201 -59 38 206 -56 minecraft:dirt
fill 37 207 -59 38 207 -56 minecraft:podzol
fill 29 201 -56 34 206 -56 minecraft:dirt
fill 29 207 -56 34 207 -56 minecraft:podzol
fill 35 201 -55 37 206 -55 minecraft:dirt
fill 35 207 -55 37 207 -55 minecraft:podzol
fill 35 201 -59 36 207 -56 minecraft:dirt
fill 35 208 -59 36 208 -56 minecraft:podzol
fill 30 201 -59 32 212 -57 minecraft:andesite
fill 30 213 -59 32 213 -57 minecraft:podzol
fill 29 201 -59 29 212 -57 minecraft:stone
fill 29 213 -59 29 213 -57 minecraft:podzol
fill 33 201 -59 34 212 -57 minecraft:stone
fill 33 213 -59 34 213 -57 minecraft:podzol
execute positioned 27 206 -44 run function rlk:room/prop/p_oak
execute positioned 27 207 -59 run function rlk:room/prop/p_dandelion
execute positioned 31 206 -52 run function rlk:room/prop/p_wildflower
execute positioned 24 206 -44 run function rlk:room/prop/p_grass
execute positioned 22 206 -47 run function rlk:room/prop/p_wildflower
execute positioned 21 206 -54 run function rlk:room/prop/p_grass
execute positioned 29 206 -47 run function rlk:room/prop/p_dandelion
execute positioned 33 206 -51 run function rlk:room/prop/p_grass
execute positioned 38 206 -49 run function rlk:room/prop/p_litter
setblock 29 214 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 29 214 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 31 214 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 31 214 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 31 214 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 32 214 -59 minecraft:short_grass keep
setblock 32 214 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 32 214 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 33 214 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 33 214 -58 minecraft:short_grass keep
setblock 33 214 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 34 214 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 34 214 -57 minecraft:azalea_leaves[persistent=true] keep
