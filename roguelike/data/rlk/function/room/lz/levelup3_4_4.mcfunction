# 구역 건설 (levelup3_4, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:podzol
fill -40 201 20 -21 210 39 minecraft:stone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -28 200 31 -26 200 34 minecraft:packed_mud
fill -37 200 23 -36 200 24 minecraft:gravel
fill -32 200 29 -29 200 30 minecraft:packed_mud
fill -40 209 30 -40 210 34 minecraft:cherry_leaves[persistent=true]
fill -40 209 35 -40 210 38 minecraft:calcite
fill -40 209 27 -40 210 31 minecraft:cherry_leaves[persistent=true]
fill -40 209 27 -40 210 30 minecraft:cherry_leaves[persistent=true]
fill -21 209 20 -21 210 24 minecraft:cherry_leaves[persistent=true]
fill -21 201 21 -21 210 21 minecraft:stripped_dark_oak_log
fill -21 209 22 -21 210 24 minecraft:cherry_leaves[persistent=true]
fill -32 209 20 -27 210 20 minecraft:cherry_leaves[persistent=true]
fill -28 201 20 -28 210 20 minecraft:stripped_dark_oak_log
fill -34 204 20 -31 207 20 minecraft:andesite
fill -34 210 39 -33 210 39 minecraft:cherry_leaves[persistent=true]
fill -29 202 39 -24 203 39 minecraft:calcite
fill -31 210 39 -27 210 39 minecraft:cherry_leaves[persistent=true]
fill -35 201 39 -30 204 39 minecraft:tuff
fill -24 201 39 -24 210 39 minecraft:stripped_dark_oak_log
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -39 201 25 -37 201 25 minecraft:podzol
fill -37 201 26 -37 201 34 minecraft:podzol
fill -25 201 30 -24 201 31 minecraft:podzol
fill -23 201 31 -22 201 32 minecraft:podzol
fill -25 201 32 -25 201 34 minecraft:podzol
fill -22 201 33 -22 201 33 minecraft:podzol
fill -39 201 34 -38 201 35 minecraft:podzol
fill -31 201 35 -26 201 35 minecraft:podzol
fill -31 201 36 -30 201 36 minecraft:podzol
fill -39 201 26 -38 201 33 minecraft:dirt
fill -39 202 26 -38 202 33 minecraft:podzol
fill -24 201 32 -24 201 38 minecraft:dirt
fill -24 202 32 -24 202 38 minecraft:podzol
fill -23 201 33 -23 201 38 minecraft:dirt
fill -23 202 33 -23 202 38 minecraft:podzol
fill -22 201 34 -22 201 38 minecraft:dirt
fill -22 202 34 -22 202 38 minecraft:podzol
fill -25 201 35 -25 201 38 minecraft:dirt
fill -25 202 35 -25 202 38 minecraft:podzol
fill -29 201 36 -26 201 36 minecraft:dirt
fill -29 202 36 -26 202 36 minecraft:podzol
fill -26 201 37 -26 201 38 minecraft:dirt
fill -26 202 37 -26 202 38 minecraft:podzol
fill -31 201 37 -27 207 38 minecraft:stone_bricks
fill -31 208 37 -27 208 38 minecraft:podzol
execute positioned -25 201 28 run function rlk:room/prop/i_lantern2
execute positioned -24 201 21 run function rlk:room/prop/i_lantern
execute positioned -24 202 30 run function rlk:room/prop/i_lantern
execute positioned -37 201 35 run function rlk:room/prop/i_wall_z
execute positioned -28 201 28 run function rlk:room/prop/i_grass
execute positioned -39 201 36 run function rlk:room/prop/i_flower
execute positioned -34 201 32 run function rlk:room/prop/i_grass
execute positioned -34 201 35 run function rlk:room/prop/i_petal
execute positioned -27 201 31 run function rlk:room/prop/i_petal
execute positioned -23 203 35 run function rlk:room/prop/i_petal
execute positioned -34 201 24 run function rlk:room/prop/i_flower
setblock -29 209 37 minecraft:short_grass keep
setblock -29 209 38 minecraft:cherry_leaves[persistent=true] keep
setblock -28 209 37 minecraft:cherry_leaves[persistent=true] keep
setblock -28 209 38 minecraft:short_grass keep
setblock -27 209 38 minecraft:cherry_leaves[persistent=true] keep
