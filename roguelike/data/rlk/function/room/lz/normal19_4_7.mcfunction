# 구역 건설 (normal19_4, 테마 7): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -60 200 -60 -41 200 -41 minecraft:podzol
fill -60 201 -60 -41 210 -41 minecraft:stone
fill -59 201 -59 -42 210 -42 minecraft:air
fill -59 209 -59 -42 209 -42 minecraft:light[level=15]
fill -49 200 -49 -46 200 -46 minecraft:moss_block
fill -45 200 -52 -44 200 -51 minecraft:gravel
fill -50 200 -46 -48 200 -43 minecraft:gravel
fill -60 208 -52 -60 210 -49 minecraft:calcite
fill -60 204 -56 -60 205 -52 minecraft:moss_block
fill -60 203 -58 -60 205 -56 minecraft:calcite
fill -41 205 -49 -41 205 -46 minecraft:diorite
fill -41 209 -47 -41 210 -42 minecraft:moss_block
fill -41 202 -58 -41 204 -57 minecraft:calcite
fill -41 210 -51 -41 210 -46 minecraft:birch_leaves[persistent=true]
fill -53 201 -60 -52 201 -60 minecraft:moss_block
fill -57 208 -60 -53 210 -60 minecraft:calcite
fill -58 209 -60 -55 210 -60 minecraft:oak_leaves[persistent=true]
fill -41 207 -60 -41 207 -60 minecraft:moss_block
fill -54 204 -60 -50 205 -60 minecraft:moss_block
fill -45 204 -41 -41 205 -41 minecraft:prismarine
fill -44 201 -41 -41 203 -41 minecraft:moss_block
fill -48 210 -41 -45 210 -41 minecraft:birch_leaves[persistent=true]
fill -48 209 -41 -44 210 -41 minecraft:diorite
fill -60 210 -60 -41 210 -41 minecraft:polished_deepslate
fill -59 210 -59 -42 210 -42 minecraft:air
fill -57 201 -59 -53 201 -59 minecraft:podzol
fill -57 201 -58 -56 201 -58 minecraft:podzol
fill -53 201 -58 -53 201 -55 minecraft:podzol
fill -59 201 -57 -57 201 -56 minecraft:podzol
fill -54 201 -55 -54 201 -55 minecraft:podzol
fill -55 201 -54 -55 201 -48 minecraft:podzol
fill -59 201 -48 -56 201 -47 minecraft:podzol
fill -55 201 -58 -54 201 -56 minecraft:dirt
fill -55 202 -58 -54 202 -56 minecraft:podzol
fill -56 201 -57 -56 201 -51 minecraft:dirt
fill -56 202 -57 -56 202 -51 minecraft:podzol
fill -59 201 -55 -57 201 -51 minecraft:dirt
fill -59 202 -55 -57 202 -51 minecraft:podzol
fill -55 201 -55 -55 201 -55 minecraft:dirt
fill -55 202 -55 -55 202 -55 minecraft:podzol
fill -59 201 -50 -58 201 -49 minecraft:dirt
fill -59 202 -50 -58 202 -49 minecraft:podzol
fill -42 201 -48 -42 206 -45 minecraft:calcite
fill -42 207 -48 -42 207 -45 minecraft:podzol
fill -42 201 -49 -42 206 -49 minecraft:diorite
fill -42 207 -49 -42 207 -49 minecraft:podzol
fill -57 201 -50 -56 207 -49 minecraft:calcite
fill -57 208 -50 -56 208 -49 minecraft:podzol
fill -51 186 -60 -41 199 -56 minecraft:stone
fill -50 186 -59 -42 186 -57 minecraft:clay
fill -50 187 -59 -42 188 -57 minecraft:water
fill -50 189 -59 -42 201 -57 minecraft:air
fill -59 199 -46 -57 199 -42 minecraft:clay
fill -59 200 -46 -57 200 -42 minecraft:water
setblock -59 200 -43 minecraft:seagrass
setblock -57 200 -46 minecraft:seagrass
execute positioned -52 201 -59 run function rlk:room/prop/fo_rock
execute positioned -46 201 -56 run function rlk:room/prop/fo_lamp
execute positioned -56 203 -55 run function rlk:room/prop/fo_rock_s
execute positioned -44 201 -49 run function rlk:room/prop/fo_flower
execute positioned -43 201 -43 run function rlk:room/prop/fo_white
execute positioned -53 201 -42 run function rlk:room/prop/fo_white
execute positioned -53 201 -49 run function rlk:room/prop/p_grass
execute positioned -58 202 -56 run function rlk:room/prop/fo_white
execute positioned -56 203 -51 run function rlk:room/prop/p_grass
execute positioned -48 201 -54 run function rlk:room/prop/p_grass
execute positioned -59 203 -54 run function rlk:room/prop/p_grass
execute positioned -56 202 -58 run function rlk:room/prop/p_grass
execute positioned -50 201 -53 run function rlk:room/prop/fo_white
setblock -57 209 -50 minecraft:short_grass keep
setblock -57 209 -49 minecraft:birch_leaves[persistent=true] keep
setblock -56 209 -49 minecraft:short_grass keep
setblock -42 208 -47 minecraft:short_grass keep
setblock -42 208 -45 minecraft:short_grass keep
