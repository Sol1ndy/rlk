# 구역 건설 (levelup7_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:moss_block
fill 1 201 -19 18 210 -1 minecraft:air
fill 1 209 -19 18 209 -1 minecraft:light[level=15]
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:moss_block
fill 1 201 0 18 210 18 minecraft:air
fill 1 209 0 18 209 18 minecraft:light[level=15]
fill 9 200 -11 10 200 -9 minecraft:packed_mud
fill 0 210 -9 0 210 -5 minecraft:jungle_leaves[persistent=true]
fill 0 209 -20 0 210 -15 minecraft:jungle_leaves[persistent=true]
fill 0 209 -9 0 209 -8 minecraft:mud_bricks
fill 19 201 -19 19 204 -15 minecraft:mossy_cobblestone
fill 19 209 -10 19 210 -10 minecraft:jungle_leaves[persistent=true]
fill 19 204 -16 19 205 -14 minecraft:mud_bricks
fill 19 210 -20 19 210 -20 minecraft:jungle_leaves[persistent=true]
fill 19 201 -11 19 210 -11 minecraft:jungle_log
fill 19 201 -16 19 201 -15 minecraft:mossy_cobblestone
fill 6 210 -20 9 210 -20 minecraft:jungle_leaves[persistent=true]
fill 12 201 -20 12 210 -20 minecraft:jungle_log
fill 12 210 -20 13 210 -20 minecraft:jungle_leaves[persistent=true]
fill 0 201 10 0 210 10 minecraft:jungle_log
fill 0 201 11 0 203 11 minecraft:mossy_cobblestone
fill 0 210 1 0 210 6 minecraft:jungle_leaves[persistent=true]
fill 0 201 9 0 210 9 minecraft:jungle_log
fill 0 210 8 0 210 13 minecraft:jungle_leaves[persistent=true]
fill 19 206 14 19 208 15 minecraft:mud_bricks
fill 19 201 3 19 210 3 minecraft:jungle_log
fill 19 209 0 19 210 1 minecraft:jungle_leaves[persistent=true]
fill 19 210 8 19 210 8 minecraft:jungle_leaves[persistent=true]
fill 19 207 10 19 208 11 minecraft:mud_bricks
fill 19 210 12 19 210 17 minecraft:mud_bricks
fill 12 202 19 16 205 19 minecraft:mossy_cobblestone
fill 10 209 19 15 210 19 minecraft:jungle_leaves[persistent=true]
fill 15 209 19 18 210 19 minecraft:jungle_leaves[persistent=true]
fill 4 208 19 4 210 19 minecraft:mossy_cobblestone
fill 5 206 19 6 208 19 minecraft:mossy_cobblestone
fill 12 201 19 14 202 19 minecraft:stone
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -1 minecraft:air
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 0 18 210 18 minecraft:air
fill 5 201 -19 6 201 -19 minecraft:podzol
fill 6 201 -18 7 201 -16 minecraft:podzol
fill 5 201 -15 6 201 -15 minecraft:podzol
fill 4 201 -14 5 201 -13 minecraft:podzol
fill 3 201 -13 3 201 -12 minecraft:podzol
fill 1 201 -12 2 201 -11 minecraft:podzol
fill 4 201 -12 4 201 -12 minecraft:podzol
fill 15 201 3 17 201 11 minecraft:podzol
fill 18 201 4 18 201 11 minecraft:podzol
fill 11 201 5 14 201 5 minecraft:podzol
fill 14 201 6 14 201 11 minecraft:podzol
fill 7 201 14 18 201 15 minecraft:podzol
fill 5 201 15 6 201 15 minecraft:podzol
fill 5 201 16 5 201 18 minecraft:podzol
fill 4 201 17 4 201 18 minecraft:podzol
fill 1 201 -19 4 201 -15 minecraft:dirt
fill 1 202 -19 4 202 -15 minecraft:podzol
fill 5 201 -18 5 201 -16 minecraft:dirt
fill 5 202 -18 5 202 -16 minecraft:podzol
fill 1 201 -14 3 201 -14 minecraft:dirt
fill 1 202 -14 3 202 -14 minecraft:podzol
fill 1 201 -13 2 201 -13 minecraft:dirt
fill 1 202 -13 2 202 -13 minecraft:podzol
fill 6 201 16 18 201 16 minecraft:dirt
fill 6 202 16 18 202 16 minecraft:podzol
fill 6 201 17 6 201 18 minecraft:dirt
fill 6 202 17 6 202 18 minecraft:podzol
fill 7 201 17 18 202 18 minecraft:dirt
fill 7 203 17 18 203 18 minecraft:podzol
fill 3 201 -8 4 206 -7 minecraft:mossy_cobblestone
fill 3 207 -8 4 207 -7 minecraft:podzol
fill 1 201 -3 2 207 1 minecraft:mossy_cobblestone
fill 1 208 -3 2 208 1 minecraft:podzol
fill 1 201 4 3 207 7 minecraft:mossy_cobblestone
fill 1 208 4 3 208 7 minecraft:podzol
fill 3 201 8 3 207 9 minecraft:mossy_cobblestone
fill 3 208 8 3 208 9 minecraft:podzol
fill 1 201 8 2 207 9 minecraft:stone
fill 1 208 8 2 208 9 minecraft:podzol
execute positioned 12 201 -17 run function rlk:room/prop/sf_log_x
execute positioned 14 201 -9 run function rlk:room/prop/sf_tree_b
execute positioned 14 201 -5 run function rlk:room/prop/sf_ruin_x
execute positioned 4 201 11 run function rlk:room/prop/sf_rock
execute positioned 14 201 -13 run function rlk:room/prop/sf_lamp
execute positioned 15 201 0 run function rlk:room/prop/sf_mush_red
execute positioned 18 201 -10 run function rlk:room/prop/sf_log_z
execute positioned 17 204 17 run function rlk:room/prop/sf_fern
execute positioned 8 201 13 run function rlk:room/prop/sf_fern
execute positioned 11 202 15 run function rlk:room/prop/sf_flower
execute positioned 11 201 3 run function rlk:room/prop/sf_moss
execute positioned 13 201 9 run function rlk:room/prop/sf_fern
execute positioned 6 201 8 run function rlk:room/prop/sf_fern
execute positioned 7 201 -4 run function rlk:room/prop/sf_fern
execute positioned 17 201 12 run function rlk:room/prop/sf_fern
execute positioned 14 201 -11 run function rlk:room/prop/sf_flower
execute positioned 16 202 7 run function rlk:room/prop/sf_moss
execute positioned 16 202 14 run function rlk:room/prop/sf_moss
execute positioned 17 201 -14 run function rlk:room/prop/sf_flower
execute positioned 5 201 -12 run function rlk:room/prop/sf_fern
execute positioned 4 201 -10 run function rlk:room/prop/sf_flower
execute positioned 12 201 -3 run function rlk:room/prop/sf_moss
execute positioned 13 201 12 run function rlk:room/prop/p_litter
execute positioned 15 201 -10 run function rlk:room/prop/sf_fern
execute positioned 18 202 11 run function rlk:room/prop/sf_flower
execute positioned 14 201 3 run function rlk:room/prop/sf_flower
execute positioned 4 202 -13 run function rlk:room/prop/sf_fern
execute positioned 15 203 16 run function rlk:room/prop/sf_fern
execute positioned 8 201 10 run function rlk:room/prop/p_litter
setblock 1 209 -2 minecraft:fern keep
setblock 1 209 -1 minecraft:jungle_leaves[persistent=true] keep
setblock 1 209 1 minecraft:fern keep
setblock 1 209 5 minecraft:fern keep
setblock 1 209 6 minecraft:jungle_leaves[persistent=true] keep
setblock 1 209 9 minecraft:fern keep
setblock 2 209 -3 minecraft:fern keep
setblock 2 209 1 minecraft:jungle_leaves[persistent=true] keep
setblock 2 209 4 minecraft:fern keep
setblock 2 209 5 minecraft:jungle_leaves[persistent=true] keep
setblock 2 209 7 minecraft:jungle_leaves[persistent=true] keep
setblock 2 209 8 minecraft:jungle_leaves[persistent=true] keep
setblock 2 209 9 minecraft:jungle_leaves[persistent=true] keep
setblock 3 208 -7 minecraft:fern keep
setblock 3 209 5 minecraft:fern keep
setblock 3 209 6 minecraft:jungle_leaves[persistent=true] keep
setblock 3 209 7 minecraft:jungle_leaves[persistent=true] keep
setblock 3 209 9 minecraft:fern keep
setblock 4 208 -7 minecraft:fern keep
