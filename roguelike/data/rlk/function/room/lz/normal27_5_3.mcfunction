# 구역 건설 (normal27_5, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -40 59 200 -21 minecraft:podzol
fill 40 201 -40 59 210 -21 minecraft:stone
fill 41 201 -39 58 210 -21 minecraft:air
fill 41 209 -39 58 209 -21 minecraft:light[level=15]
fill 40 200 -20 59 200 -1 minecraft:podzol
fill 40 201 -20 59 210 -1 minecraft:stone
fill 41 201 -20 58 210 -2 minecraft:air
fill 41 209 -20 58 209 -2 minecraft:light[level=15]
fill 47 200 -39 48 200 -36 minecraft:coarse_dirt
fill 49 200 -19 52 200 -16 minecraft:coarse_dirt
fill 42 200 -28 45 200 -25 minecraft:gravel
fill 43 200 -3 47 200 -2 minecraft:rooted_dirt
fill 41 200 -28 44 200 -25 minecraft:rooted_dirt
fill 40 210 -34 40 210 -31 minecraft:moss_block
fill 40 209 -29 40 210 -28 minecraft:cobblestone
fill 40 206 -40 40 207 -37 minecraft:cobblestone
fill 59 210 -28 59 210 -25 minecraft:oak_leaves[persistent=true]
fill 59 207 -39 59 210 -37 minecraft:andesite
fill 59 210 -35 59 210 -32 minecraft:oak_leaves[persistent=true]
fill 59 210 -29 59 210 -24 minecraft:mossy_cobblestone
fill 59 210 -34 59 210 -31 minecraft:oak_leaves[persistent=true]
fill 40 201 -40 43 203 -40 minecraft:andesite
fill 49 206 -40 54 209 -40 minecraft:moss_block
fill 40 210 -9 40 210 -4 minecraft:oak_leaves[persistent=true]
fill 40 206 -11 40 206 -9 minecraft:cobblestone
fill 59 205 -14 59 208 -9 minecraft:moss_block
fill 59 202 -8 59 205 -3 minecraft:tuff
fill 46 206 -1 47 208 -1 minecraft:moss_block
fill 57 205 -1 58 208 -1 minecraft:andesite
fill 50 209 -1 51 210 -1 minecraft:oak_leaves[persistent=true]
fill 49 202 -1 52 202 -1 minecraft:cobblestone
fill 40 210 -40 59 210 -21 minecraft:polished_deepslate
fill 41 210 -39 58 210 -21 minecraft:air
fill 40 210 -20 59 210 -1 minecraft:polished_deepslate
fill 41 210 -20 58 210 -2 minecraft:air
fill 45 201 -39 46 201 -37 minecraft:podzol
fill 41 201 -37 44 201 -37 minecraft:podzol
fill 46 201 -36 46 201 -35 minecraft:podzol
fill 46 201 -31 49 201 -31 minecraft:podzol
fill 46 201 -30 46 201 -25 minecraft:podzol
fill 49 201 -30 50 201 -25 minecraft:podzol
fill 47 201 -28 48 201 -25 minecraft:podzol
fill 42 201 -24 45 201 -22 minecraft:podzol
fill 41 201 -23 41 201 -22 minecraft:podzol
fill 45 201 -21 45 201 -16 minecraft:podzol
fill 46 201 -15 47 201 -15 minecraft:podzol
fill 47 201 -14 47 201 -12 minecraft:podzol
fill 41 201 -13 41 201 -11 minecraft:podzol
fill 45 201 -13 46 201 -12 minecraft:podzol
fill 42 201 -12 44 201 -11 minecraft:podzol
fill 45 201 -11 45 201 -11 minecraft:podzol
fill 41 201 -39 44 201 -38 minecraft:dirt
fill 41 202 -39 44 202 -38 minecraft:podzol
fill 44 201 -21 44 201 -13 minecraft:dirt
fill 44 202 -21 44 202 -13 minecraft:podzol
fill 41 201 -18 43 201 -14 minecraft:dirt
fill 41 202 -18 43 202 -14 minecraft:podzol
fill 45 201 -15 45 201 -14 minecraft:dirt
fill 45 202 -15 45 202 -14 minecraft:podzol
fill 46 201 -14 46 201 -14 minecraft:dirt
fill 46 202 -14 46 202 -14 minecraft:podzol
fill 42 201 -13 43 201 -13 minecraft:dirt
fill 42 202 -13 43 202 -13 minecraft:podzol
fill 47 201 -30 47 206 -29 minecraft:andesite
fill 47 207 -30 47 207 -29 minecraft:podzol
fill 48 201 -30 48 206 -29 minecraft:stone
fill 48 207 -30 48 207 -29 minecraft:podzol
fill 41 201 -21 41 207 -19 minecraft:andesite
fill 41 208 -21 41 208 -19 minecraft:podzol
fill 42 201 -21 43 207 -19 minecraft:stone
fill 42 208 -21 43 208 -19 minecraft:podzol
fill 52 186 -31 57 199 -26 minecraft:stone
fill 49 186 -15 54 199 -9 minecraft:stone
fill 53 186 -30 56 186 -27 minecraft:dirt
fill 53 187 -30 56 188 -27 minecraft:azalea_leaves[persistent=true]
fill 53 189 -30 56 201 -27 minecraft:air
fill 50 186 -14 53 186 -10 minecraft:dirt
fill 50 187 -14 53 188 -10 minecraft:azalea_leaves[persistent=true]
fill 50 189 -14 53 201 -10 minecraft:air
execute positioned 52 201 -37 run function rlk:room/prop/p_boulder_s
execute positioned 56 201 -5 run function rlk:room/prop/p_ruin_x
execute positioned 43 203 -15 run function rlk:room/prop/p_pillar_ruin
execute positioned 55 201 -8 run function rlk:room/prop/p_shrub_tree
execute positioned 55 201 -33 run function rlk:room/prop/p_oak
execute positioned 54 201 -39 run function rlk:room/prop/p_crates
execute positioned 46 201 -11 run function rlk:room/prop/p_pillar_ruin
execute positioned 55 201 -16 run function rlk:room/prop/p_pillar_ruin
execute positioned 48 201 -10 run function rlk:room/prop/p_boulder_s
execute positioned 41 201 -4 run function rlk:room/prop/p_pillar_ruin
execute positioned 57 201 -3 run function rlk:room/prop/p_grass
execute positioned 47 201 -39 run function rlk:room/prop/p_grass
execute positioned 49 201 -8 run function rlk:room/prop/p_grass
execute positioned 44 201 -35 run function rlk:room/prop/p_grass
execute positioned 56 201 -15 run function rlk:room/prop/p_grass
execute positioned 42 201 -26 run function rlk:room/prop/p_wildflower
execute positioned 44 203 -20 run function rlk:room/prop/p_dandelion
execute positioned 52 201 -36 run function rlk:room/prop/p_dandelion
execute positioned 43 203 -17 run function rlk:room/prop/p_wildflower
execute positioned 53 201 -25 run function rlk:room/prop/p_grass
execute positioned 45 202 -19 run function rlk:room/prop/p_litter
execute positioned 44 203 -13 run function rlk:room/prop/p_wildflower
execute positioned 56 201 -8 run function rlk:room/prop/p_wildflower
setblock 41 209 -21 minecraft:short_grass keep
setblock 41 209 -20 minecraft:short_grass keep
setblock 42 209 -20 minecraft:azalea_leaves[persistent=true] keep
setblock 43 209 -21 minecraft:azalea_leaves[persistent=true] keep
setblock 43 209 -20 minecraft:azalea_leaves[persistent=true] keep
setblock 43 209 -19 minecraft:short_grass keep
setblock 47 208 -30 minecraft:azalea_leaves[persistent=true] keep
setblock 47 208 -29 minecraft:azalea_leaves[persistent=true] keep
setblock 48 208 -30 minecraft:short_grass keep
setblock 48 208 -29 minecraft:azalea_leaves[persistent=true] keep
