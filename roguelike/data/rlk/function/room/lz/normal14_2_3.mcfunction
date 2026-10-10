# 구역 건설 (normal14_2, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:stone
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -14 200 -12 -10 200 -10 minecraft:gravel
fill -20 209 -3 -20 210 -3 minecraft:cobblestone
fill -20 209 -20 -20 210 -17 minecraft:oak_leaves[persistent=true]
fill -20 209 -14 -20 210 -10 minecraft:oak_leaves[persistent=true]
fill -20 201 -16 -20 202 -13 minecraft:moss_block
fill -1 202 -13 -1 205 -8 minecraft:andesite
fill -1 201 -5 -1 201 -3 minecraft:mossy_cobblestone
fill -1 207 -17 -1 208 -14 minecraft:mossy_cobblestone
fill -1 207 -11 -1 209 -11 minecraft:cobblestone
fill -1 207 -4 -1 210 -2 minecraft:mossy_cobblestone
fill -5 209 -20 -3 210 -20 minecraft:oak_leaves[persistent=true]
fill -8 210 -20 -5 210 -20 minecraft:oak_leaves[persistent=true]
fill -15 209 -20 -12 210 -20 minecraft:oak_leaves[persistent=true]
fill -7 203 -20 -5 204 -20 minecraft:moss_block
fill -4 210 -20 -1 210 -20 minecraft:oak_leaves[persistent=true]
fill -19 208 -20 -14 210 -20 minecraft:mossy_cobblestone
fill -7 201 -1 -2 204 -1 minecraft:mossy_cobblestone
fill -15 210 -1 -10 210 -1 minecraft:oak_leaves[persistent=true]
fill -15 209 -1 -11 210 -1 minecraft:mossy_cobblestone
fill -10 205 -1 -6 205 -1 minecraft:cobblestone
fill -7 204 -1 -5 206 -1 minecraft:mossy_cobblestone
fill -10 203 -1 -7 203 -1 minecraft:andesite
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -10 201 -5 -7 201 -5 minecraft:podzol
fill -11 201 -4 -9 201 -4 minecraft:podzol
fill -6 201 -4 -2 201 -4 minecraft:podzol
fill -10 201 -3 -10 201 -2 minecraft:podzol
fill -2 201 -3 -2 201 -2 minecraft:podzol
fill -9 201 -2 -9 201 -2 minecraft:podzol
fill -3 201 -2 -3 201 -2 minecraft:podzol
fill -8 201 -4 -7 201 -2 minecraft:dirt
fill -8 202 -4 -7 202 -2 minecraft:podzol
fill -9 201 -3 -9 201 -3 minecraft:dirt
fill -9 202 -3 -9 202 -3 minecraft:podzol
fill -6 201 -3 -3 201 -3 minecraft:dirt
fill -6 202 -3 -3 202 -3 minecraft:podzol
fill -6 201 -2 -4 201 -2 minecraft:dirt
fill -6 202 -2 -4 202 -2 minecraft:podzol
fill -17 201 -3 -14 206 -2 minecraft:stone
fill -17 207 -3 -14 207 -2 minecraft:podzol
fill -20 186 -20 -16 199 -8 minecraft:stone
fill -19 186 -19 -17 186 -9 minecraft:dirt
fill -19 187 -19 -17 188 -9 minecraft:azalea_leaves[persistent=true]
fill -19 189 -19 -17 201 -9 minecraft:air
execute positioned -11 201 -2 run function rlk:room/prop/p_pillar_ruin
execute positioned -10 201 -19 run function rlk:room/prop/p_fence_x
execute positioned -16 201 -15 run function rlk:room/prop/p_fence_z
execute positioned -16 201 -8 run function rlk:room/prop/p_hay
execute positioned -12 201 -15 run function rlk:room/prop/p_ruin_x
execute positioned -6 201 -11 run function rlk:room/prop/p_wildflower
execute positioned -18 201 -11 run function rlk:room/prop/p_dandelion
execute positioned -7 201 -11 run function rlk:room/prop/p_litter
execute positioned -18 201 -13 run function rlk:room/prop/p_grass
execute positioned -9 202 -5 run function rlk:room/prop/p_grass
execute positioned -9 202 -4 run function rlk:room/prop/p_grass
execute positioned -5 202 -4 run function rlk:room/prop/p_wildflower
setblock -17 208 -3 minecraft:azalea_leaves[persistent=true] keep
setblock -16 208 -3 minecraft:short_grass keep
setblock -16 208 -2 minecraft:azalea_leaves[persistent=true] keep
setblock -15 208 -3 minecraft:azalea_leaves[persistent=true] keep
setblock -15 208 -2 minecraft:azalea_leaves[persistent=true] keep
setblock -14 208 -3 minecraft:short_grass keep
setblock -14 208 -2 minecraft:short_grass keep
