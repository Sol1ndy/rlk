# 구역 건설 (normal12_3, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -40 -21 200 -21 minecraft:podzol
fill -40 201 -40 -21 210 -21 minecraft:moss_block
fill -39 201 -39 -22 210 -21 minecraft:air
fill -39 209 -39 -22 209 -21 minecraft:light[level=15]
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:moss_block
fill -39 201 -20 -22 210 -2 minecraft:air
fill -39 209 -20 -22 209 -2 minecraft:light[level=15]
fill -25 200 -31 -22 200 -30 minecraft:moss_block
fill -38 200 -9 -37 200 -8 minecraft:packed_mud
fill -31 200 -14 -30 200 -12 minecraft:rooted_dirt
fill -25 200 -34 -24 200 -31 minecraft:coarse_dirt
fill -40 209 -26 -40 210 -21 minecraft:jungle_leaves[persistent=true]
fill -40 201 -30 -40 203 -28 minecraft:stone
fill -40 201 -24 -40 204 -21 minecraft:mossy_cobblestone
fill -40 209 -35 -40 210 -30 minecraft:jungle_leaves[persistent=true]
fill -40 201 -35 -40 201 -31 minecraft:mud_bricks
fill -40 210 -37 -40 210 -37 minecraft:mossy_cobblestone
fill -21 202 -40 -21 203 -35 minecraft:mud_bricks
fill -21 209 -34 -21 210 -34 minecraft:jungle_leaves[persistent=true]
fill -21 209 -33 -21 210 -31 minecraft:jungle_leaves[persistent=true]
fill -21 203 -36 -21 205 -35 minecraft:mossy_cobblestone
fill -29 201 -40 -29 210 -40 minecraft:jungle_log
fill -28 201 -40 -28 210 -40 minecraft:jungle_log
fill -32 209 -40 -28 210 -40 minecraft:jungle_leaves[persistent=true]
fill -40 209 -19 -40 210 -17 minecraft:jungle_leaves[persistent=true]
fill -40 203 -8 -40 203 -4 minecraft:mud_bricks
fill -40 210 -18 -40 210 -14 minecraft:azalea_leaves[persistent=true]
fill -40 203 -15 -40 205 -11 minecraft:stone
fill -21 210 -7 -21 210 -5 minecraft:jungle_leaves[persistent=true]
fill -21 210 -11 -21 210 -8 minecraft:jungle_leaves[persistent=true]
fill -21 208 -5 -21 208 -4 minecraft:mossy_cobblestone
fill -30 201 -1 -26 201 -1 minecraft:mud_bricks
fill -28 207 -1 -24 210 -1 minecraft:mossy_cobblestone
fill -30 201 -1 -30 210 -1 minecraft:jungle_log
fill -40 209 -1 -38 210 -1 minecraft:azalea_leaves[persistent=true]
fill -36 209 -1 -33 210 -1 minecraft:jungle_leaves[persistent=true]
fill -26 201 -1 -26 210 -1 minecraft:jungle_log
fill -40 210 -40 -21 210 -21 minecraft:polished_deepslate
fill -39 210 -39 -22 210 -21 minecraft:air
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -20 -22 210 -2 minecraft:air
fill -38 201 -27 -34 201 -26 minecraft:podzol
fill -39 201 -26 -39 201 -26 minecraft:podzol
fill -33 201 -26 -32 201 -25 minecraft:podzol
fill -34 201 -25 -34 201 -25 minecraft:podzol
fill -35 201 -24 -35 201 -17 minecraft:podzol
fill -25 201 -24 -23 201 -17 minecraft:podzol
fill -22 201 -23 -22 201 -17 minecraft:podzol
fill -39 201 -19 -39 201 -18 minecraft:podzol
fill -38 201 -18 -36 201 -17 minecraft:podzol
fill -27 201 -15 -27 201 -15 minecraft:podzol
fill -36 201 -25 -35 201 -25 minecraft:dirt
fill -36 202 -25 -35 202 -25 minecraft:podzol
fill -36 201 -24 -36 201 -19 minecraft:dirt
fill -36 202 -24 -36 202 -19 minecraft:podzol
fill -39 201 -21 -37 201 -20 minecraft:dirt
fill -39 202 -21 -37 202 -20 minecraft:podzol
fill -38 201 -19 -37 201 -19 minecraft:dirt
fill -38 202 -19 -37 202 -19 minecraft:podzol
fill -26 201 -29 -25 205 -29 minecraft:mossy_cobblestone
fill -26 206 -29 -25 206 -29 minecraft:podzol
fill -26 201 -28 -25 205 -28 minecraft:stone
fill -26 206 -28 -25 206 -28 minecraft:podzol
fill -39 201 -25 -37 207 -23 minecraft:mossy_cobblestone
fill -39 208 -25 -37 208 -23 minecraft:podzol
fill -39 201 -22 -37 207 -22 minecraft:stone
fill -39 208 -22 -37 208 -22 minecraft:podzol
fill -30 186 -40 -21 199 -33 minecraft:stone
fill -29 186 -34 -21 199 -32 minecraft:stone
fill -29 186 -39 -22 186 -34 minecraft:dirt
fill -29 187 -39 -22 188 -34 minecraft:jungle_leaves[persistent=true]
fill -29 189 -39 -22 201 -34 minecraft:air
fill -28 186 -33 -22 186 -33 minecraft:dirt
fill -28 187 -33 -22 188 -33 minecraft:jungle_leaves[persistent=true]
fill -28 189 -33 -22 201 -33 minecraft:air
execute positioned -34 201 -14 run function rlk:room/prop/sf_mush_red
execute positioned -33 201 -7 run function rlk:room/prop/sf_tree
execute positioned -28 201 -32 run function rlk:room/prop/sf_ruin_z
execute positioned -28 201 -10 run function rlk:room/prop/sf_mush_s
execute positioned -24 201 -26 run function rlk:room/prop/sf_mush_s
execute positioned -30 201 -28 run function rlk:room/prop/sf_mush_s
execute positioned -36 201 -36 run function rlk:room/prop/sf_mush_brown
execute positioned -37 201 -15 run function rlk:room/prop/sf_mush_s
execute positioned -30 201 -11 run function rlk:room/prop/sf_tree
execute positioned -33 201 -31 run function rlk:room/prop/sf_mush_brown
execute positioned -31 201 -14 run function rlk:room/prop/sf_fern
execute positioned -39 202 -19 run function rlk:room/prop/sf_moss
execute positioned -23 201 -33 run function rlk:room/prop/sf_fern
execute positioned -28 201 -8 run function rlk:room/prop/sf_fern
execute positioned -34 201 -30 run function rlk:room/prop/sf_fern
execute positioned -32 202 -25 run function rlk:room/prop/sf_fern
execute positioned -22 202 -17 run function rlk:room/prop/sf_moss
execute positioned -26 201 -6 run function rlk:room/prop/sf_moss
execute positioned -23 202 -19 run function rlk:room/prop/sf_moss
execute positioned -29 201 -32 run function rlk:room/prop/sf_flower
execute positioned -38 201 -9 run function rlk:room/prop/sf_fern
execute positioned -31 201 -3 run function rlk:room/prop/sf_moss
execute positioned -35 202 -22 run function rlk:room/prop/sf_flower
execute positioned -24 201 -3 run function rlk:room/prop/sf_flower
execute positioned -27 201 -24 run function rlk:room/prop/p_litter
execute positioned -38 203 -21 run function rlk:room/prop/sf_flower
execute positioned -37 201 -12 run function rlk:room/prop/p_litter
execute positioned -36 203 -20 run function rlk:room/prop/sf_moss
execute positioned -25 201 -12 run function rlk:room/prop/sf_flower
setblock -39 209 -24 minecraft:jungle_leaves[persistent=true] keep
setblock -38 209 -25 minecraft:jungle_leaves[persistent=true] keep
setblock -38 209 -23 minecraft:fern keep
setblock -38 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -37 209 -25 minecraft:jungle_leaves[persistent=true] keep
setblock -37 209 -24 minecraft:jungle_leaves[persistent=true] keep
setblock -37 209 -23 minecraft:fern keep
setblock -37 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -26 207 -28 minecraft:jungle_leaves[persistent=true] keep
setblock -25 207 -29 minecraft:fern keep
setblock -25 207 -28 minecraft:jungle_leaves[persistent=true] keep
