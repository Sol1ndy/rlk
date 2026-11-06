# 구역 건설 (normal28_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -1 210 -2 minecraft:air
fill -19 209 -19 -1 209 -2 minecraft:light[level=15]
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 0 201 -19 18 210 -2 minecraft:air
fill 0 209 -19 18 209 -2 minecraft:light[level=15]
fill -13 200 -19 -10 200 -17 minecraft:moss_block
fill 12 200 -17 16 200 -16 minecraft:rooted_dirt
fill 10 200 -11 13 200 -10 minecraft:moss_block
fill -20 203 -13 -20 204 -13 minecraft:mossy_cobblestone
fill -20 209 -11 -20 209 -6 minecraft:cobblestone
fill -20 205 -17 -20 207 -16 minecraft:cobblestone
fill -20 201 -3 -20 201 -2 minecraft:moss_block
fill -20 204 -5 -20 204 -3 minecraft:andesite
fill -20 209 -2 -20 210 -2 minecraft:mossy_cobblestone
fill -9 210 -20 -4 210 -20 minecraft:moss_block
fill -5 203 -20 -3 206 -20 minecraft:mossy_cobblestone
fill -20 202 -20 -16 202 -20 minecraft:andesite
fill -6 209 -1 -5 210 -1 minecraft:mossy_cobblestone
fill -7 201 -1 -5 202 -1 minecraft:moss_block
fill -6 209 -1 -5 210 -1 minecraft:oak_leaves[persistent=true]
fill -17 205 -1 -12 206 -1 minecraft:moss_block
fill -12 206 -1 -7 207 -1 minecraft:cobblestone
fill 19 209 -18 19 210 -15 minecraft:oak_leaves[persistent=true]
fill 19 206 -9 19 207 -6 minecraft:mossy_cobblestone
fill 19 209 -9 19 210 -6 minecraft:oak_leaves[persistent=true]
fill 9 210 -20 9 210 -20 minecraft:andesite
fill 11 201 -20 13 201 -20 minecraft:cobblestone
fill 1 206 -20 2 208 -20 minecraft:granite
fill 9 210 -20 13 210 -20 minecraft:oak_leaves[persistent=true]
fill 4 201 -20 7 202 -20 minecraft:andesite
fill 16 204 -20 17 206 -20 minecraft:cobblestone
fill 6 208 -1 8 209 -1 minecraft:moss_block
fill 3 201 -1 7 202 -1 minecraft:cobblestone
fill 16 207 -1 16 209 -1 minecraft:moss_block
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -1 210 -2 minecraft:air
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 0 210 -19 18 210 -2 minecraft:air
fill -17 201 -19 -17 201 -15 minecraft:podzol
fill -16 201 -14 -15 201 -14 minecraft:podzol
fill -19 201 -13 -16 201 -13 minecraft:podzol
fill -19 201 -8 -18 201 -7 minecraft:podzol
fill -17 201 -7 -17 201 -2 minecraft:podzol
fill 5 201 -7 5 201 -7 minecraft:podzol
fill -1 201 -5 3 201 -5 minecraft:podzol
fill -2 201 -4 -1 201 -2 minecraft:podzol
fill 3 201 -4 3 201 -2 minecraft:podzol
fill -19 201 -19 -18 201 -14 minecraft:dirt
fill -19 202 -19 -18 202 -14 minecraft:podzol
fill -17 201 -14 -17 201 -14 minecraft:dirt
fill -17 202 -14 -17 202 -14 minecraft:podzol
fill -19 201 -6 -18 201 -2 minecraft:dirt
fill -19 202 -6 -18 202 -2 minecraft:podzol
fill 0 201 -4 2 201 -2 minecraft:dirt
fill 0 202 -4 2 202 -2 minecraft:podzol
fill -10 201 -12 -9 205 -11 minecraft:stone
fill -10 206 -12 -9 206 -11 minecraft:podzol
fill -11 201 -11 -11 205 -10 minecraft:stone
fill -11 206 -11 -11 206 -10 minecraft:podzol
fill -10 201 -10 -10 205 -10 minecraft:stone
fill -10 206 -10 -10 206 -10 minecraft:podzol
fill -2 201 -19 1 206 -19 minecraft:stone
fill -2 207 -19 1 207 -19 minecraft:podzol
fill -17 201 -12 -16 207 -11 minecraft:stone
fill -17 208 -12 -16 208 -11 minecraft:podzol
fill 5 186 -20 10 199 -10 minecraft:stone
fill 6 186 -19 9 186 -11 minecraft:dirt
fill 6 187 -19 9 188 -11 minecraft:azalea_leaves[persistent=true]
fill 6 189 -19 9 201 -11 minecraft:air
execute positioned -9 201 -8 run function rlk:room/prop/p_crates
execute positioned 13 201 -12 run function rlk:room/prop/p_hay
execute positioned -10 201 -5 run function rlk:room/prop/p_birch
execute positioned -6 201 -5 run function rlk:room/prop/p_hay
execute positioned -5 201 -12 run function rlk:room/prop/p_pillar_ruin
execute positioned 3 201 -16 run function rlk:room/prop/p_oak
execute positioned -16 201 -4 run function rlk:room/prop/p_pillar_ruin
execute positioned 11 201 -2 run function rlk:room/prop/p_wildflower
execute positioned 12 201 -9 run function rlk:room/prop/p_dandelion
execute positioned 10 201 -3 run function rlk:room/prop/p_grass
execute positioned 1 201 -8 run function rlk:room/prop/p_dandelion
execute positioned -12 201 -2 run function rlk:room/prop/p_dandelion
execute positioned 16 201 -15 run function rlk:room/prop/p_wildflower
execute positioned -15 201 -13 run function rlk:room/prop/p_litter
execute positioned -11 201 -3 run function rlk:room/prop/p_grass
execute positioned -19 202 -13 run function rlk:room/prop/p_wildflower
execute positioned -5 201 -4 run function rlk:room/prop/p_grass
execute positioned -16 201 -8 run function rlk:room/prop/p_litter
execute positioned 6 201 -9 run function rlk:room/prop/p_wildflower
execute positioned -17 202 -5 run function rlk:room/prop/p_dandelion
execute positioned -7 201 -15 run function rlk:room/prop/p_grass
execute positioned 10 201 -7 run function rlk:room/prop/p_litter
setblock -17 209 -12 minecraft:azalea_leaves[persistent=true] keep
setblock -17 209 -11 minecraft:azalea_leaves[persistent=true] keep
setblock -16 209 -12 minecraft:azalea_leaves[persistent=true] keep
setblock -16 209 -11 minecraft:short_grass keep
setblock -11 207 -11 minecraft:azalea_leaves[persistent=true] keep
setblock -11 207 -10 minecraft:short_grass keep
setblock -10 207 -12 minecraft:azalea_leaves[persistent=true] keep
setblock -10 207 -11 minecraft:azalea_leaves[persistent=true] keep
setblock -10 207 -10 minecraft:azalea_leaves[persistent=true] keep
setblock -9 207 -12 minecraft:azalea_leaves[persistent=true] keep
setblock -1 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 0 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock 1 208 -19 minecraft:short_grass keep
