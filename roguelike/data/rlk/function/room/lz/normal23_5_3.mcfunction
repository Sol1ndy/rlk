# 구역 건설 (normal23_5, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -49 200 -35 -45 200 -33 minecraft:gravel
fill -53 200 -32 -50 200 -31 minecraft:coarse_dirt
fill -51 200 -36 -47 200 -33 minecraft:rooted_dirt
fill -60 201 -26 -60 202 -25 minecraft:andesite
fill -60 201 -26 -60 201 -24 minecraft:cobblestone
fill -60 205 -34 -60 205 -32 minecraft:andesite
fill -60 207 -24 -60 209 -21 minecraft:cobblestone
fill -41 204 -23 -41 205 -21 minecraft:mossy_cobblestone
fill -41 202 -30 -41 204 -25 minecraft:mossy_cobblestone
fill -41 209 -34 -41 210 -30 minecraft:andesite
fill -41 209 -35 -41 210 -30 minecraft:oak_leaves[persistent=true]
fill -41 209 -35 -41 209 -30 minecraft:mossy_cobblestone
fill -41 204 -29 -41 207 -25 minecraft:tuff
fill -52 206 -40 -49 207 -40 minecraft:moss_block
fill -45 206 -40 -41 208 -40 minecraft:moss_block
fill -44 207 -40 -43 207 -40 minecraft:moss_block
fill -59 204 -40 -58 205 -40 minecraft:granite
fill -52 210 -40 -50 210 -40 minecraft:cobblestone
fill -47 203 -40 -47 205 -40 minecraft:cobblestone
fill -55 209 -21 -50 210 -21 minecraft:oak_leaves[persistent=true]
fill -60 206 -21 -56 209 -21 minecraft:andesite
fill -45 208 -21 -42 208 -21 minecraft:mossy_cobblestone
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -57 201 -39 -57 201 -35 minecraft:podzol
fill -56 201 -34 -55 201 -34 minecraft:podzol
fill -55 201 -33 -55 201 -31 minecraft:podzol
fill -57 201 -31 -56 201 -31 minecraft:podzol
fill -59 201 -30 -57 201 -30 minecraft:podzol
fill -56 201 -28 -55 201 -27 minecraft:podzol
fill -55 201 -26 -55 201 -26 minecraft:podzol
fill -54 201 -25 -50 201 -25 minecraft:podzol
fill -51 201 -24 -50 201 -22 minecraft:podzol
fill -58 201 -23 -57 201 -22 minecraft:podzol
fill -58 201 -39 -58 201 -35 minecraft:dirt
fill -58 202 -39 -58 202 -35 minecraft:podzol
fill -57 201 -34 -57 201 -32 minecraft:dirt
fill -57 202 -34 -57 202 -32 minecraft:podzol
fill -56 201 -33 -56 201 -32 minecraft:dirt
fill -56 202 -33 -56 202 -32 minecraft:podzol
fill -59 201 -32 -58 201 -31 minecraft:dirt
fill -59 202 -32 -58 202 -31 minecraft:podzol
fill -56 201 -26 -56 201 -22 minecraft:dirt
fill -56 202 -26 -56 202 -22 minecraft:podzol
fill -55 201 -25 -55 201 -22 minecraft:dirt
fill -55 202 -25 -55 202 -22 minecraft:podzol
fill -54 201 -24 -52 201 -22 minecraft:dirt
fill -54 202 -24 -52 202 -22 minecraft:podzol
fill -59 201 -39 -59 202 -33 minecraft:dirt
fill -59 203 -39 -59 203 -33 minecraft:podzol
fill -58 201 -34 -58 202 -33 minecraft:dirt
fill -58 203 -34 -58 203 -33 minecraft:podzol
fill -57 201 -29 -57 207 -29 minecraft:andesite
fill -57 208 -29 -57 208 -29 minecraft:podzol
fill -57 201 -26 -57 207 -24 minecraft:andesite
fill -57 208 -26 -57 208 -24 minecraft:podzol
fill -59 201 -29 -58 207 -24 minecraft:stone
fill -59 208 -29 -58 208 -24 minecraft:podzol
fill -57 201 -28 -57 207 -27 minecraft:stone
fill -57 208 -28 -57 208 -27 minecraft:podzol
execute positioned -55 203 -22 run function rlk:room/prop/p_pillar_ruin
execute positioned -47 201 -25 run function rlk:room/prop/p_oak
execute positioned -55 201 -30 run function rlk:room/prop/p_pillar_ruin
execute positioned -43 201 -38 run function rlk:room/prop/p_grass
execute positioned -49 201 -25 run function rlk:room/prop/p_grass
execute positioned -46 201 -37 run function rlk:room/prop/p_wildflower
execute positioned -56 201 -35 run function rlk:room/prop/p_dandelion
execute positioned -59 204 -36 run function rlk:room/prop/p_grass
execute positioned -57 202 -35 run function rlk:room/prop/p_litter
setblock -59 209 -26 minecraft:short_grass keep
setblock -58 209 -29 minecraft:short_grass keep
setblock -58 209 -28 minecraft:azalea_leaves[persistent=true] keep
setblock -58 209 -27 minecraft:azalea_leaves[persistent=true] keep
setblock -58 209 -25 minecraft:azalea_leaves[persistent=true] keep
setblock -58 209 -24 minecraft:short_grass keep
setblock -57 209 -28 minecraft:azalea_leaves[persistent=true] keep
setblock -57 209 -26 minecraft:short_grass keep
setblock -57 209 -24 minecraft:short_grass keep
