# 구역 건설 (first3_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:stone
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -25 200 -7 -22 200 -4 minecraft:gravel
fill -31 200 -11 -30 200 -8 minecraft:rooted_dirt
fill -40 202 -14 -40 205 -13 minecraft:moss_block
fill -40 201 -17 -40 201 -12 minecraft:mossy_cobblestone
fill -40 204 -6 -40 204 -5 minecraft:mossy_cobblestone
fill -21 210 -9 -21 210 -8 minecraft:cobblestone
fill -21 205 -12 -21 207 -8 minecraft:tuff
fill -21 210 -14 -21 210 -9 minecraft:oak_leaves[persistent=true]
fill -21 204 -8 -21 204 -6 minecraft:tuff
fill -21 210 -9 -21 210 -5 minecraft:oak_leaves[persistent=true]
fill -31 209 -20 -27 210 -20 minecraft:oak_leaves[persistent=true]
fill -26 206 -20 -22 208 -20 minecraft:mossy_cobblestone
fill -27 207 -20 -25 208 -20 minecraft:tuff
fill -31 206 -20 -30 206 -20 minecraft:tuff
fill -24 201 -20 -23 201 -20 minecraft:andesite
fill -31 206 -1 -31 208 -1 minecraft:andesite
fill -29 208 -1 -27 210 -1 minecraft:tuff
fill -38 201 -1 -35 202 -1 minecraft:andesite
fill -29 204 -1 -24 205 -1 minecraft:andesite
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -28 201 -18 -27 201 -16 minecraft:podzol
fill -26 201 -17 -22 201 -17 minecraft:podzol
fill -27 201 -15 -27 201 -15 minecraft:podzol
fill -26 201 -18 -22 201 -18 minecraft:dirt
fill -26 202 -18 -22 202 -18 minecraft:podzol
fill -30 201 -17 -29 206 -16 minecraft:stone
fill -30 207 -17 -29 207 -16 minecraft:podzol
fill -27 201 -19 -25 207 -19 minecraft:andesite
fill -27 208 -19 -25 208 -19 minecraft:podzol
fill -24 201 -19 -22 207 -19 minecraft:stone
fill -24 208 -19 -22 208 -19 minecraft:podzol
execute positioned -39 201 -5 run function rlk:room/prop/p_fence_z
execute positioned -33 201 -5 run function rlk:room/prop/p_wildflower
execute positioned -26 201 -12 run function rlk:room/prop/p_wildflower
execute positioned -23 201 -16 run function rlk:room/prop/p_wildflower
execute positioned -39 201 -2 run function rlk:room/prop/p_wildflower
execute positioned -32 201 -3 run function rlk:room/prop/p_dandelion
execute positioned -24 202 -17 run function rlk:room/prop/p_dandelion
execute positioned -27 201 -6 run function rlk:room/prop/p_grass
execute positioned -33 201 -2 run function rlk:room/prop/p_grass
setblock -29 208 -16 minecraft:short_grass keep
setblock -26 209 -19 minecraft:azalea_leaves[persistent=true] keep
setblock -25 209 -19 minecraft:short_grass keep
setblock -22 209 -19 minecraft:short_grass keep
