# 구역 건설 (levelup7_3, 테마 4): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:podzol
fill 20 201 20 39 215 39 minecraft:stone
fill 21 201 21 38 215 38 minecraft:air
fill 21 214 21 38 214 38 minecraft:light[level=15]
fill 33 205 30 36 205 33 minecraft:moss_block
fill 31 205 32 32 205 34 minecraft:gravel
fill 27 205 26 28 205 27 minecraft:coarse_dirt
fill 20 206 32 20 209 33 minecraft:tuff
fill 20 209 32 20 212 36 minecraft:calcite
fill 20 214 39 20 215 39 minecraft:cherry_leaves[persistent=true]
fill 20 207 22 20 210 23 minecraft:calcite
fill 20 214 25 20 215 29 minecraft:cherry_leaves[persistent=true]
fill 39 201 27 39 215 27 minecraft:stripped_dark_oak_log
fill 39 214 22 39 215 23 minecraft:cherry_leaves[persistent=true]
fill 39 201 36 39 215 36 minecraft:stripped_dark_oak_log
fill 39 204 25 39 206 30 minecraft:andesite
fill 25 201 20 25 215 20 minecraft:stripped_dark_oak_log
fill 25 210 20 25 211 20 minecraft:andesite
fill 20 205 20 20 206 20 minecraft:tuff
fill 26 205 20 29 206 20 minecraft:cobblestone
fill 22 205 20 24 206 20 minecraft:andesite
fill 31 215 20 32 215 20 minecraft:calcite
fill 27 215 39 27 215 39 minecraft:cherry_leaves[persistent=true]
fill 27 214 39 29 215 39 minecraft:cherry_leaves[persistent=true]
fill 26 206 39 28 206 39 minecraft:moss_block
fill 20 215 20 39 215 39 minecraft:polished_deepslate
fill 21 215 21 38 215 38 minecraft:air
fill 21 201 21 27 204 38 minecraft:dirt
fill 21 205 21 27 205 38 minecraft:podzol
fill 31 201 21 33 204 22 minecraft:dirt
fill 31 205 21 33 205 22 minecraft:podzol
fill 31 201 23 32 204 38 minecraft:dirt
fill 31 205 23 32 205 38 minecraft:podzol
fill 28 201 24 30 204 38 minecraft:dirt
fill 28 205 24 30 205 38 minecraft:podzol
fill 33 201 25 35 204 38 minecraft:dirt
fill 33 205 25 35 205 38 minecraft:podzol
fill 36 201 26 38 204 38 minecraft:dirt
fill 36 205 26 38 205 38 minecraft:podzol
fill 34 201 21 34 205 22 minecraft:dirt
fill 34 206 21 34 206 22 minecraft:podzol
fill 35 201 22 35 205 24 minecraft:dirt
fill 35 206 22 35 206 24 minecraft:podzol
fill 36 201 24 37 205 25 minecraft:dirt
fill 36 206 24 37 206 25 minecraft:podzol
fill 38 201 25 38 205 25 minecraft:dirt
fill 38 206 25 38 206 25 minecraft:podzol
fill 35 201 21 38 206 21 minecraft:dirt
fill 35 207 21 38 207 21 minecraft:podzol
fill 36 201 22 38 206 23 minecraft:dirt
fill 36 207 22 38 207 23 minecraft:podzol
fill 38 201 24 38 206 24 minecraft:dirt
fill 38 207 24 38 207 24 minecraft:podzol
fill 28 201 21 30 211 23 minecraft:stone_bricks
fill 28 212 21 30 212 23 minecraft:podzol
fill 33 201 23 34 212 24 minecraft:stone_bricks
fill 33 213 23 34 213 24 minecraft:podzol
execute positioned 21 206 21 run function rlk:room/prop/i_rock
execute positioned 36 206 29 run function rlk:room/prop/i_lantern2
execute positioned 36 206 32 run function rlk:room/prop/i_pillar
execute positioned 36 206 26 run function rlk:room/prop/i_pillar
execute positioned 35 206 35 run function rlk:room/prop/i_petal
execute positioned 23 206 33 run function rlk:room/prop/i_flower
execute positioned 22 206 23 run function rlk:room/prop/i_grass
execute positioned 30 206 33 run function rlk:room/prop/i_petal
execute positioned 28 206 33 run function rlk:room/prop/i_grass
execute positioned 31 206 30 run function rlk:room/prop/i_petal
execute positioned 31 206 21 run function rlk:room/prop/i_petal
execute positioned 37 206 28 run function rlk:room/prop/i_petal
setblock 28 213 21 minecraft:cherry_leaves[persistent=true] keep
setblock 28 213 23 minecraft:cherry_leaves[persistent=true] keep
setblock 30 213 21 minecraft:short_grass keep
setblock 30 213 22 minecraft:cherry_leaves[persistent=true] keep
setblock 33 214 23 minecraft:cherry_leaves[persistent=true] keep
setblock 33 214 24 minecraft:cherry_leaves[persistent=true] keep
setblock 34 214 23 minecraft:cherry_leaves[persistent=true] keep
setblock 34 214 24 minecraft:short_grass keep
