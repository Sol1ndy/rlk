# 구역 건설 (levelup10_5, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 0 59 200 19 minecraft:podzol
fill 40 201 0 59 210 19 minecraft:moss_block
fill 41 201 1 58 210 18 minecraft:air
fill 41 209 1 58 209 18 minecraft:light[level=15]
fill 42 200 2 43 200 5 minecraft:rooted_dirt
fill 47 200 7 49 200 9 minecraft:packed_mud
fill 40 209 0 40 210 0 minecraft:azalea_leaves[persistent=true]
fill 40 209 3 40 210 4 minecraft:jungle_leaves[persistent=true]
fill 40 210 7 40 210 11 minecraft:stone
fill 40 208 4 40 209 8 minecraft:mud_bricks
fill 59 209 2 59 209 4 minecraft:stone
fill 59 204 13 59 206 17 minecraft:mossy_cobblestone
fill 59 209 2 59 210 2 minecraft:jungle_leaves[persistent=true]
fill 42 201 0 42 210 0 minecraft:jungle_log
fill 42 201 0 42 210 0 minecraft:jungle_log
fill 40 209 0 45 210 0 minecraft:jungle_leaves[persistent=true]
fill 46 209 0 47 210 0 minecraft:jungle_leaves[persistent=true]
fill 48 210 0 51 210 0 minecraft:azalea_leaves[persistent=true]
fill 46 201 0 46 210 0 minecraft:jungle_log
fill 47 209 19 52 210 19 minecraft:jungle_leaves[persistent=true]
fill 53 206 19 58 207 19 minecraft:mossy_cobblestone
fill 53 206 19 55 208 19 minecraft:stone
fill 59 209 19 59 210 19 minecraft:jungle_leaves[persistent=true]
fill 40 210 0 59 210 19 minecraft:polished_deepslate
fill 41 210 1 58 210 18 minecraft:air
fill 43 201 11 43 201 18 minecraft:podzol
fill 44 201 12 45 201 13 minecraft:podzol
fill 44 201 14 44 201 18 minecraft:podzol
fill 41 201 15 42 201 18 minecraft:podzol
fill 41 201 9 42 207 9 minecraft:mossy_cobblestone
fill 41 208 9 42 208 9 minecraft:podzol
fill 41 201 10 41 207 14 minecraft:mossy_cobblestone
fill 41 208 10 41 208 14 minecraft:podzol
fill 42 201 14 42 207 14 minecraft:mossy_cobblestone
fill 42 208 14 42 208 14 minecraft:podzol
fill 42 201 10 42 207 13 minecraft:stone
fill 42 208 10 42 208 13 minecraft:podzol
execute positioned 56 201 5 run function rlk:room/prop/sf_ruin_z
execute positioned 45 201 5 run function rlk:room/prop/sf_mush_s
execute positioned 55 201 9 run function rlk:room/prop/sf_ruin_z
execute positioned 47 201 7 run function rlk:room/prop/sf_fern
execute positioned 51 201 9 run function rlk:room/prop/sf_fern
execute positioned 47 201 2 run function rlk:room/prop/sf_fern
execute positioned 51 201 17 run function rlk:room/prop/sf_flower
execute positioned 48 201 17 run function rlk:room/prop/sf_fern
execute positioned 51 201 1 run function rlk:room/prop/sf_flower
execute positioned 41 201 8 run function rlk:room/prop/sf_moss
execute positioned 46 201 14 run function rlk:room/prop/p_litter
execute positioned 41 201 1 run function rlk:room/prop/p_litter
setblock 41 209 9 minecraft:jungle_leaves[persistent=true] keep
setblock 41 209 10 minecraft:jungle_leaves[persistent=true] keep
setblock 41 209 13 minecraft:fern keep
setblock 42 209 9 minecraft:jungle_leaves[persistent=true] keep
setblock 42 209 10 minecraft:fern keep
setblock 42 209 11 minecraft:jungle_leaves[persistent=true] keep
setblock 42 209 12 minecraft:fern keep
setblock 42 209 14 minecraft:jungle_leaves[persistent=true] keep
