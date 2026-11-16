# 구역 건설 (normal21_1, 테마 5 우림): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -20 -1 200 -1 minecraft:podzol
fill -20 201 -20 -1 210 -1 minecraft:moss_block
fill -19 201 -19 -2 210 -2 minecraft:air
fill -19 209 -19 -2 209 -2 minecraft:light[level=15]
fill -16 200 -12 -12 200 -9 minecraft:rooted_dirt
fill -16 200 -18 -14 200 -15 minecraft:moss_block
fill -5 200 -17 -3 200 -16 minecraft:moss_block
fill -11 200 -13 -9 200 -12 minecraft:coarse_dirt
fill -20 209 -5 -20 209 -4 minecraft:stone
fill -20 209 -11 -20 210 -6 minecraft:azalea_leaves[persistent=true]
fill -20 210 -5 -20 210 -2 minecraft:jungle_leaves[persistent=true]
fill -1 209 -12 -1 210 -11 minecraft:jungle_leaves[persistent=true]
fill -1 202 -4 -1 203 -2 minecraft:mossy_cobblestone
fill -1 210 -20 -1 210 -16 minecraft:jungle_leaves[persistent=true]
fill -1 209 -10 -1 210 -5 minecraft:azalea_leaves[persistent=true]
fill -1 210 -17 -1 210 -14 minecraft:jungle_leaves[persistent=true]
fill -1 201 -6 -1 210 -6 minecraft:jungle_log
fill -4 201 -20 -4 210 -20 minecraft:jungle_log
fill -16 202 -20 -13 202 -20 minecraft:stone
fill -18 210 -20 -16 210 -20 minecraft:stone
fill -8 209 -1 -8 210 -1 minecraft:jungle_leaves[persistent=true]
fill -17 210 -1 -16 210 -1 minecraft:jungle_leaves[persistent=true]
fill -9 210 -1 -4 210 -1 minecraft:mossy_cobblestone
fill -20 210 -20 -1 210 -1 minecraft:polished_deepslate
fill -19 210 -19 -2 210 -2 minecraft:air
fill -4 201 -7 -2 201 -7 minecraft:podzol
fill -5 201 -6 -5 201 -6 minecraft:podzol
fill -6 201 -5 -6 201 -5 minecraft:podzol
fill -7 201 -4 -7 201 -2 minecraft:podzol
fill -4 201 -6 -2 201 -6 minecraft:dirt
fill -4 202 -6 -2 202 -6 minecraft:podzol
fill -5 201 -5 -5 201 -5 minecraft:dirt
fill -5 202 -5 -5 202 -5 minecraft:podzol
fill -6 201 -4 -6 201 -2 minecraft:dirt
fill -6 202 -4 -6 202 -2 minecraft:podzol
fill -4 201 -5 -2 202 -2 minecraft:dirt
fill -4 203 -5 -2 203 -2 minecraft:podzol
fill -5 201 -4 -5 202 -2 minecraft:dirt
fill -5 203 -4 -5 203 -2 minecraft:podzol
fill -10 201 -17 -9 205 -16 minecraft:mossy_cobblestone
fill -10 206 -17 -9 206 -16 minecraft:podzol
fill -11 201 -19 -10 206 -18 minecraft:mossy_cobblestone
fill -11 207 -19 -10 207 -18 minecraft:podzol
fill -9 201 -18 -8 206 -18 minecraft:mossy_cobblestone
fill -9 207 -18 -8 207 -18 minecraft:podzol
fill -9 201 -19 -8 206 -19 minecraft:stone
fill -9 207 -19 -8 207 -19 minecraft:podzol
execute positioned -11 201 -5 run function rlk:room/prop/sf_ruin_x
execute positioned -15 201 -15 run function rlk:room/prop/sf_bush
execute positioned -19 201 -17 run function rlk:room/prop/sf_fern
execute positioned -14 201 -3 run function rlk:room/prop/sf_flower
execute positioned -4 204 -3 run function rlk:room/prop/sf_fern
execute positioned -12 201 -18 run function rlk:room/prop/sf_fern
execute positioned -2 201 -9 run function rlk:room/prop/sf_fern
execute positioned -13 201 -10 run function rlk:room/prop/sf_fern
execute positioned -17 201 -14 run function rlk:room/prop/sf_fern
execute positioned -4 201 -9 run function rlk:room/prop/sf_moss
execute positioned -7 201 -17 run function rlk:room/prop/sf_fern
execute positioned -5 204 -3 run function rlk:room/prop/sf_fern
execute positioned -9 201 -11 run function rlk:room/prop/sf_fern
setblock -11 208 -18 minecraft:fern keep
setblock -10 208 -19 minecraft:jungle_leaves[persistent=true] keep
setblock -10 208 -18 minecraft:jungle_leaves[persistent=true] keep
setblock -10 207 -17 minecraft:jungle_leaves[persistent=true] keep
setblock -10 207 -16 minecraft:fern keep
setblock -9 208 -19 minecraft:jungle_leaves[persistent=true] keep
setblock -9 208 -18 minecraft:jungle_leaves[persistent=true] keep
setblock -9 207 -17 minecraft:jungle_leaves[persistent=true] keep
setblock -9 207 -16 minecraft:fern keep
