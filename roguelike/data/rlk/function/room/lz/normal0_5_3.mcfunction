# 구역 건설 (normal0_5, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -60 19 200 -41 minecraft:podzol
fill 0 201 -60 19 210 -41 minecraft:stone
fill 1 201 -59 18 210 -42 minecraft:air
fill 1 209 -59 18 209 -42 minecraft:light[level=15]
fill 7 200 -51 8 200 -50 minecraft:rooted_dirt
fill 15 200 -54 16 200 -53 minecraft:coarse_dirt
fill 7 200 -57 11 200 -55 minecraft:gravel
fill 0 209 -57 0 210 -56 minecraft:oak_leaves[persistent=true]
fill 0 201 -54 0 203 -53 minecraft:andesite
fill 0 201 -60 0 203 -55 minecraft:cobblestone
fill 0 207 -44 0 210 -41 minecraft:andesite
fill 0 210 -48 0 210 -45 minecraft:oak_leaves[persistent=true]
fill 19 210 -55 19 210 -50 minecraft:cobblestone
fill 19 207 -46 19 208 -41 minecraft:andesite
fill 19 203 -58 19 205 -57 minecraft:moss_block
fill 19 208 -59 19 210 -58 minecraft:cobblestone
fill 19 201 -52 19 201 -50 minecraft:andesite
fill 19 204 -50 19 207 -47 minecraft:andesite
fill 15 208 -60 17 210 -60 minecraft:cobblestone
fill 15 209 -60 17 210 -60 minecraft:oak_leaves[persistent=true]
fill 18 201 -60 19 203 -60 minecraft:tuff
fill 9 210 -60 11 210 -60 minecraft:oak_leaves[persistent=true]
fill 13 209 -60 17 210 -60 minecraft:oak_leaves[persistent=true]
fill 9 209 -41 11 210 -41 minecraft:cobblestone
fill 10 208 -41 14 208 -41 minecraft:andesite
fill 3 209 -41 5 210 -41 minecraft:oak_leaves[persistent=true]
fill 0 207 -41 0 208 -41 minecraft:mossy_cobblestone
fill 0 210 -60 19 210 -41 minecraft:polished_deepslate
fill 1 210 -59 18 210 -42 minecraft:air
fill 8 201 -45 14 201 -45 minecraft:podzol
fill 7 201 -44 7 201 -43 minecraft:podzol
fill 14 201 -44 15 201 -42 minecraft:podzol
fill 5 201 -42 6 201 -42 minecraft:podzol
fill 8 201 -44 13 201 -42 minecraft:dirt
fill 8 202 -44 13 202 -42 minecraft:podzol
fill 7 201 -42 7 201 -42 minecraft:dirt
fill 7 202 -42 7 202 -42 minecraft:podzol
fill 12 201 -59 13 206 -59 minecraft:andesite
fill 12 207 -59 13 207 -59 minecraft:podzol
fill 10 201 -59 11 206 -59 minecraft:stone
fill 10 207 -59 11 207 -59 minecraft:podzol
execute positioned 12 201 -55 run function rlk:room/prop/p_pillar_ruin
execute positioned 6 201 -55 run function rlk:room/prop/p_ruin_x
execute positioned 15 201 -52 run function rlk:room/prop/p_boulder
execute positioned 9 202 -45 run function rlk:room/prop/p_fence_x
execute positioned 7 203 -42 run function rlk:room/prop/p_ruin_x
execute positioned 5 201 -57 run function rlk:room/prop/p_wildflower
execute positioned 14 201 -54 run function rlk:room/prop/p_grass
execute positioned 10 201 -57 run function rlk:room/prop/p_wildflower
execute positioned 12 201 -51 run function rlk:room/prop/p_grass
execute positioned 3 201 -55 run function rlk:room/prop/p_wildflower
execute positioned 8 201 -58 run function rlk:room/prop/p_dandelion
setblock 10 208 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 11 208 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 12 208 -59 minecraft:azalea_leaves[persistent=true] keep
setblock 13 208 -59 minecraft:short_grass keep
