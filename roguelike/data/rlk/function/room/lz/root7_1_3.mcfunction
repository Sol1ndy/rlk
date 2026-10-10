# 구역 건설 (root7_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill -8 200 -15 -5 200 -12 minecraft:gravel
fill -14 200 -14 -13 200 -11 minecraft:rooted_dirt
fill 3 200 -14 7 200 -13 minecraft:moss_block
fill -12 200 -13 -9 200 -10 minecraft:coarse_dirt
fill -20 209 -12 -20 210 -10 minecraft:moss_block
fill -20 209 -17 -20 209 -15 minecraft:granite
fill -20 201 -7 -20 204 -3 minecraft:mossy_cobblestone
fill -15 206 -20 -15 207 -20 minecraft:granite
fill -18 204 -20 -13 205 -20 minecraft:tuff
fill -19 205 -20 -18 206 -20 minecraft:mossy_cobblestone
fill -20 201 -20 -20 203 -20 minecraft:cobblestone
fill -19 209 -20 -14 210 -20 minecraft:oak_leaves[persistent=true]
fill -18 210 -1 -14 210 -1 minecraft:oak_leaves[persistent=true]
fill -6 206 -1 -5 209 -1 minecraft:andesite
fill -5 208 -1 -4 210 -1 minecraft:tuff
fill 19 208 -19 19 208 -19 minecraft:tuff
fill 19 205 -8 19 208 -4 minecraft:moss_block
fill 19 207 -15 19 209 -15 minecraft:moss_block
fill 19 201 -11 19 201 -11 minecraft:moss_block
fill 6 204 -20 8 205 -20 minecraft:moss_block
fill 4 204 -20 9 204 -20 minecraft:moss_block
fill 13 202 -20 17 204 -20 minecraft:tuff
fill 15 208 -20 16 210 -20 minecraft:moss_block
fill 13 203 -20 17 203 -20 minecraft:moss_block
fill 15 208 -1 19 209 -1 minecraft:andesite
fill 0 209 -1 4 210 -1 minecraft:cobblestone
fill 12 203 -1 15 203 -1 minecraft:mossy_cobblestone
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill 9 201 -19 15 201 -17 minecraft:podzol
fill 8 201 -18 8 201 -15 minecraft:podzol
fill 16 201 -18 16 201 -17 minecraft:podzol
fill 7 201 -17 7 201 -15 minecraft:podzol
fill 17 201 -17 17 201 -17 minecraft:podzol
fill 9 201 -16 13 201 -15 minecraft:podzol
fill -18 201 -8 -15 201 -7 minecraft:podzol
fill -19 201 -7 -19 201 -2 minecraft:podzol
fill -18 201 -6 -18 201 -6 minecraft:podzol
fill -14 201 -6 -10 201 -6 minecraft:podzol
fill -11 201 -5 -10 201 -2 minecraft:podzol
fill -17 201 -6 -15 201 -2 minecraft:dirt
fill -17 202 -6 -15 202 -2 minecraft:podzol
fill -18 201 -5 -18 201 -2 minecraft:dirt
fill -18 202 -5 -18 202 -2 minecraft:podzol
fill -14 201 -5 -12 201 -2 minecraft:dirt
fill -14 202 -5 -12 202 -2 minecraft:podzol
fill 3 201 -19 5 205 -19 minecraft:andesite
fill 3 206 -19 5 206 -19 minecraft:podzol
fill 2 201 -19 2 205 -18 minecraft:stone
fill 2 206 -19 2 206 -18 minecraft:podzol
fill 3 201 -18 5 205 -18 minecraft:stone
fill 3 206 -18 5 206 -18 minecraft:podzol
fill -9 201 -19 -7 206 -19 minecraft:andesite
fill -9 207 -19 -7 207 -19 minecraft:podzol
fill -11 201 -19 -10 206 -18 minecraft:stone
fill -11 207 -19 -10 207 -18 minecraft:podzol
fill -9 201 -18 -7 206 -18 minecraft:stone
fill -9 207 -18 -7 207 -18 minecraft:podzol
execute positioned -16 201 -17 run function rlk:room/prop/p_pillar_ruin
execute positioned -6 201 -9 run function rlk:room/prop/p_boulder_s
execute positioned -2 201 -4 run function rlk:room/prop/p_shrub_tree
execute positioned 6 201 -6 run function rlk:room/prop/p_oak
execute positioned -10 201 -9 run function rlk:room/prop/p_grass
execute positioned 17 201 -2 run function rlk:room/prop/p_grass
execute positioned -16 201 -9 run function rlk:room/prop/p_litter
execute positioned 2 201 -16 run function rlk:room/prop/p_grass
execute positioned 3 201 -10 run function rlk:room/prop/p_wildflower
execute positioned 15 201 -9 run function rlk:room/prop/p_litter
execute positioned -8 201 -6 run function rlk:room/prop/p_dandelion
execute positioned 16 201 -2 run function rlk:room/prop/p_wildflower
execute positioned -1 201 -16 run function rlk:room/prop/p_grass
execute positioned -12 201 -9 run function rlk:room/prop/p_dandelion
execute positioned 9 201 -7 run function rlk:room/prop/p_grass
execute positioned -2 201 -14 run function rlk:room/prop/p_wildflower
execute positioned 3 201 -9 run function rlk:room/prop/p_wildflower
execute positioned -17 201 -19 run function rlk:room/prop/p_grass
execute positioned 12 201 -11 run function rlk:room/prop/p_litter
execute positioned -13 201 -17 run function rlk:room/prop/p_wildflower
execute positioned 18 201 -5 run function rlk:room/prop/p_wildflower
execute positioned 5 201 -15 run function rlk:room/prop/p_grass
setblock -11 208 -18 minecraft:azalea_leaves[persistent=true] keep
setblock -10 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock -9 208 -18 minecraft:azalea_leaves[persistent=true] keep
setblock -8 208 -19 minecraft:short_grass keep
setblock -8 208 -18 minecraft:azalea_leaves[persistent=true] keep
setblock -7 208 -19 minecraft:short_grass keep
setblock 2 207 -18 minecraft:azalea_leaves[persistent=true] keep
setblock 3 207 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 3 207 -18 minecraft:azalea_leaves[persistent=true] keep
setblock 4 207 -18 minecraft:azalea_leaves[persistent=true] keep
setblock 5 207 -19 minecraft:azalea_leaves[persistent=true] keep
