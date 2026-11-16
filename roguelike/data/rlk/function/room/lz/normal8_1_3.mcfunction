# 구역 건설 (normal8_1, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -11 200 -4 -9 200 -2 minecraft:rooted_dirt
fill -20 202 -8 -20 203 -7 minecraft:andesite
fill -20 210 -11 -20 210 -9 minecraft:tuff
fill -20 203 -16 -20 204 -16 minecraft:moss_block
fill -20 202 -14 -20 205 -13 minecraft:mossy_cobblestone
fill -20 201 -13 -20 202 -10 minecraft:andesite
fill -20 202 -9 -20 204 -8 minecraft:mossy_cobblestone
fill -1 201 -16 -1 202 -11 minecraft:cobblestone
fill -1 210 -12 -1 210 -11 minecraft:oak_leaves[persistent=true]
fill -1 203 -1 -1 205 -1 minecraft:moss_block
fill -1 204 -3 -1 204 -2 minecraft:moss_block
fill -12 209 -20 -11 210 -20 minecraft:oak_leaves[persistent=true]
fill -2 209 -20 -1 210 -20 minecraft:oak_leaves[persistent=true]
fill -9 209 -20 -9 210 -20 minecraft:oak_leaves[persistent=true]
fill -2 208 -20 -2 210 -20 minecraft:moss_block
fill -6 209 -20 -1 210 -20 minecraft:moss_block
fill -17 203 -1 -16 203 -1 minecraft:andesite
fill -9 210 -1 -7 210 -1 minecraft:tuff
fill -20 209 -1 -17 210 -1 minecraft:moss_block
fill -8 210 -1 -8 210 -1 minecraft:oak_leaves[persistent=true]
fill -5 207 -1 -4 209 -1 minecraft:moss_block
fill -12 207 -1 -8 208 -1 minecraft:mossy_cobblestone
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -19 201 -19 -18 201 -18 minecraft:podzol
fill -17 201 -18 -17 201 -17 minecraft:podzol
fill -16 201 -17 -16 201 -13 minecraft:podzol
fill -17 201 -13 -17 201 -12 minecraft:podzol
fill -19 201 -12 -18 201 -11 minecraft:podzol
fill -19 201 -17 -18 201 -13 minecraft:dirt
fill -19 202 -17 -18 202 -13 minecraft:podzol
fill -17 201 -16 -17 201 -14 minecraft:dirt
fill -17 202 -16 -17 202 -14 minecraft:podzol
fill -17 201 -7 -16 207 -6 minecraft:andesite
fill -17 208 -7 -16 208 -6 minecraft:podzol
fill -15 201 -3 -13 207 -2 minecraft:stone
fill -15 208 -3 -13 208 -2 minecraft:podzol
execute positioned -19 202 -19 run function rlk:room/prop/p_boulder
execute positioned -7 201 -4 run function rlk:room/prop/p_oak
execute positioned -11 201 -17 run function rlk:room/prop/p_dandelion
execute positioned -12 201 -9 run function rlk:room/prop/p_dandelion
execute positioned -3 201 -6 run function rlk:room/prop/p_wildflower
execute positioned -15 201 -19 run function rlk:room/prop/p_dandelion
execute positioned -16 201 -5 run function rlk:room/prop/p_wildflower
execute positioned -5 201 -16 run function rlk:room/prop/p_dandelion
setblock -17 209 -7 minecraft:azalea_leaves[persistent=true] keep
setblock -17 209 -6 minecraft:azalea_leaves[persistent=true] keep
setblock -16 209 -7 minecraft:azalea_leaves[persistent=true] keep
setblock -15 209 -3 minecraft:short_grass keep
setblock -15 209 -2 minecraft:azalea_leaves[persistent=true] keep
setblock -14 209 -2 minecraft:short_grass keep
setblock -13 209 -3 minecraft:azalea_leaves[persistent=true] keep
