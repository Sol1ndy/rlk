# 구역 건설 (normal13_7, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -9 200 -46 -8 200 -45 minecraft:gravel
fill -17 200 -54 -13 200 -53 minecraft:moss_block
fill -20 208 -59 -20 210 -59 minecraft:andesite
fill -20 209 -57 -20 210 -56 minecraft:oak_leaves[persistent=true]
fill -20 210 -54 -20 210 -49 minecraft:cobblestone
fill -20 209 -48 -20 210 -47 minecraft:mossy_cobblestone
fill -20 203 -60 -20 204 -60 minecraft:andesite
fill -1 203 -60 -1 203 -58 minecraft:tuff
fill -1 210 -49 -1 210 -48 minecraft:oak_leaves[persistent=true]
fill -1 210 -46 -1 210 -45 minecraft:oak_leaves[persistent=true]
fill -1 207 -55 -1 210 -52 minecraft:moss_block
fill -1 205 -60 -1 207 -58 minecraft:moss_block
fill -1 209 -54 -1 210 -52 minecraft:oak_leaves[persistent=true]
fill -2 209 -60 -1 209 -60 minecraft:moss_block
fill -19 203 -60 -19 204 -60 minecraft:tuff
fill -13 201 -60 -13 202 -60 minecraft:moss_block
fill -20 202 -41 -17 204 -41 minecraft:cobblestone
fill -6 209 -41 -4 210 -41 minecraft:cobblestone
fill -11 201 -41 -6 201 -41 minecraft:andesite
fill -10 208 -41 -8 210 -41 minecraft:moss_block
fill -8 205 -41 -7 207 -41 minecraft:granite
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -54 -18 201 -42 minecraft:podzol
fill -17 201 -46 -17 201 -43 minecraft:podzol
fill -12 201 -59 -9 205 -59 minecraft:andesite
fill -12 206 -59 -9 206 -59 minecraft:podzol
fill -14 201 -58 -13 205 -58 minecraft:andesite
fill -14 206 -58 -13 206 -58 minecraft:podzol
fill -14 201 -59 -13 205 -59 minecraft:stone
fill -14 206 -59 -13 206 -59 minecraft:podzol
fill -12 201 -58 -9 205 -58 minecraft:stone
fill -12 206 -58 -9 206 -58 minecraft:podzol
execute positioned -2 201 -49 run function rlk:room/prop/p_fence_z
execute positioned -16 201 -43 run function rlk:room/prop/p_grass
execute positioned -16 201 -55 run function rlk:room/prop/p_wildflower
execute positioned -3 201 -59 run function rlk:room/prop/p_dandelion
execute positioned -18 201 -57 run function rlk:room/prop/p_dandelion
execute positioned -19 202 -47 run function rlk:room/prop/p_dandelion
execute positioned -9 201 -52 run function rlk:room/prop/p_wildflower
setblock -14 207 -59 minecraft:azalea_leaves[persistent=true] keep
setblock -14 207 -58 minecraft:azalea_leaves[persistent=true] keep
setblock -12 207 -59 minecraft:short_grass keep
setblock -10 207 -58 minecraft:azalea_leaves[persistent=true] keep
setblock -9 207 -59 minecraft:short_grass keep
