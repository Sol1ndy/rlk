# 구역 건설 (first8_3, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 210 -41 minecraft:moss_block
fill 21 201 -59 38 210 -42 minecraft:air
fill 21 209 -59 38 209 -42 minecraft:light[level=15]
fill 24 200 -52 28 200 -51 minecraft:coarse_dirt
fill 30 200 -52 31 200 -50 minecraft:rooted_dirt
fill 20 210 -44 20 210 -42 minecraft:jungle_leaves[persistent=true]
fill 20 209 -57 20 210 -52 minecraft:jungle_leaves[persistent=true]
fill 20 203 -46 20 205 -45 minecraft:stone
fill 20 209 -54 20 210 -51 minecraft:mossy_cobblestone
fill 39 201 -51 39 210 -51 minecraft:jungle_log
fill 39 201 -52 39 210 -52 minecraft:jungle_log
fill 39 210 -51 39 210 -48 minecraft:jungle_leaves[persistent=true]
fill 36 204 -60 39 206 -60 minecraft:mossy_cobblestone
fill 20 209 -60 24 210 -60 minecraft:azalea_leaves[persistent=true]
fill 31 201 -60 34 201 -60 minecraft:mossy_cobblestone
fill 25 207 -60 26 210 -60 minecraft:mossy_cobblestone
fill 32 204 -41 33 205 -41 minecraft:stone
fill 20 209 -41 21 210 -41 minecraft:azalea_leaves[persistent=true]
fill 35 201 -41 35 201 -41 minecraft:mossy_cobblestone
fill 34 201 -41 34 210 -41 minecraft:jungle_log
fill 30 204 -41 33 207 -41 minecraft:stone
fill 38 205 -41 39 205 -41 minecraft:mud_bricks
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
fill 29 201 -59 29 207 -57 minecraft:mossy_cobblestone
fill 29 208 -59 29 208 -57 minecraft:podzol
fill 33 201 -59 34 207 -57 minecraft:mossy_cobblestone
fill 33 208 -59 34 208 -57 minecraft:podzol
fill 30 201 -59 32 207 -57 minecraft:stone
fill 30 208 -59 32 208 -57 minecraft:podzol
execute positioned 29 201 -42 run function rlk:room/prop/sf_ruin_x
execute positioned 23 201 -59 run function rlk:room/prop/sf_rock
execute positioned 34 201 -45 run function rlk:room/prop/sf_rock
execute positioned 27 202 -55 run function rlk:room/prop/p_litter
execute positioned 30 201 -44 run function rlk:room/prop/sf_fern
execute positioned 28 203 -56 run function rlk:room/prop/sf_fern
execute positioned 32 203 -56 run function rlk:room/prop/sf_fern
execute positioned 38 201 -45 run function rlk:room/prop/sf_moss
execute positioned 37 203 -58 run function rlk:room/prop/sf_fern
execute positioned 23 201 -53 run function rlk:room/prop/sf_moss
execute positioned 34 201 -42 run function rlk:room/prop/sf_fern
execute positioned 29 201 -52 run function rlk:room/prop/sf_fern
execute positioned 30 201 -49 run function rlk:room/prop/p_litter
execute positioned 35 203 -55 run function rlk:room/prop/sf_fern
execute positioned 29 201 -48 run function rlk:room/prop/sf_fern
setblock 29 209 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 29 209 -58 minecraft:jungle_leaves[persistent=true] keep
setblock 30 209 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 30 209 -58 minecraft:fern keep
setblock 31 209 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 31 209 -58 minecraft:jungle_leaves[persistent=true] keep
setblock 31 209 -57 minecraft:jungle_leaves[persistent=true] keep
setblock 32 209 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 32 209 -58 minecraft:jungle_leaves[persistent=true] keep
setblock 33 209 -59 minecraft:jungle_leaves[persistent=true] keep
setblock 33 209 -57 minecraft:jungle_leaves[persistent=true] keep
setblock 34 209 -59 minecraft:fern keep
setblock 34 209 -58 minecraft:fern keep
setblock 34 209 -57 minecraft:fern keep
