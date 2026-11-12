# 구역 건설 (first3_4, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 210 -1 minecraft:moss_block
fill -39 201 -19 -22 210 -2 minecraft:air
fill -39 209 -19 -22 209 -2 minecraft:light[level=15]
fill -26 200 -16 -23 200 -15 minecraft:packed_mud
fill -40 201 -18 -40 210 -18 minecraft:jungle_log
fill -40 210 -17 -40 210 -13 minecraft:azalea_leaves[persistent=true]
fill -40 209 -2 -40 210 -1 minecraft:jungle_leaves[persistent=true]
fill -21 210 -5 -21 210 -4 minecraft:stone
fill -21 210 -4 -21 210 -2 minecraft:jungle_leaves[persistent=true]
fill -21 201 -9 -21 210 -9 minecraft:jungle_log
fill -34 201 -20 -34 210 -20 minecraft:jungle_log
fill -39 209 -20 -36 209 -20 minecraft:mossy_cobblestone
fill -25 209 -20 -21 210 -20 minecraft:azalea_leaves[persistent=true]
fill -36 209 -20 -31 210 -20 minecraft:stone
fill -32 209 -1 -28 210 -1 minecraft:mossy_cobblestone
fill -33 205 -1 -28 206 -1 minecraft:stone
fill -23 209 -1 -21 210 -1 minecraft:jungle_leaves[persistent=true]
fill -40 210 -20 -21 210 -1 minecraft:polished_deepslate
fill -39 210 -19 -22 210 -2 minecraft:air
fill -28 201 -18 -27 201 -16 minecraft:podzol
fill -26 201 -17 -22 201 -17 minecraft:podzol
fill -27 201 -15 -27 201 -15 minecraft:podzol
fill -26 201 -18 -22 201 -18 minecraft:dirt
fill -26 202 -18 -22 202 -18 minecraft:podzol
fill -30 201 -17 -29 206 -16 minecraft:mossy_cobblestone
fill -30 207 -17 -29 207 -16 minecraft:podzol
fill -24 201 -19 -22 207 -19 minecraft:mossy_cobblestone
fill -24 208 -19 -22 208 -19 minecraft:podzol
fill -27 201 -19 -25 207 -19 minecraft:stone
fill -27 208 -19 -25 208 -19 minecraft:podzol
execute positioned -35 201 -4 run function rlk:room/prop/sf_mush_s
execute positioned -30 201 -4 run function rlk:room/prop/sf_ruin_z
execute positioned -36 201 -15 run function rlk:room/prop/sf_rock
execute positioned -33 201 -5 run function rlk:room/prop/sf_lamp
execute positioned -28 201 -13 run function rlk:room/prop/p_litter
execute positioned -27 201 -6 run function rlk:room/prop/sf_flower
execute positioned -34 201 -19 run function rlk:room/prop/sf_fern
execute positioned -28 201 -5 run function rlk:room/prop/sf_flower
execute positioned -39 201 -4 run function rlk:room/prop/sf_flower
execute positioned -33 201 -4 run function rlk:room/prop/sf_moss
execute positioned -38 201 -14 run function rlk:room/prop/sf_moss
execute positioned -35 201 -4 run function rlk:room/prop/sf_fern
execute positioned -25 201 -6 run function rlk:room/prop/sf_fern
execute positioned -38 201 -17 run function rlk:room/prop/sf_fern
setblock -30 208 -17 minecraft:fern keep
setblock -30 208 -16 minecraft:fern keep
setblock -29 208 -17 minecraft:jungle_leaves[persistent=true] keep
setblock -29 208 -16 minecraft:fern keep
setblock -27 209 -19 minecraft:jungle_leaves[persistent=true] keep
setblock -25 209 -19 minecraft:fern keep
setblock -24 209 -19 minecraft:fern keep
setblock -22 209 -19 minecraft:fern keep
