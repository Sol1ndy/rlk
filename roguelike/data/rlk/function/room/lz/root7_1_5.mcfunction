# 구역 건설 (root7_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:moss_block
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:moss_block
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill 8 200 -11 12 200 -10 minecraft:moss_block
fill 7 200 -10 10 200 -8 minecraft:moss_block
fill 12 200 -12 15 200 -9 minecraft:rooted_dirt
fill 17 200 -5 18 200 -2 minecraft:moss_block
fill -20 209 -16 -20 210 -13 minecraft:jungle_leaves[persistent=true]
fill -20 209 -16 -20 210 -12 minecraft:jungle_leaves[persistent=true]
fill -20 204 -16 -20 207 -15 minecraft:stone
fill -20 201 -15 -20 204 -10 minecraft:mud_bricks
fill -20 205 -19 -20 208 -16 minecraft:mossy_cobblestone
fill -13 209 -20 -10 210 -20 minecraft:jungle_leaves[persistent=true]
fill -19 201 -20 -19 210 -20 minecraft:jungle_log
fill -8 209 -20 -3 210 -20 minecraft:jungle_leaves[persistent=true]
fill -6 209 -20 -2 210 -20 minecraft:jungle_leaves[persistent=true]
fill -7 201 -1 -4 201 -1 minecraft:stone
fill -10 203 -1 -10 205 -1 minecraft:mossy_cobblestone
fill -19 209 -1 -16 210 -1 minecraft:jungle_leaves[persistent=true]
fill -11 206 -1 -10 208 -1 minecraft:mossy_cobblestone
fill -10 204 -1 -8 206 -1 minecraft:mossy_cobblestone
fill 19 201 -5 19 203 -2 minecraft:mossy_cobblestone
fill 19 210 -7 19 210 -6 minecraft:jungle_leaves[persistent=true]
fill 19 209 -15 19 210 -12 minecraft:jungle_leaves[persistent=true]
fill 0 210 -20 5 210 -20 minecraft:jungle_leaves[persistent=true]
fill 8 210 -20 13 210 -20 minecraft:jungle_leaves[persistent=true]
fill 5 210 -20 10 210 -20 minecraft:stone
fill 9 209 -20 10 210 -20 minecraft:azalea_leaves[persistent=true]
fill 15 207 -20 18 208 -20 minecraft:stone
fill 5 209 -1 5 210 -1 minecraft:jungle_leaves[persistent=true]
fill 12 209 -1 15 210 -1 minecraft:jungle_leaves[persistent=true]
fill 3 209 -1 6 210 -1 minecraft:jungle_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill 9 201 -19 15 201 -17 minecraft:podzol
fill 8 201 -18 8 201 -15 minecraft:podzol
fill 16 201 -18 16 201 -17 minecraft:podzol
fill 7 201 -17 7 201 -15 minecraft:podzol
fill 17 201 -17 17 201 -17 minecraft:podzol
fill 9 201 -16 13 201 -15 minecraft:podzol
fill -18 201 -8 -15 201 -7 minecraft:podzol
fill -19 201 -7 -19 201 -2 minecraft:podzol
fill -18 201 -6 -18 201 -6 minecraft:podzol
fill -14 201 -6 -10 201 -6 minecraft:podzol
fill -11 201 -5 -10 201 -2 minecraft:podzol
fill -17 201 -6 -15 201 -2 minecraft:dirt
fill -17 202 -6 -15 202 -2 minecraft:podzol
fill -18 201 -5 -18 201 -2 minecraft:dirt
fill -18 202 -5 -18 202 -2 minecraft:podzol
fill -14 201 -5 -12 201 -2 minecraft:dirt
fill -14 202 -5 -12 202 -2 minecraft:podzol
fill 2 201 -19 2 205 -18 minecraft:mossy_cobblestone
fill 2 206 -19 2 206 -18 minecraft:podzol
fill 3 201 -18 5 205 -18 minecraft:mossy_cobblestone
fill 3 206 -18 5 206 -18 minecraft:podzol
fill 3 201 -19 5 205 -19 minecraft:stone
fill 3 206 -19 5 206 -19 minecraft:podzol
fill -11 201 -19 -10 206 -18 minecraft:mossy_cobblestone
fill -11 207 -19 -10 207 -18 minecraft:podzol
fill -9 201 -18 -7 206 -18 minecraft:mossy_cobblestone
fill -9 207 -18 -7 207 -18 minecraft:podzol
fill -9 201 -19 -7 206 -19 minecraft:stone
fill -9 207 -19 -7 207 -19 minecraft:podzol
execute positioned -4 201 -4 run function rlk:room/prop/sf_log_x
execute positioned -6 201 -8 run function rlk:room/prop/sf_mush_brown
execute positioned 12 202 -16 run function rlk:room/prop/sf_rock
execute positioned -17 201 -13 run function rlk:room/prop/sf_ruin_x
execute positioned -7 201 -5 run function rlk:room/prop/sf_mush_s
execute positioned -13 201 -17 run function rlk:room/prop/sf_ruin_z
execute positioned -2 201 -19 run function rlk:room/prop/sf_log_z
execute positioned -13 203 -3 run function rlk:room/prop/sf_moss
execute positioned 17 201 -15 run function rlk:room/prop/sf_fern
execute positioned -18 202 -7 run function rlk:room/prop/sf_flower
execute positioned -15 201 -18 run function rlk:room/prop/sf_flower
execute positioned -19 202 -6 run function rlk:room/prop/sf_flower
execute positioned 2 201 -15 run function rlk:room/prop/sf_moss
execute positioned -3 201 -18 run function rlk:room/prop/sf_fern
execute positioned -7 201 -14 run function rlk:room/prop/sf_moss
execute positioned 0 201 -13 run function rlk:room/prop/sf_flower
execute positioned 6 201 -15 run function rlk:room/prop/sf_flower
execute positioned -3 201 -15 run function rlk:room/prop/sf_moss
execute positioned 8 201 -6 run function rlk:room/prop/sf_fern
execute positioned 5 201 -14 run function rlk:room/prop/sf_moss
execute positioned 11 201 -10 run function rlk:room/prop/sf_moss
execute positioned 18 201 -14 run function rlk:room/prop/sf_moss
execute positioned 1 201 -13 run function rlk:room/prop/sf_moss
execute positioned -14 201 -9 run function rlk:room/prop/sf_flower
execute positioned -16 201 -16 run function rlk:room/prop/p_litter
execute positioned -4 201 -10 run function rlk:room/prop/sf_moss
execute positioned -13 201 -13 run function rlk:room/prop/sf_flower
setblock -11 208 -19 minecraft:jungle_leaves[persistent=true] keep
setblock -9 208 -19 minecraft:jungle_leaves[persistent=true] keep
setblock -8 208 -18 minecraft:jungle_leaves[persistent=true] keep
setblock -7 208 -18 minecraft:jungle_leaves[persistent=true] keep
setblock 2 207 -18 minecraft:jungle_leaves[persistent=true] keep
setblock 3 207 -19 minecraft:fern keep
setblock 3 207 -18 minecraft:fern keep
setblock 5 207 -19 minecraft:jungle_leaves[persistent=true] keep
setblock 5 207 -18 minecraft:jungle_leaves[persistent=true] keep
