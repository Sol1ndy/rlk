# 구역 건설 (normal13_7, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -20 200 -60 -1 200 -41 minecraft:red_sand
fill -20 201 -60 -1 210 -41 minecraft:smooth_sandstone
fill -19 201 -59 -2 210 -42 minecraft:air
fill -19 209 -59 -2 209 -42 minecraft:light[level=15]
fill -10 200 -53 -7 200 -51 minecraft:cut_sandstone
fill -11 200 -45 -10 200 -44 minecraft:cut_sandstone
fill -20 201 -52 -20 204 -48 minecraft:cut_sandstone
fill -20 208 -49 -20 208 -46 minecraft:smooth_red_sandstone
fill -20 205 -54 -20 208 -53 minecraft:red_sandstone
fill -1 206 -47 -1 207 -44 minecraft:orange_terracotta
fill -1 204 -52 -1 206 -48 minecraft:sandstone
fill -1 205 -51 -1 206 -47 minecraft:smooth_red_sandstone
fill -1 202 -43 -1 204 -41 minecraft:smooth_red_sandstone
fill -1 210 -54 -1 210 -50 minecraft:sandstone
fill -1 201 -54 -1 201 -52 minecraft:red_sandstone
fill -13 201 -60 -8 201 -60 minecraft:smooth_red_sandstone
fill -20 203 -60 -20 205 -60 minecraft:smooth_red_sandstone
fill -16 204 -60 -13 205 -60 minecraft:red_sandstone
fill -10 201 -60 -6 202 -60 minecraft:orange_terracotta
fill -10 207 -60 -10 209 -60 minecraft:red_sandstone
fill -15 203 -60 -10 204 -60 minecraft:red_sandstone
fill -5 207 -41 -2 207 -41 minecraft:smooth_red_sandstone
fill -5 201 -41 -4 202 -41 minecraft:smooth_red_sandstone
fill -12 210 -41 -7 210 -41 minecraft:terracotta
fill -20 210 -60 -1 210 -41 minecraft:polished_deepslate
fill -19 210 -59 -2 210 -42 minecraft:air
fill -19 201 -54 -18 201 -42 minecraft:red_sand
fill -17 201 -46 -17 201 -43 minecraft:red_sand
fill -14 201 -59 -13 205 -59 minecraft:smooth_red_sandstone
fill -14 206 -59 -13 206 -59 minecraft:red_sand
fill -12 201 -58 -9 205 -58 minecraft:smooth_red_sandstone
fill -12 206 -58 -9 206 -58 minecraft:red_sand
fill -12 201 -59 -9 205 -59 minecraft:terracotta
fill -12 206 -59 -9 206 -59 minecraft:red_sand
fill -14 201 -58 -13 205 -58 minecraft:terracotta
fill -14 206 -58 -13 206 -58 minecraft:red_sand
execute positioned -16 201 -42 run function rlk:room/prop/sd_dry
execute positioned -14 201 -44 run function rlk:room/prop/sd_bush
execute positioned -5 201 -51 run function rlk:room/prop/sd_bush
execute positioned -10 201 -51 run function rlk:room/prop/sd_dry
execute positioned -3 201 -46 run function rlk:room/prop/sd_dry
execute positioned -17 201 -54 run function rlk:room/prop/sd_dry
setblock -13 207 -58 minecraft:dead_bush keep
setblock -12 207 -59 minecraft:dead_bush keep
setblock -11 207 -58 minecraft:dead_bush keep
setblock -9 207 -58 minecraft:dead_bush keep
