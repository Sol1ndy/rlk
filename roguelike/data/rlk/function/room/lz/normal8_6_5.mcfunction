# 구역 건설 (normal8_6, 테마 5 사막): 칸(바닥 · 벽) → 바닥 · 벽 무늬 → 지형 → 낙사 구간 → 프롭. build/layouts3.py 가 만듦
fill -40 200 20 -21 200 39 minecraft:red_sand
fill -40 201 20 -21 210 39 minecraft:smooth_sandstone
fill -39 201 21 -22 210 38 minecraft:air
fill -39 209 21 -22 209 38 minecraft:light[level=15]
fill -24 200 25 -22 200 26 minecraft:cut_sandstone
fill -25 200 37 -24 200 38 minecraft:sandstone
fill -40 202 35 -40 202 35 minecraft:sandstone
fill -40 201 30 -40 201 34 minecraft:sandstone
fill -40 208 21 -40 208 22 minecraft:smooth_red_sandstone
fill -21 209 33 -21 210 33 minecraft:sandstone
fill -21 208 29 -21 210 33 minecraft:chiseled_sandstone
fill -21 206 31 -21 209 35 minecraft:smooth_red_sandstone
fill -26 208 20 -25 208 20 minecraft:sandstone
fill -21 201 20 -21 201 20 minecraft:smooth_red_sandstone
fill -39 210 20 -35 210 20 minecraft:smooth_red_sandstone
fill -39 205 20 -37 208 20 minecraft:terracotta
fill -38 209 39 -35 210 39 minecraft:sandstone
fill -27 206 39 -24 206 39 minecraft:sandstone
fill -40 210 20 -21 210 39 minecraft:polished_deepslate
fill -39 210 21 -22 210 38 minecraft:air
fill -39 201 21 -36 201 21 minecraft:red_sand
fill -30 201 21 -29 201 21 minecraft:red_sand
fill -39 201 22 -37 201 22 minecraft:red_sand
fill -29 201 22 -28 201 25 minecraft:red_sand
fill -39 201 23 -38 201 30 minecraft:red_sand
fill -37 201 25 -37 201 26 minecraft:red_sand
fill -34 201 25 -30 201 25 minecraft:red_sand
fill -36 201 26 -35 201 26 minecraft:red_sand
fill -35 201 21 -31 201 24 minecraft:sandstone
fill -35 202 21 -31 202 24 minecraft:red_sand
fill -36 201 22 -36 201 22 minecraft:sandstone
fill -36 202 22 -36 202 22 minecraft:red_sand
fill -30 201 22 -30 201 24 minecraft:sandstone
fill -30 202 22 -30 202 24 minecraft:red_sand
fill -36 201 25 -35 201 25 minecraft:sandstone
fill -36 202 25 -35 202 25 minecraft:red_sand
fill -36 201 38 -31 205 38 minecraft:smooth_red_sandstone
fill -36 206 38 -31 206 38 minecraft:red_sand
fill -37 201 23 -37 207 24 minecraft:smooth_red_sandstone
fill -37 208 23 -37 208 24 minecraft:red_sand
fill -36 201 24 -36 207 24 minecraft:smooth_red_sandstone
fill -36 208 24 -36 208 24 minecraft:red_sand
fill -36 201 23 -36 207 23 minecraft:terracotta
fill -36 208 23 -36 208 23 minecraft:red_sand
execute positioned -30 202 25 run function rlk:room/prop/sd_dry
execute positioned -32 203 21 run function rlk:room/prop/sd_dry
execute positioned -23 201 24 run function rlk:room/prop/sd_dry
execute positioned -27 201 26 run function rlk:room/prop/sd_dry
execute positioned -33 201 33 run function rlk:room/prop/sd_dry
execute positioned -26 201 35 run function rlk:room/prop/sd_dry
execute positioned -33 201 30 run function rlk:room/prop/sd_dry
setblock -36 207 38 minecraft:dead_bush keep
setblock -35 207 38 minecraft:dead_bush keep
setblock -32 207 38 minecraft:dead_bush keep
setblock -31 207 38 minecraft:dead_bush keep
