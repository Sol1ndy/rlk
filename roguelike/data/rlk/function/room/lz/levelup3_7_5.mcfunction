# 구역 건설 (levelup3_7, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 211 -21 minecraft:moss_block
fill -19 201 -39 -2 211 -22 minecraft:air
fill -19 210 -39 -2 210 -22 minecraft:light[level=15]
fill -17 201 -30 -16 201 -29 minecraft:rooted_dirt
fill -20 206 -30 -20 208 -26 minecraft:mossy_cobblestone
fill -20 202 -35 -20 204 -35 minecraft:mossy_cobblestone
fill -20 202 -24 -20 203 -23 minecraft:mossy_cobblestone
fill -20 210 -37 -20 211 -34 minecraft:jungle_leaves[persistent=true]
fill -20 210 -39 -20 211 -39 minecraft:azalea_leaves[persistent=true]
fill -1 201 -25 -1 211 -25 minecraft:jungle_log
fill -1 211 -39 -1 211 -36 minecraft:stone
fill -1 210 -30 -1 211 -26 minecraft:jungle_leaves[persistent=true]
fill -1 210 -29 -1 211 -26 minecraft:azalea_leaves[persistent=true]
fill -6 206 -40 -6 208 -40 minecraft:mossy_cobblestone
fill -11 210 -40 -8 211 -40 minecraft:jungle_leaves[persistent=true]
fill -19 206 -40 -18 209 -40 minecraft:mossy_cobblestone
fill -13 201 -40 -13 211 -40 minecraft:jungle_log
fill -19 210 -21 -15 211 -21 minecraft:jungle_leaves[persistent=true]
fill -10 211 -21 -5 211 -21 minecraft:jungle_leaves[persistent=true]
fill -15 210 -21 -12 211 -21 minecraft:azalea_leaves[persistent=true]
fill -20 211 -40 -1 211 -21 minecraft:polished_deepslate
fill -19 211 -39 -2 211 -22 minecraft:air
fill -19 201 -39 -2 201 -27 minecraft:podzol
fill -19 201 -26 -6 201 -26 minecraft:podzol
fill -3 201 -26 -2 201 -22 minecraft:podzol
fill -19 201 -25 -15 201 -25 minecraft:podzol
fill -19 201 -24 -17 201 -22 minecraft:podzol
fill -5 201 -26 -4 201 -26 minecraft:dirt
fill -5 202 -26 -4 202 -26 minecraft:podzol
fill -14 201 -25 -6 201 -25 minecraft:dirt
fill -14 202 -25 -6 202 -25 minecraft:podzol
fill -4 201 -25 -4 201 -22 minecraft:dirt
fill -4 202 -25 -4 202 -22 minecraft:podzol
fill -16 201 -24 -15 201 -24 minecraft:dirt
fill -16 202 -24 -15 202 -24 minecraft:podzol
fill -16 201 -23 -16 201 -22 minecraft:dirt
fill -16 202 -23 -16 202 -22 minecraft:podzol
fill -5 201 -25 -5 202 -22 minecraft:dirt
fill -5 203 -25 -5 203 -22 minecraft:podzol
fill -14 201 -24 -6 202 -24 minecraft:dirt
fill -14 203 -24 -6 203 -24 minecraft:podzol
fill -15 201 -23 -14 202 -22 minecraft:dirt
fill -15 203 -23 -14 203 -22 minecraft:podzol
fill -6 201 -23 -6 202 -22 minecraft:dirt
fill -6 203 -23 -6 203 -22 minecraft:podzol
fill -13 201 -23 -7 203 -23 minecraft:dirt
fill -13 204 -23 -7 204 -23 minecraft:podzol
fill -7 201 -22 -7 203 -22 minecraft:dirt
fill -7 204 -22 -7 204 -22 minecraft:podzol
fill -13 201 -22 -8 208 -22 minecraft:stone
fill -13 209 -22 -8 209 -22 minecraft:podzol
execute positioned -9 202 -37 run function rlk:room/prop/sf_mush_red
execute positioned -13 202 -37 run function rlk:room/prop/sf_mush_red
execute positioned -9 203 -25 run function rlk:room/prop/sf_ruin_x
execute positioned -17 202 -24 run function rlk:room/prop/sf_flower
execute positioned -14 202 -28 run function rlk:room/prop/p_litter
execute positioned -5 204 -22 run function rlk:room/prop/sf_fern
execute positioned -11 202 -26 run function rlk:room/prop/sf_fern
execute positioned -11 202 -30 run function rlk:room/prop/sf_moss
execute positioned -14 202 -32 run function rlk:room/prop/p_litter
execute positioned -15 202 -31 run function rlk:room/prop/sf_fern
execute positioned -13 202 -31 run function rlk:room/prop/sf_fern
execute positioned -19 202 -36 run function rlk:room/prop/p_litter
execute positioned -14 202 -33 run function rlk:room/prop/sf_flower
setblock -13 210 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -12 210 -22 minecraft:fern keep
setblock -11 210 -22 minecraft:fern keep
setblock -10 210 -22 minecraft:jungle_leaves[persistent=true] keep
setblock -9 210 -22 minecraft:fern keep
setblock -8 210 -22 minecraft:jungle_leaves[persistent=true] keep
