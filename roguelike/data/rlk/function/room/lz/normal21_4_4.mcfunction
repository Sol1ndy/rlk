# 구역 건설 (normal21_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -1 210 -22 minecraft:air
fill -19 209 -39 -1 209 -22 minecraft:light[level=15]
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 0 201 -39 18 210 -22 minecraft:air
fill 0 209 -39 18 209 -22 minecraft:light[level=15]
fill -17 200 -29 -13 200 -28 minecraft:packed_mud
fill -2 200 -37 1 200 -36 minecraft:packed_mud
fill 10 200 -25 13 200 -24 minecraft:packed_mud
fill 10 200 -25 12 200 -24 minecraft:gravel
fill -7 200 -32 -6 200 -31 minecraft:packed_mud
fill -20 209 -25 -20 210 -24 minecraft:cherry_leaves[persistent=true]
fill -20 207 -34 -20 208 -34 minecraft:tuff
fill -20 208 -22 -20 209 -21 minecraft:calcite
fill -20 210 -37 -20 210 -32 minecraft:cherry_leaves[persistent=true]
fill -16 207 -40 -11 207 -40 minecraft:moss_block
fill -16 210 -40 -16 210 -40 minecraft:cherry_leaves[persistent=true]
fill -18 201 -40 -16 203 -40 minecraft:andesite
fill -6 201 -40 -6 210 -40 minecraft:stripped_dark_oak_log
fill -16 209 -21 -12 210 -21 minecraft:cherry_leaves[persistent=true]
fill 19 207 -36 19 209 -32 minecraft:moss_block
fill 19 210 -30 19 210 -27 minecraft:andesite
fill 19 201 -35 19 203 -30 minecraft:moss_block
fill 19 206 -40 19 209 -37 minecraft:andesite
fill 13 210 -40 18 210 -40 minecraft:cherry_leaves[persistent=true]
fill 12 210 -40 15 210 -40 minecraft:cherry_leaves[persistent=true]
fill 10 202 -40 15 203 -40 minecraft:andesite
fill 16 205 -21 16 208 -21 minecraft:moss_block
fill 12 201 -21 12 202 -21 minecraft:andesite
fill 13 210 -21 15 210 -21 minecraft:cherry_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -1 210 -22 minecraft:air
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 0 210 -39 18 210 -22 minecraft:air
fill 5 201 -33 7 201 -27 minecraft:podzol
fill 8 201 -32 8 201 -27 minecraft:podzol
fill 10 201 -32 10 201 -27 minecraft:podzol
fill 9 201 -31 9 201 -27 minecraft:podzol
fill 11 201 -31 11 201 -27 minecraft:podzol
fill -8 201 -30 -5 201 -30 minecraft:podzol
fill -6 201 -29 -5 201 -22 minecraft:podzol
fill -4 201 -25 -1 201 -24 minecraft:podzol
fill -4 201 -23 -3 201 -22 minecraft:podzol
fill 9 201 -34 9 207 -32 minecraft:mossy_stone_bricks
fill 9 208 -34 9 208 -32 minecraft:podzol
fill 10 201 -33 10 207 -33 minecraft:mossy_stone_bricks
fill 10 208 -33 10 208 -33 minecraft:podzol
fill 0 201 -22 1 207 -22 minecraft:mossy_stone_bricks
fill 0 208 -22 1 208 -22 minecraft:podzol
fill -11 201 -34 -10 207 -33 minecraft:stone_bricks
fill -11 208 -34 -10 208 -33 minecraft:podzol
fill 8 201 -33 8 207 -33 minecraft:stone_bricks
fill 8 208 -33 8 208 -33 minecraft:podzol
fill -2 201 -23 1 207 -23 minecraft:stone_bricks
fill -2 208 -23 1 208 -23 minecraft:podzol
fill -2 201 -22 -1 207 -22 minecraft:stone_bricks
fill -2 208 -22 -1 208 -22 minecraft:podzol
fill -13 186 -28 -8 199 -21 minecraft:stone
fill -20 186 -27 -12 199 -21 minecraft:stone
fill -12 186 -27 -9 186 -22 minecraft:dirt
fill -12 187 -27 -9 188 -22 minecraft:cherry_leaves[persistent=true]
fill -12 189 -27 -9 201 -22 minecraft:air
fill -19 186 -26 -13 186 -22 minecraft:dirt
fill -19 187 -26 -13 188 -22 minecraft:cherry_leaves[persistent=true]
fill -19 189 -26 -13 201 -22 minecraft:air
execute positioned -15 201 -36 run function rlk:room/prop/i_shop_r2
execute positioned -15 201 -31 run function rlk:room/prop/i_house_a_r1
execute positioned 7 202 -27 run function rlk:room/prop/i_lantern2
execute positioned 18 201 -25 run function rlk:room/prop/i_lantern
execute positioned -5 202 -25 run function rlk:room/prop/i_bamboo
execute positioned 16 201 -37 run function rlk:room/prop/i_lantern2
execute positioned 5 202 -30 run function rlk:room/prop/i_bamboo
execute positioned 10 202 -30 run function rlk:room/prop/i_lantern2
execute positioned 5 202 -33 run function rlk:room/prop/i_pillar
execute positioned 13 201 -33 run function rlk:room/prop/i_sakura
execute positioned -15 201 -37 run function rlk:room/prop/i_grass
execute positioned 12 201 -27 run function rlk:room/prop/i_flower
execute positioned -3 201 -32 run function rlk:room/prop/i_petal
execute positioned -19 201 -22 run function rlk:room/prop/i_grass
execute positioned 14 201 -38 run function rlk:room/prop/i_petal
execute positioned 3 201 -29 run function rlk:room/prop/i_grass
execute positioned -4 201 -34 run function rlk:room/prop/i_petal
execute positioned -14 201 -26 run function rlk:room/prop/i_petal
execute positioned 12 201 -32 run function rlk:room/prop/i_grass
execute positioned -15 201 -25 run function rlk:room/prop/i_grass
execute positioned 12 201 -27 run function rlk:room/prop/i_flower
execute positioned -12 201 -29 run function rlk:room/prop/i_grass
execute positioned -1 201 -33 run function rlk:room/prop/i_petal
execute positioned -7 201 -25 run function rlk:room/prop/i_petal
execute positioned 5 201 -38 run function rlk:room/prop/i_grass
execute positioned -16 201 -37 run function rlk:room/prop/i_flower
execute positioned 10 202 -29 run function rlk:room/prop/i_grass
execute positioned 16 201 -37 run function rlk:room/prop/i_flower
setblock -11 209 -34 minecraft:short_grass keep
setblock -11 209 -33 minecraft:cherry_leaves[persistent=true] keep
setblock -2 209 -23 minecraft:short_grass keep
setblock -1 209 -23 minecraft:short_grass keep
setblock -1 209 -22 minecraft:cherry_leaves[persistent=true] keep
setblock 0 209 -23 minecraft:short_grass keep
setblock 1 209 -23 minecraft:cherry_leaves[persistent=true] keep
setblock 1 209 -22 minecraft:short_grass keep
setblock 9 209 -34 minecraft:short_grass keep
setblock 9 209 -33 minecraft:short_grass keep
setblock 10 209 -33 minecraft:short_grass keep
