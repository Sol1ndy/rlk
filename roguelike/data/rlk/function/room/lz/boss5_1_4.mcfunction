# 구역 건설 (boss5_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -7 200 6 -4 200 8 minecraft:coarse_dirt
fill -20 202 1 -20 205 1 minecraft:calcite
fill -20 201 3 -20 210 3 minecraft:stripped_dark_oak_log
fill -20 209 10 -20 209 11 minecraft:calcite
fill -1 210 13 -1 210 13 minecraft:cherry_leaves[persistent=true]
fill -1 201 13 -1 210 13 minecraft:stripped_dark_oak_log
fill -1 210 13 -1 210 17 minecraft:cherry_leaves[persistent=true]
fill -1 203 5 -1 203 10 minecraft:andesite
fill -1 201 0 -1 210 0 minecraft:stripped_dark_oak_log
fill -1 209 4 -1 210 8 minecraft:andesite
fill -12 204 0 -8 206 0 minecraft:tuff
fill -3 205 0 -2 207 0 minecraft:moss_block
fill -7 210 0 -4 210 0 minecraft:cherry_leaves[persistent=true]
fill -3 201 19 -3 210 19 minecraft:stripped_dark_oak_log
fill -2 208 19 -1 209 19 minecraft:tuff
fill -18 201 19 -18 204 19 minecraft:calcite
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -4 201 11 -2 201 12 minecraft:podzol
fill -5 201 12 -5 201 14 minecraft:podzol
fill -7 201 15 -6 201 16 minecraft:podzol
fill -6 201 17 -5 201 18 minecraft:podzol
fill -4 201 18 -2 201 18 minecraft:podzol
fill -4 201 13 -2 201 17 minecraft:dirt
fill -4 202 13 -2 202 17 minecraft:podzol
fill -5 201 15 -5 201 16 minecraft:dirt
fill -5 202 15 -5 202 16 minecraft:podzol
fill -3 201 6 -2 205 7 minecraft:mossy_stone_bricks
fill -3 206 6 -2 206 7 minecraft:podzol
fill -3 201 3 -2 205 5 minecraft:stone_bricks
fill -3 206 3 -2 206 5 minecraft:podzol
execute positioned -10 201 5 run function rlk:room/prop/i_house_a_r2
execute positioned -19 201 1 run function rlk:room/prop/i_rock
execute positioned -4 201 3 run function rlk:room/prop/i_grass
execute positioned -10 201 16 run function rlk:room/prop/i_flower
execute positioned -14 201 11 run function rlk:room/prop/i_grass
execute positioned -6 201 4 run function rlk:room/prop/i_flower
execute positioned -15 201 4 run function rlk:room/prop/i_grass
execute positioned -16 201 15 run function rlk:room/prop/i_petal
execute positioned -11 201 5 run function rlk:room/prop/i_petal
setblock -3 207 4 minecraft:short_grass keep
setblock -3 207 5 minecraft:cherry_leaves[persistent=true] keep
setblock -3 207 6 minecraft:short_grass keep
setblock -2 207 3 minecraft:short_grass keep
setblock -2 207 6 minecraft:cherry_leaves[persistent=true] keep
setblock -2 207 7 minecraft:short_grass keep
