# 구역 건설 (normal16_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -60 59 200 -41 minecraft:podzol
fill 40 201 -60 59 210 -41 minecraft:stone
fill 41 201 -59 58 210 -42 minecraft:air
fill 41 209 -59 58 209 -42 minecraft:light[level=15]
fill 54 200 -45 57 200 -43 minecraft:moss_block
fill 44 200 -54 47 200 -51 minecraft:packed_mud
fill 50 200 -52 54 200 -51 minecraft:packed_mud
fill 40 201 -57 40 210 -57 minecraft:stripped_dark_oak_log
fill 40 205 -57 40 205 -56 minecraft:cobblestone
fill 40 210 -43 40 210 -43 minecraft:cherry_leaves[persistent=true]
fill 59 210 -58 59 210 -53 minecraft:cherry_leaves[persistent=true]
fill 59 210 -59 59 210 -57 minecraft:cherry_leaves[persistent=true]
fill 59 203 -52 59 206 -51 minecraft:tuff
fill 47 206 -60 50 206 -60 minecraft:andesite
fill 41 201 -60 41 210 -60 minecraft:stripped_dark_oak_log
fill 40 207 -60 45 210 -60 minecraft:andesite
fill 51 203 -60 53 203 -60 minecraft:moss_block
fill 41 201 -60 41 201 -60 minecraft:calcite
fill 55 210 -60 55 210 -60 minecraft:cherry_leaves[persistent=true]
fill 41 206 -41 41 209 -41 minecraft:calcite
fill 48 210 -41 48 210 -41 minecraft:cherry_leaves[persistent=true]
fill 47 210 -41 47 210 -41 minecraft:cherry_leaves[persistent=true]
fill 51 201 -59 51 201 -58 minecraft:podzol
fill 52 201 -58 52 201 -56 minecraft:podzol
fill 53 201 -56 54 201 -56 minecraft:podzol
fill 55 201 -55 55 201 -54 minecraft:podzol
fill 56 201 -54 56 201 -53 minecraft:podzol
fill 58 201 -54 58 201 -53 minecraft:podzol
fill 57 201 -53 57 201 -53 minecraft:podzol
fill 52 201 -59 53 201 -59 minecraft:dirt
fill 52 202 -59 53 202 -59 minecraft:podzol
fill 53 201 -58 53 201 -57 minecraft:dirt
fill 53 202 -58 53 202 -57 minecraft:podzol
fill 54 201 -57 54 201 -57 minecraft:dirt
fill 54 202 -57 54 202 -57 minecraft:podzol
fill 55 201 -56 55 201 -56 minecraft:dirt
fill 55 202 -56 55 202 -56 minecraft:podzol
fill 56 201 -55 58 201 -55 minecraft:dirt
fill 56 202 -55 58 202 -55 minecraft:podzol
fill 57 201 -54 57 201 -54 minecraft:dirt
fill 57 202 -54 57 202 -54 minecraft:podzol
fill 54 201 -59 58 202 -58 minecraft:dirt
fill 54 203 -59 58 203 -58 minecraft:podzol
fill 55 201 -57 58 202 -57 minecraft:dirt
fill 55 203 -57 58 203 -57 minecraft:podzol
fill 56 201 -56 58 202 -56 minecraft:dirt
fill 56 203 -56 58 203 -56 minecraft:podzol
fill 41 201 -52 41 207 -49 minecraft:mossy_stone_bricks
fill 41 208 -52 41 208 -49 minecraft:podzol
fill 41 201 -54 41 207 -53 minecraft:stone_bricks
fill 41 208 -54 41 208 -53 minecraft:podzol
execute positioned 56 202 -53 run function rlk:room/prop/i_lantern
execute positioned 45 201 -59 run function rlk:room/prop/i_rock
execute positioned 54 201 -51 run function rlk:room/prop/i_grass
execute positioned 50 201 -53 run function rlk:room/prop/i_petal
execute positioned 46 201 -44 run function rlk:room/prop/i_petal
execute positioned 53 201 -42 run function rlk:room/prop/i_petal
execute positioned 52 201 -45 run function rlk:room/prop/i_flower
execute positioned 56 201 -43 run function rlk:room/prop/i_petal
execute positioned 51 201 -51 run function rlk:room/prop/i_flower
execute positioned 43 201 -47 run function rlk:room/prop/i_grass
execute positioned 56 204 -57 run function rlk:room/prop/i_petal
execute positioned 52 201 -42 run function rlk:room/prop/i_flower
setblock 41 209 -50 minecraft:short_grass keep
setblock 41 209 -52 minecraft:short_grass keep
setblock 41 209 -51 minecraft:short_grass keep
setblock 41 209 -49 minecraft:cherry_leaves[persistent=true] keep
setblock 41 209 -54 minecraft:short_grass keep
setblock 41 209 -53 minecraft:short_grass keep
