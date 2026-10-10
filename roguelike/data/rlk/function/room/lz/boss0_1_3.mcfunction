# 구역 건설 (boss0_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:podzol
fill -20 201 0 -1 210 19 minecraft:stone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -12 200 12 -10 200 14 minecraft:rooted_dirt
fill -20 206 4 -20 208 4 minecraft:andesite
fill -20 210 7 -20 210 11 minecraft:oak_leaves[persistent=true]
fill -20 206 9 -20 209 13 minecraft:moss_block
fill -20 209 6 -20 210 11 minecraft:oak_leaves[persistent=true]
fill -20 207 12 -20 210 14 minecraft:moss_block
fill -1 209 5 -1 210 7 minecraft:mossy_cobblestone
fill -1 206 3 -1 207 8 minecraft:mossy_cobblestone
fill -1 207 6 -1 210 8 minecraft:mossy_cobblestone
fill -1 205 2 -1 206 7 minecraft:cobblestone
fill -1 209 19 -1 210 19 minecraft:oak_leaves[persistent=true]
fill -1 201 15 -1 202 16 minecraft:moss_block
fill -16 209 0 -14 210 0 minecraft:cobblestone
fill -3 205 0 -3 205 0 minecraft:andesite
fill -8 210 0 -4 210 0 minecraft:cobblestone
fill -12 203 0 -12 204 0 minecraft:moss_block
fill -20 209 0 -18 210 0 minecraft:oak_leaves[persistent=true]
fill -19 209 19 -17 210 19 minecraft:moss_block
fill -20 205 19 -17 208 19 minecraft:tuff
fill -2 210 19 -2 210 19 minecraft:cobblestone
fill -8 201 19 -6 203 19 minecraft:tuff
fill -11 206 19 -7 207 19 minecraft:andesite
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -15 201 11 -15 201 14 minecraft:podzol
fill -17 201 12 -16 201 13 minecraft:podzol
fill -17 201 14 -17 201 15 minecraft:podzol
fill -14 201 15 -7 201 15 minecraft:podzol
fill -8 201 16 -7 201 18 minecraft:podzol
fill -16 201 14 -16 201 18 minecraft:dirt
fill -16 202 14 -16 202 18 minecraft:podzol
fill -15 201 15 -15 201 18 minecraft:dirt
fill -15 202 15 -15 202 18 minecraft:podzol
fill -17 201 16 -17 201 18 minecraft:dirt
fill -17 202 16 -17 202 18 minecraft:podzol
fill -14 201 16 -9 201 18 minecraft:dirt
fill -14 202 16 -9 202 18 minecraft:podzol
fill -17 201 7 -16 205 8 minecraft:andesite
fill -17 206 7 -16 206 8 minecraft:podzol
fill -18 201 14 -18 206 17 minecraft:andesite
fill -18 207 14 -18 207 17 minecraft:podzol
fill -19 201 13 -18 206 13 minecraft:stone
fill -19 207 13 -18 207 13 minecraft:podzol
fill -19 201 14 -19 206 18 minecraft:stone
fill -19 207 14 -19 207 18 minecraft:podzol
fill -18 201 18 -18 206 18 minecraft:stone
fill -18 207 18 -18 207 18 minecraft:podzol
execute positioned -15 203 16 run function rlk:room/prop/p_lantern
execute positioned -4 201 14 run function rlk:room/prop/p_lantern
execute positioned -17 201 3 run function rlk:room/prop/p_dandelion
execute positioned -17 201 1 run function rlk:room/prop/p_litter
execute positioned -13 201 9 run function rlk:room/prop/p_dandelion
execute positioned -10 201 10 run function rlk:room/prop/p_wildflower
execute positioned -17 201 4 run function rlk:room/prop/p_wildflower
execute positioned -18 201 9 run function rlk:room/prop/p_grass
setblock -19 208 15 minecraft:short_grass keep
setblock -19 208 17 minecraft:azalea_leaves[persistent=true] keep
setblock -19 208 18 minecraft:short_grass keep
setblock -18 208 14 minecraft:azalea_leaves[persistent=true] keep
setblock -18 208 16 minecraft:azalea_leaves[persistent=true] keep
setblock -18 208 18 minecraft:azalea_leaves[persistent=true] keep
setblock -17 207 8 minecraft:azalea_leaves[persistent=true] keep
