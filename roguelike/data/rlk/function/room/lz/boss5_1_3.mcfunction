# 구역 건설 (boss5_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -9 200 8 -8 200 9 minecraft:moss_block
fill -20 204 18 -20 205 18 minecraft:mossy_cobblestone
fill -20 202 16 -20 204 18 minecraft:cobblestone
fill -20 208 11 -20 208 15 minecraft:mossy_cobblestone
fill -20 204 11 -20 204 14 minecraft:granite
fill -20 202 6 -20 205 11 minecraft:moss_block
fill -20 205 9 -20 205 13 minecraft:andesite
fill -1 210 10 -1 210 10 minecraft:oak_leaves[persistent=true]
fill -1 203 7 -1 204 9 minecraft:mossy_cobblestone
fill -1 203 9 -1 206 12 minecraft:andesite
fill -1 209 10 -1 210 15 minecraft:oak_leaves[persistent=true]
fill -14 209 0 -9 210 0 minecraft:oak_leaves[persistent=true]
fill -3 205 0 -2 207 0 minecraft:mossy_cobblestone
fill -17 207 0 -16 209 0 minecraft:granite
fill -11 203 0 -10 203 0 minecraft:andesite
fill -5 204 0 -5 207 0 minecraft:mossy_cobblestone
fill -15 210 19 -13 210 19 minecraft:mossy_cobblestone
fill -17 202 19 -14 202 19 minecraft:moss_block
fill -18 203 19 -16 206 19 minecraft:tuff
fill -14 207 19 -10 209 19 minecraft:cobblestone
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -4 201 11 -2 201 12 minecraft:podzol
fill -5 201 12 -5 201 14 minecraft:podzol
fill -7 201 15 -6 201 16 minecraft:podzol
fill -6 201 17 -5 201 18 minecraft:podzol
fill -4 201 18 -2 201 18 minecraft:podzol
fill -4 201 13 -2 201 17 minecraft:dirt
fill -4 202 13 -2 202 17 minecraft:podzol
fill -5 201 15 -5 201 16 minecraft:dirt
fill -5 202 15 -5 202 16 minecraft:podzol
fill -3 201 6 -2 205 7 minecraft:andesite
fill -3 206 6 -2 206 7 minecraft:podzol
fill -3 201 3 -2 205 5 minecraft:stone
fill -3 206 3 -2 206 5 minecraft:podzol
execute positioned -7 201 18 run function rlk:room/prop/p_pillar_ruin
execute positioned -2 201 2 run function rlk:room/prop/p_grass
execute positioned -11 201 16 run function rlk:room/prop/p_wildflower
execute positioned -12 201 13 run function rlk:room/prop/p_grass
execute positioned -14 201 5 run function rlk:room/prop/p_dandelion
execute positioned -3 202 12 run function rlk:room/prop/p_grass
execute positioned -12 201 9 run function rlk:room/prop/p_wildflower
execute positioned -19 201 13 run function rlk:room/prop/p_grass
setblock -3 207 3 minecraft:azalea_leaves[persistent=true] keep
setblock -3 207 4 minecraft:short_grass keep
setblock -3 207 6 minecraft:short_grass keep
setblock -3 207 7 minecraft:short_grass keep
setblock -2 207 4 minecraft:short_grass keep
