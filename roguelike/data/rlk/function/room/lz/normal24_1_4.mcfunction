# 구역 건설 (normal24_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -18 200 -18 -15 200 -17 minecraft:moss_block
fill -19 200 -8 -18 200 -7 minecraft:coarse_dirt
fill -20 203 -15 -20 203 -11 minecraft:cobblestone
fill -20 210 -15 -20 210 -14 minecraft:cherry_leaves[persistent=true]
fill -20 208 -19 -20 210 -18 minecraft:tuff
fill -20 205 -14 -20 208 -11 minecraft:tuff
fill -1 210 -12 -1 210 -8 minecraft:cherry_leaves[persistent=true]
fill -1 210 -18 -1 210 -13 minecraft:cherry_leaves[persistent=true]
fill -1 208 -19 -1 209 -14 minecraft:calcite
fill -1 209 -18 -1 210 -13 minecraft:cherry_leaves[persistent=true]
fill -1 203 -13 -1 206 -9 minecraft:tuff
fill -1 210 -20 -1 210 -16 minecraft:cherry_leaves[persistent=true]
fill -12 201 -20 -10 203 -20 minecraft:cobblestone
fill -5 203 -20 -4 205 -20 minecraft:tuff
fill -20 202 -20 -18 204 -20 minecraft:calcite
fill -16 210 -20 -13 210 -20 minecraft:moss_block
fill -18 205 -20 -16 205 -20 minecraft:andesite
fill -5 203 -1 -2 205 -1 minecraft:tuff
fill -13 203 -1 -10 203 -1 minecraft:cobblestone
fill -10 207 -1 -7 208 -1 minecraft:andesite
fill -20 204 -1 -15 205 -1 minecraft:tuff
fill -20 204 -1 -17 205 -1 minecraft:moss_block
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -7 201 -18 -3 201 -18 minecraft:podzol
fill -9 201 -17 -7 201 -15 minecraft:podzol
fill -4 201 -17 -2 201 -8 minecraft:podzol
fill -10 201 -16 -10 201 -15 minecraft:podzol
fill -6 201 -15 -5 201 -15 minecraft:podzol
fill -5 201 -14 -5 201 -8 minecraft:podzol
fill -14 201 -5 -2 201 -4 minecraft:podzol
fill -15 201 -4 -15 201 -2 minecraft:podzol
fill -14 201 -3 -2 201 -2 minecraft:dirt
fill -14 202 -3 -2 202 -2 minecraft:podzol
fill -15 201 -19 -15 206 -19 minecraft:mossy_stone_bricks
fill -15 207 -19 -15 207 -19 minecraft:podzol
fill -17 201 -19 -16 206 -19 minecraft:stone_bricks
fill -17 207 -19 -16 207 -19 minecraft:podzol
fill -6 201 -17 -5 207 -16 minecraft:stone_bricks
fill -6 208 -17 -5 208 -16 minecraft:podzol
execute positioned -16 201 -4 run function rlk:room/prop/i_lantern
execute positioned -4 202 -9 run function rlk:room/prop/i_lantern
execute positioned -5 202 -12 run function rlk:room/prop/i_petal
execute positioned -2 201 -7 run function rlk:room/prop/i_flower
execute positioned -17 201 -12 run function rlk:room/prop/i_flower
execute positioned -13 201 -8 run function rlk:room/prop/i_petal
execute positioned -9 201 -9 run function rlk:room/prop/i_petal
execute positioned -4 202 -16 run function rlk:room/prop/i_flower
execute positioned -19 201 -4 run function rlk:room/prop/i_petal
execute positioned -17 201 -12 run function rlk:room/prop/i_petal
execute positioned -7 201 -6 run function rlk:room/prop/i_petal
setblock -17 208 -19 minecraft:short_grass keep
setblock -15 208 -19 minecraft:cherry_leaves[persistent=true] keep
setblock -6 209 -17 minecraft:short_grass keep
setblock -5 209 -17 minecraft:cherry_leaves[persistent=true] keep
setblock -5 209 -16 minecraft:short_grass keep
