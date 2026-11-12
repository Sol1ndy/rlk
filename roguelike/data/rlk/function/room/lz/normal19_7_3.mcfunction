# 구역 건설 (normal19_7, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:podzol
fill -20 201 -60 -1 210 -41 minecraft:stone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -18 200 -53 -17 200 -50 minecraft:rooted_dirt
fill -19 200 -53 -16 200 -51 minecraft:rooted_dirt
fill -20 209 -54 -20 209 -49 minecraft:mossy_cobblestone
fill -20 209 -45 -20 210 -44 minecraft:oak_leaves[persistent=true]
fill -20 201 -60 -20 202 -58 minecraft:andesite
fill -1 204 -56 -1 205 -52 minecraft:cobblestone
fill -1 209 -58 -1 210 -53 minecraft:oak_leaves[persistent=true]
fill -1 202 -46 -1 202 -42 minecraft:andesite
fill -1 209 -50 -1 210 -50 minecraft:granite
fill -16 201 -60 -12 202 -60 minecraft:tuff
fill -10 201 -60 -8 201 -60 minecraft:moss_block
fill -11 209 -60 -10 210 -60 minecraft:oak_leaves[persistent=true]
fill -16 201 -41 -11 201 -41 minecraft:andesite
fill -19 209 -41 -17 210 -41 minecraft:oak_leaves[persistent=true]
fill -15 210 -41 -11 210 -41 minecraft:andesite
fill -14 209 -41 -13 210 -41 minecraft:tuff
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -14 201 -45 -6 201 -45 minecraft:podzol
fill -16 201 -44 -15 201 -42 minecraft:podzol
fill -6 201 -44 -6 201 -42 minecraft:podzol
fill -17 201 -43 -17 201 -43 minecraft:podzol
fill -5 201 -43 -5 201 -43 minecraft:podzol
fill -14 201 -44 -7 201 -44 minecraft:dirt
fill -14 202 -44 -7 202 -44 minecraft:podzol
fill -14 201 -43 -10 201 -42 minecraft:dirt
fill -14 202 -43 -10 202 -42 minecraft:podzol
fill -9 201 -43 -7 207 -43 minecraft:andesite
fill -9 208 -43 -7 208 -43 minecraft:podzol
fill -9 201 -42 -7 207 -42 minecraft:stone
fill -9 208 -42 -7 208 -42 minecraft:podzol
execute positioned -12 201 -57 run function rlk:room/prop/p_lantern
execute positioned -10 201 -56 run function rlk:room/prop/p_dandelion
execute positioned -10 201 -57 run function rlk:room/prop/p_wildflower
execute positioned -10 201 -49 run function rlk:room/prop/p_dandelion
execute positioned -5 201 -54 run function rlk:room/prop/p_grass
execute positioned -12 201 -55 run function rlk:room/prop/p_wildflower
execute positioned -14 201 -51 run function rlk:room/prop/p_wildflower
setblock -9 209 -43 minecraft:azalea_leaves[persistent=true] keep
setblock -9 209 -42 minecraft:short_grass keep
setblock -8 209 -43 minecraft:azalea_leaves[persistent=true] keep
setblock -8 209 -42 minecraft:short_grass keep
setblock -7 209 -43 minecraft:azalea_leaves[persistent=true] keep
