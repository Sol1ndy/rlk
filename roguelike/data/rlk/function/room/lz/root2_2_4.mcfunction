# 구역 건설 (root2_2, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -8 200 -35 -5 200 -34 minecraft:coarse_dirt
fill -20 202 -30 -20 203 -28 minecraft:andesite
fill -20 201 -30 -20 202 -30 minecraft:tuff
fill -20 209 -23 -20 210 -22 minecraft:cherry_leaves[persistent=true]
fill -1 209 -32 -1 210 -30 minecraft:cherry_leaves[persistent=true]
fill -1 210 -26 -1 210 -23 minecraft:cherry_leaves[persistent=true]
fill -1 210 -29 -1 210 -28 minecraft:cherry_leaves[persistent=true]
fill -10 208 -40 -9 210 -40 minecraft:andesite
fill -19 209 -40 -19 210 -40 minecraft:cherry_leaves[persistent=true]
fill -9 203 -40 -7 204 -40 minecraft:tuff
fill -5 209 -40 -3 210 -40 minecraft:cobblestone
fill -9 207 -40 -4 210 -40 minecraft:tuff
fill -7 209 -21 -2 210 -21 minecraft:cherry_leaves[persistent=true]
fill -18 208 -21 -14 209 -21 minecraft:cobblestone
fill -16 201 -21 -13 203 -21 minecraft:andesite
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -15 201 -38 -14 201 -38 minecraft:podzol
fill -16 201 -37 -15 201 -37 minecraft:podzol
fill -19 201 -36 -16 201 -36 minecraft:podzol
fill -19 201 -35 -17 201 -35 minecraft:podzol
fill -19 201 -27 -18 201 -26 minecraft:podzol
fill -17 201 -26 -17 201 -22 minecraft:podzol
fill -19 201 -39 -17 201 -37 minecraft:dirt
fill -19 202 -39 -17 202 -37 minecraft:podzol
fill -16 201 -38 -16 201 -38 minecraft:dirt
fill -16 202 -38 -16 202 -38 minecraft:podzol
fill -19 201 -25 -18 201 -22 minecraft:dirt
fill -19 202 -25 -18 202 -22 minecraft:podzol
fill -16 201 -39 -11 207 -39 minecraft:stone_bricks
fill -16 208 -39 -11 208 -39 minecraft:podzol
execute positioned -11 201 -36 run function rlk:room/prop/i_sakura
execute positioned -9 201 -31 run function rlk:room/prop/i_grass
execute positioned -3 201 -23 run function rlk:room/prop/i_flower
execute positioned -12 201 -31 run function rlk:room/prop/i_petal
execute positioned -5 201 -33 run function rlk:room/prop/i_petal
execute positioned -19 202 -26 run function rlk:room/prop/i_grass
execute positioned -7 201 -34 run function rlk:room/prop/i_grass
execute positioned -10 201 -39 run function rlk:room/prop/i_grass
execute positioned -8 201 -32 run function rlk:room/prop/i_petal
setblock -16 209 -39 minecraft:cherry_leaves[persistent=true] keep
setblock -15 209 -39 minecraft:cherry_leaves[persistent=true] keep
setblock -13 209 -39 minecraft:short_grass keep
setblock -12 209 -39 minecraft:cherry_leaves[persistent=true] keep
