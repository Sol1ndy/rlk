# 구역 건설 (first3_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 212 -1 minecraft:stone
fill -39 201 -19 -22 212 -2 minecraft:air
fill -39 211 -19 -22 211 -2 minecraft:light[level=15]
fill -38 202 -7 -37 202 -5 minecraft:packed_mud
fill -30 202 -10 -29 202 -8 minecraft:gravel
fill -40 209 -9 -40 212 -5 minecraft:tuff
fill -40 212 -10 -40 212 -7 minecraft:cherry_leaves[persistent=true]
fill -40 205 -15 -40 206 -15 minecraft:moss_block
fill -40 211 -1 -40 211 -1 minecraft:andesite
fill -40 211 -6 -40 212 -1 minecraft:cherry_leaves[persistent=true]
fill -40 210 -12 -40 212 -10 minecraft:cobblestone
fill -21 212 -12 -21 212 -8 minecraft:cherry_leaves[persistent=true]
fill -21 204 -11 -21 204 -8 minecraft:tuff
fill -21 211 -11 -21 212 -8 minecraft:tuff
fill -21 211 -17 -21 212 -12 minecraft:cherry_leaves[persistent=true]
fill -21 211 -20 -21 212 -15 minecraft:cherry_leaves[persistent=true]
fill -21 210 -19 -21 212 -16 minecraft:tuff
fill -34 210 -20 -33 210 -20 minecraft:andesite
fill -25 201 -20 -22 201 -20 minecraft:tuff
fill -29 205 -20 -24 208 -20 minecraft:calcite
fill -26 206 -20 -23 207 -20 minecraft:calcite
fill -29 211 -20 -27 212 -20 minecraft:cherry_leaves[persistent=true]
fill -39 212 -20 -38 212 -20 minecraft:calcite
fill -29 205 -1 -28 208 -1 minecraft:andesite
fill -30 209 -1 -26 211 -1 minecraft:calcite
fill -27 209 -1 -23 210 -1 minecraft:andesite
fill -40 212 -20 -21 212 -1 minecraft:polished_deepslate
fill -39 212 -19 -22 212 -2 minecraft:air
fill -39 201 -19 -28 201 -19 minecraft:dirt
fill -39 202 -19 -28 202 -19 minecraft:podzol
fill -39 201 -18 -29 201 -18 minecraft:dirt
fill -39 202 -18 -29 202 -18 minecraft:podzol
fill -39 201 -17 -31 201 -2 minecraft:dirt
fill -39 202 -17 -31 202 -2 minecraft:podzol
fill -26 201 -16 -22 201 -2 minecraft:dirt
fill -26 202 -16 -22 202 -2 minecraft:podzol
fill -30 201 -15 -28 201 -2 minecraft:dirt
fill -30 202 -15 -28 202 -2 minecraft:podzol
fill -27 201 -14 -27 201 -2 minecraft:dirt
fill -27 202 -14 -27 202 -2 minecraft:podzol
fill -28 201 -18 -27 202 -16 minecraft:dirt
fill -28 203 -18 -27 203 -16 minecraft:podzol
fill -26 201 -17 -22 202 -17 minecraft:dirt
fill -26 203 -17 -22 203 -17 minecraft:podzol
fill -27 201 -15 -27 202 -15 minecraft:dirt
fill -27 203 -15 -27 203 -15 minecraft:podzol
fill -26 201 -18 -22 203 -18 minecraft:dirt
fill -26 204 -18 -22 204 -18 minecraft:podzol
fill -30 201 -17 -29 208 -16 minecraft:stone_bricks
fill -30 209 -17 -29 209 -16 minecraft:podzol
fill -27 201 -19 -25 209 -19 minecraft:mossy_stone_bricks
fill -27 210 -19 -25 210 -19 minecraft:podzol
fill -24 201 -19 -22 209 -19 minecraft:stone_bricks
fill -24 210 -19 -22 210 -19 minecraft:podzol
execute positioned -32 203 -5 run function rlk:room/prop/i_fence_x
execute positioned -37 203 -19 run function rlk:room/prop/i_torii_x
execute positioned -23 203 -3 run function rlk:room/prop/i_grass
execute positioned -30 203 -15 run function rlk:room/prop/i_grass
execute positioned -23 203 -7 run function rlk:room/prop/i_petal
execute positioned -37 203 -15 run function rlk:room/prop/i_petal
execute positioned -37 203 -18 run function rlk:room/prop/i_grass
execute positioned -29 203 -5 run function rlk:room/prop/i_grass
execute positioned -36 203 -17 run function rlk:room/prop/i_petal
execute positioned -33 203 -14 run function rlk:room/prop/i_petal
execute positioned -30 203 -2 run function rlk:room/prop/i_petal
setblock -30 210 -17 minecraft:short_grass keep
setblock -30 210 -16 minecraft:short_grass keep
setblock -29 210 -17 minecraft:cherry_leaves[persistent=true] keep
setblock -29 210 -16 minecraft:cherry_leaves[persistent=true] keep
setblock -27 211 -19 minecraft:short_grass keep
setblock -25 211 -19 minecraft:cherry_leaves[persistent=true] keep
setblock -22 211 -19 minecraft:cherry_leaves[persistent=true] keep
