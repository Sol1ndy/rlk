# 구역 건설 (first0_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 4 200 14 8 200 17 minecraft:packed_mud
fill 0 205 0 0 207 5 minecraft:tuff
fill 0 209 16 0 210 17 minecraft:calcite
fill 0 202 13 0 203 16 minecraft:tuff
fill 0 209 5 0 210 8 minecraft:cherry_leaves[persistent=true]
fill 0 210 2 0 210 7 minecraft:calcite
fill 19 206 12 19 209 15 minecraft:tuff
fill 19 202 7 19 204 12 minecraft:calcite
fill 19 210 9 19 210 11 minecraft:cherry_leaves[persistent=true]
fill 7 204 0 7 207 0 minecraft:calcite
fill 1 206 0 4 209 0 minecraft:tuff
fill 11 205 0 14 208 0 minecraft:moss_block
fill 13 202 0 15 202 0 minecraft:calcite
fill 5 207 0 8 207 0 minecraft:calcite
fill 11 209 19 12 210 19 minecraft:cherry_leaves[persistent=true]
fill 9 208 19 10 210 19 minecraft:calcite
fill 13 210 19 17 210 19 minecraft:cherry_leaves[persistent=true]
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 1 201 16 3 201 16 minecraft:podzol
fill 3 201 17 3 201 18 minecraft:podzol
fill 1 201 17 2 201 18 minecraft:dirt
fill 1 202 17 2 202 18 minecraft:podzol
fill 18 201 2 18 206 3 minecraft:mossy_stone_bricks
fill 18 207 2 18 207 3 minecraft:podzol
fill 16 201 1 18 206 1 minecraft:stone_bricks
fill 16 207 1 18 207 1 minecraft:podzol
fill 16 201 2 17 206 3 minecraft:stone_bricks
fill 16 207 2 17 207 3 minecraft:podzol
fill 12 201 3 12 207 3 minecraft:mossy_stone_bricks
fill 12 208 3 12 208 3 minecraft:podzol
fill 11 201 3 11 207 4 minecraft:stone_bricks
fill 11 208 3 11 208 4 minecraft:podzol
fill 12 201 4 12 207 4 minecraft:stone_bricks
fill 12 208 4 12 208 4 minecraft:podzol
execute positioned 5 201 1 run function rlk:room/prop/i_lantern
execute positioned 1 201 1 run function rlk:room/prop/i_lantern
execute positioned 15 201 7 run function rlk:room/prop/i_sakura_big
execute positioned 16 201 9 run function rlk:room/prop/i_sakura
execute positioned 4 201 3 run function rlk:room/prop/i_sakura
execute positioned 3 202 18 run function rlk:room/prop/i_flower
execute positioned 7 201 14 run function rlk:room/prop/i_grass
execute positioned 1 201 2 run function rlk:room/prop/i_petal
execute positioned 16 201 7 run function rlk:room/prop/i_petal
execute positioned 2 202 16 run function rlk:room/prop/i_flower
execute positioned 11 201 15 run function rlk:room/prop/i_grass
execute positioned 6 201 5 run function rlk:room/prop/i_grass
execute positioned 8 201 2 run function rlk:room/prop/i_petal
execute positioned 14 201 9 run function rlk:room/prop/i_petal
setblock 11 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock 12 209 3 minecraft:cherry_leaves[persistent=true] keep
setblock 16 208 2 minecraft:cherry_leaves[persistent=true] keep
setblock 17 208 1 minecraft:short_grass keep
setblock 17 208 2 minecraft:short_grass keep
setblock 18 208 1 minecraft:short_grass keep
setblock 18 208 3 minecraft:cherry_leaves[persistent=true] keep
