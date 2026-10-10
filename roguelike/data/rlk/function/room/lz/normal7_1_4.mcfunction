# 구역 건설 (normal7_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 0 204 7 0 206 11 minecraft:andesite
fill 0 204 1 0 207 2 minecraft:cobblestone
fill 0 205 3 0 206 5 minecraft:andesite
fill 0 209 9 0 210 10 minecraft:cherry_leaves[persistent=true]
fill 0 201 10 0 210 10 minecraft:stripped_dark_oak_log
fill 19 210 12 19 210 14 minecraft:cherry_leaves[persistent=true]
fill 19 209 8 19 210 13 minecraft:andesite
fill 19 208 18 19 209 19 minecraft:moss_block
fill 19 206 13 19 208 16 minecraft:andesite
fill 19 209 8 19 210 11 minecraft:cherry_leaves[persistent=true]
fill 8 201 0 8 210 0 minecraft:stripped_dark_oak_log
fill 10 203 0 11 205 0 minecraft:tuff
fill 1 207 0 1 209 0 minecraft:cobblestone
fill 15 203 0 17 203 0 minecraft:cobblestone
fill 9 209 0 14 210 0 minecraft:cherry_leaves[persistent=true]
fill 11 209 19 15 210 19 minecraft:cherry_leaves[persistent=true]
fill 4 209 19 9 210 19 minecraft:tuff
fill 13 203 19 14 203 19 minecraft:calcite
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 3 201 1 3 201 3 minecraft:podzol
fill 6 201 1 7 201 2 minecraft:podzol
fill 1 201 3 2 201 3 minecraft:podzol
fill 7 201 3 18 201 3 minecraft:podzol
fill 2 201 1 2 201 2 minecraft:dirt
fill 2 202 1 2 202 2 minecraft:podzol
fill 8 201 1 18 201 2 minecraft:dirt
fill 8 202 1 18 202 2 minecraft:podzol
fill 1 201 2 1 201 2 minecraft:dirt
fill 1 202 2 1 202 2 minecraft:podzol
fill 1 201 1 1 202 1 minecraft:dirt
fill 1 203 1 1 203 1 minecraft:podzol
fill 18 201 10 18 207 11 minecraft:mossy_stone_bricks
fill 18 208 10 18 208 11 minecraft:podzol
fill 17 201 8 18 207 9 minecraft:stone_bricks
fill 17 208 8 18 208 9 minecraft:podzol
fill 17 201 10 17 207 11 minecraft:stone_bricks
fill 17 208 10 17 208 11 minecraft:podzol
execute positioned 18 201 4 run function rlk:room/prop/i_lantern
execute positioned 13 201 5 run function rlk:room/prop/i_lantern2
execute positioned 15 201 7 run function rlk:room/prop/i_lantern2
execute positioned 6 201 9 run function rlk:room/prop/i_petal
execute positioned 15 201 8 run function rlk:room/prop/i_petal
execute positioned 9 201 17 run function rlk:room/prop/i_grass
execute positioned 15 201 7 run function rlk:room/prop/i_petal
execute positioned 1 201 6 run function rlk:room/prop/i_flower
execute positioned 8 201 17 run function rlk:room/prop/i_petal
execute positioned 13 201 5 run function rlk:room/prop/i_grass
setblock 17 209 8 minecraft:cherry_leaves[persistent=true] keep
setblock 17 209 10 minecraft:short_grass keep
setblock 18 209 9 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 10 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 11 minecraft:short_grass keep
