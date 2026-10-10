# 구역 건설 (normal7_5, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:moss_block
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 14 200 25 17 200 26 minecraft:moss_block
fill 10 200 25 13 200 26 minecraft:coarse_dirt
fill 0 209 34 0 210 39 minecraft:jungle_leaves[persistent=true]
fill 0 209 29 0 210 29 minecraft:mossy_cobblestone
fill 0 201 28 0 210 28 minecraft:jungle_log
fill 19 209 22 19 210 27 minecraft:jungle_leaves[persistent=true]
fill 19 201 21 19 210 21 minecraft:jungle_log
fill 19 209 31 19 210 32 minecraft:jungle_leaves[persistent=true]
fill 16 207 20 17 209 20 minecraft:mossy_cobblestone
fill 14 210 20 19 210 20 minecraft:jungle_leaves[persistent=true]
fill 3 209 20 8 210 20 minecraft:jungle_leaves[persistent=true]
fill 18 201 20 18 210 20 minecraft:jungle_log
fill 3 201 20 7 204 20 minecraft:mud_bricks
fill 9 203 39 12 204 39 minecraft:stone
fill 5 202 39 10 202 39 minecraft:mud_bricks
fill 11 201 39 11 210 39 minecraft:jungle_log
fill 2 201 39 2 210 39 minecraft:jungle_log
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 3 201 27 5 201 28 minecraft:podzol
fill 1 201 28 2 201 29 minecraft:podzol
fill 5 201 29 5 201 34 minecraft:podzol
fill 1 201 30 1 201 30 minecraft:podzol
fill 6 201 35 8 201 35 minecraft:podzol
fill 4 201 36 7 201 36 minecraft:podzol
fill 13 201 36 18 201 36 minecraft:podzol
fill 4 201 37 5 201 37 minecraft:podzol
fill 13 201 37 14 201 38 minecraft:podzol
fill 2 201 30 2 201 32 minecraft:dirt
fill 2 202 30 2 202 32 minecraft:podzol
fill 1 201 31 1 201 32 minecraft:dirt
fill 1 202 31 1 202 32 minecraft:podzol
fill 3 201 31 4 201 32 minecraft:dirt
fill 3 202 31 4 202 32 minecraft:podzol
fill 4 201 33 4 201 35 minecraft:dirt
fill 4 202 33 4 202 35 minecraft:podzol
fill 5 201 35 5 201 35 minecraft:dirt
fill 5 202 35 5 202 35 minecraft:podzol
fill 15 201 37 18 201 38 minecraft:dirt
fill 15 202 37 18 202 38 minecraft:podzol
fill 3 201 30 4 207 30 minecraft:mossy_cobblestone
fill 3 208 30 4 208 30 minecraft:podzol
fill 3 201 33 3 207 33 minecraft:mossy_cobblestone
fill 3 208 33 3 208 33 minecraft:podzol
fill 1 201 34 2 207 37 minecraft:mossy_cobblestone
fill 1 208 34 2 208 37 minecraft:podzol
fill 3 201 38 3 207 38 minecraft:mossy_cobblestone
fill 3 208 38 3 208 38 minecraft:podzol
fill 3 201 29 4 207 29 minecraft:stone
fill 3 208 29 4 208 29 minecraft:podzol
fill 1 201 33 2 207 33 minecraft:stone
fill 1 208 33 2 208 33 minecraft:podzol
fill 3 201 34 3 207 37 minecraft:stone
fill 3 208 34 3 208 37 minecraft:podzol
fill 1 201 38 2 207 38 minecraft:stone
fill 1 208 38 2 208 38 minecraft:podzol
execute positioned 2 203 32 run function rlk:room/prop/sf_moss
execute positioned 2 201 25 run function rlk:room/prop/sf_moss
execute positioned 7 201 34 run function rlk:room/prop/sf_moss
execute positioned 13 201 24 run function rlk:room/prop/sf_fern
execute positioned 1 202 29 run function rlk:room/prop/sf_fern
execute positioned 8 201 32 run function rlk:room/prop/sf_flower
execute positioned 7 201 27 run function rlk:room/prop/sf_flower
execute positioned 9 201 36 run function rlk:room/prop/sf_fern
execute positioned 1 201 21 run function rlk:room/prop/sf_fern
setblock 1 209 34 minecraft:jungle_leaves[persistent=true] keep
setblock 1 209 35 minecraft:fern keep
setblock 1 209 36 minecraft:fern keep
setblock 1 209 37 minecraft:fern keep
setblock 1 209 38 minecraft:jungle_leaves[persistent=true] keep
setblock 2 209 33 minecraft:jungle_leaves[persistent=true] keep
setblock 2 209 34 minecraft:fern keep
setblock 2 209 37 minecraft:jungle_leaves[persistent=true] keep
setblock 2 209 38 minecraft:jungle_leaves[persistent=true] keep
setblock 3 209 29 minecraft:fern keep
setblock 3 209 30 minecraft:fern keep
setblock 3 209 33 minecraft:jungle_leaves[persistent=true] keep
setblock 3 209 34 minecraft:fern keep
setblock 3 209 35 minecraft:fern keep
setblock 3 209 36 minecraft:fern keep
setblock 3 209 37 minecraft:jungle_leaves[persistent=true] keep
setblock 3 209 38 minecraft:fern keep
setblock 4 209 30 minecraft:jungle_leaves[persistent=true] keep
