# 구역 건설 (normal18_6, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:moss_block
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 7 200 7 11 200 8 minecraft:coarse_dirt
fill 14 200 7 16 200 10 minecraft:rooted_dirt
fill 0 201 6 0 210 6 minecraft:jungle_log
fill 0 202 0 0 205 5 minecraft:mud_bricks
fill 0 210 2 0 210 2 minecraft:mud_bricks
fill 0 210 6 0 210 9 minecraft:azalea_leaves[persistent=true]
fill 19 207 1 19 208 3 minecraft:mossy_cobblestone
fill 19 209 12 19 210 13 minecraft:jungle_leaves[persistent=true]
fill 19 207 4 19 210 7 minecraft:mossy_cobblestone
fill 19 210 0 19 210 5 minecraft:mossy_cobblestone
fill 19 210 0 19 210 5 minecraft:jungle_leaves[persistent=true]
fill 8 201 0 8 210 0 minecraft:jungle_log
fill 2 209 0 5 210 0 minecraft:azalea_leaves[persistent=true]
fill 0 210 0 1 210 0 minecraft:azalea_leaves[persistent=true]
fill 1 201 19 1 210 19 minecraft:jungle_log
fill 16 201 19 17 204 19 minecraft:mossy_cobblestone
fill 3 208 19 8 210 19 minecraft:stone
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 15 201 5 18 201 6 minecraft:podzol
fill 18 201 7 18 201 15 minecraft:podzol
fill 15 201 14 17 201 15 minecraft:podzol
fill 7 201 3 8 205 4 minecraft:mossy_cobblestone
fill 7 206 3 8 206 4 minecraft:podzol
fill 10 201 17 11 206 18 minecraft:mossy_cobblestone
fill 10 207 17 11 207 18 minecraft:podzol
fill 12 201 17 12 206 18 minecraft:stone
fill 12 207 17 12 207 18 minecraft:podzol
execute positioned 8 201 16 run function rlk:room/prop/sf_mush_s
execute positioned 13 201 3 run function rlk:room/prop/sf_lamp
execute positioned 15 202 15 run function rlk:room/prop/sf_fern
execute positioned 10 201 1 run function rlk:room/prop/p_litter
execute positioned 7 201 7 run function rlk:room/prop/p_litter
execute positioned 15 201 8 run function rlk:room/prop/sf_fern
execute positioned 10 201 3 run function rlk:room/prop/sf_fern
execute positioned 8 201 18 run function rlk:room/prop/sf_fern
execute positioned 17 201 1 run function rlk:room/prop/p_litter
execute positioned 8 201 10 run function rlk:room/prop/sf_fern
execute positioned 4 201 1 run function rlk:room/prop/sf_flower
execute positioned 13 201 4 run function rlk:room/prop/sf_fern
execute positioned 13 201 3 run function rlk:room/prop/sf_fern
setblock 7 207 3 minecraft:fern keep
setblock 8 207 3 minecraft:fern keep
setblock 8 207 4 minecraft:fern keep
setblock 10 208 18 minecraft:jungle_leaves[persistent=true] keep
setblock 11 208 17 minecraft:jungle_leaves[persistent=true] keep
setblock 11 208 18 minecraft:jungle_leaves[persistent=true] keep
setblock 12 208 17 minecraft:fern keep
setblock 12 208 18 minecraft:jungle_leaves[persistent=true] keep
