# 구역 건설 (normal18_6, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 7 200 9 11 200 12 minecraft:coarse_dirt
fill 12 200 2 14 200 5 minecraft:packed_mud
fill 0 207 13 0 209 18 minecraft:tuff
fill 0 209 12 0 210 17 minecraft:cherry_leaves[persistent=true]
fill 0 203 17 0 203 19 minecraft:cobblestone
fill 0 207 5 0 208 8 minecraft:moss_block
fill 19 203 11 19 205 11 minecraft:cobblestone
fill 19 209 14 19 210 15 minecraft:cherry_leaves[persistent=true]
fill 19 209 16 19 210 18 minecraft:moss_block
fill 19 209 6 19 210 7 minecraft:cherry_leaves[persistent=true]
fill 12 201 0 12 210 0 minecraft:stripped_dark_oak_log
fill 9 202 0 12 203 0 minecraft:andesite
fill 9 201 0 13 203 0 minecraft:tuff
fill 0 209 0 3 210 0 minecraft:calcite
fill 9 202 19 10 203 19 minecraft:andesite
fill 1 208 19 5 210 19 minecraft:calcite
fill 15 204 19 17 204 19 minecraft:moss_block
fill 2 203 19 4 203 19 minecraft:moss_block
fill 8 208 19 11 210 19 minecraft:moss_block
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 15 201 5 18 201 6 minecraft:podzol
fill 18 201 7 18 201 15 minecraft:podzol
fill 15 201 14 17 201 15 minecraft:podzol
fill 7 201 3 8 205 4 minecraft:stone_bricks
fill 7 206 3 8 206 4 minecraft:podzol
fill 12 201 17 12 206 18 minecraft:mossy_stone_bricks
fill 12 207 17 12 207 18 minecraft:podzol
fill 10 201 17 11 206 18 minecraft:stone_bricks
fill 10 207 17 11 207 18 minecraft:podzol
execute positioned 18 202 6 run function rlk:room/prop/i_torii_z
execute positioned 17 201 11 run function rlk:room/prop/i_petal
execute positioned 7 201 17 run function rlk:room/prop/i_grass
execute positioned 10 201 2 run function rlk:room/prop/i_grass
execute positioned 10 201 12 run function rlk:room/prop/i_grass
execute positioned 1 201 17 run function rlk:room/prop/i_petal
execute positioned 7 201 1 run function rlk:room/prop/i_petal
execute positioned 16 201 10 run function rlk:room/prop/i_petal
setblock 8 207 4 minecraft:cherry_leaves[persistent=true] keep
setblock 11 208 18 minecraft:cherry_leaves[persistent=true] keep
setblock 12 208 17 minecraft:cherry_leaves[persistent=true] keep
setblock 12 208 18 minecraft:short_grass keep
