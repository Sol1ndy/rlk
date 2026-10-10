# 구역 건설 (boss6_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 1 200 5 3 200 6 minecraft:moss_block
fill 3 200 5 7 200 6 minecraft:coarse_dirt
fill 4 200 8 8 200 10 minecraft:gravel
fill 0 210 1 0 210 3 minecraft:granite
fill 0 209 14 0 209 18 minecraft:cobblestone
fill 0 202 16 0 202 16 minecraft:cobblestone
fill 0 203 10 0 206 15 minecraft:moss_block
fill 0 210 12 0 210 16 minecraft:oak_leaves[persistent=true]
fill 0 205 11 0 205 13 minecraft:moss_block
fill 19 209 10 19 210 14 minecraft:oak_leaves[persistent=true]
fill 19 203 7 19 203 10 minecraft:andesite
fill 19 206 0 19 207 0 minecraft:moss_block
fill 19 209 6 19 210 6 minecraft:moss_block
fill 19 207 17 19 209 17 minecraft:moss_block
fill 4 209 0 9 209 0 minecraft:tuff
fill 8 205 0 13 205 0 minecraft:mossy_cobblestone
fill 4 201 0 8 202 0 minecraft:moss_block
fill 10 209 0 15 210 0 minecraft:oak_leaves[persistent=true]
fill 3 210 19 7 210 19 minecraft:oak_leaves[persistent=true]
fill 12 203 19 16 203 19 minecraft:moss_block
fill 10 209 19 15 210 19 minecraft:mossy_cobblestone
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 16 201 1 18 201 10 minecraft:podzol
fill 15 201 6 15 201 12 minecraft:podzol
fill 16 201 11 16 201 13 minecraft:podzol
fill 18 201 11 18 206 13 minecraft:andesite
fill 18 207 11 18 207 13 minecraft:podzol
fill 17 201 12 17 206 13 minecraft:andesite
fill 17 207 12 17 207 13 minecraft:podzol
fill 17 201 11 17 206 11 minecraft:stone
fill 17 207 11 17 207 11 minecraft:podzol
fill 3 201 13 4 207 14 minecraft:stone
fill 3 208 13 4 208 14 minecraft:podzol
execute positioned 5 201 8 run function rlk:room/prop/p_oak
execute positioned 1 201 1 run function rlk:room/prop/p_pillar_ruin
execute positioned 13 201 16 run function rlk:room/prop/p_grass
execute positioned 9 201 9 run function rlk:room/prop/p_wildflower
execute positioned 15 201 17 run function rlk:room/prop/p_litter
execute positioned 15 202 8 run function rlk:room/prop/p_grass
execute positioned 1 201 6 run function rlk:room/prop/p_grass
execute positioned 17 202 3 run function rlk:room/prop/p_grass
execute positioned 4 201 12 run function rlk:room/prop/p_litter
execute positioned 8 201 13 run function rlk:room/prop/p_wildflower
execute positioned 14 201 8 run function rlk:room/prop/p_grass
setblock 3 209 13 minecraft:short_grass keep
setblock 4 209 13 minecraft:azalea_leaves[persistent=true] keep
setblock 17 208 12 minecraft:azalea_leaves[persistent=true] keep
setblock 17 208 13 minecraft:azalea_leaves[persistent=true] keep
setblock 18 208 11 minecraft:azalea_leaves[persistent=true] keep
setblock 18 208 13 minecraft:azalea_leaves[persistent=true] keep
