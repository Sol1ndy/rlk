# 구역 건설 (first0_2, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:red_sand
fill 0 201 0 19 210 19 minecraft:smooth_sandstone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 1 200 8 3 200 10 minecraft:sand
fill 13 200 11 14 200 13 minecraft:sand
fill 12 200 11 15 200 13 minecraft:smooth_sandstone
fill 0 201 0 0 201 1 minecraft:terracotta
fill 0 205 2 0 206 4 minecraft:orange_terracotta
fill 0 203 4 0 203 4 minecraft:smooth_red_sandstone
fill 0 206 3 0 206 8 minecraft:sandstone
fill 19 208 13 19 209 15 minecraft:sandstone
fill 19 201 11 19 204 11 minecraft:chiseled_sandstone
fill 19 204 6 19 207 6 minecraft:terracotta
fill 19 207 2 19 208 5 minecraft:sandstone
fill 19 210 10 19 210 10 minecraft:cut_sandstone
fill 19 207 13 19 210 15 minecraft:orange_terracotta
fill 7 203 0 11 205 0 minecraft:smooth_red_sandstone
fill 3 210 0 4 210 0 minecraft:terracotta
fill 5 208 0 10 209 0 minecraft:sandstone
fill 19 210 0 19 210 0 minecraft:terracotta
fill 14 208 19 16 210 19 minecraft:terracotta
fill 12 201 19 15 201 19 minecraft:smooth_red_sandstone
fill 11 207 19 12 208 19 minecraft:cut_sandstone
fill 17 203 19 18 204 19 minecraft:sandstone
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 1 201 16 3 201 16 minecraft:red_sand
fill 3 201 17 3 201 18 minecraft:red_sand
fill 1 201 17 2 201 18 minecraft:sandstone
fill 1 202 17 2 202 18 minecraft:red_sand
fill 16 201 1 18 206 1 minecraft:smooth_red_sandstone
fill 16 207 1 18 207 1 minecraft:red_sand
fill 16 201 2 17 206 3 minecraft:smooth_red_sandstone
fill 16 207 2 17 207 3 minecraft:red_sand
fill 18 201 2 18 206 3 minecraft:terracotta
fill 18 207 2 18 207 3 minecraft:red_sand
fill 11 201 3 11 207 4 minecraft:smooth_red_sandstone
fill 11 208 3 11 208 4 minecraft:red_sand
fill 12 201 4 12 207 4 minecraft:smooth_red_sandstone
fill 12 208 4 12 208 4 minecraft:red_sand
fill 12 201 3 12 207 3 minecraft:terracotta
fill 12 208 3 12 208 3 minecraft:red_sand
execute positioned 1 203 18 run function rlk:room/prop/sd_rock_s
execute positioned 17 201 10 run function rlk:room/prop/sd_rock
execute positioned 6 201 1 run function rlk:room/prop/sd_ruin_z
execute positioned 13 201 1 run function rlk:room/prop/sd_dry
execute positioned 3 201 12 run function rlk:room/prop/sd_dry
execute positioned 8 201 6 run function rlk:room/prop/sd_dry
execute positioned 6 201 9 run function rlk:room/prop/sd_bush
execute positioned 11 201 6 run function rlk:room/prop/sd_bush
execute positioned 14 201 4 run function rlk:room/prop/sd_dry
setblock 11 209 3 minecraft:dead_bush keep
setblock 11 209 4 minecraft:dead_bush keep
setblock 12 209 3 minecraft:dead_bush keep
setblock 16 208 1 minecraft:dead_bush keep
setblock 16 208 2 minecraft:dead_bush keep
setblock 18 208 1 minecraft:dead_bush keep
setblock 18 208 3 minecraft:dead_bush keep
