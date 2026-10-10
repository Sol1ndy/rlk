# 구역 건설 (first7_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:podzol
fill 20 201 0 39 210 19 minecraft:stone
fill 21 201 1 38 210 18 minecraft:air
fill 21 209 1 38 209 18 minecraft:light[level=15]
fill 22 200 7 25 200 10 minecraft:packed_mud
fill 24 200 6 27 200 7 minecraft:gravel
fill 20 210 11 20 210 13 minecraft:andesite
fill 20 205 13 20 207 14 minecraft:andesite
fill 20 204 17 20 206 18 minecraft:moss_block
fill 20 210 2 20 210 3 minecraft:andesite
fill 20 206 9 20 209 13 minecraft:andesite
fill 39 202 9 39 205 13 minecraft:tuff
fill 39 210 2 39 210 3 minecraft:cherry_leaves[persistent=true]
fill 39 208 1 39 210 4 minecraft:moss_block
fill 22 208 0 26 209 0 minecraft:calcite
fill 20 209 0 25 210 0 minecraft:cherry_leaves[persistent=true]
fill 30 204 0 30 206 0 minecraft:calcite
fill 28 206 19 33 206 19 minecraft:cobblestone
fill 29 210 19 32 210 19 minecraft:cherry_leaves[persistent=true]
fill 23 203 19 24 206 19 minecraft:cobblestone
fill 28 206 19 31 208 19 minecraft:andesite
fill 31 201 19 36 202 19 minecraft:andesite
fill 24 209 19 29 210 19 minecraft:andesite
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 38 210 18 minecraft:air
fill 22 201 1 22 201 3 minecraft:podzol
fill 30 201 1 30 201 2 minecraft:podzol
fill 23 201 3 25 201 3 minecraft:podzol
fill 26 201 4 26 201 5 minecraft:podzol
fill 27 201 5 30 201 5 minecraft:podzol
fill 26 201 15 33 201 15 minecraft:podzol
fill 24 201 16 25 201 18 minecraft:podzol
fill 33 201 16 34 201 18 minecraft:podzol
fill 23 201 1 24 201 2 minecraft:dirt
fill 23 202 1 24 202 2 minecraft:podzol
fill 28 201 1 29 201 1 minecraft:dirt
fill 28 202 1 29 202 1 minecraft:podzol
fill 25 201 2 25 201 2 minecraft:dirt
fill 25 202 2 25 202 2 minecraft:podzol
fill 29 201 2 29 201 4 minecraft:dirt
fill 29 202 2 29 202 4 minecraft:podzol
fill 26 201 3 26 201 3 minecraft:dirt
fill 26 202 3 26 202 3 minecraft:podzol
fill 27 201 4 28 201 4 minecraft:dirt
fill 27 202 4 28 202 4 minecraft:podzol
fill 26 201 16 32 201 17 minecraft:dirt
fill 26 202 16 32 202 17 minecraft:podzol
fill 26 201 18 26 201 18 minecraft:dirt
fill 26 202 18 26 202 18 minecraft:podzol
fill 25 201 1 27 202 1 minecraft:dirt
fill 25 203 1 27 203 1 minecraft:podzol
fill 26 201 2 28 202 2 minecraft:dirt
fill 26 203 2 28 203 2 minecraft:podzol
fill 27 201 3 28 202 3 minecraft:dirt
fill 27 203 3 28 203 3 minecraft:podzol
fill 30 201 3 31 207 4 minecraft:mossy_stone_bricks
fill 30 208 3 31 208 4 minecraft:podzol
fill 30 201 18 32 207 18 minecraft:mossy_stone_bricks
fill 30 208 18 32 208 18 minecraft:podzol
fill 27 201 18 29 207 18 minecraft:stone_bricks
fill 27 208 18 29 208 18 minecraft:podzol
execute positioned 28 202 5 run function rlk:room/prop/i_lantern
execute positioned 33 201 11 run function rlk:room/prop/i_grass
execute positioned 31 201 8 run function rlk:room/prop/i_petal
execute positioned 26 204 1 run function rlk:room/prop/i_petal
execute positioned 38 201 10 run function rlk:room/prop/i_grass
execute positioned 28 201 12 run function rlk:room/prop/i_grass
execute positioned 25 201 7 run function rlk:room/prop/i_petal
execute positioned 24 201 15 run function rlk:room/prop/i_grass
execute positioned 33 201 13 run function rlk:room/prop/i_petal
execute positioned 26 201 11 run function rlk:room/prop/i_flower
setblock 29 209 18 minecraft:short_grass keep
setblock 30 209 3 minecraft:cherry_leaves[persistent=true] keep
setblock 30 209 18 minecraft:cherry_leaves[persistent=true] keep
setblock 31 209 3 minecraft:short_grass keep
setblock 31 209 18 minecraft:cherry_leaves[persistent=true] keep
setblock 32 209 18 minecraft:cherry_leaves[persistent=true] keep
