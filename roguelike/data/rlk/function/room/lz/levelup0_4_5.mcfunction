# 구역 건설 (levelup0_4, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:podzol
fill 20 201 0 39 210 19 minecraft:moss_block
fill 21 201 1 38 210 18 minecraft:air
fill 21 209 1 38 209 18 minecraft:light[level=15]
fill 30 200 9 32 200 11 minecraft:coarse_dirt
fill 27 200 11 30 200 12 minecraft:moss_block
fill 24 200 16 28 200 18 minecraft:packed_mud
fill 20 210 2 20 210 6 minecraft:jungle_leaves[persistent=true]
fill 20 210 17 20 210 17 minecraft:mossy_cobblestone
fill 20 209 3 20 210 6 minecraft:jungle_leaves[persistent=true]
fill 20 205 15 20 206 19 minecraft:stone
fill 20 201 4 20 210 4 minecraft:jungle_log
fill 39 201 15 39 210 15 minecraft:jungle_log
fill 39 209 10 39 210 12 minecraft:azalea_leaves[persistent=true]
fill 39 210 6 39 210 9 minecraft:jungle_leaves[persistent=true]
fill 39 210 5 39 210 6 minecraft:jungle_leaves[persistent=true]
fill 39 210 12 39 210 15 minecraft:jungle_leaves[persistent=true]
fill 39 210 13 39 210 17 minecraft:jungle_leaves[persistent=true]
fill 23 201 0 28 201 0 minecraft:mud_bricks
fill 22 210 0 27 210 0 minecraft:mossy_cobblestone
fill 34 209 0 39 210 0 minecraft:jungle_leaves[persistent=true]
fill 20 206 0 25 206 0 minecraft:mossy_cobblestone
fill 23 210 19 23 210 19 minecraft:jungle_leaves[persistent=true]
fill 22 209 19 22 210 19 minecraft:jungle_leaves[persistent=true]
fill 28 210 19 33 210 19 minecraft:azalea_leaves[persistent=true]
fill 20 209 19 20 210 19 minecraft:jungle_leaves[persistent=true]
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 38 210 18 minecraft:air
fill 24 201 1 25 201 2 minecraft:podzol
fill 25 201 3 25 201 4 minecraft:podzol
fill 26 201 4 38 201 4 minecraft:podzol
fill 21 201 5 22 201 5 minecraft:podzol
fill 27 201 5 38 201 5 minecraft:podzol
fill 22 201 6 22 201 6 minecraft:podzol
fill 23 201 7 24 201 7 minecraft:podzol
fill 25 201 8 25 201 14 minecraft:podzol
fill 35 201 8 38 201 18 minecraft:podzol
fill 24 201 14 24 201 14 minecraft:podzol
fill 23 201 15 23 201 15 minecraft:podzol
fill 31 201 15 34 201 15 minecraft:podzol
fill 32 201 16 34 201 16 minecraft:podzol
fill 33 201 17 34 201 17 minecraft:podzol
fill 34 201 18 34 201 18 minecraft:podzol
fill 26 201 1 26 201 3 minecraft:dirt
fill 26 202 1 26 202 3 minecraft:podzol
fill 27 201 3 38 201 3 minecraft:dirt
fill 27 202 3 38 202 3 minecraft:podzol
fill 21 201 6 21 201 7 minecraft:dirt
fill 21 202 6 21 202 7 minecraft:podzol
fill 22 201 7 22 201 7 minecraft:dirt
fill 22 202 7 22 202 7 minecraft:podzol
fill 23 201 8 24 201 8 minecraft:dirt
fill 23 202 8 24 202 8 minecraft:podzol
fill 24 201 9 24 201 13 minecraft:dirt
fill 24 202 9 24 202 13 minecraft:podzol
fill 23 201 13 23 201 14 minecraft:dirt
fill 23 202 13 23 202 14 minecraft:podzol
fill 27 201 1 38 202 2 minecraft:dirt
fill 27 203 1 38 203 2 minecraft:podzol
fill 21 201 8 22 202 12 minecraft:dirt
fill 21 203 8 22 203 12 minecraft:podzol
fill 23 201 9 23 202 12 minecraft:dirt
fill 23 203 9 23 203 12 minecraft:podzol
fill 21 201 13 22 207 16 minecraft:mossy_cobblestone
fill 21 208 13 22 208 16 minecraft:podzol
execute positioned 29 201 15 run function rlk:room/prop/sf_lamp
execute positioned 26 201 7 run function rlk:room/prop/sf_fern
execute positioned 33 201 8 run function rlk:room/prop/p_litter
execute positioned 36 202 9 run function rlk:room/prop/sf_fern
execute positioned 34 201 11 run function rlk:room/prop/sf_moss
execute positioned 28 201 10 run function rlk:room/prop/sf_flower
execute positioned 36 202 16 run function rlk:room/prop/sf_fern
execute positioned 32 201 14 run function rlk:room/prop/sf_fern
execute positioned 35 202 13 run function rlk:room/prop/sf_flower
execute positioned 24 201 16 run function rlk:room/prop/sf_moss
setblock 21 209 13 minecraft:fern keep
setblock 21 209 14 minecraft:jungle_leaves[persistent=true] keep
setblock 21 209 15 minecraft:fern keep
setblock 21 209 16 minecraft:jungle_leaves[persistent=true] keep
setblock 22 209 13 minecraft:jungle_leaves[persistent=true] keep
setblock 22 209 14 minecraft:jungle_leaves[persistent=true] keep
setblock 22 209 16 minecraft:fern keep
