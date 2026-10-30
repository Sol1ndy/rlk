# 구역 건설 (levelup2_5, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -46 200 -25 -43 200 -22 minecraft:coarse_dirt
fill -53 200 -34 -52 200 -32 minecraft:moss_block
fill -60 210 -35 -60 210 -35 minecraft:cherry_leaves[persistent=true]
fill -41 209 -39 -41 210 -34 minecraft:cherry_leaves[persistent=true]
fill -41 207 -38 -41 209 -33 minecraft:moss_block
fill -41 210 -22 -41 210 -22 minecraft:cherry_leaves[persistent=true]
fill -41 208 -27 -41 209 -25 minecraft:calcite
fill -47 201 -40 -47 210 -40 minecraft:stripped_dark_oak_log
fill -56 206 -40 -52 207 -40 minecraft:calcite
fill -60 201 -40 -60 210 -40 minecraft:stripped_dark_oak_log
fill -54 201 -40 -50 201 -40 minecraft:tuff
fill -50 201 -21 -50 210 -21 minecraft:stripped_dark_oak_log
fill -45 209 -21 -41 210 -21 minecraft:andesite
fill -60 201 -21 -56 201 -21 minecraft:calcite
fill -59 201 -21 -58 203 -21 minecraft:moss_block
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -59 201 -35 -56 201 -35 minecraft:podzol
fill -56 201 -34 -55 201 -34 minecraft:podzol
fill -55 201 -33 -55 201 -27 minecraft:podzol
fill -56 201 -27 -56 201 -27 minecraft:podzol
fill -57 201 -26 -57 201 -23 minecraft:podzol
fill -59 201 -23 -58 201 -23 minecraft:podzol
fill -59 201 -34 -57 201 -33 minecraft:dirt
fill -59 202 -34 -57 202 -33 minecraft:podzol
fill -56 201 -33 -56 201 -28 minecraft:dirt
fill -56 202 -33 -56 202 -28 minecraft:podzol
fill -57 201 -27 -57 201 -27 minecraft:dirt
fill -57 202 -27 -57 202 -27 minecraft:podzol
fill -58 201 -26 -58 201 -24 minecraft:dirt
fill -58 202 -26 -58 202 -24 minecraft:podzol
fill -59 201 -25 -59 201 -24 minecraft:dirt
fill -59 202 -25 -59 202 -24 minecraft:podzol
fill -59 201 -32 -57 202 -28 minecraft:dirt
fill -59 203 -32 -57 203 -28 minecraft:podzol
fill -59 201 -27 -58 202 -27 minecraft:dirt
fill -59 203 -27 -58 203 -27 minecraft:podzol
fill -59 201 -26 -59 202 -26 minecraft:dirt
fill -59 203 -26 -59 203 -26 minecraft:podzol
fill -51 201 -39 -50 205 -38 minecraft:mossy_stone_bricks
fill -51 206 -39 -50 206 -38 minecraft:podzol
fill -54 201 -39 -52 205 -38 minecraft:stone_bricks
fill -54 206 -39 -52 206 -38 minecraft:podzol
fill -56 201 -37 -55 207 -37 minecraft:mossy_stone_bricks
fill -56 208 -37 -55 208 -37 minecraft:podzol
fill -56 201 -36 -55 207 -36 minecraft:stone_bricks
fill -56 208 -36 -55 208 -36 minecraft:podzol
execute positioned -47 201 -37 run function rlk:room/prop/i_lantern2
execute positioned -59 202 -35 run function rlk:room/prop/i_lantern
execute positioned -50 201 -27 run function rlk:room/prop/i_flower
execute positioned -50 201 -22 run function rlk:room/prop/i_petal
execute positioned -57 203 -27 run function rlk:room/prop/i_grass
execute positioned -57 201 -36 run function rlk:room/prop/i_grass
execute positioned -49 201 -25 run function rlk:room/prop/i_grass
execute positioned -53 201 -37 run function rlk:room/prop/i_petal
execute positioned -55 202 -33 run function rlk:room/prop/i_grass
execute positioned -57 201 -39 run function rlk:room/prop/i_petal
execute positioned -47 201 -22 run function rlk:room/prop/i_grass
execute positioned -53 201 -26 run function rlk:room/prop/i_grass
setblock -56 209 -37 minecraft:cherry_leaves[persistent=true] keep
setblock -56 209 -36 minecraft:cherry_leaves[persistent=true] keep
setblock -55 209 -37 minecraft:cherry_leaves[persistent=true] keep
setblock -55 209 -36 minecraft:cherry_leaves[persistent=true] keep
setblock -54 207 -39 minecraft:short_grass keep
setblock -54 207 -38 minecraft:short_grass keep
setblock -53 207 -39 minecraft:cherry_leaves[persistent=true] keep
setblock -53 207 -38 minecraft:short_grass keep
setblock -52 207 -38 minecraft:cherry_leaves[persistent=true] keep
setblock -50 207 -39 minecraft:short_grass keep
setblock -50 207 -38 minecraft:cherry_leaves[persistent=true] keep
