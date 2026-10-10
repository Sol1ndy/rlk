# 구역 건설 (normal8_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -13 200 -14 -10 200 -11 minecraft:coarse_dirt
fill -10 200 -14 -6 200 -11 minecraft:coarse_dirt
fill -11 200 -5 -9 200 -3 minecraft:moss_block
fill -7 200 -5 -6 200 -2 minecraft:coarse_dirt
fill -20 207 -20 -20 210 -17 minecraft:cobblestone
fill -20 207 -8 -20 210 -3 minecraft:tuff
fill -20 210 -14 -20 210 -9 minecraft:cherry_leaves[persistent=true]
fill -1 201 -3 -1 210 -3 minecraft:stripped_dark_oak_log
fill -1 207 -12 -1 210 -12 minecraft:calcite
fill -1 208 -5 -1 210 -3 minecraft:moss_block
fill -1 204 -14 -1 204 -10 minecraft:cobblestone
fill -1 210 -14 -1 210 -14 minecraft:calcite
fill -12 209 -20 -11 210 -20 minecraft:moss_block
fill -19 210 -20 -14 210 -20 minecraft:cherry_leaves[persistent=true]
fill -8 210 -20 -4 210 -20 minecraft:cherry_leaves[persistent=true]
fill -13 208 -1 -10 210 -1 minecraft:andesite
fill -15 210 -1 -14 210 -1 minecraft:cherry_leaves[persistent=true]
fill -20 210 -1 -18 210 -1 minecraft:calcite
fill -16 209 -1 -16 210 -1 minecraft:andesite
fill -7 207 -1 -2 207 -1 minecraft:moss_block
fill -11 203 -1 -8 205 -1 minecraft:tuff
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -19 201 -19 -18 201 -18 minecraft:podzol
fill -13 201 -19 -13 201 -16 minecraft:podzol
fill -17 201 -18 -17 201 -17 minecraft:podzol
fill -16 201 -17 -16 201 -13 minecraft:podzol
fill -12 201 -17 -2 201 -15 minecraft:podzol
fill -5 201 -14 -5 201 -6 minecraft:podzol
fill -17 201 -13 -17 201 -12 minecraft:podzol
fill -19 201 -12 -18 201 -11 minecraft:podzol
fill -4 201 -6 -2 201 -6 minecraft:podzol
fill -12 201 -19 -2 201 -18 minecraft:dirt
fill -12 202 -19 -2 202 -18 minecraft:podzol
fill -19 201 -17 -18 201 -13 minecraft:dirt
fill -19 202 -17 -18 202 -13 minecraft:podzol
fill -17 201 -16 -17 201 -14 minecraft:dirt
fill -17 202 -16 -17 202 -14 minecraft:podzol
fill -4 201 -14 -2 201 -7 minecraft:dirt
fill -4 202 -14 -2 202 -7 minecraft:podzol
fill -17 201 -7 -16 207 -6 minecraft:mossy_stone_bricks
fill -17 208 -7 -16 208 -6 minecraft:podzol
fill -15 201 -3 -13 207 -2 minecraft:stone_bricks
fill -15 208 -3 -13 208 -2 minecraft:podzol
execute positioned -19 201 -8 run function rlk:room/prop/i_lantern
execute positioned -16 201 -11 run function rlk:room/prop/i_rock
execute positioned -8 201 -14 run function rlk:room/prop/i_petal
execute positioned -18 201 -5 run function rlk:room/prop/i_petal
execute positioned -17 201 -10 run function rlk:room/prop/i_petal
execute positioned -17 201 -5 run function rlk:room/prop/i_flower
execute positioned -12 201 -6 run function rlk:room/prop/i_petal
execute positioned -9 201 -14 run function rlk:room/prop/i_grass
execute positioned -7 201 -9 run function rlk:room/prop/i_petal
setblock -16 209 -7 minecraft:short_grass keep
setblock -16 209 -6 minecraft:short_grass keep
setblock -15 209 -2 minecraft:cherry_leaves[persistent=true] keep
setblock -14 209 -3 minecraft:short_grass keep
setblock -14 209 -2 minecraft:cherry_leaves[persistent=true] keep
setblock -13 209 -2 minecraft:cherry_leaves[persistent=true] keep
