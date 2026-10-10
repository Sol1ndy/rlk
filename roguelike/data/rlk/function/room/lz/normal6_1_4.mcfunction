# 구역 건설 (normal6_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -7 200 -10 -4 200 -8 minecraft:moss_block
fill -18 200 -7 -14 200 -5 minecraft:packed_mud
fill -20 207 -5 -20 209 -3 minecraft:tuff
fill -20 210 -4 -20 210 -1 minecraft:cherry_leaves[persistent=true]
fill -20 206 -13 -20 207 -12 minecraft:calcite
fill -20 205 -16 -20 206 -12 minecraft:andesite
fill -20 209 -19 -20 210 -17 minecraft:cherry_leaves[persistent=true]
fill -20 204 -14 -20 207 -9 minecraft:andesite
fill -1 209 -10 -1 210 -7 minecraft:andesite
fill -1 208 -14 -1 210 -9 minecraft:cobblestone
fill -1 202 -5 -1 204 -2 minecraft:andesite
fill -17 203 -20 -17 204 -20 minecraft:calcite
fill -3 209 -20 -1 210 -20 minecraft:cherry_leaves[persistent=true]
fill -7 209 -20 -4 210 -20 minecraft:cobblestone
fill -12 202 -20 -9 205 -20 minecraft:andesite
fill -20 208 -20 -17 208 -20 minecraft:andesite
fill -16 209 -1 -13 210 -1 minecraft:cherry_leaves[persistent=true]
fill -12 210 -1 -9 210 -1 minecraft:cherry_leaves[persistent=true]
fill -16 206 -1 -12 206 -1 minecraft:moss_block
fill -3 209 -1 -2 210 -1 minecraft:cherry_leaves[persistent=true]
fill -10 210 -1 -6 210 -1 minecraft:cherry_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -18 201 -19 -18 201 -16 minecraft:podzol
fill -10 201 -19 -10 201 -16 minecraft:podzol
fill -17 201 -15 -17 201 -15 minecraft:podzol
fill -14 201 -15 -11 201 -15 minecraft:podzol
fill -16 201 -14 -15 201 -14 minecraft:podzol
fill -17 201 -19 -17 201 -16 minecraft:dirt
fill -17 202 -19 -17 202 -16 minecraft:podzol
fill -11 201 -19 -11 201 -16 minecraft:dirt
fill -11 202 -19 -11 202 -16 minecraft:podzol
fill -16 201 -16 -16 201 -15 minecraft:dirt
fill -16 202 -16 -16 202 -15 minecraft:podzol
fill -12 201 -16 -12 201 -16 minecraft:dirt
fill -12 202 -16 -12 202 -16 minecraft:podzol
fill -15 201 -15 -15 201 -15 minecraft:dirt
fill -15 202 -15 -15 202 -15 minecraft:podzol
fill -16 201 -19 -12 202 -18 minecraft:dirt
fill -16 203 -19 -12 203 -18 minecraft:podzol
fill -16 201 -17 -15 202 -17 minecraft:dirt
fill -16 203 -17 -15 203 -17 minecraft:podzol
fill -12 201 -17 -12 202 -17 minecraft:dirt
fill -12 203 -17 -12 203 -17 minecraft:podzol
fill -15 201 -16 -15 202 -16 minecraft:dirt
fill -15 203 -16 -15 203 -16 minecraft:podzol
fill -19 201 -14 -18 206 -13 minecraft:mossy_stone_bricks
fill -19 207 -14 -18 207 -13 minecraft:podzol
fill -19 201 -12 -18 206 -12 minecraft:stone_bricks
fill -19 207 -12 -18 207 -12 minecraft:podzol
fill -14 201 -16 -13 207 -16 minecraft:mossy_stone_bricks
fill -14 208 -16 -13 208 -16 minecraft:podzol
fill -14 201 -17 -13 207 -17 minecraft:stone_bricks
fill -14 208 -17 -13 208 -17 minecraft:podzol
execute positioned -19 201 -9 run function rlk:room/prop/i_lantern
execute positioned -15 201 -8 run function rlk:room/prop/i_lantern
execute positioned -13 201 -11 run function rlk:room/prop/i_petal
execute positioned -18 201 -2 run function rlk:room/prop/i_petal
execute positioned -2 201 -9 run function rlk:room/prop/i_petal
execute positioned -9 201 -12 run function rlk:room/prop/i_grass
execute positioned -7 201 -16 run function rlk:room/prop/i_petal
execute positioned -17 203 -17 run function rlk:room/prop/i_petal
execute positioned -3 201 -10 run function rlk:room/prop/i_petal
execute positioned -2 201 -10 run function rlk:room/prop/i_grass
setblock -19 208 -14 minecraft:short_grass keep
setblock -19 208 -12 minecraft:cherry_leaves[persistent=true] keep
setblock -18 208 -14 minecraft:cherry_leaves[persistent=true] keep
setblock -18 208 -13 minecraft:cherry_leaves[persistent=true] keep
setblock -18 208 -12 minecraft:short_grass keep
setblock -14 209 -17 minecraft:cherry_leaves[persistent=true] keep
setblock -13 209 -16 minecraft:short_grass keep
