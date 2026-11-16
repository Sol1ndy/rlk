# 구역 건설 (first11_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 20 19 200 39 minecraft:podzol
fill 0 201 20 19 210 39 minecraft:stone
fill 1 201 21 18 210 38 minecraft:air
fill 1 209 21 18 209 38 minecraft:light[level=15]
fill 5 200 31 8 200 33 minecraft:packed_mud
fill 6 200 31 8 200 32 minecraft:gravel
fill 0 210 25 0 210 30 minecraft:cherry_leaves[persistent=true]
fill 0 201 25 0 202 27 minecraft:calcite
fill 19 207 20 19 210 20 minecraft:calcite
fill 19 203 23 19 204 25 minecraft:tuff
fill 19 210 36 19 210 37 minecraft:calcite
fill 8 203 20 9 206 20 minecraft:moss_block
fill 3 201 20 3 202 20 minecraft:cobblestone
fill 5 209 20 8 210 20 minecraft:cherry_leaves[persistent=true]
fill 11 204 20 14 206 20 minecraft:calcite
fill 12 201 20 12 210 20 minecraft:stripped_dark_oak_log
fill 2 209 39 6 210 39 minecraft:cherry_leaves[persistent=true]
fill 6 206 39 11 209 39 minecraft:moss_block
fill 2 202 39 4 202 39 minecraft:andesite
fill 7 201 39 7 210 39 minecraft:stripped_dark_oak_log
fill 2 203 39 3 205 39 minecraft:calcite
fill 0 210 20 19 210 39 minecraft:polished_deepslate
fill 1 210 21 18 210 38 minecraft:air
fill 6 201 35 13 201 35 minecraft:podzol
fill 6 201 36 6 201 38 minecraft:podzol
fill 13 201 36 13 201 36 minecraft:podzol
fill 5 201 37 5 201 37 minecraft:podzol
fill 14 201 37 14 201 38 minecraft:podzol
fill 7 201 36 12 201 38 minecraft:dirt
fill 7 202 36 12 202 38 minecraft:podzol
fill 13 201 37 13 201 38 minecraft:dirt
fill 13 202 37 13 202 38 minecraft:podzol
fill 1 201 30 1 205 31 minecraft:mossy_stone_bricks
fill 1 206 30 1 206 31 minecraft:podzol
fill 1 201 26 1 205 29 minecraft:stone_bricks
fill 1 206 26 1 206 29 minecraft:podzol
execute positioned 5 201 35 run function rlk:room/prop/i_lantern
execute positioned 3 201 24 run function rlk:room/prop/i_lantern
execute positioned 4 201 31 run function rlk:room/prop/i_sakura
execute positioned 4 201 28 run function rlk:room/prop/i_lantern
execute positioned 3 201 29 run function rlk:room/prop/i_grass
execute positioned 6 201 26 run function rlk:room/prop/i_petal
execute positioned 6 201 27 run function rlk:room/prop/i_grass
execute positioned 12 201 27 run function rlk:room/prop/i_flower
execute positioned 17 201 23 run function rlk:room/prop/i_flower
execute positioned 7 201 23 run function rlk:room/prop/i_petal
execute positioned 6 201 29 run function rlk:room/prop/i_petal
execute positioned 2 201 29 run function rlk:room/prop/i_grass
execute positioned 2 201 25 run function rlk:room/prop/i_grass
execute positioned 6 201 25 run function rlk:room/prop/i_petal
setblock 1 207 26 minecraft:cherry_leaves[persistent=true] keep
setblock 1 207 28 minecraft:short_grass keep
setblock 1 207 30 minecraft:short_grass keep
setblock 1 207 31 minecraft:cherry_leaves[persistent=true] keep
