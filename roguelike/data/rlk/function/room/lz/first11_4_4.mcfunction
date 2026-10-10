# 구역 건설 (first11_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -60 59 200 -41 minecraft:podzol
fill 40 201 -60 59 215 -41 minecraft:stone
fill 41 201 -59 58 215 -42 minecraft:air
fill 41 214 -59 58 214 -42 minecraft:light[level=15]
fill 41 205 -48 43 205 -47 minecraft:moss_block
fill 42 205 -54 46 205 -52 minecraft:moss_block
fill 40 209 -48 40 211 -48 minecraft:tuff
fill 40 205 -51 40 207 -50 minecraft:andesite
fill 40 201 -56 40 215 -56 minecraft:stripped_dark_oak_log
fill 40 210 -50 40 212 -49 minecraft:cobblestone
fill 40 214 -58 40 215 -54 minecraft:cobblestone
fill 59 202 -57 59 205 -57 minecraft:cobblestone
fill 59 215 -56 59 215 -56 minecraft:andesite
fill 59 215 -59 59 215 -56 minecraft:cherry_leaves[persistent=true]
fill 59 210 -57 59 213 -54 minecraft:moss_block
fill 54 214 -60 57 215 -60 minecraft:calcite
fill 45 210 -60 50 210 -60 minecraft:tuff
fill 57 205 -60 59 206 -60 minecraft:moss_block
fill 44 214 -60 44 214 -60 minecraft:moss_block
fill 52 209 -60 54 212 -60 minecraft:moss_block
fill 40 215 -41 44 215 -41 minecraft:andesite
fill 43 201 -41 43 215 -41 minecraft:stripped_dark_oak_log
fill 53 214 -41 54 215 -41 minecraft:andesite
fill 40 215 -60 59 215 -41 minecraft:polished_deepslate
fill 41 215 -59 58 215 -42 minecraft:air
fill 41 201 -59 41 204 -42 minecraft:dirt
fill 41 205 -59 41 205 -42 minecraft:podzol
fill 54 201 -59 58 204 -45 minecraft:dirt
fill 54 205 -59 58 205 -45 minecraft:podzol
fill 42 201 -56 45 204 -42 minecraft:dirt
fill 42 205 -56 45 205 -42 minecraft:podzol
fill 53 201 -56 53 204 -46 minecraft:dirt
fill 53 205 -56 53 205 -46 minecraft:podzol
fill 46 201 -54 52 204 -46 minecraft:dirt
fill 46 205 -54 52 205 -46 minecraft:podzol
fill 46 201 -45 48 204 -45 minecraft:dirt
fill 46 205 -45 48 205 -45 minecraft:podzol
fill 46 201 -44 47 204 -42 minecraft:dirt
fill 46 205 -44 47 205 -42 minecraft:podzol
fill 55 201 -44 58 204 -42 minecraft:dirt
fill 55 205 -44 58 205 -42 minecraft:podzol
fill 42 201 -59 43 205 -57 minecraft:dirt
fill 42 206 -59 43 206 -57 minecraft:podzol
fill 44 201 -57 45 205 -57 minecraft:dirt
fill 44 206 -57 45 206 -57 minecraft:podzol
fill 46 201 -56 46 205 -55 minecraft:dirt
fill 46 206 -56 46 206 -55 minecraft:podzol
fill 51 201 -56 52 205 -55 minecraft:dirt
fill 51 206 -56 52 206 -55 minecraft:podzol
fill 47 201 -55 50 205 -55 minecraft:dirt
fill 47 206 -55 50 206 -55 minecraft:podzol
fill 49 201 -45 53 205 -42 minecraft:dirt
fill 49 206 -45 53 206 -42 minecraft:podzol
fill 48 201 -44 48 205 -42 minecraft:dirt
fill 48 206 -44 48 206 -42 minecraft:podzol
fill 54 201 -44 54 205 -42 minecraft:dirt
fill 54 206 -44 54 206 -42 minecraft:podzol
fill 44 201 -59 48 206 -58 minecraft:dirt
fill 44 207 -59 48 207 -58 minecraft:podzol
fill 46 201 -57 46 206 -57 minecraft:dirt
fill 46 207 -57 46 207 -57 minecraft:podzol
fill 49 201 -56 50 206 -56 minecraft:dirt
fill 49 207 -56 50 207 -56 minecraft:podzol
fill 49 201 -59 50 212 -57 minecraft:mossy_stone_bricks
fill 49 213 -59 50 213 -57 minecraft:podzol
fill 51 201 -58 53 212 -57 minecraft:mossy_stone_bricks
fill 51 213 -58 53 213 -57 minecraft:podzol
fill 48 201 -57 48 212 -56 minecraft:mossy_stone_bricks
fill 48 213 -57 48 213 -56 minecraft:podzol
fill 51 201 -59 53 212 -59 minecraft:stone_bricks
fill 51 213 -59 53 213 -59 minecraft:podzol
fill 47 201 -57 47 212 -56 minecraft:stone_bricks
fill 47 213 -57 47 213 -56 minecraft:podzol
execute positioned 56 206 -56 run function rlk:room/prop/i_lantern
execute positioned 50 206 -54 run function rlk:room/prop/i_petal
execute positioned 46 206 -46 run function rlk:room/prop/i_petal
execute positioned 43 206 -47 run function rlk:room/prop/i_flower
execute positioned 43 206 -42 run function rlk:room/prop/i_flower
execute positioned 56 206 -49 run function rlk:room/prop/i_petal
execute positioned 41 206 -59 run function rlk:room/prop/i_grass
execute positioned 50 207 -55 run function rlk:room/prop/i_flower
execute positioned 53 206 -49 run function rlk:room/prop/i_petal
execute positioned 41 206 -52 run function rlk:room/prop/i_flower
setblock 47 214 -57 minecraft:short_grass keep
setblock 47 214 -56 minecraft:cherry_leaves[persistent=true] keep
setblock 49 214 -59 minecraft:cherry_leaves[persistent=true] keep
setblock 51 214 -59 minecraft:cherry_leaves[persistent=true] keep
setblock 51 214 -58 minecraft:cherry_leaves[persistent=true] keep
setblock 51 214 -57 minecraft:short_grass keep
setblock 52 214 -58 minecraft:cherry_leaves[persistent=true] keep
setblock 53 214 -58 minecraft:cherry_leaves[persistent=true] keep
setblock 53 214 -57 minecraft:cherry_leaves[persistent=true] keep
