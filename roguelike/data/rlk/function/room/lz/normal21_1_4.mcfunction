# 구역 건설 (normal21_1, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -7 200 -17 -5 200 -14 minecraft:moss_block
fill -10 200 -13 -8 200 -12 minecraft:moss_block
fill -20 207 -20 -20 208 -19 minecraft:andesite
fill -20 205 -14 -20 206 -10 minecraft:moss_block
fill -20 201 -17 -20 201 -15 minecraft:moss_block
fill -1 201 -5 -1 202 -5 minecraft:cobblestone
fill -1 209 -3 -1 210 -1 minecraft:cherry_leaves[persistent=true]
fill -1 202 -15 -1 202 -10 minecraft:andesite
fill -9 202 -20 -9 205 -20 minecraft:moss_block
fill -20 201 -20 -20 210 -20 minecraft:stripped_dark_oak_log
fill -19 210 -20 -18 210 -20 minecraft:moss_block
fill -20 201 -20 -17 203 -20 minecraft:moss_block
fill -16 206 -20 -12 208 -20 minecraft:moss_block
fill -5 201 -1 -5 210 -1 minecraft:stripped_dark_oak_log
fill -13 209 -1 -9 210 -1 minecraft:andesite
fill -17 204 -1 -14 205 -1 minecraft:andesite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -4 201 -7 -2 201 -7 minecraft:podzol
fill -5 201 -6 -5 201 -6 minecraft:podzol
fill -6 201 -5 -6 201 -5 minecraft:podzol
fill -7 201 -4 -7 201 -2 minecraft:podzol
fill -4 201 -6 -2 201 -6 minecraft:dirt
fill -4 202 -6 -2 202 -6 minecraft:podzol
fill -5 201 -5 -5 201 -5 minecraft:dirt
fill -5 202 -5 -5 202 -5 minecraft:podzol
fill -6 201 -4 -6 201 -2 minecraft:dirt
fill -6 202 -4 -6 202 -2 minecraft:podzol
fill -4 201 -5 -2 202 -2 minecraft:dirt
fill -4 203 -5 -2 203 -2 minecraft:podzol
fill -5 201 -4 -5 202 -2 minecraft:dirt
fill -5 203 -4 -5 203 -2 minecraft:podzol
fill -10 201 -17 -9 205 -16 minecraft:stone_bricks
fill -10 206 -17 -9 206 -16 minecraft:podzol
fill -9 201 -19 -8 206 -19 minecraft:mossy_stone_bricks
fill -9 207 -19 -8 207 -19 minecraft:podzol
fill -11 201 -19 -10 206 -18 minecraft:stone_bricks
fill -11 207 -19 -10 207 -18 minecraft:podzol
fill -9 201 -18 -8 206 -18 minecraft:stone_bricks
fill -9 207 -18 -8 207 -18 minecraft:podzol
execute positioned -4 201 -19 run function rlk:room/prop/i_pillar
execute positioned -15 201 -15 run function rlk:room/prop/i_lantern2
execute positioned -7 201 -6 run function rlk:room/prop/i_grass
execute positioned -12 201 -13 run function rlk:room/prop/i_grass
execute positioned -6 201 -15 run function rlk:room/prop/i_petal
execute positioned -18 201 -5 run function rlk:room/prop/i_flower
execute positioned -10 201 -13 run function rlk:room/prop/i_petal
execute positioned -8 201 -2 run function rlk:room/prop/i_grass
execute positioned -19 201 -6 run function rlk:room/prop/i_petal
execute positioned -14 201 -14 run function rlk:room/prop/i_petal
execute positioned -5 201 -13 run function rlk:room/prop/i_petal
setblock -11 208 -19 minecraft:cherry_leaves[persistent=true] keep
setblock -11 208 -18 minecraft:cherry_leaves[persistent=true] keep
setblock -10 208 -19 minecraft:short_grass keep
setblock -10 208 -18 minecraft:cherry_leaves[persistent=true] keep
setblock -10 207 -16 minecraft:cherry_leaves[persistent=true] keep
setblock -9 208 -19 minecraft:short_grass keep
setblock -9 208 -18 minecraft:short_grass keep
setblock -8 208 -19 minecraft:short_grass keep
