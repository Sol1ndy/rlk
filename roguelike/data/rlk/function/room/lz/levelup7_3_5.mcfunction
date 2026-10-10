# 구역 건설 (levelup7_3, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:red_sand
fill 20 201 20 39 215 39 minecraft:smooth_sandstone
fill 21 201 21 38 215 38 minecraft:air
fill 21 214 21 38 214 38 minecraft:light[level=15]
fill 24 205 26 26 205 27 minecraft:sand
fill 33 205 26 36 205 27 minecraft:sandstone
fill 23 205 29 24 205 32 minecraft:sand
fill 20 205 30 20 207 33 minecraft:cut_sandstone
fill 20 211 32 20 211 37 minecraft:orange_terracotta
fill 20 205 26 20 207 27 minecraft:cut_sandstone
fill 20 206 23 20 207 25 minecraft:cut_sandstone
fill 20 212 35 20 212 39 minecraft:terracotta
fill 39 211 23 39 212 26 minecraft:orange_terracotta
fill 39 208 34 39 211 35 minecraft:cut_sandstone
fill 39 204 31 39 205 34 minecraft:sandstone
fill 39 207 29 39 207 31 minecraft:smooth_red_sandstone
fill 20 215 20 22 215 20 minecraft:sandstone
fill 20 214 20 22 215 20 minecraft:orange_terracotta
fill 29 209 20 29 209 20 minecraft:smooth_red_sandstone
fill 27 206 39 30 207 39 minecraft:sandstone
fill 33 212 39 33 215 39 minecraft:terracotta
fill 20 202 39 21 205 39 minecraft:chiseled_sandstone
fill 26 211 39 30 213 39 minecraft:red_sandstone
fill 30 214 39 33 215 39 minecraft:sandstone
fill 33 215 39 34 215 39 minecraft:sandstone
fill 20 215 20 39 215 39 minecraft:polished_deepslate
fill 21 215 21 38 215 38 minecraft:air
fill 21 201 21 27 204 38 minecraft:sandstone
fill 21 205 21 27 205 38 minecraft:red_sand
fill 31 201 21 33 204 22 minecraft:sandstone
fill 31 205 21 33 205 22 minecraft:red_sand
fill 31 201 23 32 204 38 minecraft:sandstone
fill 31 205 23 32 205 38 minecraft:red_sand
fill 28 201 24 30 204 38 minecraft:sandstone
fill 28 205 24 30 205 38 minecraft:red_sand
fill 33 201 25 35 204 38 minecraft:sandstone
fill 33 205 25 35 205 38 minecraft:red_sand
fill 36 201 26 38 204 38 minecraft:sandstone
fill 36 205 26 38 205 38 minecraft:red_sand
fill 34 201 21 34 205 22 minecraft:sandstone
fill 34 206 21 34 206 22 minecraft:red_sand
fill 35 201 22 35 205 24 minecraft:sandstone
fill 35 206 22 35 206 24 minecraft:red_sand
fill 36 201 24 37 205 25 minecraft:sandstone
fill 36 206 24 37 206 25 minecraft:red_sand
fill 38 201 25 38 205 25 minecraft:sandstone
fill 38 206 25 38 206 25 minecraft:red_sand
fill 35 201 21 38 206 21 minecraft:sandstone
fill 35 207 21 38 207 21 minecraft:red_sand
fill 36 201 22 38 206 23 minecraft:sandstone
fill 36 207 22 38 207 23 minecraft:red_sand
fill 38 201 24 38 206 24 minecraft:sandstone
fill 38 207 24 38 207 24 minecraft:red_sand
fill 28 201 21 30 211 23 minecraft:smooth_red_sandstone
fill 28 212 21 30 212 23 minecraft:red_sand
fill 33 201 23 34 212 24 minecraft:smooth_red_sandstone
fill 33 213 23 34 213 24 minecraft:red_sand
execute positioned 35 206 28 run function rlk:room/prop/sd_rock
execute positioned 35 208 21 run function rlk:room/prop/sd_obelisk
execute positioned 38 208 21 run function rlk:room/prop/sd_dry
execute positioned 31 206 32 run function rlk:room/prop/sd_dry
execute positioned 25 206 35 run function rlk:room/prop/sd_bush
execute positioned 37 206 29 run function rlk:room/prop/sd_dry
execute positioned 22 206 35 run function rlk:room/prop/sd_bush
execute positioned 26 206 30 run function rlk:room/prop/sd_bush
execute positioned 32 206 27 run function rlk:room/prop/sd_bush
setblock 28 213 21 minecraft:dead_bush keep
setblock 28 213 22 minecraft:dead_bush keep
setblock 29 213 23 minecraft:dead_bush keep
setblock 33 214 23 minecraft:dead_bush keep
setblock 34 214 23 minecraft:dead_bush keep
setblock 34 214 24 minecraft:dead_bush keep
