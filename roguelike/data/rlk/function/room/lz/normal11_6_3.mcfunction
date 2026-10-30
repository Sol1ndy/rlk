# 구역 건설 (normal11_6, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 210 39 minecraft:stone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -31 200 24 -30 200 27 minecraft:coarse_dirt
fill -29 200 30 -26 200 32 minecraft:gravel
fill -40 210 26 -40 210 31 minecraft:oak_leaves[persistent=true]
fill -40 210 22 -40 210 26 minecraft:oak_leaves[persistent=true]
fill -40 210 35 -40 210 38 minecraft:oak_leaves[persistent=true]
fill -21 206 30 -21 207 35 minecraft:granite
fill -21 209 21 -21 210 24 minecraft:oak_leaves[persistent=true]
fill -21 209 37 -21 210 37 minecraft:oak_leaves[persistent=true]
fill -21 210 35 -21 210 39 minecraft:oak_leaves[persistent=true]
fill -29 204 20 -26 207 20 minecraft:mossy_cobblestone
fill -31 210 20 -28 210 20 minecraft:oak_leaves[persistent=true]
fill -25 209 20 -24 210 20 minecraft:oak_leaves[persistent=true]
fill -34 210 20 -32 210 20 minecraft:moss_block
fill -30 205 20 -26 208 20 minecraft:tuff
fill -37 209 39 -34 209 39 minecraft:moss_block
fill -33 208 39 -28 210 39 minecraft:cobblestone
fill -25 210 39 -23 210 39 minecraft:oak_leaves[persistent=true]
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -29 201 35 -27 201 38 minecraft:podzol
fill -26 201 36 -22 201 38 minecraft:podzol
fill -34 201 38 -30 206 38 minecraft:stone
fill -34 207 38 -30 207 38 minecraft:podzol
execute positioned -37 201 26 run function rlk:room/prop/p_ruin_z
execute positioned -25 202 36 run function rlk:room/prop/p_ruin_z
execute positioned -39 201 33 run function rlk:room/prop/p_pillar_ruin
execute positioned -28 201 22 run function rlk:room/prop/p_grass
execute positioned -22 201 29 run function rlk:room/prop/p_grass
execute positioned -36 201 31 run function rlk:room/prop/p_grass
execute positioned -24 201 24 run function rlk:room/prop/p_wildflower
execute positioned -22 201 29 run function rlk:room/prop/p_dandelion
execute positioned -22 201 34 run function rlk:room/prop/p_grass
execute positioned -35 201 34 run function rlk:room/prop/p_grass
execute positioned -34 201 21 run function rlk:room/prop/p_grass
setblock -33 208 38 minecraft:azalea_leaves[persistent=true] keep
setblock -32 208 38 minecraft:short_grass keep
setblock -30 208 38 minecraft:azalea_leaves[persistent=true] keep
