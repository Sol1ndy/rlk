# 구역 건설 (first6_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:moss_block
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 0 210 -12 0 210 -12 minecraft:jungle_leaves[persistent=true]
fill 0 201 -14 0 210 -14 minecraft:jungle_log
fill 0 201 -2 0 203 -1 minecraft:mossy_cobblestone
fill 0 208 -17 0 210 -13 minecraft:mossy_cobblestone
fill 0 208 -4 0 209 -2 minecraft:mossy_cobblestone
fill 0 203 -7 0 205 -6 minecraft:mossy_cobblestone
fill 19 204 -20 19 207 -16 minecraft:stone
fill 19 201 -4 19 210 -4 minecraft:jungle_log
fill 19 209 -20 19 210 -20 minecraft:jungle_leaves[persistent=true]
fill 19 209 -11 19 210 -9 minecraft:jungle_leaves[persistent=true]
fill 19 210 -15 19 210 -12 minecraft:jungle_leaves[persistent=true]
fill 15 209 -20 18 210 -20 minecraft:azalea_leaves[persistent=true]
fill 16 209 -20 19 210 -20 minecraft:stone
fill 9 209 -20 10 210 -20 minecraft:jungle_leaves[persistent=true]
fill 6 209 -20 9 210 -20 minecraft:jungle_leaves[persistent=true]
fill 2 209 -20 3 210 -20 minecraft:jungle_leaves[persistent=true]
fill 6 208 -20 6 209 -20 minecraft:mossy_cobblestone
fill 13 209 -1 16 210 -1 minecraft:jungle_leaves[persistent=true]
fill 13 201 -1 13 201 -1 minecraft:stone
fill 1 201 -1 6 204 -1 minecraft:mossy_cobblestone
fill 13 201 -1 13 210 -1 minecraft:jungle_log
fill 0 209 -1 0 210 -1 minecraft:mud_bricks
fill 7 201 -1 7 210 -1 minecraft:jungle_log
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -19 4 201 -19 minecraft:podzol
fill 4 201 -18 4 201 -18 minecraft:podzol
fill 3 201 -15 4 201 -15 minecraft:podzol
fill 1 201 -14 3 201 -14 minecraft:podzol
fill 1 201 -13 1 201 -13 minecraft:podzol
fill 1 201 -19 2 201 -15 minecraft:dirt
fill 1 202 -19 2 202 -15 minecraft:podzol
fill 3 201 -18 3 201 -16 minecraft:dirt
fill 3 202 -18 3 202 -16 minecraft:podzol
fill 8 201 -2 12 205 -2 minecraft:mossy_cobblestone
fill 8 206 -2 12 206 -2 minecraft:podzol
fill 4 201 -17 5 207 -16 minecraft:mossy_cobblestone
fill 4 208 -17 5 208 -16 minecraft:podzol
fill 9 201 -17 10 207 -16 minecraft:stone
fill 9 208 -17 10 208 -16 minecraft:podzol
execute positioned 11 201 -14 run function rlk:room/prop/p_litter
execute positioned 14 201 -9 run function rlk:room/prop/sf_fern
execute positioned 15 201 -2 run function rlk:room/prop/sf_flower
execute positioned 2 203 -17 run function rlk:room/prop/p_litter
execute positioned 8 201 -11 run function rlk:room/prop/sf_flower
execute positioned 11 201 -10 run function rlk:room/prop/sf_moss
execute positioned 12 201 -16 run function rlk:room/prop/sf_fern
execute positioned 16 201 -16 run function rlk:room/prop/sf_moss
execute positioned 18 201 -17 run function rlk:room/prop/sf_fern
setblock 4 209 -17 minecraft:fern keep
setblock 4 209 -16 minecraft:fern keep
setblock 5 209 -17 minecraft:jungle_leaves[persistent=true] keep
setblock 8 207 -2 minecraft:jungle_leaves[persistent=true] keep
setblock 9 209 -16 minecraft:fern keep
setblock 9 207 -2 minecraft:jungle_leaves[persistent=true] keep
setblock 10 209 -17 minecraft:jungle_leaves[persistent=true] keep
setblock 10 209 -16 minecraft:jungle_leaves[persistent=true] keep
setblock 10 207 -2 minecraft:jungle_leaves[persistent=true] keep
setblock 11 207 -2 minecraft:fern keep
setblock 12 207 -2 minecraft:jungle_leaves[persistent=true] keep
