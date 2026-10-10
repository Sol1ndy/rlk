# 구역 건설 (root2_2, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:moss_block
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -9 200 -38 -5 200 -36 minecraft:packed_mud
fill -10 200 -32 -6 200 -29 minecraft:moss_block
fill -17 200 -33 -13 200 -30 minecraft:packed_mud
fill -20 207 -28 -20 207 -26 minecraft:mossy_cobblestone
fill -20 209 -29 -20 210 -25 minecraft:azalea_leaves[persistent=true]
fill -20 207 -36 -20 207 -34 minecraft:stone
fill -20 209 -31 -20 210 -29 minecraft:jungle_leaves[persistent=true]
fill -20 209 -33 -20 210 -30 minecraft:azalea_leaves[persistent=true]
fill -1 210 -36 -1 210 -34 minecraft:jungle_leaves[persistent=true]
fill -1 209 -26 -1 210 -23 minecraft:azalea_leaves[persistent=true]
fill -1 210 -26 -1 210 -23 minecraft:mossy_cobblestone
fill -18 210 -40 -14 210 -40 minecraft:jungle_leaves[persistent=true]
fill -17 206 -40 -17 209 -40 minecraft:mossy_cobblestone
fill -9 201 -40 -9 210 -40 minecraft:jungle_log
fill -10 209 -40 -8 210 -40 minecraft:jungle_leaves[persistent=true]
fill -4 202 -40 -4 204 -40 minecraft:stone
fill -9 209 -21 -4 209 -21 minecraft:mossy_cobblestone
fill -3 201 -21 -3 210 -21 minecraft:jungle_log
fill -8 209 -21 -7 210 -21 minecraft:azalea_leaves[persistent=true]
fill -17 209 -21 -12 210 -21 minecraft:jungle_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -15 201 -38 -14 201 -38 minecraft:podzol
fill -16 201 -37 -15 201 -37 minecraft:podzol
fill -19 201 -36 -16 201 -36 minecraft:podzol
fill -19 201 -35 -17 201 -35 minecraft:podzol
fill -19 201 -27 -18 201 -26 minecraft:podzol
fill -17 201 -26 -17 201 -22 minecraft:podzol
fill -19 201 -39 -17 201 -37 minecraft:dirt
fill -19 202 -39 -17 202 -37 minecraft:podzol
fill -16 201 -38 -16 201 -38 minecraft:dirt
fill -16 202 -38 -16 202 -38 minecraft:podzol
fill -19 201 -25 -18 201 -22 minecraft:dirt
fill -19 202 -25 -18 202 -22 minecraft:podzol
fill -16 201 -39 -11 207 -39 minecraft:mossy_cobblestone
fill -16 208 -39 -11 208 -39 minecraft:podzol
execute positioned -5 201 -35 run function rlk:room/prop/sf_lamp
execute positioned -15 201 -36 run function rlk:room/prop/sf_ruin_z
execute positioned -10 201 -22 run function rlk:room/prop/sf_flower
execute positioned -18 203 -23 run function rlk:room/prop/sf_fern
execute positioned -17 202 -24 run function rlk:room/prop/sf_fern
execute positioned -11 201 -26 run function rlk:room/prop/sf_flower
execute positioned -2 201 -31 run function rlk:room/prop/sf_moss
execute positioned -16 201 -31 run function rlk:room/prop/sf_flower
execute positioned -15 201 -31 run function rlk:room/prop/sf_flower
execute positioned -2 201 -30 run function rlk:room/prop/sf_fern
execute positioned -18 201 -32 run function rlk:room/prop/sf_flower
setblock -16 209 -39 minecraft:jungle_leaves[persistent=true] keep
setblock -15 209 -39 minecraft:jungle_leaves[persistent=true] keep
setblock -14 209 -39 minecraft:jungle_leaves[persistent=true] keep
setblock -13 209 -39 minecraft:fern keep
setblock -12 209 -39 minecraft:jungle_leaves[persistent=true] keep
setblock -11 209 -39 minecraft:fern keep
