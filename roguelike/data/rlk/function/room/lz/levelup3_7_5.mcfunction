# 구역 건설 (levelup3_7, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:moss_block
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -17 200 -30 -16 200 -29 minecraft:rooted_dirt
fill -20 205 -30 -20 207 -26 minecraft:mossy_cobblestone
fill -20 201 -35 -20 203 -35 minecraft:mossy_cobblestone
fill -20 201 -24 -20 202 -23 minecraft:mossy_cobblestone
fill -20 209 -37 -20 210 -34 minecraft:jungle_leaves[persistent=true]
fill -20 209 -39 -20 210 -39 minecraft:azalea_leaves[persistent=true]
fill -1 201 -25 -1 210 -25 minecraft:jungle_log
fill -1 210 -39 -1 210 -36 minecraft:stone
fill -1 209 -30 -1 210 -26 minecraft:jungle_leaves[persistent=true]
fill -1 209 -29 -1 210 -26 minecraft:azalea_leaves[persistent=true]
fill -6 205 -40 -6 207 -40 minecraft:mossy_cobblestone
fill -11 209 -40 -8 210 -40 minecraft:jungle_leaves[persistent=true]
fill -19 205 -40 -18 208 -40 minecraft:mossy_cobblestone
fill -13 201 -40 -13 210 -40 minecraft:jungle_log
fill -19 209 -21 -15 210 -21 minecraft:jungle_leaves[persistent=true]
fill -10 210 -21 -5 210 -21 minecraft:jungle_leaves[persistent=true]
fill -15 209 -21 -12 210 -21 minecraft:azalea_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -5 201 -26 -4 201 -26 minecraft:podzol
fill -14 201 -25 -6 201 -25 minecraft:podzol
fill -4 201 -25 -4 201 -22 minecraft:podzol
fill -16 201 -24 -15 201 -24 minecraft:podzol
fill -16 201 -23 -16 201 -22 minecraft:podzol
fill -5 201 -25 -5 201 -22 minecraft:dirt
fill -5 202 -25 -5 202 -22 minecraft:podzol
fill -14 201 -24 -6 201 -24 minecraft:dirt
fill -14 202 -24 -6 202 -24 minecraft:podzol
fill -15 201 -23 -14 201 -22 minecraft:dirt
fill -15 202 -23 -14 202 -22 minecraft:podzol
fill -6 201 -23 -6 201 -22 minecraft:dirt
fill -6 202 -23 -6 202 -22 minecraft:podzol
fill -13 201 -23 -7 202 -23 minecraft:dirt
fill -13 203 -23 -7 203 -23 minecraft:podzol
fill -7 201 -22 -7 202 -22 minecraft:dirt
fill -7 203 -22 -7 203 -22 minecraft:podzol
fill -13 201 -22 -8 207 -22 minecraft:stone
fill -13 208 -22 -8 208 -22 minecraft:podzol
execute positioned -9 201 -37 run function rlk:room/prop/sf_mush_red
execute positioned -13 201 -37 run function rlk:room/prop/sf_mush_red
execute positioned -9 202 -25 run function rlk:room/prop/sf_ruin_x
execute positioned -17 201 -24 run function rlk:room/prop/sf_flower
execute positioned -14 201 -28 run function rlk:room/prop/p_litter
execute positioned -5 203 -22 run function rlk:room/prop/sf_fern
execute positioned -11 201 -26 run function rlk:room/prop/sf_fern
execute positioned -11 201 -30 run function rlk:room/prop/sf_moss
execute positioned -14 201 -32 run function rlk:room/prop/p_litter
execute positioned -15 201 -31 run function rlk:room/prop/sf_fern
execute positioned -13 201 -31 run function rlk:room/prop/sf_fern
execute positioned -19 201 -36 run function rlk:room/prop/p_litter
execute positioned -14 201 -33 run function rlk:room/prop/sf_flower
setblock -13 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -12 209 -22 minecraft:fern keep
setblock -11 209 -22 minecraft:fern keep
setblock -10 209 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -9 209 -22 minecraft:fern keep
setblock -8 209 -22 minecraft:jungle_leaves[persistent=true] keep
