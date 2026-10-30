# 구역 건설 (levelup2_3, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -40 -1 200 -21 minecraft:podzol
fill -20 201 -40 -1 210 -21 minecraft:stone
fill -19 201 -39 -2 210 -22 minecraft:air
fill -19 209 -39 -2 209 -22 minecraft:light[level=15]
fill -13 200 -35 -11 200 -33 minecraft:gravel
fill -11 200 -29 -10 200 -26 minecraft:moss_block
fill -12 200 -33 -8 200 -31 minecraft:gravel
fill -20 205 -29 -20 207 -26 minecraft:calcite
fill -20 205 -40 -20 206 -38 minecraft:dark_prismarine
fill -20 210 -37 -20 210 -37 minecraft:birch_leaves[persistent=true]
fill -1 206 -33 -1 206 -28 minecraft:moss_block
fill -1 205 -40 -1 208 -37 minecraft:prismarine
fill -1 204 -34 -1 206 -31 minecraft:calcite
fill -1 207 -25 -1 209 -23 minecraft:calcite
fill -1 209 -30 -1 209 -28 minecraft:prismarine
fill -1 209 -25 -1 210 -23 minecraft:moss_block
fill -8 209 -40 -6 210 -40 minecraft:oak_leaves[persistent=true]
fill -20 210 -40 -16 210 -40 minecraft:birch_leaves[persistent=true]
fill -6 205 -40 -6 205 -40 minecraft:calcite
fill -19 210 -21 -16 210 -21 minecraft:birch_leaves[persistent=true]
fill -6 209 -21 -4 210 -21 minecraft:oak_leaves[persistent=true]
fill -19 206 -21 -15 209 -21 minecraft:moss_block
fill -20 210 -40 -1 210 -21 minecraft:polished_deepslate
fill -19 210 -39 -2 210 -22 minecraft:air
fill -11 201 -25 -7 201 -25 minecraft:podzol
fill -11 201 -24 -10 201 -22 minecraft:podzol
fill -6 201 -24 -2 201 -24 minecraft:podzol
fill -9 201 -22 -9 201 -22 minecraft:podzol
fill -9 201 -24 -7 201 -23 minecraft:dirt
fill -9 202 -24 -7 202 -23 minecraft:podzol
fill -6 201 -23 -2 201 -22 minecraft:dirt
fill -6 202 -23 -2 202 -22 minecraft:podzol
fill -8 201 -22 -7 201 -22 minecraft:dirt
fill -8 202 -22 -7 202 -22 minecraft:podzol
fill -4 201 -39 -2 205 -39 minecraft:calcite
fill -4 206 -39 -2 206 -39 minecraft:podzol
fill -14 199 -25 -12 199 -22 minecraft:clay
fill -14 200 -25 -12 200 -22 minecraft:water
fill -15 200 -22 -15 200 -22 minecraft:sand
setblock -14 200 -24 minecraft:seagrass
setblock -13 200 -22 minecraft:seagrass
execute positioned -10 201 -36 run function rlk:room/prop/fo_tree
execute positioned -14 201 -35 run function rlk:room/prop/fo_rock_s
execute positioned -7 201 -36 run function rlk:room/prop/fo_col_b
execute positioned -15 201 -39 run function rlk:room/prop/fo_rock_s
execute positioned -3 201 -35 run function rlk:room/prop/p_grass
execute positioned -8 201 -26 run function rlk:room/prop/p_grass
execute positioned -8 203 -22 run function rlk:room/prop/fo_flower
execute positioned -2 201 -34 run function rlk:room/prop/fo_white
execute positioned -6 203 -23 run function rlk:room/prop/p_grass
execute positioned -2 203 -22 run function rlk:room/prop/fo_flower
execute positioned -11 201 -26 run function rlk:room/prop/fo_white
execute positioned -12 201 -29 run function rlk:room/prop/p_grass
setblock -4 207 -39 minecraft:short_grass keep
setblock -2 207 -39 minecraft:short_grass keep
