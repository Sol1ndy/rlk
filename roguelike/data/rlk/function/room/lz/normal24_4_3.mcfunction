# 구역 건설 (normal24_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -18 200 -38 -16 200 -36 minecraft:coarse_dirt
fill -12 200 -31 -11 200 -30 minecraft:gravel
fill -20 207 -26 -20 210 -21 minecraft:mossy_cobblestone
fill -20 208 -30 -20 210 -29 minecraft:tuff
fill -20 209 -23 -20 210 -21 minecraft:granite
fill -1 208 -35 -1 209 -31 minecraft:mossy_cobblestone
fill -1 210 -27 -1 210 -24 minecraft:oak_leaves[persistent=true]
fill -1 205 -29 -1 207 -29 minecraft:moss_block
fill -1 204 -34 -1 207 -32 minecraft:mossy_cobblestone
fill -1 204 -36 -1 206 -34 minecraft:cobblestone
fill -6 209 -40 -1 210 -40 minecraft:moss_block
fill -8 203 -40 -3 205 -40 minecraft:moss_block
fill -12 204 -40 -8 205 -40 minecraft:andesite
fill -12 205 -40 -9 206 -40 minecraft:cobblestone
fill -13 206 -21 -9 206 -21 minecraft:moss_block
fill -14 210 -21 -9 210 -21 minecraft:oak_leaves[persistent=true]
fill -10 209 -21 -6 210 -21 minecraft:oak_leaves[persistent=true]
fill -9 203 -21 -8 205 -21 minecraft:cobblestone
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -7 201 -39 -7 201 -35 minecraft:podzol
fill -6 201 -35 -6 201 -35 minecraft:podzol
fill -5 201 -34 -5 201 -33 minecraft:podzol
fill -4 201 -33 -2 201 -33 minecraft:podzol
fill -6 201 -39 -5 201 -39 minecraft:dirt
fill -6 202 -39 -5 202 -39 minecraft:podzol
fill -6 201 -38 -6 201 -36 minecraft:dirt
fill -6 202 -38 -6 202 -36 minecraft:podzol
fill -5 201 -35 -5 201 -35 minecraft:dirt
fill -5 202 -35 -5 202 -35 minecraft:podzol
fill -4 201 -34 -2 201 -34 minecraft:dirt
fill -4 202 -34 -2 202 -34 minecraft:podzol
fill -4 201 -39 -2 202 -35 minecraft:dirt
fill -4 203 -39 -2 203 -35 minecraft:podzol
fill -5 201 -38 -5 202 -36 minecraft:dirt
fill -5 203 -38 -5 203 -36 minecraft:podzol
fill -11 201 -37 -10 207 -37 minecraft:andesite
fill -11 208 -37 -10 208 -37 minecraft:podzol
fill -7 201 -22 -7 207 -22 minecraft:andesite
fill -7 208 -22 -7 208 -22 minecraft:podzol
fill -11 201 -36 -10 207 -36 minecraft:stone
fill -11 208 -36 -10 208 -36 minecraft:podzol
fill -7 201 -23 -2 207 -23 minecraft:stone
fill -7 208 -23 -2 208 -23 minecraft:podzol
fill -6 201 -22 -2 207 -22 minecraft:stone
fill -6 208 -22 -2 208 -22 minecraft:podzol
execute positioned -13 201 -25 run function rlk:room/prop/p_pillar_ruin
execute positioned -16 201 -35 run function rlk:room/prop/p_fence_x
execute positioned -3 201 -28 run function rlk:room/prop/p_boulder
execute positioned -11 201 -24 run function rlk:room/prop/p_boulder_s
execute positioned -5 202 -34 run function rlk:room/prop/p_pillar_ruin
execute positioned -9 201 -38 run function rlk:room/prop/p_dandelion
execute positioned -9 201 -39 run function rlk:room/prop/p_wildflower
execute positioned -18 201 -29 run function rlk:room/prop/p_litter
execute positioned -19 201 -33 run function rlk:room/prop/p_grass
execute positioned -11 201 -24 run function rlk:room/prop/p_dandelion
execute positioned -2 201 -26 run function rlk:room/prop/p_dandelion
execute positioned -7 201 -31 run function rlk:room/prop/p_grass
execute positioned -4 201 -24 run function rlk:room/prop/p_grass
setblock -10 209 -36 minecraft:azalea_leaves[persistent=true] keep
setblock -7 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock -6 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock -6 209 -22 minecraft:short_grass keep
setblock -5 209 -22 minecraft:short_grass keep
setblock -4 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock -4 209 -22 minecraft:short_grass keep
setblock -3 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock -3 209 -22 minecraft:azalea_leaves[persistent=true] keep
setblock -2 209 -23 minecraft:azalea_leaves[persistent=true] keep
setblock -2 209 -22 minecraft:azalea_leaves[persistent=true] keep
