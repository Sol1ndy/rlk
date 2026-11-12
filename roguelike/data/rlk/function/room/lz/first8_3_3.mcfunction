# 구역 건설 (first8_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 210 -41 minecraft:stone
fill 21 201 -59 38 210 -42 minecraft:air
fill 21 209 -59 38 209 -42 minecraft:light[level=15]
fill 21 200 -55 24 200 -54 minecraft:gravel
fill 22 200 -56 26 200 -54 minecraft:coarse_dirt
fill 20 201 -51 20 201 -47 minecraft:mossy_cobblestone
fill 20 209 -59 20 210 -55 minecraft:oak_leaves[persistent=true]
fill 20 205 -58 20 207 -57 minecraft:granite
fill 39 210 -49 39 210 -47 minecraft:moss_block
fill 39 204 -55 39 206 -50 minecraft:cobblestone
fill 39 201 -51 39 201 -51 minecraft:andesite
fill 39 207 -60 39 207 -60 minecraft:mossy_cobblestone
fill 37 201 -60 38 201 -60 minecraft:andesite
fill 25 209 -60 30 210 -60 minecraft:oak_leaves[persistent=true]
fill 28 210 -60 33 210 -60 minecraft:oak_leaves[persistent=true]
fill 20 209 -60 21 210 -60 minecraft:oak_leaves[persistent=true]
fill 22 201 -41 24 204 -41 minecraft:andesite
fill 21 207 -41 21 207 -41 minecraft:moss_block
fill 22 206 -41 27 208 -41 minecraft:andesite
fill 20 210 -60 39 210 -41 minecraft:polished_deepslate
fill 21 210 -59 38 210 -42 minecraft:air
fill 26 201 -59 27 201 -57 minecraft:podzol
fill 27 201 -56 27 201 -55 minecraft:podzol
fill 28 201 -55 34 201 -55 minecraft:podzol
fill 38 201 -55 38 201 -52 minecraft:podzol
fill 35 201 -54 37 201 -54 minecraft:podzol
fill 28 201 -59 28 201 -56 minecraft:dirt
fill 28 202 -59 28 202 -56 minecraft:podzol
fill 37 201 -59 38 201 -56 minecraft:dirt
fill 37 202 -59 38 202 -56 minecraft:podzol
fill 29 201 -56 34 201 -56 minecraft:dirt
fill 29 202 -56 34 202 -56 minecraft:podzol
fill 35 201 -55 37 201 -55 minecraft:dirt
fill 35 202 -55 37 202 -55 minecraft:podzol
fill 35 201 -59 36 202 -56 minecraft:dirt
fill 35 203 -59 36 203 -56 minecraft:podzol
fill 30 201 -59 32 207 -57 minecraft:andesite
fill 30 208 -59 32 208 -57 minecraft:podzol
fill 29 201 -59 29 207 -57 minecraft:stone
fill 29 208 -59 29 208 -57 minecraft:podzol
fill 33 201 -59 34 207 -57 minecraft:stone
fill 33 208 -59 34 208 -57 minecraft:podzol
execute positioned 27 201 -44 run function rlk:room/prop/p_oak
execute positioned 27 202 -59 run function rlk:room/prop/p_dandelion
execute positioned 31 201 -52 run function rlk:room/prop/p_wildflower
execute positioned 24 201 -44 run function rlk:room/prop/p_grass
execute positioned 22 201 -47 run function rlk:room/prop/p_wildflower
execute positioned 21 201 -54 run function rlk:room/prop/p_grass
execute positioned 29 201 -47 run function rlk:room/prop/p_dandelion
execute positioned 33 201 -51 run function rlk:room/prop/p_grass
execute positioned 38 201 -49 run function rlk:room/prop/p_litter
setblock 29 209 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 29 209 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 31 209 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 31 209 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 31 209 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 32 209 -59 minecraft:short_grass keep
setblock 32 209 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 32 209 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 33 209 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 33 209 -58 minecraft:short_grass keep
setblock 33 209 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 34 209 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 34 209 -57 minecraft:azalea_leaves[persistent=true] keep
