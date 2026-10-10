# 구역 건설 (root1_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:moss_block
fill -19 201 1 -1 210 18 minecraft:air
fill -19 209 1 -1 209 18 minecraft:light[level=15]
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:moss_block
fill 0 201 1 18 210 18 minecraft:air
fill 0 209 1 18 209 18 minecraft:light[level=15]
fill 12 200 2 14 200 3 minecraft:rooted_dirt
fill -20 210 7 -20 210 8 minecraft:jungle_leaves[persistent=true]
fill -20 209 10 -20 210 12 minecraft:jungle_leaves[persistent=true]
fill -20 210 7 -20 210 7 minecraft:mossy_cobblestone
fill -20 210 11 -20 210 15 minecraft:jungle_leaves[persistent=true]
fill -20 210 7 -20 210 12 minecraft:jungle_leaves[persistent=true]
fill -18 201 0 -18 210 0 minecraft:jungle_log
fill -16 209 0 -11 210 0 minecraft:jungle_leaves[persistent=true]
fill -19 207 0 -19 207 0 minecraft:mossy_cobblestone
fill -16 210 19 -13 210 19 minecraft:jungle_leaves[persistent=true]
fill -11 209 19 -6 210 19 minecraft:jungle_leaves[persistent=true]
fill -13 201 19 -13 210 19 minecraft:jungle_log
fill -16 205 19 -16 205 19 minecraft:mossy_cobblestone
fill 19 207 1 19 208 6 minecraft:mossy_cobblestone
fill 19 210 2 19 210 7 minecraft:jungle_leaves[persistent=true]
fill 19 206 15 19 206 17 minecraft:stone
fill 19 208 12 19 210 16 minecraft:mossy_cobblestone
fill 19 204 6 19 205 10 minecraft:stone
fill 19 204 15 19 205 18 minecraft:mossy_cobblestone
fill 17 210 0 17 210 0 minecraft:azalea_leaves[persistent=true]
fill 15 209 0 16 210 0 minecraft:jungle_leaves[persistent=true]
fill 15 210 0 15 210 0 minecraft:mossy_cobblestone
fill 8 209 0 9 210 0 minecraft:jungle_leaves[persistent=true]
fill 10 207 0 11 210 0 minecraft:mossy_cobblestone
fill 6 209 0 8 210 0 minecraft:jungle_leaves[persistent=true]
fill 8 210 19 12 210 19 minecraft:jungle_leaves[persistent=true]
fill 3 201 19 3 210 19 minecraft:jungle_log
fill 5 201 19 7 204 19 minecraft:mossy_cobblestone
fill 6 207 19 11 207 19 minecraft:stone
fill 13 210 19 13 210 19 minecraft:jungle_leaves[persistent=true]
fill 4 201 19 4 210 19 minecraft:jungle_log
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -1 210 18 minecraft:air
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 0 210 1 18 210 18 minecraft:air
fill -19 201 3 -18 201 4 minecraft:podzol
fill -3 201 3 -2 201 3 minecraft:podzol
fill -17 201 4 -16 201 4 minecraft:podzol
fill -10 201 4 -8 201 5 minecraft:podzol
fill -2 201 4 -1 201 5 minecraft:podzol
fill -16 201 5 -16 201 17 minecraft:podzol
fill -7 201 5 -7 201 5 minecraft:podzol
fill -4 201 5 -3 201 5 minecraft:podzol
fill 0 201 5 0 201 5 minecraft:podzol
fill -15 201 6 -15 201 13 minecraft:podzol
fill -6 201 6 -5 201 13 minecraft:podzol
fill 16 201 13 18 201 18 minecraft:podzol
fill -9 201 14 -7 201 14 minecraft:podzol
fill -5 201 14 -5 201 15 minecraft:podzol
fill 15 201 14 15 201 18 minecraft:podzol
fill -8 201 15 -6 201 15 minecraft:podzol
fill -4 201 15 -2 201 15 minecraft:podzol
fill 14 201 15 14 201 17 minecraft:podzol
fill -17 201 16 -17 201 18 minecraft:podzol
fill -19 201 17 -18 201 18 minecraft:podzol
fill -7 201 4 -3 201 4 minecraft:dirt
fill -7 202 4 -3 202 4 minecraft:podzol
fill -19 201 5 -17 201 5 minecraft:dirt
fill -19 202 5 -17 202 5 minecraft:podzol
fill -6 201 5 -5 201 5 minecraft:dirt
fill -6 202 5 -5 202 5 minecraft:podzol
fill -17 201 6 -17 201 15 minecraft:dirt
fill -17 202 6 -17 202 15 minecraft:podzol
fill -19 201 14 -18 201 16 minecraft:dirt
fill -19 202 14 -18 202 16 minecraft:podzol
fill -6 201 14 -6 201 14 minecraft:dirt
fill -6 202 14 -6 202 14 minecraft:podzol
fill -19 201 6 -18 202 13 minecraft:dirt
fill -19 203 6 -18 203 13 minecraft:podzol
fill 9 201 3 10 206 4 minecraft:mossy_cobblestone
fill 9 207 3 10 207 4 minecraft:podzol
fill -9 201 2 -4 207 3 minecraft:mossy_cobblestone
fill -9 208 2 -4 208 3 minecraft:podzol
fill 4 201 3 5 207 4 minecraft:mossy_cobblestone
fill 4 208 3 5 208 4 minecraft:podzol
fill -9 201 1 -4 207 1 minecraft:stone
fill -9 208 1 -4 208 1 minecraft:podzol
execute positioned 16 201 9 run function rlk:room/prop/sf_ruin_z
execute positioned 14 201 1 run function rlk:room/prop/sf_rock
execute positioned 9 201 14 run function rlk:room/prop/sf_mush_red
execute positioned -5 201 16 run function rlk:room/prop/sf_ruin_x
execute positioned -15 201 14 run function rlk:room/prop/sf_rock
execute positioned 14 201 7 run function rlk:room/prop/sf_mush_red
execute positioned 14 201 12 run function rlk:room/prop/sf_moss
execute positioned -4 203 4 run function rlk:room/prop/sf_flower
execute positioned 10 201 5 run function rlk:room/prop/sf_flower
execute positioned -6 201 17 run function rlk:room/prop/p_litter
execute positioned -1 201 7 run function rlk:room/prop/sf_moss
execute positioned -9 201 12 run function rlk:room/prop/sf_fern
execute positioned 3 201 6 run function rlk:room/prop/sf_flower
execute positioned -17 201 1 run function rlk:room/prop/sf_fern
execute positioned -19 203 5 run function rlk:room/prop/sf_moss
execute positioned -8 201 16 run function rlk:room/prop/sf_moss
execute positioned -7 203 4 run function rlk:room/prop/sf_moss
execute positioned -1 201 12 run function rlk:room/prop/sf_moss
execute positioned -19 204 6 run function rlk:room/prop/sf_fern
execute positioned -3 201 10 run function rlk:room/prop/p_litter
execute positioned 2 201 9 run function rlk:room/prop/sf_flower
execute positioned 11 201 4 run function rlk:room/prop/sf_fern
execute positioned 0 201 15 run function rlk:room/prop/sf_fern
execute positioned -12 201 13 run function rlk:room/prop/sf_moss
execute positioned 8 201 8 run function rlk:room/prop/sf_flower
execute positioned -13 201 15 run function rlk:room/prop/sf_moss
setblock -9 209 1 minecraft:fern keep
setblock -9 209 2 minecraft:jungle_leaves[persistent=true] keep
setblock -8 209 3 minecraft:jungle_leaves[persistent=true] keep
setblock -7 209 1 minecraft:jungle_leaves[persistent=true] keep
setblock -7 209 2 minecraft:fern keep
setblock -7 209 3 minecraft:jungle_leaves[persistent=true] keep
setblock -6 209 1 minecraft:jungle_leaves[persistent=true] keep
setblock -6 209 2 minecraft:jungle_leaves[persistent=true] keep
setblock -5 209 1 minecraft:jungle_leaves[persistent=true] keep
setblock -4 209 1 minecraft:jungle_leaves[persistent=true] keep
setblock -4 209 2 minecraft:fern keep
setblock -4 209 3 minecraft:jungle_leaves[persistent=true] keep
setblock 4 209 3 minecraft:fern keep
setblock 4 209 4 minecraft:fern keep
setblock 5 209 3 minecraft:fern keep
setblock 5 209 4 minecraft:jungle_leaves[persistent=true] keep
setblock 9 208 3 minecraft:jungle_leaves[persistent=true] keep
setblock 10 208 3 minecraft:jungle_leaves[persistent=true] keep
setblock 10 208 4 minecraft:fern keep
