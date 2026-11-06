# 구역 건설 (first11_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 9 200 4 13 200 6 minecraft:coarse_dirt
fill 3 200 13 6 200 14 minecraft:packed_mud
fill 0 201 7 0 210 7 minecraft:stripped_dark_oak_log
fill 0 210 13 0 210 17 minecraft:cherry_leaves[persistent=true]
fill 0 210 2 0 210 2 minecraft:tuff
fill 19 205 7 19 208 7 minecraft:cobblestone
fill 19 203 3 19 204 4 minecraft:andesite
fill 19 201 19 19 201 19 minecraft:andesite
fill 19 209 5 19 210 6 minecraft:cherry_leaves[persistent=true]
fill 19 201 11 19 210 11 minecraft:stripped_dark_oak_log
fill 3 201 0 3 210 0 minecraft:stripped_dark_oak_log
fill 9 202 0 13 203 0 minecraft:cobblestone
fill 3 209 0 3 209 0 minecraft:calcite
fill 0 201 19 3 203 19 minecraft:tuff
fill 12 201 19 15 201 19 minecraft:tuff
fill 11 209 19 14 210 19 minecraft:tuff
fill 6 209 19 7 210 19 minecraft:cherry_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 4 201 3 6 201 3 minecraft:podzol
fill 2 201 4 2 201 10 minecraft:podzol
fill 5 201 4 8 201 4 minecraft:podzol
fill 6 201 5 8 201 5 minecraft:podzol
fill 1 201 6 1 201 8 minecraft:podzol
fill 5 201 6 5 201 11 minecraft:podzol
fill 3 201 9 3 201 10 minecraft:podzol
fill 4 201 10 4 201 11 minecraft:podzol
fill 5 201 5 5 201 5 minecraft:dirt
fill 5 202 5 5 202 5 minecraft:podzol
fill 3 201 6 4 201 8 minecraft:dirt
fill 3 202 6 4 202 8 minecraft:podzol
fill 4 201 9 4 201 9 minecraft:dirt
fill 4 202 9 4 202 9 minecraft:podzol
fill 3 201 4 4 207 5 minecraft:stone_bricks
fill 3 208 4 4 208 5 minecraft:podzol
execute positioned 14 201 4 run function rlk:room/prop/i_sakura
execute positioned 5 201 17 run function rlk:room/prop/i_grass
execute positioned 12 201 17 run function rlk:room/prop/i_grass
execute positioned 6 201 15 run function rlk:room/prop/i_flower
execute positioned 18 201 16 run function rlk:room/prop/i_petal
execute positioned 17 201 8 run function rlk:room/prop/i_petal
execute positioned 12 201 16 run function rlk:room/prop/i_flower
execute positioned 6 201 15 run function rlk:room/prop/i_petal
execute positioned 17 201 5 run function rlk:room/prop/i_petal
setblock 3 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock 3 209 5 minecraft:short_grass keep
setblock 4 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock 4 209 5 minecraft:cherry_leaves[persistent=true] keep
