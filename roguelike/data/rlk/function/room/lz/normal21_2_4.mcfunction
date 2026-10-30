# 구역 건설 (normal21_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -25 200 -17 -23 200 -15 minecraft:gravel
fill -40 208 -5 -40 210 -5 minecraft:calcite
fill -40 201 -15 -40 203 -14 minecraft:moss_block
fill -40 209 -9 -40 210 -9 minecraft:cherry_leaves[persistent=true]
fill -21 201 -12 -21 201 -10 minecraft:cobblestone
fill -21 207 -18 -21 209 -17 minecraft:moss_block
fill -21 201 -9 -21 210 -9 minecraft:stripped_dark_oak_log
fill -26 210 -20 -21 210 -20 minecraft:cherry_leaves[persistent=true]
fill -38 209 -20 -36 210 -20 minecraft:cherry_leaves[persistent=true]
fill -29 208 -20 -28 210 -20 minecraft:calcite
fill -31 210 -20 -29 210 -20 minecraft:moss_block
fill -30 201 -20 -27 203 -20 minecraft:cobblestone
fill -31 201 -1 -30 201 -1 minecraft:andesite
fill -34 201 -1 -34 210 -1 minecraft:stripped_dark_oak_log
fill -38 210 -1 -36 210 -1 minecraft:andesite
fill -30 208 -1 -26 209 -1 minecraft:tuff
fill -38 209 -1 -35 209 -1 minecraft:calcite
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -39 201 -10 -37 201 -7 minecraft:podzol
fill -36 201 -9 -36 201 -7 minecraft:podzol
fill -38 201 -6 -37 201 -4 minecraft:podzol
fill -39 201 -6 -39 207 -5 minecraft:mossy_stone_bricks
fill -39 208 -6 -39 208 -5 minecraft:podzol
fill -39 201 -4 -39 207 -4 minecraft:stone_bricks
fill -39 208 -4 -39 208 -4 minecraft:podzol
fill -40 186 -20 -31 199 -16 minecraft:stone
fill -39 186 -19 -32 186 -17 minecraft:dirt
fill -39 187 -19 -32 188 -17 minecraft:cherry_leaves[persistent=true]
fill -39 189 -19 -32 201 -17 minecraft:air
execute positioned -29 201 -19 run function rlk:room/prop/i_lantern
execute positioned -32 201 -6 run function rlk:room/prop/i_petal
execute positioned -35 201 -2 run function rlk:room/prop/i_grass
execute positioned -35 201 -9 run function rlk:room/prop/i_grass
execute positioned -37 201 -14 run function rlk:room/prop/i_flower
execute positioned -25 201 -16 run function rlk:room/prop/i_grass
execute positioned -28 201 -14 run function rlk:room/prop/i_flower
execute positioned -28 201 -13 run function rlk:room/prop/i_petal
execute positioned -25 201 -7 run function rlk:room/prop/i_grass
execute positioned -23 201 -13 run function rlk:room/prop/i_petal
setblock -39 209 -6 minecraft:cherry_leaves[persistent=true] keep
setblock -39 209 -5 minecraft:cherry_leaves[persistent=true] keep
setblock -39 209 -4 minecraft:short_grass keep
