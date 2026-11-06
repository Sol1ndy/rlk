# 구역 건설 (normal25_2, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:moss_block
fill -39 201 -19 -22 210 -1 minecraft:air
fill -39 209 -19 -22 209 -1 minecraft:light[level=15]
fill -40 200 0 -21 200 19 minecraft:podzol
fill -40 201 0 -21 210 19 minecraft:moss_block
fill -39 201 0 -22 210 18 minecraft:air
fill -39 209 0 -22 209 18 minecraft:light[level=15]
fill -26 200 -17 -22 200 -16 minecraft:rooted_dirt
fill -32 200 -13 -28 200 -11 minecraft:packed_mud
fill -24 200 -10 -22 200 -9 minecraft:moss_block
fill -26 200 3 -23 200 5 minecraft:moss_block
fill -40 210 -14 -40 210 -10 minecraft:jungle_leaves[persistent=true]
fill -40 210 -15 -40 210 -10 minecraft:azalea_leaves[persistent=true]
fill -40 208 -4 -40 208 -3 minecraft:mossy_cobblestone
fill -21 210 -10 -21 210 -10 minecraft:azalea_leaves[persistent=true]
fill -21 209 -19 -21 210 -14 minecraft:jungle_leaves[persistent=true]
fill -21 201 -17 -21 210 -17 minecraft:jungle_log
fill -27 210 -20 -26 210 -20 minecraft:jungle_leaves[persistent=true]
fill -39 209 -20 -36 210 -20 minecraft:jungle_leaves[persistent=true]
fill -31 210 -20 -28 210 -20 minecraft:mossy_cobblestone
fill -30 201 -20 -30 210 -20 minecraft:jungle_log
fill -40 210 13 -40 210 17 minecraft:jungle_leaves[persistent=true]
fill -40 210 14 -40 210 16 minecraft:jungle_leaves[persistent=true]
fill -40 209 13 -40 210 14 minecraft:jungle_leaves[persistent=true]
fill -40 209 13 -40 210 14 minecraft:mossy_cobblestone
fill -40 202 17 -40 202 17 minecraft:mossy_cobblestone
fill -21 210 12 -21 210 15 minecraft:azalea_leaves[persistent=true]
fill -21 201 3 -21 210 3 minecraft:jungle_log
fill -21 203 11 -21 205 16 minecraft:mossy_cobblestone
fill -21 202 1 -21 205 2 minecraft:mossy_cobblestone
fill -21 210 9 -21 210 11 minecraft:stone
fill -30 205 19 -30 207 19 minecraft:mossy_cobblestone
fill -34 209 19 -29 210 19 minecraft:jungle_leaves[persistent=true]
fill -36 210 19 -33 210 19 minecraft:jungle_leaves[persistent=true]
fill -29 201 19 -26 204 19 minecraft:mud_bricks
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -1 minecraft:air
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -39 210 0 -22 210 18 minecraft:air
fill -39 201 -3 -35 201 -3 minecraft:podzol
fill -35 201 -2 -35 201 7 minecraft:podzol
fill -39 201 5 -38 201 7 minecraft:podzol
fill -34 201 5 -30 201 5 minecraft:podzol
fill -34 201 6 -33 201 7 minecraft:podzol
fill -37 201 7 -36 201 7 minecraft:podzol
fill -39 201 -2 -36 201 -2 minecraft:dirt
fill -39 202 -2 -36 202 -2 minecraft:podzol
fill -36 201 -1 -36 201 4 minecraft:dirt
fill -36 202 -1 -36 202 4 minecraft:podzol
fill -39 201 -1 -37 207 4 minecraft:mossy_cobblestone
fill -39 208 -1 -37 208 4 minecraft:podzol
fill -37 201 5 -36 207 5 minecraft:mossy_cobblestone
fill -37 208 5 -36 208 5 minecraft:podzol
fill -37 201 6 -37 207 6 minecraft:mossy_cobblestone
fill -37 208 6 -37 208 6 minecraft:podzol
fill -36 201 6 -36 207 6 minecraft:stone
fill -36 208 6 -36 208 6 minecraft:podzol
fill -31 186 7 -27 199 19 minecraft:stone
fill -38 186 9 -33 199 17 minecraft:stone
fill -30 186 8 -28 186 18 minecraft:dirt
fill -30 187 8 -28 188 18 minecraft:jungle_leaves[persistent=true]
fill -30 189 8 -28 201 18 minecraft:air
fill -37 186 10 -34 186 16 minecraft:dirt
fill -37 187 10 -34 188 16 minecraft:jungle_leaves[persistent=true]
fill -37 189 10 -34 201 16 minecraft:air
execute positioned -33 201 -19 run function rlk:room/prop/sf_log_x
execute positioned -30 201 -13 run function rlk:room/prop/sf_ruin_z
execute positioned -25 201 -1 run function rlk:room/prop/sf_tree
execute positioned -28 201 -6 run function rlk:room/prop/sf_tree_b
execute positioned -33 201 -6 run function rlk:room/prop/sf_rock
execute positioned -27 201 -10 run function rlk:room/prop/sf_tree_b
execute positioned -31 201 7 run function rlk:room/prop/sf_lamp
execute positioned -29 201 -9 run function rlk:room/prop/sf_tree
execute positioned -31 201 -15 run function rlk:room/prop/sf_tree_b
execute positioned -35 201 -11 run function rlk:room/prop/sf_log_z
execute positioned -27 201 -15 run function rlk:room/prop/sf_ruin_z
execute positioned -25 201 -17 run function rlk:room/prop/sf_tree
execute positioned -34 201 8 run function rlk:room/prop/sf_bush
execute positioned -33 201 14 run function rlk:room/prop/sf_log_z
execute positioned -24 201 -7 run function rlk:room/prop/sf_flower
execute positioned -30 201 -7 run function rlk:room/prop/sf_fern
execute positioned -31 201 -17 run function rlk:room/prop/sf_fern
execute positioned -35 202 2 run function rlk:room/prop/sf_fern
execute positioned -37 201 -10 run function rlk:room/prop/sf_fern
execute positioned -35 201 -15 run function rlk:room/prop/sf_moss
execute positioned -28 201 16 run function rlk:room/prop/sf_fern
execute positioned -23 201 1 run function rlk:room/prop/sf_moss
execute positioned -30 201 2 run function rlk:room/prop/sf_moss
execute positioned -39 201 -6 run function rlk:room/prop/sf_fern
execute positioned -39 201 10 run function rlk:room/prop/sf_fern
execute positioned -37 201 9 run function rlk:room/prop/sf_fern
execute positioned -33 201 -10 run function rlk:room/prop/sf_fern
execute positioned -28 201 8 run function rlk:room/prop/sf_fern
execute positioned -33 201 -6 run function rlk:room/prop/sf_fern
execute positioned -36 201 -9 run function rlk:room/prop/sf_moss
execute positioned -28 201 -6 run function rlk:room/prop/sf_moss
execute positioned -29 201 -9 run function rlk:room/prop/p_litter
execute positioned -31 201 16 run function rlk:room/prop/sf_flower
execute positioned -38 201 -13 run function rlk:room/prop/sf_moss
execute positioned -35 201 -7 run function rlk:room/prop/sf_moss
execute positioned -36 201 -17 run function rlk:room/prop/sf_flower
setblock -39 209 -1 minecraft:fern keep
setblock -39 209 0 minecraft:fern keep
setblock -39 209 1 minecraft:jungle_leaves[persistent=true] keep
setblock -39 209 2 minecraft:jungle_leaves[persistent=true] keep
setblock -39 209 4 minecraft:fern keep
setblock -38 209 -1 minecraft:fern keep
setblock -38 209 1 minecraft:fern keep
setblock -38 209 4 minecraft:jungle_leaves[persistent=true] keep
setblock -37 209 0 minecraft:fern keep
setblock -37 209 1 minecraft:fern keep
setblock -37 209 2 minecraft:jungle_leaves[persistent=true] keep
setblock -37 209 3 minecraft:fern keep
setblock -37 209 4 minecraft:jungle_leaves[persistent=true] keep
setblock -36 209 5 minecraft:jungle_leaves[persistent=true] keep
