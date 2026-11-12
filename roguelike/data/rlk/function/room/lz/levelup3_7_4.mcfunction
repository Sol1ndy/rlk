# 구역 건설 (levelup3_7, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -13 200 -32 -11 200 -29 minecraft:moss_block
fill -8 200 -32 -5 200 -30 minecraft:coarse_dirt
fill -20 201 -33 -20 202 -33 minecraft:cobblestone
fill -20 207 -38 -20 208 -36 minecraft:calcite
fill -20 201 -36 -20 201 -34 minecraft:moss_block
fill -20 207 -37 -20 208 -36 minecraft:calcite
fill -20 209 -35 -20 210 -34 minecraft:cherry_leaves[persistent=true]
fill -20 201 -34 -20 202 -33 minecraft:moss_block
fill -1 210 -39 -1 210 -34 minecraft:cherry_leaves[persistent=true]
fill -1 201 -29 -1 202 -26 minecraft:moss_block
fill -1 209 -25 -1 210 -21 minecraft:cherry_leaves[persistent=true]
fill -1 210 -35 -1 210 -34 minecraft:calcite
fill -1 204 -23 -1 206 -21 minecraft:tuff
fill -19 208 -40 -18 208 -40 minecraft:calcite
fill -10 210 -40 -8 210 -40 minecraft:cherry_leaves[persistent=true]
fill -10 209 -40 -8 210 -40 minecraft:cherry_leaves[persistent=true]
fill -12 210 -40 -8 210 -40 minecraft:cherry_leaves[persistent=true]
fill -6 210 -21 -3 210 -21 minecraft:cherry_leaves[persistent=true]
fill -6 210 -21 -5 210 -21 minecraft:cherry_leaves[persistent=true]
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -5 201 -26 -4 201 -26 minecraft:podzol
fill -14 201 -25 -6 201 -25 minecraft:podzol
fill -4 201 -25 -4 201 -22 minecraft:podzol
fill -16 201 -24 -15 201 -24 minecraft:podzol
fill -16 201 -23 -16 201 -22 minecraft:podzol
fill -5 201 -25 -5 201 -22 minecraft:dirt
fill -5 202 -25 -5 202 -22 minecraft:podzol
fill -14 201 -24 -6 201 -24 minecraft:dirt
fill -14 202 -24 -6 202 -24 minecraft:podzol
fill -15 201 -23 -14 201 -22 minecraft:dirt
fill -15 202 -23 -14 202 -22 minecraft:podzol
fill -6 201 -23 -6 201 -22 minecraft:dirt
fill -6 202 -23 -6 202 -22 minecraft:podzol
fill -13 201 -23 -7 202 -23 minecraft:dirt
fill -13 203 -23 -7 203 -23 minecraft:podzol
fill -7 201 -22 -7 202 -22 minecraft:dirt
fill -7 203 -22 -7 203 -22 minecraft:podzol
fill -13 201 -22 -8 207 -22 minecraft:mossy_stone_bricks
fill -13 208 -22 -8 208 -22 minecraft:podzol
execute positioned -5 201 -35 run function rlk:room/prop/i_house_a_r2
execute positioned -13 201 -39 run function rlk:room/prop/i_pillar
execute positioned -10 201 -30 run function rlk:room/prop/i_petal
execute positioned -4 201 -27 run function rlk:room/prop/i_petal
execute positioned -16 201 -29 run function rlk:room/prop/i_petal
execute positioned -4 202 -23 run function rlk:room/prop/i_grass
execute positioned -14 201 -36 run function rlk:room/prop/i_petal
execute positioned -18 201 -32 run function rlk:room/prop/i_petal
execute positioned -18 201 -31 run function rlk:room/prop/i_grass
execute positioned -19 201 -22 run function rlk:room/prop/i_petal
setblock -13 209 -22 minecraft:short_grass keep
setblock -12 209 -22 minecraft:cherry_leaves[persistent=true] keep
setblock -11 209 -22 minecraft:short_grass keep
setblock -9 209 -22 minecraft:cherry_leaves[persistent=true] keep
setblock -8 209 -22 minecraft:short_grass keep
