# 구역 건설 (levelup0_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:podzol
fill 20 201 0 39 210 19 minecraft:stone
fill 21 201 1 38 210 18 minecraft:air
fill 21 209 1 38 209 18 minecraft:light[level=15]
fill 25 200 6 27 200 7 minecraft:rooted_dirt
fill 28 200 8 30 200 11 minecraft:rooted_dirt
fill 20 204 9 20 207 9 minecraft:moss_block
fill 20 201 15 20 201 16 minecraft:granite
fill 20 209 11 20 210 14 minecraft:moss_block
fill 20 201 14 20 203 18 minecraft:moss_block
fill 20 209 4 20 210 7 minecraft:oak_leaves[persistent=true]
fill 20 201 11 20 204 15 minecraft:mossy_cobblestone
fill 39 208 7 39 210 10 minecraft:mossy_cobblestone
fill 39 202 10 39 203 15 minecraft:moss_block
fill 39 209 1 39 210 6 minecraft:mossy_cobblestone
fill 39 201 10 39 203 14 minecraft:moss_block
fill 39 209 8 39 210 12 minecraft:oak_leaves[persistent=true]
fill 26 209 0 31 210 0 minecraft:oak_leaves[persistent=true]
fill 25 206 0 30 208 0 minecraft:tuff
fill 30 209 0 35 210 0 minecraft:oak_leaves[persistent=true]
fill 27 203 0 30 203 0 minecraft:andesite
fill 21 206 0 26 206 0 minecraft:andesite
fill 31 208 0 32 209 0 minecraft:andesite
fill 26 209 19 26 210 19 minecraft:oak_leaves[persistent=true]
fill 35 210 19 39 210 19 minecraft:oak_leaves[persistent=true]
fill 31 209 19 36 210 19 minecraft:cobblestone
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 38 210 18 minecraft:air
fill 21 201 5 22 201 5 minecraft:podzol
fill 22 201 6 22 201 6 minecraft:podzol
fill 23 201 7 24 201 7 minecraft:podzol
fill 25 201 8 25 201 14 minecraft:podzol
fill 35 201 8 38 201 18 minecraft:podzol
fill 24 201 14 24 201 14 minecraft:podzol
fill 23 201 15 23 201 15 minecraft:podzol
fill 31 201 15 34 201 15 minecraft:podzol
fill 32 201 16 34 201 16 minecraft:podzol
fill 33 201 17 34 201 17 minecraft:podzol
fill 34 201 18 34 201 18 minecraft:podzol
fill 21 201 6 21 201 7 minecraft:dirt
fill 21 202 6 21 202 7 minecraft:podzol
fill 22 201 7 22 201 7 minecraft:dirt
fill 22 202 7 22 202 7 minecraft:podzol
fill 23 201 8 24 201 8 minecraft:dirt
fill 23 202 8 24 202 8 minecraft:podzol
fill 24 201 9 24 201 13 minecraft:dirt
fill 24 202 9 24 202 13 minecraft:podzol
fill 23 201 13 23 201 14 minecraft:dirt
fill 23 202 13 23 202 14 minecraft:podzol
fill 21 201 8 22 202 12 minecraft:dirt
fill 21 203 8 22 203 12 minecraft:podzol
fill 23 201 9 23 202 12 minecraft:dirt
fill 23 203 9 23 203 12 minecraft:podzol
fill 21 201 13 22 207 16 minecraft:stone
fill 21 208 13 22 208 16 minecraft:podzol
execute positioned 21 202 5 run function rlk:room/prop/p_boulder_s
execute positioned 37 201 7 run function rlk:room/prop/p_crates
execute positioned 25 201 16 run function rlk:room/prop/p_pillar_ruin
execute positioned 28 201 10 run function rlk:room/prop/p_grass
execute positioned 21 204 10 run function rlk:room/prop/p_dandelion
execute positioned 32 201 18 run function rlk:room/prop/p_wildflower
execute positioned 31 201 1 run function rlk:room/prop/p_wildflower
execute positioned 31 201 2 run function rlk:room/prop/p_wildflower
execute positioned 36 202 11 run function rlk:room/prop/p_grass
execute positioned 29 201 5 run function rlk:room/prop/p_dandelion
setblock 21 209 13 minecraft:short_grass keep
setblock 21 209 14 minecraft:azalea_leaves[persistent=true] keep
setblock 21 209 15 minecraft:short_grass keep
setblock 21 209 16 minecraft:short_grass keep
setblock 22 209 13 minecraft:short_grass keep
setblock 22 209 14 minecraft:azalea_leaves[persistent=true] keep
setblock 22 209 16 minecraft:azalea_leaves[persistent=true] keep
