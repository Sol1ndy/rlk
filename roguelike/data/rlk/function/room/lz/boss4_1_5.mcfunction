# 구역 건설 (boss4_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:moss_block
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 2 200 -18 3 200 -15 minecraft:coarse_dirt
fill 6 200 -12 7 200 -10 minecraft:packed_mud
fill 0 209 -7 0 210 -6 minecraft:jungle_leaves[persistent=true]
fill 0 209 -5 0 210 -5 minecraft:azalea_leaves[persistent=true]
fill 0 210 -8 0 210 -6 minecraft:mud_bricks
fill 0 209 -3 0 210 -3 minecraft:jungle_leaves[persistent=true]
fill 0 207 -20 0 210 -16 minecraft:stone
fill 0 201 -17 0 203 -16 minecraft:stone
fill 19 205 -15 19 208 -14 minecraft:mossy_cobblestone
fill 19 210 -6 19 210 -2 minecraft:azalea_leaves[persistent=true]
fill 19 206 -7 19 208 -3 minecraft:mud_bricks
fill 19 202 -16 19 204 -11 minecraft:mud_bricks
fill 19 210 -10 19 210 -7 minecraft:jungle_leaves[persistent=true]
fill 19 201 -11 19 210 -11 minecraft:jungle_log
fill 10 209 -20 12 210 -20 minecraft:mud_bricks
fill 1 206 -20 2 206 -20 minecraft:mud_bricks
fill 3 201 -20 3 210 -20 minecraft:jungle_log
fill 13 209 -20 14 210 -20 minecraft:jungle_leaves[persistent=true]
fill 2 210 -20 4 210 -20 minecraft:jungle_leaves[persistent=true]
fill 0 201 -20 0 210 -20 minecraft:jungle_log
fill 2 201 -1 2 210 -1 minecraft:jungle_log
fill 4 201 -1 4 210 -1 minecraft:jungle_log
fill 7 208 -1 10 208 -1 minecraft:mossy_cobblestone
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -11 5 201 -9 minecraft:podzol
fill 2 201 -10 2 201 -7 minecraft:podzol
fill 1 201 -9 1 201 -2 minecraft:podzol
fill 5 201 -8 5 201 -6 minecraft:podzol
fill 6 201 -5 12 201 -5 minecraft:podzol
fill 11 201 -4 12 201 -2 minecraft:podzol
fill 2 201 -3 2 201 -2 minecraft:podzol
fill 10 201 -3 10 201 -2 minecraft:podzol
fill 3 201 -8 4 201 -2 minecraft:dirt
fill 3 202 -8 4 202 -2 minecraft:podzol
fill 2 201 -6 2 201 -4 minecraft:dirt
fill 2 202 -6 2 202 -4 minecraft:podzol
fill 5 201 -5 5 201 -2 minecraft:dirt
fill 5 202 -5 5 202 -2 minecraft:podzol
fill 6 201 -4 10 201 -4 minecraft:dirt
fill 6 202 -4 10 202 -4 minecraft:podzol
fill 6 201 -3 9 201 -2 minecraft:dirt
fill 6 202 -3 9 202 -2 minecraft:podzol
fill 8 201 -19 13 205 -19 minecraft:mossy_cobblestone
fill 8 206 -19 13 206 -19 minecraft:podzol
fill 5 201 -17 6 207 -16 minecraft:mossy_cobblestone
fill 5 208 -17 6 208 -16 minecraft:podzol
execute positioned 4 203 -4 run function rlk:room/prop/sf_lamp
execute positioned 4 201 -13 run function rlk:room/prop/sf_mush_s
execute positioned 17 201 -14 run function rlk:room/prop/sf_flower
execute positioned 1 201 -12 run function rlk:room/prop/sf_flower
execute positioned 7 201 -7 run function rlk:room/prop/p_litter
execute positioned 16 201 -8 run function rlk:room/prop/sf_flower
execute positioned 15 201 -9 run function rlk:room/prop/sf_flower
execute positioned 11 201 -12 run function rlk:room/prop/sf_fern
execute positioned 17 201 -13 run function rlk:room/prop/sf_fern
execute positioned 6 201 -19 run function rlk:room/prop/sf_fern
execute positioned 4 201 -17 run function rlk:room/prop/sf_flower
execute positioned 17 201 -8 run function rlk:room/prop/sf_fern
execute positioned 17 201 -3 run function rlk:room/prop/sf_fern
setblock 5 209 -16 minecraft:fern keep
setblock 6 209 -17 minecraft:jungle_leaves[persistent=true] keep
setblock 8 207 -19 minecraft:fern keep
setblock 9 207 -19 minecraft:fern keep
setblock 10 207 -19 minecraft:jungle_leaves[persistent=true] keep
setblock 11 207 -19 minecraft:fern keep
setblock 12 207 -19 minecraft:fern keep
setblock 13 207 -19 minecraft:fern keep
