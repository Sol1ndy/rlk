# 구역 건설 (normal24_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -17 200 -13 -16 200 -11 minecraft:coarse_dirt
fill -20 201 -13 -20 201 -10 minecraft:cobblestone
fill -20 208 -13 -20 208 -11 minecraft:mossy_cobblestone
fill -20 209 -8 -20 210 -6 minecraft:moss_block
fill -20 204 -12 -20 207 -8 minecraft:andesite
fill -1 210 -6 -1 210 -1 minecraft:moss_block
fill -1 202 -11 -1 202 -7 minecraft:moss_block
fill -1 209 -10 -1 209 -5 minecraft:moss_block
fill -1 207 -8 -1 208 -3 minecraft:granite
fill -1 201 -15 -1 201 -14 minecraft:cobblestone
fill -16 205 -20 -14 208 -20 minecraft:mossy_cobblestone
fill -13 207 -20 -13 207 -20 minecraft:andesite
fill -8 210 -20 -6 210 -20 minecraft:oak_leaves[persistent=true]
fill -5 207 -20 -3 208 -20 minecraft:cobblestone
fill -15 204 -20 -11 204 -20 minecraft:mossy_cobblestone
fill -13 207 -1 -10 210 -1 minecraft:moss_block
fill -20 203 -1 -17 206 -1 minecraft:andesite
fill -16 210 -1 -12 210 -1 minecraft:oak_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -7 201 -18 -3 201 -18 minecraft:podzol
fill -9 201 -17 -7 201 -15 minecraft:podzol
fill -4 201 -17 -2 201 -8 minecraft:podzol
fill -10 201 -16 -10 201 -15 minecraft:podzol
fill -6 201 -15 -5 201 -15 minecraft:podzol
fill -5 201 -14 -5 201 -8 minecraft:podzol
fill -15 201 -19 -15 206 -19 minecraft:andesite
fill -15 207 -19 -15 207 -19 minecraft:podzol
fill -17 201 -19 -16 206 -19 minecraft:stone
fill -17 207 -19 -16 207 -19 minecraft:podzol
fill -6 201 -17 -5 207 -16 minecraft:stone
fill -6 208 -17 -5 208 -16 minecraft:podzol
execute positioned -4 202 -18 run function rlk:room/prop/p_wildflower
execute positioned -9 201 -18 run function rlk:room/prop/p_grass
execute positioned -17 201 -2 run function rlk:room/prop/p_grass
execute positioned -5 202 -11 run function rlk:room/prop/p_grass
execute positioned -12 201 -8 run function rlk:room/prop/p_wildflower
execute positioned -8 201 -11 run function rlk:room/prop/p_wildflower
execute positioned -5 202 -9 run function rlk:room/prop/p_wildflower
execute positioned -18 201 -17 run function rlk:room/prop/p_wildflower
execute positioned -7 201 -5 run function rlk:room/prop/p_wildflower
setblock -16 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock -15 208 -19 minecraft:short_grass keep
setblock -6 209 -17 minecraft:azalea_leaves[persistent=true] keep
setblock -5 209 -16 minecraft:azalea_leaves[persistent=true] keep
