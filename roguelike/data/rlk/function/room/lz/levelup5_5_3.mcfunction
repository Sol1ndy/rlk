# 구역 건설 (levelup5_5, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -20 -41 200 -1 minecraft:podzol
fill -60 201 -20 -41 210 -1 minecraft:stone
fill -59 201 -19 -42 210 -2 minecraft:air
fill -59 209 -19 -42 209 -2 minecraft:light[level=15]
fill -46 200 -7 -45 200 -6 minecraft:rooted_dirt
fill -60 203 -19 -60 203 -14 minecraft:moss_block
fill -60 209 -17 -60 210 -14 minecraft:oak_leaves[persistent=true]
fill -60 210 -18 -60 210 -17 minecraft:cobblestone
fill -41 204 -14 -41 204 -13 minecraft:andesite
fill -41 201 -13 -41 201 -8 minecraft:tuff
fill -43 204 -20 -42 206 -20 minecraft:andesite
fill -60 209 -20 -56 210 -20 minecraft:oak_leaves[persistent=true]
fill -59 203 -20 -59 205 -20 minecraft:cobblestone
fill -46 208 -20 -45 210 -20 minecraft:tuff
fill -60 210 -1 -57 210 -1 minecraft:oak_leaves[persistent=true]
fill -59 208 -1 -55 210 -1 minecraft:moss_block
fill -60 210 -20 -41 210 -1 minecraft:polished_deepslate
fill -59 210 -19 -42 210 -2 minecraft:air
fill -58 201 -19 -58 201 -18 minecraft:podzol
fill -50 201 -19 -50 201 -18 minecraft:podzol
fill -59 201 -18 -59 201 -16 minecraft:podzol
fill -49 201 -18 -49 201 -16 minecraft:podzol
fill -58 201 -16 -58 201 -14 minecraft:podzol
fill -50 201 -16 -50 201 -15 minecraft:podzol
fill -54 201 -15 -51 201 -15 minecraft:podzol
fill -57 201 -14 -55 201 -14 minecraft:podzol
fill -58 201 -10 -58 201 -7 minecraft:podzol
fill -59 201 -9 -59 201 -8 minecraft:podzol
fill -57 201 -6 -57 201 -2 minecraft:podzol
fill -59 201 -4 -59 201 -3 minecraft:podzol
fill -58 201 -3 -58 201 -2 minecraft:podzol
fill -57 201 -19 -57 201 -15 minecraft:dirt
fill -57 202 -19 -57 202 -15 minecraft:podzol
fill -52 201 -19 -51 201 -19 minecraft:dirt
fill -52 202 -19 -51 202 -19 minecraft:podzol
fill -51 201 -18 -51 201 -16 minecraft:dirt
fill -51 202 -18 -51 202 -16 minecraft:podzol
fill -58 201 -17 -58 201 -17 minecraft:dirt
fill -58 202 -17 -58 202 -17 minecraft:podzol
fill -50 201 -17 -50 201 -17 minecraft:dirt
fill -50 202 -17 -50 202 -17 minecraft:podzol
fill -54 201 -16 -52 201 -16 minecraft:dirt
fill -54 202 -16 -52 202 -16 minecraft:podzol
fill -56 201 -15 -55 201 -15 minecraft:dirt
fill -56 202 -15 -55 202 -15 minecraft:podzol
fill -59 201 -7 -59 201 -5 minecraft:dirt
fill -59 202 -7 -59 202 -5 minecraft:podzol
fill -58 201 -6 -58 201 -4 minecraft:dirt
fill -58 202 -6 -58 202 -4 minecraft:podzol
fill -56 201 -18 -52 202 -17 minecraft:dirt
fill -56 203 -18 -52 203 -17 minecraft:podzol
fill -56 201 -16 -55 202 -16 minecraft:dirt
fill -56 203 -16 -55 203 -16 minecraft:podzol
fill -56 201 -19 -53 207 -19 minecraft:stone
fill -56 208 -19 -53 208 -19 minecraft:podzol
fill -48 201 -17 -47 207 -16 minecraft:stone
fill -48 208 -17 -47 208 -16 minecraft:podzol
execute positioned -57 203 -17 run function rlk:room/prop/p_ruin_z
execute positioned -46 201 -7 run function rlk:room/prop/p_dandelion
execute positioned -52 204 -17 run function rlk:room/prop/p_grass
execute positioned -46 201 -8 run function rlk:room/prop/p_grass
execute positioned -52 202 -15 run function rlk:room/prop/p_wildflower
execute positioned -59 201 -14 run function rlk:room/prop/p_litter
execute positioned -59 201 -13 run function rlk:room/prop/p_dandelion
setblock -56 209 -19 minecraft:azalea_leaves[persistent=true] keep
setblock -55 209 -19 minecraft:short_grass keep
setblock -53 209 -19 minecraft:short_grass keep
setblock -48 209 -17 minecraft:short_grass keep
setblock -47 209 -17 minecraft:azalea_leaves[persistent=true] keep
setblock -47 209 -16 minecraft:short_grass keep
