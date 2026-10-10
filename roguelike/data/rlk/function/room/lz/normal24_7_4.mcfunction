# 구역 건설 (normal24_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -40 -41 200 -21 minecraft:podzol
fill -60 201 -40 -41 212 -21 minecraft:stone
fill -59 201 -39 -42 212 -22 minecraft:air
fill -59 211 -39 -42 211 -22 minecraft:light[level=15]
fill -58 202 -25 -56 202 -23 minecraft:coarse_dirt
fill -60 210 -27 -60 212 -22 minecraft:calcite
fill -60 211 -31 -60 212 -30 minecraft:calcite
fill -60 211 -33 -60 212 -31 minecraft:cherry_leaves[persistent=true]
fill -41 211 -35 -41 212 -33 minecraft:cherry_leaves[persistent=true]
fill -41 207 -37 -41 209 -32 minecraft:andesite
fill -41 201 -38 -41 201 -34 minecraft:andesite
fill -52 201 -40 -51 202 -40 minecraft:calcite
fill -60 210 -40 -56 212 -40 minecraft:tuff
fill -60 210 -40 -58 211 -40 minecraft:tuff
fill -58 207 -21 -54 208 -21 minecraft:calcite
fill -57 212 -21 -53 212 -21 minecraft:cherry_leaves[persistent=true]
fill -52 207 -21 -48 209 -21 minecraft:calcite
fill -50 203 -21 -49 206 -21 minecraft:tuff
fill -60 212 -40 -41 212 -21 minecraft:polished_deepslate
fill -59 212 -39 -42 212 -22 minecraft:air
fill -59 201 -39 -59 201 -22 minecraft:dirt
fill -59 202 -39 -59 202 -22 minecraft:podzol
fill -49 201 -39 -42 201 -26 minecraft:dirt
fill -49 202 -39 -42 202 -26 minecraft:podzol
fill -58 201 -38 -58 201 -22 minecraft:dirt
fill -58 202 -38 -58 202 -22 minecraft:podzol
fill -50 201 -38 -50 201 -26 minecraft:dirt
fill -50 202 -38 -50 202 -26 minecraft:podzol
fill -51 201 -36 -51 201 -26 minecraft:dirt
fill -51 202 -36 -51 202 -26 minecraft:podzol
fill -55 201 -35 -55 201 -22 minecraft:dirt
fill -55 202 -35 -55 202 -22 minecraft:podzol
fill -53 201 -35 -52 201 -22 minecraft:dirt
fill -53 202 -35 -52 202 -22 minecraft:podzol
fill -57 201 -34 -56 201 -22 minecraft:dirt
fill -57 202 -34 -56 202 -22 minecraft:podzol
fill -54 201 -34 -54 201 -22 minecraft:dirt
fill -54 202 -34 -54 202 -22 minecraft:podzol
fill -46 201 -25 -42 201 -25 minecraft:dirt
fill -46 202 -25 -42 202 -25 minecraft:podzol
fill -58 201 -39 -57 202 -39 minecraft:dirt
fill -58 203 -39 -57 203 -39 minecraft:podzol
fill -51 201 -39 -50 202 -39 minecraft:dirt
fill -51 203 -39 -50 203 -39 minecraft:podzol
fill -57 201 -38 -57 202 -37 minecraft:dirt
fill -57 203 -38 -57 203 -37 minecraft:podzol
fill -51 201 -38 -51 202 -37 minecraft:dirt
fill -51 203 -38 -51 203 -37 minecraft:podzol
fill -56 201 -37 -56 202 -37 minecraft:dirt
fill -56 203 -37 -56 203 -37 minecraft:podzol
fill -52 201 -37 -52 202 -36 minecraft:dirt
fill -52 203 -37 -52 203 -36 minecraft:podzol
fill -55 201 -36 -53 202 -36 minecraft:dirt
fill -55 203 -36 -53 203 -36 minecraft:podzol
fill -54 201 -35 -54 202 -35 minecraft:dirt
fill -54 203 -35 -54 203 -35 minecraft:podzol
fill -51 201 -25 -47 202 -24 minecraft:dirt
fill -51 203 -25 -47 203 -24 minecraft:podzol
fill -46 201 -24 -42 202 -22 minecraft:dirt
fill -46 203 -24 -42 203 -22 minecraft:podzol
fill -48 201 -23 -47 202 -22 minecraft:dirt
fill -48 203 -23 -47 203 -22 minecraft:podzol
fill -56 201 -39 -52 203 -38 minecraft:dirt
fill -56 204 -39 -52 204 -38 minecraft:podzol
fill -55 201 -37 -53 203 -37 minecraft:dirt
fill -55 204 -37 -53 204 -37 minecraft:podzol
fill -51 201 -23 -49 208 -22 minecraft:mossy_stone_bricks
fill -51 209 -23 -49 209 -22 minecraft:podzol
fill -57 201 -36 -56 209 -35 minecraft:stone_bricks
fill -57 210 -36 -56 210 -35 minecraft:podzol
execute positioned -53 203 -25 run function rlk:room/prop/i_pillar
execute positioned -55 203 -26 run function rlk:room/prop/i_lantern
execute positioned -57 203 -24 run function rlk:room/prop/i_lantern
execute positioned -52 203 -23 run function rlk:room/prop/i_flower
execute positioned -49 203 -27 run function rlk:room/prop/i_flower
execute positioned -56 203 -26 run function rlk:room/prop/i_grass
execute positioned -53 203 -24 run function rlk:room/prop/i_petal
execute positioned -50 203 -34 run function rlk:room/prop/i_grass
execute positioned -44 203 -30 run function rlk:room/prop/i_petal
execute positioned -50 203 -27 run function rlk:room/prop/i_grass
execute positioned -49 203 -34 run function rlk:room/prop/i_grass
setblock -57 211 -35 minecraft:short_grass keep
setblock -56 211 -36 minecraft:short_grass keep
setblock -56 211 -35 minecraft:short_grass keep
setblock -51 210 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -51 210 -22 minecraft:short_grass keep
setblock -50 210 -23 minecraft:cherry_leaves[persistent=true] keep
setblock -50 210 -22 minecraft:cherry_leaves[persistent=true] keep
setblock -49 210 -23 minecraft:cherry_leaves[persistent=true] keep
