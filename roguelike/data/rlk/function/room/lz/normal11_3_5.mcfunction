# 구역 건설 (normal11_3, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 -40 -21 200 -21 minecraft:podzol
fill -40 201 -40 -21 210 -21 minecraft:moss_block
fill -39 201 -39 -22 210 -22 minecraft:air
fill -39 209 -39 -22 209 -22 minecraft:light[level=15]
fill -27 200 -26 -25 200 -24 minecraft:packed_mud
fill -40 201 -29 -40 210 -29 minecraft:jungle_log
fill -40 209 -36 -40 210 -33 minecraft:jungle_leaves[persistent=true]
fill -40 201 -33 -40 210 -33 minecraft:jungle_log
fill -21 209 -36 -21 210 -35 minecraft:azalea_leaves[persistent=true]
fill -21 210 -37 -21 210 -37 minecraft:jungle_leaves[persistent=true]
fill -21 208 -26 -21 209 -25 minecraft:mud_bricks
fill -21 204 -37 -21 205 -34 minecraft:mud_bricks
fill -30 209 -40 -25 210 -40 minecraft:jungle_leaves[persistent=true]
fill -25 210 -40 -23 210 -40 minecraft:jungle_leaves[persistent=true]
fill -33 209 -40 -31 210 -40 minecraft:mossy_cobblestone
fill -31 203 -40 -29 204 -40 minecraft:mud_bricks
fill -40 201 -40 -40 210 -40 minecraft:jungle_log
fill -39 201 -40 -39 210 -40 minecraft:jungle_log
fill -29 202 -21 -26 203 -21 minecraft:mossy_cobblestone
fill -23 209 -21 -22 210 -21 minecraft:azalea_leaves[persistent=true]
fill -24 201 -21 -24 210 -21 minecraft:jungle_log
fill -40 210 -40 -21 210 -21 minecraft:polished_deepslate
fill -39 210 -39 -22 210 -22 minecraft:air
fill -28 201 -39 -27 201 -39 minecraft:podzol
fill -23 201 -39 -22 201 -39 minecraft:podzol
fill -28 201 -38 -28 201 -35 minecraft:podzol
fill -22 201 -38 -22 201 -37 minecraft:podzol
fill -29 201 -37 -29 201 -37 minecraft:podzol
fill -26 201 -37 -23 201 -37 minecraft:podzol
fill -27 201 -36 -27 201 -35 minecraft:podzol
fill -38 201 -28 -37 201 -22 minecraft:podzol
fill -36 201 -27 -36 201 -27 minecraft:podzol
fill -39 201 -24 -39 201 -22 minecraft:podzol
fill -26 201 -39 -24 201 -38 minecraft:dirt
fill -26 202 -39 -24 202 -38 minecraft:podzol
fill -27 201 -38 -27 201 -37 minecraft:dirt
fill -27 202 -38 -27 202 -37 minecraft:podzol
fill -23 201 -38 -23 201 -38 minecraft:dirt
fill -23 202 -38 -23 202 -38 minecraft:podzol
fill -37 201 -37 -36 207 -37 minecraft:mossy_cobblestone
fill -37 208 -37 -36 208 -37 minecraft:podzol
fill -36 201 -36 -36 207 -36 minecraft:mossy_cobblestone
fill -36 208 -36 -36 208 -36 minecraft:podzol
fill -39 201 -26 -39 207 -25 minecraft:mossy_cobblestone
fill -39 208 -26 -39 208 -25 minecraft:podzol
fill -37 201 -36 -37 207 -36 minecraft:stone
fill -37 208 -36 -37 208 -36 minecraft:podzol
fill -39 201 -29 -39 207 -27 minecraft:stone
fill -39 208 -29 -39 208 -27 minecraft:podzol
execute positioned -32 201 -39 run function rlk:room/prop/sf_rock
execute positioned -33 201 -35 run function rlk:room/prop/sf_mush_red
execute positioned -28 202 -36 run function rlk:room/prop/sf_bush
execute positioned -39 202 -22 run function rlk:room/prop/sf_ruin_x
execute positioned -37 201 -32 run function rlk:room/prop/sf_ruin_x
execute positioned -32 201 -36 run function rlk:room/prop/sf_moss
execute positioned -31 201 -29 run function rlk:room/prop/sf_moss
execute positioned -24 201 -33 run function rlk:room/prop/sf_fern
execute positioned -32 201 -36 run function rlk:room/prop/sf_moss
execute positioned -27 201 -23 run function rlk:room/prop/sf_moss
execute positioned -37 201 -38 run function rlk:room/prop/sf_moss
execute positioned -35 201 -27 run function rlk:room/prop/sf_moss
execute positioned -30 201 -39 run function rlk:room/prop/sf_fern
execute positioned -23 201 -28 run function rlk:room/prop/p_litter
execute positioned -27 202 -35 run function rlk:room/prop/sf_flower
execute positioned -26 201 -22 run function rlk:room/prop/sf_moss
execute positioned -37 201 -32 run function rlk:room/prop/sf_flower
setblock -39 209 -28 minecraft:fern keep
setblock -39 209 -27 minecraft:jungle_leaves[persistent=true] keep
setblock -39 209 -26 minecraft:fern keep
setblock -39 209 -25 minecraft:fern keep
setblock -37 209 -37 minecraft:fern keep
setblock -36 209 -37 minecraft:jungle_leaves[persistent=true] keep
setblock -36 209 -36 minecraft:jungle_leaves[persistent=true] keep
