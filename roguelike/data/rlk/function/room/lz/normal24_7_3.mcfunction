# 구역 건설 (normal24_7, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -54 200 -32 -52 200 -31 minecraft:rooted_dirt
fill -58 200 -23 -56 200 -22 minecraft:moss_block
fill -54 200 -29 -51 200 -27 minecraft:rooted_dirt
fill -60 208 -24 -60 210 -22 minecraft:moss_block
fill -60 206 -27 -60 209 -26 minecraft:tuff
fill -60 201 -31 -60 202 -30 minecraft:tuff
fill -60 209 -26 -60 210 -22 minecraft:cobblestone
fill -60 208 -37 -60 210 -35 minecraft:moss_block
fill -60 203 -39 -60 206 -35 minecraft:moss_block
fill -41 202 -26 -41 203 -24 minecraft:andesite
fill -41 206 -29 -41 207 -27 minecraft:andesite
fill -41 210 -38 -41 210 -33 minecraft:oak_leaves[persistent=true]
fill -41 205 -24 -41 207 -22 minecraft:moss_block
fill -41 201 -38 -41 202 -36 minecraft:mossy_cobblestone
fill -46 208 -40 -42 208 -40 minecraft:tuff
fill -52 206 -40 -47 207 -40 minecraft:moss_block
fill -47 209 -40 -45 209 -40 minecraft:moss_block
fill -54 206 -40 -49 207 -40 minecraft:mossy_cobblestone
fill -58 206 -40 -55 209 -40 minecraft:mossy_cobblestone
fill -42 201 -40 -41 201 -40 minecraft:andesite
fill -58 207 -21 -58 209 -21 minecraft:moss_block
fill -49 210 -21 -44 210 -21 minecraft:moss_block
fill -57 204 -21 -55 205 -21 minecraft:tuff
fill -49 210 -21 -47 210 -21 minecraft:mossy_cobblestone
fill -51 207 -21 -49 207 -21 minecraft:granite
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -58 201 -39 -57 201 -39 minecraft:podzol
fill -51 201 -39 -50 201 -39 minecraft:podzol
fill -57 201 -38 -57 201 -37 minecraft:podzol
fill -51 201 -38 -51 201 -37 minecraft:podzol
fill -56 201 -37 -56 201 -37 minecraft:podzol
fill -52 201 -37 -52 201 -36 minecraft:podzol
fill -55 201 -36 -53 201 -36 minecraft:podzol
fill -54 201 -35 -54 201 -35 minecraft:podzol
fill -51 201 -25 -47 201 -24 minecraft:podzol
fill -46 201 -24 -42 201 -22 minecraft:podzol
fill -48 201 -23 -47 201 -22 minecraft:podzol
fill -56 201 -39 -52 201 -38 minecraft:dirt
fill -56 202 -39 -52 202 -38 minecraft:podzol
fill -55 201 -37 -53 201 -37 minecraft:dirt
fill -55 202 -37 -53 202 -37 minecraft:podzol
fill -51 201 -23 -49 206 -22 minecraft:andesite
fill -51 207 -23 -49 207 -22 minecraft:podzol
fill -57 201 -36 -56 207 -35 minecraft:stone
fill -57 208 -36 -56 208 -35 minecraft:podzol
execute positioned -49 201 -35 run function rlk:room/prop/p_lantern
execute positioned -56 203 -39 run function rlk:room/prop/p_litter
execute positioned -56 201 -22 run function rlk:room/prop/p_wildflower
execute positioned -53 203 -39 run function rlk:room/prop/p_grass
execute positioned -44 202 -23 run function rlk:room/prop/p_litter
execute positioned -42 201 -25 run function rlk:room/prop/p_wildflower
execute positioned -55 201 -27 run function rlk:room/prop/p_dandelion
execute positioned -53 203 -37 run function rlk:room/prop/p_grass
execute positioned -56 201 -34 run function rlk:room/prop/p_grass
execute positioned -44 201 -25 run function rlk:room/prop/p_litter
setblock -57 209 -36 minecraft:short_grass keep
setblock -57 209 -35 minecraft:azalea_leaves[persistent=true] keep
setblock -56 209 -35 minecraft:short_grass keep
setblock -51 208 -23 minecraft:short_grass keep
setblock -51 208 -22 minecraft:azalea_leaves[persistent=true] keep
setblock -49 208 -23 minecraft:azalea_leaves[persistent=true] keep
setblock -49 208 -22 minecraft:azalea_leaves[persistent=true] keep
