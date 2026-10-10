# 구역 건설 (normal13_3, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 1 201 -39 18 210 -22 minecraft:air
fill 1 209 -39 18 209 -22 minecraft:light[level=15]
fill 11 200 -24 13 200 -23 minecraft:gravel
fill 0 210 -29 0 210 -26 minecraft:tuff
fill 0 209 -27 0 210 -24 minecraft:tuff
fill 0 203 -34 0 204 -30 minecraft:moss_block
fill 0 210 -27 0 210 -24 minecraft:cherry_leaves[persistent=true]
fill 0 201 -31 0 204 -27 minecraft:calcite
fill 19 202 -29 19 204 -28 minecraft:andesite
fill 19 201 -27 19 201 -23 minecraft:cobblestone
fill 19 209 -32 19 210 -31 minecraft:cherry_leaves[persistent=true]
fill 19 203 -34 19 206 -29 minecraft:cobblestone
fill 19 210 -39 19 210 -37 minecraft:cherry_leaves[persistent=true]
fill 11 209 -40 11 210 -40 minecraft:cherry_leaves[persistent=true]
fill 0 201 -40 0 210 -40 minecraft:stripped_dark_oak_log
fill 12 204 -40 14 207 -40 minecraft:calcite
fill 11 209 -40 15 209 -40 minecraft:cobblestone
fill 6 201 -21 6 210 -21 minecraft:stripped_dark_oak_log
fill 8 201 -21 8 210 -21 minecraft:stripped_dark_oak_log
fill 6 209 -21 10 210 -21 minecraft:cherry_leaves[persistent=true]
fill 12 210 -21 12 210 -21 minecraft:cherry_leaves[persistent=true]
fill 13 201 -21 13 210 -21 minecraft:stripped_dark_oak_log
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 1 210 -39 18 210 -22 minecraft:air
fill 5 201 -39 6 201 -38 minecraft:podzol
fill 6 201 -37 18 201 -37 minecraft:podzol
fill 7 201 -36 18 201 -36 minecraft:podzol
fill 15 201 -33 18 201 -32 minecraft:podzol
fill 15 201 -31 17 201 -31 minecraft:podzol
fill 15 201 -30 16 201 -30 minecraft:podzol
fill 15 201 -29 15 201 -27 minecraft:podzol
fill 16 201 -26 16 201 -22 minecraft:podzol
fill 18 201 -22 18 201 -22 minecraft:podzol
fill 7 201 -39 18 201 -38 minecraft:dirt
fill 7 202 -39 18 202 -38 minecraft:podzol
fill 17 201 -30 17 201 -22 minecraft:dirt
fill 17 202 -30 17 202 -22 minecraft:podzol
fill 16 201 -29 16 201 -27 minecraft:dirt
fill 16 202 -29 16 202 -27 minecraft:podzol
fill 18 201 -25 18 201 -23 minecraft:dirt
fill 18 202 -25 18 202 -23 minecraft:podzol
fill 18 201 -28 18 207 -27 minecraft:mossy_stone_bricks
fill 18 208 -28 18 208 -27 minecraft:podzol
fill 18 201 -31 18 207 -29 minecraft:stone_bricks
fill 18 208 -31 18 208 -29 minecraft:podzol
fill 18 201 -26 18 207 -26 minecraft:stone_bricks
fill 18 208 -26 18 208 -26 minecraft:podzol
execute positioned 15 202 -33 run function rlk:room/prop/i_bamboo
execute positioned 1 201 -39 run function rlk:room/prop/i_lantern
execute positioned 1 201 -29 run function rlk:room/prop/i_flower
execute positioned 16 202 -31 run function rlk:room/prop/i_grass
execute positioned 15 203 -39 run function rlk:room/prop/i_grass
execute positioned 17 203 -22 run function rlk:room/prop/i_petal
execute positioned 17 201 -35 run function rlk:room/prop/i_petal
execute positioned 10 201 -31 run function rlk:room/prop/i_petal
execute positioned 6 202 -39 run function rlk:room/prop/i_petal
setblock 18 209 -31 minecraft:short_grass keep
setblock 18 209 -30 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 -29 minecraft:short_grass keep
setblock 18 209 -28 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 -27 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 -26 minecraft:short_grass keep
