# 구역 건설 (levelup5_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 40 -21 200 59 minecraft:podzol
fill -40 201 40 -21 210 59 minecraft:stone
fill -39 201 41 -22 210 58 minecraft:air
fill -39 209 41 -22 209 58 minecraft:light[level=15]
fill -27 200 43 -25 200 45 minecraft:gravel
fill -36 200 49 -33 200 51 minecraft:coarse_dirt
fill -38 200 56 -37 200 58 minecraft:gravel
fill -40 201 44 -40 210 44 minecraft:stripped_dark_oak_log
fill -40 209 53 -40 210 55 minecraft:cherry_leaves[persistent=true]
fill -40 201 45 -40 210 45 minecraft:stripped_dark_oak_log
fill -40 210 49 -40 210 54 minecraft:cherry_leaves[persistent=true]
fill -40 206 42 -40 209 43 minecraft:cobblestone
fill -40 204 50 -40 204 50 minecraft:moss_block
fill -21 201 44 -21 210 44 minecraft:stripped_dark_oak_log
fill -21 209 50 -21 210 51 minecraft:andesite
fill -21 210 45 -21 210 48 minecraft:cherry_leaves[persistent=true]
fill -21 206 43 -21 206 47 minecraft:calcite
fill -37 205 40 -36 207 40 minecraft:cobblestone
fill -30 210 40 -28 210 40 minecraft:cherry_leaves[persistent=true]
fill -38 204 40 -34 205 40 minecraft:tuff
fill -28 209 40 -26 210 40 minecraft:cobblestone
fill -31 210 40 -28 210 40 minecraft:cobblestone
fill -34 210 40 -29 210 40 minecraft:cherry_leaves[persistent=true]
fill -30 209 59 -27 210 59 minecraft:cherry_leaves[persistent=true]
fill -37 206 59 -33 207 59 minecraft:calcite
fill -26 207 59 -26 207 59 minecraft:cobblestone
fill -30 201 59 -30 210 59 minecraft:stripped_dark_oak_log
fill -39 202 59 -35 203 59 minecraft:calcite
fill -40 210 40 -21 210 59 minecraft:polished_deepslate
fill -39 210 41 -22 210 58 minecraft:air
fill -39 201 41 -37 201 41 minecraft:podzol
fill -37 201 42 -37 201 45 minecraft:podzol
fill -36 201 46 -35 201 46 minecraft:podzol
fill -35 201 47 -35 201 48 minecraft:podzol
fill -36 201 48 -36 201 48 minecraft:podzol
fill -39 201 49 -37 201 49 minecraft:podzol
fill -39 201 42 -38 201 42 minecraft:dirt
fill -39 202 42 -38 202 42 minecraft:podzol
fill -38 201 43 -38 201 45 minecraft:dirt
fill -38 202 43 -38 202 45 minecraft:podzol
fill -37 201 46 -37 201 46 minecraft:dirt
fill -37 202 46 -37 202 46 minecraft:podzol
fill -36 201 47 -36 201 47 minecraft:dirt
fill -36 202 47 -36 202 47 minecraft:podzol
fill -39 201 48 -37 201 48 minecraft:dirt
fill -39 202 48 -37 202 48 minecraft:podzol
fill -39 201 43 -39 202 47 minecraft:dirt
fill -39 203 43 -39 203 47 minecraft:podzol
fill -38 201 46 -38 202 47 minecraft:dirt
fill -38 203 46 -38 203 47 minecraft:podzol
fill -37 201 47 -37 202 47 minecraft:dirt
fill -37 203 47 -37 203 47 minecraft:podzol
fill -33 201 57 -31 206 57 minecraft:mossy_stone_bricks
fill -33 207 57 -31 207 57 minecraft:podzol
fill -34 201 58 -34 206 58 minecraft:mossy_stone_bricks
fill -34 207 58 -34 207 58 minecraft:podzol
fill -34 201 57 -34 206 57 minecraft:stone_bricks
fill -34 207 57 -34 207 57 minecraft:podzol
fill -30 201 57 -30 206 58 minecraft:stone_bricks
fill -30 207 57 -30 207 58 minecraft:podzol
fill -33 201 58 -31 206 58 minecraft:stone_bricks
fill -33 207 58 -31 207 58 minecraft:podzol
fill -25 186 47 -21 199 59 minecraft:stone
fill -24 186 48 -22 186 58 minecraft:dirt
fill -24 187 48 -22 188 58 minecraft:cherry_leaves[persistent=true]
fill -24 189 48 -22 201 58 minecraft:air
execute positioned -35 201 50 run function rlk:room/prop/i_house_a_r1
execute positioned -37 203 46 run function rlk:room/prop/i_lantern
execute positioned -37 202 43 run function rlk:room/prop/i_lantern
execute positioned -25 201 48 run function rlk:room/prop/i_fence_z
execute positioned -35 201 45 run function rlk:room/prop/i_petal
execute positioned -22 201 47 run function rlk:room/prop/i_grass
execute positioned -31 201 41 run function rlk:room/prop/i_flower
execute positioned -28 201 44 run function rlk:room/prop/i_petal
execute positioned -29 201 42 run function rlk:room/prop/i_grass
execute positioned -24 201 56 run function rlk:room/prop/i_petal
execute positioned -25 201 51 run function rlk:room/prop/i_petal
execute positioned -27 201 51 run function rlk:room/prop/i_petal
setblock -34 208 57 minecraft:short_grass keep
setblock -34 208 58 minecraft:short_grass keep
setblock -33 208 57 minecraft:short_grass keep
setblock -32 208 57 minecraft:short_grass keep
setblock -31 208 58 minecraft:cherry_leaves[persistent=true] keep
setblock -30 208 57 minecraft:cherry_leaves[persistent=true] keep
setblock -30 208 58 minecraft:short_grass keep
