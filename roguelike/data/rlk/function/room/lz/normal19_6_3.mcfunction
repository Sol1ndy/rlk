# 구역 건설 (normal19_6, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 0 -41 200 19 minecraft:podzol
fill -60 201 0 -41 210 19 minecraft:stone
fill -59 201 1 -42 210 18 minecraft:air
fill -59 209 1 -42 209 18 minecraft:light[level=15]
fill -52 200 8 -49 200 11 minecraft:coarse_dirt
fill -60 210 16 -60 210 16 minecraft:oak_leaves[persistent=true]
fill -60 208 4 -60 210 8 minecraft:cobblestone
fill -60 203 1 -60 205 2 minecraft:tuff
fill -60 201 14 -60 202 17 minecraft:andesite
fill -60 205 0 -60 206 5 minecraft:andesite
fill -60 205 0 -60 206 5 minecraft:moss_block
fill -41 209 0 -41 210 0 minecraft:oak_leaves[persistent=true]
fill -41 203 9 -41 205 11 minecraft:moss_block
fill -41 208 10 -41 209 15 minecraft:tuff
fill -41 209 0 -41 209 1 minecraft:moss_block
fill -41 209 6 -41 210 7 minecraft:oak_leaves[persistent=true]
fill -41 210 14 -41 210 17 minecraft:oak_leaves[persistent=true]
fill -58 201 0 -54 203 0 minecraft:moss_block
fill -51 208 0 -50 209 0 minecraft:moss_block
fill -56 207 0 -55 209 0 minecraft:mossy_cobblestone
fill -56 207 19 -55 210 19 minecraft:mossy_cobblestone
fill -44 201 19 -41 201 19 minecraft:tuff
fill -50 204 19 -50 206 19 minecraft:andesite
fill -46 202 19 -41 204 19 minecraft:andesite
fill -50 209 19 -50 210 19 minecraft:mossy_cobblestone
fill -60 210 0 -41 210 19 minecraft:polished_deepslate
fill -59 210 1 -42 210 18 minecraft:air
fill -59 201 9 -57 201 9 minecraft:podzol
fill -57 201 10 -56 201 10 minecraft:podzol
fill -56 201 11 -56 201 14 minecraft:podzol
fill -57 201 14 -57 201 15 minecraft:podzol
fill -59 201 15 -58 201 15 minecraft:podzol
fill -59 201 10 -58 201 14 minecraft:dirt
fill -59 202 10 -58 202 14 minecraft:podzol
fill -57 201 11 -57 201 13 minecraft:dirt
fill -57 202 11 -57 202 13 minecraft:podzol
fill -54 201 18 -52 206 18 minecraft:andesite
fill -54 207 18 -52 207 18 minecraft:podzol
fill -51 201 3 -50 206 4 minecraft:stone
fill -51 207 3 -50 207 4 minecraft:podzol
fill -51 201 18 -51 206 18 minecraft:stone
fill -51 207 18 -51 207 18 minecraft:podzol
fill -56 201 3 -55 207 4 minecraft:stone
fill -56 208 3 -55 208 4 minecraft:podzol
fill -57 201 4 -57 207 5 minecraft:stone
fill -57 208 4 -57 208 5 minecraft:podzol
fill -56 201 5 -56 207 5 minecraft:stone
fill -56 208 5 -56 208 5 minecraft:podzol
execute positioned -57 201 16 run function rlk:room/prop/p_ruin_z
execute positioned -44 201 16 run function rlk:room/prop/p_birch
execute positioned -53 201 15 run function rlk:room/prop/p_birch
execute positioned -59 203 11 run function rlk:room/prop/p_hay
execute positioned -49 201 15 run function rlk:room/prop/p_crates
execute positioned -44 201 18 run function rlk:room/prop/p_grass
execute positioned -46 201 18 run function rlk:room/prop/p_grass
execute positioned -57 201 16 run function rlk:room/prop/p_grass
execute positioned -42 201 18 run function rlk:room/prop/p_dandelion
execute positioned -54 201 15 run function rlk:room/prop/p_grass
execute positioned -51 201 17 run function rlk:room/prop/p_grass
setblock -57 209 5 minecraft:short_grass keep
setblock -56 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock -56 209 5 minecraft:azalea_leaves[persistent=true] keep
setblock -55 209 4 minecraft:azalea_leaves[persistent=true] keep
setblock -54 208 18 minecraft:short_grass keep
setblock -52 208 18 minecraft:short_grass keep
setblock -51 208 3 minecraft:short_grass keep
setblock -51 208 18 minecraft:short_grass keep
setblock -50 208 4 minecraft:short_grass keep
