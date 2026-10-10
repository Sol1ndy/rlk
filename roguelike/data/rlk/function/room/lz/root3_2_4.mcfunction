# 구역 건설 (root3_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 -20 39 200 -1 minecraft:podzol
fill 20 201 -20 39 210 -1 minecraft:stone
fill 21 201 -19 38 210 -2 minecraft:air
fill 21 209 -19 38 209 -2 minecraft:light[level=15]
fill 31 200 -9 34 200 -7 minecraft:gravel
fill 35 200 -18 38 200 -17 minecraft:moss_block
fill 20 210 -19 20 210 -16 minecraft:cherry_leaves[persistent=true]
fill 20 204 -5 20 207 -5 minecraft:andesite
fill 20 203 -16 20 204 -13 minecraft:andesite
fill 39 209 -16 39 210 -16 minecraft:cherry_leaves[persistent=true]
fill 39 209 -5 39 210 -1 minecraft:cherry_leaves[persistent=true]
fill 39 210 -18 39 210 -18 minecraft:cherry_leaves[persistent=true]
fill 39 210 -11 39 210 -10 minecraft:andesite
fill 29 210 -20 31 210 -20 minecraft:moss_block
fill 25 209 -20 29 210 -20 minecraft:cherry_leaves[persistent=true]
fill 37 201 -20 39 202 -20 minecraft:calcite
fill 30 205 -20 30 205 -20 minecraft:andesite
fill 32 203 -1 32 204 -1 minecraft:moss_block
fill 37 201 -1 37 202 -1 minecraft:andesite
fill 26 210 -1 30 210 -1 minecraft:cherry_leaves[persistent=true]
fill 26 202 -1 28 204 -1 minecraft:andesite
fill 20 210 -20 39 210 -1 minecraft:polished_deepslate
fill 21 210 -19 38 210 -2 minecraft:air
fill 38 201 -8 38 201 -3 minecraft:podzol
fill 35 201 -6 37 201 -6 minecraft:podzol
fill 31 201 -5 34 201 -5 minecraft:podzol
fill 37 201 -5 37 201 -3 minecraft:podzol
fill 30 201 -4 31 201 -4 minecraft:podzol
fill 31 201 -3 31 201 -2 minecraft:podzol
fill 32 201 -2 32 201 -2 minecraft:podzol
fill 35 201 -5 36 201 -3 minecraft:dirt
fill 35 202 -5 36 202 -3 minecraft:podzol
fill 32 201 -4 34 201 -3 minecraft:dirt
fill 32 202 -4 34 202 -3 minecraft:podzol
fill 33 201 -2 35 201 -2 minecraft:dirt
fill 33 202 -2 35 202 -2 minecraft:podzol
fill 36 201 -2 38 206 -2 minecraft:mossy_stone_bricks
fill 36 207 -2 38 207 -2 minecraft:podzol
fill 28 201 -17 29 207 -16 minecraft:mossy_stone_bricks
fill 28 208 -17 29 208 -16 minecraft:podzol
execute positioned 35 201 -19 run function rlk:room/prop/i_rock
execute positioned 26 201 -19 run function rlk:room/prop/i_lantern
execute positioned 23 201 -13 run function rlk:room/prop/i_petal
execute positioned 33 201 -15 run function rlk:room/prop/i_grass
execute positioned 26 201 -9 run function rlk:room/prop/i_flower
execute positioned 37 201 -17 run function rlk:room/prop/i_petal
execute positioned 32 201 -14 run function rlk:room/prop/i_grass
execute positioned 37 201 -11 run function rlk:room/prop/i_petal
execute positioned 31 201 -7 run function rlk:room/prop/i_petal
execute positioned 35 201 -13 run function rlk:room/prop/i_grass
setblock 28 209 -17 minecraft:cherry_leaves[persistent=true] keep
setblock 29 209 -16 minecraft:short_grass keep
setblock 36 208 -2 minecraft:short_grass keep
setblock 37 208 -2 minecraft:short_grass keep
setblock 38 208 -2 minecraft:cherry_leaves[persistent=true] keep
