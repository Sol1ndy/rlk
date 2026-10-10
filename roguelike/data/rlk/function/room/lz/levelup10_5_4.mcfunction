# 구역 건설 (levelup10_5, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 0 59 200 19 minecraft:podzol
fill 40 201 0 59 213 19 minecraft:stone
fill 41 201 1 58 213 18 minecraft:air
fill 41 212 1 58 212 18 minecraft:light[level=15]
fill 43 203 5 45 203 8 minecraft:moss_block
fill 46 203 10 47 203 12 minecraft:coarse_dirt
fill 40 202 10 40 205 10 minecraft:tuff
fill 40 212 14 40 213 14 minecraft:cherry_leaves[persistent=true]
fill 40 212 18 40 213 19 minecraft:tuff
fill 40 201 16 40 213 16 minecraft:stripped_dark_oak_log
fill 40 211 13 40 213 13 minecraft:andesite
fill 59 205 1 59 207 4 minecraft:tuff
fill 59 211 9 59 212 14 minecraft:calcite
fill 59 213 5 59 213 9 minecraft:cherry_leaves[persistent=true]
fill 59 212 16 59 213 18 minecraft:andesite
fill 59 213 11 59 213 13 minecraft:moss_block
fill 59 206 8 59 206 12 minecraft:calcite
fill 47 212 0 47 213 0 minecraft:cherry_leaves[persistent=true]
fill 55 212 0 59 213 0 minecraft:moss_block
fill 52 201 0 52 213 0 minecraft:stripped_dark_oak_log
fill 46 209 0 49 211 0 minecraft:andesite
fill 53 206 19 56 207 19 minecraft:andesite
fill 45 210 19 49 213 19 minecraft:moss_block
fill 43 212 19 46 213 19 minecraft:cherry_leaves[persistent=true]
fill 44 213 19 45 213 19 minecraft:cherry_leaves[persistent=true]
fill 46 201 19 46 213 19 minecraft:stripped_dark_oak_log
fill 40 213 0 59 213 19 minecraft:polished_deepslate
fill 41 213 1 58 213 18 minecraft:air
fill 41 201 1 45 202 8 minecraft:dirt
fill 41 203 1 45 203 8 minecraft:podzol
fill 46 201 4 46 202 18 minecraft:dirt
fill 46 203 4 46 203 18 minecraft:podzol
fill 47 201 5 58 202 14 minecraft:dirt
fill 47 203 5 58 203 14 minecraft:podzol
fill 43 201 9 45 202 10 minecraft:dirt
fill 43 203 9 45 203 10 minecraft:podzol
fill 44 201 11 45 202 11 minecraft:dirt
fill 44 203 11 45 203 11 minecraft:podzol
fill 45 201 14 45 202 18 minecraft:dirt
fill 45 203 14 45 203 18 minecraft:podzol
fill 47 201 15 47 202 15 minecraft:dirt
fill 47 203 15 47 203 15 minecraft:podzol
fill 46 201 1 46 203 3 minecraft:dirt
fill 46 204 1 46 204 3 minecraft:podzol
fill 47 201 3 58 203 4 minecraft:dirt
fill 47 204 3 58 204 4 minecraft:podzol
fill 43 201 11 43 203 18 minecraft:dirt
fill 43 204 11 43 204 18 minecraft:podzol
fill 44 201 12 45 203 13 minecraft:dirt
fill 44 204 12 45 204 13 minecraft:podzol
fill 44 201 14 44 203 18 minecraft:dirt
fill 44 204 14 44 204 18 minecraft:podzol
fill 41 201 15 42 203 18 minecraft:dirt
fill 41 204 15 42 204 18 minecraft:podzol
fill 48 201 15 58 203 16 minecraft:dirt
fill 48 204 15 58 204 16 minecraft:podzol
fill 47 201 16 47 203 18 minecraft:dirt
fill 47 204 16 47 204 18 minecraft:podzol
fill 47 201 1 58 204 2 minecraft:dirt
fill 47 205 1 58 205 2 minecraft:podzol
fill 48 201 17 58 204 18 minecraft:dirt
fill 48 205 17 58 205 18 minecraft:podzol
fill 42 201 10 42 210 13 minecraft:mossy_stone_bricks
fill 42 211 10 42 211 13 minecraft:podzol
fill 41 201 9 42 210 9 minecraft:stone_bricks
fill 41 211 9 42 211 9 minecraft:podzol
fill 41 201 10 41 210 14 minecraft:stone_bricks
fill 41 211 10 41 211 14 minecraft:podzol
fill 42 201 14 42 210 14 minecraft:stone_bricks
fill 42 211 14 42 211 14 minecraft:podzol
execute positioned 45 204 6 run function rlk:room/prop/i_house_c_r2
execute positioned 55 204 11 run function rlk:room/prop/i_lantern
execute positioned 41 204 5 run function rlk:room/prop/i_petal
execute positioned 57 206 1 run function rlk:room/prop/i_petal
execute positioned 57 204 8 run function rlk:room/prop/i_petal
execute positioned 48 205 3 run function rlk:room/prop/i_petal
execute positioned 50 204 9 run function rlk:room/prop/i_petal
execute positioned 55 205 3 run function rlk:room/prop/i_petal
execute positioned 50 205 15 run function rlk:room/prop/i_grass
execute positioned 54 204 13 run function rlk:room/prop/i_petal
setblock 41 212 9 minecraft:cherry_leaves[persistent=true] keep
setblock 41 212 10 minecraft:cherry_leaves[persistent=true] keep
setblock 41 212 11 minecraft:cherry_leaves[persistent=true] keep
setblock 41 212 12 minecraft:short_grass keep
setblock 41 212 13 minecraft:cherry_leaves[persistent=true] keep
setblock 42 212 11 minecraft:short_grass keep
setblock 42 212 13 minecraft:cherry_leaves[persistent=true] keep
