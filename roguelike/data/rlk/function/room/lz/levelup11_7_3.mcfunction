# 구역 건설 (levelup11_7, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 40 -41 200 59 minecraft:podzol
fill -60 201 40 -41 210 59 minecraft:stone
fill -59 201 41 -42 210 58 minecraft:air
fill -59 209 41 -42 209 58 minecraft:light[level=15]
fill -51 200 43 -47 200 46 minecraft:moss_block
fill -48 200 54 -44 200 55 minecraft:coarse_dirt
fill -53 200 41 -51 200 44 minecraft:coarse_dirt
fill -60 206 40 -60 209 44 minecraft:andesite
fill -60 206 40 -60 207 40 minecraft:mossy_cobblestone
fill -60 209 56 -60 210 59 minecraft:oak_leaves[persistent=true]
fill -60 202 40 -60 205 45 minecraft:andesite
fill -60 206 56 -60 207 59 minecraft:andesite
fill -41 203 40 -41 205 45 minecraft:tuff
fill -41 209 54 -41 210 54 minecraft:oak_leaves[persistent=true]
fill -41 210 44 -41 210 48 minecraft:oak_leaves[persistent=true]
fill -41 206 45 -41 207 47 minecraft:tuff
fill -47 206 40 -45 209 40 minecraft:moss_block
fill -45 206 40 -44 206 40 minecraft:andesite
fill -48 209 40 -46 210 40 minecraft:moss_block
fill -59 206 59 -55 207 59 minecraft:cobblestone
fill -60 208 59 -59 210 59 minecraft:andesite
fill -57 209 59 -53 210 59 minecraft:andesite
fill -48 205 59 -45 205 59 minecraft:tuff
fill -44 201 44 -42 201 44 minecraft:podzol
fill -59 201 47 -56 201 57 minecraft:podzol
fill -55 201 55 -49 201 55 minecraft:podzol
fill -55 201 56 -55 201 56 minecraft:podzol
fill -49 201 56 -49 201 56 minecraft:podzol
fill -48 201 57 -48 201 58 minecraft:podzol
fill -56 201 58 -56 201 58 minecraft:podzol
fill -44 201 45 -44 201 45 minecraft:andesite
fill -44 202 45 -44 202 45 minecraft:podzol
fill -43 201 45 -42 201 45 minecraft:dirt
fill -43 202 45 -42 202 45 minecraft:podzol
fill -54 201 56 -50 201 56 minecraft:dirt
fill -54 202 56 -50 202 56 minecraft:podzol
fill -55 201 57 -55 201 58 minecraft:dirt
fill -55 202 57 -55 202 58 minecraft:podzol
fill -49 201 57 -49 201 58 minecraft:dirt
fill -49 202 57 -49 202 58 minecraft:podzol
fill -45 201 52 -45 202 53 minecraft:andesite
fill -45 203 52 -45 203 53 minecraft:podzol
fill -44 201 53 -43 202 53 minecraft:andesite
fill -44 203 53 -43 203 53 minecraft:podzol
fill -44 201 46 -42 202 52 minecraft:dirt
fill -44 203 46 -42 203 52 minecraft:podzol
fill -54 201 57 -50 202 58 minecraft:dirt
fill -54 203 57 -50 203 58 minecraft:podzol
fill -45 201 46 -45 202 51 minecraft:stone
fill -45 203 46 -45 203 51 minecraft:podzol
fill -42 201 53 -42 202 53 minecraft:stone
fill -42 203 53 -42 203 53 minecraft:podzol
fill -59 201 44 -59 205 45 minecraft:andesite
fill -59 206 44 -59 206 45 minecraft:podzol
fill -59 201 41 -59 205 43 minecraft:stone
fill -59 206 41 -59 206 43 minecraft:podzol
setblock -44 201 44 minecraft:mossy_stone_brick_stairs[facing=south]
setblock -44 202 45 minecraft:mossy_stone_brick_stairs[facing=south]
setblock -43 201 44 minecraft:mossy_stone_brick_stairs[facing=south]
setblock -43 202 45 minecraft:mossy_stone_brick_stairs[facing=south]
setblock -42 201 44 minecraft:mossy_stone_brick_stairs[facing=south]
setblock -42 202 45 minecraft:mossy_stone_brick_stairs[facing=south]
execute positioned -54 204 57 run function rlk:room/prop/p_hay
execute positioned -44 204 52 run function rlk:room/prop/p_grass
execute positioned -46 201 57 run function rlk:room/prop/p_grass
execute positioned -44 201 42 run function rlk:room/prop/p_wildflower
execute positioned -47 201 53 run function rlk:room/prop/p_grass
execute positioned -43 204 52 run function rlk:room/prop/p_litter
execute positioned -44 204 50 run function rlk:room/prop/p_dandelion
execute positioned -45 201 58 run function rlk:room/prop/p_grass
setblock -59 207 42 minecraft:azalea_leaves[persistent=true] keep
