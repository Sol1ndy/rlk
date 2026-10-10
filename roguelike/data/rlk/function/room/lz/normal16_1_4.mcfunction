# 구역 건설 (normal16_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 13 200 10 16 200 12 minecraft:moss_block
fill 1 200 17 3 200 18 minecraft:moss_block
fill 0 209 4 0 210 5 minecraft:cobblestone
fill 0 209 2 0 210 4 minecraft:cherry_leaves[persistent=true]
fill 0 208 11 0 209 16 minecraft:andesite
fill 19 210 16 19 210 16 minecraft:cherry_leaves[persistent=true]
fill 19 201 6 19 210 6 minecraft:stripped_dark_oak_log
fill 19 209 8 19 210 9 minecraft:cherry_leaves[persistent=true]
fill 19 201 2 19 202 3 minecraft:moss_block
fill 19 210 3 19 210 4 minecraft:cherry_leaves[persistent=true]
fill 19 210 3 19 210 8 minecraft:cherry_leaves[persistent=true]
fill 9 209 0 10 210 0 minecraft:cherry_leaves[persistent=true]
fill 2 210 0 7 210 0 minecraft:tuff
fill 7 201 0 7 210 0 minecraft:stripped_dark_oak_log
fill 18 203 0 18 204 0 minecraft:andesite
fill 14 205 0 14 208 0 minecraft:tuff
fill 4 208 19 7 210 19 minecraft:tuff
fill 14 210 19 17 210 19 minecraft:cobblestone
fill 5 209 19 6 210 19 minecraft:cherry_leaves[persistent=true]
fill 0 206 19 0 209 19 minecraft:tuff
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 13 201 1 14 201 5 minecraft:podzol
fill 1 201 4 4 201 5 minecraft:podzol
fill 4 201 6 5 201 13 minecraft:podzol
fill 15 201 6 18 201 6 minecraft:podzol
fill 15 201 7 16 201 7 minecraft:podzol
fill 1 201 14 4 201 14 minecraft:podzol
fill 1 201 15 3 201 15 minecraft:podzol
fill 7 201 15 18 201 16 minecraft:podzol
fill 6 201 16 6 201 18 minecraft:podzol
fill 15 201 1 18 201 5 minecraft:dirt
fill 15 202 1 18 202 5 minecraft:podzol
fill 1 201 6 3 201 13 minecraft:dirt
fill 1 202 6 3 202 13 minecraft:podzol
fill 7 201 17 18 201 18 minecraft:dirt
fill 7 202 17 18 202 18 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:mossy_stone_bricks
fill 12 208 3 12 208 3 minecraft:podzol
fill 18 201 10 18 207 10 minecraft:mossy_stone_bricks
fill 18 208 10 18 208 10 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:stone_bricks
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:stone_bricks
fill 12 208 4 12 208 4 minecraft:podzol
fill 17 201 7 18 207 9 minecraft:stone_bricks
fill 17 208 7 18 208 9 minecraft:podzol
fill 17 201 10 17 207 10 minecraft:stone_bricks
fill 17 208 10 17 208 10 minecraft:podzol
execute positioned 18 203 1 run function rlk:room/prop/i_lantern
execute positioned 1 201 1 run function rlk:room/prop/i_rock
execute positioned 6 201 14 run function rlk:room/prop/i_flower
execute positioned 17 203 2 run function rlk:room/prop/i_flower
execute positioned 12 201 6 run function rlk:room/prop/i_grass
execute positioned 7 201 8 run function rlk:room/prop/i_flower
execute positioned 11 201 1 run function rlk:room/prop/i_grass
execute positioned 11 203 17 run function rlk:room/prop/i_grass
execute positioned 18 203 18 run function rlk:room/prop/i_petal
setblock 11 209 4 minecraft:short_grass keep
setblock 12 209 3 minecraft:cherry_leaves[persistent=true] keep
setblock 12 209 4 minecraft:short_grass keep
setblock 17 209 7 minecraft:cherry_leaves[persistent=true] keep
setblock 17 209 8 minecraft:cherry_leaves[persistent=true] keep
setblock 17 209 10 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 7 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 9 minecraft:short_grass keep
setblock 18 209 10 minecraft:short_grass keep
