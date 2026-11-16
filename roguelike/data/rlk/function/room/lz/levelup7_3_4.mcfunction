# 구역 건설 (levelup7_3, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:podzol
fill 20 201 20 39 210 39 minecraft:stone
fill 21 201 21 38 210 38 minecraft:air
fill 21 209 21 38 209 38 minecraft:light[level=15]
fill 33 200 30 36 200 33 minecraft:moss_block
fill 31 200 32 32 200 34 minecraft:gravel
fill 27 200 26 28 200 27 minecraft:coarse_dirt
fill 20 201 32 20 204 33 minecraft:tuff
fill 20 204 32 20 207 36 minecraft:calcite
fill 20 209 39 20 210 39 minecraft:cherry_leaves[persistent=true]
fill 20 202 22 20 205 23 minecraft:calcite
fill 20 209 25 20 210 29 minecraft:cherry_leaves[persistent=true]
fill 39 201 27 39 210 27 minecraft:stripped_dark_oak_log
fill 39 209 22 39 210 23 minecraft:cherry_leaves[persistent=true]
fill 39 201 36 39 210 36 minecraft:stripped_dark_oak_log
fill 39 201 25 39 201 30 minecraft:andesite
fill 25 201 20 25 210 20 minecraft:stripped_dark_oak_log
fill 25 205 20 25 206 20 minecraft:andesite
fill 20 201 20 20 201 20 minecraft:tuff
fill 26 201 20 29 201 20 minecraft:cobblestone
fill 22 201 20 24 201 20 minecraft:andesite
fill 31 210 20 32 210 20 minecraft:calcite
fill 27 210 39 27 210 39 minecraft:cherry_leaves[persistent=true]
fill 27 209 39 29 210 39 minecraft:cherry_leaves[persistent=true]
fill 26 201 39 28 201 39 minecraft:moss_block
fill 20 210 20 39 210 39 minecraft:polished_deepslate
fill 21 210 21 38 210 38 minecraft:air
fill 34 201 21 34 201 22 minecraft:podzol
fill 35 201 22 35 201 24 minecraft:podzol
fill 36 201 24 37 201 25 minecraft:podzol
fill 38 201 25 38 201 25 minecraft:podzol
fill 35 201 21 38 201 21 minecraft:dirt
fill 35 202 21 38 202 21 minecraft:podzol
fill 36 201 22 38 201 23 minecraft:dirt
fill 36 202 22 38 202 23 minecraft:podzol
fill 38 201 24 38 201 24 minecraft:dirt
fill 38 202 24 38 202 24 minecraft:podzol
fill 28 201 21 30 206 23 minecraft:stone_bricks
fill 28 207 21 30 207 23 minecraft:podzol
fill 33 201 23 34 207 24 minecraft:stone_bricks
fill 33 208 23 34 208 24 minecraft:podzol
execute positioned 21 201 21 run function rlk:room/prop/i_rock
execute positioned 36 201 29 run function rlk:room/prop/i_lantern2
execute positioned 36 201 32 run function rlk:room/prop/i_pillar
execute positioned 36 201 26 run function rlk:room/prop/i_pillar
execute positioned 35 201 35 run function rlk:room/prop/i_petal
execute positioned 23 201 33 run function rlk:room/prop/i_flower
execute positioned 22 201 23 run function rlk:room/prop/i_grass
execute positioned 30 201 33 run function rlk:room/prop/i_petal
execute positioned 28 201 33 run function rlk:room/prop/i_grass
execute positioned 31 201 30 run function rlk:room/prop/i_petal
execute positioned 31 201 21 run function rlk:room/prop/i_petal
execute positioned 37 201 28 run function rlk:room/prop/i_petal
setblock 28 208 21 minecraft:cherry_leaves[persistent=true] keep
setblock 28 208 23 minecraft:cherry_leaves[persistent=true] keep
setblock 30 208 21 minecraft:short_grass keep
setblock 30 208 22 minecraft:cherry_leaves[persistent=true] keep
setblock 33 209 23 minecraft:cherry_leaves[persistent=true] keep
setblock 33 209 24 minecraft:cherry_leaves[persistent=true] keep
setblock 34 209 23 minecraft:cherry_leaves[persistent=true] keep
setblock 34 209 24 minecraft:short_grass keep
