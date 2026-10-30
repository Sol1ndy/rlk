# 구역 건설 (normal28_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill 14 200 -15 15 200 -14 minecraft:gravel
fill 12 200 -14 13 200 -13 minecraft:packed_mud
fill -1 200 -15 0 200 -14 minecraft:coarse_dirt
fill -11 200 -17 -10 200 -14 minecraft:packed_mud
fill -2 200 -14 1 200 -11 minecraft:packed_mud
fill -14 200 -9 -11 200 -7 minecraft:gravel
fill -20 209 -9 -20 210 -8 minecraft:cherry_leaves[persistent=true]
fill -20 203 -20 -20 206 -19 minecraft:moss_block
fill -20 207 -10 -20 209 -9 minecraft:calcite
fill -6 201 -20 -5 201 -20 minecraft:cobblestone
fill -15 203 -20 -10 206 -20 minecraft:cobblestone
fill -20 207 -20 -15 210 -20 minecraft:andesite
fill -7 209 -1 -6 210 -1 minecraft:cherry_leaves[persistent=true]
fill -17 209 -1 -16 210 -1 minecraft:cherry_leaves[persistent=true]
fill -3 206 -1 -1 208 -1 minecraft:moss_block
fill -4 201 -1 -4 203 -1 minecraft:tuff
fill -7 204 -1 -6 206 -1 minecraft:tuff
fill -8 209 -1 -3 210 -1 minecraft:cherry_leaves[persistent=true]
fill 19 202 -14 19 202 -12 minecraft:tuff
fill 19 201 -13 19 204 -9 minecraft:calcite
fill 19 201 -18 19 210 -18 minecraft:stripped_dark_oak_log
fill 19 210 -13 19 210 -9 minecraft:cherry_leaves[persistent=true]
fill 19 203 -4 19 204 -1 minecraft:moss_block
fill 19 201 -9 19 210 -9 minecraft:stripped_dark_oak_log
fill 9 209 -20 13 210 -20 minecraft:cherry_leaves[persistent=true]
fill 9 208 -20 12 209 -20 minecraft:cobblestone
fill 0 210 -20 3 210 -20 minecraft:cherry_leaves[persistent=true]
fill 10 209 -20 11 210 -20 minecraft:cherry_leaves[persistent=true]
fill 10 210 -1 13 210 -1 minecraft:andesite
fill 11 201 -1 11 210 -1 minecraft:stripped_dark_oak_log
fill 7 207 -1 12 208 -1 minecraft:tuff
fill 1 209 -1 5 210 -1 minecraft:cherry_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill -17 201 -19 -17 201 -15 minecraft:podzol
fill -16 201 -14 -15 201 -14 minecraft:podzol
fill -19 201 -13 -16 201 -13 minecraft:podzol
fill -19 201 -8 -18 201 -7 minecraft:podzol
fill -17 201 -7 -17 201 -2 minecraft:podzol
fill 5 201 -7 5 201 -7 minecraft:podzol
fill -1 201 -5 3 201 -5 minecraft:podzol
fill -2 201 -4 -1 201 -2 minecraft:podzol
fill 3 201 -4 3 201 -2 minecraft:podzol
fill -19 201 -19 -18 201 -14 minecraft:dirt
fill -19 202 -19 -18 202 -14 minecraft:podzol
fill -17 201 -14 -17 201 -14 minecraft:dirt
fill -17 202 -14 -17 202 -14 minecraft:podzol
fill -19 201 -6 -18 201 -2 minecraft:dirt
fill -19 202 -6 -18 202 -2 minecraft:podzol
fill 0 201 -4 2 201 -2 minecraft:dirt
fill 0 202 -4 2 202 -2 minecraft:podzol
fill -10 201 -12 -9 205 -11 minecraft:stone_bricks
fill -10 206 -12 -9 206 -11 minecraft:podzol
fill -11 201 -11 -11 205 -10 minecraft:stone_bricks
fill -11 206 -11 -11 206 -10 minecraft:podzol
fill -10 201 -10 -10 205 -10 minecraft:stone_bricks
fill -10 206 -10 -10 206 -10 minecraft:podzol
fill -2 201 -19 1 206 -19 minecraft:stone_bricks
fill -2 207 -19 1 207 -19 minecraft:podzol
fill -17 201 -12 -16 207 -11 minecraft:stone_bricks
fill -17 208 -12 -16 208 -11 minecraft:podzol
fill 5 186 -20 10 199 -10 minecraft:stone
fill 6 186 -19 9 186 -11 minecraft:dirt
fill 6 187 -19 9 188 -11 minecraft:cherry_leaves[persistent=true]
fill 6 189 -19 9 201 -11 minecraft:air
execute positioned -13 201 -5 run function rlk:room/prop/i_shop
execute positioned 13 201 -11 run function rlk:room/prop/i_torii_z
execute positioned 15 201 -9 run function rlk:room/prop/i_lantern
execute positioned 3 202 -4 run function rlk:room/prop/i_lantern
execute positioned 14 201 -17 run function rlk:room/prop/i_sakura
execute positioned -16 201 -5 run function rlk:room/prop/i_fence_z
execute positioned 12 201 -15 run function rlk:room/prop/i_pillar
execute positioned -4 201 -16 run function rlk:room/prop/i_pillar
execute positioned -1 201 -15 run function rlk:room/prop/i_sakura
execute positioned -5 201 -9 run function rlk:room/prop/i_petal
execute positioned -1 201 -16 run function rlk:room/prop/i_grass
execute positioned 10 201 -9 run function rlk:room/prop/i_grass
execute positioned 7 201 -2 run function rlk:room/prop/i_petal
execute positioned 15 201 -17 run function rlk:room/prop/i_petal
execute positioned 16 201 -16 run function rlk:room/prop/i_grass
execute positioned -7 201 -12 run function rlk:room/prop/i_flower
execute positioned 18 201 -4 run function rlk:room/prop/i_grass
execute positioned 6 201 -4 run function rlk:room/prop/i_flower
execute positioned 8 201 -19 run function rlk:room/prop/i_petal
execute positioned -15 201 -16 run function rlk:room/prop/i_petal
execute positioned 10 201 -6 run function rlk:room/prop/i_petal
execute positioned -1 202 -4 run function rlk:room/prop/i_petal
execute positioned -11 201 -19 run function rlk:room/prop/i_grass
execute positioned -5 201 -5 run function rlk:room/prop/i_petal
execute positioned 8 201 -14 run function rlk:room/prop/i_grass
execute positioned 7 201 -11 run function rlk:room/prop/i_petal
setblock -17 209 -12 minecraft:cherry_leaves[persistent=true] keep
setblock -16 209 -12 minecraft:cherry_leaves[persistent=true] keep
setblock -16 209 -11 minecraft:short_grass keep
setblock -11 207 -11 minecraft:cherry_leaves[persistent=true] keep
setblock -11 207 -10 minecraft:short_grass keep
setblock -10 207 -11 minecraft:cherry_leaves[persistent=true] keep
setblock -10 207 -10 minecraft:cherry_leaves[persistent=true] keep
setblock -9 207 -12 minecraft:cherry_leaves[persistent=true] keep
setblock -9 207 -11 minecraft:cherry_leaves[persistent=true] keep
setblock -2 208 -19 minecraft:short_grass keep
