# 구역 건설 (normal21_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -16 200 -8 -12 200 -6 minecraft:rooted_dirt
fill -3 200 -19 -2 200 -17 minecraft:rooted_dirt
fill -20 209 -18 -20 210 -18 minecraft:andesite
fill -20 210 -19 -20 210 -18 minecraft:andesite
fill -20 206 -18 -20 206 -16 minecraft:tuff
fill -20 207 -12 -20 210 -9 minecraft:mossy_cobblestone
fill -20 206 -11 -20 209 -10 minecraft:moss_block
fill -20 201 -12 -20 202 -12 minecraft:mossy_cobblestone
fill -1 209 -6 -1 210 -6 minecraft:oak_leaves[persistent=true]
fill -1 205 -7 -1 206 -4 minecraft:mossy_cobblestone
fill -1 207 -17 -1 209 -15 minecraft:moss_block
fill -12 209 -20 -9 210 -20 minecraft:moss_block
fill -19 209 -20 -19 210 -20 minecraft:oak_leaves[persistent=true]
fill -8 210 -20 -5 210 -20 minecraft:oak_leaves[persistent=true]
fill -13 206 -20 -10 207 -20 minecraft:cobblestone
fill -15 208 -20 -10 210 -20 minecraft:mossy_cobblestone
fill -5 209 -1 -5 210 -1 minecraft:oak_leaves[persistent=true]
fill -10 206 -1 -5 207 -1 minecraft:cobblestone
fill -3 204 -1 -1 204 -1 minecraft:moss_block
fill -14 209 -1 -14 210 -1 minecraft:oak_leaves[persistent=true]
fill -14 209 -1 -9 210 -1 minecraft:oak_leaves[persistent=true]
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -19 201 -15 -17 201 -15 minecraft:podzol
fill -17 201 -14 -17 201 -6 minecraft:podzol
fill -4 201 -7 -2 201 -7 minecraft:podzol
fill -19 201 -6 -18 201 -5 minecraft:podzol
fill -5 201 -6 -5 201 -6 minecraft:podzol
fill -6 201 -5 -6 201 -5 minecraft:podzol
fill -7 201 -4 -7 201 -2 minecraft:podzol
fill -19 201 -14 -18 201 -7 minecraft:dirt
fill -19 202 -14 -18 202 -7 minecraft:podzol
fill -4 201 -6 -2 201 -6 minecraft:dirt
fill -4 202 -6 -2 202 -6 minecraft:podzol
fill -5 201 -5 -5 201 -5 minecraft:dirt
fill -5 202 -5 -5 202 -5 minecraft:podzol
fill -6 201 -4 -6 201 -2 minecraft:dirt
fill -6 202 -4 -6 202 -2 minecraft:podzol
fill -4 201 -5 -2 202 -2 minecraft:dirt
fill -4 203 -5 -2 203 -2 minecraft:podzol
fill -5 201 -4 -5 202 -2 minecraft:dirt
fill -5 203 -4 -5 203 -2 minecraft:podzol
fill -10 201 -17 -9 205 -16 minecraft:stone
fill -10 206 -17 -9 206 -16 minecraft:podzol
fill -9 201 -19 -8 206 -19 minecraft:andesite
fill -9 207 -19 -8 207 -19 minecraft:podzol
fill -11 201 -19 -10 206 -18 minecraft:stone
fill -11 207 -19 -10 207 -18 minecraft:podzol
fill -9 201 -18 -8 206 -18 minecraft:stone
fill -9 207 -18 -8 207 -18 minecraft:podzol
execute positioned -4 201 -10 run function rlk:room/prop/p_pillar_ruin
execute positioned -15 201 -5 run function rlk:room/prop/p_fence_z
execute positioned -13 201 -8 run function rlk:room/prop/p_dandelion
execute positioned -6 201 -17 run function rlk:room/prop/p_grass
execute positioned -11 201 -13 run function rlk:room/prop/p_grass
execute positioned -8 201 -15 run function rlk:room/prop/p_grass
execute positioned -5 201 -16 run function rlk:room/prop/p_wildflower
execute positioned -11 201 -4 run function rlk:room/prop/p_grass
setblock -11 208 -19 minecraft:short_grass keep
setblock -10 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock -10 208 -18 minecraft:short_grass keep
setblock -10 207 -16 minecraft:short_grass keep
setblock -9 208 -19 minecraft:azalea_leaves[persistent=true] keep
setblock -9 208 -18 minecraft:short_grass keep
setblock -9 207 -16 minecraft:azalea_leaves[persistent=true] keep
setblock -8 208 -18 minecraft:azalea_leaves[persistent=true] keep
