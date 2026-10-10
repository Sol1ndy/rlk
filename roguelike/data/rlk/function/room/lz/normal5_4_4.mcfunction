# 구역 건설 (normal5_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -8 200 -23 -6 200 -22 minecraft:packed_mud
fill -20 206 -34 -20 206 -34 minecraft:tuff
fill -20 204 -37 -20 204 -35 minecraft:tuff
fill -20 201 -34 -20 202 -32 minecraft:andesite
fill -20 201 -31 -20 210 -31 minecraft:stripped_dark_oak_log
fill -20 208 -33 -20 209 -28 minecraft:tuff
fill -20 202 -23 -20 205 -21 minecraft:andesite
fill -1 207 -31 -1 209 -29 minecraft:tuff
fill -1 207 -36 -1 209 -36 minecraft:andesite
fill -1 201 -28 -1 202 -27 minecraft:cobblestone
fill -1 201 -30 -1 204 -28 minecraft:andesite
fill -1 210 -39 -1 210 -35 minecraft:cherry_leaves[persistent=true]
fill -1 210 -26 -1 210 -22 minecraft:cherry_leaves[persistent=true]
fill -3 203 -40 -3 203 -40 minecraft:cobblestone
fill -6 209 -40 -3 210 -40 minecraft:cherry_leaves[persistent=true]
fill -18 210 -40 -15 210 -40 minecraft:moss_block
fill -7 207 -40 -6 207 -40 minecraft:cobblestone
fill -3 210 -40 -3 210 -40 minecraft:cherry_leaves[persistent=true]
fill -11 202 -21 -6 205 -21 minecraft:andesite
fill -3 210 -21 -2 210 -21 minecraft:cherry_leaves[persistent=true]
fill -16 209 -21 -12 209 -21 minecraft:moss_block
fill -5 209 -21 -4 210 -21 minecraft:cherry_leaves[persistent=true]
fill -19 207 -21 -15 207 -21 minecraft:calcite
fill -3 203 -21 -2 206 -21 minecraft:cobblestone
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -19 201 -39 -19 201 -35 minecraft:podzol
fill -9 201 -39 -8 201 -35 minecraft:podzol
fill -14 201 -35 -10 201 -35 minecraft:podzol
fill -15 201 -34 -15 201 -30 minecraft:podzol
fill -19 201 -31 -19 201 -30 minecraft:podzol
fill -18 201 -30 -16 201 -30 minecraft:podzol
fill -18 201 -39 -10 201 -37 minecraft:dirt
fill -18 202 -39 -10 202 -37 minecraft:podzol
fill -18 201 -36 -18 201 -31 minecraft:dirt
fill -18 202 -36 -18 202 -31 minecraft:podzol
fill -15 201 -36 -10 201 -36 minecraft:dirt
fill -15 202 -36 -10 202 -36 minecraft:podzol
fill -15 201 -35 -15 201 -35 minecraft:dirt
fill -15 202 -35 -15 202 -35 minecraft:podzol
fill -19 201 -34 -19 201 -32 minecraft:dirt
fill -19 202 -34 -19 202 -32 minecraft:podzol
fill -17 201 -34 -16 201 -31 minecraft:dirt
fill -17 202 -34 -16 202 -31 minecraft:podzol
fill -19 201 -24 -19 207 -22 minecraft:mossy_stone_bricks
fill -19 208 -24 -19 208 -22 minecraft:podzol
fill -17 201 -36 -16 207 -35 minecraft:stone_bricks
fill -17 208 -36 -16 208 -35 minecraft:podzol
fill -19 201 -25 -19 207 -25 minecraft:stone_bricks
fill -19 208 -25 -19 208 -25 minecraft:podzol
execute positioned -4 201 -39 run function rlk:room/prop/i_lantern2
execute positioned -12 203 -37 run function rlk:room/prop/i_pillar
execute positioned -4 201 -26 run function rlk:room/prop/i_petal
execute positioned -9 202 -37 run function rlk:room/prop/i_flower
execute positioned -7 201 -28 run function rlk:room/prop/i_petal
execute positioned -2 201 -23 run function rlk:room/prop/i_grass
execute positioned -17 202 -30 run function rlk:room/prop/i_petal
execute positioned -12 201 -22 run function rlk:room/prop/i_petal
execute positioned -15 201 -28 run function rlk:room/prop/i_flower
setblock -19 209 -24 minecraft:short_grass keep
setblock -19 209 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -19 209 -22 minecraft:short_grass keep
setblock -17 209 -36 minecraft:cherry_leaves[persistent=true] keep
setblock -17 209 -35 minecraft:cherry_leaves[persistent=true] keep
setblock -16 209 -36 minecraft:cherry_leaves[persistent=true] keep
setblock -16 209 -35 minecraft:short_grass keep
