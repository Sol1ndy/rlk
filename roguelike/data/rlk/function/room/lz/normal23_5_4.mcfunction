# 구역 건설 (normal23_5, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 210 -21 minecraft:stone
fill -59 201 -39 -42 210 -22 minecraft:air
fill -59 209 -39 -42 209 -22 minecraft:light[level=15]
fill -48 200 -30 -44 200 -28 minecraft:gravel
fill -52 200 -35 -48 200 -34 minecraft:coarse_dirt
fill -44 200 -30 -43 200 -28 minecraft:gravel
fill -60 209 -37 -60 210 -36 minecraft:cherry_leaves[persistent=true]
fill -60 207 -21 -60 210 -21 minecraft:cobblestone
fill -60 203 -34 -60 206 -32 minecraft:andesite
fill -60 209 -26 -60 210 -24 minecraft:cherry_leaves[persistent=true]
fill -60 206 -31 -60 208 -28 minecraft:tuff
fill -60 209 -39 -60 210 -39 minecraft:cherry_leaves[persistent=true]
fill -41 209 -24 -41 210 -24 minecraft:cherry_leaves[persistent=true]
fill -41 205 -27 -41 206 -22 minecraft:andesite
fill -41 210 -37 -41 210 -32 minecraft:calcite
fill -41 202 -28 -41 202 -23 minecraft:andesite
fill -41 204 -30 -41 205 -29 minecraft:cobblestone
fill -41 209 -40 -41 210 -36 minecraft:cherry_leaves[persistent=true]
fill -58 205 -40 -56 207 -40 minecraft:tuff
fill -49 210 -40 -49 210 -40 minecraft:cherry_leaves[persistent=true]
fill -58 209 -40 -55 210 -40 minecraft:cherry_leaves[persistent=true]
fill -55 210 -40 -53 210 -40 minecraft:andesite
fill -55 206 -21 -53 207 -21 minecraft:calcite
fill -57 210 -21 -53 210 -21 minecraft:cherry_leaves[persistent=true]
fill -48 201 -21 -46 202 -21 minecraft:cobblestone
fill -48 210 -21 -47 210 -21 minecraft:moss_block
fill -51 209 -21 -46 210 -21 minecraft:cobblestone
fill -60 210 -40 -41 210 -21 minecraft:polished_deepslate
fill -59 210 -39 -42 210 -22 minecraft:air
fill -57 201 -39 -57 201 -35 minecraft:podzol
fill -56 201 -34 -55 201 -34 minecraft:podzol
fill -55 201 -33 -55 201 -31 minecraft:podzol
fill -57 201 -31 -56 201 -31 minecraft:podzol
fill -59 201 -30 -57 201 -30 minecraft:podzol
fill -56 201 -28 -55 201 -27 minecraft:podzol
fill -55 201 -26 -55 201 -26 minecraft:podzol
fill -54 201 -25 -50 201 -25 minecraft:podzol
fill -51 201 -24 -50 201 -22 minecraft:podzol
fill -58 201 -23 -57 201 -22 minecraft:podzol
fill -58 201 -39 -58 201 -35 minecraft:dirt
fill -58 202 -39 -58 202 -35 minecraft:podzol
fill -57 201 -34 -57 201 -32 minecraft:dirt
fill -57 202 -34 -57 202 -32 minecraft:podzol
fill -56 201 -33 -56 201 -32 minecraft:dirt
fill -56 202 -33 -56 202 -32 minecraft:podzol
fill -59 201 -32 -58 201 -31 minecraft:dirt
fill -59 202 -32 -58 202 -31 minecraft:podzol
fill -56 201 -26 -56 201 -22 minecraft:dirt
fill -56 202 -26 -56 202 -22 minecraft:podzol
fill -55 201 -25 -55 201 -22 minecraft:dirt
fill -55 202 -25 -55 202 -22 minecraft:podzol
fill -54 201 -24 -52 201 -22 minecraft:dirt
fill -54 202 -24 -52 202 -22 minecraft:podzol
fill -59 201 -39 -59 202 -33 minecraft:dirt
fill -59 203 -39 -59 203 -33 minecraft:podzol
fill -58 201 -34 -58 202 -33 minecraft:dirt
fill -58 203 -34 -58 203 -33 minecraft:podzol
fill -57 201 -29 -57 207 -29 minecraft:mossy_stone_bricks
fill -57 208 -29 -57 208 -29 minecraft:podzol
fill -57 201 -26 -57 207 -24 minecraft:mossy_stone_bricks
fill -57 208 -26 -57 208 -24 minecraft:podzol
fill -59 201 -29 -58 207 -24 minecraft:stone_bricks
fill -59 208 -29 -58 208 -24 minecraft:podzol
fill -57 201 -28 -57 207 -27 minecraft:stone_bricks
fill -57 208 -28 -57 208 -27 minecraft:podzol
execute positioned -45 201 -24 run function rlk:room/prop/i_lantern
execute positioned -53 202 -25 run function rlk:room/prop/i_lantern2
execute positioned -57 203 -32 run function rlk:room/prop/i_pillar
execute positioned -46 201 -33 run function rlk:room/prop/i_grass
execute positioned -47 201 -38 run function rlk:room/prop/i_grass
execute positioned -57 202 -31 run function rlk:room/prop/i_petal
execute positioned -59 203 -31 run function rlk:room/prop/i_grass
execute positioned -57 202 -38 run function rlk:room/prop/i_petal
execute positioned -45 201 -34 run function rlk:room/prop/i_grass
execute positioned -47 201 -33 run function rlk:room/prop/i_petal
execute positioned -49 201 -36 run function rlk:room/prop/i_grass
execute positioned -47 201 -28 run function rlk:room/prop/i_petal
setblock -59 209 -29 minecraft:short_grass keep
setblock -59 209 -28 minecraft:cherry_leaves[persistent=true] keep
setblock -59 209 -27 minecraft:short_grass keep
setblock -59 209 -26 minecraft:cherry_leaves[persistent=true] keep
setblock -59 209 -24 minecraft:short_grass keep
setblock -58 209 -28 minecraft:cherry_leaves[persistent=true] keep
setblock -58 209 -25 minecraft:cherry_leaves[persistent=true] keep
setblock -58 209 -24 minecraft:cherry_leaves[persistent=true] keep
setblock -57 209 -29 minecraft:cherry_leaves[persistent=true] keep
setblock -57 209 -28 minecraft:short_grass keep
setblock -57 209 -26 minecraft:cherry_leaves[persistent=true] keep
setblock -57 209 -25 minecraft:cherry_leaves[persistent=true] keep
setblock -57 209 -24 minecraft:cherry_leaves[persistent=true] keep
