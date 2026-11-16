# 구역 건설 (normal3_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 40 200 40 59 200 59 minecraft:podzol
fill 40 201 40 59 210 59 minecraft:stone
fill 41 201 41 58 210 58 minecraft:air
fill 41 209 41 58 209 58 minecraft:light[level=15]
fill 54 200 52 58 200 54 minecraft:moss_block
fill 57 200 49 58 200 51 minecraft:moss_block
fill 53 200 51 57 200 52 minecraft:moss_block
fill 40 204 56 40 204 56 minecraft:diorite
fill 40 210 41 40 210 42 minecraft:birch_leaves[persistent=true]
fill 40 209 42 40 210 47 minecraft:birch_leaves[persistent=true]
fill 40 210 50 40 210 51 minecraft:calcite
fill 40 204 43 40 206 48 minecraft:diorite
fill 59 210 49 59 210 52 minecraft:oak_leaves[persistent=true]
fill 59 201 42 59 202 47 minecraft:calcite
fill 59 209 44 59 210 45 minecraft:birch_leaves[persistent=true]
fill 59 201 45 59 202 46 minecraft:moss_block
fill 59 207 46 59 208 47 minecraft:prismarine
fill 51 201 40 54 204 40 minecraft:moss_block
fill 46 206 40 46 206 40 minecraft:dark_prismarine
fill 44 202 40 48 205 40 minecraft:calcite
fill 57 207 59 58 208 59 minecraft:moss_block
fill 49 209 59 54 210 59 minecraft:prismarine
fill 45 209 59 45 210 59 minecraft:oak_leaves[persistent=true]
fill 42 210 59 47 210 59 minecraft:birch_leaves[persistent=true]
fill 40 210 40 59 210 59 minecraft:polished_deepslate
fill 41 210 41 58 210 58 minecraft:air
fill 43 201 41 43 201 45 minecraft:podzol
fill 44 201 46 45 201 46 minecraft:podzol
fill 45 201 47 45 201 51 minecraft:podzol
fill 41 201 51 44 201 51 minecraft:podzol
fill 41 201 41 42 201 42 minecraft:dirt
fill 41 202 41 42 202 42 minecraft:podzol
fill 42 201 43 42 201 45 minecraft:dirt
fill 42 202 43 42 202 45 minecraft:podzol
fill 43 201 46 43 201 46 minecraft:dirt
fill 43 202 46 43 202 46 minecraft:podzol
fill 44 201 47 44 201 50 minecraft:dirt
fill 44 202 47 44 202 50 minecraft:podzol
fill 41 201 48 41 201 50 minecraft:dirt
fill 41 202 48 41 202 50 minecraft:podzol
fill 42 201 49 43 201 50 minecraft:dirt
fill 42 202 49 43 202 50 minecraft:podzol
fill 41 201 43 41 202 47 minecraft:dirt
fill 41 203 43 41 203 47 minecraft:podzol
fill 42 201 46 42 202 48 minecraft:dirt
fill 42 203 46 42 203 48 minecraft:podzol
fill 43 201 47 43 202 48 minecraft:dirt
fill 43 203 47 43 203 48 minecraft:podzol
fill 51 201 57 53 207 58 minecraft:diorite
fill 51 208 57 53 208 58 minecraft:podzol
fill 55 199 49 56 199 51 minecraft:clay
fill 55 200 49 56 200 51 minecraft:water
fill 41 199 52 45 199 53 minecraft:clay
fill 41 200 52 45 200 53 minecraft:water
fill 55 200 48 55 200 48 minecraft:sand
fill 57 200 48 57 200 52 minecraft:sand
fill 41 200 54 45 200 54 minecraft:sand
setblock 43 200 52 minecraft:seagrass
setblock 44 200 53 minecraft:seagrass
execute positioned 43 202 45 run function rlk:room/prop/fo_lamp
execute positioned 56 201 45 run function rlk:room/prop/fo_lamp
execute positioned 50 201 55 run function rlk:room/prop/fo_lamp
execute positioned 55 201 55 run function rlk:room/prop/fo_bench
execute positioned 51 201 47 run function rlk:room/prop/fo_flower
execute positioned 41 204 45 run function rlk:room/prop/fo_white
execute positioned 58 201 58 run function rlk:room/prop/p_grass
execute positioned 51 201 42 run function rlk:room/prop/fo_flower
execute positioned 45 201 41 run function rlk:room/prop/p_grass
execute positioned 50 201 55 run function rlk:room/prop/fo_flower
execute positioned 47 201 46 run function rlk:room/prop/fo_flower
execute positioned 48 201 57 run function rlk:room/prop/fo_flower
execute positioned 43 202 51 run function rlk:room/prop/p_grass
execute positioned 42 201 57 run function rlk:room/prop/p_grass
setblock 51 209 57 minecraft:short_grass keep
setblock 51 209 58 minecraft:short_grass keep
setblock 52 209 57 minecraft:birch_leaves[persistent=true] keep
setblock 52 209 58 minecraft:short_grass keep
setblock 53 209 58 minecraft:birch_leaves[persistent=true] keep
