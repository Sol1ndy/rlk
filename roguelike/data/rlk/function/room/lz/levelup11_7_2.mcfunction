# 구역 건설 (levelup11_7, 테마 2): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 40 -41 200 59 minecraft:podzol
fill -60 201 40 -41 210 59 minecraft:mossy_cobblestone
fill -59 201 41 -42 210 58 minecraft:air
fill -59 209 41 -42 209 58 minecraft:light[level=15]
fill -46 200 56 -44 200 57 minecraft:moss_block
fill -50 200 44 -46 200 45 minecraft:rooted_dirt
fill -51 200 46 -49 200 48 minecraft:rooted_dirt
fill -60 210 40 -60 210 43 minecraft:mossy_stone_bricks
fill -60 207 40 -60 209 45 minecraft:moss_block
fill -60 209 56 -60 210 56 minecraft:oak_leaves[persistent=true]
fill -60 207 55 -60 208 56 minecraft:mossy_stone_bricks
fill -41 209 44 -41 210 48 minecraft:oak_leaves[persistent=true]
fill -41 203 56 -41 206 57 minecraft:moss_block
fill -41 207 57 -41 210 59 minecraft:moss_block
fill -41 210 52 -41 210 54 minecraft:moss_block
fill -41 205 41 -41 205 43 minecraft:stone
fill -60 209 40 -55 210 40 minecraft:oak_leaves[persistent=true]
fill -49 201 40 -49 210 40 minecraft:oak_log
fill -45 209 40 -43 210 40 minecraft:stone
fill -58 201 59 -58 210 59 minecraft:oak_log
fill -52 201 59 -52 210 59 minecraft:oak_log
fill -50 205 59 -50 207 59 minecraft:stone
fill -51 201 59 -51 210 59 minecraft:oak_log
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
fill -44 201 45 -44 201 45 minecraft:mossy_cobblestone
fill -44 202 45 -44 202 45 minecraft:podzol
fill -44 201 46 -42 202 52 minecraft:dirt
fill -44 203 46 -42 203 52 minecraft:podzol
fill -54 201 57 -50 202 58 minecraft:dirt
fill -54 203 57 -50 203 58 minecraft:podzol
fill -45 201 52 -45 202 53 minecraft:mossy_cobblestone
fill -45 203 52 -45 203 53 minecraft:podzol
fill -44 201 53 -43 202 53 minecraft:mossy_cobblestone
fill -44 203 53 -43 203 53 minecraft:podzol
fill -45 201 46 -45 202 51 minecraft:stone
fill -45 203 46 -45 203 51 minecraft:podzol
fill -42 201 53 -42 202 53 minecraft:stone
fill -42 203 53 -42 203 53 minecraft:podzol
fill -59 201 44 -59 205 45 minecraft:mossy_cobblestone
fill -59 206 44 -59 206 45 minecraft:podzol
fill -59 201 41 -59 205 43 minecraft:stone
fill -59 206 41 -59 206 43 minecraft:podzol
setblock -44 201 44 minecraft:mossy_cobblestone_stairs[facing=south]
setblock -44 202 45 minecraft:mossy_cobblestone_stairs[facing=south]
setblock -43 201 44 minecraft:mossy_cobblestone_stairs[facing=south]
setblock -43 202 45 minecraft:mossy_cobblestone_stairs[facing=south]
setblock -42 201 44 minecraft:mossy_cobblestone_stairs[facing=south]
setblock -42 202 45 minecraft:mossy_cobblestone_stairs[facing=south]
execute positioned -47 201 42 run function rlk:room/prop/f_grass
execute positioned -57 201 42 run function rlk:room/prop/f_flower
execute positioned -42 201 54 run function rlk:room/prop/f_grass
execute positioned -51 201 41 run function rlk:room/prop/f_grass
