# 구역 건설 (levelup9_6, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 40 59 200 59 minecraft:podzol
fill 40 201 40 59 210 59 minecraft:stone
fill 41 201 41 58 210 58 minecraft:air
fill 41 209 41 58 209 58 minecraft:light[level=15]
fill 50 200 51 54 200 52 minecraft:packed_mud
fill 45 200 49 47 200 52 minecraft:packed_mud
fill 40 209 42 40 210 47 minecraft:cherry_leaves[persistent=true]
fill 40 206 40 40 208 43 minecraft:andesite
fill 40 201 56 40 203 56 minecraft:tuff
fill 40 202 48 40 205 53 minecraft:moss_block
fill 59 201 56 59 210 56 minecraft:stripped_dark_oak_log
fill 59 209 40 59 210 44 minecraft:cherry_leaves[persistent=true]
fill 59 210 49 59 210 52 minecraft:andesite
fill 50 207 40 53 208 40 minecraft:moss_block
fill 54 201 40 57 204 40 minecraft:calcite
fill 42 208 40 43 208 40 minecraft:andesite
fill 40 209 40 41 210 40 minecraft:cherry_leaves[persistent=true]
fill 53 209 40 56 210 40 minecraft:cherry_leaves[persistent=true]
fill 45 202 59 47 205 59 minecraft:andesite
fill 46 210 59 50 210 59 minecraft:cherry_leaves[persistent=true]
fill 45 209 59 48 210 59 minecraft:cherry_leaves[persistent=true]
fill 46 209 59 50 210 59 minecraft:cherry_leaves[persistent=true]
fill 51 209 59 54 210 59 minecraft:calcite
fill 55 201 50 57 201 50 minecraft:podzol
fill 55 201 51 55 201 54 minecraft:podzol
fill 57 201 51 58 201 51 minecraft:podzol
fill 58 201 52 58 201 52 minecraft:podzol
fill 41 201 55 43 201 55 minecraft:podzol
fill 48 201 55 54 201 55 minecraft:podzol
fill 48 201 56 49 201 56 minecraft:podzol
fill 47 201 57 48 201 58 minecraft:podzol
fill 58 201 58 58 201 58 minecraft:podzol
fill 56 201 51 56 201 54 minecraft:dirt
fill 56 202 51 56 202 54 minecraft:podzol
fill 57 201 52 57 201 52 minecraft:dirt
fill 57 202 52 57 202 52 minecraft:podzol
fill 41 201 54 42 201 54 minecraft:dirt
fill 41 202 54 42 202 54 minecraft:podzol
fill 55 201 55 55 201 55 minecraft:dirt
fill 55 202 55 55 202 55 minecraft:podzol
fill 50 201 56 54 201 56 minecraft:dirt
fill 50 202 56 54 202 56 minecraft:podzol
fill 58 201 56 58 201 57 minecraft:dirt
fill 58 202 56 58 202 57 minecraft:podzol
fill 49 201 57 51 201 58 minecraft:dirt
fill 49 202 57 51 202 58 minecraft:podzol
fill 57 201 57 57 201 58 minecraft:dirt
fill 57 202 57 57 202 58 minecraft:podzol
fill 52 201 58 52 201 58 minecraft:dirt
fill 52 202 58 52 202 58 minecraft:podzol
fill 56 201 58 56 201 58 minecraft:dirt
fill 56 202 58 56 202 58 minecraft:podzol
fill 43 201 54 43 201 54 minecraft:stone_bricks
fill 43 202 54 43 202 54 minecraft:podzol
fill 41 201 47 43 202 53 minecraft:dirt
fill 41 203 47 43 203 53 minecraft:podzol
fill 56 201 55 56 202 57 minecraft:dirt
fill 56 203 55 56 203 57 minecraft:podzol
fill 55 201 56 55 202 58 minecraft:dirt
fill 55 203 56 55 203 58 minecraft:podzol
fill 57 201 56 57 202 56 minecraft:dirt
fill 57 203 56 57 203 56 minecraft:podzol
fill 52 201 57 54 202 57 minecraft:dirt
fill 52 203 57 54 203 57 minecraft:podzol
fill 53 201 58 54 202 58 minecraft:dirt
fill 53 203 58 54 203 58 minecraft:podzol
fill 44 201 48 44 202 51 minecraft:mossy_stone_bricks
fill 44 203 48 44 203 51 minecraft:podzol
fill 41 201 46 44 202 46 minecraft:stone_bricks
fill 41 203 46 44 203 46 minecraft:podzol
fill 44 201 47 44 202 47 minecraft:stone_bricks
fill 44 203 47 44 203 47 minecraft:podzol
fill 44 201 52 44 202 53 minecraft:stone_bricks
fill 44 203 52 44 203 53 minecraft:podzol
fill 57 201 54 58 207 55 minecraft:mossy_stone_bricks
fill 57 208 54 58 208 55 minecraft:podzol
fill 57 201 53 58 207 53 minecraft:stone_bricks
fill 57 208 53 58 208 53 minecraft:podzol
setblock 41 202 54 minecraft:stone_brick_stairs[facing=north]
setblock 41 201 55 minecraft:stone_brick_stairs[facing=north]
setblock 42 202 54 minecraft:stone_brick_stairs[facing=north]
setblock 42 201 55 minecraft:stone_brick_stairs[facing=north]
setblock 43 202 54 minecraft:stone_brick_stairs[facing=north]
setblock 43 201 55 minecraft:stone_brick_stairs[facing=north]
execute positioned 57 203 57 run function rlk:room/prop/i_petal
execute positioned 43 203 54 run function rlk:room/prop/i_petal
execute positioned 58 201 45 run function rlk:room/prop/i_petal
execute positioned 53 201 42 run function rlk:room/prop/i_petal
execute positioned 45 201 57 run function rlk:room/prop/i_grass
execute positioned 50 201 49 run function rlk:room/prop/i_petal
execute positioned 57 203 57 run function rlk:room/prop/i_grass
execute positioned 50 201 52 run function rlk:room/prop/i_petal
execute positioned 54 201 41 run function rlk:room/prop/i_petal
setblock 57 209 53 minecraft:cherry_leaves[persistent=true] keep
setblock 57 209 54 minecraft:cherry_leaves[persistent=true] keep
setblock 58 209 54 minecraft:short_grass keep
setblock 57 209 55 minecraft:cherry_leaves[persistent=true] keep
setblock 58 209 53 minecraft:short_grass keep
setblock 58 209 55 minecraft:short_grass keep
