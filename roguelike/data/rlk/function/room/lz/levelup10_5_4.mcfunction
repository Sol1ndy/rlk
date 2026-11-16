# 구역 건설 (levelup10_5, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 0 59 200 19 minecraft:podzol
fill 40 201 0 59 210 19 minecraft:stone
fill 41 201 1 58 210 18 minecraft:air
fill 41 209 1 58 209 18 minecraft:light[level=15]
fill 43 200 5 45 200 8 minecraft:moss_block
fill 46 200 10 47 200 12 minecraft:coarse_dirt
fill 40 201 10 40 202 10 minecraft:tuff
fill 40 209 14 40 210 14 minecraft:cherry_leaves[persistent=true]
fill 40 209 18 40 210 19 minecraft:tuff
fill 40 201 16 40 210 16 minecraft:stripped_dark_oak_log
fill 40 208 13 40 210 13 minecraft:andesite
fill 59 202 1 59 204 4 minecraft:tuff
fill 59 208 9 59 209 14 minecraft:calcite
fill 59 210 5 59 210 9 minecraft:cherry_leaves[persistent=true]
fill 59 209 16 59 210 18 minecraft:andesite
fill 59 210 11 59 210 13 minecraft:moss_block
fill 59 203 8 59 203 12 minecraft:calcite
fill 47 209 0 47 210 0 minecraft:cherry_leaves[persistent=true]
fill 55 209 0 59 210 0 minecraft:moss_block
fill 52 201 0 52 210 0 minecraft:stripped_dark_oak_log
fill 46 206 0 49 208 0 minecraft:andesite
fill 53 203 19 56 204 19 minecraft:andesite
fill 45 207 19 49 210 19 minecraft:moss_block
fill 43 209 19 46 210 19 minecraft:cherry_leaves[persistent=true]
fill 44 210 19 45 210 19 minecraft:cherry_leaves[persistent=true]
fill 46 201 19 46 210 19 minecraft:stripped_dark_oak_log
fill 40 210 0 59 210 19 minecraft:polished_deepslate
fill 41 210 1 58 210 18 minecraft:air
fill 43 201 11 43 201 18 minecraft:podzol
fill 44 201 12 45 201 13 minecraft:podzol
fill 44 201 14 44 201 18 minecraft:podzol
fill 41 201 15 42 201 18 minecraft:podzol
fill 42 201 10 42 207 13 minecraft:mossy_stone_bricks
fill 42 208 10 42 208 13 minecraft:podzol
fill 41 201 9 42 207 9 minecraft:stone_bricks
fill 41 208 9 42 208 9 minecraft:podzol
fill 41 201 10 41 207 14 minecraft:stone_bricks
fill 41 208 10 41 208 14 minecraft:podzol
fill 42 201 14 42 207 14 minecraft:stone_bricks
fill 42 208 14 42 208 14 minecraft:podzol
execute positioned 45 201 6 run function rlk:room/prop/i_house_c_r2
execute positioned 55 201 11 run function rlk:room/prop/i_lantern
execute positioned 41 201 5 run function rlk:room/prop/i_petal
execute positioned 57 201 1 run function rlk:room/prop/i_petal
execute positioned 57 201 8 run function rlk:room/prop/i_petal
execute positioned 48 201 3 run function rlk:room/prop/i_petal
execute positioned 50 201 9 run function rlk:room/prop/i_petal
execute positioned 55 201 3 run function rlk:room/prop/i_petal
execute positioned 50 201 15 run function rlk:room/prop/i_grass
execute positioned 54 201 13 run function rlk:room/prop/i_petal
setblock 41 209 9 minecraft:cherry_leaves[persistent=true] keep
setblock 41 209 10 minecraft:cherry_leaves[persistent=true] keep
setblock 41 209 11 minecraft:cherry_leaves[persistent=true] keep
setblock 41 209 12 minecraft:short_grass keep
setblock 41 209 13 minecraft:cherry_leaves[persistent=true] keep
setblock 42 209 11 minecraft:short_grass keep
setblock 42 209 13 minecraft:cherry_leaves[persistent=true] keep
