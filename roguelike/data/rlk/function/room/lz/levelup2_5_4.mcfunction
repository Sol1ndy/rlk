# 구역 건설 (levelup2_5, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 215 -21 minecraft:stone
fill -59 201 -39 -42 215 -22 minecraft:air
fill -59 214 -39 -42 214 -22 minecraft:light[level=15]
fill -46 205 -25 -43 205 -22 minecraft:coarse_dirt
fill -53 205 -34 -52 205 -32 minecraft:moss_block
fill -60 215 -35 -60 215 -35 minecraft:cherry_leaves[persistent=true]
fill -60 203 -31 -60 203 -26 minecraft:andesite
fill -60 203 -38 -60 204 -38 minecraft:andesite
fill -41 214 -39 -41 215 -34 minecraft:cherry_leaves[persistent=true]
fill -41 212 -38 -41 214 -33 minecraft:moss_block
fill -41 215 -22 -41 215 -22 minecraft:cherry_leaves[persistent=true]
fill -41 213 -27 -41 214 -25 minecraft:calcite
fill -47 201 -40 -47 215 -40 minecraft:stripped_dark_oak_log
fill -56 211 -40 -52 212 -40 minecraft:calcite
fill -60 201 -40 -60 215 -40 minecraft:stripped_dark_oak_log
fill -54 203 -40 -50 206 -40 minecraft:tuff
fill -50 201 -21 -50 215 -21 minecraft:stripped_dark_oak_log
fill -45 214 -21 -41 215 -21 minecraft:andesite
fill -60 206 -21 -56 206 -21 minecraft:calcite
fill -59 205 -21 -58 208 -21 minecraft:moss_block
fill -60 215 -40 -41 215 -21 minecraft:polished_deepslate
fill -59 215 -39 -42 215 -22 minecraft:air
fill -59 201 -39 -55 204 -38 minecraft:dirt
fill -59 205 -39 -55 205 -38 minecraft:podzol
fill -49 201 -39 -42 204 -22 minecraft:dirt
fill -49 205 -39 -42 205 -22 minecraft:podzol
fill -59 201 -37 -57 204 -36 minecraft:dirt
fill -59 205 -37 -57 205 -36 minecraft:podzol
fill -54 201 -37 -50 204 -22 minecraft:dirt
fill -54 205 -37 -50 205 -22 minecraft:podzol
fill -55 201 -35 -55 204 -35 minecraft:dirt
fill -55 205 -35 -55 205 -35 minecraft:podzol
fill -56 201 -26 -55 204 -22 minecraft:dirt
fill -56 205 -26 -55 205 -22 minecraft:podzol
fill -59 201 -22 -57 204 -22 minecraft:dirt
fill -59 205 -22 -57 205 -22 minecraft:podzol
fill -59 201 -35 -56 205 -35 minecraft:dirt
fill -59 206 -35 -56 206 -35 minecraft:podzol
fill -56 201 -34 -55 205 -34 minecraft:dirt
fill -56 206 -34 -55 206 -34 minecraft:podzol
fill -55 201 -33 -55 205 -27 minecraft:dirt
fill -55 206 -33 -55 206 -27 minecraft:podzol
fill -56 201 -27 -56 205 -27 minecraft:dirt
fill -56 206 -27 -56 206 -27 minecraft:podzol
fill -57 201 -26 -57 205 -23 minecraft:dirt
fill -57 206 -26 -57 206 -23 minecraft:podzol
fill -59 201 -23 -58 205 -23 minecraft:dirt
fill -59 206 -23 -58 206 -23 minecraft:podzol
fill -59 201 -34 -57 206 -33 minecraft:dirt
fill -59 207 -34 -57 207 -33 minecraft:podzol
fill -56 201 -33 -56 206 -28 minecraft:dirt
fill -56 207 -33 -56 207 -28 minecraft:podzol
fill -57 201 -27 -57 206 -27 minecraft:dirt
fill -57 207 -27 -57 207 -27 minecraft:podzol
fill -58 201 -26 -58 206 -24 minecraft:dirt
fill -58 207 -26 -58 207 -24 minecraft:podzol
fill -59 201 -25 -59 206 -24 minecraft:dirt
fill -59 207 -25 -59 207 -24 minecraft:podzol
fill -59 201 -32 -57 207 -28 minecraft:dirt
fill -59 208 -32 -57 208 -28 minecraft:podzol
fill -59 201 -27 -58 207 -27 minecraft:dirt
fill -59 208 -27 -58 208 -27 minecraft:podzol
fill -59 201 -26 -59 207 -26 minecraft:dirt
fill -59 208 -26 -59 208 -26 minecraft:podzol
fill -51 201 -39 -50 210 -38 minecraft:mossy_stone_bricks
fill -51 211 -39 -50 211 -38 minecraft:podzol
fill -54 201 -39 -52 210 -38 minecraft:stone_bricks
fill -54 211 -39 -52 211 -38 minecraft:podzol
fill -56 201 -37 -55 212 -37 minecraft:mossy_stone_bricks
fill -56 213 -37 -55 213 -37 minecraft:podzol
fill -56 201 -36 -55 212 -36 minecraft:stone_bricks
fill -56 213 -36 -55 213 -36 minecraft:podzol
execute positioned -47 206 -37 run function rlk:room/prop/i_lantern2
execute positioned -59 207 -35 run function rlk:room/prop/i_lantern
execute positioned -50 206 -27 run function rlk:room/prop/i_flower
execute positioned -50 206 -22 run function rlk:room/prop/i_petal
execute positioned -57 208 -27 run function rlk:room/prop/i_grass
execute positioned -57 206 -36 run function rlk:room/prop/i_grass
execute positioned -49 206 -25 run function rlk:room/prop/i_grass
execute positioned -53 206 -37 run function rlk:room/prop/i_petal
execute positioned -55 207 -33 run function rlk:room/prop/i_grass
execute positioned -57 206 -39 run function rlk:room/prop/i_petal
execute positioned -47 206 -22 run function rlk:room/prop/i_grass
execute positioned -53 206 -26 run function rlk:room/prop/i_grass
setblock -56 214 -37 minecraft:cherry_leaves[persistent=true] keep
setblock -56 214 -36 minecraft:cherry_leaves[persistent=true] keep
setblock -55 214 -37 minecraft:cherry_leaves[persistent=true] keep
setblock -55 214 -36 minecraft:cherry_leaves[persistent=true] keep
setblock -54 212 -39 minecraft:short_grass keep
setblock -54 212 -38 minecraft:short_grass keep
setblock -53 212 -39 minecraft:cherry_leaves[persistent=true] keep
setblock -53 212 -38 minecraft:short_grass keep
setblock -52 212 -38 minecraft:cherry_leaves[persistent=true] keep
setblock -50 212 -39 minecraft:short_grass keep
setblock -50 212 -38 minecraft:cherry_leaves[persistent=true] keep
