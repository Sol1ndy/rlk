# 구역 건설 (boss6_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 15 200 14 17 200 17 minecraft:gravel
fill 2 200 6 3 200 8 minecraft:gravel
fill 12 200 2 14 200 4 minecraft:coarse_dirt
fill 0 210 16 0 210 18 minecraft:andesite
fill 0 202 8 0 202 13 minecraft:andesite
fill 0 210 9 0 210 11 minecraft:tuff
fill 0 203 13 0 205 15 minecraft:andesite
fill 19 204 9 19 207 9 minecraft:moss_block
fill 19 210 5 19 210 5 minecraft:cherry_leaves[persistent=true]
fill 19 209 9 19 210 9 minecraft:cherry_leaves[persistent=true]
fill 19 202 7 19 204 12 minecraft:calcite
fill 0 201 0 3 202 0 minecraft:andesite
fill 3 210 0 3 210 0 minecraft:cherry_leaves[persistent=true]
fill 1 203 0 6 206 0 minecraft:calcite
fill 16 209 0 18 210 0 minecraft:cherry_leaves[persistent=true]
fill 11 202 19 14 205 19 minecraft:tuff
fill 0 209 19 4 210 19 minecraft:cherry_leaves[persistent=true]
fill 4 208 19 7 209 19 minecraft:tuff
fill 13 209 19 14 210 19 minecraft:cherry_leaves[persistent=true]
fill 2 210 19 5 210 19 minecraft:cherry_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 16 201 1 18 201 10 minecraft:podzol
fill 15 201 6 15 201 12 minecraft:podzol
fill 16 201 11 16 201 13 minecraft:podzol
fill 18 201 11 18 206 13 minecraft:mossy_stone_bricks
fill 18 207 11 18 207 13 minecraft:podzol
fill 17 201 12 17 206 13 minecraft:mossy_stone_bricks
fill 17 207 12 17 207 13 minecraft:podzol
fill 17 201 11 17 206 11 minecraft:stone_bricks
fill 17 207 11 17 207 11 minecraft:podzol
fill 3 201 13 4 207 14 minecraft:stone_bricks
fill 3 208 13 4 208 14 minecraft:podzol
execute positioned 6 201 15 run function rlk:room/prop/i_shop
execute positioned 3 201 9 run function rlk:room/prop/i_rock
execute positioned 13 201 8 run function rlk:room/prop/i_grass
execute positioned 14 201 13 run function rlk:room/prop/i_petal
execute positioned 18 201 14 run function rlk:room/prop/i_petal
execute positioned 18 202 4 run function rlk:room/prop/i_grass
execute positioned 14 201 8 run function rlk:room/prop/i_petal
execute positioned 9 201 6 run function rlk:room/prop/i_grass
execute positioned 6 201 6 run function rlk:room/prop/i_petal
execute positioned 16 202 1 run function rlk:room/prop/i_petal
execute positioned 13 201 16 run function rlk:room/prop/i_grass
setblock 3 209 13 minecraft:cherry_leaves[persistent=true] keep
setblock 4 209 14 minecraft:cherry_leaves[persistent=true] keep
setblock 17 208 12 minecraft:cherry_leaves[persistent=true] keep
setblock 18 208 11 minecraft:cherry_leaves[persistent=true] keep
