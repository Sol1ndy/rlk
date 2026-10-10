# 구역 건설 (normal6_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:moss_block
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -11 200 -11 -8 200 -9 minecraft:packed_mud
fill -6 200 -9 -5 200 -7 minecraft:rooted_dirt
fill -20 204 -20 -20 204 -18 minecraft:mossy_cobblestone
fill -20 209 -9 -20 210 -5 minecraft:azalea_leaves[persistent=true]
fill -20 210 -16 -20 210 -16 minecraft:azalea_leaves[persistent=true]
fill -20 208 -20 -20 210 -17 minecraft:mossy_cobblestone
fill -1 210 -20 -1 210 -20 minecraft:azalea_leaves[persistent=true]
fill -1 209 -9 -1 210 -6 minecraft:jungle_leaves[persistent=true]
fill -1 209 -16 -1 210 -13 minecraft:jungle_leaves[persistent=true]
fill -5 203 -20 -2 206 -20 minecraft:stone
fill -19 208 -20 -18 209 -20 minecraft:mossy_cobblestone
fill -7 205 -20 -5 208 -20 minecraft:mud_bricks
fill -1 201 -20 -1 201 -20 minecraft:mossy_cobblestone
fill -14 209 -1 -10 210 -1 minecraft:mossy_cobblestone
fill -6 206 -1 -4 206 -1 minecraft:stone
fill -14 210 -1 -10 210 -1 minecraft:jungle_leaves[persistent=true]
fill -12 207 -1 -9 209 -1 minecraft:mossy_cobblestone
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -18 201 -19 -18 201 -16 minecraft:podzol
fill -10 201 -19 -10 201 -16 minecraft:podzol
fill -17 201 -15 -17 201 -15 minecraft:podzol
fill -14 201 -15 -11 201 -15 minecraft:podzol
fill -16 201 -14 -15 201 -14 minecraft:podzol
fill -17 201 -19 -17 201 -16 minecraft:dirt
fill -17 202 -19 -17 202 -16 minecraft:podzol
fill -11 201 -19 -11 201 -16 minecraft:dirt
fill -11 202 -19 -11 202 -16 minecraft:podzol
fill -16 201 -16 -16 201 -15 minecraft:dirt
fill -16 202 -16 -16 202 -15 minecraft:podzol
fill -12 201 -16 -12 201 -16 minecraft:dirt
fill -12 202 -16 -12 202 -16 minecraft:podzol
fill -15 201 -15 -15 201 -15 minecraft:dirt
fill -15 202 -15 -15 202 -15 minecraft:podzol
fill -16 201 -19 -12 202 -18 minecraft:dirt
fill -16 203 -19 -12 203 -18 minecraft:podzol
fill -16 201 -17 -15 202 -17 minecraft:dirt
fill -16 203 -17 -15 203 -17 minecraft:podzol
fill -12 201 -17 -12 202 -17 minecraft:dirt
fill -12 203 -17 -12 203 -17 minecraft:podzol
fill -15 201 -16 -15 202 -16 minecraft:dirt
fill -15 203 -16 -15 203 -16 minecraft:podzol
fill -19 201 -12 -18 206 -12 minecraft:mossy_cobblestone
fill -19 207 -12 -18 207 -12 minecraft:podzol
fill -19 201 -14 -18 206 -13 minecraft:stone
fill -19 207 -14 -18 207 -13 minecraft:podzol
fill -14 201 -17 -13 207 -17 minecraft:mossy_cobblestone
fill -14 208 -17 -13 208 -17 minecraft:podzol
fill -14 201 -16 -13 207 -16 minecraft:stone
fill -14 208 -16 -13 208 -16 minecraft:podzol
execute positioned -16 201 -11 run function rlk:room/prop/sf_bush
execute positioned -5 201 -16 run function rlk:room/prop/sf_mush_red
execute positioned -4 201 -11 run function rlk:room/prop/sf_ruin_x
execute positioned -16 203 -16 run function rlk:room/prop/sf_fern
execute positioned -9 201 -14 run function rlk:room/prop/sf_moss
execute positioned -9 201 -5 run function rlk:room/prop/p_litter
execute positioned -9 201 -17 run function rlk:room/prop/sf_fern
execute positioned -4 201 -10 run function rlk:room/prop/sf_moss
execute positioned -17 203 -19 run function rlk:room/prop/sf_fern
execute positioned -18 201 -2 run function rlk:room/prop/sf_fern
execute positioned -16 201 -7 run function rlk:room/prop/sf_moss
execute positioned -5 201 -4 run function rlk:room/prop/sf_fern
setblock -19 208 -14 minecraft:jungle_leaves[persistent=true] keep
setblock -18 208 -14 minecraft:jungle_leaves[persistent=true] keep
setblock -18 208 -13 minecraft:jungle_leaves[persistent=true] keep
setblock -18 208 -12 minecraft:jungle_leaves[persistent=true] keep
setblock -14 209 -17 minecraft:jungle_leaves[persistent=true] keep
setblock -14 209 -16 minecraft:fern keep
