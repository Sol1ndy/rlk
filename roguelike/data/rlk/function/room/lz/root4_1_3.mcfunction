# 구역 건설 (root4_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill 0 200 -7 4 200 -6 minecraft:moss_block
fill -4 200 -5 -2 200 -4 minecraft:gravel
fill -14 200 -18 -10 200 -17 minecraft:moss_block
fill 11 200 -6 12 200 -4 minecraft:rooted_dirt
fill -7 200 -13 -6 200 -12 minecraft:coarse_dirt
fill -20 202 -8 -20 203 -4 minecraft:cobblestone
fill -20 207 -11 -20 208 -10 minecraft:tuff
fill -20 203 -11 -20 203 -7 minecraft:mossy_cobblestone
fill -20 201 -12 -20 203 -9 minecraft:granite
fill -11 202 -20 -9 202 -20 minecraft:cobblestone
fill -10 207 -20 -5 210 -20 minecraft:moss_block
fill -15 208 -20 -14 210 -20 minecraft:tuff
fill -1 210 -20 -1 210 -20 minecraft:oak_leaves[persistent=true]
fill -3 205 -20 -2 205 -20 minecraft:moss_block
fill -6 203 -1 -1 205 -1 minecraft:moss_block
fill -12 210 -1 -11 210 -1 minecraft:oak_leaves[persistent=true]
fill -17 205 -1 -17 208 -1 minecraft:granite
fill -20 203 -1 -19 206 -1 minecraft:moss_block
fill -1 209 -1 -1 210 -1 minecraft:mossy_cobblestone
fill 19 209 -20 19 210 -19 minecraft:andesite
fill 19 209 -12 19 210 -8 minecraft:oak_leaves[persistent=true]
fill 19 202 -6 19 205 -5 minecraft:mossy_cobblestone
fill 0 204 -20 4 205 -20 minecraft:granite
fill 4 209 -20 4 210 -20 minecraft:oak_leaves[persistent=true]
fill 2 201 -20 4 203 -20 minecraft:moss_block
fill 17 201 -1 17 202 -1 minecraft:mossy_cobblestone
fill 6 210 -1 10 210 -1 minecraft:andesite
fill 11 206 -1 15 209 -1 minecraft:mossy_cobblestone
fill 5 205 -1 10 206 -1 minecraft:moss_block
fill 14 206 -1 15 208 -1 minecraft:andesite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill 10 201 -19 10 201 -15 minecraft:podzol
fill 9 201 -18 9 201 -15 minecraft:podzol
fill -2 201 -16 -1 201 -15 minecraft:podzol
fill -17 201 -15 -13 201 -15 minecraft:podzol
fill 0 201 -15 4 201 -15 minecraft:podzol
fill 6 201 -15 8 201 -15 minecraft:podzol
fill -18 201 -14 -15 201 -9 minecraft:podzol
fill 5 201 -14 5 201 -11 minecraft:podzol
fill -19 201 -13 -19 201 -10 minecraft:podzol
fill -16 201 -8 -15 201 -7 minecraft:podzol
fill -15 201 -6 -15 201 -4 minecraft:podzol
fill -16 201 -5 -16 201 -3 minecraft:podzol
fill -18 201 -3 -17 201 -2 minecraft:podzol
fill -19 201 -2 -19 201 -2 minecraft:podzol
fill 2 201 -19 3 201 -16 minecraft:dirt
fill 2 202 -19 3 202 -16 minecraft:podzol
fill 4 201 -18 8 201 -16 minecraft:dirt
fill 4 202 -18 8 202 -16 minecraft:podzol
fill 0 201 -16 1 201 -16 minecraft:dirt
fill 0 202 -16 1 202 -16 minecraft:podzol
fill 5 201 -15 5 201 -15 minecraft:dirt
fill 5 202 -15 5 202 -15 minecraft:podzol
fill -19 201 -9 -19 201 -3 minecraft:dirt
fill -19 202 -9 -19 202 -3 minecraft:podzol
fill -18 201 -8 -17 201 -4 minecraft:dirt
fill -18 202 -8 -17 202 -4 minecraft:podzol
fill -16 201 -6 -16 201 -6 minecraft:dirt
fill -16 202 -6 -16 202 -6 minecraft:podzol
fill 4 201 -19 5 207 -19 minecraft:andesite
fill 4 208 -19 5 208 -19 minecraft:podzol
fill -2 201 -19 1 207 -17 minecraft:stone
fill -2 208 -19 1 208 -17 minecraft:podzol
fill 6 201 -19 9 207 -19 minecraft:stone
fill 6 208 -19 9 208 -19 minecraft:podzol
execute positioned -14 201 -19 run function rlk:room/prop/p_fence_x
execute positioned -3 201 -3 run function rlk:room/prop/p_boulder
execute positioned -9 201 -6 run function rlk:room/prop/p_shrub_tree
execute positioned -10 201 -4 run function rlk:room/prop/p_oak
execute positioned -9 201 -17 run function rlk:room/prop/p_wildflower
execute positioned -4 201 -7 run function rlk:room/prop/p_grass
execute positioned 4 201 -3 run function rlk:room/prop/p_dandelion
execute positioned 0 201 -11 run function rlk:room/prop/p_wildflower
execute positioned 14 201 -4 run function rlk:room/prop/p_wildflower
execute positioned -3 201 -19 run function rlk:room/prop/p_grass
execute positioned 8 201 -4 run function rlk:room/prop/p_dandelion
execute positioned -5 201 -10 run function rlk:room/prop/p_dandelion
execute positioned -9 201 -13 run function rlk:room/prop/p_wildflower
execute positioned -3 201 -17 run function rlk:room/prop/p_dandelion
execute positioned -3 201 -16 run function rlk:room/prop/p_litter
execute positioned 10 202 -17 run function rlk:room/prop/p_wildflower
execute positioned 16 201 -13 run function rlk:room/prop/p_litter
execute positioned -16 201 -17 run function rlk:room/prop/p_wildflower
execute positioned -3 201 -7 run function rlk:room/prop/p_grass
setblock -2 209 -18 minecraft:azalea_leaves[persistent=true] keep
setblock -2 209 -17 minecraft:azalea_leaves[persistent=true] keep
setblock -1 209 -19 minecraft:azalea_leaves[persistent=true] keep
setblock -1 209 -17 minecraft:short_grass keep
setblock 0 209 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 -18 minecraft:short_grass keep
setblock 1 209 -17 minecraft:short_grass keep
setblock 4 209 -19 minecraft:short_grass keep
setblock 5 209 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 7 209 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 9 209 -19 minecraft:azalea_leaves[persistent=true] keep
