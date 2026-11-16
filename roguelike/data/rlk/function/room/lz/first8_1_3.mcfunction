# 구역 건설 (first8_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -13 200 -10 -9 200 -9 minecraft:moss_block
fill -9 200 -9 -5 200 -8 minecraft:coarse_dirt
fill -7 200 -11 -6 200 -9 minecraft:rooted_dirt
fill -20 204 -16 -20 207 -15 minecraft:moss_block
fill -20 209 -1 -20 210 -1 minecraft:oak_leaves[persistent=true]
fill -20 210 -5 -20 210 -3 minecraft:oak_leaves[persistent=true]
fill -1 209 -11 -1 210 -10 minecraft:mossy_cobblestone
fill -1 208 -14 -1 210 -14 minecraft:moss_block
fill -1 204 -3 -1 204 -3 minecraft:moss_block
fill -1 207 -20 -1 210 -16 minecraft:cobblestone
fill -1 210 -10 -1 210 -9 minecraft:moss_block
fill -10 208 -20 -7 210 -20 minecraft:mossy_cobblestone
fill -5 202 -20 -1 205 -20 minecraft:tuff
fill -6 201 -20 -5 201 -20 minecraft:mossy_cobblestone
fill -9 203 -1 -6 204 -1 minecraft:moss_block
fill -9 210 -1 -7 210 -1 minecraft:oak_leaves[persistent=true]
fill -15 210 -1 -10 210 -1 minecraft:moss_block
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -18 201 -19 -18 201 -16 minecraft:podzol
fill -17 201 -15 -17 201 -14 minecraft:podzol
fill -16 201 -13 -15 201 -13 minecraft:podzol
fill -15 201 -12 -15 201 -10 minecraft:podzol
fill -16 201 -10 -16 201 -9 minecraft:podzol
fill -19 201 -9 -17 201 -9 minecraft:podzol
fill -19 201 -19 -19 201 -16 minecraft:dirt
fill -19 202 -19 -19 202 -16 minecraft:podzol
fill -18 201 -15 -18 201 -14 minecraft:dirt
fill -18 202 -15 -18 202 -14 minecraft:podzol
fill -17 201 -13 -17 201 -13 minecraft:dirt
fill -17 202 -13 -17 202 -13 minecraft:podzol
fill -16 201 -12 -16 201 -11 minecraft:dirt
fill -16 202 -12 -16 202 -11 minecraft:podzol
fill -19 201 -11 -17 201 -10 minecraft:dirt
fill -19 202 -11 -17 202 -10 minecraft:podzol
fill -19 201 -15 -19 202 -12 minecraft:dirt
fill -19 203 -15 -19 203 -12 minecraft:podzol
fill -18 201 -13 -18 202 -12 minecraft:dirt
fill -18 203 -13 -18 203 -12 minecraft:podzol
fill -17 201 -12 -17 202 -12 minecraft:dirt
fill -17 203 -12 -17 203 -12 minecraft:podzol
fill -17 201 -7 -16 206 -6 minecraft:andesite
fill -17 207 -7 -16 207 -6 minecraft:podzol
fill -8 201 -3 -5 206 -2 minecraft:stone
fill -8 207 -3 -5 207 -2 minecraft:podzol
execute positioned -5 201 -7 run function rlk:room/prop/p_oak
execute positioned -19 204 -12 run function rlk:room/prop/p_pillar_ruin
execute positioned -7 201 -4 run function rlk:room/prop/p_wildflower
execute positioned -17 201 -19 run function rlk:room/prop/p_dandelion
execute positioned -7 201 -5 run function rlk:room/prop/p_grass
execute positioned -5 201 -9 run function rlk:room/prop/p_grass
execute positioned -19 201 -4 run function rlk:room/prop/p_grass
execute positioned -10 201 -8 run function rlk:room/prop/p_wildflower
execute positioned -8 201 -16 run function rlk:room/prop/p_wildflower
execute positioned -15 202 -11 run function rlk:room/prop/p_wildflower
setblock -17 208 -7 minecraft:azalea_leaves[persistent=true] keep
setblock -17 208 -6 minecraft:short_grass keep
setblock -8 208 -3 minecraft:azalea_leaves[persistent=true] keep
setblock -8 208 -2 minecraft:azalea_leaves[persistent=true] keep
setblock -7 208 -3 minecraft:azalea_leaves[persistent=true] keep
setblock -7 208 -2 minecraft:azalea_leaves[persistent=true] keep
setblock -6 208 -3 minecraft:azalea_leaves[persistent=true] keep
setblock -6 208 -2 minecraft:azalea_leaves[persistent=true] keep
setblock -5 208 -3 minecraft:azalea_leaves[persistent=true] keep
