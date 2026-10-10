# 구역 건설 (boss6_1, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill 0 200 0 19 200 19 minecraft:red_sand
fill 0 201 0 19 210 19 minecraft:smooth_sandstone
fill 1 201 1 18 210 18 minecraft:air
fill 1 209 1 18 209 18 minecraft:light[level=15]
fill 7 200 8 11 200 11 minecraft:sandstone
fill 7 200 12 10 200 14 minecraft:smooth_sandstone
fill 11 200 2 13 200 3 minecraft:smooth_sandstone
fill 0 209 13 0 210 15 minecraft:red_sandstone
fill 0 210 12 0 210 14 minecraft:red_sandstone
fill 0 208 5 0 209 6 minecraft:sandstone
fill 0 205 11 0 207 12 minecraft:cut_sandstone
fill 0 204 13 0 207 14 minecraft:terracotta
fill 0 206 9 0 208 10 minecraft:cut_sandstone
fill 19 201 0 19 201 5 minecraft:sandstone
fill 19 201 10 19 203 12 minecraft:cut_sandstone
fill 19 204 6 19 204 7 minecraft:cut_sandstone
fill 19 201 12 19 204 14 minecraft:smooth_red_sandstone
fill 2 205 0 7 205 0 minecraft:red_sandstone
fill 11 210 0 14 210 0 minecraft:sandstone
fill 3 203 0 7 206 0 minecraft:sandstone
fill 12 201 0 12 204 0 minecraft:sandstone
fill 0 208 19 2 210 19 minecraft:smooth_red_sandstone
fill 3 203 19 7 205 19 minecraft:sandstone
fill 4 201 19 4 203 19 minecraft:cut_sandstone
fill 0 210 0 19 210 19 minecraft:polished_deepslate
fill 1 210 1 18 210 18 minecraft:air
fill 16 201 1 18 201 10 minecraft:red_sand
fill 15 201 6 15 201 12 minecraft:red_sand
fill 16 201 11 16 201 13 minecraft:red_sand
fill 17 201 11 17 206 11 minecraft:smooth_red_sandstone
fill 17 207 11 17 207 11 minecraft:red_sand
fill 18 201 11 18 206 13 minecraft:terracotta
fill 18 207 11 18 207 13 minecraft:red_sand
fill 17 201 12 17 206 13 minecraft:terracotta
fill 17 207 12 17 207 13 minecraft:red_sand
fill 3 201 13 4 207 14 minecraft:smooth_red_sandstone
fill 3 208 13 4 208 14 minecraft:red_sand
execute positioned 13 201 15 run function rlk:room/prop/sd_obelisk
execute positioned 5 201 8 run function rlk:room/prop/sd_palm
execute positioned 14 201 1 run function rlk:room/prop/sd_bush
execute positioned 13 201 12 run function rlk:room/prop/sd_dry
execute positioned 14 201 18 run function rlk:room/prop/sd_dry
execute positioned 5 201 4 run function rlk:room/prop/sd_dry
execute positioned 13 201 1 run function rlk:room/prop/sd_dry
execute positioned 18 202 9 run function rlk:room/prop/sd_dry
execute positioned 5 201 5 run function rlk:room/prop/sd_dry
execute positioned 10 201 10 run function rlk:room/prop/sd_dry
setblock 4 209 13 minecraft:dead_bush keep
setblock 17 208 11 minecraft:dead_bush keep
setblock 18 208 11 minecraft:dead_bush keep
setblock 18 208 12 minecraft:dead_bush keep
