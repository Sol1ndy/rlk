# 구역 건설 (levelup10_5, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 0 59 200 19 minecraft:podzol
fill 40 201 0 59 213 19 minecraft:moss_block
fill 41 201 1 58 213 18 minecraft:air
fill 41 212 1 58 212 18 minecraft:light[level=15]
fill 42 203 2 43 203 5 minecraft:rooted_dirt
fill 47 203 7 49 203 9 minecraft:packed_mud
fill 40 212 0 40 213 0 minecraft:azalea_leaves[persistent=true]
fill 40 212 3 40 213 4 minecraft:jungle_leaves[persistent=true]
fill 40 201 10 40 201 10 minecraft:stone
fill 40 213 7 40 213 11 minecraft:stone
fill 40 211 4 40 212 8 minecraft:mud_bricks
fill 59 212 2 59 212 4 minecraft:stone
fill 59 207 13 59 209 17 minecraft:mossy_cobblestone
fill 59 212 2 59 213 2 minecraft:jungle_leaves[persistent=true]
fill 42 201 0 42 213 0 minecraft:jungle_log
fill 42 201 0 42 213 0 minecraft:jungle_log
fill 40 212 0 45 213 0 minecraft:jungle_leaves[persistent=true]
fill 46 212 0 47 213 0 minecraft:jungle_leaves[persistent=true]
fill 48 213 0 51 213 0 minecraft:azalea_leaves[persistent=true]
fill 46 201 0 46 213 0 minecraft:jungle_log
fill 47 212 19 52 213 19 minecraft:jungle_leaves[persistent=true]
fill 53 209 19 58 210 19 minecraft:mossy_cobblestone
fill 53 209 19 55 211 19 minecraft:stone
fill 59 212 19 59 213 19 minecraft:jungle_leaves[persistent=true]
fill 40 213 0 59 213 19 minecraft:polished_deepslate
fill 41 213 1 58 213 18 minecraft:air
fill 41 201 1 45 202 8 minecraft:dirt
fill 41 203 1 45 203 8 minecraft:podzol
fill 46 201 4 46 202 18 minecraft:dirt
fill 46 203 4 46 203 18 minecraft:podzol
fill 47 201 5 58 202 14 minecraft:dirt
fill 47 203 5 58 203 14 minecraft:podzol
fill 43 201 9 45 202 10 minecraft:dirt
fill 43 203 9 45 203 10 minecraft:podzol
fill 44 201 11 45 202 11 minecraft:dirt
fill 44 203 11 45 203 11 minecraft:podzol
fill 45 201 14 45 202 18 minecraft:dirt
fill 45 203 14 45 203 18 minecraft:podzol
fill 47 201 15 47 202 15 minecraft:dirt
fill 47 203 15 47 203 15 minecraft:podzol
fill 46 201 1 46 203 3 minecraft:dirt
fill 46 204 1 46 204 3 minecraft:podzol
fill 47 201 3 58 203 4 minecraft:dirt
fill 47 204 3 58 204 4 minecraft:podzol
fill 43 201 11 43 203 18 minecraft:dirt
fill 43 204 11 43 204 18 minecraft:podzol
fill 44 201 12 45 203 13 minecraft:dirt
fill 44 204 12 45 204 13 minecraft:podzol
fill 44 201 14 44 203 18 minecraft:dirt
fill 44 204 14 44 204 18 minecraft:podzol
fill 41 201 15 42 203 18 minecraft:dirt
fill 41 204 15 42 204 18 minecraft:podzol
fill 48 201 15 58 203 16 minecraft:dirt
fill 48 204 15 58 204 16 minecraft:podzol
fill 47 201 16 47 203 18 minecraft:dirt
fill 47 204 16 47 204 18 minecraft:podzol
fill 47 201 1 58 204 2 minecraft:dirt
fill 47 205 1 58 205 2 minecraft:podzol
fill 48 201 17 58 204 18 minecraft:dirt
fill 48 205 17 58 205 18 minecraft:podzol
fill 41 201 9 42 210 9 minecraft:mossy_cobblestone
fill 41 211 9 42 211 9 minecraft:podzol
fill 41 201 10 41 210 14 minecraft:mossy_cobblestone
fill 41 211 10 41 211 14 minecraft:podzol
fill 42 201 14 42 210 14 minecraft:mossy_cobblestone
fill 42 211 14 42 211 14 minecraft:podzol
fill 42 201 10 42 210 13 minecraft:stone
fill 42 211 10 42 211 13 minecraft:podzol
execute positioned 56 204 5 run function rlk:room/prop/sf_ruin_z
execute positioned 45 204 5 run function rlk:room/prop/sf_mush_s
execute positioned 55 204 9 run function rlk:room/prop/sf_ruin_z
execute positioned 47 204 7 run function rlk:room/prop/sf_fern
execute positioned 51 204 9 run function rlk:room/prop/sf_fern
execute positioned 47 206 2 run function rlk:room/prop/sf_fern
execute positioned 51 206 17 run function rlk:room/prop/sf_flower
execute positioned 48 206 17 run function rlk:room/prop/sf_fern
execute positioned 51 206 1 run function rlk:room/prop/sf_flower
execute positioned 41 204 8 run function rlk:room/prop/sf_moss
execute positioned 46 204 14 run function rlk:room/prop/p_litter
execute positioned 41 204 1 run function rlk:room/prop/p_litter
setblock 41 212 9 minecraft:jungle_leaves[persistent=true] keep
setblock 41 212 10 minecraft:jungle_leaves[persistent=true] keep
setblock 41 212 13 minecraft:fern keep
setblock 42 212 9 minecraft:jungle_leaves[persistent=true] keep
setblock 42 212 10 minecraft:fern keep
setblock 42 212 11 minecraft:jungle_leaves[persistent=true] keep
setblock 42 212 12 minecraft:fern keep
setblock 42 212 14 minecraft:jungle_leaves[persistent=true] keep
