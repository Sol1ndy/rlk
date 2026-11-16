# 구역 건설 (normal21_6, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -9 200 -56 -8 200 -53 minecraft:rooted_dirt
fill -13 200 -44 -11 200 -42 minecraft:rooted_dirt
fill -20 206 -56 -20 207 -55 minecraft:cobblestone
fill -20 208 -44 -20 210 -42 minecraft:andesite
fill -20 206 -47 -20 208 -44 minecraft:moss_block
fill -1 203 -50 -1 206 -48 minecraft:andesite
fill -1 201 -51 -1 201 -47 minecraft:andesite
fill -1 204 -49 -1 204 -45 minecraft:moss_block
fill -1 209 -50 -1 209 -46 minecraft:cobblestone
fill -1 201 -52 -1 202 -48 minecraft:mossy_cobblestone
fill -7 209 -60 -4 210 -60 minecraft:oak_leaves[persistent=true]
fill -6 210 -60 -6 210 -60 minecraft:moss_block
fill -15 209 -60 -15 210 -60 minecraft:tuff
fill -19 209 -60 -15 210 -60 minecraft:oak_leaves[persistent=true]
fill -7 209 -60 -7 210 -60 minecraft:oak_leaves[persistent=true]
fill -14 210 -41 -11 210 -41 minecraft:oak_leaves[persistent=true]
fill -17 204 -41 -14 206 -41 minecraft:andesite
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -44 -17 201 -44 minecraft:podzol
fill -17 201 -43 -17 201 -42 minecraft:podzol
fill -19 201 -43 -18 201 -42 minecraft:dirt
fill -19 202 -43 -18 202 -42 minecraft:podzol
fill -12 201 -59 -8 205 -59 minecraft:andesite
fill -12 206 -59 -8 206 -59 minecraft:podzol
fill -13 201 -59 -13 205 -59 minecraft:stone
fill -13 206 -59 -13 206 -59 minecraft:podzol
execute positioned -5 201 -52 run function rlk:room/prop/p_oak_big
execute positioned -3 201 -43 run function rlk:room/prop/p_boulder
execute positioned -11 201 -55 run function rlk:room/prop/p_boulder_s
execute positioned -7 201 -52 run function rlk:room/prop/p_dandelion
execute positioned -5 201 -45 run function rlk:room/prop/p_grass
execute positioned -3 201 -49 run function rlk:room/prop/p_grass
execute positioned -2 201 -53 run function rlk:room/prop/p_wildflower
execute positioned -17 201 -56 run function rlk:room/prop/p_wildflower
execute positioned -11 201 -52 run function rlk:room/prop/p_wildflower
execute positioned -11 201 -50 run function rlk:room/prop/p_dandelion
execute positioned -14 201 -47 run function rlk:room/prop/p_dandelion
setblock -13 207 -59 minecraft:azalea_leaves[persistent=true] keep
setblock -12 207 -59 minecraft:short_grass keep
setblock -10 207 -59 minecraft:azalea_leaves[persistent=true] keep
setblock -9 207 -59 minecraft:short_grass keep
