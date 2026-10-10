# 구역 건설 (first11_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -60 59 200 -41 minecraft:podzol
fill 40 201 -60 59 215 -41 minecraft:stone
fill 41 201 -59 58 215 -42 minecraft:air
fill 41 214 -59 58 214 -42 minecraft:light[level=15]
fill 57 205 -57 58 205 -55 minecraft:coarse_dirt
fill 52 205 -49 54 205 -46 minecraft:rooted_dirt
fill 40 212 -44 40 214 -41 minecraft:andesite
fill 40 214 -51 40 215 -51 minecraft:oak_leaves[persistent=true]
fill 40 201 -47 40 202 -44 minecraft:moss_block
fill 40 207 -51 40 207 -47 minecraft:granite
fill 40 206 -56 40 207 -56 minecraft:granite
fill 59 206 -48 59 208 -44 minecraft:tuff
fill 59 215 -58 59 215 -56 minecraft:oak_leaves[persistent=true]
fill 59 215 -45 59 215 -42 minecraft:moss_block
fill 43 212 -60 46 214 -60 minecraft:mossy_cobblestone
fill 51 215 -60 54 215 -60 minecraft:tuff
fill 52 202 -60 53 202 -60 minecraft:granite
fill 46 214 -41 46 215 -41 minecraft:oak_leaves[persistent=true]
fill 40 215 -41 42 215 -41 minecraft:oak_leaves[persistent=true]
fill 52 214 -41 53 215 -41 minecraft:andesite
fill 44 202 -41 45 204 -41 minecraft:cobblestone
fill 50 210 -41 54 213 -41 minecraft:andesite
fill 40 215 -60 59 215 -41 minecraft:polished_deepslate
fill 41 215 -59 58 215 -42 minecraft:air
fill 41 201 -59 41 204 -42 minecraft:dirt
fill 41 205 -59 41 205 -42 minecraft:podzol
fill 54 201 -59 58 204 -45 minecraft:dirt
fill 54 205 -59 58 205 -45 minecraft:podzol
fill 42 201 -56 45 204 -42 minecraft:dirt
fill 42 205 -56 45 205 -42 minecraft:podzol
fill 53 201 -56 53 204 -46 minecraft:dirt
fill 53 205 -56 53 205 -46 minecraft:podzol
fill 46 201 -54 52 204 -46 minecraft:dirt
fill 46 205 -54 52 205 -46 minecraft:podzol
fill 46 201 -45 48 204 -45 minecraft:dirt
fill 46 205 -45 48 205 -45 minecraft:podzol
fill 46 201 -44 47 204 -42 minecraft:dirt
fill 46 205 -44 47 205 -42 minecraft:podzol
fill 55 201 -44 58 204 -42 minecraft:dirt
fill 55 205 -44 58 205 -42 minecraft:podzol
fill 42 201 -59 43 205 -57 minecraft:dirt
fill 42 206 -59 43 206 -57 minecraft:podzol
fill 44 201 -57 45 205 -57 minecraft:dirt
fill 44 206 -57 45 206 -57 minecraft:podzol
fill 46 201 -56 46 205 -55 minecraft:dirt
fill 46 206 -56 46 206 -55 minecraft:podzol
fill 51 201 -56 52 205 -55 minecraft:dirt
fill 51 206 -56 52 206 -55 minecraft:podzol
fill 47 201 -55 50 205 -55 minecraft:dirt
fill 47 206 -55 50 206 -55 minecraft:podzol
fill 49 201 -45 53 205 -42 minecraft:dirt
fill 49 206 -45 53 206 -42 minecraft:podzol
fill 48 201 -44 48 205 -42 minecraft:dirt
fill 48 206 -44 48 206 -42 minecraft:podzol
fill 54 201 -44 54 205 -42 minecraft:dirt
fill 54 206 -44 54 206 -42 minecraft:podzol
fill 44 201 -59 48 206 -58 minecraft:dirt
fill 44 207 -59 48 207 -58 minecraft:podzol
fill 46 201 -57 46 206 -57 minecraft:dirt
fill 46 207 -57 46 207 -57 minecraft:podzol
fill 49 201 -56 50 206 -56 minecraft:dirt
fill 49 207 -56 50 207 -56 minecraft:podzol
fill 49 201 -59 50 212 -57 minecraft:andesite
fill 49 213 -59 50 213 -57 minecraft:podzol
fill 51 201 -58 53 212 -57 minecraft:andesite
fill 51 213 -58 53 213 -57 minecraft:podzol
fill 48 201 -57 48 212 -56 minecraft:andesite
fill 48 213 -57 48 213 -56 minecraft:podzol
fill 51 201 -59 53 212 -59 minecraft:stone
fill 51 213 -59 53 213 -59 minecraft:podzol
fill 47 201 -57 47 212 -56 minecraft:stone
fill 47 213 -57 47 213 -56 minecraft:podzol
execute positioned 55 206 -45 run function rlk:room/prop/p_boulder
execute positioned 51 207 -55 run function rlk:room/prop/p_grass
execute positioned 54 206 -50 run function rlk:room/prop/p_grass
execute positioned 44 206 -56 run function rlk:room/prop/p_wildflower
execute positioned 58 206 -51 run function rlk:room/prop/p_grass
execute positioned 43 207 -58 run function rlk:room/prop/p_grass
execute positioned 49 206 -50 run function rlk:room/prop/p_dandelion
setblock 47 214 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 49 214 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 50 214 -59 minecraft:short_grass keep
setblock 50 214 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 51 214 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 51 214 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 51 214 -57 minecraft:azalea_leaves[persistent=true] keep
setblock 52 214 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 52 214 -58 minecraft:azalea_leaves[persistent=true] keep
setblock 52 214 -57 minecraft:short_grass keep
setblock 53 214 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 53 214 -58 minecraft:short_grass keep
setblock 53 214 -57 minecraft:short_grass keep
