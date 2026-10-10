# 구역 건설 (first5_2, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 20 200 0 39 200 19 minecraft:red_sand
fill 20 201 0 39 210 19 minecraft:smooth_sandstone
fill 21 201 1 38 210 18 minecraft:air
fill 21 209 1 38 209 18 minecraft:light[level=15]
fill 23 200 12 24 200 14 minecraft:cut_sandstone
fill 20 202 1 20 205 3 minecraft:smooth_red_sandstone
fill 20 207 10 20 210 12 minecraft:orange_terracotta
fill 20 205 3 20 205 6 minecraft:cut_sandstone
fill 20 209 3 20 210 5 minecraft:red_sandstone
fill 39 204 18 39 204 19 minecraft:red_sandstone
fill 39 203 6 39 205 7 minecraft:orange_terracotta
fill 39 207 17 39 208 18 minecraft:chiseled_sandstone
fill 38 208 0 39 208 0 minecraft:cut_sandstone
fill 22 208 0 23 210 0 minecraft:smooth_red_sandstone
fill 33 206 0 36 207 0 minecraft:sandstone
fill 34 207 0 36 208 0 minecraft:sandstone
fill 30 202 19 34 205 19 minecraft:cut_sandstone
fill 30 209 19 32 210 19 minecraft:orange_terracotta
fill 26 203 19 29 206 19 minecraft:cut_sandstone
fill 33 210 19 38 210 19 minecraft:smooth_red_sandstone
fill 30 204 19 32 204 19 minecraft:chiseled_sandstone
fill 28 202 19 32 202 19 minecraft:smooth_red_sandstone
fill 20 210 0 39 210 19 minecraft:polished_deepslate
fill 21 210 1 38 210 18 minecraft:air
fill 25 201 1 34 201 1 minecraft:red_sand
fill 26 201 2 34 201 2 minecraft:red_sand
fill 21 201 3 32 201 3 minecraft:red_sand
fill 26 201 4 32 201 5 minecraft:red_sand
fill 35 201 4 37 201 4 minecraft:red_sand
fill 33 201 5 36 201 5 minecraft:red_sand
fill 35 201 6 35 201 6 minecraft:red_sand
fill 21 201 1 24 201 2 minecraft:sandstone
fill 21 202 1 24 202 2 minecraft:red_sand
fill 25 201 2 25 201 2 minecraft:sandstone
fill 25 202 2 25 202 2 minecraft:red_sand
fill 35 201 1 38 207 3 minecraft:smooth_red_sandstone
fill 35 208 1 38 208 3 minecraft:red_sand
fill 33 201 3 34 207 3 minecraft:smooth_red_sandstone
fill 33 208 3 34 208 3 minecraft:red_sand
fill 33 201 4 34 207 4 minecraft:terracotta
fill 33 208 4 34 208 4 minecraft:red_sand
execute positioned 26 202 3 run function rlk:room/prop/sd_gate_x
execute positioned 35 201 12 run function rlk:room/prop/sd_dry
execute positioned 32 201 16 run function rlk:room/prop/sd_bush
execute positioned 24 201 11 run function rlk:room/prop/sd_bush
execute positioned 25 203 2 run function rlk:room/prop/sd_dry
execute positioned 21 201 6 run function rlk:room/prop/sd_dry
setblock 33 209 4 minecraft:dead_bush keep
setblock 34 209 3 minecraft:dead_bush keep
setblock 35 209 3 minecraft:dead_bush keep
setblock 37 209 2 minecraft:dead_bush keep
setblock 38 209 3 minecraft:dead_bush keep
