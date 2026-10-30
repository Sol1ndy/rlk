# 구역 건설 (first3_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -38 200 -7 -37 200 -5 minecraft:packed_mud
fill -30 200 -10 -29 200 -8 minecraft:gravel
fill -40 207 -9 -40 210 -5 minecraft:tuff
fill -40 210 -10 -40 210 -7 minecraft:cherry_leaves[persistent=true]
fill -40 203 -15 -40 204 -15 minecraft:moss_block
fill -40 209 -1 -40 209 -1 minecraft:andesite
fill -40 209 -6 -40 210 -1 minecraft:cherry_leaves[persistent=true]
fill -40 208 -12 -40 210 -10 minecraft:cobblestone
fill -21 210 -12 -21 210 -8 minecraft:cherry_leaves[persistent=true]
fill -21 202 -11 -21 202 -8 minecraft:tuff
fill -21 209 -11 -21 210 -8 minecraft:tuff
fill -21 209 -17 -21 210 -12 minecraft:cherry_leaves[persistent=true]
fill -21 209 -20 -21 210 -15 minecraft:cherry_leaves[persistent=true]
fill -21 208 -19 -21 210 -16 minecraft:tuff
fill -34 208 -20 -33 208 -20 minecraft:andesite
fill -29 203 -20 -24 206 -20 minecraft:calcite
fill -26 204 -20 -23 205 -20 minecraft:calcite
fill -29 209 -20 -27 210 -20 minecraft:cherry_leaves[persistent=true]
fill -39 210 -20 -38 210 -20 minecraft:calcite
fill -29 203 -1 -28 206 -1 minecraft:andesite
fill -30 207 -1 -26 209 -1 minecraft:calcite
fill -27 207 -1 -23 208 -1 minecraft:andesite
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -28 201 -18 -27 201 -16 minecraft:podzol
fill -26 201 -17 -22 201 -17 minecraft:podzol
fill -27 201 -15 -27 201 -15 minecraft:podzol
fill -26 201 -18 -22 201 -18 minecraft:dirt
fill -26 202 -18 -22 202 -18 minecraft:podzol
fill -30 201 -17 -29 206 -16 minecraft:stone_bricks
fill -30 207 -17 -29 207 -16 minecraft:podzol
fill -27 201 -19 -25 207 -19 minecraft:mossy_stone_bricks
fill -27 208 -19 -25 208 -19 minecraft:podzol
fill -24 201 -19 -22 207 -19 minecraft:stone_bricks
fill -24 208 -19 -22 208 -19 minecraft:podzol
execute positioned -32 201 -5 run function rlk:room/prop/i_fence_x
execute positioned -37 201 -19 run function rlk:room/prop/i_torii_x
execute positioned -23 201 -3 run function rlk:room/prop/i_grass
execute positioned -30 201 -15 run function rlk:room/prop/i_grass
execute positioned -23 201 -7 run function rlk:room/prop/i_petal
execute positioned -37 201 -15 run function rlk:room/prop/i_petal
execute positioned -37 201 -18 run function rlk:room/prop/i_grass
execute positioned -29 201 -5 run function rlk:room/prop/i_grass
execute positioned -36 201 -17 run function rlk:room/prop/i_petal
execute positioned -33 201 -14 run function rlk:room/prop/i_petal
execute positioned -30 201 -2 run function rlk:room/prop/i_petal
setblock -30 208 -17 minecraft:short_grass keep
setblock -30 208 -16 minecraft:short_grass keep
setblock -29 208 -17 minecraft:cherry_leaves[persistent=true] keep
setblock -29 208 -16 minecraft:cherry_leaves[persistent=true] keep
setblock -27 209 -19 minecraft:short_grass keep
setblock -25 209 -19 minecraft:cherry_leaves[persistent=true] keep
setblock -22 209 -19 minecraft:cherry_leaves[persistent=true] keep
