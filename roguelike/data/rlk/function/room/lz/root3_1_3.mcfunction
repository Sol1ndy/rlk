# 구역 건설 (root3_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill 4 200 -8 6 200 -6 minecraft:coarse_dirt
fill -12 200 -11 -10 200 -8 minecraft:coarse_dirt
fill -11 200 -9 -7 200 -7 minecraft:rooted_dirt
fill -2 200 -5 1 200 -4 minecraft:coarse_dirt
fill -2 200 -12 1 200 -10 minecraft:moss_block
fill 2 200 -14 3 200 -12 minecraft:gravel
fill 7 200 -14 9 200 -13 minecraft:rooted_dirt
fill -20 210 -20 -20 210 -18 minecraft:oak_leaves[persistent=true]
fill -20 209 -5 -20 209 -3 minecraft:moss_block
fill -20 204 -10 -20 205 -7 minecraft:mossy_cobblestone
fill -20 209 -20 -20 210 -15 minecraft:oak_leaves[persistent=true]
fill -20 209 -20 -20 210 -20 minecraft:andesite
fill -20 210 -6 -20 210 -6 minecraft:oak_leaves[persistent=true]
fill -15 206 -20 -15 207 -20 minecraft:tuff
fill -6 207 -20 -4 208 -20 minecraft:mossy_cobblestone
fill -12 202 -20 -10 204 -20 minecraft:andesite
fill -2 210 -20 -1 210 -20 minecraft:oak_leaves[persistent=true]
fill -10 210 -20 -5 210 -20 minecraft:oak_leaves[persistent=true]
fill -18 207 -1 -15 208 -1 minecraft:granite
fill -17 205 -1 -13 207 -1 minecraft:moss_block
fill -3 209 -1 -2 210 -1 minecraft:oak_leaves[persistent=true]
fill -7 204 -1 -6 205 -1 minecraft:mossy_cobblestone
fill -10 209 -1 -10 210 -1 minecraft:oak_leaves[persistent=true]
fill 19 209 -20 19 210 -18 minecraft:oak_leaves[persistent=true]
fill 19 203 -14 19 205 -9 minecraft:cobblestone
fill 19 203 -8 19 206 -8 minecraft:tuff
fill 19 209 -13 19 210 -9 minecraft:oak_leaves[persistent=true]
fill 19 210 -4 19 210 -2 minecraft:oak_leaves[persistent=true]
fill 19 204 -14 19 207 -9 minecraft:moss_block
fill 14 201 -20 14 202 -20 minecraft:moss_block
fill 0 203 -20 5 205 -20 minecraft:cobblestone
fill 0 201 -20 4 202 -20 minecraft:andesite
fill 14 208 -20 15 209 -20 minecraft:tuff
fill 3 206 -20 6 206 -20 minecraft:moss_block
fill 9 209 -20 14 210 -20 minecraft:oak_leaves[persistent=true]
fill 12 208 -1 12 209 -1 minecraft:granite
fill 3 201 -1 6 204 -1 minecraft:cobblestone
fill 10 210 -1 15 210 -1 minecraft:oak_leaves[persistent=true]
fill 6 210 -1 6 210 -1 minecraft:oak_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill -19 201 -19 -9 201 -17 minecraft:podzol
fill -1 201 -19 -1 201 -15 minecraft:podzol
fill 4 201 -19 9 201 -19 minecraft:podzol
fill 17 201 -19 18 201 -19 minecraft:podzol
fill 4 201 -18 8 201 -15 minecraft:podzol
fill 18 201 -18 18 201 -17 minecraft:podzol
fill 14 201 -17 17 201 -17 minecraft:podzol
fill -19 201 -16 -18 201 -14 minecraft:podzol
fill -15 201 -16 -9 201 -15 minecraft:podzol
fill 0 201 -16 3 201 -15 minecraft:podzol
fill 13 201 -16 13 201 -15 minecraft:podzol
fill 9 201 -15 12 201 -15 minecraft:podzol
fill -17 201 -14 -15 201 -12 minecraft:podzol
fill 5 201 -14 5 201 -13 minecraft:podzol
fill -18 201 -13 -18 201 -13 minecraft:podzol
fill 10 201 -19 16 201 -18 minecraft:dirt
fill 10 202 -19 16 202 -18 minecraft:podzol
fill 9 201 -18 9 201 -16 minecraft:dirt
fill 9 202 -18 9 202 -16 minecraft:podzol
fill 17 201 -18 17 201 -18 minecraft:dirt
fill 17 202 -18 17 202 -18 minecraft:podzol
fill 10 201 -17 13 201 -17 minecraft:dirt
fill 10 202 -17 13 202 -17 minecraft:podzol
fill 10 201 -16 12 201 -16 minecraft:dirt
fill 10 202 -16 12 202 -16 minecraft:podzol
fill 3 201 -19 3 206 -19 minecraft:andesite
fill 3 207 -19 3 207 -19 minecraft:podzol
fill 0 201 -19 2 206 -17 minecraft:stone
fill 0 207 -19 2 207 -17 minecraft:podzol
fill 3 201 -18 3 206 -17 minecraft:stone
fill 3 207 -18 3 207 -17 minecraft:podzol
fill -17 201 -16 -16 207 -15 minecraft:stone
fill -17 208 -16 -16 208 -15 minecraft:podzol
execute positioned 5 201 -6 run function rlk:room/prop/p_oak
execute positioned -9 201 -5 run function rlk:room/prop/p_shrub_tree
execute positioned 15 201 -4 run function rlk:room/prop/p_lantern
execute positioned 3 201 -4 run function rlk:room/prop/p_oak
execute positioned -2 201 -13 run function rlk:room/prop/p_grass
execute positioned 2 201 -2 run function rlk:room/prop/p_wildflower
execute positioned 6 202 -16 run function rlk:room/prop/p_wildflower
execute positioned 17 201 -11 run function rlk:room/prop/p_litter
execute positioned -1 201 -6 run function rlk:room/prop/p_grass
execute positioned -9 202 -17 run function rlk:room/prop/p_grass
execute positioned -4 201 -10 run function rlk:room/prop/p_dandelion
execute positioned 12 201 -2 run function rlk:room/prop/p_litter
execute positioned -13 202 -15 run function rlk:room/prop/p_grass
execute positioned 16 201 -8 run function rlk:room/prop/p_grass
execute positioned 1 201 -10 run function rlk:room/prop/p_grass
execute positioned -8 201 -12 run function rlk:room/prop/p_wildflower
execute positioned 4 201 -4 run function rlk:room/prop/p_grass
execute positioned -9 201 -13 run function rlk:room/prop/p_wildflower
execute positioned -9 201 -8 run function rlk:room/prop/p_grass
execute positioned 8 201 -9 run function rlk:room/prop/p_dandelion
setblock -16 209 -16 minecraft:short_grass keep
setblock 0 208 -19 minecraft:short_grass keep
setblock 1 208 -19 minecraft:short_grass keep
setblock 1 208 -18 minecraft:short_grass keep
setblock 1 208 -17 minecraft:azalea_leaves[persistent=true] keep
setblock 2 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 2 208 -17 minecraft:short_grass keep
setblock 3 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 3 208 -18 minecraft:azalea_leaves[persistent=true] keep
setblock 3 208 -17 minecraft:short_grass keep
