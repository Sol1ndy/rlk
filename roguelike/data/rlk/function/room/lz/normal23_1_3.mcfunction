# 구역 건설 (normal23_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -13 200 2 -9 200 4 minecraft:rooted_dirt
fill -8 200 8 -4 200 9 minecraft:coarse_dirt
fill -20 206 9 -20 206 9 minecraft:andesite
fill -20 206 10 -20 208 14 minecraft:mossy_cobblestone
fill -20 210 13 -20 210 16 minecraft:mossy_cobblestone
fill -1 207 9 -1 207 10 minecraft:andesite
fill -1 210 17 -1 210 19 minecraft:oak_leaves[persistent=true]
fill -1 209 2 -1 210 6 minecraft:andesite
fill -8 206 0 -5 207 0 minecraft:andesite
fill -4 209 0 -3 210 0 minecraft:oak_leaves[persistent=true]
fill -16 210 0 -16 210 0 minecraft:oak_leaves[persistent=true]
fill -5 208 0 -2 210 0 minecraft:andesite
fill -5 202 19 -4 202 19 minecraft:moss_block
fill -10 209 19 -6 210 19 minecraft:moss_block
fill -14 210 19 -10 210 19 minecraft:mossy_cobblestone
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -4 201 1 -2 201 3 minecraft:podzol
fill -18 201 8 -17 205 9 minecraft:andesite
fill -18 206 8 -17 206 9 minecraft:podzol
fill -19 201 8 -19 205 10 minecraft:stone
fill -19 206 8 -19 206 10 minecraft:podzol
fill -18 201 10 -17 205 10 minecraft:stone
fill -18 206 10 -17 206 10 minecraft:podzol
execute positioned -5 201 16 run function rlk:room/prop/p_boulder_s
execute positioned -5 201 9 run function rlk:room/prop/p_grass
execute positioned -9 201 12 run function rlk:room/prop/p_wildflower
execute positioned -8 201 14 run function rlk:room/prop/p_grass
execute positioned -6 201 15 run function rlk:room/prop/p_litter
execute positioned -18 201 1 run function rlk:room/prop/p_dandelion
execute positioned -10 201 11 run function rlk:room/prop/p_grass
execute positioned -6 201 15 run function rlk:room/prop/p_grass
execute positioned -12 201 9 run function rlk:room/prop/p_grass
execute positioned -7 201 1 run function rlk:room/prop/p_wildflower
setblock -18 207 8 minecraft:azalea_leaves[persistent=true] keep
setblock -18 207 9 minecraft:azalea_leaves[persistent=true] keep
setblock -18 207 10 minecraft:azalea_leaves[persistent=true] keep
setblock -17 207 8 minecraft:short_grass keep
setblock -17 207 9 minecraft:azalea_leaves[persistent=true] keep
