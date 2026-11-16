# 구역 건설 (levelup7_3, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 20 39 200 39 minecraft:red_sand
fill 20 201 20 39 210 39 minecraft:smooth_sandstone
fill 21 201 21 38 210 38 minecraft:air
fill 21 209 21 38 209 38 minecraft:light[level=15]
fill 24 200 26 26 200 27 minecraft:sand
fill 33 200 26 36 200 27 minecraft:sandstone
fill 23 200 29 24 200 32 minecraft:sand
fill 20 201 30 20 202 33 minecraft:cut_sandstone
fill 20 206 32 20 206 37 minecraft:orange_terracotta
fill 20 201 26 20 202 27 minecraft:cut_sandstone
fill 20 201 23 20 202 25 minecraft:cut_sandstone
fill 20 207 35 20 207 39 minecraft:terracotta
fill 39 206 23 39 207 26 minecraft:orange_terracotta
fill 39 203 34 39 206 35 minecraft:cut_sandstone
fill 39 202 29 39 202 31 minecraft:smooth_red_sandstone
fill 20 210 20 22 210 20 minecraft:sandstone
fill 20 209 20 22 210 20 minecraft:orange_terracotta
fill 29 204 20 29 204 20 minecraft:smooth_red_sandstone
fill 27 201 39 30 202 39 minecraft:sandstone
fill 33 207 39 33 210 39 minecraft:terracotta
fill 26 206 39 30 208 39 minecraft:red_sandstone
fill 30 209 39 33 210 39 minecraft:sandstone
fill 33 210 39 34 210 39 minecraft:sandstone
fill 20 210 20 39 210 39 minecraft:polished_deepslate
fill 21 210 21 38 210 38 minecraft:air
fill 34 201 21 34 201 22 minecraft:red_sand
fill 35 201 22 35 201 24 minecraft:red_sand
fill 36 201 24 37 201 25 minecraft:red_sand
fill 38 201 25 38 201 25 minecraft:red_sand
fill 35 201 21 38 201 21 minecraft:sandstone
fill 35 202 21 38 202 21 minecraft:red_sand
fill 36 201 22 38 201 23 minecraft:sandstone
fill 36 202 22 38 202 23 minecraft:red_sand
fill 38 201 24 38 201 24 minecraft:sandstone
fill 38 202 24 38 202 24 minecraft:red_sand
fill 28 201 21 30 206 23 minecraft:smooth_red_sandstone
fill 28 207 21 30 207 23 minecraft:red_sand
fill 33 201 23 34 207 24 minecraft:smooth_red_sandstone
fill 33 208 23 34 208 24 minecraft:red_sand
execute positioned 35 201 28 run function rlk:room/prop/sd_rock
execute positioned 35 203 21 run function rlk:room/prop/sd_obelisk
execute positioned 38 203 21 run function rlk:room/prop/sd_dry
execute positioned 31 201 32 run function rlk:room/prop/sd_dry
execute positioned 25 201 35 run function rlk:room/prop/sd_bush
execute positioned 37 201 29 run function rlk:room/prop/sd_dry
execute positioned 22 201 35 run function rlk:room/prop/sd_bush
execute positioned 26 201 30 run function rlk:room/prop/sd_bush
execute positioned 32 201 27 run function rlk:room/prop/sd_bush
setblock 28 208 21 minecraft:dead_bush keep
setblock 28 208 22 minecraft:dead_bush keep
setblock 29 208 23 minecraft:dead_bush keep
setblock 33 209 23 minecraft:dead_bush keep
setblock 34 209 23 minecraft:dead_bush keep
setblock 34 209 24 minecraft:dead_bush keep
