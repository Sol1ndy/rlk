# 구역 건설 (normal11_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -40 -21 200 -21 minecraft:podzol
fill -40 201 -40 -21 210 -21 minecraft:stone
fill -39 201 -39 -22 210 -22 minecraft:air
fill -39 209 -39 -22 209 -22 minecraft:light[level=15]
fill -38 200 -30 -35 200 -29 minecraft:moss_block
fill -40 204 -40 -40 204 -36 minecraft:andesite
fill -40 208 -37 -40 210 -36 minecraft:andesite
fill -40 209 -28 -40 210 -23 minecraft:oak_leaves[persistent=true]
fill -40 210 -35 -40 210 -33 minecraft:mossy_cobblestone
fill -40 201 -27 -40 202 -26 minecraft:moss_block
fill -21 201 -26 -21 202 -22 minecraft:andesite
fill -21 210 -33 -21 210 -30 minecraft:mossy_cobblestone
fill -21 206 -35 -21 207 -32 minecraft:moss_block
fill -31 205 -40 -29 205 -40 minecraft:moss_block
fill -31 205 -40 -27 205 -40 minecraft:mossy_cobblestone
fill -25 201 -40 -25 202 -40 minecraft:mossy_cobblestone
fill -30 207 -40 -29 208 -40 minecraft:moss_block
fill -27 201 -40 -26 202 -40 minecraft:cobblestone
fill -36 208 -21 -32 208 -21 minecraft:moss_block
fill -23 210 -21 -23 210 -21 minecraft:oak_leaves[persistent=true]
fill -31 209 -21 -31 210 -21 minecraft:oak_leaves[persistent=true]
fill -37 205 -21 -32 207 -21 minecraft:moss_block
fill -34 206 -21 -34 208 -21 minecraft:moss_block
fill -40 210 -40 -21 210 -21 minecraft:polished_deepslate
fill -39 210 -39 -22 210 -22 minecraft:air
fill -28 201 -39 -27 201 -39 minecraft:podzol
fill -23 201 -39 -22 201 -39 minecraft:podzol
fill -28 201 -38 -28 201 -35 minecraft:podzol
fill -22 201 -38 -22 201 -37 minecraft:podzol
fill -29 201 -37 -29 201 -37 minecraft:podzol
fill -26 201 -37 -23 201 -37 minecraft:podzol
fill -27 201 -36 -27 201 -35 minecraft:podzol
fill -38 201 -28 -37 201 -22 minecraft:podzol
fill -36 201 -27 -36 201 -27 minecraft:podzol
fill -39 201 -24 -39 201 -22 minecraft:podzol
fill -26 201 -39 -24 201 -38 minecraft:dirt
fill -26 202 -39 -24 202 -38 minecraft:podzol
fill -27 201 -38 -27 201 -37 minecraft:dirt
fill -27 202 -38 -27 202 -37 minecraft:podzol
fill -23 201 -38 -23 201 -38 minecraft:dirt
fill -23 202 -38 -23 202 -38 minecraft:podzol
fill -37 201 -36 -37 207 -36 minecraft:andesite
fill -37 208 -36 -37 208 -36 minecraft:podzol
fill -39 201 -29 -39 207 -27 minecraft:andesite
fill -39 208 -29 -39 208 -27 minecraft:podzol
fill -37 201 -37 -36 207 -37 minecraft:stone
fill -37 208 -37 -36 208 -37 minecraft:podzol
fill -36 201 -36 -36 207 -36 minecraft:stone
fill -36 208 -36 -36 208 -36 minecraft:podzol
fill -39 201 -26 -39 207 -25 minecraft:stone
fill -39 208 -26 -39 208 -25 minecraft:podzol
execute positioned -31 201 -37 run function rlk:room/prop/p_hay
execute positioned -33 201 -35 run function rlk:room/prop/p_lantern
execute positioned -27 203 -37 run function rlk:room/prop/p_pillar_ruin
execute positioned -37 201 -33 run function rlk:room/prop/p_oak
execute positioned -39 201 -39 run function rlk:room/prop/p_pillar_ruin
execute positioned -37 201 -35 run function rlk:room/prop/p_litter
execute positioned -29 201 -23 run function rlk:room/prop/p_grass
execute positioned -24 202 -37 run function rlk:room/prop/p_wildflower
execute positioned -32 201 -26 run function rlk:room/prop/p_grass
execute positioned -33 201 -38 run function rlk:room/prop/p_wildflower
execute positioned -38 202 -24 run function rlk:room/prop/p_litter
execute positioned -26 203 -39 run function rlk:room/prop/p_dandelion
setblock -39 209 -29 minecraft:azalea_leaves[persistent=true] keep
setblock -39 209 -28 minecraft:azalea_leaves[persistent=true] keep
setblock -39 209 -27 minecraft:azalea_leaves[persistent=true] keep
setblock -39 209 -26 minecraft:azalea_leaves[persistent=true] keep
setblock -37 209 -37 minecraft:azalea_leaves[persistent=true] keep
setblock -37 209 -36 minecraft:azalea_leaves[persistent=true] keep
setblock -36 209 -37 minecraft:short_grass keep
