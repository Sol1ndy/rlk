# 구역 건설 (normal13_7, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 212 -41 minecraft:stone
fill -19 201 -59 -2 212 -42 minecraft:air
fill -19 211 -59 -2 211 -42 minecraft:light[level=15]
fill -9 202 -46 -8 202 -45 minecraft:gravel
fill -17 202 -54 -13 202 -53 minecraft:moss_block
fill -20 210 -59 -20 212 -59 minecraft:andesite
fill -20 211 -57 -20 212 -56 minecraft:oak_leaves[persistent=true]
fill -20 212 -54 -20 212 -49 minecraft:cobblestone
fill -20 211 -48 -20 212 -47 minecraft:mossy_cobblestone
fill -20 205 -60 -20 206 -60 minecraft:andesite
fill -1 205 -60 -1 205 -58 minecraft:tuff
fill -1 212 -49 -1 212 -48 minecraft:oak_leaves[persistent=true]
fill -1 212 -46 -1 212 -45 minecraft:oak_leaves[persistent=true]
fill -1 209 -55 -1 212 -52 minecraft:moss_block
fill -1 207 -60 -1 209 -58 minecraft:moss_block
fill -1 211 -54 -1 212 -52 minecraft:oak_leaves[persistent=true]
fill -2 211 -60 -1 211 -60 minecraft:moss_block
fill -19 205 -60 -19 206 -60 minecraft:tuff
fill -13 202 -60 -13 204 -60 minecraft:moss_block
fill -20 204 -41 -17 206 -41 minecraft:cobblestone
fill -6 211 -41 -4 212 -41 minecraft:cobblestone
fill -11 201 -41 -6 203 -41 minecraft:andesite
fill -10 210 -41 -8 212 -41 minecraft:moss_block
fill -10 202 -41 -8 202 -41 minecraft:tuff
fill -8 207 -41 -7 209 -41 minecraft:granite
fill -20 212 -60 -1 212 -41 minecraft:polished_deepslate
fill -19 212 -59 -2 212 -42 minecraft:air
fill -19 201 -59 -15 201 -55 minecraft:dirt
fill -19 202 -59 -15 202 -55 minecraft:podzol
fill -8 201 -59 -2 201 -42 minecraft:dirt
fill -8 202 -59 -2 202 -42 minecraft:podzol
fill -14 201 -57 -9 201 -42 minecraft:dirt
fill -14 202 -57 -9 202 -42 minecraft:podzol
fill -17 201 -54 -15 201 -47 minecraft:dirt
fill -17 202 -54 -15 202 -47 minecraft:podzol
fill -16 201 -46 -15 201 -42 minecraft:dirt
fill -16 202 -46 -15 202 -42 minecraft:podzol
fill -17 201 -42 -17 201 -42 minecraft:dirt
fill -17 202 -42 -17 202 -42 minecraft:podzol
fill -19 201 -54 -18 202 -42 minecraft:dirt
fill -19 203 -54 -18 203 -42 minecraft:podzol
fill -17 201 -46 -17 202 -43 minecraft:dirt
fill -17 203 -46 -17 203 -43 minecraft:podzol
fill -12 201 -59 -9 207 -59 minecraft:andesite
fill -12 208 -59 -9 208 -59 minecraft:podzol
fill -14 201 -58 -13 207 -58 minecraft:andesite
fill -14 208 -58 -13 208 -58 minecraft:podzol
fill -14 201 -59 -13 207 -59 minecraft:stone
fill -14 208 -59 -13 208 -59 minecraft:podzol
fill -12 201 -58 -9 207 -58 minecraft:stone
fill -12 208 -58 -9 208 -58 minecraft:podzol
execute positioned -2 203 -49 run function rlk:room/prop/p_fence_z
execute positioned -16 203 -43 run function rlk:room/prop/p_grass
execute positioned -16 203 -55 run function rlk:room/prop/p_wildflower
execute positioned -3 203 -59 run function rlk:room/prop/p_dandelion
execute positioned -18 203 -57 run function rlk:room/prop/p_dandelion
execute positioned -19 204 -47 run function rlk:room/prop/p_dandelion
execute positioned -9 203 -52 run function rlk:room/prop/p_wildflower
setblock -14 209 -59 minecraft:azalea_leaves[persistent=true] keep
setblock -14 209 -58 minecraft:azalea_leaves[persistent=true] keep
setblock -12 209 -59 minecraft:short_grass keep
setblock -10 209 -58 minecraft:azalea_leaves[persistent=true] keep
setblock -9 209 -59 minecraft:short_grass keep
