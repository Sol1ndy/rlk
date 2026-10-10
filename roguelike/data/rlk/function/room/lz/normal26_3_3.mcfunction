# 구역 건설 (normal26_3, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -40 -21 200 -21 minecraft:podzol
fill -40 201 -40 -21 210 -21 minecraft:stone
fill -39 201 -39 -22 210 -22 minecraft:air
fill -39 209 -39 -22 209 -22 minecraft:light[level=15]
fill -23 200 -30 -22 200 -27 minecraft:rooted_dirt
fill -26 200 -24 -24 200 -23 minecraft:moss_block
fill -40 203 -35 -40 204 -35 minecraft:moss_block
fill -40 206 -33 -40 208 -33 minecraft:mossy_cobblestone
fill -40 210 -39 -40 210 -34 minecraft:oak_leaves[persistent=true]
fill -21 204 -26 -21 207 -25 minecraft:mossy_cobblestone
fill -21 210 -40 -21 210 -35 minecraft:oak_leaves[persistent=true]
fill -21 210 -29 -21 210 -29 minecraft:oak_leaves[persistent=true]
fill -21 202 -36 -21 205 -31 minecraft:mossy_cobblestone
fill -33 204 -40 -32 207 -40 minecraft:moss_block
fill -40 204 -40 -37 206 -40 minecraft:moss_block
fill -30 206 -40 -30 208 -40 minecraft:andesite
fill -35 206 -40 -33 208 -40 minecraft:moss_block
fill -33 206 -40 -31 208 -40 minecraft:mossy_cobblestone
fill -30 210 -40 -25 210 -40 minecraft:tuff
fill -32 210 -21 -32 210 -21 minecraft:mossy_cobblestone
fill -24 206 -21 -21 206 -21 minecraft:cobblestone
fill -29 210 -21 -29 210 -21 minecraft:moss_block
fill -40 210 -40 -21 210 -21 minecraft:polished_deepslate
fill -39 210 -39 -22 210 -22 minecraft:air
fill -34 201 -39 -34 201 -35 minecraft:podzol
fill -29 201 -39 -29 201 -36 minecraft:podzol
fill -25 201 -39 -25 201 -37 minecraft:podzol
fill -28 201 -38 -28 201 -38 minecraft:podzol
fill -24 201 -37 -22 201 -37 minecraft:podzol
fill -30 201 -36 -30 201 -35 minecraft:podzol
fill -33 201 -35 -31 201 -35 minecraft:podzol
fill -33 201 -39 -30 201 -38 minecraft:dirt
fill -33 202 -39 -30 202 -38 minecraft:podzol
fill -24 201 -39 -23 201 -38 minecraft:dirt
fill -24 202 -39 -23 202 -38 minecraft:podzol
fill -22 201 -38 -22 201 -38 minecraft:dirt
fill -22 202 -38 -22 202 -38 minecraft:podzol
fill -33 201 -37 -33 201 -36 minecraft:dirt
fill -33 202 -37 -33 202 -36 minecraft:podzol
fill -30 201 -37 -30 201 -37 minecraft:dirt
fill -30 202 -37 -30 202 -37 minecraft:podzol
fill -22 201 -39 -22 202 -39 minecraft:dirt
fill -22 203 -39 -22 203 -39 minecraft:podzol
fill -39 201 -29 -39 206 -27 minecraft:andesite
fill -39 207 -29 -39 207 -27 minecraft:podzol
fill -39 201 -26 -39 206 -26 minecraft:stone
fill -39 207 -26 -39 207 -26 minecraft:podzol
fill -32 201 -37 -31 207 -36 minecraft:andesite
fill -32 208 -37 -31 208 -36 minecraft:podzol
fill -40 186 -40 -36 199 -33 minecraft:stone
fill -39 186 -39 -37 186 -34 minecraft:dirt
fill -39 187 -39 -37 188 -34 minecraft:azalea_leaves[persistent=true]
fill -39 189 -39 -37 201 -34 minecraft:air
execute positioned -36 201 -35 run function rlk:room/prop/p_crates
execute positioned -36 201 -27 run function rlk:room/prop/p_shrub_tree
execute positioned -37 201 -31 run function rlk:room/prop/p_birch
execute positioned -27 201 -27 run function rlk:room/prop/p_grass
execute positioned -25 201 -24 run function rlk:room/prop/p_grass
execute positioned -29 201 -34 run function rlk:room/prop/p_dandelion
execute positioned -24 201 -23 run function rlk:room/prop/p_grass
execute positioned -24 201 -29 run function rlk:room/prop/p_grass
execute positioned -38 201 -32 run function rlk:room/prop/p_wildflower
execute positioned -32 201 -25 run function rlk:room/prop/p_dandelion
execute positioned -30 201 -29 run function rlk:room/prop/p_grass
execute positioned -25 201 -32 run function rlk:room/prop/p_dandelion
setblock -39 208 -29 minecraft:azalea_leaves[persistent=true] keep
setblock -39 208 -28 minecraft:short_grass keep
setblock -39 208 -27 minecraft:azalea_leaves[persistent=true] keep
setblock -39 208 -26 minecraft:azalea_leaves[persistent=true] keep
setblock -32 209 -37 minecraft:short_grass keep
setblock -32 209 -36 minecraft:azalea_leaves[persistent=true] keep
setblock -31 209 -37 minecraft:azalea_leaves[persistent=true] keep
