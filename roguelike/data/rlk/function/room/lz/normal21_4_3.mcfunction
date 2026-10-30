# 구역 건설 (normal21_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -1 210 -22 minecraft:air
fill -19 209 -39 -1 209 -22 minecraft:light[level=15]
fill 0 200 -40 19 200 -21 minecraft:podzol
fill 0 201 -40 19 210 -21 minecraft:stone
fill 0 201 -39 18 210 -22 minecraft:air
fill 0 209 -39 18 209 -22 minecraft:light[level=15]
fill -18 200 -32 -15 200 -29 minecraft:moss_block
fill 0 200 -36 2 200 -33 minecraft:rooted_dirt
fill -20 205 -26 -20 208 -25 minecraft:tuff
fill -20 203 -34 -20 204 -29 minecraft:andesite
fill -20 207 -36 -20 210 -35 minecraft:andesite
fill -20 209 -26 -20 210 -26 minecraft:moss_block
fill -5 207 -40 -5 208 -40 minecraft:cobblestone
fill -16 201 -40 -13 204 -40 minecraft:andesite
fill -20 201 -40 -18 202 -40 minecraft:moss_block
fill -2 206 -40 -2 207 -40 minecraft:cobblestone
fill -8 202 -21 -6 204 -21 minecraft:cobblestone
fill -1 204 -21 -1 207 -21 minecraft:andesite
fill -6 202 -21 -4 204 -21 minecraft:andesite
fill -12 201 -21 -12 203 -21 minecraft:mossy_cobblestone
fill 19 209 -33 19 210 -32 minecraft:andesite
fill 19 203 -28 19 205 -25 minecraft:tuff
fill 5 209 -40 6 210 -40 minecraft:moss_block
fill 11 201 -40 12 201 -40 minecraft:moss_block
fill 7 204 -40 11 204 -40 minecraft:andesite
fill 17 201 -40 19 204 -40 minecraft:moss_block
fill 13 201 -40 15 204 -40 minecraft:granite
fill 1 203 -21 6 205 -21 minecraft:moss_block
fill 13 209 -21 16 210 -21 minecraft:oak_leaves[persistent=true]
fill 4 202 -21 8 203 -21 minecraft:moss_block
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -1 210 -22 minecraft:air
fill 0 210 -40 19 210 -21 minecraft:polished_deepslate
fill 0 210 -39 18 210 -22 minecraft:air
fill 5 201 -33 7 201 -27 minecraft:podzol
fill 8 201 -32 8 201 -27 minecraft:podzol
fill 10 201 -32 10 201 -27 minecraft:podzol
fill 9 201 -31 9 201 -27 minecraft:podzol
fill 11 201 -31 11 201 -27 minecraft:podzol
fill -8 201 -30 -5 201 -30 minecraft:podzol
fill -6 201 -29 -5 201 -22 minecraft:podzol
fill -4 201 -25 -1 201 -24 minecraft:podzol
fill -4 201 -23 -3 201 -22 minecraft:podzol
fill 9 201 -34 9 207 -32 minecraft:andesite
fill 9 208 -34 9 208 -32 minecraft:podzol
fill 10 201 -33 10 207 -33 minecraft:andesite
fill 10 208 -33 10 208 -33 minecraft:podzol
fill 0 201 -22 1 207 -22 minecraft:andesite
fill 0 208 -22 1 208 -22 minecraft:podzol
fill -11 201 -34 -10 207 -33 minecraft:stone
fill -11 208 -34 -10 208 -33 minecraft:podzol
fill 8 201 -33 8 207 -33 minecraft:stone
fill 8 208 -33 8 208 -33 minecraft:podzol
fill -2 201 -23 1 207 -23 minecraft:stone
fill -2 208 -23 1 208 -23 minecraft:podzol
fill -2 201 -22 -1 207 -22 minecraft:stone
fill -2 208 -22 -1 208 -22 minecraft:podzol
fill -13 186 -28 -8 199 -21 minecraft:stone
fill -20 186 -27 -12 199 -21 minecraft:stone
fill -12 186 -27 -9 186 -22 minecraft:dirt
fill -12 187 -27 -9 188 -22 minecraft:azalea_leaves[persistent=true]
fill -12 189 -27 -9 201 -22 minecraft:air
fill -19 186 -26 -13 186 -22 minecraft:dirt
fill -19 187 -26 -13 188 -22 minecraft:azalea_leaves[persistent=true]
fill -19 189 -26 -13 201 -22 minecraft:air
execute positioned -16 201 -30 run function rlk:room/prop/p_shrub_tree
execute positioned -2 201 -35 run function rlk:room/prop/p_boulder_s
execute positioned -7 201 -35 run function rlk:room/prop/p_boulder_s
execute positioned -4 201 -37 run function rlk:room/prop/p_boulder_s
execute positioned 16 201 -26 run function rlk:room/prop/p_ruin_x
execute positioned 14 201 -33 run function rlk:room/prop/p_ruin_z
execute positioned 9 202 -29 run function rlk:room/prop/p_ruin_x
execute positioned -15 201 -32 run function rlk:room/prop/p_grass
execute positioned -11 201 -25 run function rlk:room/prop/p_grass
execute positioned 13 201 -27 run function rlk:room/prop/p_grass
execute positioned -14 201 -23 run function rlk:room/prop/p_wildflower
execute positioned 13 201 -22 run function rlk:room/prop/p_grass
execute positioned 7 201 -39 run function rlk:room/prop/p_grass
execute positioned 17 201 -22 run function rlk:room/prop/p_grass
execute positioned -17 201 -36 run function rlk:room/prop/p_wildflower
execute positioned -4 201 -28 run function rlk:room/prop/p_wildflower
execute positioned 15 201 -28 run function rlk:room/prop/p_wildflower
execute positioned 17 201 -38 run function rlk:room/prop/p_dandelion
execute positioned -12 201 -35 run function rlk:room/prop/p_litter
execute positioned -13 201 -24 run function rlk:room/prop/p_dandelion
execute positioned -6 202 -28 run function rlk:room/prop/p_grass
execute positioned 3 201 -30 run function rlk:room/prop/p_grass
setblock -11 209 -33 minecraft:azalea_leaves[persistent=true] keep
setblock -10 209 -34 minecraft:azalea_leaves[persistent=true] keep
setblock -10 209 -33 minecraft:short_grass keep
setblock -2 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock -2 209 -22 minecraft:short_grass keep
setblock -1 209 -23 minecraft:short_grass keep
setblock -1 209 -22 minecraft:azalea_leaves[persistent=true] keep
setblock 0 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock 0 209 -22 minecraft:azalea_leaves[persistent=true] keep
setblock 1 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock 8 209 -33 minecraft:short_grass keep
setblock 9 209 -34 minecraft:short_grass keep
