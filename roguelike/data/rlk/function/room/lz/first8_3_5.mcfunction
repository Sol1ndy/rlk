# 구역 건설 (first8_3, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 215 -41 minecraft:moss_block
fill 21 201 -59 38 215 -42 minecraft:air
fill 21 214 -59 38 214 -42 minecraft:light[level=15]
fill 24 205 -52 28 205 -51 minecraft:coarse_dirt
fill 30 205 -52 31 205 -50 minecraft:rooted_dirt
fill 20 215 -44 20 215 -42 minecraft:jungle_leaves[persistent=true]
fill 20 203 -58 20 205 -54 minecraft:mossy_cobblestone
fill 20 204 -44 20 204 -44 minecraft:stone
fill 20 214 -57 20 215 -52 minecraft:jungle_leaves[persistent=true]
fill 20 208 -46 20 210 -45 minecraft:stone
fill 20 214 -54 20 215 -51 minecraft:mossy_cobblestone
fill 39 201 -51 39 215 -51 minecraft:jungle_log
fill 39 201 -52 39 215 -52 minecraft:jungle_log
fill 39 215 -51 39 215 -48 minecraft:jungle_leaves[persistent=true]
fill 36 209 -60 39 211 -60 minecraft:mossy_cobblestone
fill 20 214 -60 24 215 -60 minecraft:azalea_leaves[persistent=true]
fill 20 203 -60 25 204 -60 minecraft:mossy_cobblestone
fill 31 204 -60 34 206 -60 minecraft:mossy_cobblestone
fill 25 212 -60 26 215 -60 minecraft:mossy_cobblestone
fill 32 209 -41 33 210 -41 minecraft:stone
fill 20 214 -41 21 215 -41 minecraft:azalea_leaves[persistent=true]
fill 35 206 -41 35 206 -41 minecraft:mossy_cobblestone
fill 34 201 -41 34 215 -41 minecraft:jungle_log
fill 30 209 -41 33 212 -41 minecraft:stone
fill 38 210 -41 39 210 -41 minecraft:mud_bricks
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
fill 29 201 -59 29 212 -57 minecraft:mossy_cobblestone
fill 29 213 -59 29 213 -57 minecraft:podzol
fill 33 201 -59 34 212 -57 minecraft:mossy_cobblestone
fill 33 213 -59 34 213 -57 minecraft:podzol
fill 30 201 -59 32 212 -57 minecraft:stone
fill 30 213 -59 32 213 -57 minecraft:podzol
execute positioned 29 206 -42 run function rlk:room/prop/sf_ruin_x
execute positioned 23 206 -59 run function rlk:room/prop/sf_rock
execute positioned 34 206 -45 run function rlk:room/prop/sf_rock
execute positioned 27 207 -55 run function rlk:room/prop/p_litter
execute positioned 30 206 -44 run function rlk:room/prop/sf_fern
execute positioned 28 208 -56 run function rlk:room/prop/sf_fern
execute positioned 32 208 -56 run function rlk:room/prop/sf_fern
execute positioned 38 206 -45 run function rlk:room/prop/sf_moss
execute positioned 37 208 -58 run function rlk:room/prop/sf_fern
execute positioned 23 206 -53 run function rlk:room/prop/sf_moss
execute positioned 34 206 -42 run function rlk:room/prop/sf_fern
execute positioned 29 206 -52 run function rlk:room/prop/sf_fern
execute positioned 30 206 -49 run function rlk:room/prop/p_litter
execute positioned 35 208 -55 run function rlk:room/prop/sf_fern
execute positioned 29 206 -48 run function rlk:room/prop/sf_fern
setblock 29 214 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 29 214 -58 minecraft:jungle_leaves[persistent=true] keep
setblock 30 214 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 30 214 -58 minecraft:fern keep
setblock 31 214 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 31 214 -58 minecraft:jungle_leaves[persistent=true] keep
setblock 31 214 -57 minecraft:jungle_leaves[persistent=true] keep
setblock 32 214 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 32 214 -58 minecraft:jungle_leaves[persistent=true] keep
setblock 33 214 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 33 214 -57 minecraft:jungle_leaves[persistent=true] keep
setblock 34 214 -59 minecraft:fern keep
setblock 34 214 -58 minecraft:fern keep
setblock 34 214 -57 minecraft:fern keep
