# 구역 건설 (root1_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -1 210 18 minecraft:air
fill -19 209 1 -1 209 18 minecraft:light[level=15]
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 0 201 1 18 210 18 minecraft:air
fill 0 209 1 18 209 18 minecraft:light[level=15]
fill -2 200 10 1 200 11 minecraft:coarse_dirt
fill 14 200 7 15 200 9 minecraft:packed_mud
fill 7 200 12 9 200 14 minecraft:packed_mud
fill -20 209 12 -20 210 13 minecraft:tuff
fill -20 201 8 -20 202 11 minecraft:tuff
fill -20 202 6 -20 202 10 minecraft:moss_block
fill -20 210 14 -20 210 15 minecraft:calcite
fill -20 201 13 -20 210 13 minecraft:stripped_dark_oak_log
fill -19 209 0 -19 210 0 minecraft:moss_block
fill -20 207 0 -15 210 0 minecraft:andesite
fill -9 210 0 -7 210 0 minecraft:cherry_leaves[persistent=true]
fill -17 210 19 -15 210 19 minecraft:moss_block
fill -15 210 19 -14 210 19 minecraft:cherry_leaves[persistent=true]
fill -11 210 19 -7 210 19 minecraft:cherry_leaves[persistent=true]
fill 19 206 1 19 206 4 minecraft:cobblestone
fill 19 201 3 19 203 6 minecraft:tuff
fill 19 203 3 19 203 3 minecraft:andesite
fill 19 206 2 19 207 2 minecraft:andesite
fill 19 201 9 19 210 9 minecraft:stripped_dark_oak_log
fill 19 204 11 19 205 14 minecraft:cobblestone
fill 4 205 0 4 208 0 minecraft:andesite
fill 4 201 0 4 210 0 minecraft:stripped_dark_oak_log
fill 14 209 0 18 210 0 minecraft:cherry_leaves[persistent=true]
fill 9 209 0 9 210 0 minecraft:moss_block
fill 4 209 0 4 210 0 minecraft:cherry_leaves[persistent=true]
fill 13 210 19 17 210 19 minecraft:cherry_leaves[persistent=true]
fill 12 210 19 17 210 19 minecraft:cherry_leaves[persistent=true]
fill 15 209 19 19 210 19 minecraft:tuff
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -1 210 18 minecraft:air
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 0 210 1 18 210 18 minecraft:air
fill -3 201 3 -2 201 3 minecraft:podzol
fill -10 201 4 -8 201 5 minecraft:podzol
fill -2 201 4 -1 201 5 minecraft:podzol
fill -7 201 5 -7 201 5 minecraft:podzol
fill -4 201 5 -3 201 5 minecraft:podzol
fill 0 201 5 0 201 5 minecraft:podzol
fill -6 201 6 -5 201 13 minecraft:podzol
fill 16 201 13 18 201 18 minecraft:podzol
fill -9 201 14 -7 201 14 minecraft:podzol
fill -5 201 14 -5 201 15 minecraft:podzol
fill 15 201 14 15 201 18 minecraft:podzol
fill -8 201 15 -6 201 15 minecraft:podzol
fill -4 201 15 -2 201 15 minecraft:podzol
fill 14 201 15 14 201 17 minecraft:podzol
fill -7 201 4 -3 201 4 minecraft:dirt
fill -7 202 4 -3 202 4 minecraft:podzol
fill -6 201 5 -5 201 5 minecraft:dirt
fill -6 202 5 -5 202 5 minecraft:podzol
fill -6 201 14 -6 201 14 minecraft:dirt
fill -6 202 14 -6 202 14 minecraft:podzol
fill 9 201 3 10 206 4 minecraft:stone_bricks
fill 9 207 3 10 207 4 minecraft:podzol
fill -9 201 1 -4 207 1 minecraft:mossy_stone_bricks
fill -9 208 1 -4 208 1 minecraft:podzol
fill -9 201 2 -4 207 3 minecraft:stone_bricks
fill -9 208 2 -4 208 3 minecraft:podzol
fill 4 201 3 5 207 4 minecraft:stone_bricks
fill 4 208 3 5 208 4 minecraft:podzol
execute positioned 7 201 14 run function rlk:room/prop/i_house_b
execute positioned 14 201 11 run function rlk:room/prop/i_pillar
execute positioned -14 201 5 run function rlk:room/prop/i_fence_x
execute positioned 4 201 16 run function rlk:room/prop/i_sakura
execute positioned 16 201 3 run function rlk:room/prop/i_wall_z
execute positioned 5 201 11 run function rlk:room/prop/i_lantern2
execute positioned 2 201 9 run function rlk:room/prop/i_petal
execute positioned -18 201 4 run function rlk:room/prop/i_grass
execute positioned 11 201 16 run function rlk:room/prop/i_petal
execute positioned -3 201 18 run function rlk:room/prop/i_petal
execute positioned -10 201 7 run function rlk:room/prop/i_flower
execute positioned -6 202 8 run function rlk:room/prop/i_petal
execute positioned -15 201 10 run function rlk:room/prop/i_petal
execute positioned 18 201 12 run function rlk:room/prop/i_flower
execute positioned 13 201 5 run function rlk:room/prop/i_petal
execute positioned 7 201 3 run function rlk:room/prop/i_grass
execute positioned -5 202 12 run function rlk:room/prop/i_flower
execute positioned 12 201 14 run function rlk:room/prop/i_flower
execute positioned 17 201 3 run function rlk:room/prop/i_grass
execute positioned -2 201 1 run function rlk:room/prop/i_grass
execute positioned 11 201 14 run function rlk:room/prop/i_flower
execute positioned -4 202 5 run function rlk:room/prop/i_petal
setblock -9 209 2 minecraft:cherry_leaves[persistent=true] keep
setblock -9 209 3 minecraft:cherry_leaves[persistent=true] keep
setblock -8 209 2 minecraft:cherry_leaves[persistent=true] keep
setblock -7 209 3 minecraft:cherry_leaves[persistent=true] keep
setblock -6 209 1 minecraft:short_grass keep
setblock -6 209 2 minecraft:cherry_leaves[persistent=true] keep
setblock -5 209 2 minecraft:cherry_leaves[persistent=true] keep
setblock -5 209 3 minecraft:short_grass keep
setblock -4 209 1 minecraft:short_grass keep
setblock -4 209 2 minecraft:cherry_leaves[persistent=true] keep
setblock -4 209 3 minecraft:short_grass keep
setblock 4 209 4 minecraft:short_grass keep
setblock 5 209 3 minecraft:cherry_leaves[persistent=true] keep
setblock 9 208 3 minecraft:cherry_leaves[persistent=true] keep
setblock 9 208 4 minecraft:cherry_leaves[persistent=true] keep
setblock 10 208 4 minecraft:cherry_leaves[persistent=true] keep
