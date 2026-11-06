# 구역 건설 (normal25_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -1 minecraft:air
fill -39 209 -19 -22 209 -1 minecraft:light[level=15]
fill -40 200 0 -21 200 19 minecraft:podzol
fill -40 201 0 -21 210 19 minecraft:stone
fill -39 201 0 -22 210 18 minecraft:air
fill -39 209 0 -22 209 18 minecraft:light[level=15]
fill -35 200 -14 -32 200 -11 minecraft:gravel
fill -27 200 15 -25 200 18 minecraft:coarse_dirt
fill -28 200 -9 -27 200 -7 minecraft:coarse_dirt
fill -40 201 -3 -40 202 -2 minecraft:tuff
fill -40 209 -17 -40 210 -15 minecraft:oak_leaves[persistent=true]
fill -40 205 -17 -40 207 -13 minecraft:moss_block
fill -40 208 -10 -40 209 -8 minecraft:granite
fill -40 209 -14 -40 210 -9 minecraft:mossy_cobblestone
fill -21 206 -15 -21 209 -10 minecraft:moss_block
fill -21 203 -10 -21 206 -5 minecraft:tuff
fill -21 205 -5 -21 206 -5 minecraft:andesite
fill -34 208 -20 -33 208 -20 minecraft:granite
fill -35 206 -20 -34 206 -20 minecraft:cobblestone
fill -36 203 -20 -35 204 -20 minecraft:mossy_cobblestone
fill -35 210 -20 -31 210 -20 minecraft:oak_leaves[persistent=true]
fill -34 209 -20 -29 210 -20 minecraft:oak_leaves[persistent=true]
fill -39 204 -20 -39 206 -20 minecraft:mossy_cobblestone
fill -40 209 1 -40 210 6 minecraft:mossy_cobblestone
fill -40 201 1 -40 201 3 minecraft:moss_block
fill -40 210 14 -40 210 14 minecraft:oak_leaves[persistent=true]
fill -40 210 9 -40 210 13 minecraft:oak_leaves[persistent=true]
fill -40 203 15 -40 205 19 minecraft:moss_block
fill -21 210 15 -21 210 19 minecraft:oak_leaves[persistent=true]
fill -21 210 11 -21 210 12 minecraft:oak_leaves[persistent=true]
fill -21 201 18 -21 201 18 minecraft:moss_block
fill -21 202 5 -21 204 5 minecraft:moss_block
fill -36 206 19 -33 209 19 minecraft:andesite
fill -37 210 19 -32 210 19 minecraft:oak_leaves[persistent=true]
fill -30 204 19 -26 204 19 minecraft:andesite
fill -22 209 19 -21 210 19 minecraft:oak_leaves[persistent=true]
fill -34 206 19 -32 208 19 minecraft:cobblestone
fill -34 206 19 -31 209 19 minecraft:mossy_cobblestone
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -1 minecraft:air
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -39 210 0 -22 210 18 minecraft:air
fill -39 201 -3 -35 201 -3 minecraft:podzol
fill -35 201 -2 -35 201 7 minecraft:podzol
fill -39 201 5 -38 201 7 minecraft:podzol
fill -34 201 5 -30 201 5 minecraft:podzol
fill -34 201 6 -33 201 7 minecraft:podzol
fill -37 201 7 -36 201 7 minecraft:podzol
fill -39 201 -2 -36 201 -2 minecraft:dirt
fill -39 202 -2 -36 202 -2 minecraft:podzol
fill -36 201 -1 -36 201 4 minecraft:dirt
fill -36 202 -1 -36 202 4 minecraft:podzol
fill -36 201 6 -36 207 6 minecraft:andesite
fill -36 208 6 -36 208 6 minecraft:podzol
fill -39 201 -1 -37 207 4 minecraft:stone
fill -39 208 -1 -37 208 4 minecraft:podzol
fill -37 201 5 -36 207 5 minecraft:stone
fill -37 208 5 -36 208 5 minecraft:podzol
fill -37 201 6 -37 207 6 minecraft:stone
fill -37 208 6 -37 208 6 minecraft:podzol
fill -31 186 7 -27 199 19 minecraft:stone
fill -38 186 9 -33 199 17 minecraft:stone
fill -30 186 8 -28 186 18 minecraft:dirt
fill -30 187 8 -28 188 18 minecraft:azalea_leaves[persistent=true]
fill -30 189 8 -28 201 18 minecraft:air
fill -37 186 10 -34 186 16 minecraft:dirt
fill -37 187 10 -34 188 16 minecraft:azalea_leaves[persistent=true]
fill -37 189 10 -34 201 16 minecraft:air
execute positioned -34 201 -15 run function rlk:room/prop/p_fence_z
execute positioned -33 201 15 run function rlk:room/prop/p_pillar_ruin
execute positioned -35 201 -17 run function rlk:room/prop/p_lantern
execute positioned -28 201 -9 run function rlk:room/prop/p_birch
execute positioned -30 201 -6 run function rlk:room/prop/p_boulder_s
execute positioned -27 201 -11 run function rlk:room/prop/p_lantern
execute positioned -31 201 -12 run function rlk:room/prop/p_lantern
execute positioned -39 201 14 run function rlk:room/prop/p_boulder
execute positioned -27 201 15 run function rlk:room/prop/p_wildflower
execute positioned -23 201 -8 run function rlk:room/prop/p_grass
execute positioned -33 201 9 run function rlk:room/prop/p_grass
execute positioned -32 201 17 run function rlk:room/prop/p_wildflower
execute positioned -33 201 -9 run function rlk:room/prop/p_grass
execute positioned -25 201 -4 run function rlk:room/prop/p_wildflower
execute positioned -26 201 5 run function rlk:room/prop/p_wildflower
execute positioned -22 201 16 run function rlk:room/prop/p_grass
execute positioned -36 201 -4 run function rlk:room/prop/p_grass
execute positioned -29 201 15 run function rlk:room/prop/p_grass
execute positioned -22 201 17 run function rlk:room/prop/p_grass
execute positioned -22 201 5 run function rlk:room/prop/p_litter
execute positioned -22 201 -8 run function rlk:room/prop/p_grass
execute positioned -38 201 18 run function rlk:room/prop/p_grass
execute positioned -22 201 -19 run function rlk:room/prop/p_litter
setblock -39 209 -1 minecraft:short_grass keep
setblock -39 209 0 minecraft:short_grass keep
setblock -39 209 1 minecraft:short_grass keep
setblock -39 209 3 minecraft:short_grass keep
setblock -39 209 4 minecraft:short_grass keep
setblock -38 209 1 minecraft:short_grass keep
setblock -37 209 -1 minecraft:short_grass keep
setblock -37 209 2 minecraft:azalea_leaves[persistent=true] keep
setblock -37 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock -37 209 5 minecraft:short_grass keep
setblock -37 209 6 minecraft:short_grass keep
setblock -36 209 6 minecraft:azalea_leaves[persistent=true] keep
