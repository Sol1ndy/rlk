# 구역 건설 (levelup7_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -1 minecraft:air
fill 1 209 -19 18 209 -1 minecraft:light[level=15]
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 0 18 210 18 minecraft:air
fill 1 209 0 18 209 18 minecraft:light[level=15]
fill 8 200 -16 11 200 -15 minecraft:gravel
fill 12 200 -11 16 200 -10 minecraft:moss_block
fill 7 200 -14 11 200 -11 minecraft:moss_block
fill 10 200 -10 14 200 -7 minecraft:coarse_dirt
fill 0 207 -16 0 210 -15 minecraft:moss_block
fill 0 203 -14 0 204 -11 minecraft:andesite
fill 0 210 -14 0 210 -9 minecraft:cherry_leaves[persistent=true]
fill 0 206 -20 0 208 -16 minecraft:andesite
fill 0 207 -20 0 209 -19 minecraft:tuff
fill 19 201 -13 19 210 -13 minecraft:stripped_dark_oak_log
fill 19 202 -6 19 204 -6 minecraft:andesite
fill 19 201 -7 19 210 -7 minecraft:stripped_dark_oak_log
fill 6 201 -20 6 210 -20 minecraft:stripped_dark_oak_log
fill 8 206 -20 12 209 -20 minecraft:andesite
fill 4 208 -20 7 209 -20 minecraft:moss_block
fill 7 202 -20 12 204 -20 minecraft:andesite
fill 0 209 -20 2 210 -20 minecraft:cherry_leaves[persistent=true]
fill 0 206 13 0 209 16 minecraft:tuff
fill 0 209 6 0 210 10 minecraft:andesite
fill 0 210 11 0 210 14 minecraft:cherry_leaves[persistent=true]
fill 0 210 8 0 210 9 minecraft:cherry_leaves[persistent=true]
fill 0 209 4 0 210 6 minecraft:andesite
fill 19 205 8 19 207 10 minecraft:tuff
fill 19 201 11 19 204 15 minecraft:moss_block
fill 19 210 4 19 210 9 minecraft:cherry_leaves[persistent=true]
fill 19 209 19 19 210 19 minecraft:calcite
fill 13 201 19 13 210 19 minecraft:stripped_dark_oak_log
fill 12 209 19 15 210 19 minecraft:cherry_leaves[persistent=true]
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -1 minecraft:air
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 0 18 210 18 minecraft:air
fill 5 201 -19 6 201 -19 minecraft:podzol
fill 6 201 -18 7 201 -16 minecraft:podzol
fill 5 201 -15 6 201 -15 minecraft:podzol
fill 4 201 -14 5 201 -13 minecraft:podzol
fill 3 201 -13 3 201 -12 minecraft:podzol
fill 1 201 -12 2 201 -11 minecraft:podzol
fill 4 201 -12 4 201 -12 minecraft:podzol
fill 15 201 3 17 201 11 minecraft:podzol
fill 18 201 4 18 201 11 minecraft:podzol
fill 11 201 5 14 201 5 minecraft:podzol
fill 14 201 6 14 201 11 minecraft:podzol
fill 1 201 -19 4 201 -15 minecraft:dirt
fill 1 202 -19 4 202 -15 minecraft:podzol
fill 5 201 -18 5 201 -16 minecraft:dirt
fill 5 202 -18 5 202 -16 minecraft:podzol
fill 1 201 -14 3 201 -14 minecraft:dirt
fill 1 202 -14 3 202 -14 minecraft:podzol
fill 1 201 -13 2 201 -13 minecraft:dirt
fill 1 202 -13 2 202 -13 minecraft:podzol
fill 3 201 -8 4 206 -7 minecraft:stone_bricks
fill 3 207 -8 4 207 -7 minecraft:podzol
fill 1 201 8 2 207 9 minecraft:mossy_stone_bricks
fill 1 208 8 2 208 9 minecraft:podzol
fill 1 201 -3 2 207 1 minecraft:stone_bricks
fill 1 208 -3 2 208 1 minecraft:podzol
fill 1 201 4 3 207 7 minecraft:stone_bricks
fill 1 208 4 3 208 7 minecraft:podzol
fill 3 201 8 3 207 9 minecraft:stone_bricks
fill 3 208 8 3 208 9 minecraft:podzol
execute positioned 16 202 6 run function rlk:room/prop/i_fence_z
execute positioned 16 201 0 run function rlk:room/prop/i_lantern2
execute positioned 4 203 -16 run function rlk:room/prop/i_lantern
execute positioned 7 201 5 run function rlk:room/prop/i_pillar
execute positioned 1 203 -14 run function rlk:room/prop/i_pillar
execute positioned 11 201 -17 run function rlk:room/prop/i_petal
execute positioned 15 201 -13 run function rlk:room/prop/i_flower
execute positioned 5 202 -14 run function rlk:room/prop/i_flower
execute positioned 13 201 7 run function rlk:room/prop/i_flower
execute positioned 5 201 18 run function rlk:room/prop/i_grass
execute positioned 17 202 11 run function rlk:room/prop/i_petal
execute positioned 14 201 1 run function rlk:room/prop/i_grass
execute positioned 12 201 -13 run function rlk:room/prop/i_petal
execute positioned 5 201 3 run function rlk:room/prop/i_petal
execute positioned 4 201 9 run function rlk:room/prop/i_petal
execute positioned 11 201 -7 run function rlk:room/prop/i_petal
execute positioned 15 202 10 run function rlk:room/prop/i_flower
execute positioned 5 201 2 run function rlk:room/prop/i_flower
execute positioned 4 201 -4 run function rlk:room/prop/i_flower
setblock 1 209 -2 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 -1 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 0 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 6 minecraft:short_grass keep
setblock 1 209 7 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 9 minecraft:cherry_leaves[persistent=true] keep
setblock 2 209 -3 minecraft:short_grass keep
setblock 2 209 -2 minecraft:short_grass keep
setblock 2 209 -1 minecraft:cherry_leaves[persistent=true] keep
setblock 2 209 1 minecraft:cherry_leaves[persistent=true] keep
setblock 2 209 4 minecraft:cherry_leaves[persistent=true] keep
setblock 2 209 9 minecraft:cherry_leaves[persistent=true] keep
setblock 3 208 -8 minecraft:cherry_leaves[persistent=true] keep
setblock 3 209 4 minecraft:short_grass keep
setblock 3 209 5 minecraft:cherry_leaves[persistent=true] keep
setblock 3 209 8 minecraft:short_grass keep
setblock 3 209 9 minecraft:cherry_leaves[persistent=true] keep
setblock 4 208 -8 minecraft:short_grass keep
