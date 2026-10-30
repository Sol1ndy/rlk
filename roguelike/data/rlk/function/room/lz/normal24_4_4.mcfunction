# 구역 건설 (normal24_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -6 200 -32 -4 200 -30 minecraft:moss_block
fill -18 200 -24 -14 200 -23 minecraft:coarse_dirt
fill -20 205 -25 -20 208 -23 minecraft:andesite
fill -20 202 -36 -20 204 -32 minecraft:cobblestone
fill -20 209 -31 -20 210 -30 minecraft:cherry_leaves[persistent=true]
fill -20 204 -25 -20 207 -24 minecraft:moss_block
fill -20 201 -33 -20 204 -33 minecraft:andesite
fill -20 209 -27 -20 210 -23 minecraft:andesite
fill -1 208 -39 -1 208 -36 minecraft:tuff
fill -1 205 -22 -1 206 -22 minecraft:andesite
fill -1 202 -27 -1 205 -22 minecraft:calcite
fill -1 206 -40 -1 209 -35 minecraft:cobblestone
fill -1 209 -40 -1 210 -36 minecraft:cherry_leaves[persistent=true]
fill -11 209 -40 -10 210 -40 minecraft:cherry_leaves[persistent=true]
fill -7 210 -40 -3 210 -40 minecraft:tuff
fill -5 204 -40 -1 204 -40 minecraft:moss_block
fill -16 202 -40 -14 204 -40 minecraft:andesite
fill -20 208 -21 -15 210 -21 minecraft:tuff
fill -18 202 -21 -14 203 -21 minecraft:calcite
fill -20 210 -21 -19 210 -21 minecraft:cherry_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -7 201 -39 -7 201 -35 minecraft:podzol
fill -6 201 -35 -6 201 -35 minecraft:podzol
fill -5 201 -34 -5 201 -33 minecraft:podzol
fill -4 201 -33 -2 201 -33 minecraft:podzol
fill -6 201 -39 -5 201 -39 minecraft:dirt
fill -6 202 -39 -5 202 -39 minecraft:podzol
fill -6 201 -38 -6 201 -36 minecraft:dirt
fill -6 202 -38 -6 202 -36 minecraft:podzol
fill -5 201 -35 -5 201 -35 minecraft:dirt
fill -5 202 -35 -5 202 -35 minecraft:podzol
fill -4 201 -34 -2 201 -34 minecraft:dirt
fill -4 202 -34 -2 202 -34 minecraft:podzol
fill -4 201 -39 -2 202 -35 minecraft:dirt
fill -4 203 -39 -2 203 -35 minecraft:podzol
fill -5 201 -38 -5 202 -36 minecraft:dirt
fill -5 203 -38 -5 203 -36 minecraft:podzol
fill -11 201 -37 -10 207 -37 minecraft:mossy_stone_bricks
fill -11 208 -37 -10 208 -37 minecraft:podzol
fill -7 201 -22 -7 207 -22 minecraft:mossy_stone_bricks
fill -7 208 -22 -7 208 -22 minecraft:podzol
fill -11 201 -36 -10 207 -36 minecraft:stone_bricks
fill -11 208 -36 -10 208 -36 minecraft:podzol
fill -7 201 -23 -2 207 -23 minecraft:stone_bricks
fill -7 208 -23 -2 208 -23 minecraft:podzol
fill -6 201 -22 -2 207 -22 minecraft:stone_bricks
fill -6 208 -22 -2 208 -22 minecraft:podzol
execute positioned -5 201 -27 run function rlk:room/prop/i_shop_r3
execute positioned -11 201 -25 run function rlk:room/prop/i_lantern2
execute positioned -17 201 -37 run function rlk:room/prop/i_rock
execute positioned -19 201 -22 run function rlk:room/prop/i_wall_x
execute positioned -8 201 -30 run function rlk:room/prop/i_petal
execute positioned -11 201 -34 run function rlk:room/prop/i_grass
execute positioned -18 201 -32 run function rlk:room/prop/i_grass
execute positioned -10 201 -38 run function rlk:room/prop/i_petal
execute positioned -15 201 -26 run function rlk:room/prop/i_flower
execute positioned -5 201 -29 run function rlk:room/prop/i_flower
execute positioned -7 201 -27 run function rlk:room/prop/i_petal
execute positioned -7 201 -25 run function rlk:room/prop/i_flower
execute positioned -2 204 -36 run function rlk:room/prop/i_petal
setblock -11 209 -37 minecraft:short_grass keep
setblock -10 209 -37 minecraft:cherry_leaves[persistent=true] keep
setblock -7 209 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -6 209 -23 minecraft:short_grass keep
setblock -6 209 -22 minecraft:short_grass keep
setblock -5 209 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -5 209 -22 minecraft:cherry_leaves[persistent=true] keep
setblock -4 209 -22 minecraft:short_grass keep
setblock -2 209 -22 minecraft:cherry_leaves[persistent=true] keep
