# 구역 건설 (first8_3, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -60 39 200 -41 minecraft:podzol
fill 20 201 -60 39 210 -41 minecraft:stone
fill 21 201 -59 38 210 -42 minecraft:air
fill 21 209 -59 38 209 -42 minecraft:light[level=15]
fill 33 200 -47 37 200 -44 minecraft:packed_mud
fill 20 201 -57 20 202 -53 minecraft:moss_block
fill 20 209 -46 20 210 -44 minecraft:cherry_leaves[persistent=true]
fill 20 206 -53 20 206 -52 minecraft:tuff
fill 20 210 -47 20 210 -44 minecraft:moss_block
fill 39 209 -59 39 210 -57 minecraft:cherry_leaves[persistent=true]
fill 39 209 -41 39 209 -41 minecraft:cobblestone
fill 33 207 -60 34 210 -60 minecraft:calcite
fill 32 207 -60 36 208 -60 minecraft:tuff
fill 34 206 -60 39 208 -60 minecraft:moss_block
fill 25 209 -60 26 210 -60 minecraft:cherry_leaves[persistent=true]
fill 34 201 -60 34 210 -60 minecraft:stripped_dark_oak_log
fill 25 208 -41 26 210 -41 minecraft:moss_block
fill 23 201 -41 28 204 -41 minecraft:andesite
fill 26 210 -41 30 210 -41 minecraft:cherry_leaves[persistent=true]
fill 27 206 -41 29 208 -41 minecraft:moss_block
fill 20 210 -60 39 210 -41 minecraft:polished_deepslate
fill 21 210 -59 38 210 -42 minecraft:air
fill 26 201 -59 27 201 -57 minecraft:podzol
fill 27 201 -56 27 201 -55 minecraft:podzol
fill 28 201 -55 34 201 -55 minecraft:podzol
fill 38 201 -55 38 201 -52 minecraft:podzol
fill 35 201 -54 37 201 -54 minecraft:podzol
fill 28 201 -59 28 201 -56 minecraft:dirt
fill 28 202 -59 28 202 -56 minecraft:podzol
fill 37 201 -59 38 201 -56 minecraft:dirt
fill 37 202 -59 38 202 -56 minecraft:podzol
fill 29 201 -56 34 201 -56 minecraft:dirt
fill 29 202 -56 34 202 -56 minecraft:podzol
fill 35 201 -55 37 201 -55 minecraft:dirt
fill 35 202 -55 37 202 -55 minecraft:podzol
fill 35 201 -59 36 202 -56 minecraft:dirt
fill 35 203 -59 36 203 -56 minecraft:podzol
fill 30 201 -59 32 207 -57 minecraft:mossy_stone_bricks
fill 30 208 -59 32 208 -57 minecraft:podzol
fill 29 201 -59 29 207 -57 minecraft:stone_bricks
fill 29 208 -59 29 208 -57 minecraft:podzol
fill 33 201 -59 34 207 -57 minecraft:stone_bricks
fill 33 208 -59 34 208 -57 minecraft:podzol
execute positioned 33 201 -45 run function rlk:room/prop/i_pillar
execute positioned 36 201 -45 run function rlk:room/prop/i_pillar
execute positioned 21 201 -54 run function rlk:room/prop/i_grass
execute positioned 35 201 -44 run function rlk:room/prop/i_petal
execute positioned 35 201 -50 run function rlk:room/prop/i_grass
execute positioned 30 201 -42 run function rlk:room/prop/i_petal
execute positioned 35 201 -51 run function rlk:room/prop/i_flower
execute positioned 29 201 -49 run function rlk:room/prop/i_petal
execute positioned 33 203 -56 run function rlk:room/prop/i_petal
setblock 29 209 -59 minecraft:cherry_leaves[persistent=true] keep
setblock 30 209 -58 minecraft:cherry_leaves[persistent=true] keep
setblock 30 209 -57 minecraft:cherry_leaves[persistent=true] keep
setblock 32 209 -58 minecraft:short_grass keep
setblock 33 209 -59 minecraft:short_grass keep
setblock 33 209 -57 minecraft:short_grass keep
setblock 34 209 -57 minecraft:cherry_leaves[persistent=true] keep
