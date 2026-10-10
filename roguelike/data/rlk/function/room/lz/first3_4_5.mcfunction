# 구역 건설 (first3_4, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -20 -21 200 -1 minecraft:podzol
fill -40 201 -20 -21 212 -1 minecraft:moss_block
fill -39 201 -19 -22 212 -2 minecraft:air
fill -39 211 -19 -22 211 -2 minecraft:light[level=15]
fill -26 202 -16 -23 202 -15 minecraft:packed_mud
fill -40 201 -18 -40 212 -18 minecraft:jungle_log
fill -40 212 -17 -40 212 -13 minecraft:azalea_leaves[persistent=true]
fill -40 211 -2 -40 212 -1 minecraft:jungle_leaves[persistent=true]
fill -21 212 -5 -21 212 -4 minecraft:stone
fill -21 212 -4 -21 212 -2 minecraft:jungle_leaves[persistent=true]
fill -21 201 -9 -21 212 -9 minecraft:jungle_log
fill -34 201 -20 -34 212 -20 minecraft:jungle_log
fill -39 211 -20 -36 211 -20 minecraft:mossy_cobblestone
fill -25 211 -20 -21 212 -20 minecraft:azalea_leaves[persistent=true]
fill -36 211 -20 -31 212 -20 minecraft:stone
fill -32 211 -1 -28 212 -1 minecraft:mossy_cobblestone
fill -33 207 -1 -28 208 -1 minecraft:stone
fill -23 211 -1 -21 212 -1 minecraft:jungle_leaves[persistent=true]
fill -40 212 -20 -21 212 -1 minecraft:polished_deepslate
fill -39 212 -19 -22 212 -2 minecraft:air
fill -39 201 -19 -28 201 -19 minecraft:dirt
fill -39 202 -19 -28 202 -19 minecraft:podzol
fill -39 201 -18 -29 201 -18 minecraft:dirt
fill -39 202 -18 -29 202 -18 minecraft:podzol
fill -39 201 -17 -31 201 -2 minecraft:dirt
fill -39 202 -17 -31 202 -2 minecraft:podzol
fill -26 201 -16 -22 201 -2 minecraft:dirt
fill -26 202 -16 -22 202 -2 minecraft:podzol
fill -30 201 -15 -28 201 -2 minecraft:dirt
fill -30 202 -15 -28 202 -2 minecraft:podzol
fill -27 201 -14 -27 201 -2 minecraft:dirt
fill -27 202 -14 -27 202 -2 minecraft:podzol
fill -28 201 -18 -27 202 -16 minecraft:dirt
fill -28 203 -18 -27 203 -16 minecraft:podzol
fill -26 201 -17 -22 202 -17 minecraft:dirt
fill -26 203 -17 -22 203 -17 minecraft:podzol
fill -27 201 -15 -27 202 -15 minecraft:dirt
fill -27 203 -15 -27 203 -15 minecraft:podzol
fill -26 201 -18 -22 203 -18 minecraft:dirt
fill -26 204 -18 -22 204 -18 minecraft:podzol
fill -30 201 -17 -29 208 -16 minecraft:mossy_cobblestone
fill -30 209 -17 -29 209 -16 minecraft:podzol
fill -24 201 -19 -22 209 -19 minecraft:mossy_cobblestone
fill -24 210 -19 -22 210 -19 minecraft:podzol
fill -27 201 -19 -25 209 -19 minecraft:stone
fill -27 210 -19 -25 210 -19 minecraft:podzol
execute positioned -35 203 -4 run function rlk:room/prop/sf_mush_s
execute positioned -30 203 -4 run function rlk:room/prop/sf_ruin_z
execute positioned -36 203 -15 run function rlk:room/prop/sf_rock
execute positioned -33 203 -5 run function rlk:room/prop/sf_lamp
execute positioned -28 203 -13 run function rlk:room/prop/p_litter
execute positioned -27 203 -6 run function rlk:room/prop/sf_flower
execute positioned -34 203 -19 run function rlk:room/prop/sf_fern
execute positioned -28 203 -5 run function rlk:room/prop/sf_flower
execute positioned -39 203 -4 run function rlk:room/prop/sf_flower
execute positioned -33 203 -4 run function rlk:room/prop/sf_moss
execute positioned -38 203 -14 run function rlk:room/prop/sf_moss
execute positioned -35 203 -4 run function rlk:room/prop/sf_fern
execute positioned -25 203 -6 run function rlk:room/prop/sf_fern
execute positioned -38 203 -17 run function rlk:room/prop/sf_fern
setblock -30 210 -17 minecraft:fern keep
setblock -30 210 -16 minecraft:fern keep
setblock -29 210 -17 minecraft:jungle_leaves[persistent=true] keep
setblock -29 210 -16 minecraft:fern keep
setblock -27 211 -19 minecraft:jungle_leaves[persistent=true] keep
setblock -25 211 -19 minecraft:fern keep
setblock -24 211 -19 minecraft:fern keep
setblock -22 211 -19 minecraft:fern keep
