# 구역 건설 (levelup2_5, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -45 200 -33 -43 200 -30 minecraft:coarse_dirt
fill -54 200 -26 -53 200 -23 minecraft:gravel
fill -60 202 -25 -60 205 -21 minecraft:cobblestone
fill -60 209 -27 -60 210 -23 minecraft:oak_leaves[persistent=true]
fill -60 201 -37 -60 201 -33 minecraft:andesite
fill -41 204 -25 -41 207 -24 minecraft:tuff
fill -41 201 -22 -41 203 -21 minecraft:tuff
fill -41 210 -37 -41 210 -32 minecraft:tuff
fill -41 204 -32 -41 204 -27 minecraft:mossy_cobblestone
fill -58 201 -40 -53 203 -40 minecraft:andesite
fill -46 205 -40 -46 207 -40 minecraft:andesite
fill -59 203 -40 -55 203 -40 minecraft:tuff
fill -60 209 -40 -55 210 -40 minecraft:andesite
fill -59 206 -40 -57 207 -40 minecraft:moss_block
fill -59 209 -40 -54 210 -40 minecraft:oak_leaves[persistent=true]
fill -54 201 -21 -50 201 -21 minecraft:andesite
fill -57 207 -21 -54 209 -21 minecraft:moss_block
fill -55 209 -21 -53 210 -21 minecraft:oak_leaves[persistent=true]
fill -54 204 -21 -52 207 -21 minecraft:granite
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -59 201 -35 -56 201 -35 minecraft:podzol
fill -56 201 -34 -55 201 -34 minecraft:podzol
fill -55 201 -33 -55 201 -27 minecraft:podzol
fill -56 201 -27 -56 201 -27 minecraft:podzol
fill -57 201 -26 -57 201 -23 minecraft:podzol
fill -59 201 -23 -58 201 -23 minecraft:podzol
fill -59 201 -34 -57 201 -33 minecraft:dirt
fill -59 202 -34 -57 202 -33 minecraft:podzol
fill -56 201 -33 -56 201 -28 minecraft:dirt
fill -56 202 -33 -56 202 -28 minecraft:podzol
fill -57 201 -27 -57 201 -27 minecraft:dirt
fill -57 202 -27 -57 202 -27 minecraft:podzol
fill -58 201 -26 -58 201 -24 minecraft:dirt
fill -58 202 -26 -58 202 -24 minecraft:podzol
fill -59 201 -25 -59 201 -24 minecraft:dirt
fill -59 202 -25 -59 202 -24 minecraft:podzol
fill -59 201 -32 -57 202 -28 minecraft:dirt
fill -59 203 -32 -57 203 -28 minecraft:podzol
fill -59 201 -27 -58 202 -27 minecraft:dirt
fill -59 203 -27 -58 203 -27 minecraft:podzol
fill -59 201 -26 -59 202 -26 minecraft:dirt
fill -59 203 -26 -59 203 -26 minecraft:podzol
fill -51 201 -39 -50 205 -38 minecraft:andesite
fill -51 206 -39 -50 206 -38 minecraft:podzol
fill -54 201 -39 -52 205 -38 minecraft:stone
fill -54 206 -39 -52 206 -38 minecraft:podzol
fill -56 201 -37 -55 207 -37 minecraft:andesite
fill -56 208 -37 -55 208 -37 minecraft:podzol
fill -56 201 -36 -55 207 -36 minecraft:stone
fill -56 208 -36 -55 208 -36 minecraft:podzol
execute positioned -47 201 -36 run function rlk:room/prop/p_pillar_ruin
execute positioned -59 204 -32 run function rlk:room/prop/p_ruin_x
execute positioned -44 201 -37 run function rlk:room/prop/p_oak
execute positioned -58 203 -26 run function rlk:room/prop/p_grass
execute positioned -53 201 -27 run function rlk:room/prop/p_grass
execute positioned -48 201 -23 run function rlk:room/prop/p_dandelion
execute positioned -57 202 -35 run function rlk:room/prop/p_grass
execute positioned -57 201 -36 run function rlk:room/prop/p_wildflower
execute positioned -57 204 -29 run function rlk:room/prop/p_wildflower
execute positioned -57 204 -32 run function rlk:room/prop/p_litter
execute positioned -55 201 -26 run function rlk:room/prop/p_litter
execute positioned -57 201 -37 run function rlk:room/prop/p_dandelion
setblock -56 209 -37 minecraft:azalea_leaves[persistent=true] keep
setblock -56 209 -36 minecraft:azalea_leaves[persistent=true] keep
setblock -55 209 -37 minecraft:short_grass keep
setblock -54 207 -39 minecraft:azalea_leaves[persistent=true] keep
setblock -53 207 -39 minecraft:azalea_leaves[persistent=true] keep
setblock -53 207 -38 minecraft:azalea_leaves[persistent=true] keep
setblock -51 207 -39 minecraft:short_grass keep
