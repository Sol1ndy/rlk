# 구역 건설 (root1_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 0 -21 200 19 minecraft:podzol
fill -40 201 0 -21 210 19 minecraft:stone
fill -39 201 1 -22 210 18 minecraft:air
fill -39 209 1 -22 209 18 minecraft:light[level=15]
fill -34 200 8 -32 200 10 minecraft:gravel
fill -30 200 14 -28 200 15 minecraft:rooted_dirt
fill -40 209 4 -40 210 7 minecraft:andesite
fill -40 209 1 -40 210 5 minecraft:oak_leaves[persistent=true]
fill -40 210 8 -40 210 12 minecraft:oak_leaves[persistent=true]
fill -40 205 1 -40 205 5 minecraft:tuff
fill -40 202 12 -40 202 16 minecraft:tuff
fill -21 209 17 -21 209 18 minecraft:mossy_cobblestone
fill -21 210 3 -21 210 4 minecraft:andesite
fill -21 204 4 -21 207 5 minecraft:cobblestone
fill -21 209 1 -21 210 4 minecraft:moss_block
fill -21 207 11 -21 208 16 minecraft:cobblestone
fill -32 208 0 -32 210 0 minecraft:andesite
fill -39 205 0 -38 207 0 minecraft:moss_block
fill -34 204 0 -33 206 0 minecraft:andesite
fill -28 209 0 -28 210 0 minecraft:oak_leaves[persistent=true]
fill -24 209 0 -23 210 0 minecraft:oak_leaves[persistent=true]
fill -29 210 0 -28 210 0 minecraft:oak_leaves[persistent=true]
fill -37 201 19 -37 202 19 minecraft:andesite
fill -39 208 19 -36 208 19 minecraft:andesite
fill -37 210 19 -34 210 19 minecraft:oak_leaves[persistent=true]
fill -37 206 19 -33 208 19 minecraft:andesite
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -39 210 1 -22 210 18 minecraft:air
fill -29 201 2 -29 201 5 minecraft:podzol
fill -34 201 5 -30 201 5 minecraft:podzol
fill -39 201 6 -39 201 7 minecraft:podzol
fill -37 201 6 -35 201 6 minecraft:podzol
fill -38 201 7 -38 201 8 minecraft:podzol
fill -39 201 1 -39 201 5 minecraft:dirt
fill -39 202 1 -39 202 5 minecraft:podzol
fill -31 201 1 -30 201 4 minecraft:dirt
fill -31 202 1 -30 202 4 minecraft:podzol
fill -38 201 4 -38 201 6 minecraft:dirt
fill -38 202 4 -38 202 6 minecraft:podzol
fill -32 201 4 -32 201 4 minecraft:dirt
fill -32 202 4 -32 202 4 minecraft:podzol
fill -37 201 5 -35 201 5 minecraft:dirt
fill -37 202 5 -35 202 5 minecraft:podzol
fill -38 201 1 -32 202 2 minecraft:dirt
fill -38 203 1 -32 203 2 minecraft:podzol
fill -38 201 3 -35 202 3 minecraft:dirt
fill -38 203 3 -35 203 3 minecraft:podzol
fill -32 201 3 -32 202 3 minecraft:dirt
fill -32 203 3 -32 203 3 minecraft:podzol
fill -37 201 4 -35 202 4 minecraft:dirt
fill -37 203 4 -35 203 4 minecraft:podzol
fill -29 201 1 -27 207 1 minecraft:stone
fill -29 208 1 -27 208 1 minecraft:podzol
fill -34 201 3 -33 207 4 minecraft:stone
fill -34 208 3 -33 208 4 minecraft:podzol
execute positioned -29 201 16 run function rlk:room/prop/p_oak
execute positioned -37 201 15 run function rlk:room/prop/p_crates
execute positioned -27 201 15 run function rlk:room/prop/p_grass
execute positioned -38 203 6 run function rlk:room/prop/p_grass
execute positioned -28 201 11 run function rlk:room/prop/p_litter
execute positioned -35 204 4 run function rlk:room/prop/p_litter
execute positioned -29 202 5 run function rlk:room/prop/p_dandelion
execute positioned -38 201 13 run function rlk:room/prop/p_grass
execute positioned -23 201 9 run function rlk:room/prop/p_litter
execute positioned -27 201 12 run function rlk:room/prop/p_grass
execute positioned -26 201 15 run function rlk:room/prop/p_grass
setblock -34 209 3 minecraft:short_grass keep
setblock -34 209 4 minecraft:short_grass keep
setblock -33 209 3 minecraft:short_grass keep
setblock -33 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock -29 209 1 minecraft:short_grass keep
setblock -28 209 1 minecraft:azalea_leaves[persistent=true] keep
setblock -27 209 1 minecraft:azalea_leaves[persistent=true] keep
