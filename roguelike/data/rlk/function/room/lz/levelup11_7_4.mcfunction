# 구역 건설 (levelup11_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 40 -41 200 59 minecraft:podzol
fill -60 201 40 -41 210 59 minecraft:stone
fill -59 201 41 -42 210 58 minecraft:air
fill -59 209 41 -42 209 58 minecraft:light[level=15]
fill -43 200 42 -42 200 43 minecraft:coarse_dirt
fill -60 208 41 -60 208 42 minecraft:tuff
fill -60 209 40 -60 210 42 minecraft:cherry_leaves[persistent=true]
fill -60 202 57 -60 205 57 minecraft:calcite
fill -60 209 55 -60 210 57 minecraft:cobblestone
fill -60 210 47 -60 210 49 minecraft:andesite
fill -41 209 49 -41 210 49 minecraft:cherry_leaves[persistent=true]
fill -41 201 52 -41 210 52 minecraft:stripped_dark_oak_log
fill -41 209 48 -41 210 53 minecraft:cherry_leaves[persistent=true]
fill -41 210 58 -41 210 59 minecraft:cherry_leaves[persistent=true]
fill -41 210 53 -41 210 55 minecraft:cherry_leaves[persistent=true]
fill -60 209 40 -56 210 40 minecraft:cherry_leaves[persistent=true]
fill -54 201 40 -54 210 40 minecraft:stripped_dark_oak_log
fill -60 209 40 -57 210 40 minecraft:cherry_leaves[persistent=true]
fill -49 203 40 -46 203 40 minecraft:moss_block
fill -51 206 40 -51 206 40 minecraft:calcite
fill -46 204 40 -46 205 40 minecraft:cobblestone
fill -51 207 59 -49 209 59 minecraft:tuff
fill -54 203 59 -53 205 59 minecraft:moss_block
fill -49 206 59 -49 209 59 minecraft:moss_block
fill -44 202 59 -44 203 59 minecraft:tuff
fill -58 209 59 -54 210 59 minecraft:cherry_leaves[persistent=true]
fill -44 201 44 -42 201 44 minecraft:podzol
fill -59 201 47 -56 201 57 minecraft:podzol
fill -55 201 55 -49 201 55 minecraft:podzol
fill -55 201 56 -55 201 56 minecraft:podzol
fill -49 201 56 -49 201 56 minecraft:podzol
fill -48 201 57 -48 201 58 minecraft:podzol
fill -56 201 58 -56 201 58 minecraft:podzol
fill -43 201 45 -42 201 45 minecraft:dirt
fill -43 202 45 -42 202 45 minecraft:podzol
fill -54 201 56 -50 201 56 minecraft:dirt
fill -54 202 56 -50 202 56 minecraft:podzol
fill -55 201 57 -55 201 58 minecraft:dirt
fill -55 202 57 -55 202 58 minecraft:podzol
fill -49 201 57 -49 201 58 minecraft:dirt
fill -49 202 57 -49 202 58 minecraft:podzol
fill -44 201 45 -44 201 45 minecraft:mossy_stone_bricks
fill -44 202 45 -44 202 45 minecraft:podzol
fill -44 201 46 -42 202 52 minecraft:dirt
fill -44 203 46 -42 203 52 minecraft:podzol
fill -54 201 57 -50 202 58 minecraft:dirt
fill -54 203 57 -50 203 58 minecraft:podzol
fill -45 201 52 -45 202 53 minecraft:mossy_stone_bricks
fill -45 203 52 -45 203 53 minecraft:podzol
fill -44 201 53 -43 202 53 minecraft:mossy_stone_bricks
fill -44 203 53 -43 203 53 minecraft:podzol
fill -45 201 46 -45 202 51 minecraft:stone_bricks
fill -45 203 46 -45 203 51 minecraft:podzol
fill -42 201 53 -42 202 53 minecraft:stone_bricks
fill -42 203 53 -42 203 53 minecraft:podzol
fill -59 201 44 -59 205 45 minecraft:mossy_stone_bricks
fill -59 206 44 -59 206 45 minecraft:podzol
fill -59 201 41 -59 205 43 minecraft:stone_bricks
fill -59 206 41 -59 206 43 minecraft:podzol
setblock -44 201 44 minecraft:stone_brick_stairs[facing=south]
setblock -44 202 45 minecraft:stone_brick_stairs[facing=south]
setblock -43 201 44 minecraft:stone_brick_stairs[facing=south]
setblock -43 202 45 minecraft:stone_brick_stairs[facing=south]
setblock -42 201 44 minecraft:stone_brick_stairs[facing=south]
setblock -42 202 45 minecraft:stone_brick_stairs[facing=south]
execute positioned -56 202 48 run function rlk:room/prop/i_shop_r1
execute positioned -48 202 58 run function rlk:room/prop/i_lantern
execute positioned -44 201 58 run function rlk:room/prop/i_lantern
execute positioned -56 202 56 run function rlk:room/prop/i_pillar
execute positioned -55 201 52 run function rlk:room/prop/i_grass
execute positioned -55 201 51 run function rlk:room/prop/i_grass
execute positioned -58 201 41 run function rlk:room/prop/i_petal
execute positioned -56 201 44 run function rlk:room/prop/i_petal
execute positioned -49 201 43 run function rlk:room/prop/i_petal
execute positioned -57 202 50 run function rlk:room/prop/i_flower
execute positioned -54 202 55 run function rlk:room/prop/i_petal
execute positioned -50 201 46 run function rlk:room/prop/i_grass
setblock -59 207 41 minecraft:short_grass keep
