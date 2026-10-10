# 구역 건설 (first3_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -20 203 4 -20 206 4 minecraft:calcite
fill -20 209 17 -20 210 19 minecraft:calcite
fill -20 210 15 -20 210 17 minecraft:cherry_leaves[persistent=true]
fill -20 210 2 -20 210 5 minecraft:cherry_leaves[persistent=true]
fill -20 209 1 -20 210 1 minecraft:cherry_leaves[persistent=true]
fill -1 203 2 -1 203 7 minecraft:cobblestone
fill -1 202 4 -1 203 4 minecraft:andesite
fill -1 210 6 -1 210 9 minecraft:cherry_leaves[persistent=true]
fill -5 203 0 -4 206 0 minecraft:andesite
fill -12 201 0 -12 210 0 minecraft:stripped_dark_oak_log
fill -8 210 0 -3 210 0 minecraft:cherry_leaves[persistent=true]
fill -3 209 0 -2 210 0 minecraft:cherry_leaves[persistent=true]
fill -8 210 0 -5 210 0 minecraft:moss_block
fill -18 202 0 -17 203 0 minecraft:cobblestone
fill -13 209 19 -11 210 19 minecraft:cherry_leaves[persistent=true]
fill -7 205 19 -3 205 19 minecraft:andesite
fill -14 209 19 -9 210 19 minecraft:cherry_leaves[persistent=true]
fill -2 201 19 -2 210 19 minecraft:stripped_dark_oak_log
fill -10 203 19 -5 206 19 minecraft:cobblestone
fill -16 201 19 -14 201 19 minecraft:cobblestone
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -17 201 7 -15 201 13 minecraft:podzol
fill -18 201 8 -18 201 12 minecraft:podzol
fill -5 201 18 -2 206 18 minecraft:stone_bricks
fill -5 207 18 -2 207 18 minecraft:podzol
execute positioned -17 201 15 run function rlk:room/prop/i_shop
execute positioned -16 202 10 run function rlk:room/prop/i_pillar
execute positioned -8 201 15 run function rlk:room/prop/i_rock
execute positioned -13 201 6 run function rlk:room/prop/i_grass
execute positioned -13 201 7 run function rlk:room/prop/i_petal
execute positioned -17 201 17 run function rlk:room/prop/i_petal
execute positioned -4 201 1 run function rlk:room/prop/i_grass
execute positioned -6 201 10 run function rlk:room/prop/i_grass
execute positioned -17 202 7 run function rlk:room/prop/i_petal
execute positioned -2 201 6 run function rlk:room/prop/i_grass
execute positioned -9 201 11 run function rlk:room/prop/i_petal
execute positioned -4 201 17 run function rlk:room/prop/i_grass
setblock -4 208 18 minecraft:cherry_leaves[persistent=true] keep
setblock -3 208 18 minecraft:short_grass keep
setblock -2 208 18 minecraft:cherry_leaves[persistent=true] keep
