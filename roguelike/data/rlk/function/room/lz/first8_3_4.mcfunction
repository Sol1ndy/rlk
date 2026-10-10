# 구역 건설 (first8_3, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 215 -41 minecraft:stone
fill 21 201 -59 38 215 -42 minecraft:air
fill 21 214 -59 38 214 -42 minecraft:light[level=15]
fill 33 205 -47 37 205 -44 minecraft:packed_mud
fill 20 206 -57 20 207 -53 minecraft:moss_block
fill 20 214 -46 20 215 -44 minecraft:cherry_leaves[persistent=true]
fill 20 211 -53 20 211 -52 minecraft:tuff
fill 20 215 -47 20 215 -44 minecraft:moss_block
fill 39 214 -59 39 215 -57 minecraft:cherry_leaves[persistent=true]
fill 39 214 -41 39 214 -41 minecraft:cobblestone
fill 39 202 -54 39 205 -54 minecraft:calcite
fill 33 212 -60 34 215 -60 minecraft:calcite
fill 32 212 -60 36 213 -60 minecraft:tuff
fill 34 211 -60 39 213 -60 minecraft:moss_block
fill 25 214 -60 26 215 -60 minecraft:cherry_leaves[persistent=true]
fill 34 201 -60 34 215 -60 minecraft:stripped_dark_oak_log
fill 26 204 -60 27 205 -60 minecraft:moss_block
fill 25 213 -41 26 215 -41 minecraft:moss_block
fill 23 206 -41 28 209 -41 minecraft:andesite
fill 26 215 -41 30 215 -41 minecraft:cherry_leaves[persistent=true]
fill 27 211 -41 29 213 -41 minecraft:moss_block
fill 20 215 -60 39 215 -41 minecraft:polished_deepslate
fill 21 215 -59 38 215 -42 minecraft:air
fill 21 201 -59 25 204 -42 minecraft:dirt
fill 21 205 -59 25 205 -42 minecraft:podzol
fill 26 201 -56 26 204 -42 minecraft:dirt
fill 26 205 -56 26 205 -42 minecraft:podzol
fill 27 201 -54 34 204 -42 minecraft:dirt
fill 27 205 -54 34 205 -42 minecraft:podzol
fill 35 201 -53 37 204 -42 minecraft:dirt
fill 35 205 -53 37 205 -42 minecraft:podzol
fill 38 201 -51 38 204 -42 minecraft:dirt
fill 38 205 -51 38 205 -42 minecraft:podzol
fill 26 201 -59 27 205 -57 minecraft:dirt
fill 26 206 -59 27 206 -57 minecraft:podzol
fill 27 201 -56 27 205 -55 minecraft:dirt
fill 27 206 -56 27 206 -55 minecraft:podzol
fill 28 201 -55 34 205 -55 minecraft:dirt
fill 28 206 -55 34 206 -55 minecraft:podzol
fill 38 201 -55 38 205 -52 minecraft:dirt
fill 38 206 -55 38 206 -52 minecraft:podzol
fill 35 201 -54 37 205 -54 minecraft:dirt
fill 35 206 -54 37 206 -54 minecraft:podzol
fill 28 201 -59 28 206 -56 minecraft:dirt
fill 28 207 -59 28 207 -56 minecraft:podzol
fill 37 201 -59 38 206 -56 minecraft:dirt
fill 37 207 -59 38 207 -56 minecraft:podzol
fill 29 201 -56 34 206 -56 minecraft:dirt
fill 29 207 -56 34 207 -56 minecraft:podzol
fill 35 201 -55 37 206 -55 minecraft:dirt
fill 35 207 -55 37 207 -55 minecraft:podzol
fill 35 201 -59 36 207 -56 minecraft:dirt
fill 35 208 -59 36 208 -56 minecraft:podzol
fill 30 201 -59 32 212 -57 minecraft:mossy_stone_bricks
fill 30 213 -59 32 213 -57 minecraft:podzol
fill 29 201 -59 29 212 -57 minecraft:stone_bricks
fill 29 213 -59 29 213 -57 minecraft:podzol
fill 33 201 -59 34 212 -57 minecraft:stone_bricks
fill 33 213 -59 34 213 -57 minecraft:podzol
execute positioned 33 206 -45 run function rlk:room/prop/i_pillar
execute positioned 36 206 -45 run function rlk:room/prop/i_pillar
execute positioned 21 206 -54 run function rlk:room/prop/i_grass
execute positioned 35 206 -44 run function rlk:room/prop/i_petal
execute positioned 35 206 -50 run function rlk:room/prop/i_grass
execute positioned 30 206 -42 run function rlk:room/prop/i_petal
execute positioned 35 206 -51 run function rlk:room/prop/i_flower
execute positioned 29 206 -49 run function rlk:room/prop/i_petal
execute positioned 33 208 -56 run function rlk:room/prop/i_petal
setblock 29 214 -59 minecraft:cherry_leaves[persistent=true] keep
setblock 30 214 -58 minecraft:cherry_leaves[persistent=true] keep
setblock 30 214 -57 minecraft:cherry_leaves[persistent=true] keep
setblock 32 214 -58 minecraft:short_grass keep
setblock 33 214 -59 minecraft:short_grass keep
setblock 33 214 -57 minecraft:short_grass keep
setblock 34 214 -57 minecraft:cherry_leaves[persistent=true] keep
