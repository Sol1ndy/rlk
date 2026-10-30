# 구역 건설 (normal12_3, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -40 -21 200 -21 minecraft:podzol
fill -40 201 -40 -21 210 -21 minecraft:stone
fill -39 201 -39 -22 210 -21 minecraft:air
fill -39 209 -39 -22 209 -21 minecraft:light[level=15]
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -20 -22 210 -2 minecraft:air
fill -39 209 -20 -22 209 -2 minecraft:light[level=15]
fill -33 200 -21 -29 200 -20 minecraft:gravel
fill -34 200 -10 -32 200 -8 minecraft:packed_mud
fill -28 200 -32 -24 200 -30 minecraft:coarse_dirt
fill -39 200 -16 -37 200 -14 minecraft:coarse_dirt
fill -36 200 -35 -34 200 -33 minecraft:packed_mud
fill -40 201 -26 -40 203 -22 minecraft:andesite
fill -40 207 -24 -40 209 -21 minecraft:moss_block
fill -40 209 -34 -40 210 -30 minecraft:cherry_leaves[persistent=true]
fill -40 203 -31 -40 205 -28 minecraft:cobblestone
fill -21 208 -37 -21 209 -32 minecraft:calcite
fill -21 201 -38 -21 210 -38 minecraft:stripped_dark_oak_log
fill -21 201 -25 -21 210 -25 minecraft:stripped_dark_oak_log
fill -21 209 -31 -21 210 -31 minecraft:cherry_leaves[persistent=true]
fill -33 210 -40 -29 210 -40 minecraft:cherry_leaves[persistent=true]
fill -30 201 -40 -28 202 -40 minecraft:tuff
fill -39 210 -40 -39 210 -40 minecraft:cherry_leaves[persistent=true]
fill -31 209 -40 -26 210 -40 minecraft:calcite
fill -40 203 -18 -40 206 -14 minecraft:tuff
fill -40 209 -15 -40 210 -14 minecraft:cherry_leaves[persistent=true]
fill -40 208 -12 -40 210 -10 minecraft:moss_block
fill -21 209 -10 -21 210 -8 minecraft:cherry_leaves[persistent=true]
fill -21 204 -9 -21 204 -5 minecraft:calcite
fill -21 209 -5 -21 210 -5 minecraft:cherry_leaves[persistent=true]
fill -21 209 -4 -21 210 -3 minecraft:cherry_leaves[persistent=true]
fill -21 205 -14 -21 207 -12 minecraft:andesite
fill -29 207 -1 -26 210 -1 minecraft:moss_block
fill -26 204 -1 -22 205 -1 minecraft:tuff
fill -34 210 -1 -29 210 -1 minecraft:moss_block
fill -40 210 -40 -21 210 -21 minecraft:polished_deepslate
fill -39 210 -39 -22 210 -21 minecraft:air
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -20 -22 210 -2 minecraft:air
fill -38 201 -27 -34 201 -26 minecraft:podzol
fill -39 201 -26 -39 201 -26 minecraft:podzol
fill -33 201 -26 -32 201 -25 minecraft:podzol
fill -34 201 -25 -34 201 -25 minecraft:podzol
fill -35 201 -24 -35 201 -17 minecraft:podzol
fill -25 201 -24 -23 201 -17 minecraft:podzol
fill -22 201 -23 -22 201 -17 minecraft:podzol
fill -39 201 -19 -39 201 -18 minecraft:podzol
fill -38 201 -18 -36 201 -17 minecraft:podzol
fill -27 201 -15 -27 201 -15 minecraft:podzol
fill -36 201 -25 -35 201 -25 minecraft:dirt
fill -36 202 -25 -35 202 -25 minecraft:podzol
fill -36 201 -24 -36 201 -19 minecraft:dirt
fill -36 202 -24 -36 202 -19 minecraft:podzol
fill -39 201 -21 -37 201 -20 minecraft:dirt
fill -39 202 -21 -37 202 -20 minecraft:podzol
fill -38 201 -19 -37 201 -19 minecraft:dirt
fill -38 202 -19 -37 202 -19 minecraft:podzol
fill -26 201 -28 -25 205 -28 minecraft:mossy_stone_bricks
fill -26 206 -28 -25 206 -28 minecraft:podzol
fill -26 201 -29 -25 205 -29 minecraft:stone_bricks
fill -26 206 -29 -25 206 -29 minecraft:podzol
fill -39 201 -22 -37 207 -22 minecraft:mossy_stone_bricks
fill -39 208 -22 -37 208 -22 minecraft:podzol
fill -39 201 -25 -37 207 -23 minecraft:stone_bricks
fill -39 208 -25 -37 208 -23 minecraft:podzol
fill -30 186 -40 -21 199 -33 minecraft:stone
fill -29 186 -34 -21 199 -32 minecraft:stone
fill -29 186 -39 -22 186 -34 minecraft:dirt
fill -29 187 -39 -22 188 -34 minecraft:cherry_leaves[persistent=true]
fill -29 189 -39 -22 201 -34 minecraft:air
fill -28 186 -33 -22 186 -33 minecraft:dirt
fill -28 187 -33 -22 188 -33 minecraft:cherry_leaves[persistent=true]
fill -28 189 -33 -22 201 -33 minecraft:air
execute positioned -36 201 -33 run function rlk:room/prop/i_shop_r1
execute positioned -35 201 -14 run function rlk:room/prop/i_house_a_r1
execute positioned -27 201 -12 run function rlk:room/prop/i_lantern
execute positioned -24 201 -25 run function rlk:room/prop/i_lantern2
execute positioned -31 201 -33 run function rlk:room/prop/i_fence_z
execute positioned -24 202 -22 run function rlk:room/prop/i_fence_z
execute positioned -33 201 -37 run function rlk:room/prop/i_rock
execute positioned -36 201 -37 run function rlk:room/prop/i_sakura
execute positioned -26 201 -32 run function rlk:room/prop/i_lantern
execute positioned -28 201 -7 run function rlk:room/prop/i_sakura
execute positioned -26 201 -2 run function rlk:room/prop/i_grass
execute positioned -33 201 -17 run function rlk:room/prop/i_grass
execute positioned -22 201 -29 run function rlk:room/prop/i_grass
execute positioned -32 201 -13 run function rlk:room/prop/i_grass
execute positioned -36 201 -8 run function rlk:room/prop/i_petal
execute positioned -36 201 -38 run function rlk:room/prop/i_flower
execute positioned -33 201 -35 run function rlk:room/prop/i_grass
execute positioned -29 201 -14 run function rlk:room/prop/i_petal
execute positioned -26 201 -35 run function rlk:room/prop/i_petal
execute positioned -24 201 -15 run function rlk:room/prop/i_flower
execute positioned -35 201 -9 run function rlk:room/prop/i_grass
execute positioned -37 201 -35 run function rlk:room/prop/i_petal
execute positioned -23 201 -28 run function rlk:room/prop/i_flower
execute positioned -33 201 -35 run function rlk:room/prop/i_grass
execute positioned -34 201 -7 run function rlk:room/prop/i_petal
execute positioned -22 201 -6 run function rlk:room/prop/i_petal
execute positioned -25 201 -26 run function rlk:room/prop/i_petal
setblock -39 209 -25 minecraft:short_grass keep
setblock -38 209 -25 minecraft:cherry_leaves[persistent=true] keep
setblock -38 209 -24 minecraft:cherry_leaves[persistent=true] keep
setblock -38 209 -23 minecraft:short_grass keep
setblock -38 209 -22 minecraft:short_grass keep
setblock -37 209 -24 minecraft:short_grass keep
setblock -37 209 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -37 209 -22 minecraft:cherry_leaves[persistent=true] keep
setblock -26 207 -28 minecraft:short_grass keep
setblock -25 207 -29 minecraft:cherry_leaves[persistent=true] keep
