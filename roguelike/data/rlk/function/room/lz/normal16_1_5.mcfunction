# 구역 건설 (normal16_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:moss_block
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 10 200 6 13 200 7 minecraft:coarse_dirt
fill 8 200 4 9 200 5 minecraft:packed_mud
fill 0 202 18 0 203 18 minecraft:mossy_cobblestone
fill 0 201 15 0 210 15 minecraft:jungle_log
fill 0 201 12 0 210 12 minecraft:jungle_log
fill 19 209 0 19 210 2 minecraft:jungle_leaves[persistent=true]
fill 19 201 16 19 202 17 minecraft:stone
fill 19 210 4 19 210 6 minecraft:jungle_leaves[persistent=true]
fill 19 201 2 19 202 2 minecraft:stone
fill 19 210 10 19 210 10 minecraft:mud_bricks
fill 3 210 0 7 210 0 minecraft:azalea_leaves[persistent=true]
fill 14 206 0 17 206 0 minecraft:mossy_cobblestone
fill 12 209 0 12 210 0 minecraft:jungle_leaves[persistent=true]
fill 4 210 0 8 210 0 minecraft:jungle_leaves[persistent=true]
fill 16 202 19 19 204 19 minecraft:stone
fill 0 210 19 1 210 19 minecraft:azalea_leaves[persistent=true]
fill 8 210 19 8 210 19 minecraft:jungle_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 13 201 1 14 201 5 minecraft:podzol
fill 15 201 6 18 201 6 minecraft:podzol
fill 15 201 7 16 201 7 minecraft:podzol
fill 15 201 1 18 201 5 minecraft:dirt
fill 15 202 1 18 202 5 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:mossy_cobblestone
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:mossy_cobblestone
fill 12 208 4 12 208 4 minecraft:podzol
fill 17 201 7 18 207 9 minecraft:mossy_cobblestone
fill 17 208 7 18 208 9 minecraft:podzol
fill 17 201 10 17 207 10 minecraft:mossy_cobblestone
fill 17 208 10 17 208 10 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:stone
fill 12 208 3 12 208 3 minecraft:podzol
fill 18 201 10 18 207 10 minecraft:stone
fill 18 208 10 18 208 10 minecraft:podzol
execute positioned 7 201 5 run function rlk:room/prop/sf_mush_s
execute positioned 15 203 4 run function rlk:room/prop/sf_moss
execute positioned 11 201 12 run function rlk:room/prop/sf_flower
execute positioned 11 201 6 run function rlk:room/prop/sf_fern
execute positioned 8 201 5 run function rlk:room/prop/sf_moss
execute positioned 2 201 3 run function rlk:room/prop/sf_fern
execute positioned 15 201 18 run function rlk:room/prop/sf_flower
execute positioned 6 201 17 run function rlk:room/prop/sf_moss
execute positioned 4 201 14 run function rlk:room/prop/p_litter
execute positioned 16 202 7 run function rlk:room/prop/sf_flower
execute positioned 16 203 4 run function rlk:room/prop/sf_moss
execute positioned 14 201 7 run function rlk:room/prop/sf_fern
setblock 11 209 3 minecraft:jungle_leaves[persistent=true] keep
setblock 11 209 4 minecraft:jungle_leaves[persistent=true] keep
setblock 12 209 4 minecraft:fern keep
setblock 17 209 7 minecraft:jungle_leaves[persistent=true] keep
setblock 17 209 10 minecraft:fern keep
setblock 18 209 9 minecraft:fern keep
