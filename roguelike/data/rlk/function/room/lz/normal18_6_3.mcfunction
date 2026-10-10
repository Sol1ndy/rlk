# 구역 건설 (normal18_6, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:podzol
fill 0 201 0 19 210 19 minecraft:stone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 4 200 8 7 200 11 minecraft:gravel
fill 12 200 13 13 200 14 minecraft:gravel
fill 9 200 1 11 200 4 minecraft:gravel
fill 0 204 10 0 207 11 minecraft:tuff
fill 0 207 12 0 209 12 minecraft:mossy_cobblestone
fill 0 206 7 0 206 12 minecraft:andesite
fill 19 209 0 19 210 3 minecraft:oak_leaves[persistent=true]
fill 19 201 4 19 202 5 minecraft:andesite
fill 19 204 7 19 205 10 minecraft:tuff
fill 19 208 1 19 210 5 minecraft:tuff
fill 19 203 8 19 204 11 minecraft:tuff
fill 19 210 13 19 210 18 minecraft:tuff
fill 8 205 0 8 208 0 minecraft:granite
fill 10 204 0 14 207 0 minecraft:mossy_cobblestone
fill 1 203 0 3 203 0 minecraft:mossy_cobblestone
fill 6 210 19 9 210 19 minecraft:moss_block
fill 10 207 19 12 210 19 minecraft:andesite
fill 2 207 19 5 208 19 minecraft:andesite
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 15 201 5 18 201 6 minecraft:podzol
fill 18 201 7 18 201 15 minecraft:podzol
fill 15 201 14 17 201 15 minecraft:podzol
fill 7 201 3 8 205 4 minecraft:stone
fill 7 206 3 8 206 4 minecraft:podzol
fill 12 201 17 12 206 18 minecraft:andesite
fill 12 207 17 12 207 18 minecraft:podzol
fill 10 201 17 11 206 18 minecraft:stone
fill 10 207 17 11 207 18 minecraft:podzol
execute positioned 11 201 4 run function rlk:room/prop/p_lantern
execute positioned 13 201 2 run function rlk:room/prop/p_wildflower
execute positioned 18 201 4 run function rlk:room/prop/p_litter
execute positioned 17 201 11 run function rlk:room/prop/p_dandelion
execute positioned 7 201 5 run function rlk:room/prop/p_grass
execute positioned 10 201 15 run function rlk:room/prop/p_dandelion
execute positioned 7 201 13 run function rlk:room/prop/p_dandelion
execute positioned 9 201 9 run function rlk:room/prop/p_wildflower
execute positioned 15 201 9 run function rlk:room/prop/p_wildflower
execute positioned 9 201 11 run function rlk:room/prop/p_dandelion
setblock 7 207 4 minecraft:short_grass keep
setblock 8 207 3 minecraft:azalea_leaves[persistent=true] keep
setblock 10 208 18 minecraft:short_grass keep
setblock 12 208 17 minecraft:short_grass keep
