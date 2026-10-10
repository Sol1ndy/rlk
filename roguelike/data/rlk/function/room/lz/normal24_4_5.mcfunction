# 구역 건설 (normal24_4, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:moss_block
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -11 200 -34 -7 200 -32 minecraft:moss_block
fill -13 200 -33 -10 200 -30 minecraft:rooted_dirt
fill -20 201 -26 -20 210 -26 minecraft:jungle_log
fill -20 209 -31 -20 210 -31 minecraft:jungle_leaves[persistent=true]
fill -20 201 -30 -20 210 -30 minecraft:jungle_log
fill -1 210 -27 -1 210 -27 minecraft:jungle_leaves[persistent=true]
fill -1 210 -25 -1 210 -23 minecraft:jungle_leaves[persistent=true]
fill -1 201 -31 -1 210 -31 minecraft:jungle_log
fill -17 201 -40 -17 210 -40 minecraft:jungle_log
fill -6 209 -40 -1 210 -40 minecraft:azalea_leaves[persistent=true]
fill -5 210 -40 -4 210 -40 minecraft:jungle_leaves[persistent=true]
fill -1 205 -40 -1 205 -40 minecraft:mud_bricks
fill -3 210 -21 -2 210 -21 minecraft:jungle_leaves[persistent=true]
fill -15 202 -21 -13 202 -21 minecraft:mossy_cobblestone
fill -6 210 -21 -6 210 -21 minecraft:jungle_leaves[persistent=true]
fill -8 201 -21 -8 210 -21 minecraft:jungle_log
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -7 201 -39 -7 201 -35 minecraft:podzol
fill -19 201 -35 -17 201 -35 minecraft:podzol
fill -6 201 -35 -6 201 -35 minecraft:podzol
fill -17 201 -34 -16 201 -27 minecraft:podzol
fill -5 201 -34 -5 201 -33 minecraft:podzol
fill -4 201 -33 -2 201 -33 minecraft:podzol
fill -19 201 -26 -17 201 -26 minecraft:podzol
fill -19 201 -25 -18 201 -25 minecraft:podzol
fill -6 201 -39 -5 201 -39 minecraft:dirt
fill -6 202 -39 -5 202 -39 minecraft:podzol
fill -6 201 -38 -6 201 -36 minecraft:dirt
fill -6 202 -38 -6 202 -36 minecraft:podzol
fill -5 201 -35 -5 201 -35 minecraft:dirt
fill -5 202 -35 -5 202 -35 minecraft:podzol
fill -19 201 -34 -18 201 -27 minecraft:dirt
fill -19 202 -34 -18 202 -27 minecraft:podzol
fill -4 201 -34 -2 201 -34 minecraft:dirt
fill -4 202 -34 -2 202 -34 minecraft:podzol
fill -4 201 -39 -2 202 -35 minecraft:dirt
fill -4 203 -39 -2 203 -35 minecraft:podzol
fill -5 201 -38 -5 202 -36 minecraft:dirt
fill -5 203 -38 -5 203 -36 minecraft:podzol
fill -11 201 -36 -10 207 -36 minecraft:mossy_cobblestone
fill -11 208 -36 -10 208 -36 minecraft:podzol
fill -7 201 -23 -2 207 -23 minecraft:mossy_cobblestone
fill -7 208 -23 -2 208 -23 minecraft:podzol
fill -6 201 -22 -2 207 -22 minecraft:mossy_cobblestone
fill -6 208 -22 -2 208 -22 minecraft:podzol
fill -11 201 -37 -10 207 -37 minecraft:stone
fill -11 208 -37 -10 208 -37 minecraft:podzol
fill -7 201 -22 -7 207 -22 minecraft:stone
fill -7 208 -22 -7 208 -22 minecraft:podzol
execute positioned -10 201 -25 run function rlk:room/prop/sf_mush_red
execute positioned -5 201 -28 run function rlk:room/prop/sf_tree
execute positioned -4 204 -37 run function rlk:room/prop/sf_mush_s
execute positioned -4 201 -30 run function rlk:room/prop/sf_mush_red
execute positioned -12 201 -22 run function rlk:room/prop/sf_ruin_x
execute positioned -17 201 -24 run function rlk:room/prop/sf_lamp
execute positioned -16 201 -37 run function rlk:room/prop/sf_bush
execute positioned -18 203 -33 run function rlk:room/prop/p_litter
execute positioned -7 201 -30 run function rlk:room/prop/sf_moss
execute positioned -19 203 -29 run function rlk:room/prop/sf_fern
execute positioned -3 201 -28 run function rlk:room/prop/sf_flower
execute positioned -19 201 -38 run function rlk:room/prop/sf_moss
execute positioned -12 201 -23 run function rlk:room/prop/sf_fern
execute positioned -5 202 -33 run function rlk:room/prop/sf_fern
execute positioned -4 201 -32 run function rlk:room/prop/sf_flower
execute positioned -12 201 -32 run function rlk:room/prop/sf_moss
execute positioned -14 201 -25 run function rlk:room/prop/sf_flower
setblock -11 209 -37 minecraft:jungle_leaves[persistent=true] keep
setblock -7 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -6 209 -23 minecraft:fern keep
setblock -5 209 -23 minecraft:fern keep
setblock -4 209 -23 minecraft:fern keep
setblock -3 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -2 209 -23 minecraft:jungle_leaves[persistent=true] keep
setblock -2 209 -22 minecraft:fern keep
