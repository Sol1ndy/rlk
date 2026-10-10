# 구역 건설 (levelup7_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 20 59 200 39 minecraft:podzol
fill 40 201 20 59 210 39 minecraft:stone
fill 41 201 21 58 210 38 minecraft:air
fill 41 209 21 58 209 38 minecraft:light[level=15]
fill 41 200 31 45 200 32 minecraft:gravel
fill 46 200 23 48 200 26 minecraft:packed_mud
fill 51 200 22 53 200 24 minecraft:gravel
fill 40 209 24 40 210 27 minecraft:cherry_leaves[persistent=true]
fill 40 209 21 40 210 23 minecraft:cherry_leaves[persistent=true]
fill 40 210 21 40 210 21 minecraft:calcite
fill 40 208 34 40 208 38 minecraft:calcite
fill 40 209 35 40 209 36 minecraft:andesite
fill 59 208 24 59 210 24 minecraft:moss_block
fill 59 208 23 59 208 24 minecraft:calcite
fill 59 207 22 59 209 22 minecraft:andesite
fill 42 210 20 47 210 20 minecraft:cherry_leaves[persistent=true]
fill 54 202 20 58 203 20 minecraft:calcite
fill 44 206 20 45 209 20 minecraft:tuff
fill 51 208 39 53 210 39 minecraft:calcite
fill 55 208 39 57 208 39 minecraft:tuff
fill 44 209 39 47 209 39 minecraft:andesite
fill 46 205 39 51 207 39 minecraft:calcite
fill 43 210 39 44 210 39 minecraft:cherry_leaves[persistent=true]
fill 48 208 39 48 208 39 minecraft:andesite
fill 56 201 30 58 201 38 minecraft:podzol
fill 55 201 31 55 201 38 minecraft:podzol
fill 41 201 33 43 201 38 minecraft:podzol
fill 44 201 34 44 201 38 minecraft:podzol
fill 53 201 35 54 201 37 minecraft:podzol
fill 54 201 38 54 201 38 minecraft:podzol
fill 46 201 37 50 205 38 minecraft:stone_bricks
fill 46 206 37 50 206 38 minecraft:podzol
execute positioned 43 201 25 run function rlk:room/prop/i_bamboo
execute positioned 55 202 33 run function rlk:room/prop/i_rock
execute positioned 54 201 33 run function rlk:room/prop/i_petal
execute positioned 43 201 24 run function rlk:room/prop/i_petal
execute positioned 51 201 25 run function rlk:room/prop/i_grass
execute positioned 57 202 36 run function rlk:room/prop/i_petal
execute positioned 49 201 22 run function rlk:room/prop/i_flower
execute positioned 55 201 25 run function rlk:room/prop/i_grass
execute positioned 52 201 34 run function rlk:room/prop/i_grass
setblock 49 207 38 minecraft:cherry_leaves[persistent=true] keep
setblock 50 207 38 minecraft:cherry_leaves[persistent=true] keep
setblock 46 207 38 minecraft:short_grass keep
setblock 49 207 37 minecraft:short_grass keep
setblock 48 207 38 minecraft:short_grass keep
setblock 47 207 37 minecraft:short_grass keep
