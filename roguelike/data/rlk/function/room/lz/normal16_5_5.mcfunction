# 구역 건설 (normal16_5, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 0 -21 200 19 minecraft:podzol
fill -40 201 0 -21 210 19 minecraft:moss_block
fill -39 201 1 -22 210 18 minecraft:air
fill -39 209 1 -22 209 18 minecraft:light[level=15]
fill -27 200 12 -23 200 13 minecraft:rooted_dirt
fill -40 201 8 -40 202 11 minecraft:mossy_cobblestone
fill -40 210 14 -40 210 16 minecraft:mud_bricks
fill -40 210 4 -40 210 4 minecraft:jungle_leaves[persistent=true]
fill -40 209 2 -40 210 5 minecraft:jungle_leaves[persistent=true]
fill -21 201 5 -21 210 5 minecraft:jungle_log
fill -21 204 7 -21 206 8 minecraft:mossy_cobblestone
fill -21 210 2 -21 210 7 minecraft:jungle_leaves[persistent=true]
fill -21 202 1 -21 205 3 minecraft:stone
fill -21 201 18 -21 210 18 minecraft:jungle_log
fill -21 203 11 -21 205 16 minecraft:mossy_cobblestone
fill -40 201 0 -40 210 0 minecraft:jungle_log
fill -37 201 0 -37 201 0 minecraft:stone
fill -40 210 0 -37 210 0 minecraft:jungle_leaves[persistent=true]
fill -37 209 0 -32 209 0 minecraft:mossy_cobblestone
fill -37 201 0 -37 210 0 minecraft:jungle_log
fill -39 206 19 -34 208 19 minecraft:mossy_cobblestone
fill -25 201 19 -21 203 19 minecraft:mossy_cobblestone
fill -40 210 19 -38 210 19 minecraft:azalea_leaves[persistent=true]
fill -37 210 19 -34 210 19 minecraft:jungle_leaves[persistent=true]
fill -40 210 0 -21 210 19 minecraft:polished_deepslate
fill -39 210 1 -22 210 18 minecraft:air
fill -33 201 1 -33 201 5 minecraft:podzol
fill -27 201 1 -26 201 1 minecraft:podzol
fill -26 201 2 -26 201 3 minecraft:podzol
fill -27 201 3 -27 201 5 minecraft:podzol
fill -32 201 5 -28 201 5 minecraft:podzol
fill -35 201 11 -35 201 14 minecraft:podzol
fill -36 201 12 -36 201 15 minecraft:podzol
fill -37 201 13 -37 201 18 minecraft:podzol
fill -38 201 14 -38 201 18 minecraft:podzol
fill -34 201 15 -27 201 15 minecraft:podzol
fill -27 201 16 -26 201 18 minecraft:podzol
fill -32 201 1 -28 201 4 minecraft:dirt
fill -32 202 1 -28 202 4 minecraft:podzol
fill -27 201 2 -27 201 2 minecraft:dirt
fill -27 202 2 -27 202 2 minecraft:podzol
fill -35 201 15 -35 201 17 minecraft:dirt
fill -35 202 15 -35 202 17 minecraft:podzol
fill -36 201 16 -36 201 18 minecraft:dirt
fill -36 202 16 -36 202 18 minecraft:podzol
fill -34 201 16 -28 201 17 minecraft:dirt
fill -34 202 16 -28 202 17 minecraft:podzol
fill -29 201 18 -28 201 18 minecraft:dirt
fill -29 202 18 -28 202 18 minecraft:podzol
fill -35 201 18 -30 207 18 minecraft:mossy_cobblestone
fill -35 208 18 -30 208 18 minecraft:podzol
fill -40 186 0 -35 199 7 minecraft:stone
fill -39 186 1 -36 186 6 minecraft:dirt
fill -39 187 1 -36 188 6 minecraft:jungle_leaves[persistent=true]
fill -39 189 1 -36 201 6 minecraft:air
execute positioned -33 202 3 run function rlk:room/prop/sf_ruin_z
execute positioned -24 201 3 run function rlk:room/prop/sf_lamp
execute positioned -37 202 15 run function rlk:room/prop/sf_mush_s
execute positioned -30 201 8 run function rlk:room/prop/sf_fern
execute positioned -27 202 15 run function rlk:room/prop/sf_fern
execute positioned -25 201 18 run function rlk:room/prop/sf_fern
execute positioned -36 203 16 run function rlk:room/prop/sf_moss
execute positioned -23 201 4 run function rlk:room/prop/sf_fern
execute positioned -27 202 17 run function rlk:room/prop/sf_flower
execute positioned -29 201 13 run function rlk:room/prop/sf_fern
execute positioned -32 201 11 run function rlk:room/prop/sf_fern
execute positioned -29 203 2 run function rlk:room/prop/p_litter
setblock -35 209 18 minecraft:jungle_leaves[persistent=true] keep
setblock -34 209 18 minecraft:jungle_leaves[persistent=true] keep
setblock -33 209 18 minecraft:jungle_leaves[persistent=true] keep
setblock -32 209 18 minecraft:fern keep
setblock -31 209 18 minecraft:jungle_leaves[persistent=true] keep
setblock -30 209 18 minecraft:jungle_leaves[persistent=true] keep
