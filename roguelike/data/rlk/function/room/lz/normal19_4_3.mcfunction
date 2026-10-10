# 구역 건설 (normal19_4, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -60 -41 200 -41 minecraft:podzol
fill -60 201 -60 -41 210 -41 minecraft:stone
fill -59 201 -59 -42 210 -42 minecraft:air
fill -59 209 -59 -42 209 -42 minecraft:light[level=15]
fill -48 200 -52 -46 200 -49 minecraft:rooted_dirt
fill -54 200 -50 -51 200 -49 minecraft:rooted_dirt
fill -45 200 -52 -44 200 -49 minecraft:coarse_dirt
fill -60 202 -41 -60 202 -41 minecraft:cobblestone
fill -60 206 -52 -60 208 -47 minecraft:moss_block
fill -60 209 -47 -60 210 -46 minecraft:mossy_cobblestone
fill -41 208 -56 -41 210 -55 minecraft:cobblestone
fill -41 201 -48 -41 203 -46 minecraft:andesite
fill -41 206 -50 -41 208 -47 minecraft:granite
fill -41 205 -56 -41 206 -53 minecraft:granite
fill -41 210 -56 -41 210 -53 minecraft:andesite
fill -41 209 -48 -41 210 -45 minecraft:oak_leaves[persistent=true]
fill -49 208 -60 -44 210 -60 minecraft:moss_block
fill -59 205 -60 -56 208 -60 minecraft:tuff
fill -49 204 -60 -46 205 -60 minecraft:tuff
fill -50 209 -60 -48 210 -60 minecraft:andesite
fill -59 203 -60 -59 206 -60 minecraft:tuff
fill -55 210 -60 -54 210 -60 minecraft:oak_leaves[persistent=true]
fill -47 202 -41 -43 203 -41 minecraft:moss_block
fill -60 210 -41 -58 210 -41 minecraft:andesite
fill -56 205 -41 -52 206 -41 minecraft:moss_block
fill -45 210 -41 -44 210 -41 minecraft:oak_leaves[persistent=true]
fill -56 204 -41 -54 206 -41 minecraft:andesite
fill -60 210 -60 -41 210 -41 minecraft:polished_deepslate
fill -59 210 -59 -42 210 -42 minecraft:air
fill -57 201 -59 -53 201 -59 minecraft:podzol
fill -57 201 -58 -56 201 -58 minecraft:podzol
fill -53 201 -58 -53 201 -55 minecraft:podzol
fill -59 201 -57 -57 201 -56 minecraft:podzol
fill -54 201 -55 -54 201 -55 minecraft:podzol
fill -55 201 -54 -55 201 -48 minecraft:podzol
fill -59 201 -48 -56 201 -47 minecraft:podzol
fill -55 201 -58 -54 201 -56 minecraft:dirt
fill -55 202 -58 -54 202 -56 minecraft:podzol
fill -56 201 -57 -56 201 -51 minecraft:dirt
fill -56 202 -57 -56 202 -51 minecraft:podzol
fill -59 201 -55 -57 201 -51 minecraft:dirt
fill -59 202 -55 -57 202 -51 minecraft:podzol
fill -55 201 -55 -55 201 -55 minecraft:dirt
fill -55 202 -55 -55 202 -55 minecraft:podzol
fill -59 201 -50 -58 201 -49 minecraft:dirt
fill -59 202 -50 -58 202 -49 minecraft:podzol
fill -42 201 -49 -42 206 -49 minecraft:andesite
fill -42 207 -49 -42 207 -49 minecraft:podzol
fill -42 201 -48 -42 206 -45 minecraft:stone
fill -42 207 -48 -42 207 -45 minecraft:podzol
fill -57 201 -50 -56 207 -49 minecraft:stone
fill -57 208 -50 -56 208 -49 minecraft:podzol
fill -51 186 -60 -41 199 -56 minecraft:stone
fill -50 186 -59 -42 186 -57 minecraft:dirt
fill -50 187 -59 -42 188 -57 minecraft:azalea_leaves[persistent=true]
fill -50 189 -59 -42 201 -57 minecraft:air
execute positioned -56 202 -59 run function rlk:room/prop/p_fence_x
execute positioned -45 201 -48 run function rlk:room/prop/p_lantern
execute positioned -45 201 -53 run function rlk:room/prop/p_boulder_s
execute positioned -58 201 -46 run function rlk:room/prop/p_dandelion
execute positioned -42 201 -51 run function rlk:room/prop/p_grass
execute positioned -59 203 -51 run function rlk:room/prop/p_wildflower
execute positioned -43 201 -57 run function rlk:room/prop/p_wildflower
execute positioned -51 201 -46 run function rlk:room/prop/p_grass
execute positioned -54 201 -51 run function rlk:room/prop/p_wildflower
execute positioned -51 201 -58 run function rlk:room/prop/p_dandelion
execute positioned -46 201 -56 run function rlk:room/prop/p_wildflower
setblock -57 209 -49 minecraft:short_grass keep
setblock -56 209 -50 minecraft:azalea_leaves[persistent=true] keep
setblock -56 209 -49 minecraft:short_grass keep
setblock -42 208 -48 minecraft:azalea_leaves[persistent=true] keep
setblock -42 208 -47 minecraft:short_grass keep
setblock -42 208 -45 minecraft:short_grass keep
