# 구역 건설 (first5_3, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:moss_block
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 15 200 -13 16 200 -12 minecraft:moss_block
fill 0 209 -19 0 210 -14 minecraft:azalea_leaves[persistent=true]
fill 0 210 -20 0 210 -19 minecraft:jungle_leaves[persistent=true]
fill 0 209 -11 0 210 -9 minecraft:jungle_leaves[persistent=true]
fill 0 209 -9 0 210 -5 minecraft:jungle_leaves[persistent=true]
fill 0 203 -8 0 204 -5 minecraft:mossy_cobblestone
fill 19 203 -18 19 203 -15 minecraft:stone
fill 19 209 -8 19 210 -3 minecraft:jungle_leaves[persistent=true]
fill 19 210 -17 19 210 -13 minecraft:jungle_leaves[persistent=true]
fill 19 201 -15 19 202 -13 minecraft:mossy_cobblestone
fill 19 209 -20 19 209 -15 minecraft:mossy_cobblestone
fill 19 209 -10 19 210 -5 minecraft:stone
fill 1 201 -20 1 201 -20 minecraft:mossy_cobblestone
fill 8 206 -20 9 209 -20 minecraft:stone
fill 16 209 -20 16 210 -20 minecraft:jungle_leaves[persistent=true]
fill 12 201 -20 12 210 -20 minecraft:jungle_log
fill 2 210 -20 7 210 -20 minecraft:jungle_leaves[persistent=true]
fill 11 201 -20 15 203 -20 minecraft:mud_bricks
fill 1 201 -1 2 202 -1 minecraft:stone
fill 9 201 -1 14 202 -1 minecraft:stone
fill 13 201 -1 13 210 -1 minecraft:jungle_log
fill 13 210 -1 14 210 -1 minecraft:mud_bricks
fill 12 209 -1 16 210 -1 minecraft:jungle_leaves[persistent=true]
fill 3 208 -1 7 210 -1 minecraft:stone
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 6 201 -19 6 201 -15 minecraft:podzol
fill 9 201 -19 10 201 -19 minecraft:podzol
fill 10 201 -18 10 201 -15 minecraft:podzol
fill 7 201 -15 9 201 -15 minecraft:podzol
fill 15 201 -9 17 201 -8 minecraft:podzol
fill 18 201 -8 18 201 -8 minecraft:podzol
fill 15 201 -7 15 201 -7 minecraft:podzol
fill 16 201 -6 16 201 -2 minecraft:podzol
fill 17 201 -2 18 201 -2 minecraft:podzol
fill 7 201 -19 8 201 -18 minecraft:dirt
fill 7 202 -19 8 202 -18 minecraft:podzol
fill 9 201 -18 9 201 -18 minecraft:dirt
fill 9 202 -18 9 202 -18 minecraft:podzol
fill 7 201 -17 7 201 -16 minecraft:dirt
fill 7 202 -17 7 202 -16 minecraft:podzol
fill 16 201 -7 18 201 -7 minecraft:dirt
fill 16 202 -7 18 202 -7 minecraft:podzol
fill 17 201 -6 18 201 -3 minecraft:dirt
fill 17 202 -6 18 202 -3 minecraft:podzol
fill 8 201 -17 8 207 -16 minecraft:mossy_cobblestone
fill 8 208 -17 8 208 -16 minecraft:podzol
fill 17 201 -15 18 207 -13 minecraft:mossy_cobblestone
fill 17 208 -15 18 208 -13 minecraft:podzol
fill 9 201 -17 9 207 -16 minecraft:stone
fill 9 208 -17 9 208 -16 minecraft:podzol
fill 17 201 -12 18 207 -11 minecraft:stone
fill 17 208 -12 18 208 -11 minecraft:podzol
fill 0 186 -20 4 199 -13 minecraft:stone
fill 1 186 -19 3 186 -14 minecraft:dirt
fill 1 187 -19 3 188 -14 minecraft:jungle_leaves[persistent=true]
fill 1 189 -19 3 201 -14 minecraft:air
execute positioned 15 201 -16 run function rlk:room/prop/sf_mush_s
execute positioned 12 201 -17 run function rlk:room/prop/sf_mush_s
execute positioned 13 201 -19 run function rlk:room/prop/sf_ruin_x
execute positioned 1 201 -13 run function rlk:room/prop/sf_ruin_z
execute positioned 4 201 -17 run function rlk:room/prop/sf_rock
execute positioned 5 201 -7 run function rlk:room/prop/sf_mush_s
execute positioned 2 201 -12 run function rlk:room/prop/sf_fern
execute positioned 2 201 -13 run function rlk:room/prop/p_litter
execute positioned 7 203 -18 run function rlk:room/prop/sf_flower
execute positioned 13 201 -9 run function rlk:room/prop/sf_moss
execute positioned 17 201 -18 run function rlk:room/prop/sf_moss
execute positioned 3 201 -5 run function rlk:room/prop/p_litter
execute positioned 6 201 -14 run function rlk:room/prop/sf_fern
execute positioned 6 201 -6 run function rlk:room/prop/sf_fern
execute positioned 7 203 -16 run function rlk:room/prop/sf_fern
execute positioned 7 201 -6 run function rlk:room/prop/sf_moss
execute positioned 7 201 -13 run function rlk:room/prop/p_litter
setblock 8 209 -17 minecraft:jungle_leaves[persistent=true] keep
setblock 9 209 -16 minecraft:jungle_leaves[persistent=true] keep
setblock 17 209 -13 minecraft:jungle_leaves[persistent=true] keep
setblock 17 209 -12 minecraft:fern keep
setblock 17 209 -11 minecraft:fern keep
setblock 18 209 -14 minecraft:fern keep
setblock 18 209 -13 minecraft:fern keep
setblock 18 209 -12 minecraft:fern keep
setblock 18 209 -11 minecraft:fern keep
