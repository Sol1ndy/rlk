# 구역 건설 (root2_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -16 200 -27 -14 200 -24 minecraft:moss_block
fill -10 200 -23 -7 200 -22 minecraft:coarse_dirt
fill -20 206 -29 -20 206 -25 minecraft:andesite
fill -20 203 -24 -20 204 -23 minecraft:mossy_cobblestone
fill -20 209 -36 -20 209 -36 minecraft:moss_block
fill -20 209 -27 -20 210 -23 minecraft:oak_leaves[persistent=true]
fill -1 209 -22 -1 210 -21 minecraft:mossy_cobblestone
fill -1 201 -38 -1 204 -35 minecraft:andesite
fill -1 210 -30 -1 210 -29 minecraft:granite
fill -1 202 -29 -1 203 -24 minecraft:andesite
fill -1 210 -33 -1 210 -32 minecraft:mossy_cobblestone
fill -1 206 -34 -1 209 -34 minecraft:moss_block
fill -16 202 -40 -16 205 -40 minecraft:tuff
fill -11 210 -40 -6 210 -40 minecraft:moss_block
fill -14 210 -40 -14 210 -40 minecraft:oak_leaves[persistent=true]
fill -9 204 -40 -5 204 -40 minecraft:cobblestone
fill -13 210 -40 -11 210 -40 minecraft:oak_leaves[persistent=true]
fill -7 209 -40 -3 210 -40 minecraft:oak_leaves[persistent=true]
fill -18 210 -21 -14 210 -21 minecraft:mossy_cobblestone
fill -16 205 -21 -14 205 -21 minecraft:moss_block
fill -10 203 -21 -7 206 -21 minecraft:moss_block
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -15 201 -38 -14 201 -38 minecraft:podzol
fill -16 201 -37 -15 201 -37 minecraft:podzol
fill -19 201 -36 -16 201 -36 minecraft:podzol
fill -19 201 -35 -17 201 -35 minecraft:podzol
fill -19 201 -27 -18 201 -26 minecraft:podzol
fill -17 201 -26 -17 201 -22 minecraft:podzol
fill -19 201 -39 -17 201 -37 minecraft:dirt
fill -19 202 -39 -17 202 -37 minecraft:podzol
fill -16 201 -38 -16 201 -38 minecraft:dirt
fill -16 202 -38 -16 202 -38 minecraft:podzol
fill -19 201 -25 -18 201 -22 minecraft:dirt
fill -19 202 -25 -18 202 -22 minecraft:podzol
fill -16 201 -39 -11 207 -39 minecraft:stone
fill -16 208 -39 -11 208 -39 minecraft:podzol
execute positioned -7 201 -35 run function rlk:room/prop/p_fence_x
execute positioned -7 201 -27 run function rlk:room/prop/p_wildflower
execute positioned -18 202 -27 run function rlk:room/prop/p_litter
execute positioned -4 201 -27 run function rlk:room/prop/p_wildflower
execute positioned -2 201 -26 run function rlk:room/prop/p_wildflower
execute positioned -7 201 -35 run function rlk:room/prop/p_grass
execute positioned -7 201 -35 run function rlk:room/prop/p_dandelion
setblock -16 209 -39 minecraft:short_grass keep
setblock -14 209 -39 minecraft:short_grass keep
setblock -13 209 -39 minecraft:azalea_leaves[persistent=true] keep
setblock -12 209 -39 minecraft:azalea_leaves[persistent=true] keep
setblock -11 209 -39 minecraft:azalea_leaves[persistent=true] keep
