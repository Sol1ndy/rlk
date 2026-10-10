# 구역 건설 (boss4_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 11 200 -12 13 200 -9 minecraft:coarse_dirt
fill 9 200 -16 12 200 -15 minecraft:coarse_dirt
fill 12 200 -17 15 200 -16 minecraft:coarse_dirt
fill 0 209 -4 0 210 -3 minecraft:tuff
fill 0 210 -19 0 210 -19 minecraft:cherry_leaves[persistent=true]
fill 0 201 -17 0 210 -17 minecraft:stripped_dark_oak_log
fill 19 207 -14 19 208 -10 minecraft:cobblestone
fill 19 208 -18 19 208 -17 minecraft:tuff
fill 19 209 -11 19 210 -9 minecraft:cherry_leaves[persistent=true]
fill 8 204 -20 10 207 -20 minecraft:cobblestone
fill 15 202 -20 19 203 -20 minecraft:tuff
fill 8 204 -20 9 206 -20 minecraft:cobblestone
fill 14 203 -20 19 206 -20 minecraft:moss_block
fill 15 201 -20 15 210 -20 minecraft:stripped_dark_oak_log
fill 4 203 -1 8 204 -1 minecraft:calcite
fill 6 206 -1 11 206 -1 minecraft:cobblestone
fill 0 201 -1 2 204 -1 minecraft:calcite
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 3 201 -11 5 201 -9 minecraft:podzol
fill 2 201 -10 2 201 -7 minecraft:podzol
fill 1 201 -9 1 201 -2 minecraft:podzol
fill 5 201 -8 5 201 -6 minecraft:podzol
fill 6 201 -5 12 201 -5 minecraft:podzol
fill 11 201 -4 12 201 -2 minecraft:podzol
fill 2 201 -3 2 201 -2 minecraft:podzol
fill 10 201 -3 10 201 -2 minecraft:podzol
fill 3 201 -8 4 201 -2 minecraft:dirt
fill 3 202 -8 4 202 -2 minecraft:podzol
fill 2 201 -6 2 201 -4 minecraft:dirt
fill 2 202 -6 2 202 -4 minecraft:podzol
fill 5 201 -5 5 201 -2 minecraft:dirt
fill 5 202 -5 5 202 -2 minecraft:podzol
fill 6 201 -4 10 201 -4 minecraft:dirt
fill 6 202 -4 10 202 -4 minecraft:podzol
fill 6 201 -3 9 201 -2 minecraft:dirt
fill 6 202 -3 9 202 -2 minecraft:podzol
fill 8 201 -19 13 205 -19 minecraft:stone_bricks
fill 8 206 -19 13 206 -19 minecraft:podzol
fill 5 201 -17 6 207 -16 minecraft:stone_bricks
fill 5 208 -17 6 208 -16 minecraft:podzol
execute positioned 12 202 -4 run function rlk:room/prop/i_lantern
execute positioned 1 202 -8 run function rlk:room/prop/i_rock
execute positioned 10 202 -2 run function rlk:room/prop/i_lantern
execute positioned 8 201 -13 run function rlk:room/prop/i_petal
execute positioned 6 201 -18 run function rlk:room/prop/i_petal
execute positioned 15 201 -11 run function rlk:room/prop/i_grass
execute positioned 12 201 -14 run function rlk:room/prop/i_grass
execute positioned 9 201 -18 run function rlk:room/prop/i_grass
execute positioned 17 201 -2 run function rlk:room/prop/i_petal
execute positioned 3 201 -19 run function rlk:room/prop/i_petal
execute positioned 14 201 -3 run function rlk:room/prop/i_grass
execute positioned 11 201 -10 run function rlk:room/prop/i_flower
execute positioned 13 201 -7 run function rlk:room/prop/i_petal
setblock 5 209 -17 minecraft:cherry_leaves[persistent=true] keep
setblock 5 209 -16 minecraft:cherry_leaves[persistent=true] keep
setblock 6 209 -17 minecraft:short_grass keep
setblock 6 209 -16 minecraft:cherry_leaves[persistent=true] keep
setblock 9 207 -19 minecraft:short_grass keep
setblock 10 207 -19 minecraft:short_grass keep
setblock 13 207 -19 minecraft:short_grass keep
