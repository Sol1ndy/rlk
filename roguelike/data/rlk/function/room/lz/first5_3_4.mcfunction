# 구역 건설 (first5_3, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 -20 19 200 -1 minecraft:podzol
fill 0 201 -20 19 210 -1 minecraft:stone
fill 1 201 -19 18 210 -2 minecraft:air
fill 1 209 -19 18 209 -2 minecraft:light[level=15]
fill 13 200 -17 16 200 -14 minecraft:gravel
fill 0 208 -6 0 209 -4 minecraft:moss_block
fill 0 201 -12 0 204 -10 minecraft:tuff
fill 0 210 -6 0 210 -4 minecraft:cherry_leaves[persistent=true]
fill 0 202 -8 0 202 -8 minecraft:tuff
fill 0 210 -14 0 210 -11 minecraft:cherry_leaves[persistent=true]
fill 19 209 -17 19 210 -14 minecraft:cherry_leaves[persistent=true]
fill 19 208 -5 19 210 -5 minecraft:calcite
fill 19 201 -19 19 203 -14 minecraft:cobblestone
fill 19 209 -10 19 210 -5 minecraft:cherry_leaves[persistent=true]
fill 19 206 -5 19 207 -3 minecraft:cobblestone
fill 19 209 -13 19 210 -11 minecraft:andesite
fill 3 209 -20 8 210 -20 minecraft:cherry_leaves[persistent=true]
fill 2 210 -20 2 210 -20 minecraft:cherry_leaves[persistent=true]
fill 18 206 -20 18 209 -20 minecraft:calcite
fill 1 209 -20 3 210 -20 minecraft:calcite
fill 14 208 -20 16 208 -20 minecraft:tuff
fill 0 206 -1 3 206 -1 minecraft:calcite
fill 12 201 -1 16 203 -1 minecraft:moss_block
fill 0 210 -1 3 210 -1 minecraft:andesite
fill 0 210 -20 19 210 -1 minecraft:polished_deepslate
fill 1 210 -19 18 210 -2 minecraft:air
fill 6 201 -19 6 201 -15 minecraft:podzol
fill 9 201 -19 10 201 -19 minecraft:podzol
fill 10 201 -18 10 201 -15 minecraft:podzol
fill 7 201 -15 9 201 -15 minecraft:podzol
fill 15 201 -9 17 201 -8 minecraft:podzol
fill 18 201 -8 18 201 -8 minecraft:podzol
fill 15 201 -7 15 201 -7 minecraft:podzol
fill 16 201 -6 16 201 -2 minecraft:podzol
fill 17 201 -2 18 201 -2 minecraft:podzol
fill 7 201 -19 8 201 -18 minecraft:dirt
fill 7 202 -19 8 202 -18 minecraft:podzol
fill 9 201 -18 9 201 -18 minecraft:dirt
fill 9 202 -18 9 202 -18 minecraft:podzol
fill 7 201 -17 7 201 -16 minecraft:dirt
fill 7 202 -17 7 202 -16 minecraft:podzol
fill 16 201 -7 18 201 -7 minecraft:dirt
fill 16 202 -7 18 202 -7 minecraft:podzol
fill 17 201 -6 18 201 -3 minecraft:dirt
fill 17 202 -6 18 202 -3 minecraft:podzol
fill 9 201 -17 9 207 -16 minecraft:mossy_stone_bricks
fill 9 208 -17 9 208 -16 minecraft:podzol
fill 17 201 -12 18 207 -11 minecraft:mossy_stone_bricks
fill 17 208 -12 18 208 -11 minecraft:podzol
fill 8 201 -17 8 207 -16 minecraft:stone_bricks
fill 8 208 -17 8 208 -16 minecraft:podzol
fill 17 201 -15 18 207 -13 minecraft:stone_bricks
fill 17 208 -15 18 208 -13 minecraft:podzol
fill 0 186 -20 4 199 -13 minecraft:stone
fill 1 186 -19 3 186 -14 minecraft:dirt
fill 1 187 -19 3 188 -14 minecraft:cherry_leaves[persistent=true]
fill 1 189 -19 3 201 -14 minecraft:air
execute positioned 4 201 -11 run function rlk:room/prop/i_sakura
execute positioned 1 201 -10 run function rlk:room/prop/i_torii_z
execute positioned 4 201 -8 run function rlk:room/prop/i_rock
execute positioned 13 201 -16 run function rlk:room/prop/i_lantern
execute positioned 4 201 -15 run function rlk:room/prop/i_pillar
execute positioned 9 201 -2 run function rlk:room/prop/i_grass
execute positioned 2 201 -12 run function rlk:room/prop/i_petal
execute positioned 11 201 -17 run function rlk:room/prop/i_petal
execute positioned 4 201 -7 run function rlk:room/prop/i_flower
execute positioned 10 201 -6 run function rlk:room/prop/i_petal
execute positioned 3 201 -16 run function rlk:room/prop/i_petal
execute positioned 4 201 -15 run function rlk:room/prop/i_petal
execute positioned 17 203 -7 run function rlk:room/prop/i_grass
setblock 8 209 -17 minecraft:cherry_leaves[persistent=true] keep
setblock 8 209 -16 minecraft:short_grass keep
setblock 9 209 -16 minecraft:cherry_leaves[persistent=true] keep
setblock 17 209 -15 minecraft:cherry_leaves[persistent=true] keep
setblock 17 209 -13 minecraft:cherry_leaves[persistent=true] keep
setblock 17 209 -12 minecraft:cherry_leaves[persistent=true] keep
setblock 17 209 -11 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 -14 minecraft:cherry_leaves[persistent=true] keep
setblock 18 209 -13 minecraft:short_grass keep
setblock 18 209 -12 minecraft:short_grass keep
setblock 18 209 -11 minecraft:cherry_leaves[persistent=true] keep
