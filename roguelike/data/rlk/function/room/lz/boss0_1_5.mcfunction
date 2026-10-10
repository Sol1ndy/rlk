# 구역 건설 (boss0_1, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 0 -1 200 19 minecraft:red_sand
fill -20 201 0 -1 210 19 minecraft:smooth_sandstone
fill -19 201 1 -2 210 18 minecraft:air
fill -19 209 1 -2 209 18 minecraft:light[level=15]
fill -13 200 7 -10 200 10 minecraft:cut_sandstone
fill -9 200 4 -8 200 5 minecraft:sandstone
fill -8 200 2 -4 200 5 minecraft:cut_sandstone
fill -20 204 14 -20 205 17 minecraft:smooth_red_sandstone
fill -20 204 12 -20 207 15 minecraft:sandstone
fill -20 205 2 -20 207 4 minecraft:chiseled_sandstone
fill -20 202 9 -20 203 14 minecraft:red_sandstone
fill -20 202 10 -20 203 14 minecraft:chiseled_sandstone
fill -20 203 14 -20 206 14 minecraft:red_sandstone
fill -1 201 4 -1 202 5 minecraft:cut_sandstone
fill -1 210 11 -1 210 13 minecraft:cut_sandstone
fill -1 206 0 -1 209 3 minecraft:sandstone
fill -1 205 9 -1 205 13 minecraft:terracotta
fill -19 206 0 -17 209 0 minecraft:red_sandstone
fill -15 203 0 -12 203 0 minecraft:sandstone
fill -7 203 0 -5 204 0 minecraft:cut_sandstone
fill -14 201 0 -12 202 0 minecraft:smooth_red_sandstone
fill -19 202 19 -14 202 19 minecraft:cut_sandstone
fill -20 208 19 -20 208 19 minecraft:sandstone
fill -17 209 19 -13 209 19 minecraft:orange_terracotta
fill -13 206 19 -10 206 19 minecraft:sandstone
fill -20 210 0 -1 210 19 minecraft:polished_deepslate
fill -19 210 1 -2 210 18 minecraft:air
fill -15 201 11 -15 201 14 minecraft:red_sand
fill -17 201 12 -16 201 13 minecraft:red_sand
fill -17 201 14 -17 201 15 minecraft:red_sand
fill -14 201 15 -7 201 15 minecraft:red_sand
fill -8 201 16 -7 201 18 minecraft:red_sand
fill -16 201 14 -16 201 18 minecraft:sandstone
fill -16 202 14 -16 202 18 minecraft:red_sand
fill -15 201 15 -15 201 18 minecraft:sandstone
fill -15 202 15 -15 202 18 minecraft:red_sand
fill -17 201 16 -17 201 18 minecraft:sandstone
fill -17 202 16 -17 202 18 minecraft:red_sand
fill -14 201 16 -9 201 18 minecraft:sandstone
fill -14 202 16 -9 202 18 minecraft:red_sand
fill -17 201 7 -16 205 8 minecraft:terracotta
fill -17 206 7 -16 206 8 minecraft:red_sand
fill -19 201 13 -18 206 13 minecraft:smooth_red_sandstone
fill -19 207 13 -18 207 13 minecraft:red_sand
fill -19 201 14 -19 206 18 minecraft:smooth_red_sandstone
fill -19 207 14 -19 207 18 minecraft:red_sand
fill -18 201 18 -18 206 18 minecraft:smooth_red_sandstone
fill -18 207 18 -18 207 18 minecraft:red_sand
fill -18 201 14 -18 206 17 minecraft:terracotta
fill -18 207 14 -18 207 17 minecraft:red_sand
execute positioned -5 201 11 run function rlk:room/prop/sd_pots
execute positioned -13 202 15 run function rlk:room/prop/sd_rock_s
execute positioned -9 201 5 run function rlk:room/prop/sd_dry
execute positioned -2 201 14 run function rlk:room/prop/sd_bush
execute positioned -8 201 8 run function rlk:room/prop/sd_bush
execute positioned -8 201 11 run function rlk:room/prop/sd_dry
execute positioned -19 201 5 run function rlk:room/prop/sd_dry
execute positioned -14 201 3 run function rlk:room/prop/sd_dry
execute positioned -14 201 7 run function rlk:room/prop/sd_bush
setblock -19 208 14 minecraft:dead_bush keep
setblock -19 208 17 minecraft:dead_bush keep
setblock -18 208 13 minecraft:dead_bush keep
setblock -18 208 17 minecraft:dead_bush keep
setblock -17 207 7 minecraft:dead_bush keep
