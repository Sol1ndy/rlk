# 구역 건설 (normal24_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -58 200 -25 -56 200 -23 minecraft:coarse_dirt
fill -60 208 -27 -60 210 -22 minecraft:calcite
fill -60 209 -31 -60 210 -30 minecraft:calcite
fill -60 209 -33 -60 210 -31 minecraft:cherry_leaves[persistent=true]
fill -41 209 -35 -41 210 -33 minecraft:cherry_leaves[persistent=true]
fill -41 205 -37 -41 207 -32 minecraft:andesite
fill -60 208 -40 -56 210 -40 minecraft:tuff
fill -60 208 -40 -58 209 -40 minecraft:tuff
fill -58 205 -21 -54 206 -21 minecraft:calcite
fill -57 210 -21 -53 210 -21 minecraft:cherry_leaves[persistent=true]
fill -52 205 -21 -48 207 -21 minecraft:calcite
fill -50 201 -21 -49 204 -21 minecraft:tuff
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -58 201 -39 -57 201 -39 minecraft:podzol
fill -51 201 -39 -50 201 -39 minecraft:podzol
fill -57 201 -38 -57 201 -37 minecraft:podzol
fill -51 201 -38 -51 201 -37 minecraft:podzol
fill -56 201 -37 -56 201 -37 minecraft:podzol
fill -52 201 -37 -52 201 -36 minecraft:podzol
fill -55 201 -36 -53 201 -36 minecraft:podzol
fill -54 201 -35 -54 201 -35 minecraft:podzol
fill -51 201 -25 -47 201 -24 minecraft:podzol
fill -46 201 -24 -42 201 -22 minecraft:podzol
fill -48 201 -23 -47 201 -22 minecraft:podzol
fill -56 201 -39 -52 201 -38 minecraft:dirt
fill -56 202 -39 -52 202 -38 minecraft:podzol
fill -55 201 -37 -53 201 -37 minecraft:dirt
fill -55 202 -37 -53 202 -37 minecraft:podzol
fill -51 201 -23 -49 206 -22 minecraft:mossy_stone_bricks
fill -51 207 -23 -49 207 -22 minecraft:podzol
fill -57 201 -36 -56 207 -35 minecraft:stone_bricks
fill -57 208 -36 -56 208 -35 minecraft:podzol
execute positioned -53 201 -25 run function rlk:room/prop/i_pillar
execute positioned -55 201 -26 run function rlk:room/prop/i_lantern
execute positioned -57 201 -24 run function rlk:room/prop/i_lantern
execute positioned -52 201 -23 run function rlk:room/prop/i_flower
execute positioned -49 201 -27 run function rlk:room/prop/i_flower
execute positioned -56 201 -26 run function rlk:room/prop/i_grass
execute positioned -53 201 -24 run function rlk:room/prop/i_petal
execute positioned -50 201 -34 run function rlk:room/prop/i_grass
execute positioned -44 201 -30 run function rlk:room/prop/i_petal
execute positioned -50 201 -27 run function rlk:room/prop/i_grass
execute positioned -49 201 -34 run function rlk:room/prop/i_grass
setblock -57 209 -35 minecraft:short_grass keep
setblock -56 209 -36 minecraft:short_grass keep
setblock -56 209 -35 minecraft:short_grass keep
setblock -51 208 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -51 208 -22 minecraft:short_grass keep
setblock -50 208 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -50 208 -22 minecraft:cherry_leaves[persistent=true] keep
setblock -49 208 -23 minecraft:cherry_leaves[persistent=true] keep
