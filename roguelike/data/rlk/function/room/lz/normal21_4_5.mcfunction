# 구역 건설 (normal21_4, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:moss_block
fill -19 201 -39 -1 210 -22 minecraft:air
fill -19 209 -39 -1 209 -22 minecraft:light[level=15]
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:moss_block
fill 0 201 -39 18 210 -22 minecraft:air
fill 0 209 -39 18 209 -22 minecraft:light[level=15]
fill 11 200 -25 12 200 -23 minecraft:rooted_dirt
fill 10 200 -26 13 200 -25 minecraft:coarse_dirt
fill -8 200 -37 -6 200 -34 minecraft:packed_mud
fill -11 200 -37 -9 200 -36 minecraft:rooted_dirt
fill -11 200 -37 -9 200 -36 minecraft:rooted_dirt
fill 14 200 -31 16 200 -28 minecraft:moss_block
fill -20 210 -33 -20 210 -28 minecraft:jungle_leaves[persistent=true]
fill -20 209 -29 -20 210 -25 minecraft:mossy_cobblestone
fill -20 201 -37 -20 210 -37 minecraft:jungle_log
fill -20 209 -39 -20 210 -36 minecraft:jungle_leaves[persistent=true]
fill -12 210 -40 -9 210 -40 minecraft:jungle_leaves[persistent=true]
fill -6 201 -40 -6 210 -40 minecraft:jungle_log
fill -13 210 -40 -10 210 -40 minecraft:jungle_leaves[persistent=true]
fill -16 201 -21 -16 210 -21 minecraft:jungle_log
fill -15 210 -21 -13 210 -21 minecraft:jungle_leaves[persistent=true]
fill -17 201 -21 -17 210 -21 minecraft:jungle_log
fill -9 205 -21 -8 206 -21 minecraft:mossy_cobblestone
fill -18 201 -21 -18 210 -21 minecraft:jungle_log
fill 19 209 -22 19 210 -22 minecraft:jungle_leaves[persistent=true]
fill 19 209 -25 19 210 -21 minecraft:jungle_leaves[persistent=true]
fill 15 201 -40 15 203 -40 minecraft:stone
fill 9 201 -40 13 201 -40 minecraft:mossy_cobblestone
fill 3 209 -40 8 210 -40 minecraft:jungle_leaves[persistent=true]
fill 13 209 -40 16 210 -40 minecraft:jungle_leaves[persistent=true]
fill 6 210 -40 11 210 -40 minecraft:mossy_cobblestone
fill 0 201 -21 2 202 -21 minecraft:mud_bricks
fill 1 209 -21 6 209 -21 minecraft:mossy_cobblestone
fill 7 209 -21 11 210 -21 minecraft:jungle_leaves[persistent=true]
fill 7 210 -21 12 210 -21 minecraft:jungle_leaves[persistent=true]
fill 5 207 -21 9 208 -21 minecraft:mud_bricks
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -1 210 -22 minecraft:air
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 0 210 -39 18 210 -22 minecraft:air
fill 5 201 -33 7 201 -27 minecraft:podzol
fill 8 201 -32 8 201 -27 minecraft:podzol
fill 10 201 -32 10 201 -27 minecraft:podzol
fill 9 201 -31 9 201 -27 minecraft:podzol
fill 11 201 -31 11 201 -27 minecraft:podzol
fill -8 201 -30 -5 201 -30 minecraft:podzol
fill -6 201 -29 -5 201 -22 minecraft:podzol
fill -4 201 -25 -1 201 -24 minecraft:podzol
fill -4 201 -23 -3 201 -22 minecraft:podzol
fill -11 201 -34 -10 207 -33 minecraft:mossy_cobblestone
fill -11 208 -34 -10 208 -33 minecraft:podzol
fill 8 201 -33 8 207 -33 minecraft:mossy_cobblestone
fill 8 208 -33 8 208 -33 minecraft:podzol
fill -2 201 -23 1 207 -23 minecraft:mossy_cobblestone
fill -2 208 -23 1 208 -23 minecraft:podzol
fill -2 201 -22 -1 207 -22 minecraft:mossy_cobblestone
fill -2 208 -22 -1 208 -22 minecraft:podzol
fill 9 201 -34 9 207 -32 minecraft:stone
fill 9 208 -34 9 208 -32 minecraft:podzol
fill 10 201 -33 10 207 -33 minecraft:stone
fill 10 208 -33 10 208 -33 minecraft:podzol
fill 0 201 -22 1 207 -22 minecraft:stone
fill 0 208 -22 1 208 -22 minecraft:podzol
fill -13 186 -28 -8 199 -21 minecraft:stone
fill -20 186 -27 -12 199 -21 minecraft:stone
fill -12 186 -27 -9 186 -22 minecraft:dirt
fill -12 187 -27 -9 188 -22 minecraft:jungle_leaves[persistent=true]
fill -12 189 -27 -9 201 -22 minecraft:air
fill -19 186 -26 -13 186 -22 minecraft:dirt
fill -19 187 -26 -13 188 -22 minecraft:jungle_leaves[persistent=true]
fill -19 189 -26 -13 201 -22 minecraft:air
execute positioned 13 201 -35 run function rlk:room/prop/sf_rock
execute positioned 5 202 -30 run function rlk:room/prop/sf_ruin_z
execute positioned 2 201 -25 run function rlk:room/prop/sf_mush_s
execute positioned 10 201 -37 run function rlk:room/prop/sf_bush
execute positioned -17 201 -29 run function rlk:room/prop/sf_mush_red
execute positioned -13 201 -31 run function rlk:room/prop/sf_rock
execute positioned 1 201 -35 run function rlk:room/prop/sf_log_x
execute positioned -17 201 -36 run function rlk:room/prop/sf_mush_red
execute positioned -13 201 -35 run function rlk:room/prop/sf_lamp
execute positioned -6 201 -34 run function rlk:room/prop/sf_tree_b
execute positioned 8 202 -29 run function rlk:room/prop/sf_mush_red
execute positioned -16 201 -31 run function rlk:room/prop/sf_mush_red
execute positioned -6 202 -27 run function rlk:room/prop/sf_ruin_z
execute positioned 17 201 -24 run function rlk:room/prop/sf_fern
execute positioned 15 201 -36 run function rlk:room/prop/sf_flower
execute positioned -6 202 -25 run function rlk:room/prop/sf_fern
execute positioned 1 201 -36 run function rlk:room/prop/sf_flower
execute positioned -4 201 -36 run function rlk:room/prop/sf_fern
execute positioned 2 201 -28 run function rlk:room/prop/sf_fern
execute positioned 2 201 -34 run function rlk:room/prop/sf_moss
execute positioned 15 201 -27 run function rlk:room/prop/sf_moss
execute positioned -12 201 -31 run function rlk:room/prop/p_litter
execute positioned -12 201 -35 run function rlk:room/prop/sf_flower
execute positioned 16 201 -26 run function rlk:room/prop/sf_fern
execute positioned 1 201 -35 run function rlk:room/prop/sf_fern
execute positioned -13 201 -34 run function rlk:room/prop/sf_moss
execute positioned -9 201 -35 run function rlk:room/prop/sf_moss
execute positioned 7 201 -25 run function rlk:room/prop/sf_flower
execute positioned 17 201 -31 run function rlk:room/prop/p_litter
execute positioned 14 201 -25 run function rlk:room/prop/sf_fern
execute positioned 8 202 -28 run function rlk:room/prop/p_litter
execute positioned -3 201 -29 run function rlk:room/prop/sf_fern
execute positioned 12 201 -31 run function rlk:room/prop/sf_moss
execute positioned 10 201 -35 run function rlk:room/prop/sf_fern
setblock -11 209 -34 minecraft:jungle_leaves[persistent=true] keep
setblock -11 209 -33 minecraft:jungle_leaves[persistent=true] keep
setblock -10 209 -33 minecraft:fern keep
setblock -2 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -1 209 -23 minecraft:jungle_leaves[persistent=true] keep
setblock -1 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock 0 209 -23 minecraft:jungle_leaves[persistent=true] keep
setblock 0 209 -22 minecraft:fern keep
setblock 1 209 -23 minecraft:jungle_leaves[persistent=true] keep
setblock 9 209 -32 minecraft:jungle_leaves[persistent=true] keep
setblock 10 209 -33 minecraft:fern keep
