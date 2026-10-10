# 구역 건설 (levelup5_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 40 -21 200 59 minecraft:podzol
fill -40 201 40 -21 210 59 minecraft:stone
fill -39 201 41 -22 210 58 minecraft:air
fill -39 209 41 -22 209 58 minecraft:light[level=15]
fill -38 200 50 -35 200 52 minecraft:moss_block
fill -40 201 54 -40 204 56 minecraft:tuff
fill -40 210 43 -40 210 46 minecraft:oak_leaves[persistent=true]
fill -40 203 40 -40 204 40 minecraft:moss_block
fill -21 204 51 -21 206 55 minecraft:tuff
fill -21 204 41 -21 204 42 minecraft:tuff
fill -21 207 46 -21 208 46 minecraft:cobblestone
fill -21 201 51 -21 202 52 minecraft:andesite
fill -21 208 42 -21 209 44 minecraft:andesite
fill -21 202 52 -21 204 56 minecraft:moss_block
fill -38 202 40 -36 202 40 minecraft:moss_block
fill -39 209 40 -34 210 40 minecraft:mossy_cobblestone
fill -39 210 40 -34 210 40 minecraft:oak_leaves[persistent=true]
fill -35 203 40 -35 204 40 minecraft:granite
fill -36 207 40 -31 210 40 minecraft:andesite
fill -29 203 40 -25 205 40 minecraft:moss_block
fill -21 209 59 -21 210 59 minecraft:oak_leaves[persistent=true]
fill -36 206 59 -34 208 59 minecraft:andesite
fill -36 204 59 -34 206 59 minecraft:andesite
fill -37 201 59 -35 202 59 minecraft:andesite
fill -26 209 59 -22 210 59 minecraft:oak_leaves[persistent=true]
fill -26 206 59 -25 208 59 minecraft:cobblestone
fill -40 210 40 -21 210 59 minecraft:polished_deepslate
fill -39 210 41 -22 210 58 minecraft:air
fill -39 201 41 -37 201 41 minecraft:podzol
fill -37 201 42 -37 201 45 minecraft:podzol
fill -36 201 46 -35 201 46 minecraft:podzol
fill -35 201 47 -35 201 48 minecraft:podzol
fill -36 201 48 -36 201 48 minecraft:podzol
fill -39 201 49 -37 201 49 minecraft:podzol
fill -39 201 42 -38 201 42 minecraft:dirt
fill -39 202 42 -38 202 42 minecraft:podzol
fill -38 201 43 -38 201 45 minecraft:dirt
fill -38 202 43 -38 202 45 minecraft:podzol
fill -37 201 46 -37 201 46 minecraft:dirt
fill -37 202 46 -37 202 46 minecraft:podzol
fill -36 201 47 -36 201 47 minecraft:dirt
fill -36 202 47 -36 202 47 minecraft:podzol
fill -39 201 48 -37 201 48 minecraft:dirt
fill -39 202 48 -37 202 48 minecraft:podzol
fill -39 201 43 -39 202 47 minecraft:dirt
fill -39 203 43 -39 203 47 minecraft:podzol
fill -38 201 46 -38 202 47 minecraft:dirt
fill -38 203 46 -38 203 47 minecraft:podzol
fill -37 201 47 -37 202 47 minecraft:dirt
fill -37 203 47 -37 203 47 minecraft:podzol
fill -33 201 57 -31 206 57 minecraft:andesite
fill -33 207 57 -31 207 57 minecraft:podzol
fill -34 201 58 -34 206 58 minecraft:andesite
fill -34 207 58 -34 207 58 minecraft:podzol
fill -34 201 57 -34 206 57 minecraft:stone
fill -34 207 57 -34 207 57 minecraft:podzol
fill -30 201 57 -30 206 58 minecraft:stone
fill -30 207 57 -30 207 58 minecraft:podzol
fill -33 201 58 -31 206 58 minecraft:stone
fill -33 207 58 -31 207 58 minecraft:podzol
fill -25 186 47 -21 199 59 minecraft:stone
fill -24 186 48 -22 186 58 minecraft:dirt
fill -24 187 48 -22 188 58 minecraft:azalea_leaves[persistent=true]
fill -24 189 48 -22 201 58 minecraft:air
execute positioned -36 201 52 run function rlk:room/prop/p_boulder
execute positioned -39 201 50 run function rlk:room/prop/p_boulder_s
execute positioned -27 201 56 run function rlk:room/prop/p_shrub_tree
execute positioned -30 201 52 run function rlk:room/prop/p_dandelion
execute positioned -32 201 47 run function rlk:room/prop/p_grass
execute positioned -26 201 56 run function rlk:room/prop/p_grass
execute positioned -29 201 41 run function rlk:room/prop/p_wildflower
execute positioned -38 201 51 run function rlk:room/prop/p_grass
execute positioned -35 201 42 run function rlk:room/prop/p_grass
execute positioned -32 201 55 run function rlk:room/prop/p_grass
execute positioned -36 201 42 run function rlk:room/prop/p_dandelion
setblock -34 208 57 minecraft:short_grass keep
setblock -33 208 57 minecraft:azalea_leaves[persistent=true] keep
setblock -32 208 57 minecraft:short_grass keep
setblock -32 208 58 minecraft:short_grass keep
setblock -31 208 58 minecraft:azalea_leaves[persistent=true] keep
setblock -30 208 57 minecraft:short_grass keep
setblock -30 208 58 minecraft:azalea_leaves[persistent=true] keep
