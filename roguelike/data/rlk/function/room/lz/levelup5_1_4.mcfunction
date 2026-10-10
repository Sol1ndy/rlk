# 구역 건설 (levelup5_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -1 minecraft:air
fill -19 209 -19 -2 209 -1 minecraft:light[level=15]
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 0 -2 210 18 minecraft:air
fill -19 209 0 -2 209 18 minecraft:light[level=15]
fill -13 200 1 -9 200 4 minecraft:moss_block
fill -18 200 -16 -17 200 -14 minecraft:coarse_dirt
fill -16 200 13 -13 200 16 minecraft:coarse_dirt
fill -15 200 9 -12 200 10 minecraft:gravel
fill -20 201 -10 -20 203 -9 minecraft:andesite
fill -20 209 -18 -20 210 -14 minecraft:cherry_leaves[persistent=true]
fill -20 204 -6 -20 204 -6 minecraft:tuff
fill -20 203 -18 -20 204 -17 minecraft:tuff
fill -20 209 -10 -20 210 -6 minecraft:cherry_leaves[persistent=true]
fill -1 201 -3 -1 210 -3 minecraft:stripped_dark_oak_log
fill -1 209 -7 -1 210 -2 minecraft:andesite
fill -1 201 -20 -1 203 -15 minecraft:calcite
fill -13 210 -20 -13 210 -20 minecraft:cherry_leaves[persistent=true]
fill -12 206 -20 -9 207 -20 minecraft:tuff
fill -13 210 -20 -12 210 -20 minecraft:cherry_leaves[persistent=true]
fill -9 210 -20 -6 210 -20 minecraft:cherry_leaves[persistent=true]
fill -16 210 -20 -15 210 -20 minecraft:cherry_leaves[persistent=true]
fill -20 201 8 -20 210 8 minecraft:stripped_dark_oak_log
fill -20 209 10 -20 210 14 minecraft:cherry_leaves[persistent=true]
fill -20 209 6 -20 210 11 minecraft:cherry_leaves[persistent=true]
fill -20 201 2 -20 210 2 minecraft:stripped_dark_oak_log
fill -20 209 3 -20 210 5 minecraft:cherry_leaves[persistent=true]
fill -20 209 11 -20 210 16 minecraft:cherry_leaves[persistent=true]
fill -1 204 11 -1 205 13 minecraft:moss_block
fill -1 205 9 -1 205 12 minecraft:calcite
fill -1 204 1 -1 205 2 minecraft:tuff
fill -1 202 15 -1 205 19 minecraft:cobblestone
fill -1 209 9 -1 210 12 minecraft:calcite
fill -14 210 19 -11 210 19 minecraft:cherry_leaves[persistent=true]
fill -20 210 19 -15 210 19 minecraft:cherry_leaves[persistent=true]
fill -18 209 19 -13 210 19 minecraft:tuff
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -1 minecraft:air
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 0 -2 210 18 minecraft:air
fill -7 201 -19 -2 201 -19 minecraft:podzol
fill -7 201 -18 -7 201 -15 minecraft:podzol
fill -8 201 -15 -8 201 -15 minecraft:podzol
fill -6 201 -14 -6 201 -13 minecraft:podzol
fill -5 201 -13 -2 201 -13 minecraft:podzol
fill -5 201 -12 -3 201 -12 minecraft:podzol
fill -5 201 0 -2 201 0 minecraft:podzol
fill -5 201 1 -5 201 4 minecraft:podzol
fill -2 201 1 -2 201 1 minecraft:podzol
fill -9 201 5 -6 201 5 minecraft:podzol
fill -6 201 6 -6 201 13 minecraft:podzol
fill -2 201 9 -2 201 17 minecraft:podzol
fill -5 201 10 -3 201 13 minecraft:podzol
fill -4 201 14 -3 201 18 minecraft:podzol
fill -6 201 -18 -2 201 -15 minecraft:dirt
fill -6 202 -18 -2 202 -15 minecraft:podzol
fill -5 201 -14 -2 201 -14 minecraft:dirt
fill -5 202 -14 -2 202 -14 minecraft:podzol
fill -4 201 1 -3 201 2 minecraft:dirt
fill -4 202 1 -3 202 2 minecraft:podzol
fill -2 201 2 -2 201 2 minecraft:dirt
fill -2 202 2 -2 202 2 minecraft:podzol
fill -4 201 3 -4 201 4 minecraft:dirt
fill -4 202 3 -4 202 4 minecraft:podzol
fill -5 201 5 -5 201 9 minecraft:dirt
fill -5 202 5 -5 202 9 minecraft:podzol
fill -4 201 8 -2 201 8 minecraft:dirt
fill -4 202 8 -2 202 8 minecraft:podzol
fill -4 201 9 -3 201 9 minecraft:dirt
fill -4 202 9 -3 202 9 minecraft:podzol
fill -3 201 3 -2 202 7 minecraft:dirt
fill -3 203 3 -2 203 7 minecraft:podzol
fill -4 201 5 -4 202 7 minecraft:dirt
fill -4 203 5 -4 203 7 minecraft:podzol
fill -19 201 -3 -19 205 -1 minecraft:stone_bricks
fill -19 206 -3 -19 206 -1 minecraft:podzol
fill -17 201 2 -16 205 3 minecraft:stone_bricks
fill -17 206 2 -16 206 3 minecraft:podzol
fill -9 201 -17 -8 207 -16 minecraft:stone_bricks
fill -9 208 -17 -8 208 -16 minecraft:podzol
fill -19 201 9 -19 207 14 minecraft:stone_bricks
fill -19 208 9 -19 208 14 minecraft:podzol
execute positioned -15 201 -11 run function rlk:room/prop/i_house_a_r1
execute positioned -6 202 12 run function rlk:room/prop/i_bamboo
execute positioned -15 201 10 run function rlk:room/prop/i_sakura
execute positioned -15 201 -1 run function rlk:room/prop/i_pillar
execute positioned -13 201 -17 run function rlk:room/prop/i_bamboo
execute positioned -15 201 -16 run function rlk:room/prop/i_pillar
execute positioned -17 201 -8 run function rlk:room/prop/i_flower
execute positioned -18 201 -6 run function rlk:room/prop/i_grass
execute positioned -5 201 17 run function rlk:room/prop/i_petal
execute positioned -3 201 -2 run function rlk:room/prop/i_petal
execute positioned -4 201 -2 run function rlk:room/prop/i_grass
execute positioned -9 201 0 run function rlk:room/prop/i_petal
execute positioned -8 201 -19 run function rlk:room/prop/i_grass
execute positioned -18 201 -18 run function rlk:room/prop/i_petal
execute positioned -11 201 5 run function rlk:room/prop/i_flower
execute positioned -5 201 -9 run function rlk:room/prop/i_petal
execute positioned -6 203 -15 run function rlk:room/prop/i_petal
execute positioned -14 201 16 run function rlk:room/prop/i_petal
execute positioned -4 203 4 run function rlk:room/prop/i_petal
execute positioned -9 201 14 run function rlk:room/prop/i_grass
setblock -19 207 -2 minecraft:short_grass keep
setblock -19 207 -1 minecraft:short_grass keep
setblock -19 209 9 minecraft:cherry_leaves[persistent=true] keep
setblock -19 209 10 minecraft:short_grass keep
setblock -19 209 12 minecraft:cherry_leaves[persistent=true] keep
setblock -19 209 13 minecraft:short_grass keep
setblock -19 209 14 minecraft:cherry_leaves[persistent=true] keep
setblock -17 207 3 minecraft:cherry_leaves[persistent=true] keep
setblock -16 207 2 minecraft:cherry_leaves[persistent=true] keep
setblock -8 209 -17 minecraft:short_grass keep
setblock -8 209 -16 minecraft:short_grass keep
