# 구역 건설 (first11_2, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:moss_block
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 3 200 31 4 200 32 minecraft:moss_block
fill 14 200 22 17 200 23 minecraft:rooted_dirt
fill 4 200 21 8 200 23 minecraft:moss_block
fill 0 201 27 0 210 27 minecraft:jungle_log
fill 0 201 30 0 210 30 minecraft:jungle_log
fill 0 207 34 0 208 39 minecraft:stone
fill 0 205 29 0 206 29 minecraft:stone
fill 0 210 32 0 210 32 minecraft:jungle_leaves[persistent=true]
fill 19 210 23 19 210 27 minecraft:azalea_leaves[persistent=true]
fill 19 210 38 19 210 38 minecraft:jungle_leaves[persistent=true]
fill 19 209 32 19 210 35 minecraft:jungle_leaves[persistent=true]
fill 0 208 20 2 209 20 minecraft:mossy_cobblestone
fill 10 209 20 12 210 20 minecraft:jungle_leaves[persistent=true]
fill 9 209 20 11 210 20 minecraft:jungle_leaves[persistent=true]
fill 1 209 39 6 210 39 minecraft:jungle_leaves[persistent=true]
fill 3 210 39 7 210 39 minecraft:jungle_leaves[persistent=true]
fill 8 209 39 8 210 39 minecraft:mossy_cobblestone
fill 6 209 39 9 210 39 minecraft:jungle_leaves[persistent=true]
fill 12 209 39 14 210 39 minecraft:jungle_leaves[persistent=true]
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 6 201 35 13 201 35 minecraft:podzol
fill 6 201 36 6 201 38 minecraft:podzol
fill 13 201 36 13 201 36 minecraft:podzol
fill 5 201 37 5 201 37 minecraft:podzol
fill 14 201 37 14 201 38 minecraft:podzol
fill 7 201 36 12 201 38 minecraft:dirt
fill 7 202 36 12 202 38 minecraft:podzol
fill 13 201 37 13 201 38 minecraft:dirt
fill 13 202 37 13 202 38 minecraft:podzol
fill 1 201 26 1 205 29 minecraft:mossy_cobblestone
fill 1 206 26 1 206 29 minecraft:podzol
fill 1 201 30 1 205 31 minecraft:stone
fill 1 206 30 1 206 31 minecraft:podzol
execute positioned 4 201 26 run function rlk:room/prop/sf_mush_s
execute positioned 4 201 32 run function rlk:room/prop/sf_tree
execute positioned 1 201 37 run function rlk:room/prop/sf_rock
execute positioned 3 201 34 run function rlk:room/prop/sf_mush_red
execute positioned 5 201 28 run function rlk:room/prop/sf_tree_b
execute positioned 3 201 23 run function rlk:room/prop/sf_tree
execute positioned 15 201 33 run function rlk:room/prop/sf_ruin_z
execute positioned 8 202 35 run function rlk:room/prop/sf_flower
execute positioned 13 201 26 run function rlk:room/prop/sf_moss
execute positioned 6 202 35 run function rlk:room/prop/sf_flower
execute positioned 4 201 31 run function rlk:room/prop/p_litter
execute positioned 7 201 30 run function rlk:room/prop/p_litter
execute positioned 9 201 23 run function rlk:room/prop/sf_fern
execute positioned 7 203 37 run function rlk:room/prop/sf_fern
execute positioned 9 201 21 run function rlk:room/prop/sf_flower
execute positioned 16 201 23 run function rlk:room/prop/sf_moss
execute positioned 2 201 36 run function rlk:room/prop/sf_moss
execute positioned 9 203 38 run function rlk:room/prop/sf_flower
setblock 1 207 26 minecraft:fern keep
setblock 1 207 27 minecraft:jungle_leaves[persistent=true] keep
setblock 1 207 29 minecraft:jungle_leaves[persistent=true] keep
setblock 1 207 30 minecraft:jungle_leaves[persistent=true] keep
setblock 1 207 31 minecraft:fern keep
