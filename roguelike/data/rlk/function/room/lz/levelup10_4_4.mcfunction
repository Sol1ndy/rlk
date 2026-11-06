# 구역 건설 (levelup10_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -20 59 200 -1 minecraft:podzol
fill 40 201 -20 59 210 -1 minecraft:stone
fill 41 201 -19 58 210 -2 minecraft:air
fill 41 209 -19 58 209 -2 minecraft:light[level=15]
fill 40 209 -11 40 210 -7 minecraft:cherry_leaves[persistent=true]
fill 40 201 -17 40 210 -17 minecraft:stripped_dark_oak_log
fill 40 210 -20 40 210 -19 minecraft:cherry_leaves[persistent=true]
fill 59 201 -9 59 210 -9 minecraft:stripped_dark_oak_log
fill 59 201 -7 59 202 -4 minecraft:tuff
fill 59 209 -14 59 210 -9 minecraft:cherry_leaves[persistent=true]
fill 59 201 -8 59 210 -8 minecraft:stripped_dark_oak_log
fill 46 201 -20 48 202 -20 minecraft:moss_block
fill 40 208 -20 40 209 -20 minecraft:cobblestone
fill 56 210 -20 59 210 -20 minecraft:cherry_leaves[persistent=true]
fill 45 201 -1 45 210 -1 minecraft:stripped_dark_oak_log
fill 52 201 -1 52 210 -1 minecraft:stripped_dark_oak_log
fill 40 210 -20 59 210 -1 minecraft:polished_deepslate
fill 41 210 -19 58 210 -2 minecraft:air
fill 43 201 -15 43 201 -14 minecraft:podzol
fill 42 201 -14 42 201 -10 minecraft:podzol
fill 44 201 -14 45 201 -14 minecraft:podzol
fill 45 201 -13 45 201 -9 minecraft:podzol
fill 43 201 -11 44 201 -9 minecraft:podzol
fill 43 201 -12 44 206 -12 minecraft:mossy_stone_bricks
fill 43 207 -12 44 207 -12 minecraft:podzol
fill 43 201 -13 44 206 -13 minecraft:stone_bricks
fill 43 207 -13 44 207 -13 minecraft:podzol
execute positioned 55 201 -9 run function rlk:room/prop/i_shop_r3
execute positioned 41 201 -7 run function rlk:room/prop/i_lantern
execute positioned 49 201 -19 run function rlk:room/prop/i_flower
execute positioned 55 201 -18 run function rlk:room/prop/i_petal
execute positioned 56 201 -19 run function rlk:room/prop/i_flower
execute positioned 58 201 -2 run function rlk:room/prop/i_grass
execute positioned 52 201 -3 run function rlk:room/prop/i_petal
execute positioned 45 202 -12 run function rlk:room/prop/i_petal
execute positioned 41 201 -8 run function rlk:room/prop/i_petal
setblock 43 208 -13 minecraft:cherry_leaves[persistent=true] keep
setblock 43 208 -12 minecraft:short_grass keep
setblock 44 208 -12 minecraft:cherry_leaves[persistent=true] keep
