# 구역 건설 (first3_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -6 200 8 -2 200 9 minecraft:gravel
fill -20 206 15 -20 208 18 minecraft:mossy_cobblestone
fill -20 203 9 -20 203 12 minecraft:andesite
fill -20 208 6 -20 210 9 minecraft:andesite
fill -1 206 8 -1 206 11 minecraft:moss_block
fill -1 209 6 -1 210 10 minecraft:oak_leaves[persistent=true]
fill -1 206 3 -1 209 5 minecraft:tuff
fill -2 204 0 -1 204 0 minecraft:moss_block
fill -1 201 0 -1 201 0 minecraft:moss_block
fill -16 202 0 -15 203 0 minecraft:moss_block
fill -10 210 0 -9 210 0 minecraft:oak_leaves[persistent=true]
fill -16 208 0 -16 210 0 minecraft:moss_block
fill -14 209 0 -10 210 0 minecraft:tuff
fill -19 210 19 -19 210 19 minecraft:mossy_cobblestone
fill -16 209 19 -14 210 19 minecraft:oak_leaves[persistent=true]
fill -11 207 19 -9 207 19 minecraft:moss_block
fill -5 205 19 -1 205 19 minecraft:moss_block
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -17 201 7 -15 201 13 minecraft:podzol
fill -18 201 8 -18 201 12 minecraft:podzol
fill -5 201 18 -2 206 18 minecraft:stone
fill -5 207 18 -2 207 18 minecraft:podzol
execute positioned -17 202 8 run function rlk:room/prop/p_pillar_ruin
execute positioned -19 201 3 run function rlk:room/prop/p_boulder_s
execute positioned -19 201 8 run function rlk:room/prop/p_wildflower
execute positioned -6 201 1 run function rlk:room/prop/p_wildflower
execute positioned -13 201 18 run function rlk:room/prop/p_litter
execute positioned -14 201 10 run function rlk:room/prop/p_wildflower
execute positioned -11 201 12 run function rlk:room/prop/p_grass
execute positioned -13 201 5 run function rlk:room/prop/p_litter
execute positioned -14 201 7 run function rlk:room/prop/p_litter
setblock -5 208 18 minecraft:azalea_leaves[persistent=true] keep
setblock -4 208 18 minecraft:azalea_leaves[persistent=true] keep
setblock -2 208 18 minecraft:azalea_leaves[persistent=true] keep
