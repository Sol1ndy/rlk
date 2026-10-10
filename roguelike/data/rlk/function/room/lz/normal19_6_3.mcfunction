# 구역 건설 (normal19_6, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 0 -41 200 19 minecraft:podzol
fill -60 201 0 -41 211 19 minecraft:stone
fill -59 201 1 -42 211 18 minecraft:air
fill -59 210 1 -42 210 18 minecraft:light[level=15]
fill -52 201 8 -49 201 11 minecraft:coarse_dirt
fill -60 211 16 -60 211 16 minecraft:oak_leaves[persistent=true]
fill -60 209 4 -60 211 8 minecraft:cobblestone
fill -60 204 1 -60 206 2 minecraft:tuff
fill -60 202 14 -60 203 17 minecraft:andesite
fill -60 206 0 -60 207 5 minecraft:andesite
fill -60 206 0 -60 207 5 minecraft:moss_block
fill -41 210 0 -41 211 0 minecraft:oak_leaves[persistent=true]
fill -41 204 9 -41 206 11 minecraft:moss_block
fill -41 209 10 -41 210 15 minecraft:tuff
fill -41 210 0 -41 210 1 minecraft:moss_block
fill -41 210 6 -41 211 7 minecraft:oak_leaves[persistent=true]
fill -41 211 14 -41 211 17 minecraft:oak_leaves[persistent=true]
fill -58 202 0 -54 204 0 minecraft:moss_block
fill -51 209 0 -50 210 0 minecraft:moss_block
fill -56 208 0 -55 210 0 minecraft:mossy_cobblestone
fill -56 208 19 -55 211 19 minecraft:mossy_cobblestone
fill -44 202 19 -41 202 19 minecraft:tuff
fill -50 205 19 -50 207 19 minecraft:andesite
fill -46 203 19 -41 205 19 minecraft:andesite
fill -50 210 19 -50 211 19 minecraft:mossy_cobblestone
fill -60 211 0 -41 211 19 minecraft:polished_deepslate
fill -59 211 1 -42 211 18 minecraft:air
fill -59 201 1 -42 201 2 minecraft:podzol
fill -59 201 3 -57 201 3 minecraft:podzol
fill -54 201 3 -52 201 17 minecraft:podzol
fill -49 201 3 -42 201 18 minecraft:podzol
fill -59 201 4 -58 201 8 minecraft:podzol
fill -55 201 5 -55 201 18 minecraft:podzol
fill -51 201 5 -50 201 17 minecraft:podzol
fill -57 201 6 -56 201 8 minecraft:podzol
fill -56 201 9 -56 201 9 minecraft:podzol
fill -56 201 15 -56 201 18 minecraft:podzol
fill -59 201 16 -57 201 18 minecraft:podzol
fill -50 201 18 -50 201 18 minecraft:podzol
fill -59 201 9 -57 201 9 minecraft:dirt
fill -59 202 9 -57 202 9 minecraft:podzol
fill -57 201 10 -56 201 10 minecraft:dirt
fill -57 202 10 -56 202 10 minecraft:podzol
fill -56 201 11 -56 201 14 minecraft:dirt
fill -56 202 11 -56 202 14 minecraft:podzol
fill -57 201 14 -57 201 15 minecraft:dirt
fill -57 202 14 -57 202 15 minecraft:podzol
fill -59 201 15 -58 201 15 minecraft:dirt
fill -59 202 15 -58 202 15 minecraft:podzol
fill -59 201 10 -58 202 14 minecraft:dirt
fill -59 203 10 -58 203 14 minecraft:podzol
fill -57 201 11 -57 202 13 minecraft:dirt
fill -57 203 11 -57 203 13 minecraft:podzol
fill -54 201 18 -52 207 18 minecraft:andesite
fill -54 208 18 -52 208 18 minecraft:podzol
fill -51 201 3 -50 207 4 minecraft:stone
fill -51 208 3 -50 208 4 minecraft:podzol
fill -51 201 18 -51 207 18 minecraft:stone
fill -51 208 18 -51 208 18 minecraft:podzol
fill -56 201 3 -55 208 4 minecraft:stone
fill -56 209 3 -55 209 4 minecraft:podzol
fill -57 201 4 -57 208 5 minecraft:stone
fill -57 209 4 -57 209 5 minecraft:podzol
fill -56 201 5 -56 208 5 minecraft:stone
fill -56 209 5 -56 209 5 minecraft:podzol
execute positioned -57 202 16 run function rlk:room/prop/p_ruin_z
execute positioned -44 202 16 run function rlk:room/prop/p_birch
execute positioned -53 202 15 run function rlk:room/prop/p_birch
execute positioned -59 204 11 run function rlk:room/prop/p_hay
execute positioned -49 202 15 run function rlk:room/prop/p_crates
execute positioned -44 202 18 run function rlk:room/prop/p_grass
execute positioned -46 202 18 run function rlk:room/prop/p_grass
execute positioned -57 202 16 run function rlk:room/prop/p_grass
execute positioned -42 202 18 run function rlk:room/prop/p_dandelion
execute positioned -54 202 15 run function rlk:room/prop/p_grass
execute positioned -51 202 17 run function rlk:room/prop/p_grass
setblock -57 210 5 minecraft:short_grass keep
setblock -56 210 4 minecraft:azalea_leaves[persistent=true] keep
setblock -56 210 5 minecraft:azalea_leaves[persistent=true] keep
setblock -55 210 4 minecraft:azalea_leaves[persistent=true] keep
setblock -54 209 18 minecraft:short_grass keep
setblock -52 209 18 minecraft:short_grass keep
setblock -51 209 3 minecraft:short_grass keep
setblock -51 209 18 minecraft:short_grass keep
setblock -50 209 4 minecraft:short_grass keep
