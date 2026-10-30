# 구역 건설 (normal6_6, 테마 3): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 -20 59 200 -1 minecraft:podzol
fill 40 201 -20 59 210 -1 minecraft:stone
fill 41 201 -19 58 210 -2 minecraft:air
fill 41 209 -19 58 209 -2 minecraft:light[level=15]
fill 50 200 -15 53 200 -13 minecraft:rooted_dirt
fill 40 210 -11 40 210 -7 minecraft:oak_leaves[persistent=true]
fill 40 201 -16 40 204 -11 minecraft:tuff
fill 40 209 -17 40 210 -17 minecraft:andesite
fill 40 205 -6 40 208 -1 minecraft:moss_block
fill 40 202 -5 40 204 -4 minecraft:tuff
fill 40 205 -11 40 208 -10 minecraft:cobblestone
fill 59 201 -12 59 202 -9 minecraft:andesite
fill 59 210 -11 59 210 -11 minecraft:oak_leaves[persistent=true]
fill 42 202 -20 43 205 -20 minecraft:cobblestone
fill 51 210 -20 51 210 -20 minecraft:oak_leaves[persistent=true]
fill 52 201 -20 56 202 -20 minecraft:mossy_cobblestone
fill 43 210 -1 48 210 -1 minecraft:cobblestone
fill 40 210 -20 59 210 -1 minecraft:polished_deepslate
fill 41 210 -19 58 210 -2 minecraft:air
fill 57 201 -12 58 201 -12 minecraft:podzol
fill 55 201 -11 56 201 -10 minecraft:podzol
fill 55 201 -9 55 201 -3 minecraft:podzol
fill 54 201 -5 54 201 -4 minecraft:podzol
fill 56 201 -4 56 201 -3 minecraft:podzol
fill 57 201 -3 58 201 -2 minecraft:podzol
fill 56 201 -9 56 201 -5 minecraft:dirt
fill 56 202 -9 56 202 -5 minecraft:podzol
fill 57 201 -8 58 201 -4 minecraft:dirt
fill 57 202 -8 58 202 -4 minecraft:podzol
fill 57 201 -11 58 207 -9 minecraft:stone
fill 57 208 -11 58 208 -9 minecraft:podzol
execute positioned 44 201 -8 run function rlk:room/prop/p_lantern
execute positioned 50 201 -4 run function rlk:room/prop/p_boulder_s
execute positioned 45 201 -4 run function rlk:room/prop/p_ruin_z
execute positioned 54 202 -4 run function rlk:room/prop/p_ruin_x
execute positioned 46 201 -4 run function rlk:room/prop/p_wildflower
execute positioned 41 201 -11 run function rlk:room/prop/p_grass
execute positioned 46 201 -5 run function rlk:room/prop/p_grass
execute positioned 50 201 -2 run function rlk:room/prop/p_grass
execute positioned 52 201 -7 run function rlk:room/prop/p_dandelion
execute positioned 55 202 -3 run function rlk:room/prop/p_wildflower
setblock 57 209 -10 minecraft:azalea_leaves[persistent=true] keep
setblock 57 209 -9 minecraft:short_grass keep
setblock 58 209 -11 minecraft:short_grass keep
setblock 58 209 -10 minecraft:azalea_leaves[persistent=true] keep
