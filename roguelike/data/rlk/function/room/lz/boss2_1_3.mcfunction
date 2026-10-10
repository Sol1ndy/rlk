# 구역 건설 (boss2_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 6 200 12 9 200 13 minecraft:rooted_dirt
fill 8 200 11 11 200 14 minecraft:gravel
fill 0 206 4 0 209 4 minecraft:tuff
fill 0 206 4 0 208 8 minecraft:andesite
fill 0 206 4 0 207 4 minecraft:granite
fill 19 209 13 19 210 13 minecraft:oak_leaves[persistent=true]
fill 19 209 1 19 210 5 minecraft:oak_leaves[persistent=true]
fill 19 201 3 19 201 4 minecraft:andesite
fill 19 209 4 19 210 6 minecraft:oak_leaves[persistent=true]
fill 19 201 0 19 203 5 minecraft:cobblestone
fill 19 210 8 19 210 12 minecraft:moss_block
fill 10 210 0 10 210 0 minecraft:andesite
fill 11 210 0 12 210 0 minecraft:oak_leaves[persistent=true]
fill 3 204 0 4 204 0 minecraft:moss_block
fill 16 201 19 17 201 19 minecraft:andesite
fill 3 209 19 4 210 19 minecraft:oak_leaves[persistent=true]
fill 13 202 19 18 202 19 minecraft:andesite
fill 6 209 19 10 210 19 minecraft:oak_leaves[persistent=true]
fill 1 206 19 1 206 19 minecraft:andesite
fill 7 205 19 9 208 19 minecraft:cobblestone
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 1 201 5 2 201 15 minecraft:podzol
fill 3 201 6 4 201 14 minecraft:podzol
fill 5 201 7 5 201 13 minecraft:podzol
fill 3 201 4 4 207 5 minecraft:stone
fill 3 208 4 4 208 5 minecraft:podzol
execute positioned 4 202 14 run function rlk:room/prop/p_pillar_ruin
execute positioned 3 202 10 run function rlk:room/prop/p_ruin_z
execute positioned 11 201 11 run function rlk:room/prop/p_grass
execute positioned 17 201 17 run function rlk:room/prop/p_grass
execute positioned 13 201 12 run function rlk:room/prop/p_litter
execute positioned 8 201 1 run function rlk:room/prop/p_wildflower
execute positioned 17 201 7 run function rlk:room/prop/p_grass
execute positioned 18 201 7 run function rlk:room/prop/p_grass
execute positioned 13 201 15 run function rlk:room/prop/p_wildflower
execute positioned 3 201 17 run function rlk:room/prop/p_wildflower
execute positioned 7 201 14 run function rlk:room/prop/p_wildflower
setblock 3 209 4 minecraft:short_grass keep
setblock 3 209 5 minecraft:short_grass keep
setblock 4 209 5 minecraft:short_grass keep
